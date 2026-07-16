#!/usr/bin/env python3
"""Stage-2 cycle-edge typing under rubric v2. Sidecar only. Do not commit."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from mermaid_graph import (  # noqa: E402
    parse_mermaid,
    _enumerate_simple_cycles,
    _unique_edges,
)

HARVEST = Path(__file__).resolve().parent
PROCESSES = ROOT / "glmp-v2" / "processes"
OUT = HARVEST / "cycle_edge_types.tsv"
COLS = [
    "chart_id",
    "source_id",
    "source_label",
    "target_id",
    "target_label",
    "edge_label",
    "edge_type",
    "confidence",
    "rule_applied",
    "rationale",
]

PILOT_FILES = [
    HARVEST / "pilot_edge_types.retyped.tsv",
    HARVEST / "pilot_edge_types_round2.retyped.tsv",
]

BAR = "\u22a3"  # ⊣
MINUS = "\u2212"  # −

NODE_DECL_RE = re.compile(
    r"(?P<id>[A-Za-z][A-Za-z0-9_]*)\s*"
    r"(?P<label>"
    r'\["[^"]*"\]|\[[^\]]*\]|'
    r'\("[^"]*"\)|\([^)]*\)|'
    r"\{[^}]*\}|"
    r"/\[[^\]]*\]/|"
    r"\[\[[^\]]*\]\]|"
    r">[^|]*\|"
    r")"
)

EDGE_LINE_RE = re.compile(
    r"(?P<src>[A-Za-z][A-Za-z0-9_]*)"
    r"(?:\s*(?:\[[^\]]*\]|\([^)]*\)|\{[^}]*\}|/\[[^\]]*\]/))*"
    r"\s*(?P<arrow>"
    r"<-->|<==>|x--x|o--o|"
    r"-\.-+\>|-\.-+|"
    r"==+\>|==+|"
    r"--+\>|--+|"
    r"--[xo]|[ox]--"
    r")"
    r"(?:\|(?P<elab>[^|]*)\|)?"
    r"\s*(?P<tgt>[A-Za-z][A-Za-z0-9_]*)"
)

OUTCOME_TOKENS = (
    "yes",
    "no",
    "passed",
    "failed",
    "high",
    "low",
    "active",
    "inactive",
    "true",
    "false",
    "on",
    "off",
    "present",
    "absent",
    "sufficient",
    "insufficient",
    "ok",
    "not ok",
    "continuous",
    "better",
    "worse",
    "favorable",
    "unfavorable",
    "correct",
    "mismatch",
    "none",
    "permissive",
    "random",
    "equilibrium",
    "incomplete",
    "unstable",
    "missing",
    "initiate",
    "coordinated",
)


def load_pilots() -> set[str]:
    pilots: set[str] = set()
    for fn in PILOT_FILES:
        with fn.open(encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                pilots.add(r["chart_id"])
    return pilots


def chart_path(cid: str) -> Path:
    hits = list(PROCESSES.rglob(f"{cid}.json"))
    if not hits:
        raise FileNotFoundError(cid)
    return hits[0]


def clean_label(raw: str) -> str:
    s = (raw or "").strip()
    for _ in range(3):
        if len(s) >= 2 and s[0] in "[{(/<" and s[-1] in "]})>/":
            s = s[1:-1]
        elif len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            s = s[1:-1]
        else:
            break
    return s.strip().strip("/").replace("\\", "").strip()


def node_meta(mermaid: str) -> dict[str, dict]:
    meta: dict[str, dict] = {}
    for m in NODE_DECL_RE.finditer(mermaid):
        nid = m.group("id")
        raw = m.group("label")
        if nid in meta:
            continue
        lab = clean_label(raw)
        is_dec = raw.startswith("{") or lab.endswith("?")
        meta[nid] = {"label": lab, "shape_raw": raw, "is_decision": is_dec}
    return meta


def parse_edge_instances(mermaid: str) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for raw in (mermaid or "").splitlines():
        s = raw.strip()
        if not s or s.startswith("%%"):
            continue
        pos = 0
        while True:
            m = EDGE_LINE_RE.search(s, pos)
            if not m:
                break
            elab = (m.group("elab") or "").strip()
            out.append((m.group("src"), m.group("tgt"), elab))
            pos = m.start("tgt")
    return out


def cycle_edge_set(mermaid: str) -> set[tuple[str, str]]:
    _, edges = parse_mermaid(mermaid)
    edges = _unique_edges(edges)
    cycles, capped = _enumerate_simple_cycles(edges)
    if capped:
        raise RuntimeError("cycle enumeration capped")
    cyc: set[tuple[str, str]] = set()
    for c in cycles:
        for i in range(len(c)):
            cyc.add((c[i], c[(i + 1) % len(c)]))
    return cyc


def is_outcome_branch(elab: str) -> bool:
    """Rule 2 keys on structure: any non-empty edge label from a decision node."""
    return bool((elab or "").strip())


def branch_polarity(elab: str, tgt: str) -> str | None:
    """
    Return activates/represses, or None if polarity is genuinely unclear.
    Gate path-selection labels (σ70, Path 1, …) enable their target -> activates.
    """
    el = (elab or "").strip().lower()
    tl = (tgt or "").lower()
    if not el:
        return None

    if el.startswith("inactive") or el.startswith("phosphorylated"):
        if any(w in tl for w in ("inactive", "repress", "no ", "block", "stall", "off")):
            return "activates"
        if any(w in tl for w in ("induct", "onset", "start", "enable", "active")):
            return "activates"
        return "represses"

    if el.startswith("active"):
        return "activates"

    permit_prefixes = (
        "passed",
        "yes",
        "high",
        "true",
        "on",
        "present",
        "sufficient",
        "ok",
        "continuous",
        "better",
        "favorable",
        "correct",
        "permissive",
        "initiate",
        "coordinated",
        "equilibrium",
        "random",
        "team",
        "chain",
    )
    block_prefixes = (
        "failed",
        "no",
        "low",
        "false",
        "off",
        "absent",
        "insufficient",
        "not ok",
        "worse",
        "unfavorable",
        "mismatch",
        "none",
        "incomplete",
        "missing",
        "not found",
    )
    block_words = (
        "unstable",
        "incomplete",
        "mismatch",
        "missing",
        "failed",
        "block",
        "stall",
        "absent",
        "worse",
        "unfavorable",
        "not found",
    )

    if any(el.startswith(p) for p in permit_prefixes) or "present" in el:
        return "activates"
    if any(el.startswith(p) for p in block_prefixes) or any(w in el for w in block_words):
        # fail-branch into a wait/block/restart sink enables that sink
        if any(
            w in tl
            for w in ("stall", "block", "arrest", "inactive", "repress", "wait", "no ", "disassembly", "restart")
        ):
            return "activates"
        return "represses"
    # path-selection / named branch (σ70, Path 1, RecFOR, …): enables target
    return "activates"


def is_expression_event(lab: str) -> bool:
    sl = (lab or "").lower()
    return bool(
        sl.startswith("upregulation of ")
        or sl.startswith("derepression of ")
        or sl.startswith("downregulation of ")
        or (sl.startswith("increased ") and "gene" in sl)
        or (sl.startswith("decreased ") and "gene" in sl)
        or sl.endswith(" transcription")
        or sl.endswith(" gene expression")
        or " transcription of " in sl
    )


def expression_own_product(src: str, tgt: str) -> bool:
    s, t = (src or "").strip(), (tgt or "").strip()
    sl, tl = s.lower(), t.lower()
    if sl.startswith("transcriptional derepression by ") or sl.startswith(
        "transcriptional repression by "
    ):
        return False
    if not is_expression_event(s):
        return False
    tokens: list[str] = []
    m = re.match(r"(?:upregulation|derepression|downregulation) of (.+)", sl)
    if m:
        x = re.split(r"[\(/,;]", m.group(1))[0].strip()
        tokens = [w for w in re.split(r"[^a-z0-9]+", x) if len(w) >= 3]
    else:
        m2 = re.match(r"(?:increased|decreased) (.+?) genes?", sl)
        if m2:
            tokens = [w for w in re.split(r"[^a-z0-9]+", m2.group(1)) if len(w) >= 3]
        else:
            m3 = re.search(r"transcription of (.+)", sl)
            if m3:
                tokens = [w for w in re.split(r"[^a-z0-9]+", m3.group(1)) if len(w) >= 3]
    if not tokens:
        return False
    return any(tok in tl for tok in tokens)


def words12(s: str) -> str:
    return " ".join(s.split()[:12])


def type_edge(
    src_lab: str,
    tgt_lab: str,
    elab: str,
    src_is_dec: bool,
    tgt_is_dec: bool,
) -> tuple[str, str, str, str]:
    sl = (src_lab or "").lower()
    tl = (tgt_lab or "").lower()
    el = (elab or "").strip()
    ell = el.lower()

    # RULE 1 — explicit markers
    if (
        BAR in el
        or MINUS in el
        or ell in {"-|", "--o", "x", "inhibit", "inhibits", "represses"}
        or re.match(r"^[-−]\s*feedback", ell)
    ):
        if "sequester" in sl or "sequester" in tl:
            return "sequesters", "high", "1", words12("Rule1 bar-head sequestration mechanism")
        return "represses", "high", "1", words12("Rule1 explicit bar-head inhibition")
    if (
        ell in {"+", "activates", "enhances", "enhance", "stimulates", "stimulate"}
        or ell.startswith("activates")
        or ell.startswith("+")
    ):
        return "activates", "high", "1", words12("Rule1 explicit Activates/+ marker")

    if re.search(r"\binhibit", ell) or re.search(r"\brepress", ell):
        return "represses", "high", "1", words12("Rule1 explicit inhibit/repress label")
    if re.search(r"\bactivat", ell) and not src_is_dec:
        return "activates", "high", "1", words12("Rule1 explicit activate label")

    # RULE 2 — STRUCTURE: decision node + any non-empty outcome label
    # (Yes/No/Passed/… list was illustrative; σ70, Path 1, Z-ring unstable all qualify)
    if src_is_dec and is_outcome_branch(el):
        pol = branch_polarity(el, tgt_lab)
        if pol is None:
            return "UNTYPABLE", "low", "2", words12("Rule2 gate but polarity unclear")
        return pol, "high", "2", words12(f"Rule2 gate outcome {el} -> {pol}")

    # RULE 3 — expression -> own machinery
    if expression_own_product(src_lab, tgt_lab):
        return "produces", "high", "3", words12("Rule3 expression yields own machinery")

    # Explicit material / structure verbs on edge label
    if ell in {
        "synthesize",
        "synthesis",
        "produce",
        "produces",
        "form",
        "forms",
        "generate",
        "generates",
    }:
        return "produces", "high", "none", words12("edge label is material production")
    if ell in {"requires", "require", "needs", "need"}:
        return "proceeds", "med", "none", words12("structural dependency advances assembly")

    # Cross-entity transcriptional control
    if sl.startswith("transcriptional derepression by ") or (
        "derepression by" in sl and "upregulation" in tl
    ):
        return "activates", "high", "none", words12("regulator controls different expression")
    if sl.startswith("transcriptional repression by "):
        return "represses", "high", "none", words12("regulator represses different expression")

    if any(
        w in sl
        for w in (
            "kinase",
            "phosphatase",
            "tf ",
            "transcription factor",
            "repressor",
            "activator",
            "receptor",
            "sensor",
        )
    ) and any(w in tl for w in ("activ", "phosphoryl", "induct", "express", "transcri")):
        if "repress" in tl or "inhibit" in tl or "inactiv" in tl:
            return "represses", "med", "none", words12("regulator drives inhibitory state")
        return "activates", "med", "none", words12("regulator changes target capacity")

    if "repress" in sl and ("gene" in tl or "express" in tl or "transcri" in tl):
        return "represses", "med", "none", words12("repression of expression")
    if "activat" in sl and (
        "complex" in tl or "pathway" in tl or "cascade" in tl or "response" in tl
    ):
        return "activates", "med", "none", words12("activation enables downstream process")

    if "sequester" in tl or "sequester" in sl:
        return "sequesters", "high", "none", words12("physical sequestration/binding")
    if ("bind" in sl or "binding" in sl) and (
        "stabiliz" in tl or "block" in tl or "inhibit" in tl
    ):
        if "stabiliz" in tl:
            return "activates", "med", "none", words12("binding stabilizes capacity")
        return "represses", "med", "none", words12("binding blocks capacity")

    signalish_src = any(
        w in sl
        for w in (
            "atp",
            "amp",
            "camp",
            "gtp",
            "calcium",
            "ca2",
            "iron",
            "phosphate",
            "nutrient",
            "starvation",
            "stress",
            "hormone",
            "ligand",
            "signal",
            "rapamycin",
            "glucose",
            "tryptophan",
            "amino acid",
        )
    )
    sensorish_tgt = any(
        w in tl
        for w in (
            "kinase",
            "receptor",
            "sensor",
            "ampk",
            "tor",
            "pka",
            "tf",
            "factor",
            "regulon",
            "response",
        )
    )
    if signalish_src and sensorish_tgt and not any(
        w in sl for w in ("synthesis", "production", "catabolism", "glycolysis")
    ):
        return "induces", "med", "none", words12("effector as signal to sensor")

    if any(
        w in sl
        for w in (
            "synthesis",
            "synthase",
            "production",
            "produces",
            "formation",
            "generated",
            "generation",
            "export",
            "uptake",
            "release",
            "catabolism",
            "biosynthesis",
        )
    ) and any(
        w in tl
        for w in (
            "pool",
            "product",
            "atp",
            "metabolite",
            "availability",
            "level",
            "concentration",
            "intermediate",
        )
    ):
        return "produces", "med", "none", words12("material production/appearance")

    if "conjugate" in tl or "assembled" in tl or "complex" in tl:
        if any(w in sl for w in ("enzyme", "atg", "subunit", "component", "binding")):
            return "produces", "med", "none", words12("assembly yields complex/product")

    if any(w in ell for w in ("phosphorylat", "acetylat", "ubiquitin", "methylat")) or any(
        w in sl for w in ("phosphorylat", "acetylat", "ubiquitin")
    ):
        return "modifies", "med", "none", words12("covalent modification event")

    if tgt_is_dec and not el:
        return "proceeds", "high", "none", words12("process feeds decision gate")
    if src_is_dec and not el:
        return "proceeds", "med", "none", words12("gate continues without outcome label")

    if any(
        w in sl or w in tl
        for w in (
            "cycle",
            "glycolysis",
            "tca",
            "pathway",
            "elongation",
            "initiation",
            "termination",
            "transport",
            "membrane",
            "vesicle",
            "phagophore",
            "autophagy",
            "replication",
            "translation",
            "transcription elongation",
            "recycling",
        )
    ):
        if "feedback" in ell or "inhibit" in tl:
            return "represses", "low", "none", words12("feedback/inhibit language weak")
        return "proceeds", "med", "none", words12("pathway/state advances")

    if el == "" or ell in {"next", "then", "to", "into"}:
        return "proceeds", "med", "none", words12("unlabeled process step")

    return "UNTYPABLE", "low", "none", words12(f"no rubric rule covers label {el!r}")


def list_remaining() -> list[tuple[str, int]]:
    pilots = load_pilots()
    remaining: list[tuple[str, int]] = []
    for p in sorted(PROCESSES.rglob("*.json")):
        cid = p.stem
        if cid in pilots:
            continue
        m = json.loads(p.read_text(encoding="utf-8")).get("mermaid") or ""
        if not m:
            continue
        try:
            cyc = cycle_edge_set(m)
        except RuntimeError:
            continue
        if cyc:
            remaining.append((cid, len(cyc)))
    remaining.sort(key=lambda x: x[0])
    return remaining


def already_done() -> set[str]:
    if not OUT.exists():
        return set()
    done: set[str] = set()
    with OUT.open(encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            done.add(r["chart_id"])
    return done


def type_chart(cid: str) -> list[dict]:
    m = json.loads(chart_path(cid).read_text(encoding="utf-8"))["mermaid"]
    meta = node_meta(m)
    order, _ = parse_mermaid(m)
    for nid in order:
        meta.setdefault(nid, {"label": nid, "shape_raw": "", "is_decision": False})
        if meta[nid]["label"].endswith("?"):
            meta[nid]["is_decision"] = True

    cyc = cycle_edge_set(m)
    instances = parse_edge_instances(m)
    label_map: dict[tuple[str, str], str] = {}
    for a, b, el in instances:
        if (a, b) in cyc and (a, b) not in label_map:
            label_map[(a, b)] = el

    rows: list[dict] = []
    for a, b in sorted(cyc):
        src_lab = meta.get(a, {}).get("label", a)
        tgt_lab = meta.get(b, {}).get("label", b)
        elab = label_map.get((a, b), "")
        src_dec = bool(meta.get(a, {}).get("is_decision"))
        tgt_dec = bool(meta.get(b, {}).get("is_decision"))
        et, conf, rule, rat = type_edge(src_lab, tgt_lab, elab, src_dec, tgt_dec)
        rows.append(
            {
                "chart_id": cid,
                "source_id": a,
                "source_label": src_lab,
                "target_id": b,
                "target_label": tgt_lab,
                "edge_label": elab,
                "edge_type": et,
                "confidence": conf,
                "rule_applied": rule,
                "rationale": rat,
            }
        )
    return rows


def append_rows(rows: list[dict]) -> None:
    new_file = not OUT.exists()
    with OUT.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, delimiter="\t", lineterminator="\n")
        if new_file:
            w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in COLS})


def report(batch_rows: list[dict], batch_charts: list[str], batch_num: int) -> None:
    all_rows: list[dict] = []
    if OUT.exists():
        with OUT.open(encoding="utf-8") as f:
            all_rows = list(csv.DictReader(f, delimiter="\t"))
    types = Counter(r["edge_type"] for r in batch_rows)
    confs = Counter(r["confidence"] for r in batch_rows)
    rules = Counter(r["rule_applied"] for r in batch_rows)
    untyp = types.get("UNTYPABLE", 0)
    n = len(batch_rows)
    print(f"=== BATCH {batch_num} GATE ===")
    print(f"charts done this batch: {len(batch_charts)}")
    for c in batch_charts:
        print(f"  - {c}")
    print(f"cycle edges typed this batch: {n}")
    print(
        f"running total edges: {len(all_rows)} across "
        f"{len({r['chart_id'] for r in all_rows})} charts"
    )
    print(f"type distribution: {dict(types)}")
    print(f"UNTYPABLE: {untyp}/{n} ({100 * untyp / n if n else 0:.1f}%)")
    print(f"confidence: {dict(confs)}")
    print(f"rule_applied: {dict(rules)}")
    by = defaultdict(list)
    for r in batch_rows:
        by[r["chart_id"]].append(r)
    flagged = []
    for cid, rs in by.items():
        u = sum(1 for r in rs if r["edge_type"] == "UNTYPABLE")
        if u / len(rs) > 0.30:
            flagged.append((cid, u, len(rs)))
    if flagged:
        print("charts with >30% UNTYPABLE:")
        for cid, u, tot in flagged:
            print(f"  {cid}: {u}/{tot} ({100 * u / tot:.0f}%)")
    else:
        print("charts with >30% UNTYPABLE: none")
    print(">>> PAUSE for Gary's go before the next batch. <<<")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=1)
    ap.add_argument("--size", type=int, default=20)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    remaining = list_remaining()
    done = already_done()
    todo = [(c, n) for c, n in remaining if c not in done]
    batch = todo[: args.size]
    if not batch:
        print("Nothing left to type.")
        return
    print(
        f"Remaining before batch: {len(todo)} charts, {sum(n for _, n in todo)} edges"
    )
    print(f"Typing batch of {len(batch)} charts...")

    all_batch_rows: list[dict] = []
    chart_ids: list[str] = []
    for cid, _n in batch:
        rows = type_chart(cid)
        all_batch_rows.extend(rows)
        chart_ids.append(cid)
        print(f"  typed {cid}: {len(rows)} cycle edges")

    if not args.dry_run:
        append_rows(all_batch_rows)
    report(all_batch_rows, chart_ids, args.batch)


if __name__ == "__main__":
    main()
