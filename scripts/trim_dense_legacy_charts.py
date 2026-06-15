#!/usr/bin/env python3
"""
Replace dense legacy LLM flowcharts with regulatory-core topology schematics.

Phase A (this script): seven charts with the worst legacy loop inflation.
Phase B (future): remaining ~98 dense microbial charts (detailLevel=detailed).

Run:
  python3 scripts/trim_dense_legacy_charts.py
  python3 scripts/trim_dense_legacy_charts.py --apply
  python3 scripts/compute_regulatory_cycles.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_synthetic_batch1 import build_mermaid, compute_stats
from mermaid_graph import compute_regulatory_stats

PROC_DIR = ROOT / "glmp-v2" / "processes"

# nodes: (id, label_with_shape, color); edges: (src, dst, label); gates: (or, and, not)
REGULATORY_CORE: dict[str, dict] = {
    "ecoli_antibiotic_efflux_pumps": {
        "nodes": [
            ("A", "[Antibiotic exposure]", "red"),
            ("B", "[Inducers (salicylate, bile, tetracycline)]", "red"),
            ("C", "[/MarR repressor on mar/]", "blue"),
            ("D", "[MarA / SoxS / Rob activators]", "yellow"),
            ("E", "{Efflux promoters derepressed?}", "blue"),
            ("F", "[acrAB & RND pump transcription]", "green"),
            ("G", "[AcrAB-TolC tripartite assembly]", "yellow"),
            ("H", "[Antibiotic substrate at pump]", "blue"),
            ("I", "{PMF or ATP available?}", "blue"),
            ("J", "[Active antibiotic efflux]", "green"),
            ("K", "[Reduced intracellular drug]", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", "derepress"), ("C", "D", ""), ("D", "E", ""),
            ("E", "F", ""), ("F", "G", ""), ("A", "H", ""), ("G", "H", ""),
            ("H", "I", ""), ("I", "J", ""), ("J", "K", ""),
        ],
        "gates": (0, 1, 1),
        "notes": "Regulatory-core efflux execution schematic (Class I). Replaces dense LLM chart; MarR/SoxS/MarA induction and AcrAB-TolC export only.",
    },
    "ecoli_protein_folding_chaperones": {
        "nodes": [
            ("A", "[Nascent polypeptide on ribosome]", "red"),
            ("B", "[Trigger Factor / DnaK-DnaJ capture]", "yellow"),
            ("C", "[DnaK-GrpE ATPase folding cycle]", "green"),
            ("D", "[Folded intermediate]", "blue"),
            ("E", "{Requires GroEL/GroES?}", "blue"),
            ("F", "[GroEL/GroES chamber folding]", "yellow"),
            ("G", "[Native folded protein]", "violet"),
            ("H", "[Persistent misfold → protease]", "green"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "F", "yes"), ("F", "G", ""),
            ("E", "G", "no"), ("D", "H", "chronic misfold"),
        ],
        "gates": (0, 0, 0),
        "notes": "Regulatory-core chaperone execution schematic (Class I). DnaK/DnaJ/GrpE and GroEL/GroES decision branch only.",
    },
    "ecoli_e._coli_osmotic_stress_response": {
        "nodes": [
            ("A", "[High external osmolarity]", "red"),
            ("B", "[Turgor loss / water efflux]", "red"),
            ("C", "[RpoS (σS) stabilized]", "yellow"),
            ("D", "[Osmoprotectant gene transcription]", "green"),
            ("E", "[Compatible solute accumulation]", "green"),
            ("F", "[\\Turgor & cell volume restored/]", "blue"),
            ("G", "(Osmotic homeostasis)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "E", ""),
            ("E", "F", ""), ("F", "B", "− feedback"), ("F", "G", ""),
        ],
        "gates": (0, 0, 0),
        "notes": "Regulatory-core osmoadaptation negative-feedback homeostat (Class II). RpoS-driven compatible-solute accumulation restores turgor.",
    },
    "yeast_yeast_glycolysis_regulation": {
        "nodes": [
            ("A", "[Glucose uptake]", "red"),
            ("B", "[Hexokinase (Hxk)]", "yellow"),
            ("C", "[G6P pool]", "blue"),
            ("D", "[/G6P inhibits Hxk/]", "green"),
            ("E", "[Phosphofructokinase (Pfk-1)]", "yellow"),
            ("F", "[F1,6BP]", "blue"),
            ("G", "[Pyruvate kinase (Pyk)]", "yellow"),
            ("H", "[ATP / glycolytic flux]", "violet"),
            ("I", "[/High ATP inhibits Pfk-1/]", "green"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "B", "−"),
            ("C", "E", ""), ("E", "F", ""), ("F", "G", ""), ("G", "H", ""),
            ("H", "I", ""), ("I", "E", "−"),
        ],
        "gates": (0, 0, 0),
        "notes": "Regulatory-core glycolysis allosteric feedback (Class II). G6P product inhibition of Hxk and ATP inhibition of Pfk-1.",
    },
    "yeast_dna_replication": {
        "nodes": [
            ("A", "[Origin licensing (ORC/Cdc6/Cdt1)]", "red"),
            ("B", "[Pre-replicative complex at ARS]", "yellow"),
            ("C", "[Cdc45-MCM-GINS helicase activation]", "green"),
            ("D", "[Leading / lagging strand synthesis]", "yellow"),
            ("E", "[Okazaki fragment maturation]", "green"),
            ("F", "[Replication fork progression]", "green"),
            ("G", "[Checkpoint pause (Rad53/Mrc1)]", "blue"),
            ("H", "[S-phase completion]", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "E", ""),
            ("E", "F", ""), ("G", "C", "pause on damage"), ("F", "H", ""),
        ],
        "gates": (0, 0, 0),
        "notes": "Regulatory-core replication execution schematic (Class I). Origin licensing through fork progression with damage checkpoint arm.",
    },
    "ecoli_peptidoglycan_biosynthesis": {
        "nodes": [
            ("A", "[UDP-GlcNAc / UDP-MurNAc precursors]", "red"),
            ("B", "[Stem-peptide ligases (MurD–MurF)]", "yellow"),
            ("C", "[Lipid II (undecaprenyl-P-P-Mur-GlcNAc)]", "blue"),
            ("D", "[Glycosyltransfer → glycan chain elongation]", "green"),
            ("E", "[Transpeptidase cross-linking]", "green"),
            ("F", "[Sacculus expansion / cell growth]", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 0),
        "notes": "Regulatory-core peptidoglycan biosynthesis execution schematic (Class I). Linear lipid-II pathway without spurious metabolic convergence hubs.",
    },
    "yeast_ribosome_biogenesis": {
        "nodes": [
            ("A", "[rDNA transcription (Pol I)]", "red"),
            ("B", "[35S pre-rRNA processing]", "green"),
            ("C", "[Ribosomal protein assembly]", "yellow"),
            ("D", "[SSU / LSU subunit maturation]", "green"),
            ("E", "[Nuclear export]", "green"),
            ("F", "[Mature 40S / 60S ribosome]", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 0),
        "notes": "Regulatory-core ribosome biogenesis execution schematic (Class I). rRNA transcription through subunit export.",
    },
}

# Ground-truth Class III chart that lost its intercellular feedback loop during expansion.
SEGMENT_POLARITY_FIX: dict = {
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
        ("G", "E", "+"), ("E", "B", "+ maintain en"), ("C", "H", ""),
        ("H", "F", ""), ("F", "E", "+"), ("E", "D", ""), ("B", "I", ""),
    ],
    "gates": (0, 0, 0),
    "notes": "Restored wg↔en/hh intercellular feedback cycle (Class III) lost in prior expansion.",
}


def find_process_path(process_id: str) -> Path | None:
    for path in PROC_DIR.rglob(f"{process_id}.json"):
        return path
    return None


def apply_trim(path: Path, spec: dict, reason: str) -> dict:
    proc = json.loads(path.read_text(encoding="utf-8"))
    nodes, edges = spec["nodes"], spec["edges"]
    gates = spec.get("gates", (0, 0, 0))
    mermaid = build_mermaid(nodes, edges)
    stats = compute_regulatory_stats(mermaid)

    proc["mermaid"] = mermaid
    proc["totalNodes"] = stats["nodes"]
    proc["edges"] = stats["edges"]
    proc["loops"] = stats["loops"]
    proc["feedbackEdges"] = stats["feedbackEdges"]
    proc["conditionals"] = stats["conditionals"]
    proc["logicGates"] = {"or": gates[0], "and": gates[1], "not": gates[2]}
    proc["notGates"] = gates[2]
    proc["complexity"]["nodes"] = stats["nodes"]
    proc["complexity"]["detailLevel"] = "regulatory_core"
    proc["complexity"]["logicGates"] = {
        "orGates": gates[0], "andGates": gates[1], "total": gates[0] + gates[1],
    }
    if "notes" in spec:
        proc["notes"] = spec["notes"]
    proc["lastUpdated"] = "2026-06-13"
    proc["qualityAudit"] = {
        "regulatoryCoreTrimmed": True,
        "trimDate": "2026-06-13",
        "reason": reason,
    }
    path.write_text(json.dumps(proc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    all_specs = {**REGULATORY_CORE, "drosophila_segment_polarity": SEGMENT_POLARITY_FIX}
    missing = []

    for pid, spec in all_specs.items():
        path = find_process_path(pid)
        if not path:
            missing.append(pid)
            continue
        reason = "phase_a_dense_legacy_trim" if pid in REGULATORY_CORE else "segment_polarity_cycle_restore"
        if args.apply:
            stats = apply_trim(path, spec, reason)
            print(f"Trimmed {pid}: {stats['nodes']} nodes, {stats['loops']} loops (was legacy-inflated)")
        else:
            mermaid = build_mermaid(spec["nodes"], spec["edges"])
            stats = compute_regulatory_stats(mermaid)
            print(f"Would trim {pid}: → {stats['nodes']} nodes, {stats['loops']} loops")

    if missing:
        print(f"Missing: {missing}")
    if not args.apply:
        print("Re-run with --apply to write.")


if __name__ == "__main__":
    main()
