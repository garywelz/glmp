#!/usr/bin/env python3
"""
GLMP Hybridization Pipeline
============================
Applies RegulonDB backbone alignment, topology classification, and consistency
normalization to the 108-chart GLMP database.

Three stages:
  1. ANALYZE  — Parse all charts, classify topology, check consistency, identify
                RegulonDB-relevant genes. Produces a report (no changes).
  2. HYBRIDIZE — For E. coli charts, generate V2 hybrid Mermaid using RegulonDB
                 backbone + LLM. Requires --regulondb-network and --api-key.
  3. APPLY     — Write V2 JSONs to processes_v2/ with changelog and metadata.

Usage:
  python3 glmp_hybridization_pipeline.py analyze
  python3 glmp_hybridization_pipeline.py analyze --output report.json
  python3 glmp_hybridization_pipeline.py hybridize --regulondb-network /path/to/NetworkRegulatorGene.tsv --api-key sk-...
  python3 glmp_hybridization_pipeline.py apply --hybridized-dir /path/to/staged/

Requires: the GLMP processes directory and optionally RegulonDB flat files.
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────

PROCESSES_DIR = Path(
    "/home/gdubs/copernicus-web-public/huggingface-space/"
    "glmp-processes-database/processes"
)
V2_DIR = Path(
    "/home/gdubs/copernicus-web-public/huggingface-space/"
    "glmp-processes-database/processes_v2"
)
STAGING_DIR = Path("/home/gdubs/progframe/glmp_v2_staging")

# ── GLMP Color Palette (canonical) ────────────────────────────────────────────

GLMP_COLORS = {
    "trigger":      {"hex": "#e74c3c", "fg": "#fff", "role": "Triggers & Inputs"},
    "structure":    {"hex": "#ffd43b", "fg": "#000", "role": "Structures & Objects (TFs, proteins)"},
    "processing":   {"hex": "#51cf66", "fg": "#fff", "role": "Processing & Operations"},
    "intermediate": {"hex": "#74c0fc", "fg": "#000", "role": "Intermediates & States"},
    "product":      {"hex": "#b197fc", "fg": "#fff", "role": "Products & Outputs"},
    "or_gate":      {"hex": "#ff9f43", "fg": "#fff", "role": "OR Logic Gates (decisions)"},
    "and_gate":     {"hex": "#b4b4dc", "fg": "#000", "role": "AND Logic Gates"},
    "not_gate":     {"hex": "#e74c3c", "fg": "#fff", "role": "NOT Logic Gates (repression)"},
}

VALID_FILL_COLORS = {c["hex"].lower() for c in GLMP_COLORS.values()}


# ── Mermaid Parsing (adapted from count_flowchart_loops.py) ───────────────────

def parse_mermaid_to_graph(mermaid: str):
    """Parse Mermaid flowchart into (nodes: set, edges: list[(src, tgt, label)])."""
    nodes = set()
    edges = []

    lines = []
    for line in mermaid.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("%%") or stripped.startswith("style "):
            continue
        if stripped.startswith("graph ") or stripped.startswith("classDef "):
            continue
        if stripped.startswith("class "):
            continue
        lines.append(stripped)

    text = " ".join(lines)

    edge_pat = re.compile(
        r'([A-Za-z0-9_]+)'
        r'(?:\[[^\]]*\]|\{[^}]*\}|\([^)]*\))?'
        r'\s*-->\s*'
        r'(?:\|([^|]*)\|\s*)?'
        r'([A-Za-z0-9_]+)'
        r'(?:\[[^\]]*\]|\{[^}]*\}|\([^)]*\))?'
    )

    for m in edge_pat.finditer(text):
        src, label, tgt = m.group(1), m.group(2) or "", m.group(3)
        nodes.add(src)
        nodes.add(tgt)
        edges.append((src, tgt, label.strip()))

    return nodes, edges


def extract_node_labels(mermaid: str) -> dict:
    """Extract node_id -> label text from Mermaid source."""
    labels = {}
    for pattern in [
        r'([A-Za-z0-9_]+)\[([^\]]+)\]',
        r'([A-Za-z0-9_]+)\{([^}]+)\}',
        r'([A-Za-z0-9_]+)\(([^)]+)\)',
    ]:
        for m in re.finditer(pattern, mermaid):
            nid = m.group(1).strip()
            text = m.group(2).strip()
            if nid and text and not text.startswith("%"):
                text = re.sub(r'<br\s*/?>', ' ', text, flags=re.IGNORECASE)
                text = text.strip("/ \\")
                labels[nid] = text
    return labels


def extract_style_colors(mermaid: str) -> dict:
    """Extract node_id -> fill color hex from style lines."""
    colors = {}
    for m in re.finditer(r'style\s+([A-Za-z0-9_]+)\s+fill:(#[0-9a-fA-F]{6})', mermaid):
        colors[m.group(1)] = m.group(2).lower()
    return colors


# ── Topology Classification ───────────────────────────────────────────────────

def compute_layers(nodes, edges):
    """BFS layering from source nodes (in-degree 0)."""
    in_deg = defaultdict(int)
    out_adj = defaultdict(list)
    for u, v, _ in edges:
        out_adj[u].append(v)
        in_deg[v] += 1
    for n in nodes:
        in_deg.setdefault(n, 0)

    layer = {}
    sources = [n for n in nodes if in_deg[n] == 0]
    if sources:
        q = deque((s, 0) for s in sources)
        while q:
            u, d = q.popleft()
            if u in layer:
                continue
            layer[u] = d
            for v in out_adj[u]:
                if v not in layer:
                    q.append((v, d + 1))

    unreachable = [n for n in nodes if n not in layer]
    while unreachable:
        start = min(unreachable)
        q = deque([(start, 0)])
        while q:
            u, d = q.popleft()
            if u in layer:
                continue
            layer[u] = d
            for v in out_adj[u]:
                if v not in layer:
                    q.append((v, d + 1))
        unreachable = [n for n in nodes if n not in layer]

    return layer


def find_back_edges(nodes, edges, layer):
    """Return list of back-edges (u, v, label) where layer[u] >= layer[v]."""
    back = []
    for u, v, label in edges:
        if u == v:
            back.append((u, v, label))
        elif u in layer and v in layer and layer[u] >= layer[v]:
            back.append((u, v, label))
    return back


def find_cycles(nodes, edges):
    """Find all strongly connected components with >1 node (i.e., real cycles)."""
    adj = defaultdict(list)
    for u, v, _ in edges:
        adj[u].append(v)

    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    on_stack = set()
    sccs = []

    def strongconnect(v):
        index[v] = index_counter[0]
        lowlink[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack.add(v)

        for w in adj[v]:
            if w not in index:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], index[w])

        if lowlink[v] == index[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                scc.append(w)
                if w == v:
                    break
            if len(scc) > 1:
                sccs.append(set(scc))

    for n in nodes:
        if n not in index:
            strongconnect(n)

    return sccs


def classify_feedback_type(back_edges, node_labels):
    """
    Heuristic classification of feedback edges based on label keywords.
    Returns set of types found: {'negative', 'positive', 'mixed', 'unknown'}
    """
    types = set()
    neg_keywords = {"repress", "inhibit", "block", "negative", "depletion", "reduced", "down"}
    pos_keywords = {"activat", "positive", "enhanc", "amplif", "upregulat", "stimulat"}

    for u, v, label in back_edges:
        label_lower = label.lower() if label else ""
        u_label = (node_labels.get(u, "") + " " + label_lower).lower()
        v_label = (node_labels.get(v, "") + " " + label_lower).lower()
        combined = u_label + " " + v_label

        is_neg = any(k in combined for k in neg_keywords)
        is_pos = any(k in combined for k in pos_keywords)

        if is_neg and is_pos:
            types.add("mixed")
        elif is_neg:
            types.add("negative")
        elif is_pos:
            types.add("positive")
        else:
            types.add("unknown")

    return types


def classify_topology(mermaid: str) -> dict:
    """
    Classify a chart's topology per the five-class complexity ladder.
    Returns dict with class (I-V), details, counts.
    """
    nodes, edges = parse_mermaid_to_graph(mermaid)
    labels = extract_node_labels(mermaid)
    layer = compute_layers(nodes, edges)
    back_edges = find_back_edges(nodes, edges, layer)
    cycles = find_cycles(nodes, edges)
    feedback_types = classify_feedback_type(back_edges, labels) if back_edges else set()

    has_and = bool(re.search(r'\{.*AND', mermaid, re.IGNORECASE))
    has_or = bool(re.search(r'\{.*(?:OR|Is\s+\w+\s+\w+\?)', mermaid, re.IGNORECASE))

    and_count = len(re.findall(r'\{[^}]*AND[^}]*\}', mermaid, re.IGNORECASE))
    or_count = len(re.findall(r'\{[^}]*(?:Is\s|OR)[^}]*\}', mermaid, re.IGNORECASE))

    epigenetic_keywords = {"epigenet", "methylat", "chromatin", "histone", "acetylat",
                           "silenc", "imprint"}
    mermaid_lower = mermaid.lower()
    has_epigenetic = any(k in mermaid_lower for k in epigenetic_keywords)

    if not back_edges:
        complexity_class = "I"
        class_name = "Feed-forward only"
    elif feedback_types <= {"negative", "unknown"} and not has_epigenetic:
        complexity_class = "II"
        class_name = "Negative feedback (damped regulation)"
    elif "positive" in feedback_types and "negative" not in feedback_types:
        complexity_class = "III"
        class_name = "Positive feedback (bistable switches)"
    elif has_epigenetic:
        complexity_class = "V"
        class_name = "Self-modifying / epigenetic feedback"
    else:
        if len(back_edges) >= 2 or len(cycles) >= 2:
            complexity_class = "IV"
            class_name = "Mixed feedback (oscillators)"
        else:
            complexity_class = "III"
            class_name = "Positive feedback (bistable switches)"

    return {
        "complexity_class": complexity_class,
        "class_name": class_name,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "back_edge_count": len(back_edges),
        "cycle_count": len(cycles),
        "feedback_types": sorted(feedback_types),
        "and_gates": and_count,
        "or_gates": or_count,
        "has_epigenetic_keywords": has_epigenetic,
    }


# ── Consistency Checks ────────────────────────────────────────────────────────

def check_consistency(mermaid: str, process_id: str) -> list:
    """Check color scheme compliance, diamond shapes for gates, etc."""
    issues = []

    style_colors = extract_style_colors(mermaid)
    for nid, color in style_colors.items():
        if color not in VALID_FILL_COLORS:
            issues.append({
                "type": "non_standard_color",
                "node": nid,
                "color": color,
                "process": process_id,
            })

    labels = extract_node_labels(mermaid)
    gate_keywords = {"AND", "OR", "Is "}
    for nid, label in labels.items():
        is_gate = any(k in label for k in gate_keywords)
        is_diamond = bool(re.search(rf'{nid}\{{', mermaid))
        if is_gate and not is_diamond:
            issues.append({
                "type": "gate_not_diamond",
                "node": nid,
                "label": label,
                "process": process_id,
            })

    feedback_pat = re.compile(r'-->.*feedback', re.IGNORECASE)
    nodes, edges = parse_mermaid_to_graph(mermaid)
    layer = compute_layers(nodes, edges)
    back_edges = find_back_edges(nodes, edges, layer)
    if back_edges:
        has_labeled_feedback = bool(feedback_pat.search(mermaid))
        unlabeled_back = [
            (u, v) for u, v, lbl in back_edges
            if not lbl and u != v
        ]
        if unlabeled_back and not has_labeled_feedback:
            issues.append({
                "type": "unlabeled_feedback_edges",
                "edges": [(u, v) for u, v in unlabeled_back[:5]],
                "process": process_id,
            })

    return issues


# ── RegulonDB Loading ─────────────────────────────────────────────────────────

def load_regulondb_network(path: str) -> list:
    """
    Load RegulonDB NetworkRegulatorGene.tsv.
    Returns list of (regulator_gene, regulated_gene, effect).
    """
    edges = []
    with open(path) as f:
        raw = [line.strip() for line in f if line.strip()]

    lines = [ln for ln in raw if not ln.startswith("#")]
    if not lines:
        return edges

    header = lines[0].lower().split("\t")
    norm = [h.split(")")[-1].strip() for h in header]

    def find_col(*names):
        for n in names:
            for i, h in enumerate(norm):
                if n in h:
                    return i
        return None

    idx_reg = find_col("regulatorgenename", "regulatorname", "regulator")
    idx_tgt = find_col("regulatedname", "regulated", "gene")
    idx_eff = find_col("function", "effect")
    if idx_reg is None:
        idx_reg = 0
    if idx_tgt is None:
        idx_tgt = 1

    for line in lines[1:]:
        parts = line.split("\t")
        if len(parts) <= max(idx_reg, idx_tgt):
            continue
        reg = parts[idx_reg].strip().lower()
        tgt = parts[idx_tgt].strip().lower()
        eff = parts[idx_eff].strip() if idx_eff is not None and len(parts) > idx_eff else ""
        if reg and tgt:
            edges.append((reg, tgt, eff))
    return edges


def extract_gene_names_from_chart(mermaid: str) -> set:
    """
    Extract plausible E. coli gene names from a Mermaid chart.
    Looks for common patterns: lacI, lacZ, crp, recA, lexA, ompR, envZ, etc.
    """
    gene_pat = re.compile(r'\b([a-z]{3,4}[A-Z0-9]?)\b')
    candidates = set()
    for m in gene_pat.finditer(mermaid):
        candidates.add(m.group(1).lower())

    label_pat = re.compile(r'\b([A-Z][a-z]{2,3}[A-Z])\b')
    for m in label_pat.finditer(mermaid):
        candidates.add(m.group(1).lower())

    return candidates


def find_missing_regulondb_edges(mermaid: str, regulondb_edges: list,
                                  process_genes: set) -> list:
    """
    Find RegulonDB edges relevant to this chart's genes that are not in the Mermaid.
    Returns list of (regulator, regulated, effect) that are missing.
    """
    relevant = [
        (r, t, e) for r, t, e in regulondb_edges
        if r in process_genes and t in process_genes
    ]

    mermaid_lower = mermaid.lower()
    missing = []
    for reg, tgt, eff in relevant:
        if reg not in mermaid_lower or tgt not in mermaid_lower:
            continue
        missing.append((reg, tgt, eff))

    return missing


# ── Analysis Stage ────────────────────────────────────────────────────────────

def load_all_charts(processes_dir: Path) -> list:
    """Load all process JSONs (excluding metadata.json and .backup files)."""
    charts = []
    for f in sorted(processes_dir.glob("*.json")):
        if f.name == "metadata.json" or f.name.endswith(".backup"):
            continue
        try:
            data = json.loads(f.read_text())
            data["_filename"] = f.name
            data["_process_id"] = f.stem
            charts.append(data)
        except Exception as e:
            print(f"  Warning: could not load {f.name}: {e}", file=sys.stderr)
    return charts


def run_analyze(processes_dir: Path, regulondb_path: str = None,
                output_path: str = None):
    """Stage 1: Analyze all charts — topology, consistency, RegulonDB coverage."""
    print(f"Loading charts from {processes_dir} ...")
    charts = load_all_charts(processes_dir)
    print(f"  Loaded {len(charts)} charts\n")

    regulondb_edges = []
    if regulondb_path and os.path.isfile(regulondb_path):
        regulondb_edges = load_regulondb_network(regulondb_path)
        print(f"Loaded RegulonDB network: {len(regulondb_edges)} edges\n")

    report = {
        "generated": datetime.utcnow().isoformat() + "Z",
        "total_charts": len(charts),
        "organisms": {},
        "topology_distribution": defaultdict(int),
        "consistency_issues_total": 0,
        "charts": [],
    }

    for chart in charts:
        pid = chart["_process_id"]
        organism = chart.get("organism", "unknown")
        mermaid = chart.get("mermaid", "")

        if organism not in report["organisms"]:
            report["organisms"][organism] = 0
        report["organisms"][organism] += 1

        if not mermaid or not mermaid.strip():
            report["charts"].append({
                "process_id": pid,
                "organism": organism,
                "error": "no mermaid content",
            })
            continue

        topo = classify_topology(mermaid)
        issues = check_consistency(mermaid, pid)
        report["topology_distribution"][topo["complexity_class"]] += 1
        report["consistency_issues_total"] += len(issues)

        chart_report = {
            "process_id": pid,
            "organism": organism,
            "name": chart.get("name", ""),
            "topology": topo,
            "consistency_issues": issues,
        }

        if organism == "E. coli" and regulondb_edges:
            genes = extract_gene_names_from_chart(mermaid)
            missing = find_missing_regulondb_edges(mermaid, regulondb_edges, genes)
            chart_report["regulondb_gene_matches"] = len(genes)
            chart_report["regulondb_missing_edges"] = [
                {"regulator": r, "regulated": t, "effect": e}
                for r, t, e in missing[:20]
            ]

        report["charts"].append(chart_report)

    report["topology_distribution"] = dict(report["topology_distribution"])

    print("=" * 65)
    print("GLMP HYBRIDIZATION PIPELINE — ANALYSIS REPORT")
    print("=" * 65)
    print(f"\nTotal charts: {report['total_charts']}")
    print(f"Organisms: {json.dumps(report['organisms'], indent=2)}")
    print(f"\nTopology distribution (five-class ladder):")
    class_names = {
        "I": "Feed-forward only",
        "II": "Negative feedback",
        "III": "Positive feedback / bistable",
        "IV": "Mixed feedback / oscillators",
        "V": "Self-modifying / epigenetic",
    }
    for cls in ["I", "II", "III", "IV", "V"]:
        count = report["topology_distribution"].get(cls, 0)
        name = class_names.get(cls, "")
        bar = "█" * count
        print(f"  Class {cls} ({name}): {count}  {bar}")

    print(f"\nConsistency issues found: {report['consistency_issues_total']}")

    issue_types = defaultdict(int)
    for c in report["charts"]:
        for iss in c.get("consistency_issues", []):
            issue_types[iss["type"]] += 1
    if issue_types:
        for t, cnt in sorted(issue_types.items()):
            print(f"  {t}: {cnt}")

    if regulondb_edges:
        ecoli_charts = [c for c in report["charts"] if c.get("organism") == "E. coli"]
        with_missing = [c for c in ecoli_charts if c.get("regulondb_missing_edges")]
        print(f"\nRegulonDB analysis (E. coli charts only):")
        print(f"  E. coli charts: {len(ecoli_charts)}")
        print(f"  Charts with potential missing RegulonDB edges: {len(with_missing)}")

    if output_path:
        Path(output_path).write_text(json.dumps(report, indent=2))
        print(f"\nFull report written to: {output_path}")

    print()
    return report


# ── Hybridization Prompt ──────────────────────────────────────────────────────

HYBRIDIZATION_SYSTEM_PROMPT = """\
You are a molecular biology expert helping to improve gene regulatory flowcharts.
You will receive:
1. An existing Mermaid flowchart (V1) of an E. coli regulatory process
2. A set of regulatory edges from RegulonDB (regulator → regulated gene, effect +/-)

