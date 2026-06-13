#!/usr/bin/env python3
"""
Expand tier-C (and selected tier-B) thin ground-truth flowcharts.

Adds named intermediates to pathway schematics flagged by audit_recent_flowchart_quality.py.
Preserves sources, sequenceAnnotation, circuit class, and copernicusIntegration.

Run:
  python3 scripts/audit_recent_flowchart_quality.py   # identify tiers
  python3 scripts/expand_thin_groundtruth_charts.py --apply
  python3 scripts/audit_recent_flowchart_quality.py   # verify
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_synthetic_batch1 import build_mermaid, compute_stats

ROOT = Path(__file__).resolve().parents[1]
PROC_DIR = ROOT / "glmp-v2" / "processes"

# nodes: (id, label_with_shape, color); edges: (src, dst, label); gates: (or, and, not)
EXPANSIONS: dict[str, dict] = {
    "human_tlr4_lps_amplification": {
        "nodes": [
            ("A", "[LPS + CD14]", "red"),
            ("B", "[TLR4–MD2 receptor]", "yellow"),
            ("C", "[MyD88 / TRAF6 / IRAK]", "green"),
            ("D", "[/IκBα degraded/]", "green"),
            ("E", "[NF-κB p65 nuclear]", "yellow"),
            ("F", "[TNF-α + IL-1β + IL-6]", "green"),
            ("G", "[\\Cytokines amplify adaptor signaling/]", "green"),
            ("H", "[MAPK → AP-1 arm]", "green"),
            ("I", "(High inflammatory state)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "E", ""),
            ("C", "H", ""), ("E", "F", ""), ("F", "G", ""), ("G", "C", "+ amplify"),
            ("E", "I", ""), ("F", "I", ""),
        ],
        "gates": (0, 0, 1),
        "notes": "Human Class III inflammatory amplifier — expanded with IκBα, adaptor complex, and cytokine feedback arm.",
    },
    "human_rig_i_mavs_antiviral": {
        "nodes": [
            ("A", "[Viral 5'-ppp dsRNA]", "red"),
            ("B", "[RIG-I CARD exposed]", "yellow"),
            ("C", "[MAVS filaments on mitochondria]", "green"),
            ("D", "[TBK1 / IKKε recruited]", "green"),
            ("E", "[IRF3 phosphorylated + dimer]", "yellow"),
            ("F", "{IRF3 AND NF-κB enhanceosome?}", "blue"),
            ("G", "[IFN-β transcribed]", "green"),
            ("H", "[\\MAVS filament self-amplification/]", "green"),
            ("I", "(All-or-none antiviral state)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "E", ""),
            ("E", "F", ""), ("F", "G", "Yes"), ("C", "H", ""), ("H", "C", "+"),
            ("G", "I", ""),
        ],
        "gates": (0, 1, 0),
        "notes": "Human Class III antiviral switch — expanded with TBK1, IRF3 dimerization, and enhanceosome AND gate.",
    },
    "human_nlrp3_inflammasome": {
        "nodes": [
            ("A", "[Priming: TLR/NF-κB]", "red"),
            ("B", "[Danger signal: K+ efflux / crystals]", "red"),
            ("C", "[NLRP3 activated]", "yellow"),
            ("D", "[\\Nucleates ASC speck/]", "green"),
            ("E", "[Caspase-1 activated]", "green"),
            ("F", "[IL-1β maturation]", "green"),
            ("G", "[Pyroptosis / GSDMD pore]", "green"),
            ("H", "(All-or-none inflammasome firing)", "violet"),
        ],
        "edges": [
            ("A", "C", "license"), ("B", "C", "trigger"), ("C", "D", ""),
            ("D", "E", ""), ("E", "D", "+ self-template"), ("E", "F", ""),
            ("F", "G", ""), ("G", "H", ""),
        ],
        "gates": (0, 0, 0),
        "notes": "Human Class III inflammasome — expanded with separate priming and danger signals.",
    },
    "human_il6_stat3_inflammation": {
        "nodes": [
            ("A", "[Inflammatory trigger]", "red"),
            ("B", "[IL-6 secreted]", "yellow"),
            ("C", "[IL-6R + gp130 → JAK]", "green"),
            ("D", "[STAT3 phosphorylated]", "yellow"),
            ("E", "[NF-κB crosstalk]", "green"),
            ("F", "[\\STAT3 + NF-κB induce IL-6/]", "green"),
            ("G", "[Inflammatory gene program]", "green"),
            ("H", "(Self-sustaining inflammation)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "E", ""),
            ("D", "F", ""), ("E", "F", ""), ("F", "B", "+"), ("D", "G", ""), ("G", "H", ""),
        ],
        "gates": (0, 0, 0),
        "notes": "Human Class IIIa IL-6/STAT3 switch — expanded with receptor complex and NF-κB crosstalk.",
    },
    "human_irf7_interferon_amplifier": {
        "nodes": [
            ("A", "[Viral RNA / TLR7/9]", "red"),
            ("B", "[IRF3 / IRF7 activated]", "yellow"),
            ("C", "[IFN-β secreted]", "green"),
            ("D", "[IFNAR → JAK1/TYK2]", "green"),
            ("E", "[STAT1-STAT2-ISGF3]", "yellow"),
            ("F", "[\\Induces more IRF7/]", "green"),
            ("G", "[Antiviral ISG program]", "green"),
            ("H", "(All-or-none antiviral state)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "E", ""),
            ("E", "F", ""), ("F", "B", "+"), ("E", "G", ""), ("G", "H", ""),
        ],
        "gates": (0, 0, 0),
        "notes": "Human Class III IRF7 amplifier — expanded with IFNAR/JAK and ISGF3 complex.",
    },
    "human_scl_tal1_hematopoietic_switch": {
        "nodes": [
            ("A", "[Hemogenic mesoderm]", "red"),
            ("B", "[Notch/RBPJ signal]", "red"),
            ("C", "[SCL/TAL1 + LMO2 + E2A]", "yellow"),
            ("D", "[\\TAL1 autoactivation/]", "green"),
            ("E", "[GATA2 cooperative binding]", "green"),
            ("F", "[Hematopoietic TF network]", "green"),
            ("G", "(Committed hematopoietic progenitor)", "violet"),
        ],
        "edges": [
            ("A", "C", ""), ("B", "C", ""), ("C", "D", ""), ("D", "C", "+"),
            ("C", "E", ""), ("E", "F", ""), ("F", "G", ""),
        ],
        "gates": (0, 0, 0),
        "notes": "Human Class IIIa SCL/TAL1 switch — expanded with LMO2/E2A complex and GATA2 cooperation.",
    },
    "human_foxp3_treg_switch": {
        "nodes": [
            ("A", "[TCR antigen signal]", "red"),
            ("B", "[IL-2 → STAT5]", "red"),
            ("C", "[Foxp3 induced]", "yellow"),
            ("D", "[\\Foxp3 CNS2 autoactivation/]", "green"),
            ("E", "[SMAD3 + TGF-β cooperation]", "green"),
            ("F", "[Treg program: CTLA-4, CD25]", "green"),
            ("G", "(Stable regulatory T cell)", "violet"),
        ],
        "edges": [
            ("A", "C", ""), ("B", "C", ""), ("C", "D", ""), ("D", "C", "+"),
            ("C", "E", ""), ("E", "F", ""), ("F", "G", ""),
        ],
        "gates": (0, 0, 0),
        "notes": "Human Class IIIa Foxp3 switch — expanded with IL-2/STAT5 and TGF-β/SMAD3 inputs.",
    },
    "human_cebpa_myeloid_commitment": {
        "nodes": [
            ("A", "[G-CSF / myeloid cue]", "red"),
            ("B", "[C/EBPα]", "yellow"),
            ("C", "[\\C/EBPα autoactivation/]", "green"),
            ("D", "[/Antagonizes PU.1 alternative fate/]", "green"),
            ("E", "[Myeloid genes: Mpo, Elane]", "green"),
            ("F", "(Committed myeloid cell)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "B", "+"),
            ("B", "D", ""), ("B", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 1),
        "notes": "Human Class IIIa C/EBPα switch — expanded with G-CSF cue and PU.1 antagonism.",
    },
    "human_myod_myogenesis": {
        "nodes": [
            ("A", "[Wnt / Shh myogenic cue]", "red"),
            ("B", "[MyoD bHLH]", "yellow"),
            ("C", "[\\MyoD autoactivation/]", "green"),
            ("D", "[MEF2 cooperation at E-box]", "green"),
            ("E", "[p21 → cell-cycle exit]", "green"),
            ("F", "(Committed myoblast)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "B", "+"),
            ("B", "D", ""), ("D", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 0),
        "notes": "Human Class IIIa MyoD switch — expanded with MEF2 cooperation and p21 cell-cycle exit.",
    },
    "human_estrogen_receptor_switch": {
        "nodes": [
            ("A", "[Estrogen ligand]", "red"),
            ("B", "[ERα + SRC coactivator]", "yellow"),
            ("C", "[\\ERα activates ESR1/]", "green"),
            ("D", "[Cyclin D1 / MYC targets]", "green"),
            ("E", "[Proliferative ERE program]", "green"),
            ("F", "(Bistable ER+ luminal state)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "B", "+"),
            ("B", "D", ""), ("D", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 0),
        "notes": "Human Class IIIa ERα switch — expanded with coactivator and proliferative targets.",
    },
    "human_cgas_sting_dna_sensing": {
        "nodes": [
            ("A", "[Cytosolic dsDNA]", "red"),
            ("B", "[cGAS binds DNA]", "yellow"),
            ("C", "[2'3'-cGAMP synthesized]", "blue"),
            ("D", "[STING activated at ER]", "yellow"),
            ("E", "[TBK1 phosphorylates IRF3]", "green"),
            ("F", "[Type-I interferon induced]", "blue"),
            ("G", "[/STING trafficked + degraded/]", "green"),
            ("H", "(Resolved antiviral response)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "E", ""),
            ("E", "F", ""), ("F", "G", ""), ("G", "E", "⊣ feedback"), ("F", "H", ""),
        ],
        "gates": (0, 0, 1),
        "notes": "Human Class II cGAS-STING — expanded with cGAMP messenger and STING trafficking.",
    },
    "drosophila_gap_gene_network": {
        "nodes": [
            ("A", "[Bicoid + Caudal gradients]", "red"),
            ("B", "[hunchback (hb)]", "yellow"),
            ("C", "[Krüppel (Kr)]", "yellow"),
            ("D", "[giant (gt)]", "yellow"),
            ("E", "[knirps (kni)]", "yellow"),
            ("F", "[\\Gap genes mutual repression/]", "green"),
            ("G", "[Sharp domain boundaries]", "blue"),
            ("H", "(Multistable AP gap pattern)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("A", "C", ""), ("A", "D", ""), ("A", "E", ""),
            ("B", "F", ""), ("C", "F", ""), ("D", "F", ""), ("E", "F", ""),
            ("F", "B", "⊣"), ("F", "C", "⊣"), ("F", "D", "⊣"), ("F", "E", "⊣"),
            ("B", "G", ""), ("G", "H", ""),
        ],
        "gates": (0, 0, 1),
        "notes": "Ground-truth Drosophila gap-gene network — expanded with named gap genes and mutual repression.",
    },
    "drosophila_segment_polarity": {
        "nodes": [
            ("A", "[Pair-rule prepattern]", "red"),
            ("B", "[engrailed (en)]", "yellow"),
            ("C", "[hedgehog (hh)]", "yellow"),
            ("D", "[patched (ptc) in neighbors]", "yellow"),
            ("E", "[wingless (wg)]", "yellow"),
            ("F", "[Ci activator in receiving cell]", "green"),
            ("G", "[\\Wg maintains en/hh/]", "green"),
            ("H", "[\\Hh sustains wg via Ci/]", "green"),
            ("I", "(Bistable segment boundary)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("A", "E", ""), ("B", "C", ""), ("B", "G", ""),
            ("G", "E", "+"), ("C", "H", ""), ("H", "F", ""), ("F", "E", "+"),
            ("E", "D", ""), ("B", "I", ""),
        ],
        "gates": (0, 0, 0),
        "notes": "Ground-truth Drosophila segment-polarity module — expanded with en/hh/wg/ptc/Ci nodes.",
    },
}


def find_process_path(process_id: str) -> Path | None:
    for path in PROC_DIR.rglob(f"{process_id}.json"):
        return path
    return None


def apply_one(path: Path, expansion: dict) -> bool:
    proc = json.loads(path.read_text(encoding="utf-8"))
    nodes, edges = expansion["nodes"], expansion["edges"]
    gates = expansion.get("gates", (
        proc.get("logicGates", {}).get("or", 0),
        proc.get("logicGates", {}).get("and", 0),
        proc.get("logicGates", {}).get("not", 0),
    ))
    stats = compute_stats(nodes, edges)
    proc["mermaid"] = build_mermaid(nodes, edges)
    proc["totalNodes"] = stats["nodes"]
    proc["edges"] = stats["edges"]
    proc["loops"] = stats["loops"]
    proc["conditionals"] = stats["conditionals"]
    proc["logicGates"] = {"or": gates[0], "and": gates[1], "not": gates[2]}
    proc["notGates"] = gates[2]
    proc["complexity"]["nodes"] = stats["nodes"]
    proc["complexity"]["logicGates"] = {
        "orGates": gates[0], "andGates": gates[1], "total": gates[0] + gates[1],
    }
    if "notes" in expansion:
        proc["notes"] = expansion["notes"]
    proc["lastUpdated"] = "2026-06-13"
    proc["qualityAudit"] = {"expanded": True, "expansionDate": "2026-06-13", "reason": "thin pathway schematic"}
    path.write_text(json.dumps(proc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    missing = []
    for pid, exp in EXPANSIONS.items():
        path = find_process_path(pid)
        if not path:
            missing.append(pid)
            continue
        if args.apply:
            apply_one(path, exp)
            print(f"Expanded {pid}: {exp['nodes'].__len__()} nodes")
        else:
            print(f"Would expand {pid}: → {len(exp['nodes'])} nodes")
    if missing:
        print(f"Missing: {missing}")
    if not args.apply:
        print("Re-run with --apply to write.")


if __name__ == "__main__":
    main()
