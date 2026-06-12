#!/usr/bin/env python3
"""
Batch 2 of the GLMP collection: canonical *human* regulatory circuits, with emphasis
on the Class III(a) persistent bistable switch that motivates the RPE1/RegVelo work.

These are the human counterparts to the bacterial/yeast circuits already in the
collection and are directly relevant to the K562 Perturb-seq empirical sequel
(Paper III). Each carries an authored circuit class (curated from human literature)
and a sequenceAnnotation block mapping human TF binding motifs to logical operators.

Honest class assignment (the ladder applied to human circuits, not forced to one class):
  - GATA1 / PU.1     -> III  (persistent bistable, "IIIa": mutual repression + dual autoactivation)
  - p53 / MDM2       -> IV   (delayed negative feedback -> damped oscillations; Lahav et al. 2004)
  - MYC              -> II   (negative autoregulation of its own promoter; Penn et al. 1990)
  - VHL / HIF        -> II   (PHD/VHL negative-feedback oxygen homeostasis; switch-like O2 response)

Reuses the Batch 1 helpers so schema/stats stay identical.
Output: glmp-v2/processes/human/<id>.json
"""

import json
from pathlib import Path

from build_synthetic_batch1 import (
    COLOR_SCHEME, CLASS_NAME, build_mermaid, compute_stats,
)

OUT_DIR = Path("glmp-v2/processes/human")
ORGANISM = "Homo sapiens"