Your task: produce an improved V2 Mermaid flowchart that:
- PRESERVES all existing AND/OR logic gates, feedback loops, and logical structure
- PRESERVES all existing node IDs and style lines
- ADDS any molecular entities (TF expression steps, autoregulatory loops, missing
  regulator→gene edges) that RegulonDB shows but V1 omits
- Uses the SAME color scheme (add style lines for new nodes matching the palette)
- Adds a comment line for each RegulonDB-sourced addition: %% RegulonDB: [description]
- Does NOT remove or rename existing nodes
- Does NOT change the graph direction (TD/LR)

Color palette for new nodes:
- Triggers/inputs: fill:#e74c3c,color:#fff
- TFs/proteins: fill:#ffd43b,color:#000
- Processing: fill:#51cf66,color:#fff
- Intermediates: fill:#74c0fc,color:#000
- Products: fill:#b197fc,color:#fff
- AND gates: fill:#b4b4dc,color:#000
- OR gates: fill:#ff9f43,color:#fff

Return ONLY the complete Mermaid source (graph TD ... style lines), no explanation."""


def build_hybridization_prompt(v1_mermaid: str, process_name: str,
                                regulondb_edges: list) -> str:
    """Build the user prompt for hybridization."""
    edges_text = "\n".join(
        f"  {r} → {t} (effect: {e})" for r, t, e in regulondb_edges
    )
    return f"""Process: {process_name}

