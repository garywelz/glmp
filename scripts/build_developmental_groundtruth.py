#!/usr/bin/env python3
"""
Ground-truth developmental circuits from two new model organisms — Drosophila
melanogaster and Caenorhabditis elegans — broadening the eukaryotic developmental
coverage of the collection.

  drosophila_gap_gene_network   -> III  Bicoid -> gap-gene cross-repression patterning (Jaeger 2011)
  drosophila_segment_polarity   -> III  wg/en/hh bistable segment-boundary module (von Dassow 2000)
  celegans_dauer_decision       -> III  insulin/TGF-β dauer vs reproductive switch (Hu 2007)
  celegans_heterochronic_clock  -> I    lin-4/let-7 microRNA developmental timing cascade (Ambros 2011)

Writes to glmp-v2/processes/{drosophila,celegans}/. Run scripts/integrate_developmental_groundtruth.py after.
Adds organisms "Drosophila melanogaster" and "Caenorhabditis elegans"; the viewer
(processLoader.js) and database table recognize the drosophila_/celegans_ prefixes.
"""

import json
from pathlib import Path

from build_microbial_groundtruth import make_process

BASE = Path("glmp-v2/processes")


def out_dir_for(pid):
    if pid.startswith("drosophila_"):
        return BASE / "drosophila"
    if pid.startswith("celegans_"):
        return BASE / "celegans"
    raise ValueError(f"unknown organism prefix: {pid}")


