#!/usr/bin/env python3
"""
Batch 7 of synthetic-biology ground-truth circuits (extends build_synthetic_batch1-6).

Coverage:
  Class I  : distributed multicellular consortium logic (Tamsir 2011),
             RNA transcriptional attenuator logic (Lucks 2011)
  Class III: double-positive (mutual-activation) bistable switch

Reuses Batch 1 helpers. Output: glmp-v2/processes/synthetic/<id>.json
"""

import json

from build_synthetic_batch1 import make_process, OUT_DIR

SPECS = [
    {
        "id": "synthetic_consortium_logic",
        "name": "Distributed Multicellular Consortium Logic",
        "circuitClass": "I",
        "topologyType": "distributed_combinational_logic",
        "rationale": "Simple NOR-gate cells are wired together by diffusible AHL signals so that the colony computes complex Boolean functions distributed across cell types; the overall computation is feed-forward combinational logic with no feedback loop. Class I (Tamsir, Tabor & Voigt 2011).",
        "description": "Rather than cram a whole circuit into one cell, logic is spread across a microbial consortium: each strain implements a simple NOR gate and communicates via quorum-sensing molecules, so that wiring colonies in space computes more complex functions. The network is a feed-forward combinational program realized at the community level.",
        "scientificAccuracy": "Ground-truth circuit. Distributed logic from NOR-gate cells wired by chemical signals was built by Tamsir, Tabor & Voigt (2011).",
        "nodes": [
            ("A", "[Inputs across cell types]", "red"),
            ("B", "[Sender cells compute partial logic]", "yellow"),
            ("C", "[AHL wiring between colonies]", "blue"),
            ("D", "[/Receiver NOR gates/]", "green"),
            ("E", "[Combined logic at output colony]", "green"),
            ("F", "(Distributed multicellular logic)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Robust multicellular computing using genetically encoded NOR gates and chemical wires", "authors": "Tamsir A, Tabor JJ, Voigt CA", "journal": "Nature", "year": 2011, "volume": "469", "pages": "212-215", "pmid": "21150903", "doi": "10.1038/nature09565"},
        ],
        "keywords": ["consortium", "distributed logic", "NOR", "chemical wiring", "multicellular", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_layered_nor_cascade", "synthetic_edge_detector"],
        "notes": "Ground-truth Class I distributed combinational computing across a cell consortium (feed-forward).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "per-cell NOR promoters + lux wiring", "boundFactor": "repressors + LuxR-AHL", "operator": "NOR (distributed)", "effect": "community-level combinational logic", "sequenceMotif": "operator + lux box", "note": "spatial wiring composes the function"},
            ],
            "derivedLogic": "Output = f(inputs) composed from NOR cells wired by AHL",
            "references": ["Tamsir et al. 2011"],
        },
    },
    {
        "id": "synthetic_rna_attenuator",
        "name": "RNA Transcriptional Attenuator Logic",
        "circuitClass": "I",
        "topologyType": "rna_cis_antisense_feed_forward",
        "rationale": "An antisense RNA reconfigures an attenuator hairpin in a target mRNA leader to switch transcription between termination and read-through; the regulation is RNA-only, fast, and feed-forward, with no protein feedback loop. Class I (Lucks et al. 2011 pT181-based attenuators).",
        "description": "Logic implemented purely in RNA. A cis attenuator in an mRNA's 5' leader folds into a terminator hairpin by default; a trans antisense RNA binds and refolds it to permit read-through. Chaining orthogonal attenuators builds RNA-only AND/cascade logic — a fast, protein-free, feed-forward regulatory layer.",
        "scientificAccuracy": "Ground-truth circuit. Engineered pT181-derived transcriptional attenuators and their composition were demonstrated by Lucks et al. (2011).",
        "nodes": [
            ("A", "[Antisense RNA input]", "red"),
            ("B", "[/Refolds attenuator hairpin/]", "green"),
            ("C", "{terminate or read-through?}", "blue"),
            ("D", "[Downstream gene expressed]", "green"),
            ("E", "(RNA-only logic output)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", "read-through"), ("D", "E", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Versatile RNA-sensing transcriptional regulators for engineering genetic networks", "authors": "Lucks JB, Qi L, Mutalik VK, Wang D, Arkin AP", "journal": "PNAS", "year": 2011, "volume": "108", "pages": "8617-8622", "pmid": "21555549", "doi": "10.1073/pnas.1015741108"},
        ],
        "keywords": ["RNA", "attenuator", "antisense", "pT181", "riboregulator", "feed-forward", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_toehold_riboregulator", "synthetic_riboswitch"],
        "notes": "Ground-truth Class I RNA-only regulation (transcriptional attenuator); cis/antisense, no feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "attenuator leader hairpin", "boundFactor": "trans antisense RNA", "operator": "IF (refold) / NOT(terminate)", "effect": "switches termination vs read-through", "sequenceMotif": "pT181 antisense/sense hairpin", "note": "RNA-level, composable into AND/cascade"},
            ],
            "derivedLogic": "Output = IF antisense bound (read-through) ELSE terminate",
            "references": ["Lucks et al. 2011"],
        },
    },
    {
        "id": "synthetic_mutual_activation_bistable",
        "name": "Double-Positive Mutual-Activation Switch",
        "circuitClass": "III", "circuitSubclass": "IIIa",
        "topologyType": "double_positive_feedback_bistable",
        "rationale": "Two activators each drive the other's expression (a double-positive loop); like mutual repression this yields bistability, latching the system into a high/high or low/low state — a persistent (IIIa) memory switch with a topology distinct from the repressor toggle.",
        "description": "A bistable switch built from mutual activation instead of mutual repression. Activator X turns on Y and Y turns on X, so a transient input that raises either one can lock both high, while the absence of input keeps both low. The double-positive feedback gives a hysteretic, memory-holding switch — the activator-based counterpart of the Gardner–Collins toggle.",
        "scientificAccuracy": "Bistability from double-positive feedback is a well-characterized synthetic motif (e.g., mutual-activation switches engineered following Gardner et al. 2000 design principles).",
        "nodes": [
            ("A", "[Inducer pulse]", "red"),
            ("B", "[Activator X]", "yellow"),
            ("C", "[Activator Y]", "yellow"),
            ("D", "[\\X activates Y/]", "green"),
            ("E", "[\\Y activates X/]", "green"),
            ("F", "(Bistable high/high state)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "D", ""), ("D", "C", "+"),
            ("C", "E", ""), ("E", "B", "+"), ("B", "F", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "Construction of a genetic toggle switch in Escherichia coli", "authors": "Gardner TS, Cantor CR, Collins JJ", "journal": "Nature", "year": 2000, "volume": "403", "pages": "339-342", "pmid": "10659857", "doi": "10.1038/35002131"},
        ],
        "keywords": ["mutual activation", "double positive", "bistable", "memory", "toggle", "Class IIIa", "ground truth"],
        "relatedProcesses": ["synthetic_toggle_switch", "human_gata1_pu1_switch"],
        "notes": "Ground-truth Class IIIa bistable switch via double-positive feedback (mutual activation).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "PX, PY activator-driven promoters", "boundFactor": "activator X / activator Y", "operator": "double IF / positive feedback", "effect": "mutual activation latches state", "sequenceMotif": "activator operator pair", "note": "high/high and low/low stable states"},
            ],
            "derivedLogic": "X = IF Y ; Y = IF X (double positive) -> bistable",
            "references": ["Gardner et al. 2000"],
        },
    },
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for spec in SPECS:
        proc = make_process(spec)
        if spec.get("circuitSubclass"):
            proc["circuitSubclass"] = spec["circuitSubclass"]
        path = OUT_DIR / f"{spec['id']}.json"
        with open(path, "w") as fh:
            json.dump(proc, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        rows.append((proc["id"], proc["circuitClass"], proc.get("circuitSubclass") or "-",
                     proc["totalNodes"], proc["loops"], proc["logicGates"]))
    print(f"Wrote {len(rows)} synthetic Batch-7 process files -> {OUT_DIR}\n")
    print(f"{'id':<42} {'cls':<4} {'sub':<5} {'nodes':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<42} {r[1]:<4} {r[2]:<5} {r[3]:<6} {r[4]:<6} {r[5]}")


if __name__ == "__main__":
    main()