## Existing V1 Mermaid flowchart:

```mermaid
{v1_mermaid}
```

## RegulonDB regulatory edges relevant to this process:

{edges_text}

Please produce the V2 hybrid Mermaid flowchart following the instructions above."""


# ── Hybridization Stage ──────────────────────────────────────────────────────

def run_hybridize(processes_dir: Path, regulondb_path: str,
                   staging_dir: Path, api_key: str = None,
                   dry_run: bool = False):
    """
    Stage 2: Generate V2 hybrids for E. coli charts.
    If --dry-run, just produces the prompts without calling the API.
    """
    print(f"Loading charts from {processes_dir} ...")
    charts = load_all_charts(processes_dir)
    ecoli = [c for c in charts if c.get("organism") == "E. coli"]
    print(f"  {len(ecoli)} E. coli charts to hybridize\n")

    regulondb_edges = load_regulondb_network(regulondb_path)
    print(f"Loaded RegulonDB: {len(regulondb_edges)} edges\n")

    regulondb_by_gene = defaultdict(list)
    for r, t, e in regulondb_edges:
        regulondb_by_gene[r].append((r, t, e))
        regulondb_by_gene[t].append((r, t, e))

    staging_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir = staging_dir / "prompts"
    prompts_dir.mkdir(exist_ok=True)

    for chart in ecoli:
        pid = chart["_process_id"]
        mermaid = chart.get("mermaid", "")
        if not mermaid:
            continue

        genes = extract_gene_names_from_chart(mermaid)
        relevant_edges = set()
        for g in genes:
            for edge in regulondb_by_gene.get(g, []):
                if edge[0] in genes or edge[1] in genes:
                    relevant_edges.add(edge)

        relevant_edges = sorted(relevant_edges)

        if not relevant_edges:
            print(f"  {pid}: no RegulonDB edges found for chart genes, skipping")
            continue

        prompt = build_hybridization_prompt(
            mermaid, chart.get("name", pid), relevant_edges
        )

        prompt_file = prompts_dir / f"{pid}_prompt.txt"
        prompt_file.write_text(prompt)

        if dry_run:
            print(f"  {pid}: prompt saved ({len(relevant_edges)} RegulonDB edges)")
            continue

        if not api_key:
            print(f"  {pid}: prompt saved; no API key, skipping LLM call")
            continue

        print(f"  {pid}: calling LLM ({len(relevant_edges)} RegulonDB edges) ...")
        v2_mermaid = call_llm_for_hybridization(
            HYBRIDIZATION_SYSTEM_PROMPT, prompt, api_key
        )

        if v2_mermaid:
            result = {
                **chart,
                "mermaid": v2_mermaid,
                "regulondb_backbone": True,
                "regulondb_version": "v13",
                "changelog_v2": (
                    f"V2 aligned with RegulonDB: {len(relevant_edges)} "
                    f"regulatory edges checked. Generated {datetime.utcnow().isoformat()}Z."
                ),
            }
            result.pop("_filename", None)
            result.pop("_process_id", None)

            out_file = staging_dir / f"{pid}.json"
            out_file.write_text(json.dumps(result, indent=2))
            print(f"    → saved to {out_file}")
        else:
            print(f"    → LLM returned empty; skipping")

    print(f"\nStaged V2 charts in: {staging_dir}")
    print("Review these before running 'apply'.")


def call_llm_for_hybridization(system_prompt: str, user_prompt: str,
                                api_key: str) -> str:
    """
    Call Anthropic Claude API to generate V2 hybrid Mermaid.
    Returns the Mermaid source string, or empty string on failure.
    """
    try:
        import anthropic
    except ImportError:
        print("ERROR: pip install anthropic  (required for LLM calls)")
        return ""

    client = anthropic.Anthropic(api_key=api_key)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8192,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = response.content[0].text

        mermaid_match = re.search(r'```(?:mermaid)?\s*\n(.*?)```', text, re.DOTALL)
        if mermaid_match:
            return mermaid_match.group(1).strip()
        if text.strip().startswith("graph"):
            return text.strip()
        return text.strip()
    except Exception as e:
        print(f"  LLM error: {e}", file=sys.stderr)
        return ""


# ── Apply Stage ───────────────────────────────────────────────────────────────

def run_apply(staging_dir: Path, v2_dir: Path):
    """Stage 3: Copy reviewed V2 JSONs from staging to processes_v2/."""
    if not staging_dir.exists():
        print(f"Staging dir not found: {staging_dir}")
        sys.exit(1)

    v2_dir.mkdir(parents=True, exist_ok=True)

    staged = sorted(staging_dir.glob("*.json"))
    if not staged:
        print("No staged V2 JSONs found.")
        return

    print(f"Applying {len(staged)} V2 charts to {v2_dir} ...")
    for f in staged:
        dest = v2_dir / f.name
        data = json.loads(f.read_text())

        topo = classify_topology(data.get("mermaid", ""))
        data["topology_class"] = topo["complexity_class"]
        data["topology_class_name"] = topo["class_name"]
        data["lastUpdated"] = datetime.utcnow().strftime("%Y-%m-%d")

        dest.write_text(json.dumps(data, indent=2))
        print(f"  {f.name} → {dest}")

    print(f"\nDone. {len(staged)} V2 charts written to {v2_dir}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="GLMP Hybridization Pipeline: analyze, hybridize, apply",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # analyze
    p_analyze = sub.add_parser("analyze", help="Analyze all charts (no changes)")
    p_analyze.add_argument("--processes-dir", type=Path, default=PROCESSES_DIR)
    p_analyze.add_argument("--regulondb-network", type=str, default=None,
                           help="Path to RegulonDB NetworkRegulatorGene.tsv")
    p_analyze.add_argument("--output", type=str, default=None,
                           help="Write JSON report to this path")

    # hybridize
    p_hyb = sub.add_parser("hybridize", help="Generate V2 hybrids for E. coli charts")
    p_hyb.add_argument("--processes-dir", type=Path, default=PROCESSES_DIR)
    p_hyb.add_argument("--regulondb-network", type=str, required=True)
    p_hyb.add_argument("--staging-dir", type=Path, default=STAGING_DIR)
    p_hyb.add_argument("--api-key", type=str, default=None,
                       help="Anthropic API key (or set ANTHROPIC_API_KEY env var)")
    p_hyb.add_argument("--dry-run", action="store_true",
                       help="Generate prompts only, don't call LLM")

    # apply
    p_apply = sub.add_parser("apply", help="Copy staged V2 charts to processes_v2/")
    p_apply.add_argument("--staging-dir", type=Path, default=STAGING_DIR)
    p_apply.add_argument("--v2-dir", type=Path, default=V2_DIR)

    args = parser.parse_args()

    if args.command == "analyze":
        run_analyze(args.processes_dir, args.regulondb_network, args.output)
    elif args.command == "hybridize":
        api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        run_hybridize(args.processes_dir, args.regulondb_network,
                      args.staging_dir, api_key, args.dry_run)
    elif args.command == "apply":
        run_apply(args.staging_dir, args.v2_dir)


if __name__ == "__main__":
    main()
