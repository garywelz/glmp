#!/usr/bin/env python3
"""
Ground-truth mouse circuits (Mus musculus) — cross-organism ortholog anchors for the
grammar-decoding program (collaboration plan Batch 5).

  mouse_gata1_spi1_switch      -> III (IIIa)  ortholog of human GATA1/PU.1 lineage switch
  mouse_sox2_oct4_pluripotency -> III (IIIa)  ortholog of human OCT4/SOX2/NANOG pluripotency
  mouse_p53_mdm2_oscillator    -> IV          ortholog of human p53-MDM2 delayed-feedback oscillator

Writes to glmp-v2/processes/mouse/. Run scripts/integrate_mouse_groundtruth.py after.
Note: adds organism "Mus musculus"; viewer (processLoader.js) and database table updated
for the mouse_ prefix.
"""

import json
from pathlib import Path

from build_microbial_groundtruth import make_process

OUT_DIR = Path("glmp-v2/processes/mouse")
ORGANISM = "Mus musculus"

SPECS = [
    {
        "id": "mouse_gata1_spi1_switch",
        "name": "Mouse GATA1–SPI1 Hematopoietic Switch",
        "organism": ORGANISM,
        "category": "Hematopoiesis",
        "circuitClass": "III",
        "circuitSubclass": "IIIa",
        "topologyType": "mutual_repression_dual_autoactivation_bistable",
        "rationale": "Mouse Gata1 and Spi1 (PU.1) cross-repress and each autoactivates, giving the same persistent bistable erythroid/megakaryocyte vs. myeloid switch topology as the human ortholog — a cross-organism anchor for the universal grammar hypothesis. Class IIIa.",
        "description": "The mouse hematopoietic master switch. Gata1 and Spi1 antagonize each other while reinforcing their own expression, locking multipotent progenitors into either the erythroid/megakaryocyte or myeloid program. Topology is conserved with human GATA1/PU.1 despite different binding motifs.",
        "scientificAccuracy": "Mutual Gata1/Spi1 antagonism and bistable lineage choice in mouse are established (Nerlov & Graf 2007; Huang et al. 2007).",
        "nodes": [
            ("A", "[Mouse CMP / progenitor]", "red"),
            ("B", "[Gata1]", "yellow"),
            ("C", "[Spi1 / PU.1]", "yellow"),
            ("D", "[\\Gata1 autoactivation/]", "green"),
            ("E", "[\\Spi1 autoactivation/]", "green"),
            ("F", "[/Gata1 represses Spi1/]", "green"),
            ("G", "[/Spi1 represses Gata1/]", "green"),
            ("H", "(Erythroid / megakaryocyte)", "violet"),
            ("I", "(Myeloid fate)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("A", "C", ""), ("B", "D", ""), ("D", "B", "+"),
            ("C", "E", ""), ("E", "C", "+"), ("B", "F", ""), ("F", "C", "⊣"),
            ("C", "G", ""), ("G", "B", "⊣"), ("B", "H", ""), ("C", "I", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "PU.1 induces the commitment of multipotent progenitors to the myeloid lineage", "authors": "Nerlov C, Graf T", "journal": "Genes & Development", "year": 2007, "volume": "21", "pages": "1313-1326", "pmid": "17510284", "doi": "10.1101/gad.1522707"},
            {"title": "Bifurcation dynamics in lineage-commitment in bipotent progenitor cells", "authors": "Huang S, Guo YP, May G, Enver T", "journal": "Developmental Biology", "year": 2007, "volume": "305", "pages": "695-713", "pmid": "17412320", "doi": "10.1016/j.ydbio.2007.02.036"},
        ],
        "keywords": ["Gata1", "Spi1", "PU.1", "mouse", "hematopoiesis", "bistable", "Class IIIa", "ground truth", "ortholog"],
        "relatedProcesses": ["human_gata1_pu1_switch", "mouse_sox2_oct4_pluripotency"],
        "notes": "Mouse Class IIIa ortholog of human GATA1/PU.1 switch — conserved bistable topology.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Gata1 autoregulatory enhancer (G1HE)", "boundFactor": "Gata1", "operator": "positive autoregulation", "effect": "sustains Gata1", "sequenceMotif": "WGATAR (GATA motif)", "note": "mouse motifs differ from human but topology conserved"},
                {"name": "Spi1 autoregulatory upstream element", "boundFactor": "Spi1", "operator": "positive autoregulation", "effect": "sustains Spi1", "sequenceMotif": "GGAA (ETS motif)", "note": "cross-repression with Gata1"},
            ],
            "derivedLogic": "Erythroid = Gata1 AND NOT Spi1 ; Myeloid = Spi1 AND NOT Gata1",
            "references": ["Nerlov & Graf 2007"],
        },
    },
    {
        "id": "mouse_sox2_oct4_pluripotency",
        "name": "Mouse Sox2–Oct4 Pluripotency Switch",
        "organism": ORGANISM,
        "category": "Pluripotency",
        "circuitClass": "III",
        "circuitSubclass": "IIIa",
        "topologyType": "mutual_activation_positive_feedback_bistable",
        "rationale": "Oct4 (Pou5f1) and Sox2 co-bind and activate each other's enhancers plus Nanog, forming a self-sustaining pluripotency network; the cooperative positive feedback creates a persistent stem-cell attractor. Class IIIa — mouse ortholog of the human OCT4/SOX2/NANOG circuit.",
        "description": "The mouse pluripotency lock. Sox2 and Oct4 bind composite Sox-Oct motifs to cross-activate their own regulatory elements and Nanog, maintaining the embryonic-stem-cell state. The mutual positive feedback is the archetypal persistent Class IIIa attractor tested in mouse reprogramming experiments.",
        "scientificAccuracy": "Oct4-Sox2 mutual activation and pluripotency maintenance in mouse ES cells are established (Masui et al. 2007; Niwa et al. 2000).",
        "nodes": [
            ("A", "[Differentiation cues absent]", "red"),
            ("B", "[Oct4 / Pou5f1]", "yellow"),
            ("C", "[Sox2]", "yellow"),
            ("D", "[\\Oct4-Sox2 activate Oct4 enhancer/]", "green"),
            ("E", "[\\Oct4-Sox2 activate Sox2 enhancer/]", "green"),
            ("F", "[Nanog sustained]", "green"),
            ("G", "(Pluripotent ES cell state)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("A", "C", ""), ("B", "D", ""), ("D", "B", "+"),
            ("C", "E", ""), ("E", "C", "+"), ("B", "F", ""), ("C", "F", ""),
            ("F", "G", ""), ("B", "G", ""), ("C", "G", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "Pluripotency governed by Sox2 via regulation of Oct3/4 expression in mouse embryonic stem cells", "authors": "Masui S, Nakatake Y, Toyooka Y, et al.", "journal": "Genes & Development", "year": 2007, "volume": "21", "pages": "2754-2769", "pmid": "17908933", "doi": "10.1101/gad.1583407"},
            {"title": "Quantitative expression of Oct-3/4 defines differentiation, dedifferentiation or self-renewal of ES cells", "authors": "Niwa H, Miyazaki J, Smith AG", "journal": "Nature Genetics", "year": 2000, "volume": "24", "pages": "372-376", "pmid": "10742100", "doi": "10.1038/74199"},
        ],
        "keywords": ["Sox2", "Oct4", "Pou5f1", "Nanog", "pluripotency", "mouse", "Class IIIa", "ground truth", "ortholog"],
        "relatedProcesses": ["human_oct4_sox2_nanog_pluripotency", "mouse_gata1_spi1_switch"],
        "notes": "Mouse Class IIIa pluripotency attractor — ortholog of human OCT4/SOX2/NANOG network.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Oct4 distal enhancer (DE)", "boundFactor": "Oct4 + Sox2", "operator": "AND (cooperative)", "effect": "sustains Pou5f1", "sequenceMotif": "Sox-Oct composite motif", "note": "mouse ES-cell ground truth"},
                {"name": "Sox2 enhancer (SRR2)", "boundFactor": "Oct4 + Sox2", "operator": "AND (cooperative)", "effect": "sustains Sox2", "sequenceMotif": "Sox-Oct composite motif", "note": "mutual activation loop"},
            ],
            "derivedLogic": "Pluripotency = Oct4 AND Sox2 (mutual activation) -> Nanog",
            "references": ["Masui et al. 2007"],
        },
    },
    {
        "id": "mouse_p53_mdm2_oscillator",
        "name": "Mouse p53–Mdm2 Oscillator",
        "organism": ORGANISM,
        "category": "DNA Damage Response",
        "circuitClass": "IV",
        "topologyType": "delayed_negative_feedback_oscillator",
        "rationale": "DNA damage stabilizes mouse p53, which transcribes Mdm2; Mdm2 protein accumulates with delay, ubiquitinates p53 and exports it, lowering p53 — a delayed negative-feedback loop that produces damped p53 pulses. Class IV — mouse ortholog of the human p53–MDM2 oscillator (Lahav et al. 2004).",
        "description": "The mouse DNA-damage oscillator. Stress stabilizes Trp53 (p53), which induces Mdm2; after a transcription/translation delay Mdm2 tags p53 for degradation, terminating the pulse. The interlocked delayed repression generates the stereotyped p53 pulses observed in single MEF cells after γ-irradiation.",
        "scientificAccuracy": "p53–Mdm2 delayed negative feedback and pulsatile dynamics in mouse cells are established (Lahav et al. 2004; Geva-Zatorsky et al. 2006).",
        "nodes": [
            ("A", "[DNA damage / stress]", "red"),
            ("B", "[p53 stabilized]", "yellow"),
            ("C", "[Mdm2 transcribed]", "green"),
            ("D", "[Mdm2 protein accumulates]", "blue"),
            ("E", "[/Mdm2 degrades p53/]", "green"),
            ("F", "(p53 pulse / oscillation)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", "delay"), ("D", "E", ""),
            ("E", "B", "⊣"), ("B", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Dynamics of the p53-Mdm2 feedback loop in individual cells", "authors": "Lahav G, Rosenfeld N, Sigal A, et al.", "journal": "Nature Genetics", "year": 2004, "volume": "36", "pages": "147-150", "pmid": "14730303", "doi": "10.1038/ng1293"},
            {"title": "Oscillations and variability in the p53 system", "authors": "Geva-Zatorsky N, Rosenfeld N, Itzkovitz S, et al.", "journal": "Molecular Systems Biology", "year": 2006, "volume": "2", "pages": "2006.0033", "pmid": "16773083", "doi": "10.1038/msb4100068"},
        ],
        "keywords": ["p53", "Mdm2", "Trp53", "oscillator", "mouse", "Class IV", "ground truth", "ortholog"],
        "relatedProcesses": ["human_p53_mdm2", "human_p53_apoptosis_decision"],
        "notes": "Mouse Class IV ortholog of human p53–MDM2 oscillator (delayed negative feedback).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Mdm2 promoter (p53-responsive)", "boundFactor": "p53", "operator": "IF damage (conditional induction)", "effect": "Mdm2 transcription", "sequenceMotif": "RRRCWWGYYY (p53 RE)", "note": "Mdm2 protein feeds back to degrade p53 -> pulse"},
            ],
            "derivedLogic": "Mdm2 = IF p53 ; Mdm2 -| p53 (delayed) -> oscillation",
            "references": ["Lahav et al. 2004"],
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
        rows.append((proc["id"], proc["organism"], proc["circuitClass"],
                     proc.get("circuitSubclass") or "-", proc["totalNodes"],
                     proc["loops"], proc["logicGates"]))
    print(f"Wrote {len(rows)} mouse ground-truth files -> {OUT_DIR}\n")
    print(f"{'id':<32} {'organism':<16} {'cls':<4} {'sub':<5} {'nodes':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<32} {r[1]:<16} {r[2]:<4} {r[3]:<5} {r[4]:<6} {r[5]:<6} {r[6]}")


if __name__ == "__main__":
    main()
