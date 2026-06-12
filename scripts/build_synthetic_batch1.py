#!/usr/bin/env python3
"""
Build Batch 1 of the GLMP flowchart collection: canonical synthetic-biology circuits
with *known* ground-truth circuit classes.

Why synthetic circuits first (per glmp-collaboration-plan-2026.md):
  - Their topology AND their dynamic behaviour are established by construction
    (Elowitz, Collins, Alon, et al.), so they are unambiguous ground-truth anchors
    for the five-class complexity ladder used everywhere else in the collection.
  - Their regulatory sequences are known, so each one carries a `sequenceAnnotation`
    block: the explicit mapping from binding-site arrangement -> logical operator.
    That is the sequence -> logic training pair the Big Picture goal is built on,
    demonstrated on circuits where the answer is not in doubt.

Output: glmp-v2/processes/synthetic/<id>.json   (full process schema, viewer-ready)

Stats (nodes / edges / loops / conditionals) are derived from the authored Mermaid so
they always agree with the diagram. Logic-gate counts (or/and/not) are declared per
circuit because they are semantic, not syntactic.
"""

import json
from pathlib import Path

OUT_DIR = Path("glmp-v2/processes/synthetic")

COLOR_SCHEME = {
    "red":    {"hex": "#ff6b6b", "category": "Triggers & Inputs",        "description": "Inducers, signals, environmental inputs"},
    "yellow": {"hex": "#ffd43b", "category": "Structures & Objects",      "description": "Transcription factors, repressors, regulatory proteins"},
    "green":  {"hex": "#51cf66", "category": "Processing & Operations",   "description": "Transcription, translation, regulatory action"},
    "blue":   {"hex": "#74c0fc", "category": "Intermediates & States",    "description": "Promoter states, circuit states, attractors"},
    "violet": {"hex": "#b197fc", "category": "Products & Outputs",        "description": "Reporter output, circuit behaviour"},
}
HEX = {k: v["hex"] for k, v in COLOR_SCHEME.items()}
TEXT_BLACK = {"yellow"}  # yellow needs dark text

CLASS_NAME = {
    "I": "Feed-forward cascade",
    "II": "Negative feedback (homeostatic)",
    "III": "Bistable switch / positive feedback",
    "IV": "Delayed negative feedback (oscillator)",
    "V": "Self-modifying chromatin / epigenetic",
}


def build_mermaid(nodes, edges):
    """nodes: list of (id, label_with_shape, color). edges: list of (src, dst, edge_label)."""
    lines = ["graph TD"]
    for nid, shape, _ in nodes:
        lines.append(f"    {nid}{shape}")
    lines.append("")
    for src, dst, lbl in edges:
        if lbl:
            lines.append(f"    {src} -->|{lbl}| {dst}")
        else:
            lines.append(f"    {src} --> {dst}")
    lines.append("")
    for nid, _, color in nodes:
        txt = "#000" if color in TEXT_BLACK else "#fff"
        lines.append(f"    style {nid} fill:{HEX[color]},color:{txt}")
    return "\n".join(lines)


def compute_stats(nodes, edges):
    order = {nid: i for i, (nid, _, _) in enumerate(nodes)}
    loop_sources = set()
    for src, dst, _ in edges:
        if src in order and dst in order and order[dst] < order[src]:
            loop_sources.add(src)
    conditionals = sum(1 for _, shape, _ in nodes if "{" in shape)
    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "loops": len(loop_sources),
        "conditionals": conditionals,
    }