def make_process(spec):
    nodes, edges = spec["nodes"], spec["edges"]
    stats = compute_stats(nodes, edges)
    or_g, and_g, not_g = spec["gates"]
    cls = spec["circuitClass"]
    return {
        "id": spec["id"],
        "name": spec["name"],
        "organism": ORGANISM,
        "category": spec["category"],
        "description": spec["description"],
        "scientificAccuracy": spec["scientificAccuracy"],
        "complexity": {
            "nodes": stats["nodes"],
            "uniqueIdentifiers": True,
            "colorCoded": True,
            "detailLevel": "curated",
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
        "verifiedBy": "Curated from primary human regulatory-biology literature",
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
        "circuitClassEvidence": "curated_literature",
        "groundTruth": True,
        "circuitSubclass": spec.get("circuitSubclass"),
    }


SPECS = [
    {
        "id": "human_gata1_pu1_switch",
        "name": "GATA1–PU.1 Hematopoietic Lineage Switch",
        "category": "Hematopoiesis",
        "circuitClass": "III",
        "circuitSubclass": "IIIa",
        "topologyType": "mutual_repression_dual_autoactivation_bistable",
        "rationale": "GATA1 and PU.1 (SPI1) repress each other and each activates its own expression. Mutual repression plus dual positive autoregulation is the textbook persistent bistable (Class IIIa) cell-fate switch governing the erythroid/megakaryocyte vs. myeloid decision.",
        "description": "The master switch of myeloid-erythroid commitment. GATA1 and PU.1 bind and inhibit each other's activity while each reinforces its own expression. The double-negative-plus-autoactivation topology has two stable states, locking a multipotent progenitor into either the erythroid/megakaryocyte or the myeloid program — the canonical human Class IIIa bistable switch.",
        "scientificAccuracy": "Mutual antagonism (protein-protein inhibition + cross-repression) and autoregulation are established for GATA1/PU.1; the bistable interpretation follows standard developmental-systems-biology modeling (Huang et al. 2007; Graf & Enver 2009).",
        "nodes": [
            ("A", "[Multipotent progenitor / CMP]", "red"),
            ("B", "[GATA1]", "yellow"),
            ("C", "[PU.1 / SPI1]", "yellow"),
            ("D", "[\\GATA1 autoactivation/]", "green"),
            ("E", "[\\PU.1 autoactivation/]", "green"),
            ("F", "[/GATA1 represses PU.1/]", "green"),
            ("G", "[/PU.1 represses GATA1/]", "green"),
            ("H", "(Erythroid / megakaryocyte fate)", "violet"),
            ("I", "(Myeloid fate)", "violet"),
        ],
        "edges": [
            ("A", "B", ""),
            ("A", "C", ""),
            ("B", "D", ""),
            ("D", "B", "+"),
            ("C", "E", ""),
            ("E", "C", "+"),
            ("B", "F", ""),
            ("F", "C", "⊣"),
            ("C", "G", ""),
            ("G", "B", "⊣"),
            ("B", "H", ""),
            ("C", "I", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "Bifurcation dynamics in lineage-commitment in bipotent progenitor cells", "authors": "Huang S, Guo YP, May G, Enver T", "journal": "Developmental Biology", "year": 2007, "volume": "305", "pages": "695-713", "pmid": "17412320", "doi": "10.1016/j.ydbio.2007.02.036"},
            {"title": "Forcing cells to change lineages", "authors": "Graf T, Enver T", "journal": "Nature", "year": 2009, "volume": "462", "pages": "587-594", "pmid": "19956253", "doi": "10.1038/nature08533"},
        ],
        "keywords": ["GATA1", "PU.1", "SPI1", "bistable switch", "mutual repression", "hematopoiesis", "cell fate", "Class IIIa", "ground truth"],
        "relatedProcesses": ["synthetic_toggle_switch"],
        "notes": "Flagship human Class IIIa bistable switch. Two cross-repressions (NOT) plus two autoactivations create the double-positive/double-negative bistability.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "GATA motif (target & self enhancers)", "boundFactor": "GATA1", "operator": "IF", "effect": "activation (self) / repression (PU.1 loci)", "sequenceMotif": "WGATAR", "note": "GATA1 occupies its own enhancers (autoactivation) and antagonizes PU.1"},
                {"name": "ETS / PU-box", "boundFactor": "PU.1 (SPI1)", "operator": "IF", "effect": "activation (self) / repression (GATA1 loci)", "sequenceMotif": "AGAGGAAGTG", "note": "purine-rich ETS core GGAA; PU.1 autoactivates and antagonizes GATA1"},
            ],
            "derivedLogic": "GATA1 = GATA1 AND NOT PU.1 ; PU.1 = PU.1 AND NOT GATA1  -> two stable fates",
            "references": ["Huang et al. 2007", "Graf & Enver 2009"],
        },
    },
    {
        "id": "human_p53_mdm2",
        "name": "p53–MDM2 DNA-Damage Response Oscillator",
        "category": "Tumor Suppressor",
        "circuitClass": "IV",
        "topologyType": "delayed_negative_feedback_oscillator",
        "rationale": "p53 transcriptionally induces MDM2, and MDM2 ubiquitinates p53 for degradation — a delayed negative-feedback loop that produces a train of p53 pulses after DNA damage (Lahav et al. 2004). Delayed negative feedback with oscillation is Class IV.",
        "description": "The core DNA-damage response loop: DNA damage activates ATM/ATR, which stabilizes p53; p53 induces its own negative regulator MDM2, which targets p53 for degradation. The transcription-degradation delay turns this negative-feedback loop into an oscillator — repeated p53 pulses whose number tunes the cell-fate outcome.",
        "scientificAccuracy": "p53→MDM2→p53 negative feedback and damage-induced p53 pulses are directly measured at the single-cell level (Lahav et al. 2004; Batchelor et al. 2011).",
        "nodes": [
            ("A", "[DNA damage]", "red"),
            ("B", "[ATM / ATR active]", "green"),
            ("C", "[p53 stabilized]", "yellow"),
            ("D", "[Target transcription: p21, PUMA]", "green"),
            ("E", "[MDM2 expressed]", "yellow"),
            ("F", "[/MDM2 ubiquitinates p53/]", "green"),
            ("G", "(p53 pulses: arrest or apoptosis)", "violet"),
        ],
        "edges": [
            ("A", "B", ""),
            ("B", "C", ""),
            ("C", "D", ""),
            ("C", "E", ""),
            ("E", "F", ""),
            ("F", "C", "⊣ delayed"),
            ("D", "G", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Dynamics of the p53-Mdm2 feedback loop in individual cells", "authors": "Lahav G, Rosenfeld N, Sigal A, Geva-Zatorsky N, Levine AJ, Elowitz MB, Alon U", "journal": "Nature Genetics", "year": 2004, "volume": "36", "pages": "147-150", "pmid": "14730303", "doi": "10.1038/ng1293"},
            {"title": "Stimulus-dependent dynamics of p53 in single cells", "authors": "Batchelor E, Loewer A, Mock C, Lahav G", "journal": "Molecular Systems Biology", "year": 2011, "volume": "7", "pages": "488", "pmid": "21556066", "doi": "10.1038/msb.2011.20"},
        ],
        "keywords": ["p53", "MDM2", "negative feedback", "oscillator", "DNA damage", "tumor suppressor", "Class IV", "ground truth"],
        "relatedProcesses": ["synthetic_negative_autoregulation", "synthetic_repressilator"],
        "notes": "Human Class IV oscillator. One delayed repression (NOT) closes the negative-feedback loop driving p53 pulses.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "p53 response element (MDM2 P2 promoter)", "boundFactor": "p53 tetramer", "operator": "IF", "effect": "activation of MDM2", "sequenceMotif": "RRRCWWGYYY-RRRCWWGYYY", "note": "two decameric half-sites; p53 induces its own antagonist"},
                {"name": "MDM2-p53 degron", "boundFactor": "MDM2 (E3 ligase)", "operator": "NOT", "effect": "ubiquitination -> p53 degradation", "sequenceMotif": "(protein-level)", "note": "closes the negative-feedback loop with delay"},
            ],
            "derivedLogic": "MDM2 = p53 ; p53 = NOT MDM2(t-τ)  -> delayed negative feedback -> pulses",
            "references": ["Lahav et al. 2004"],
        },
    },
    {
        "id": "human_myc_autoregulation",
        "name": "MYC Proliferation Hub with Autosuppression",
        "category": "Oncogene Signaling",
        "circuitClass": "II",
        "topologyType": "negative_autoregulation_hub",
        "rationale": "MYC is induced by mitogenic signaling and represses its own promoter (MYC autosuppression; Penn et al. 1990). The dominant local feedback on MYC level is negative autoregulation — Class II — even though MYC acts as a broad feed-forward amplifier on its targets.",
        "description": "MYC sits downstream of mitogenic (Wnt/ERK) signaling and, as a MYC-MAX dimer, activates a large E-box target program driving proliferation and metabolism. MYC also suppresses transcription from its own promoter, a negative-autoregulation loop that keeps MYC levels bounded; loss of this autosuppression is a recurrent feature of MYC-driven cancers.",
        "scientificAccuracy": "MYC autosuppression of its own promoter and MYC-MAX E-box activation are well established (Penn et al. 1990; Grandori et al. 2000).",
        "nodes": [
            ("A", "[Mitogenic signal: Wnt / ERK]", "red"),
            ("B", "[MYC transcription]", "green"),
            ("C", "[MYC-MAX dimer]", "yellow"),
            ("D", "[E-box target activation]", "green"),
            ("E", "[/MYC suppresses own promoter/]", "green"),
            ("F", "(Proliferation / metabolism program)", "violet"),
        ],
        "edges": [
            ("A", "B", ""),
            ("B", "C", ""),
            ("C", "D", ""),
            ("C", "E", ""),
            ("E", "B", "⊣"),
            ("D", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Negative autoregulation of c-myc transcription", "authors": "Penn LJ, Brooks MW, Laufer EM, Land H", "journal": "EMBO Journal", "year": 1990, "volume": "9", "pages": "1113-1121", "pmid": "2182320", "doi": "10.1002/j.1460-2075.1990.tb08217.x"},
            {"title": "The Myc/Max/Mad network and the transcriptional control of cell behavior", "authors": "Grandori C, Cowley SM, James LP, Eisenman RN", "journal": "Annual Review of Cell and Developmental Biology", "year": 2000, "volume": "16", "pages": "653-699", "pmid": "11031250", "doi": "10.1146/annurev.cellbio.16.1.653"},
        ],
        "keywords": ["MYC", "negative autoregulation", "E-box", "oncogene", "proliferation", "Class II", "ground truth"],
        "relatedProcesses": ["synthetic_negative_autoregulation"],
        "notes": "Human Class II circuit (negative autoregulation). The human analogue of the bacterial NAR ground-truth motif.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "E-box (target promoters)", "boundFactor": "MYC-MAX", "operator": "IF", "effect": "activation", "sequenceMotif": "CACGTG", "note": "canonical MYC-MAX E-box"},
                {"name": "MYC P2 promoter", "boundFactor": "MYC", "operator": "NOT", "effect": "autosuppression", "sequenceMotif": "(MYC P2 region)", "note": "negative autoregulation bounding MYC level"},
            ],
            "derivedLogic": "targets = MYC-MAX(E-box) ; MYC = mitogen AND NOT MYC  (autosuppression)",
            "references": ["Penn et al. 1990"],
        },
    },
    {
        "id": "human_vhl_hif_oxygen_sensing",
        "name": "VHL–HIF Oxygen-Sensing Homeostat",
        "category": "Hypoxia Signaling",
        "circuitClass": "II",
        "topologyType": "phd_vhl_negative_feedback_homeostat",
        "rationale": "In normoxia PHD enzymes hydroxylate HIF-1α, flagging it for VHL-mediated degradation; hypoxia stabilizes HIF-1α, which induces PHD2/PHD3 — a negative-feedback loop that restores oxygen homeostasis. Switch-like in O2 but homeostatic in topology — Class II.",
        "description": "The cellular oxygen sensor. Under normoxia, prolyl hydroxylases (PHDs) modify HIF-1α so the VHL E3 ligase destroys it. Under hypoxia HIF-1α is stabilized, dimerizes with HIF-1β, and activates hypoxia-response genes (VEGF, EPO, glycolytic enzymes) — including PHD2/PHD3, which feed back negatively to re-tune the set-point.",
        "scientificAccuracy": "PHD-dependent hydroxylation, VHL-mediated degradation, and HIF-induced PHD2/PHD3 negative feedback are established (Kaelin & Ratcliffe 2008, Nobel-recognized oxygen-sensing pathway).",
        "nodes": [
            ("A", "[O2 / 2-oxoglutarate]", "red"),
            ("B", "{Normoxia?}", "blue"),
            ("C", "[PHD hydroxylates HIF-1α]", "green"),
            ("D", "[VHL E3 ubiquitin ligase]", "yellow"),
            ("E", "[\\HIF-1α degraded/]", "green"),
            ("F", "[HIF-1α stabilized]", "yellow"),
            ("G", "[HIF-1α/HIF-1β + HRE]", "green"),
            ("H", "(VEGF, EPO, glycolysis)", "violet"),
            ("I", "[/Induces PHD2 / PHD3/]", "green"),
        ],
        "edges": [
            ("A", "B", ""),
            ("B", "C", "Yes"),
            ("C", "D", ""),
            ("D", "E", ""),
            ("B", "F", "No: hypoxia"),
            ("F", "G", ""),
            ("G", "H", ""),
            ("G", "I", ""),
            ("I", "C", "⊣ feedback"),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Oxygen sensing by metazoans: the central role of the HIF hydroxylase pathway", "authors": "Kaelin WG Jr, Ratcliffe PJ", "journal": "Molecular Cell", "year": 2008, "volume": "30", "pages": "393-402", "pmid": "18498744", "doi": "10.1016/j.molcel.2008.04.009"},
        ],
        "keywords": ["VHL", "HIF-1", "hypoxia", "oxygen sensing", "PHD", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["synthetic_negative_autoregulation"],
        "notes": "Human Class II homeostat. Switch-like O2 response with HIF-induced PHD negative feedback (one feedback edge).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "HRE (hypoxia response element)", "boundFactor": "HIF-1α/HIF-1β", "operator": "IF", "effect": "activation", "sequenceMotif": "RCGTG", "note": "HIF heterodimer binds HRE in hypoxia targets including PHD2/PHD3"},
                {"name": "HIF-1α ODD degron", "boundFactor": "PHD -> VHL", "operator": "NOT", "effect": "O2-dependent hydroxylation -> degradation", "sequenceMotif": "(protein-level, Pro402/Pro564)", "note": "normoxic OFF-switch; feedback via HIF-induced PHDs"},
            ],
            "derivedLogic": "HIF targets = NOT O2 ; PHD = HIF target  -> negative-feedback O2 homeostat",
            "references": ["Kaelin & Ratcliffe 2008"],
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
        rows.append((proc["id"], proc["circuitClass"], proc.get("circuitSubclass") or "-",
                     proc["totalNodes"], proc["edges"], proc["loops"], proc["logicGates"]))
    print(f"Wrote {len(rows)} human process files -> {OUT_DIR}\n")
    print(f"{'id':<36} {'cls':<4} {'sub':<5} {'nodes':<6} {'edges':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<36} {r[1]:<4} {r[2]:<5} {r[3]:<6} {r[4]:<6} {r[5]:<6} {r[6]}")


if __name__ == "__main__":
    main()
