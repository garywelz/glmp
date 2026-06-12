#!/usr/bin/env python3
"""
Batch 4 of synthetic-biology ground-truth circuits (extends build_synthetic_batch1-3).
Adds canonical oscillators, a fold-change detector, multi-input logic, and an RNA
post-transcriptional regulator.

Coverage:
  Class I  : 3-input AND gate, toggle-RNA riboregulator (translational activation)
  Class II : incoherent-FFL fold-change detector (FCD)
  Class IV : Atkinson relaxation oscillator, Stricker fast dual-feedback oscillator

Reuses Batch 1 helpers so schema/stats stay identical.
Output: glmp-v2/processes/synthetic/<id>.json
"""

import json

from build_synthetic_batch1 import make_process, OUT_DIR

SPECS = [
    # ----------------------------------------------------------------- Class I
    {
        "id": "synthetic_three_input_and",
        "name": "Three-Input Transcriptional AND Gate",
        "circuitClass": "I",
        "topologyType": "layered_transcriptional_AND",
        "rationale": "Three inputs are combined through layered split-activator / integrase logic so the output fires only when all three are present: out = A AND B AND C. Feed-forward, no cycle — Class I — extending two-input logic to deeper combinatorial control (Moon et al. 2012).",
        "description": "A three-input AND gate assembled by layering two-input AND modules (e.g. hrpRS plus a third inducible input). The output promoter fires only when all three inputs are present, demonstrating scalable combinatorial transcriptional logic with no feedback.",
        "scientificAccuracy": "Ground-truth circuit. A genetic 3-input AND gate built from layered modules was demonstrated by Moon et al. (2012).",
        "nodes": [
            ("A", "[Input 1]", "red"),
            ("B", "[Input 2]", "red"),
            ("C", "[Input 3]", "red"),
            ("D", "{Input 1 AND Input 2?}", "blue"),
            ("E", "[Intermediate activator]", "yellow"),
            ("F", "{intermediate AND Input 3?}", "blue"),
            ("G", "[Output promoter active]", "green"),
            ("H", "(Output GFP: all three required)", "violet"),
        ],
        "edges": [
            ("A", "D", ""), ("B", "D", ""), ("D", "E", "Yes"),
            ("E", "F", ""), ("C", "F", ""), ("F", "G", "Yes"), ("G", "H", ""),
        ],
        "gates": (0, 2, 0),
        "sources": [
            {"title": "Genetic programs constructed from layered logic gates in single cells", "authors": "Moon TS, Lou C, Tamsir A, Stanton BC, Voigt CA", "journal": "Nature", "year": 2012, "volume": "491", "pages": "249-253", "pmid": "23041931", "doi": "10.1038/nature11516"},
        ],
        "keywords": ["AND gate", "three-input", "layered logic", "feed-forward", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_and_gate"],
        "notes": "Ground-truth Class I deep logic: two layered AND gates, no feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "layered AND promoters", "boundFactor": "split activators / integrases", "operator": "AND (x2)", "effect": "activation only if all inputs present", "sequenceMotif": "(module-specific)", "note": "two AND layers compose a 3-input AND"},
            ],
            "derivedLogic": "Output = Input1 AND Input2 AND Input3",
            "references": ["Moon et al. 2012"],
        },
    },
    {
        "id": "synthetic_toehold_riboregulator",
        "name": "Toehold Switch Riboregulator",
        "circuitClass": "I",
        "topologyType": "rna_trans_translational_activation",
        "rationale": "A trans-acting trigger RNA opens a cis-repressed hairpin to expose the ribosome-binding site, switching translation ON. A programmable RNA input device with no feedback. Class I.",
        "description": "A toehold switch: the output mRNA carries a hairpin that sequesters its own ribosome-binding site. A separate trigger RNA binds the single-stranded toehold and unfolds the hairpin, exposing the RBS and turning on translation. Sequence-programmable and orthogonal, with no regulatory loop.",
        "scientificAccuracy": "Ground-truth circuit. Toehold-switch riboregulators with high dynamic range and orthogonality were engineered by Green et al. (2014).",
        "nodes": [
            ("A", "[Trigger RNA input]", "red"),
            ("B", "[Binds toehold of hairpin mRNA]", "yellow"),
            ("C", "[\\Hairpin unfolds, exposes RBS/]", "green"),
            ("D", "[Ribosome-binding site free]", "blue"),
            ("E", "[Translation ON]", "green"),
            ("F", "(Output protein)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "Toehold switches: de-novo-designed regulators of gene expression", "authors": "Green AA, Silver PA, Collins JJ, Yin P", "journal": "Cell", "year": 2014, "volume": "159", "pages": "925-939", "pmid": "25417166", "doi": "10.1016/j.cell.2014.10.002"},
        ],
        "keywords": ["toehold switch", "riboregulator", "trigger RNA", "translation", "feed-forward", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_theophylline_riboswitch"],
        "notes": "Ground-truth Class I RNA input device (trans-activating, feed-forward).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "toehold + hairpin with sequestered RBS", "boundFactor": "trigger RNA", "operator": "IF", "effect": "RNA-gated translation activation", "sequenceMotif": "programmable toehold (linear-linear hybridization)", "note": "trigger binding exposes Shine-Dalgarno + start codon"},
            ],
            "derivedLogic": "Output = IF trigger-RNA THEN translate",
            "references": ["Green et al. 2014"],
        },
    },
    # ----------------------------------------------------------------- Class II
    {
        "id": "synthetic_fold_change_detector",
        "name": "Incoherent-FFL Fold-Change Detector",
        "circuitClass": "II",
        "topologyType": "incoherent_ffl_fold_change_detection",
        "rationale": "An incoherent feed-forward loop with the right (e.g. division-like) interaction responds to the fold-change of the input rather than its absolute level — a form of exact adaptation. The internal repression branch acts as a negative regulator of the output, so it is grouped with the adaptive/homeostatic Class II circuits (Goentoro et al. 2009).",
        "description": "A fold-change detector built on an incoherent feed-forward loop: the input activates the output and, through an intermediate, also represses it in proportion to input level. The output then depends only on the relative (fold) change of the input, not its absolute value — the synthetic realization of fold-change detection / exact adaptation.",
        "scientificAccuracy": "Ground-truth design. The IFFL fold-change-detection property was derived and demonstrated (Goentoro, Shoval, Kirschner & Alon 2009).",
        "nodes": [
            ("A", "[Input signal X]", "red"),
            ("B", "[Activates output Z]", "green"),
            ("C", "[Intermediate Y tracks X]", "yellow"),
            ("D", "[/Y represses Z in proportion to X/]", "green"),
            ("E", "{Z = X / Y?}", "blue"),
            ("F", "(Output Z: responds to fold-change)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("A", "C", ""), ("C", "D", ""),
            ("B", "E", ""), ("D", "E", "⊣"), ("E", "F", "Yes"),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "The incoherent feedforward loop can provide fold-change detection in gene regulation", "authors": "Goentoro L, Shoval O, Kirschner MW, Alon U", "journal": "Molecular Cell", "year": 2009, "volume": "36", "pages": "894-899", "pmid": "20005851", "doi": "10.1016/j.molcel.2009.11.018"},
        ],
        "keywords": ["fold-change detection", "incoherent feed-forward", "exact adaptation", "scale invariance", "Class II", "ground truth"],
        "relatedProcesses": ["synthetic_incoherent_ffl"],
        "notes": "Ground-truth circuit grouped in Class II (adaptive negative regulation); functionally a fold-change detector.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "output promoter (activator + proportional repressor)", "boundFactor": "X (activator) + Y (X-driven repressor)", "operator": "X AND NOT Y", "effect": "output ~ X/Y", "sequenceMotif": "(activator + operator)", "note": "repressor scales with input -> fold-change readout"},
            ],
            "derivedLogic": "Z ~ X / Y where Y ~ X -> Z responds to fold-change of X",
            "references": ["Goentoro et al. 2009"],
        },
    },
    # ----------------------------------------------------------------- Class IV
    {
        "id": "synthetic_atkinson_oscillator",
        "name": "Atkinson Relaxation Oscillator",
        "circuitClass": "IV",
        "topologyType": "coupled_pos_neg_feedback_oscillator",
        "rationale": "Couples a positive-feedback activator module to a negative-feedback repressor module; the delayed negative arm against the fast positive arm produces relaxation oscillations in E. coli (Atkinson, Savageau, Myers & Ninfa 2003). Class IV.",
        "description": "One of the first engineered gene oscillators: an NRI activator that activates its own promoter (positive feedback) is coupled to a LacI repressor module it drives, which in turn represses the activator (delayed negative feedback). The interplay of the fast positive and slow negative loops gives relaxation-type oscillations.",
        "scientificAccuracy": "Ground-truth circuit. Built and shown to oscillate (damped) in E. coli by Atkinson et al. (2003).",
        "nodes": [
            ("A", "[Activator NRI]", "yellow"),
            ("B", "[\\NRI activates own promoter/]", "green"),
            ("C", "[Represser LacI expressed]", "yellow"),
            ("D", "[/LacI represses NRI promoter/]", "green"),
            ("E", "(Relaxation oscillation)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "A", "+"),
            ("A", "C", ""), ("C", "D", ""), ("D", "A", "⊣ delayed"),
            ("A", "E", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Development of genetic circuitry exhibiting toggle switch or oscillatory behavior in Escherichia coli", "authors": "Atkinson MR, Savageau MA, Myers JT, Ninfa AJ", "journal": "Cell", "year": 2003, "volume": "113", "pages": "597-607", "pmid": "12787501", "doi": "10.1016/S0092-8674(03)00346-5"},
        ],
        "keywords": ["oscillator", "relaxation oscillator", "positive feedback", "negative feedback", "Atkinson", "Class IV", "ground truth"],
        "relatedProcesses": ["synthetic_repressilator", "synthetic_stricker_oscillator"],
        "notes": "Ground-truth Class IV oscillator: coupled positive + delayed negative feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "glnAp2 (NRI-activated)", "boundFactor": "NRI~P (activator)", "operator": "IF / positive feedback", "effect": "activation of activator + repressor modules", "sequenceMotif": "NRI enhancer", "note": "positive arm"},
                {"name": "lac operator", "boundFactor": "LacI", "operator": "NOT", "effect": "delayed repression of activator", "sequenceMotif": "AATTGTGAGCGGATAACAATT", "note": "negative arm"},
            ],
            "derivedLogic": "NRI = +NRI AND NOT LacI(t-τ) -> relaxation oscillation",
            "references": ["Atkinson et al. 2003"],
        },
    },
    {
        "id": "synthetic_stricker_oscillator",
        "name": "Stricker Fast Dual-Feedback Oscillator",
        "circuitClass": "IV",
        "topologyType": "dual_feedback_oscillator",
        "rationale": "A hybrid promoter is activated by AraC (positive feedback) and repressed by LacI (negative feedback), both driven from the same promoter; the interlinked fast positive and negative loops give robust, tunable, fast oscillations (Stricker et al. 2008). Class IV.",
        "description": "A robust, fast synthetic oscillator. A single hybrid promoter drives both AraC (an activator of that promoter, positive feedback) and LacI (a repressor of it, negative feedback). The interlinked positive and negative loops, with matched protein degradation, produce tunable oscillations far more regular than the original repressilator.",
        "scientificAccuracy": "Ground-truth circuit. Built and characterized with single-cell microfluidics by Stricker et al. (2008).",
        "nodes": [
            ("A", "[Inducers: arabinose + IPTG]", "red"),
            ("B", "[Hybrid promoter Plac/ara]", "blue"),
            ("C", "[AraC activator]", "yellow"),
            ("D", "[\\AraC activates promoter/]", "green"),
            ("E", "[LacI repressor]", "yellow"),
            ("F", "[/LacI represses promoter/]", "green"),
            ("G", "(Fast tunable oscillation)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "B", "+"),
            ("B", "E", ""), ("E", "F", ""), ("F", "B", "⊣"),
            ("B", "G", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "A fast, robust and tunable synthetic gene oscillator", "authors": "Stricker J, Cookson S, Bennett MR, Mather WH, Tsimring LS, Hasty J", "journal": "Nature", "year": 2008, "volume": "456", "pages": "516-519", "pmid": "18971928", "doi": "10.1038/nature07389"},
        ],
        "keywords": ["oscillator", "dual feedback", "AraC", "LacI", "Stricker", "Class IV", "ground truth"],
        "relatedProcesses": ["synthetic_atkinson_oscillator", "synthetic_repressilator"],
        "notes": "Ground-truth Class IV oscillator: interlinked positive + negative feedback on one hybrid promoter.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Plac/ara-1 hybrid promoter", "boundFactor": "AraC (activator) + LacI (repressor)", "operator": "positive AND NOT", "effect": "interlinked activation + repression", "sequenceMotif": "araI + lacO within one promoter", "note": "both regulators expressed from this promoter"},
            ],
            "derivedLogic": "P = +AraC AND NOT LacI -> fast oscillation",
            "references": ["Stricker et al. 2008"],
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
    print(f"Wrote {len(rows)} synthetic Batch-4 process files -> {OUT_DIR}\n")
    print(f"{'id':<42} {'cls':<4} {'nodes':<6} {'edges':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<42} {r[1]:<4} {r[2]:<6} {r[3]:<6} {r[4]:<6} {r[5]}")


if __name__ == "__main__":
    main()