def make_process(spec):
    nodes, edges = spec["nodes"], spec["edges"]
    stats = compute_stats(nodes, edges)
    or_g, and_g, not_g = spec["gates"]
    cls = spec["circuitClass"]
    proc = {
        "id": spec["id"],
        "name": spec["name"],
        "organism": "Synthetic circuit",
        "category": "Synthetic Biology",
        "description": spec["description"],
        "scientificAccuracy": spec["scientificAccuracy"],
        "complexity": {
            "nodes": stats["nodes"],
            "uniqueIdentifiers": True,
            "colorCoded": True,
            "detailLevel": "ground-truth",
            "logicGates": {"orGates": or_g, "andGates": and_g, "total": or_g + and_g},
        },
        "colorScheme": COLOR_SCHEME,
        "mermaid": build_mermaid(nodes, edges),
        "sources": spec["sources"],
        "keywords": spec["keywords"],
        "relatedProcesses": spec.get("relatedProcesses", []),
        "created": "2026-06-12",
        "lastUpdated": "2026-06-12",
        "verified": True,
        "verifiedBy": "Canonical synthetic-biology literature (ground-truth circuit)",
        "notes": spec["notes"],
        "sequenceAnnotation": spec["sequenceAnnotation"],
        "logicGates": {"or": or_g, "and": and_g, "not": not_g},
        "notGates": not_g,
        "conditionals": stats["conditionals"],
        "totalNodes": stats["nodes"],
        "edges": stats["edges"],
        "loops": stats["loops"],
        "circuitClass": cls,
        "circuitClassName": CLASS_NAME[cls],
        "topologyType": spec["topologyType"],
        "circuitClassConfidence": "high",
        "circuitClassNeedsReview": False,
        "circuitClassRationale": spec["rationale"],
        "groundTruth": True,
    }
    return proc


