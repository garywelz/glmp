#!/usr/bin/env python3
"""
Batch 3 of synthetic-biology ground-truth circuits (extends build_synthetic_batch1/2).
Adds the remaining canonical motifs, including a Class V self-modifying recombinase
memory device — a clean synthetic anchor for the otherwise rare top rung of the ladder.

Coverage:
  Class I  : sender/receiver quorum-sensing relay, theophylline riboswitch, NOR gate
  Class II : antithetic integral-feedback controller (robust perfect adaptation)
  Class IV : five-repressor ring oscillator
  Class V  : integrase/recombinase permanent memory (self-modifying DNA)

Reuses Batch 1 helpers so schema/stats stay identical.
Output: glmp-v2/processes/synthetic/<id>.json
"""

import json

from build_synthetic_batch1 import make_process, OUT_DIR

SPECS = [
    # ----------------------------------------------------------------- Class I
    {
        "id": "synthetic_sender_receiver_qs",
        "name": "Sender–Receiver Quorum-Sensing Relay",
        "circuitClass": "I",
        "topologyType": "intercellular_feed_forward_relay",
        "rationale": "A sender cell synthesizes a diffusible AHL signal via LuxI; a receiver cell detects it through LuxR and fires an output promoter. No feedback edge — a pure intercellular feed-forward relay. Class I.",
        "description": "The minimal cell-cell communication module. Sender cells express LuxI to make the diffusible autoinducer AHL; receiver cells express LuxR, which binds AHL and activates an output promoter. With no feedback it is a feed-forward relay, the building block of synthetic multicellular pattern-formation systems.",
        "scientificAccuracy": "Ground-truth circuit. Engineered sender/receiver AHL communication is established (Weiss & Knight 2000; Basu et al. 2005).",
        "nodes": [
            ("A", "[Sender cell]", "red"),
            ("B", "[LuxI synthesizes AHL]", "green"),
            ("C", "[AHL diffuses]", "blue"),
            ("D", "[Receiver: LuxR-AHL]", "yellow"),
            ("E", "[Receiver output promoter active]", "green"),
            ("F", "(Coordinated GFP output)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "A synthetic multicellular system for programmed pattern formation", "authors": "Basu S, Gerchman Y, Collins CH, Arnold FH, Weiss R", "journal": "Nature", "year": 2005, "volume": "434", "pages": "1130-1134", "pmid": "15858574", "doi": "10.1038/nature03461"},
        ],
        "keywords": ["quorum sensing", "sender receiver", "LuxI", "LuxR", "feed-forward", "cell communication", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_population_control", "synthetic_band_detector"],
        "notes": "Ground-truth Class I intercellular relay (feed-forward, no feedback).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Plux (receiver)", "boundFactor": "LuxR-AHL", "operator": "IF", "effect": "activation on signal receipt", "sequenceMotif": "ACCTGTAGGATCGTACAGGT (lux box)", "note": "AHL produced by sender's LuxI"},
            ],
            "derivedLogic": "Output_receiver = AHL_sender (feed-forward relay)",
            "references": ["Basu et al. 2005"],
        },
    },
    {
        "id": "synthetic_theophylline_riboswitch",
        "name": "Theophylline Riboswitch (ligand-gated translation)",
        "circuitClass": "I",
        "topologyType": "rna_ligand_gated_translation",
        "rationale": "A synthetic aptamer in the 5' UTR binds theophylline and rearranges to expose the ribosome-binding site, switching translation ON. A pure input-to-output sensor with no feedback. Class I.",
        "description": "An RNA-based input device: a theophylline aptamer fused to a ribosome-binding site. Without ligand the RBS is sequestered; theophylline binding restructures the RNA to expose the RBS and switch on translation of the downstream gene. A feed-forward molecular sensor with no regulatory loop.",
        "scientificAccuracy": "Ground-truth circuit. Synthetic theophylline riboswitches controlling translation were engineered and characterized (Desai & Gallivan 2004; Topp & Gallivan 2007).",
        "nodes": [
            ("A", "[Theophylline ligand]", "red"),
            ("B", "[Aptamer binds ligand]", "yellow"),
            ("C", "[\\RNA refolds, exposes RBS/]", "green"),
            ("D", "[Ribosome-binding site available]", "blue"),
            ("E", "[Translation ON]", "green"),
            ("F", "(Output protein)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "Genetic screens and selections for small molecules based on a synthetic riboswitch that activates protein translation", "authors": "Desai SK, Gallivan JP", "journal": "Journal of the American Chemical Society", "year": 2004, "volume": "126", "pages": "13247-13254", "pmid": "15479073", "doi": "10.1021/ja048634j"},
        ],
        "keywords": ["riboswitch", "aptamer", "theophylline", "translation control", "RNA", "feed-forward", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_and_gate"],
        "notes": "Ground-truth Class I RNA sensor (feed-forward, no feedback).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "5' UTR aptamer + RBS", "boundFactor": "theophylline (small molecule)", "operator": "IF", "effect": "ligand-gated translation initiation", "sequenceMotif": "theophylline aptamer + downstream RBS", "note": "ligand binding exposes the Shine-Dalgarno sequence"},
            ],
            "derivedLogic": "Output = IF theophylline THEN translate (ligand-gated)",
            "references": ["Desai & Gallivan 2004"],
        },
    },
    {
        "id": "synthetic_nor_gate",
        "name": "Transcriptional NOR Gate",
        "circuitClass": "I",
        "topologyType": "transcriptional_NOR_gate",
        "rationale": "Either input expresses a repressor that silences the output; the output is ON only when neither input is present: out = NOT (A OR B). Feed-forward, no cycle — Class I — and the universal gate from which Tamsir et al. built cellular logic.",
        "description": "A two-input NOR gate: either input drives a repressor of the shared output promoter, so the output is ON only when both inputs are absent. NOR is functionally complete, and distributing NOR gates across communicating colonies is how Tamsir, Tabor & Voigt built multicellular Boolean logic.",
        "scientificAccuracy": "Ground-truth circuit. NOR-gate cells and chemical-wire logic were built and characterized by Tamsir, Tabor & Voigt (2011).",
        "nodes": [
            ("A", "[Input 1]", "red"),
            ("B", "[Input 2]", "red"),
            ("C", "{Input 1 OR Input 2?}", "blue"),
            ("D", "[/Repressor silences output/]", "green"),
            ("E", "[Output promoter active]", "green"),
            ("F", "(Output GFP: NOR)", "violet"),
        ],
        "edges": [
            ("A", "C", ""), ("B", "C", ""),
            ("C", "D", "Yes"), ("D", "E", "⊣"), ("E", "F", ""),
        ],
        "gates": (1, 0, 1),
        "sources": [
            {"title": "Robust multicellular computing using genetically encoded NOR gates and chemical 'wires'", "authors": "Tamsir A, Tabor JJ, Voigt CA", "journal": "Nature", "year": 2011, "volume": "469", "pages": "212-215", "pmid": "21150903", "doi": "10.1038/nature09565"},
        ],
        "keywords": ["NOR gate", "logic gate", "functionally complete", "feed-forward", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_and_gate", "synthetic_or_gate"],
        "notes": "Ground-truth Class I universal logic element: one OR + one NOT, no feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "output promoter (operator-controlled)", "boundFactor": "input-driven repressor", "operator": "NOR", "effect": "repression if either input present", "sequenceMotif": "(repressor operator)", "note": "ON only when both inputs absent"},
            ],
            "derivedLogic": "Output = NOT (Input1 OR Input2)",
            "references": ["Tamsir et al. 2011"],
        },
    },
    # ----------------------------------------------------------------- Class II
    {
        "id": "synthetic_antithetic_integral_feedback",
        "name": "Antithetic Integral-Feedback Controller",
        "circuitClass": "II",
        "topologyType": "antithetic_integral_feedback",
        "rationale": "Two controller species are produced in proportion to reference and output and annihilate each other; the sequestration implements integral feedback, giving robust perfect adaptation of the output to disturbances (Briat, Gupta & Khammash 2016). A designed negative-feedback homeostat — Class II.",
        "description": "A synthetic controller that achieves robust perfect adaptation. Controller species Z1 is made at a reference rate and activates the output; the output drives production of Z2, and Z1 and Z2 annihilate each other. This molecular sequestration integrates the error over time (integral feedback), so the steady-state output is invariant to disturbances and parameter changes.",
        "scientificAccuracy": "Ground-truth circuit. The antithetic integral-feedback motif and its perfect-adaptation property were derived and demonstrated (Briat, Gupta & Khammash 2016; Aoki et al. 2019).",
        "nodes": [
            ("A", "[Reference input]", "red"),
            ("B", "[Controller Z1 produced]", "yellow"),
            ("C", "[Z1 activates output X]", "green"),
            ("D", "[Output species X]", "yellow"),
            ("E", "[X produces Z2]", "green"),
            ("F", "[/Z1 + Z2 annihilate/]", "green"),
            ("G", "(Robust perfect adaptation of X)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "F", ""), ("F", "B", "⊣ sequester"),
            ("D", "G", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Antithetic integral feedback ensures robust perfect adaptation in noisy biomolecular networks", "authors": "Briat C, Gupta A, Khammash M", "journal": "Cell Systems", "year": 2016, "volume": "2", "pages": "15-26", "pmid": "27136686", "doi": "10.1016/j.cels.2016.01.004"},
            {"title": "A universal biomolecular integral feedback controller for robust perfect adaptation", "authors": "Aoki SK, Lillacci G, Gupta A, Baumschlager A, Schweingruber D, Khammash M", "journal": "Nature", "year": 2019, "volume": "570", "pages": "533-537", "pmid": "31217585", "doi": "10.1038/s41586-019-1321-1"},
        ],
        "keywords": ["antithetic", "integral feedback", "perfect adaptation", "control theory", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["synthetic_negative_autoregulation"],
        "notes": "Ground-truth Class II designed homeostat: integral (negative) feedback via molecular sequestration.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Z1 / Z2 production + sequestration", "boundFactor": "sigma factor / anti-sigma (one realization)", "operator": "integral NOT", "effect": "error-integrating negative feedback", "sequenceMotif": "(reference promoter for Z1; output promoter for Z2)", "note": "Z1+Z2 annihilation integrates error"},
            ],
            "derivedLogic": "X_steady-state = reference (integral feedback -> perfect adaptation)",
            "references": ["Briat et al. 2016"],
        },
    },
    # ----------------------------------------------------------------- Class IV
    {
        "id": "synthetic_5node_repressilator",
        "name": "Five-Repressor Ring Oscillator",
        "circuitClass": "IV",
        "topologyType": "odd_ring_oscillator_delayed_neg_feedback",
        "rationale": "Five repressors in a cyclic chain, each repressing the next. The odd number of inversions around the loop gives delayed negative feedback and sustained oscillation, generalizing the three-node repressilator (Elowitz & Leibler 2000) to a longer, slower ring. Class IV.",
        "description": "A longer ring oscillator: five repressors arranged so each represses the next and the last closes the loop on the first. An odd number of repressions makes the loop a delayed negative-feedback circuit that oscillates, with a longer period and more phase steps than the canonical three-node repressilator.",
        "scientificAccuracy": "Ground-truth design. Odd-length repressor rings oscillate by the same delayed-negative-feedback principle established for the three-node repressilator (Elowitz & Leibler 2000); robust long-period rings characterized by Potvin-Trottier et al. 2016.",
        "nodes": [
            ("A", "[Repressor R1]", "yellow"),
            ("B", "[Repressor R2]", "yellow"),
            ("C", "[Repressor R3]", "yellow"),
            ("D", "[Repressor R4]", "yellow"),
            ("E", "[Repressor R5]", "yellow"),
            ("F", "(Oscillating reporter, long period)", "violet"),
        ],
        "edges": [
            ("A", "B", "⊣"), ("B", "C", "⊣"), ("C", "D", "⊣"),
            ("D", "E", "⊣"), ("E", "A", "⊣"), ("A", "F", ""),
        ],
        "gates": (0, 0, 5),
        "sources": [
            {"title": "A synthetic oscillatory network of transcriptional regulators", "authors": "Elowitz MB, Leibler S", "journal": "Nature", "year": 2000, "volume": "403", "pages": "335-338", "pmid": "10659856", "doi": "10.1038/35002125"},
            {"title": "Synchronous long-term oscillations in a synthetic gene circuit", "authors": "Potvin-Trottier L, Lord ND, Vinnicombe G, Paulsson J", "journal": "Nature", "year": 2016, "volume": "538", "pages": "514-517", "pmid": "27732583", "doi": "10.1038/nature19841"},
        ],
        "keywords": ["repressilator", "ring oscillator", "five-node", "delayed negative feedback", "Class IV", "ground truth"],
        "relatedProcesses": ["synthetic_repressilator", "synthetic_metabolator"],
        "notes": "Ground-truth Class IV oscillator: five repressions (odd ring) -> one delayed-feedback loop.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "five operator-controlled promoters in a ring", "boundFactor": "R1..R5 repressors", "operator": "NOT (x5)", "effect": "cyclic repression", "sequenceMotif": "(distinct operator per repressor)", "note": "odd number of inversions -> oscillation"},
            ],
            "derivedLogic": "Ri = NOT R(i-1) around a 5-ring -> sustained oscillation",
            "references": ["Elowitz & Leibler 2000"],
        },
    },
    # ----------------------------------------------------------------- Class V
    {
        "id": "synthetic_integrase_memory",
        "name": "Integrase Recombinase Permanent Memory",
        "circuitClass": "V",
        "topologyType": "self_modifying_dna_recombinase_memory",
        "rationale": "An input pulse expresses a site-specific integrase that inverts (or excises) a DNA segment between recombination sites, permanently rewriting the cell's own genetic state. The circuit modifies its own DNA template and the new state is heritable without further input — the synthetic analogue of the self-modifying (Class V) rung (Bonnet et al. 2012; Siuti et al. 2013).",
        "description": "A permanent genetic memory device. A transient input drives a site-specific serine integrase that flips a DNA segment between attB/attP sites, switching a reporter ON and changing the orientation of its own DNA. Because the edit is to the DNA sequence itself, the state is digital, heritable, and persists indefinitely without the input — a circuit that rewrites its own genome rather than only its expression state.",
        "scientificAccuracy": "Ground-truth circuit. Recombinase-based rewritable memory and integrase state machines were built and characterized (Bonnet, Subsoontorn & Endy 2012; Siuti, Yazbek & Lu 2013).",
        "nodes": [
            ("A", "[Input signal pulse]", "red"),
            ("B", "[Integrase expressed]", "yellow"),
            ("C", "[\\Inverts DNA between att sites/]", "green"),
            ("D", "[Rewritten DNA state, heritable]", "blue"),
            ("E", "[Reporter ON]", "green"),
            ("F", "(Permanent genetic memory)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "Rewritable digital data storage in live cells via engineered control of recombination directionality", "authors": "Bonnet J, Subsoontorn P, Endy D", "journal": "PNAS", "year": 2012, "volume": "109", "pages": "8884-8889", "pmid": "22615351", "doi": "10.1073/pnas.1202344109"},
            {"title": "Synthetic circuits integrating logic and memory in living cells", "authors": "Siuti P, Yazbek J, Lu TK", "journal": "Nature Biotechnology", "year": 2013, "volume": "31", "pages": "448-452", "pmid": "23396014", "doi": "10.1038/nbt.2510"},
        ],
        "keywords": ["integrase", "recombinase", "memory", "self-modifying DNA", "DNA inversion", "Class V", "ground truth"],
        "relatedProcesses": ["synthetic_toggle_switch", "synthetic_crispri_toggle"],
        "notes": "Ground-truth Class V anchor: the circuit edits its own DNA (self-modifying genetic state), giving heritable memory without standing feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "attB / attP recombination sites", "boundFactor": "serine integrase", "operator": "SELF-MODIFY", "effect": "irreversible DNA inversion/excision", "sequenceMotif": "attB x attP -> attL / attR", "note": "directionality set by integrase +/- RDF; rewrites the DNA template itself"},
            ],
            "derivedLogic": "DNA_state := flip(DNA_state) on input pulse -> heritable memory (self-modifying)",
            "references": ["Bonnet et al. 2012", "Siuti et al. 2013"],
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
    print(f"Wrote {len(rows)} synthetic Batch-3 process files -> {OUT_DIR}\n")
    print(f"{'id':<42} {'cls':<4} {'nodes':<6} {'edges':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<42} {r[1]:<4} {r[2]:<6} {r[3]:<6} {r[4]:<6} {r[5]}")


if __name__ == "__main__":
    main()
