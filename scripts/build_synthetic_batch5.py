#!/usr/bin/env python3
"""
Batch 5 of synthetic-biology ground-truth circuits (extends build_synthetic_batch1-4).
Population-level and spatial circuits, plus a second Class V self-modifying device.

Coverage:
  Class I  : light sensor (bacterial photography), multicellular edge detector
  Class IV : synchronized quorum-of-clocks population oscillator
  Class V  : recombinase-based counter / DNA state machine (self-modifying DNA)

Reuses Batch 1 helpers so schema/stats stay identical.
Output: glmp-v2/processes/synthetic/<id>.json
"""

import json

from build_synthetic_batch1 import make_process, OUT_DIR

SPECS = [
    # ----------------------------------------------------------------- Class IV
    {
        "id": "synthetic_synchronized_qs_oscillator",
        "name": "Synchronized Quorum-of-Clocks Oscillator",
        "circuitClass": "IV",
        "topologyType": "quorum_coupled_delayed_neg_feedback_oscillator",
        "rationale": "Each cell runs a LuxI/AHL positive arm and a delayed aiiA-degradation negative arm; the diffusible AHL couples and synchronizes thousands of cellular oscillators into a population-wide rhythm (Danino, Mondragón-Palomino, Tsimring & Hasty 2010). Delayed negative feedback with oscillation — Class IV.",
        "description": "A synthetic oscillator that synchronizes across a colony. In every cell, LuxR-AHL activates luxI (positive feedback, making more AHL) and aiiA (which degrades AHL with delay, negative feedback). Because AHL diffuses between cells, the autoinducer couples the individual clocks into coherent, population-wide oscillations.",
        "scientificAccuracy": "Ground-truth circuit. Synchronized quorum-sensing oscillations were built and imaged in microfluidics by Danino et al. (2010).",
        "nodes": [
            ("A", "[Cell population]", "red"),
            ("B", "[LuxI makes AHL]", "green"),
            ("C", "[AHL diffuses + synchronizes]", "blue"),
            ("D", "[\\LuxR-AHL activates luxI/]", "green"),
            ("E", "[/aiiA degrades AHL, delayed/]", "green"),
            ("F", "(Synchronized population oscillation)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "B", "+"),
            ("C", "E", ""), ("E", "C", "⊣ delayed"), ("C", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "A synchronized quorum of genetic clocks", "authors": "Danino T, Mondragón-Palomino O, Tsimring L, Hasty J", "journal": "Nature", "year": 2010, "volume": "463", "pages": "326-330", "pmid": "20090747", "doi": "10.1038/nature08753"},
        ],
        "keywords": ["synchronized oscillator", "quorum sensing", "LuxI", "aiiA", "population coupling", "Class IV", "ground truth"],
        "relatedProcesses": ["synthetic_repressilator", "synthetic_population_control"],
        "notes": "Ground-truth Class IV population oscillator: positive (luxI) + delayed negative (aiiA) feedback, coupled by diffusible AHL.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Plux (drives luxI and aiiA)", "boundFactor": "LuxR-AHL", "operator": "IF / delayed NOT", "effect": "activates synthesis (luxI) and degradation (aiiA) of AHL", "sequenceMotif": "ACCTGTAGGATCGTACAGGT (lux box)", "note": "AHL diffusion couples cells"},
            ],
            "derivedLogic": "luxI = +AHL ; aiiA = -AHL(delayed) -> synchronized oscillation",
            "references": ["Danino et al. 2010"],
        },
    },
    # ----------------------------------------------------------------- Class V
    {
        "id": "synthetic_recombinase_counter",
        "name": "Recombinase DNA Counter / State Machine",
        "circuitClass": "V",
        "topologyType": "self_modifying_dna_state_machine",
        "rationale": "Each input pulse expresses a recombinase that flips a DNA register, advancing a permanently DNA-encoded count; the circuit rewrites its own genome to store state, the defining feature of the self-modifying (Class V) rung (Friedland et al. 2009; Roquet et al. 2016).",
        "description": "A genetically encoded counter. Successive input pulses drive recombinases that sequentially invert DNA registers, so the cell's DNA records how many pulses have occurred. Because the state is stored in the DNA sequence itself (and is heritable), the device is a self-modifying state machine rather than an expression-level circuit.",
        "scientificAccuracy": "Ground-truth circuit. DNA-based counters and recombinase state machines were built and characterized (Friedland et al. 2009; Roquet et al. 2016).",
        "nodes": [
            ("A", "[Input pulses]", "red"),
            ("B", "[Recombinase per pulse]", "yellow"),
            ("C", "[\\Each pulse inverts a DNA register/]", "green"),
            ("D", "[DNA-encoded count state advances]", "blue"),
            ("E", "[Output reflects pulse count]", "green"),
            ("F", "(Heritable counter / state machine)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "Synthetic gene networks that count", "authors": "Friedland AE, Lu TK, Wang X, Shi D, Church G, Collins JJ", "journal": "Science", "year": 2009, "volume": "324", "pages": "1199-1202", "pmid": "19478183", "doi": "10.1126/science.1172005"},
            {"title": "Synthetic recombinase-based state machines in living cells", "authors": "Roquet N, Soleimany AP, Ferris AC, Aaronson S, Lu TK", "journal": "Science", "year": 2016, "volume": "353", "pages": "aad8559", "pmid": "27463678", "doi": "10.1126/science.aad8559"},
        ],
        "keywords": ["counter", "recombinase", "state machine", "self-modifying DNA", "memory", "Class V", "ground truth"],
        "relatedProcesses": ["synthetic_integrase_memory", "yeast_sup35_prion"],
        "notes": "Ground-truth Class V: DNA-rewriting state machine (self-modifying genetic state).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "ordered recombination registers", "boundFactor": "orthogonal recombinases", "operator": "SELF-MODIFY (sequential)", "effect": "irreversible DNA inversions encode a count", "sequenceMotif": "attB/attP register array", "note": "state stored in DNA, heritable"},
            ],
            "derivedLogic": "DNA_state := advance(DNA_state) per pulse -> DNA-encoded count",
            "references": ["Roquet et al. 2016"],
        },
    },
    # ----------------------------------------------------------------- Class I
    {
        "id": "synthetic_light_sensor",
        "name": "Light Sensor (Bacterial Photography)",
        "circuitClass": "I",
        "topologyType": "photoreceptor_feed_forward_sensor",
        "rationale": "A chimeric red-light photoreceptor (Cph8 = phytochrome fused to the EnvZ kinase) represses an output promoter in the light, so a bacterial lawn prints a high-resolution image. A pure feed-forward light-to-output sensor. Class I.",
        "description": "The bacterial 'camera'. The Cph8 fusion couples a cyanobacterial phytochrome to the EnvZ histidine kinase: red light switches its kinase activity, controlling the ompC promoter so that pigment is produced only in the dark. A lawn of these cells reproduces a projected image — a feed-forward sensor with no regulatory loop.",
        "scientificAccuracy": "Ground-truth circuit. The Cph8 light sensor and bacterial photography were built by Levskaya et al. (2005).",
        "nodes": [
            ("A", "[Red light pattern]", "red"),
            ("B", "[Cph8 phytochrome senses light]", "yellow"),
            ("C", "[/Light represses ompC promoter/]", "green"),
            ("D", "[Pigment produced in dark only]", "green"),
            ("E", "(Bacterial photograph)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", "⊣"), ("D", "E", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Synthetic biology: engineering Escherichia coli to see light", "authors": "Levskaya A, Chevalier AA, Tabor JJ, et al.", "journal": "Nature", "year": 2005, "volume": "438", "pages": "441-442", "pmid": "16306980", "doi": "10.1038/nature04405"},
        ],
        "keywords": ["light sensor", "optogenetics", "Cph8", "phytochrome", "feed-forward", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_edge_detector"],
        "notes": "Ground-truth Class I sensor (feed-forward; one repression, no feedback loop).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "ompC promoter", "boundFactor": "OmpR~P (set by Cph8/EnvZ light state)", "operator": "NOT(light)", "effect": "repression in light", "sequenceMotif": "OmpR boxes", "note": "light state transduced via two-component phosphorelay"},
            ],
            "derivedLogic": "Output = NOT light (per-pixel sensor)",
            "references": ["Levskaya et al. 2005"],
        },
    },
    {
        "id": "synthetic_edge_detector",
        "name": "Multicellular Edge Detector",
        "circuitClass": "I",
        "topologyType": "feed_forward_AND_edge_detection",
        "rationale": "Combines the light sensor with quorum sensing so a cell makes pigment only where it is dark AND adjacent to light (a diffusible signal from lit cells): output = dark AND neighbor-lit. Feed-forward with one AND — Class I — that computes image edges (Tabor et al. 2009).",
        "description": "A community computation: cells detect the boundary between light and dark. Lit cells secrete a diffusible signal; a cell produces pigment only if it is itself in the dark AND close enough to lit neighbors to receive the signal. The AND of 'dark' and 'neighbor-lit' is true only at edges, so the colony outlines the projected image.",
        "scientificAccuracy": "Ground-truth circuit. The genetic edge-detection program was built and characterized by Tabor et al. (2009).",
        "nodes": [
            ("A", "[Projected light pattern]", "red"),
            ("B", "[Dark-sensing branch active]", "yellow"),
            ("C", "[Lit neighbors secrete AHL]", "yellow"),
            ("D", "{dark AND neighbor-lit?}", "blue"),
            ("E", "[Pigment produced at boundary]", "green"),
            ("F", "(Edge-detected image)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("A", "C", ""),
            ("B", "D", ""), ("C", "D", ""), ("D", "E", "Yes"), ("E", "F", ""),
        ],
        "gates": (0, 1, 0),
        "sources": [
            {"title": "A synthetic genetic edge detection program", "authors": "Tabor JJ, Salis HM, Simpson ZB, et al.", "journal": "Cell", "year": 2009, "volume": "137", "pages": "1272-1281", "pmid": "19563759", "doi": "10.1016/j.cell.2009.04.048"},
        ],
        "keywords": ["edge detection", "multicellular", "quorum sensing", "AND gate", "feed-forward", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_light_sensor", "synthetic_band_detector"],
        "notes": "Ground-truth Class I image-processing circuit: AND of light sensing and quorum sensing, no feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "edge-output promoter", "boundFactor": "dark-state regulator + LuxR-AHL", "operator": "AND", "effect": "pigment only where dark and near light", "sequenceMotif": "(dark-responsive + lux box)", "note": "computes spatial edges"},
            ],
            "derivedLogic": "Output = dark AND neighbor-lit -> edges",
            "references": ["Tabor et al. 2009"],
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
                     proc["edges"], proc["loops"], proc["logicGates"]))
    print(f"Wrote {len(rows)} synthetic Batch-5 process files -> {OUT_DIR}\n")
    print(f"{'id':<42} {'cls':<4} {'nodes':<6} {'edges':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<42} {r[1]:<4} {r[2]:<6} {r[3]:<6} {r[4]:<6} {r[5]}")


if __name__ == "__main__":
    main()