SPECS = [
    {
        "id": "drosophila_gap_gene_network",
        "name": "Drosophila Gap-Gene Patterning Network",
        "organism": "Drosophila melanogaster",
        "category": "Developmental Patterning",
        "circuitClass": "III",
        "topologyType": "cross_repression_multistable_patterning",
        "rationale": "The maternal Bicoid/Caudal gradients switch on the gap genes (hunchback, Krüppel, giant, knirps), which mutually cross-repress; the mutual repression sharpens broad inputs into discrete, multistable expression domains with precise boundaries. Class III (positive-feedback/multistable patterning).",
        "description": "Anterior-posterior pre-patterning of the fly embryo. Maternal morphogen gradients (Bicoid, Caudal) provide graded positional input that activates the zygotic gap genes; the gap proteins then mutually repress one another, and that cross-repression converts smooth gradients into sharply bounded, mutually exclusive expression domains — a multistable spatial switch that sets up the downstream stripes.",
        "scientificAccuracy": "Gap-gene cross-repression and boundary sharpening are established (Jaeger 2011; Clyde et al. 2003).",
        "nodes": [
            ("A", "[Bicoid + Caudal gradients]", "red"),
            ("B", "[Gap genes: hb, Kr, gt, kni]", "yellow"),
            ("C", "[\\Gap genes cross-repress/]", "green"),
            ("D", "[Sharp gap-domain boundaries]", "blue"),
            ("E", "[Positional information for stripes]", "green"),
            ("F", "(Multistable AP gap pattern)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "B", "⊣ mutual"),
            ("B", "D", ""), ("D", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "The gap gene network", "authors": "Jaeger J", "journal": "Cellular and Molecular Life Sciences", "year": 2011, "volume": "68", "pages": "243-274", "pmid": "20927566", "doi": "10.1007/s00018-010-0536-y"},
            {"title": "A self-organizing system of repressor gradients establishes segmental complexity in Drosophila", "authors": "Clyde DE, Corado MSG, Wu X, et al.", "journal": "Nature", "year": 2003, "volume": "426", "pages": "849-853", "pmid": "14685241", "doi": "10.1038/nature02189"},
        ],
        "keywords": ["gap genes", "Bicoid", "hunchback", "Kruppel", "cross-repression", "Drosophila", "patterning", "Class III", "ground truth"],
        "relatedProcesses": ["drosophila_segment_polarity", "human_gata1_pu1_switch"],
        "notes": "Ground-truth Drosophila Class III multistable patterning: morphogen input + gap-gene cross-repression.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "gap-gene CRMs (e.g., eve, hb enhancers)", "boundFactor": "Bicoid (activator) + gap repressors", "operator": "IF (Bcd) AND NOT (other gap)", "effect": "graded activation + mutual repression", "sequenceMotif": "TAATCC (Bicoid); gap-repressor sites", "note": "cross-repression sets domain boundaries"},
            ],
            "derivedLogic": "gap_i = Bcd AND NOT gap_j (mutual) -> discrete multistable domains",
            "references": ["Jaeger 2011"],
        },
    },
    {
        "id": "drosophila_segment_polarity",
        "name": "Segment-Polarity Network (wg/en/hh)",
        "organism": "Drosophila melanogaster",
        "category": "Developmental Patterning",
        "circuitClass": "III",
        "topologyType": "intercellular_positive_feedback_bistable_module",
        "rationale": "Adjacent cells expressing engrailed/hedgehog and wingless reinforce each other across the boundary — Wg sustains en/hh and Hh sustains wg — an intercellular positive-feedback loop that locks in a stable, self-maintaining segment boundary robust to perturbation. Class III (von Dassow et al. 2000).",
        "description": "Maintenance of segment boundaries after the pair-rule prepattern fades. Engrailed/Hedgehog-expressing cells and adjacent Wingless-expressing cells form a reciprocal signaling loop: Wingless maintains engrailed/hedgehog in neighbors, and Hedgehog maintains wingless, so the boundary becomes a bistable, self-stabilizing module famously robust to parameter changes.",
        "scientificAccuracy": "The robust, self-maintaining segment-polarity module was demonstrated computationally and experimentally (von Dassow et al. 2000).",
        "nodes": [
            ("A", "[Pair-rule prepattern]", "red"),
            ("B", "[engrailed + hedgehog cells]", "yellow"),
            ("C", "[wingless in neighbor cells]", "yellow"),
            ("D", "[\\Wg sustains en/hh/]", "green"),
            ("E", "[\\Hh sustains wg/]", "green"),
            ("F", "(Bistable self-maintaining boundary)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("A", "C", ""), ("B", "D", ""),
            ("D", "C", "+"), ("C", "E", ""), ("E", "B", "+"), ("B", "F", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "The segment polarity network is a robust developmental module", "authors": "von Dassow G, Meir E, Munro EM, Odell GM", "journal": "Nature", "year": 2000, "volume": "406", "pages": "188-192", "pmid": "10910359", "doi": "10.1038/35018085"},
        ],
        "keywords": ["segment polarity", "wingless", "engrailed", "hedgehog", "positive feedback", "bistable", "Drosophila", "Class III", "ground truth"],
        "relatedProcesses": ["drosophila_gap_gene_network", "human_notch_delta"],
        "notes": "Ground-truth Drosophila Class III intercellular bistable module (wg/en/hh boundary maintenance).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "en / wg enhancers", "boundFactor": "Ci (Hh pathway) / TCF (Wg pathway)", "operator": "IF / reciprocal positive feedback", "effect": "cross-maintenance of en/hh and wg", "sequenceMotif": "Ci sites; TCF/HMG sites", "note": "intercellular positive feedback -> bistable boundary"},
            ],
            "derivedLogic": "en/hh = IF Wg ; wg = IF Hh (reciprocal positive) -> stable boundary",
            "references": ["von Dassow et al. 2000"],
        },
    },
    {
        "id": "celegans_dauer_decision",
        "name": "C. elegans Dauer Developmental Switch",
        "organism": "Caenorhabditis elegans",
        "category": "Developmental Decision",
        "circuitClass": "III",
        "topologyType": "signal_integrated_bistable_decision",
        "rationale": "Favorable conditions keep insulin (DAF-2) and TGF-β (DAF-7) signaling high, driving reproductive development; adversity lowers them, freeing DAF-16/DAF-3 to commit to the dauer larva, a decision reinforced by feedback into an all-or-none, long-lived arrested state. Class III bistable decision (Hu 2007).",
        "description": "A larva-stage life-or-death bet. Crowding, scarce food, and dauer pheromone are integrated through insulin/IGF (DAF-2) and TGF-β (DAF-7) pathways: high signaling promotes reproductive growth; low signaling releases the FOXO factor DAF-16 and DAF-3 to commit to the stress-resistant, non-aging dauer larva. Reinforcing feedback makes the commitment switch-like.",
        "scientificAccuracy": "Integration of insulin/TGF-β signaling into the dauer decision is established (Hu 2007; Golden & Riddle 1984).",
        "nodes": [
            ("A", "[Crowding / low food / pheromone]", "red"),
            ("B", "{favorable conditions?}", "blue"),
            ("C", "[DAF-2 insulin + DAF-7 TGF-β high]", "green"),
            ("D", "(Reproductive development)", "violet"),
            ("E", "[/Low signaling: DAF-16 + DAF-3 active/]", "green"),
            ("F", "[\\Commit to dauer larva/]", "green"),
            ("G", "(Dauer arrest, stress-resistant)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", "Yes"), ("C", "D", ""),
            ("B", "E", "No"), ("E", "F", ""), ("F", "E", "+ commit"), ("F", "G", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Dauer", "authors": "Hu PJ", "journal": "WormBook", "year": 2007, "volume": "", "pages": "1-19", "pmid": "17988075", "doi": "10.1895/wormbook.1.144.1"},
            {"title": "A pheromone influences larval development in the nematode Caenorhabditis elegans", "authors": "Golden JW, Riddle DL", "journal": "Science", "year": 1982, "volume": "218", "pages": "578-580", "pmid": "6896933", "doi": "10.1126/science.6896933"},
        ],
        "keywords": ["dauer", "DAF-2", "DAF-7", "DAF-16", "insulin", "TGF-beta", "decision", "C. elegans", "Class III", "ground truth"],
        "relatedProcesses": ["human_insulin_akt_foxo", "bacillus_spo0a_sporulation"],
        "notes": "Ground-truth C. elegans Class III developmental decision (dauer vs reproductive), signal-integrated and switch-like.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "DAF-16/FOXO targets (dauer + longevity genes)", "boundFactor": "DAF-16 (gated by DAF-2/AKT)", "operator": "IF / NOT(insulin)", "effect": "activation of dauer/stress program when signaling low", "sequenceMotif": "TTGTTTAC (DAF-16 binding element)", "note": "TGF-β (DAF-7) input integrated in parallel"},
            ],
            "derivedLogic": "dauer = NOT (DAF-2 AND DAF-7) ; commitment feedback -> bistable",
            "references": ["Hu 2007"],
        },
    },
    {
        "id": "celegans_heterochronic_clock",
        "name": "Heterochronic microRNA Timing Cascade",
        "organism": "Caenorhabditis elegans",
        "category": "Developmental Timing",
        "circuitClass": "I",
        "topologyType": "feed_forward_temporal_cascade",
        "rationale": "Stage-specific microRNAs act in an ordered relay — lin-4 rises to repress lin-14, then let-7 rises to repress lin-41 — driving each larval-to-adult transition; the sequential repression is a feed-forward temporal cascade with no feedback loop. Class I (Ambros 2011; Reinhart et al. 2000).",
        "description": "The worm's developmental stopwatch. Heterochronic microRNAs are expressed in sequence: lin-4 accumulates to switch off lin-14 (ending the L1 program), and later let-7 accumulates to switch off lin-41 (enabling the adult program). Each microRNA gates the next stage, producing the correct temporal order of cell fates as a feed-forward cascade.",
        "scientificAccuracy": "The lin-4/lin-14 and let-7/lin-41 heterochronic relay is established (Lee et al. 1993; Reinhart et al. 2000; Ambros 2011).",
        "nodes": [
            ("A", "[Developmental time cues]", "red"),
            ("B", "[lin-4 microRNA rises]", "green"),
            ("C", "[/Represses lin-14/]", "green"),
            ("D", "[let-7 microRNA rises later]", "green"),
            ("E", "[/Represses lin-41/]", "green"),
            ("F", "[Stage fates: L1 to adult]", "green"),
            ("G", "(Ordered temporal patterning)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", "⊣ lin-14"), ("C", "D", ""),
            ("D", "E", "⊣ lin-41"), ("E", "F", ""), ("F", "G", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "The C. elegans heterochronic gene lin-4 encodes small RNAs with antisense complementarity to lin-14", "authors": "Lee RC, Feinbaum RL, Ambros V", "journal": "Cell", "year": 1993, "volume": "75", "pages": "843-854", "pmid": "8252621", "doi": "10.1016/0092-8674(93)90529-Y"},
            {"title": "The 21-nucleotide let-7 RNA regulates developmental timing in Caenorhabditis elegans", "authors": "Reinhart BJ, Slack FJ, Basson M, et al.", "journal": "Nature", "year": 2000, "volume": "403", "pages": "901-906", "pmid": "10706289", "doi": "10.1038/35002607"},
        ],
        "keywords": ["heterochronic", "lin-4", "let-7", "lin-14", "lin-41", "microRNA", "timing", "feed-forward", "C. elegans", "Class I", "ground truth"],
        "relatedProcesses": ["ecoli_flhdc_flagellar", "human_circadian_clock"],
        "notes": "Ground-truth C. elegans Class I temporal cascade (lin-4 -> let-7 microRNA relay), feed-forward.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "lin-14 / lin-41 3'UTRs", "boundFactor": "lin-4 / let-7 microRNAs", "operator": "NOT (sequential)", "effect": "stage-specific translational repression", "sequenceMotif": "miRNA seed-complementary sites in 3'UTR", "note": "ordered relay times the stages"},
            ],
            "derivedLogic": "lin-14 = NOT lin-4 ; lin-41 = NOT let-7 (later) -> staged timing",
            "references": ["Lee et al. 1993", "Reinhart et al. 2000"],
        },
    },
]


def main():
    rows = []
    for spec in SPECS:
        proc = make_process(spec)
        d = out_dir_for(spec["id"])
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"{spec['id']}.json"
        with open(path, "w") as fh:
            json.dump(proc, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        rows.append((proc["id"], proc["organism"], proc["circuitClass"],
                     proc["totalNodes"], proc["loops"], proc["logicGates"]))
    print(f"Wrote {len(rows)} developmental ground-truth files\n")
    print(f"{'id':<32} {'organism':<26} {'cls':<4} {'nodes':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<32} {r[1]:<26} {r[2]:<4} {r[3]:<6} {r[4]:<6} {r[5]}")


if __name__ == "__main__":
    main()
