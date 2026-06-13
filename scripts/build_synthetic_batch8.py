#!/usr/bin/env python3
"""
Batch 8 of synthetic-biology ground-truth circuits (extends build_synthetic_batch1-7).

Coverage:
  Class I  : CRISPR-dCas9 programmable NOR/NOT logic (Gander et al. 2017)
  Class II : capacity/burden feedback controller for stable expression (Ceroni et al. 2018)
  Class V  : CRISPR DNA event recorder (Farzadfard & Lu 2014; Farzadfard et al. 2019)

Reuses Batch 1 helpers. Output: glmp-v2/processes/synthetic/<id>.json
"""

import json

from build_synthetic_batch1 import make_process, OUT_DIR

SPECS = [
    {
        "id": "synthetic_dcas9_logic",
        "name": "CRISPR-dCas9 Programmable Logic",
        "circuitClass": "I",
        "topologyType": "crispr_layered_combinational_logic",
        "rationale": "Inputs drive guide RNAs that target dCas9 to repress output promoters; layering these CRISPR NOR/NOT gates realizes arbitrary combinational logic with a single programmable protein and no feedback loop. Class I (Gander et al. 2017).",
        "description": "Logic built entirely from CRISPR interference. A single catalytically-dead dCas9 paired with input-controlled guide RNAs represses target promoters; because any gRNA can be designed against any promoter, layers of these NOR/NOT gates implement large combinational circuits in one cell. The computation is feed-forward.",
        "scientificAccuracy": "Ground-truth circuit. dCas9-based NOR gates and layered digital logic were built by Gander et al. (2017).",
        "nodes": [
            ("A", "[Inputs drive guide RNAs]", "red"),
            ("B", "[dCas9 + guide RNAs]", "yellow"),
            ("C", "[/gRNA-dCas9 represses promoters/]", "green"),
            ("D", "[Layered NOR/NOT logic]", "green"),
            ("E", "(Programmable CRISPR logic output)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", "⊣"), ("D", "E", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Digital logic circuits in yeast with CRISPR-dCas9 NOR gates", "authors": "Gander MW, Vrana JD, Voje WE, Carothers JM, Klavins E", "journal": "Nature Communications", "year": 2017, "volume": "8", "pages": "15459", "pmid": "28526819", "doi": "10.1038/ncomms15459"},
        ],
        "keywords": ["CRISPR", "dCas9", "NOR", "logic", "combinational", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_layered_nor_cascade", "synthetic_crispri_toggle"],
        "notes": "Ground-truth Class I CRISPR combinational logic (dCas9 NOR layers, feed-forward).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "gRNA-targeted promoters", "boundFactor": "dCas9-gRNA", "operator": "NOR / NOT (programmable)", "effect": "guide-directed repression", "sequenceMotif": "20-nt protospacer + PAM", "note": "any promoter targetable -> scalable logic"},
            ],
            "derivedLogic": "Output = f(inputs) via layered dCas9 NOR (combinational)",
            "references": ["Gander et al. 2017"],
        },
    },
    {
        "id": "synthetic_burden_feedback_controller",
        "name": "Capacity/Burden Feedback Controller",
        "circuitClass": "II",
        "topologyType": "burden_negative_feedback_homeostat",
        "rationale": "A cellular-capacity monitor senses the stress imposed by heterologous expression and throttles the synthetic gene; as burden falls, the throttle relaxes — a negative-feedback homeostat that stabilizes output and protects growth. Class II (Ceroni et al. 2018).",
        "description": "Engineered circuits impose a metabolic burden that destabilizes them. A burden-responsive feedback controller uses a capacity monitor (e.g., a stress-promoter sensor driving a dCas9/sgRNA brake) to detect overload and downregulate the heterologous gene; lower burden then releases the brake, dynamically balancing expression against host health.",
        "scientificAccuracy": "Ground-truth circuit. Burden-driven feedback regulation that stabilizes synthetic expression was built by Ceroni et al. (2018).",
        "nodes": [
            ("A", "[Heterologous expression burden]", "red"),
            ("B", "[Capacity monitor senses stress]", "green"),
            ("C", "[/Feedback throttles synthetic gene/]", "green"),
            ("D", "[Restored growth capacity]", "blue"),
            ("E", "[/Lower burden relaxes throttle/]", "green"),
            ("F", "(Stable expression, healthy growth)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "A", "⊣ feedback"), ("D", "F", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "Burden-driven feedback control of gene expression", "authors": "Ceroni F, Boo A, Furini S, et al.", "journal": "Nature Methods", "year": 2018, "volume": "15", "pages": "387-393", "pmid": "29578536", "doi": "10.1038/nmeth.4635"},
        ],
        "keywords": ["burden", "capacity", "feedback control", "homeostasis", "robustness", "Class II", "ground truth"],
        "relatedProcesses": ["synthetic_antithetic_controller", "synthetic_negative_autoregulation"],
        "notes": "Ground-truth Class II homeostat: burden-sensing negative feedback stabilizes heterologous expression.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "capacity-monitor stress promoter", "boundFactor": "stress regulator -> dCas9 brake", "operator": "NOT (burden-gated)", "effect": "throttles synthetic gene under load", "sequenceMotif": "htrA/groSL-type stress promoter", "note": "closes a burden negative-feedback loop"},
            ],
            "derivedLogic": "synthetic-gene = NOT burden ; burden -| output (negative feedback)",
            "references": ["Ceroni et al. 2018"],
        },
    },
    {
        "id": "synthetic_crispr_recorder",
        "name": "CRISPR DNA Event Recorder",
        "circuitClass": "V",
        "topologyType": "self_modifying_dna_recorder",
        "rationale": "A stimulus drives a writer (recombinase/retron-SCRIBE or base/prime editor) that introduces stimulus- and time-dependent mutations into genomic DNA, so the genome accumulates an analog record of past events read out by sequencing — a self-modifying-DNA memory. Class V (Farzadfard & Lu 2014; Farzadfard et al. 2019).",
        "description": "A genomic ticker-tape. A signal-controlled DNA writer continuously edits a defined genomic locus, accumulating mutations in proportion to signal strength and duration; sequencing later reconstructs the history of stimuli a cell population experienced. Because the device records by rewriting its own DNA, it is a self-modifying memory.",
        "scientificAccuracy": "Ground-truth circuit. In-vivo DNA recorders (SCRIBE, DOMINO/CAMERA) were built and characterized (Farzadfard & Lu 2014; Farzadfard et al. 2019).",
        "nodes": [
            ("A", "[Signal over time]", "red"),
            ("B", "[Writer: editor/recombinase]", "yellow"),
            ("C", "[\\Writes edits into genomic DNA/]", "green"),
            ("D", "[DNA accumulates an event record]", "blue"),
            ("E", "[Sequencing reads out history]", "green"),
            ("F", "(Heritable molecular ticker-tape)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "Genomically encoded analog memory with precise in vivo DNA writing in living cell populations", "authors": "Farzadfard F, Lu TK", "journal": "Science", "year": 2014, "volume": "346", "pages": "1256272", "pmid": "25395541", "doi": "10.1126/science.1256272"},
            {"title": "Single-nucleotide-resolution computing and memory in living cells (DOMINO)", "authors": "Farzadfard F, Gharaei N, Higashikuni Y, et al.", "journal": "Molecular Cell", "year": 2019, "volume": "75", "pages": "769-780", "pmid": "31302002", "doi": "10.1016/j.molcel.2019.07.011"},
        ],
        "keywords": ["recorder", "SCRIBE", "DOMINO", "base editing", "self-modifying DNA", "memory", "Class V", "ground truth"],
        "relatedProcesses": ["synthetic_recombinase_counter", "synthetic_integrase_memory"],
        "notes": "Ground-truth Class V: signal-driven DNA writing records history into the genome (self-modifying).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "recorder locus", "boundFactor": "signal-gated DNA writer", "operator": "SELF-MODIFY (analog)", "effect": "accumulates mutations encoding signal history", "sequenceMotif": "target locus + ssDNA donor / editing window", "note": "heritable, read by sequencing"},
            ],
            "derivedLogic": "DNA_state := write(signal, time) -> analog genomic record",
            "references": ["Farzadfard & Lu 2014", "Farzadfard et al. 2019"],
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
    print(f"Wrote {len(rows)} synthetic Batch-8 process files -> {OUT_DIR}\n")
    print(f"{'id':<42} {'cls':<4} {'nodes':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<42} {r[1]:<4} {r[2]:<6} {r[3]:<6} {r[4]}")


if __name__ == "__main__":
    main()