SPECS = [
    # ---------------------------------------------------------------- Class II
    {
        "id": "synthetic_negative_autoregulation",
        "name": "Negative Autoregulation (NAR motif)",
        "circuitClass": "II",
        "topologyType": "negative_autoregulation",
        "rationale": "A transcription factor represses its own promoter — the minimal negative-feedback motif. Speeds the response time and reduces cell-to-cell noise (Rosenfeld, Elowitz & Alon 2002); the single most common network motif in E. coli.",
        "description": "The simplest homeostatic circuit: a transcription factor X represses the very promoter that produces it. This single negative-feedback loop accelerates the rise-time to steady state and buffers expression noise, and is the most statistically over-represented one-node motif in the E. coli transcription network.",
        "scientificAccuracy": "Ground-truth circuit. Topology (X ⊣ X) and behaviour (faster response, reduced noise) are established by direct synthetic measurement (Rosenfeld et al. 2002; Becskei & Serrano 2000).",
        "nodes": [
            ("A", "[Inducer signal]", "red"),
            ("B", "{Promoter P active?}", "blue"),
            ("C", "[Transcription of gene X]", "green"),
            ("D", "[Repressor protein X]", "yellow"),
            ("E", "[/X represses own promoter P/]", "green"),
            ("F", "(Fast, noise-buffered steady state)", "violet"),
        ],
        "edges": [
            ("A", "B", ""),
            ("B", "C", "derepressed"),
            ("C", "D", ""),
            ("D", "E", ""),
            ("E", "B", "feedback"),
            ("D", "F", ""),
        ],
        "gates": (0, 0, 1),
        "notGates": 1,
        "sources": [
            {"title": "Negative autoregulation speeds the response times of transcription networks", "authors": "Rosenfeld N, Elowitz MB, Alon U", "journal": "Journal of Molecular Biology", "year": 2002, "volume": "323", "pages": "785-793", "pmid": "12417193", "doi": "10.1016/S0022-2836(02)00994-4"},
            {"title": "Engineering stability in gene networks by autoregulation", "authors": "Becskei A, Serrano L", "journal": "Nature", "year": 2000, "volume": "405", "pages": "590-593", "pmid": "10850721", "doi": "10.1038/35014651"},
        ],
        "keywords": ["negative autoregulation", "network motif", "negative feedback", "noise reduction", "response time", "NAR", "ground truth"],
        "notes": "Ground-truth Class II anchor. One repression edge (NOT) forming a single self-loop.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Promoter P (e.g. PLtetO-1)", "boundFactor": "X (e.g. TetR)", "site": "operator overlapping -10/-35", "operator": "NOT", "effect": "repression", "sequenceMotif": "TCCCTATCAGTGATAGAGA", "note": "tetO2 palindrome; X occupancy blocks RNAP recruitment"},
            ],
            "derivedLogic": "X = NOT X(t-τ)   (self-repression -> homeostatic set-point)",
        },
    },
    # --------------------------------------------------------------- Class III
    {
        "id": "synthetic_positive_autoregulation",
        "name": "Positive Autoregulation (PAR motif)",
        "circuitClass": "III",
        "topologyType": "positive_autoregulation",
        "rationale": "A transcription factor activates its own promoter — positive feedback that, above a threshold, produces bistability and cellular memory (an ON state that persists after the inducer is removed). Slows response and increases variability relative to NAR.",
        "description": "A transcription factor X that activates its own promoter. Positive feedback creates a threshold: once X passes it, the circuit latches into a self-sustaining ON state that persists after the input is gone — the molecular basis of cellular memory and a building block of bistable switches.",
        "scientificAccuracy": "Ground-truth circuit. Positive autoregulation producing bistability/memory is established synthetically (Becskei, Séraphin & Serrano 2001; Maeda & Sano 2006).",
        "nodes": [
            ("A", "[Inducer signal]", "red"),
            ("B", "{Promoter P active?}", "blue"),
            ("C", "[Transcription of gene X]", "green"),
            ("D", "[Activator protein X]", "yellow"),
            ("E", "[\\X activates own promoter P/]", "green"),
            ("F", "(Bistable ON state / memory)", "violet"),
        ],
        "edges": [
            ("A", "B", ""),
            ("B", "C", "active"),
            ("C", "D", ""),
            ("D", "E", ""),
            ("E", "B", "feedback"),
            ("D", "F", ""),
        ],
        "gates": (0, 0, 0),
        "notGates": 0,
        "sources": [
            {"title": "Positive feedback in eukaryotic gene networks: cell differentiation by graded to binary response conversion", "authors": "Becskei A, Séraphin B, Serrano L", "journal": "EMBO Journal", "year": 2001, "volume": "20", "pages": "2528-2535", "pmid": "11350942", "doi": "10.1093/emboj/20.10.2528"},
            {"title": "Regulatory dynamics of synthetic gene networks with positive feedback", "authors": "Maeda YT, Sano M", "journal": "Journal of Molecular Biology", "year": 2006, "volume": "359", "pages": "1107-1124", "pmid": "16701695", "doi": "10.1016/j.jmb.2006.03.064"},
        ],
        "keywords": ["positive autoregulation", "bistability", "cellular memory", "positive feedback", "PAR", "ground truth"],
        "notes": "Ground-truth Class III anchor. Activating self-loop (no NOT); bistable for sufficient feedback gain.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Promoter P", "boundFactor": "X (activator)", "site": "upstream activating sequence", "operator": "IDENTITY/IF", "effect": "activation", "sequenceMotif": "(activator-specific UAS)", "note": "X occupancy recruits RNAP -> self-amplification"},
            ],
            "derivedLogic": "X = IF X(t-τ) > threshold THEN ON  (positive feedback -> latch)",
        },
    },
    {
        "id": "synthetic_toggle_switch",
        "name": "Genetic Toggle Switch (Gardner-Collins)",
        "circuitClass": "III",
        "topologyType": "mutual_repression_bistable",
        "rationale": "Two repressors each transcribed from a promoter the other represses (LacI ⊣ TetR ⊣ LacI). Mutual repression yields two stable states; transient inducer pulses flip between them. The canonical engineered bistable switch (Gardner, Cantor & Collins 2000).",
        "description": "The first engineered bistable gene circuit: two repressors, each driven by a promoter the other represses. The double-negative loop has two stable states (high-LacI or high-TetR). A transient pulse of IPTG or aTc flips the switch, which then holds its state — a one-bit memory built from transcription.",
        "scientificAccuracy": "Ground-truth circuit. Construction and bistability demonstrated in E. coli by Gardner, Cantor & Collins (2000).",
        "nodes": [
            ("A", "[Input: IPTG pulse]", "red"),
            ("G", "[Input: aTc pulse]", "red"),
            ("B", "[\\LacI inactivated/]", "green"),
            ("H", "[\\TetR inactivated/]", "green"),
            ("C", "[TetR expressed]", "yellow"),
            ("F", "[LacI expressed]", "yellow"),
            ("D", "[/TetR represses Plac/]", "green"),
            ("E", "[/LacI represses Ptet/]", "green"),
            ("I", "(Stable state A: high TetR)", "violet"),
            ("J", "(Stable state B: high LacI)", "violet"),
        ],
        "edges": [
            ("A", "B", ""),
            ("G", "H", ""),
            ("B", "C", "derepress Ptet"),
            ("H", "F", "derepress Plac"),
            ("C", "D", ""),
            ("F", "E", ""),
            ("D", "F", "⊣"),
            ("E", "C", "⊣"),
            ("C", "I", ""),
            ("F", "J", ""),
        ],
        "gates": (0, 0, 2),
        "notGates": 2,
        "sources": [
            {"title": "Construction of a genetic toggle switch in Escherichia coli", "authors": "Gardner TS, Cantor CR, Collins JJ", "journal": "Nature", "year": 2000, "volume": "403", "pages": "339-342", "pmid": "10659857", "doi": "10.1038/35002131"},
        ],
        "keywords": ["toggle switch", "bistability", "mutual repression", "synthetic biology", "memory", "LacI", "TetR", "ground truth"],
        "notes": "Ground-truth Class III anchor. Two mutual-repression edges (2 NOT) form the bistable double-negative loop.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Ptrc-2 (LacI-repressed)", "boundFactor": "LacI", "site": "lac operator", "operator": "NOT", "effect": "repression", "sequenceMotif": "AATTGTGAGCGGATAACAATT", "note": "natural lacO1; controls TetR cistron"},
                {"name": "PLtetO-1 (TetR-repressed)", "boundFactor": "TetR", "site": "tetO2", "operator": "NOT", "effect": "repression", "sequenceMotif": "TCCCTATCAGTGATAGAGA", "note": "controls LacI cistron"},
            ],
            "derivedLogic": "TetR = NOT LacI ; LacI = NOT TetR  -> two stable fixed points",
        },
    },
    # ---------------------------------------------------------------- Class IV
    {
        "id": "synthetic_repressilator",
        "name": "Repressilator (3-repressor ring oscillator)",
        "circuitClass": "IV",
        "topologyType": "ring_oscillator_delayed_neg_feedback",
        "rationale": "Three repressors in a cyclic chain (LacI ⊣ TetR ⊣ cI ⊣ LacI). The odd number of inversions around the loop gives delayed negative feedback, producing sustained oscillations in protein level — the canonical synthetic oscillator (Elowitz & Leibler 2000).",
        "description": "A ring of three repressors in which each represses the next: LacI represses TetR, TetR represses λ cI, and cI represses LacI. The odd number of repressions makes the loop a delayed negative-feedback circuit that oscillates, driving a periodic GFP reporter — the first engineered gene-network oscillator.",
        "scientificAccuracy": "Ground-truth circuit. Topology and oscillatory behaviour demonstrated in E. coli by Elowitz & Leibler (2000).",
        "nodes": [
            ("A", "[LacI]", "yellow"),
            ("B", "[/LacI represses TetR/]", "green"),
            ("C", "[TetR]", "yellow"),
            ("D", "[/TetR represses cI/]", "green"),
            ("E", "[cI]", "yellow"),
            ("F", "[/cI represses LacI/]", "green"),
            ("G", "(Oscillating GFP reporter)", "violet"),
        ],
        "edges": [
            ("A", "B", ""),
            ("B", "C", "⊣"),
            ("C", "D", ""),
            ("D", "E", "⊣"),
            ("E", "F", ""),
            ("F", "A", "⊣"),
            ("A", "G", ""),
        ],
        "gates": (0, 0, 3),
        "notGates": 3,
        "sources": [
            {"title": "A synthetic oscillatory network of transcriptional regulators", "authors": "Elowitz MB, Leibler S", "journal": "Nature", "year": 2000, "volume": "403", "pages": "335-338", "pmid": "10659856", "doi": "10.1038/35002125"},
        ],
        "keywords": ["repressilator", "oscillator", "delayed negative feedback", "ring oscillator", "synthetic biology", "ground truth"],
        "notes": "Ground-truth Class IV anchor. Three repressions (3 NOT) around a closed ring -> one feedback loop with delay.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "PLtetO-1", "boundFactor": "TetR", "site": "tetO2", "operator": "NOT", "effect": "repression", "sequenceMotif": "TCCCTATCAGTGATAGAGA", "note": "drives next cistron in ring"},
                {"name": "PLlacO-1", "boundFactor": "LacI", "site": "lacO", "operator": "NOT", "effect": "repression", "sequenceMotif": "AATTGTGAGCGGATAACAATT"},
                {"name": "PR (lambda)", "boundFactor": "cI", "site": "OR1/OR2", "operator": "NOT", "effect": "repression", "sequenceMotif": "TACCTCTGGCGGTGATAA", "note": "lambda right operator consensus"},
            ],
            "derivedLogic": "TetR=NOT LacI ; cI=NOT TetR ; LacI=NOT cI  -> odd inversions -> oscillation",
        },
    },
    # ----------------------------------------------------------------- Class I
    {
        "id": "synthetic_coherent_ffl",
        "name": "Coherent Feed-Forward Loop (type-1, AND)",
        "circuitClass": "I",
        "topologyType": "coherent_feed_forward_AND",
        "rationale": "X activates Y, and X and Y jointly (AND) activate Z. No cycle — a feed-forward cascade. Functions as a sign-sensitive delay / persistence detector: Z turns on only after a sustained input, filtering transient pulses (Mangan & Alon 2003).",
        "description": "The most common coherent feed-forward loop: X activates Y, and both X and Y are required (AND logic) to activate the output Z. With no feedback edge it is a pure feed-forward cascade, but the AND gate makes Z respond only to a persistent input — a built-in noise filter and persistence detector.",
        "scientificAccuracy": "Ground-truth circuit. Topology and sign-sensitive-delay behaviour established by Mangan & Alon (2003) and Mangan, Zaslaver & Alon (2003).",
        "nodes": [
            ("A", "[Signal Sx]", "red"),
            ("B", "[TF X active]", "yellow"),
            ("C", "[TF Y expressed]", "yellow"),
            ("D", "{X AND Y present?}", "blue"),
            ("E", "[Gene Z expressed]", "green"),
            ("F", "(Output Z: delayed ON, immediate OFF)", "violet"),
        ],
        "edges": [
            ("A", "B", ""),
            ("B", "C", ""),
            ("B", "D", ""),
            ("C", "D", ""),
            ("D", "E", "Yes"),
            ("E", "F", ""),
        ],
        "gates": (0, 1, 0),
        "notGates": 0,
        "sources": [
            {"title": "Structure and function of the feed-forward loop network motif", "authors": "Mangan S, Alon U", "journal": "PNAS", "year": 2003, "volume": "100", "pages": "11980-11985", "pmid": "14530388", "doi": "10.1073/pnas.2133841100"},
            {"title": "The coherent feedforward loop serves as a sign-sensitive delay element in transcription networks", "authors": "Mangan S, Zaslaver A, Alon U", "journal": "Journal of Molecular Biology", "year": 2003, "volume": "334", "pages": "197-204", "pmid": "14607112", "doi": "10.1016/j.jmb.2003.09.049"},
        ],
        "keywords": ["feed-forward loop", "coherent FFL", "AND gate", "sign-sensitive delay", "persistence detector", "network motif", "ground truth"],
        "notes": "Ground-truth Class I anchor. Feed-forward (no cycle) with one AND gate.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Promoter of Z", "boundFactor": "X and Y", "site": "two adjacent activator sites", "operator": "AND", "effect": "activation", "sequenceMotif": "(X-site)...(Y-site)", "note": "both sites must be occupied for RNAP recruitment"},
                {"name": "Promoter of Y", "boundFactor": "X", "site": "activator site", "operator": "IF", "effect": "activation", "sequenceMotif": "(X-site)"},
            ],
            "derivedLogic": "Y = X ; Z = X AND Y  -> Z requires sustained X",
        },
    },
    {
        "id": "synthetic_incoherent_ffl",
        "name": "Incoherent Feed-Forward Loop (type-1, pulse)",
        "circuitClass": "I",
        "topologyType": "incoherent_feed_forward_pulse",
        "rationale": "X activates both Z and a repressor Y, and Y represses Z (Z = X AND NOT Y). No cycle — still a feed-forward cascade — but the delayed repression generates a transient pulse and partial adaptation. Class I by topology; flagged as functionally adaptive (Mangan & Alon 2003; Basu et al. 2004).",
        "description": "An incoherent feed-forward loop: X directly activates the output Z and also activates a repressor Y that shuts Z back down. Because Y arrives later, Z first rises then falls — a pulse generator that also speeds the response and gives partial adaptation. Topologically feed-forward (no feedback edge), so Class I, but functionally distinct from a simple cascade.",
        "scientificAccuracy": "Ground-truth circuit. Pulse-generation / response-acceleration behaviour established by Mangan & Alon (2003); synthetic pulse-generator built by Basu et al. (2004).",
        "nodes": [
            ("A", "[Signal Sx]", "red"),
            ("B", "[TF X active]", "yellow"),
            ("C", "[Z activated by X]", "green"),
            ("D", "[Repressor Y expressed]", "yellow"),
            ("E", "[/Y represses Z/]", "green"),
            ("F", "{Z = X AND NOT Y?}", "blue"),
            ("G", "(Output Z: transient pulse / adaptation)", "violet"),
        ],
        "edges": [
            ("A", "B", ""),
            ("B", "C", ""),
            ("B", "D", ""),
            ("D", "E", ""),
            ("C", "F", ""),
            ("E", "F", "delayed"),
            ("F", "G", "Yes"),
        ],
        "gates": (0, 1, 1),
        "notGates": 1,
        "sources": [
            {"title": "Structure and function of the feed-forward loop network motif", "authors": "Mangan S, Alon U", "journal": "PNAS", "year": 2003, "volume": "100", "pages": "11980-11985", "pmid": "14530388", "doi": "10.1073/pnas.2133841100"},
            {"title": "Spatiotemporal control of gene expression with pulse-generating networks", "authors": "Basu S, Mehreja R, Thiberge S, Chen MT, Weiss R", "journal": "PNAS", "year": 2004, "volume": "101", "pages": "6355-6360", "pmid": "15096621", "doi": "10.1073/pnas.0307571101"},
        ],
        "keywords": ["incoherent feed-forward loop", "pulse generator", "adaptation", "AND NOT", "network motif", "ground truth"],
        "notes": "Ground-truth Class I anchor (feed-forward topology). Carries one AND and one NOT; functionally a pulse generator (recorded in rationale).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Promoter of Z", "boundFactor": "X (activator) + Y (repressor)", "site": "overlapping activator + operator", "operator": "AND NOT", "effect": "activation gated by repression", "sequenceMotif": "(X-site)+(Y-operator)", "note": "Z on when X present and Y absent"},
                {"name": "Promoter of Y", "boundFactor": "X", "site": "activator site", "operator": "IF", "effect": "activation", "sequenceMotif": "(X-site)"},
            ],
            "derivedLogic": "Y = X ; Z = X AND NOT Y  -> delayed repression -> pulse",
        },
    },
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for spec in SPECS:
        proc = make_process(spec)
        path = OUT_DIR / f"{spec['id']}.json"
        with open(path, "w") as fh:
            json.dump(proc, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        written.append((proc["id"], proc["circuitClass"], proc["totalNodes"],
                        proc["edges"], proc["loops"], proc["conditionals"],
                        proc["logicGates"]))
    print(f"Wrote {len(written)} synthetic process files -> {OUT_DIR}\n")
    print(f"{'id':<38} {'cls':<4} {'nodes':<6} {'edges':<6} {'loops':<6} {'cond':<5} gates")
    for r in written:
        print(f"{r[0]:<38} {r[1]:<4} {r[2]:<6} {r[3]:<6} {r[4]:<6} {r[5]:<5} {r[6]}")


if __name__ == "__main__":
    main()
