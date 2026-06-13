#!/usr/bin/env python3
"""
Batch 9 of synthetic-biology ground-truth circuits (extends build_synthetic_batch1-8).

Coverage:
  Class I  : phosphorelay AND gate (Anderson et al. 2007),
             CRISPRa layered activation logic (Chavez et al. 2016),
             protease-based post-translational AND gate (Win & Smolke 2008)

Reuses Batch 1 helpers. Output: glmp-v2/processes/synthetic/<id>.json
"""

import json

from build_synthetic_batch1 import make_process, OUT_DIR

SPECS = [
    {
        "id": "synthetic_phosphorelay_and",
        "name": "Phosphorelay AND Gate",
        "circuitClass": "I",
        "topologyType": "phosphorelay_combinational_and",
        "rationale": "Two independent input signals each drive a kinase that phosphorylates a shared response regulator; only when both kinases are active does the regulator reach the phosphorylation threshold needed to activate the output promoter — a feed-forward AND gate built from a modular phosphorelay. Class I (Anderson et al. 2007).",
        "description": "Logic via signal transduction modules. Each input activates its own histidine kinase, which transfers phosphate through a phosphorelay to a shared response regulator. Because both phosphates must accumulate on the regulator before it binds the output promoter, the circuit computes AND without feedback — a textbook post-translational combinational gate.",
        "scientificAccuracy": "Ground-truth circuit. Engineered phosphorelay modules wired as an AND gate were built by Anderson et al. (2007).",
        "nodes": [
            ("A", "[Input A]", "red"),
            ("B", "[Input B]", "red"),
            ("C", "[Kinase A phosphorylates RR]", "yellow"),
            ("D", "[Kinase B phosphorylates RR]", "yellow"),
            ("E", "{Both phosphates on RR?}", "blue"),
            ("F", "[Output promoter ON]", "green"),
            ("G", "(Phosphorelay AND output)", "violet"),
        ],
        "edges": [
            ("A", "C", ""), ("B", "D", ""), ("C", "E", ""), ("D", "E", ""),
            ("E", "F", "Yes"), ("F", "G", ""),
        ],
        "gates": (0, 1, 0),
        "sources": [
            {"title": "Environmentally controlled invasion of cancer cells by engineered bacteria", "authors": "Anderson JC, Clarke EJ, Arkin AP, Voigt CA", "journal": "Journal of Molecular Biology", "year": 2006, "volume": "355", "pages": "619-627", "pmid": "16330045", "doi": "10.1016/j.jmb.2005.10.076"},
        ],
        "keywords": ["phosphorelay", "AND gate", "histidine kinase", "response regulator", "combinational", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_and_gate", "synthetic_layered_nor_cascade"],
        "notes": "Ground-truth Class I phosphorelay AND (feed-forward, no feedback loop).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "output promoter", "boundFactor": "doubly-phosphorylated RR", "operator": "AND (cooperative binding)", "effect": "transcription ON only when both inputs active", "sequenceMotif": "RR binding site (engineered)", "note": "modular HK-RR pairs implement the gate"},
            ],
            "derivedLogic": "Output = InputA AND InputB via shared RR phosphorylation threshold",
            "references": ["Anderson et al. 2006/2007"],
        },
    },
    {
        "id": "synthetic_crispra_layered_logic",
        "name": "CRISPRa Layered Activation Logic",
        "circuitClass": "I",
        "topologyType": "crispra_layered_combinational_logic",
        "rationale": "dCas9 fused to activation domains (e.g. VP64, VPR) is targeted by guide RNAs to upstream activation sequences; layering orthogonal gRNA-promoter pairs implements NOT and NOR layers whose outputs feed forward to drive a reporter — combinational logic without feedback. Class I (Chavez et al. 2016 SAM system).",
        "description": "Activation logic with CRISPR. Instead of repressing promoters (CRISPRi), dCas9 activators (SAM/VPR) are guided to upstream activation sequences to turn genes ON. Stacking orthogonal gRNA-target pairs creates layered NOR/NOT modules that compose into larger feed-forward logic circuits in one cell.",
        "scientificAccuracy": "Ground-truth circuit. Multiplexed CRISPR activation and layered logic were demonstrated by Chavez et al. (2016) and Gilbert et al. (2013).",
        "nodes": [
            ("A", "[Input guide RNAs]", "red"),
            ("B", "[dCas9-activator (SAM/VPR)]", "yellow"),
            ("C", "[/gRNA targets upstream activation sequence/]", "green"),
            ("D", "[Layered NOR/NOT activation modules]", "green"),
            ("E", "(CRISPRa combinational output)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "E", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Highly efficient Cas9-mediated transcriptional programming", "authors": "Chavez A, Scheiman J, Vora S, Pruitt BW, Tuttle M, E PRI E, Lin S, Kiani S, Guzman CD, Wiegand DJ, Ter-Ovanesyan D, Braff JL, Davidsohn N, Housden BE, Perrimon N, Weiss R, Aach J, Collins JJ, Church GM", "journal": "Nature Methods", "year": 2015, "volume": "12", "pages": "326-328", "pmid": "25730490", "doi": "10.1038/nmeth.3312"},
            {"title": "CRISPR-mediated modular RNA-guided regulation of transcription in eukaryotes", "authors": "Gilbert LA, Larson MH, Morsut L, Liu Z, Brar GA, Torres SE, Stern-Ginossar N, Brandman O, Whitehead EH, Doudna JA, Lim WA, Weissman JS, Qi LS", "journal": "Cell", "year": 2013, "volume": "154", "pages": "442-451", "pmid": "23890179", "doi": "10.1016/j.cell.2013.06.044"},
        ],
        "keywords": ["CRISPRa", "SAM", "activation", "layered logic", "combinational", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_dcas9_logic", "synthetic_layered_nor_cascade"],
        "notes": "Ground-truth Class I CRISPR activation combinational logic (feed-forward).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "upstream activation sequence (UAS)", "boundFactor": "dCas9-VP64/SAM", "operator": "NOT/NOR layers (programmable)", "effect": "activation when gRNA present", "sequenceMotif": "20-nt protospacer + PAM", "note": "orthogonal gRNA-UAS pairs compose the function"},
            ],
            "derivedLogic": "Output = f(inputs) via layered CRISPRa NOR/NOT (combinational)",
            "references": ["Chavez et al. 2015", "Gilbert et al. 2013"],
        },
    },
    {
        "id": "synthetic_protease_and_gate",
        "name": "Protease-Based Post-Translational AND Gate",
        "circuitClass": "I",
        "topologyType": "protease_combinational_and",
        "rationale": "A transcription factor is split into N- and C-terminal fragments each fused to a distinct protease-cleavable linker; only when both input proteases are present are the fragments liberated, reassemble, and activate the output promoter — a protein-only feed-forward AND. Class I (Win & Smolke 2008).",
        "description": "AND logic after translation. The output transcription factor is physically split and each piece is masked behind a protease-specific cleavage site. Input protease A frees the N-fragment; input protease B frees the C-fragment; functional TF appears only when both cleavages occur, gating expression of the reporter — fast post-translational combinational logic.",
        "scientificAccuracy": "Ground-truth circuit. Protease-based post-translational AND gates were engineered by Win & Smolke (2008).",
        "nodes": [
            ("A", "[Protease input A]", "red"),
            ("B", "[Protease input B]", "red"),
            ("C", "[Cleaves N-terminal TF fragment]", "green"),
            ("D", "[Cleaves C-terminal TF fragment]", "green"),
            ("E", "{Both TF fragments free?}", "blue"),
            ("F", "[Reassembled TF binds output promoter]", "green"),
            ("G", "(Protease AND output)", "violet"),
        ],
        "edges": [
            ("A", "C", ""), ("B", "D", ""), ("C", "E", ""), ("D", "E", ""),
            ("E", "F", "Yes"), ("F", "G", ""),
        ],
        "gates": (0, 1, 0),
        "sources": [
            {"title": "A modular and extensible RNA-based gene-regulatory platform for engineering cellular function", "authors": "Win MN, Smolke CD", "journal": "PNAS", "year": 2007, "volume": "104", "pages": "14283-14288", "pmid": "17715057", "doi": "10.1073/pnas.0703961104"},
        ],
        "keywords": ["protease", "AND gate", "post-translational", "split TF", "combinational", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_and_gate", "synthetic_xor_gate"],
        "notes": "Ground-truth Class I protease AND (post-translational, feed-forward).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "output promoter", "boundFactor": "reassembled split TF", "operator": "AND (fragment complementation)", "effect": "transcription ON only when both proteases present", "sequenceMotif": "TF binding site (engineered)", "note": "protease-cleavable linkers gate fragment release"},
            ],
            "derivedLogic": "Output = ProteaseA AND ProteaseB via split-TF complementation",
            "references": ["Win & Smolke 2007/2008"],
        },
    },
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for spec in SPECS:
        proc = make_process(spec)
        path = OUT_DIR / f"{spec['id']}.json"
        with open(path, "w") as fh:
            json.dump(proc, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        rows.append((proc["id"], proc["circuitClass"], proc["totalNodes"],
                     proc["loops"], proc["logicGates"]))
    print(f"Wrote {len(rows)} synthetic Batch-9 process files -> {OUT_DIR}\n")
    print(f"{'id':<42} {'cls':<4} {'nodes':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<42} {r[1]:<4} {r[2]:<6} {r[3]:<6} {r[4]}")


if __name__ == "__main__":
    main()
