#!/usr/bin/env python3
"""
Batch 6 of synthetic-biology ground-truth circuits (extends build_synthetic_batch1-5).
Programmable logic and light-controlled memory.

Coverage:
  Class I  : recombinase Boolean XOR gate, Cello-style layered NOR cascade
  Class III: optogenetic bistable toggle (light-set/reset memory)

Reuses Batch 1 helpers. Output: glmp-v2/processes/synthetic/<id>.json
"""

import json

from build_synthetic_batch1 import make_process, OUT_DIR

SPECS = [
    {
        "id": "synthetic_xor_gate",
        "name": "Recombinase Boolean XOR Gate",
        "circuitClass": "I",
        "topologyType": "recombinase_combinational_logic",
        "rationale": "Two inputs drive orthogonal recombinases that set the orientation of a DNA register so that output is ON only when exactly one input is present; the device computes the combinational function XOR with no feedback loop. Class I (a logic function, not a memory loop) — Bonnet et al. 2013.",
        "description": "A genetically encoded XOR gate built from site-specific recombinases. Each input triggers a recombinase that flips a segment of DNA; the register ends in an output-ON orientation only when exactly one of the two inputs is active. The circuit computes a Boolean function of its current inputs — a combinational logic element rather than a stateful counter.",
        "scientificAccuracy": "Ground-truth circuit. Recombinase-based amplifying Boolean logic gates, including XOR, were built and characterized by Bonnet et al. (2013).",
        "nodes": [
            ("A", "[Inputs A and B]", "red"),
            ("B", "[Orthogonal recombinases]", "yellow"),
            ("C", "[\\Set DNA register orientation/]", "green"),
            ("D", "{exactly one input ON?}", "blue"),
            ("E", "[Output expressed]", "green"),
            ("F", "(XOR output)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", "Yes"), ("E", "F", ""),
        ],
        "gates": (1, 0, 1),
        "sources": [
            {"title": "Amplifying genetic logic gates", "authors": "Bonnet J, Yin P, Ortiz ME, Subsoontorn P, Endy D", "journal": "Science", "year": 2013, "volume": "340", "pages": "599-603", "pmid": "23539178", "doi": "10.1126/science.1232758"},
        ],
        "keywords": ["XOR", "recombinase", "logic gate", "combinational", "Boolean", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_and_gate", "synthetic_recombinase_counter"],
        "notes": "Ground-truth Class I combinational logic: XOR computed by recombinase register orientation (no feedback).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "invertible output register", "boundFactor": "input-gated recombinases", "operator": "XOR", "effect": "output ON iff one input", "sequenceMotif": "attB/attP flanking output", "note": "combinational, recombinase-implemented"},
            ],
            "derivedLogic": "Output = A XOR B",
            "references": ["Bonnet et al. 2013"],
        },
    },
    {
        "id": "synthetic_layered_nor_cascade",
        "name": "Layered NOR Logic Cascade (Cello)",
        "circuitClass": "I",
        "topologyType": "layered_combinational_NOR_logic",
        "rationale": "Programmable circuits compiled by Cello are layers of NOR/NOT gates wired by orthogonal repressors; any combinational truth table is realized by a feed-forward cascade with no feedback loop. Class I — Nielsen et al. 2016.",
        "description": "The output of a genetic-circuit compiler: an arbitrary combinational function built from a feed-forward cascade of NOR gates, each a repressor-driven promoter. Cello (Nielsen et al. 2016) places and routes these gates from a Verilog specification, demonstrating that layered NOT/NOR logic spans the combinational design space.",
        "scientificAccuracy": "Ground-truth circuit. Genetic-circuit design automation with layered NOR/NOT gates was demonstrated by Nielsen et al. (2016).",
        "nodes": [
            ("A", "[Inputs]", "red"),
            ("B", "[/NOR layer 1/]", "green"),
            ("C", "[/NOR layer 2/]", "green"),
            ("D", "[Programmed combinational output]", "green"),
            ("E", "(Compiled logic function)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", "⊣"), ("C", "D", "⊣"), ("D", "E", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "Genetic circuit design automation", "authors": "Nielsen AAK, Der BS, Shin J, et al.", "journal": "Science", "year": 2016, "volume": "352", "pages": "aac7341", "pmid": "27034378", "doi": "10.1126/science.aac7341"},
        ],
        "keywords": ["NOR", "Cello", "logic cascade", "combinational", "design automation", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_nor_gate", "synthetic_and_gate"],
        "notes": "Ground-truth Class I combinational computation: layered repressor NOR gates, feed-forward (no loop).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "repressor-controlled gate promoters", "boundFactor": "orthogonal TetR-family repressors", "operator": "NOR / NOT (layered)", "effect": "feed-forward combinational logic", "sequenceMotif": "repressor operator array", "note": "any truth table via NOR layers"},
            ],
            "derivedLogic": "Output = f(inputs) via layered NOR (combinational)",
            "references": ["Nielsen et al. 2016"],
        },
    },
    {
        "id": "synthetic_optogenetic_toggle",
        "name": "Optogenetic Bistable Toggle (Light Memory)",
        "circuitClass": "III", "circuitSubclass": "IIIa",
        "topologyType": "mutual_repression_bistable_light_switchable",
        "rationale": "Two repressors mutually repress (a toggle); light inputs set or reset the state by transiently inducing one arm, after which mutual repression holds the state — a persistent, light-switchable bistable memory. Class IIIa (Yazawa-style optogenetic control of a Gardner–Collins-type toggle).",
        "description": "A light-controlled memory cell. A mutual-repression toggle (each repressor blocks the other's promoter) is bistable; brief optogenetic input flips it ON or OFF by transiently relieving or driving one arm, and the state then persists in the dark. It marries the synthetic toggle's bistability with optogenetic set/reset addressing.",
        "scientificAccuracy": "Ground-truth components: the bistable toggle (Gardner, Cantor & Collins 2000) and optogenetic transcriptional control (Yazawa et al. 2009) are each established; the light-switchable toggle composes them.",
        "nodes": [
            ("A", "[Light set/reset input]", "red"),
            ("B", "[Repressor A]", "yellow"),
            ("C", "[Repressor B]", "yellow"),
            ("D", "[/A represses B/]", "green"),
            ("E", "[/B represses A/]", "green"),
            ("F", "(Bistable light-stored memory)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "D", ""), ("D", "C", "⊣"),
            ("C", "E", ""), ("E", "B", "⊣"), ("B", "F", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "Construction of a genetic toggle switch in Escherichia coli", "authors": "Gardner TS, Cantor CR, Collins JJ", "journal": "Nature", "year": 2000, "volume": "403", "pages": "339-342", "pmid": "10659857", "doi": "10.1038/35002131"},
            {"title": "Induction of protein-protein interactions in live cells using light", "authors": "Yazawa M, Sadaghiani AM, Hsueh B, Dolmetsch RE", "journal": "Nature Biotechnology", "year": 2009, "volume": "27", "pages": "941-945", "pmid": "19801976", "doi": "10.1038/nbt.1569"},
        ],
        "keywords": ["optogenetics", "toggle", "bistable", "memory", "mutual repression", "Class IIIa", "ground truth"],
        "relatedProcesses": ["synthetic_toggle_switch", "synthetic_integrase_memory"],
        "notes": "Ground-truth Class IIIa: light-addressable bistable toggle (mutual repression + optogenetic set/reset).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "toggle promoters PA, PB", "boundFactor": "repressor A / repressor B (light-modulated)", "operator": "double NOT / set-reset", "effect": "bistable state held by mutual repression", "sequenceMotif": "operator pair", "note": "light transiently biases one arm to flip state"},
            ],
            "derivedLogic": "A = NOT B ; B = NOT A ; light -> set/reset -> latched state",
            "references": ["Gardner et al. 2000", "Yazawa et al. 2009"],
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
    print(f"Wrote {len(rows)} synthetic Batch-6 process files -> {OUT_DIR}\n")
    print(f"{'id':<40} {'cls':<4} {'sub':<5} {'nodes':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<40} {r[1]:<4} {r[2]:<5} {r[3]:<6} {r[4]:<6} {r[5]}")


if __name__ == "__main__":
    main()
