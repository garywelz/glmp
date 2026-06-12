#!/usr/bin/env python3
"""
Batch 2 of synthetic-biology ground-truth circuits (extends build_synthetic_batch1.py).
More canonical engineered circuits whose topology AND behaviour are known by
construction, each with a sequenceAnnotation block.

Coverage:
  Class I  : transcriptional AND gate, OR gate, band-pass / edge detector
  Class II : quorum-sensing population control (You et al. 2004)
  Class III: CRISPRi mutual-repression toggle
  Class IV : metabolator metabolic oscillator (Fung et al. 2005)

Reuses Batch 1 helpers so schema/stats stay identical.
Output: glmp-v2/processes/synthetic/<id>.json
"""

import json

from build_synthetic_batch1 import make_process, OUT_DIR

SPECS = [
    # ----------------------------------------------------------------- Class I
    {
        "id": "synthetic_and_gate",
        "name": "Transcriptional AND Gate (hrpR/hrpS)",
        "circuitClass": "I",
        "topologyType": "transcriptional_AND_gate",
        "rationale": "Two inputs each drive one subunit of a hetero-activator; only when both subunits are present (AND) is the output promoter activated. Pure feed-forward, no cycle — Class I — implementing Boolean AND (Wang, Kitney, Joly & Buck 2011).",
        "description": "A two-input transcriptional AND gate built from the hrpR/hrpS sigma-54 activator pair. Input 1 drives HrpR, input 2 drives HrpS; both proteins must be present to form the active hetero-hexamer that fires the pHrpL output promoter. With no feedback edge it is a feed-forward logic element.",
        "scientificAccuracy": "Ground-truth circuit. The hrpRS AND gate was built and characterized in E. coli (Wang et al. 2011).",
        "nodes": [
            ("A", "[Input 1: inducer A]", "red"),
            ("B", "[Input 2: inducer B]", "red"),
            ("C", "[HrpR expressed]", "yellow"),
            ("D", "[HrpS expressed]", "yellow"),
            ("E", "{HrpR AND HrpS?}", "blue"),
            ("F", "[pHrpL output promoter active]", "green"),
            ("G", "(Output GFP: only if both inputs)", "violet"),
        ],
        "edges": [
            ("A", "C", ""), ("B", "D", ""),
            ("C", "E", ""), ("D", "E", ""),
            ("E", "F", "Yes"), ("F", "G", ""),
        ],
        "gates": (0, 1, 0),
        "sources": [
            {"title": "Engineering modular and orthogonal genetic logic gates for robust digital-like synthetic biology", "authors": "Wang B, Kitney RI, Joly N, Buck M", "journal": "Nature Communications", "year": 2011, "volume": "2", "pages": "508", "pmid": "22009040", "doi": "10.1038/ncomms1516"},
        ],
        "keywords": ["AND gate", "logic gate", "hrpR", "hrpS", "feed-forward", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_or_gate", "synthetic_coherent_ffl"],
        "notes": "Ground-truth Class I logic element: one AND gate, no feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "pHrpL (sigma-54 promoter)", "boundFactor": "HrpR-HrpS hetero-hexamer", "operator": "AND", "effect": "activation", "sequenceMotif": "TGGCAC-N5-TTGCA (sigma-54 -24/-12)", "note": "requires both bEBP subunits to fire"},
            ],
            "derivedLogic": "Output = HrpR AND HrpS = Input1 AND Input2",
            "references": ["Wang et al. 2011"],
        },
    },
    {
        "id": "synthetic_or_gate",
        "name": "Transcriptional OR Gate (tandem promoters)",
        "circuitClass": "I",
        "topologyType": "transcriptional_OR_gate",
        "rationale": "Either of two inducible promoters in tandem drives the same output; the output is ON if either input is present (OR). Feed-forward, no cycle — Class I — implementing Boolean OR.",
        "description": "A two-input OR gate built from two inducible promoters arranged in tandem upstream of one reporter. Either aTc (via PLtetO-1) or AHL (via Plux) is sufficient to transcribe the output. No feedback edge, so it is a feed-forward Boolean logic element.",
        "scientificAccuracy": "Ground-truth circuit. Tandem-promoter OR gates are a standard, well-characterized synthetic logic primitive (Tamsir, Tabor & Voigt 2011).",
        "nodes": [
            ("A", "[Input 1: aTc]", "red"),
            ("B", "[Input 2: AHL]", "red"),
            ("C", "{Input 1 OR Input 2?}", "blue"),
            ("D", "[Tandem output promoter active]", "green"),
            ("E", "(Output GFP: if either input)", "violet"),
        ],
        "edges": [
            ("A", "C", ""), ("B", "C", ""),
            ("C", "D", "Yes"), ("D", "E", ""),
        ],
        "gates": (1, 0, 0),
        "sources": [
            {"title": "Robust multicellular computing using genetically encoded NOR gates and chemical 'wires'", "authors": "Tamsir A, Tabor JJ, Voigt CA", "journal": "Nature", "year": 2011, "volume": "469", "pages": "212-215", "pmid": "21150903", "doi": "10.1038/nature09565"},
        ],
        "keywords": ["OR gate", "logic gate", "tandem promoter", "feed-forward", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_and_gate"],
        "notes": "Ground-truth Class I logic element: one OR gate, no feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "PLtetO-1", "boundFactor": "TetR (relieved by aTc)", "operator": "IF", "effect": "activation on induction", "sequenceMotif": "TCCCTATCAGTGATAGAGA", "note": "first promoter in tandem"},
                {"name": "Plux", "boundFactor": "LuxR-AHL", "operator": "IF", "effect": "activation on induction", "sequenceMotif": "ACCTGTAGGATCGTACAGGT (lux box)", "note": "second promoter in tandem"},
            ],
            "derivedLogic": "Output = Input1 OR Input2",
            "references": ["Tamsir et al. 2011"],
        },
    },
    {
        "id": "synthetic_band_detector",
        "name": "Band-Pass / Edge Detector (Basu 2005)",
        "circuitClass": "I",
        "topologyType": "incoherent_feed_forward_band_pass",
        "rationale": "An incoherent feed-forward arrangement with a low-threshold activating branch and a high-threshold repressing branch makes the output ON only for an intermediate inducer concentration: output = LOW-on AND NOT HIGH-on. Feed-forward topology (Class I), functional band-pass (Basu et al. 2005).",
        "description": "A synthetic band-pass filter: a diffusible signal feeds two branches with different thresholds. The low-threshold branch activates the reporter; the high-threshold branch represses it. The output is therefore ON only at intermediate signal levels, producing concentric ring patterns in a lawn of receiver cells — an edge/band detector.",
        "scientificAccuracy": "Ground-truth circuit. The band-detect receiver and ring patterning were built and characterized by Basu, Gerchman, Collins, Arnold & Weiss (2005).",
        "nodes": [
            ("A", "[AHL concentration gradient]", "red"),
            ("B", "[Low-threshold branch: activates]", "yellow"),
            ("C", "[High-threshold branch: represses]", "yellow"),
            ("D", "[Low AHL activates reporter]", "green"),
            ("E", "[/High AHL represses reporter/]", "green"),
            ("F", "{Low-on AND NOT High-on?}", "blue"),
            ("G", "(Output GFP: band-pass)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("A", "C", ""),
            ("B", "D", ""), ("C", "E", ""),
            ("D", "F", ""), ("E", "F", "⊣"),
            ("F", "G", "Yes"),
        ],
        "gates": (0, 1, 1),
        "sources": [
            {"title": "A synthetic multicellular system for programmed pattern formation", "authors": "Basu S, Gerchman Y, Collins CH, Arnold FH, Weiss R", "journal": "Nature", "year": 2005, "volume": "434", "pages": "1130-1134", "pmid": "15858574", "doi": "10.1038/nature03461"},
        ],
        "keywords": ["band detector", "band-pass", "edge detection", "incoherent feed-forward", "pattern formation", "Class I", "ground truth"],
        "relatedProcesses": ["synthetic_incoherent_ffl"],
        "notes": "Ground-truth Class I (feed-forward) circuit with band-pass function: one AND + one NOT, no feedback edge.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "lux promoter (low-threshold)", "boundFactor": "LuxR-AHL (high affinity)", "operator": "IF", "effect": "activation at low AHL", "sequenceMotif": "ACCTGTAGGATCGTACAGGT", "note": "drives reporter and a repressor"},
                {"name": "reporter promoter (repressed at high AHL)", "boundFactor": "CI/LacI repressor (induced at high AHL)", "operator": "NOT", "effect": "repression at high AHL", "sequenceMotif": "(operator)", "note": "sets the upper edge of the band"},
            ],
            "derivedLogic": "Output = (AHL > low) AND NOT (AHL > high)  -> band-pass",
            "references": ["Basu et al. 2005"],
        },
    },
    # ----------------------------------------------------------------- Class II
    {
        "id": "synthetic_population_control",
        "name": "Quorum-Sensing Population Control (You 2004)",
        "circuitClass": "II",
        "topologyType": "quorum_sensing_negative_feedback",
        "rationale": "Cell density drives LuxI/AHL synthesis; accumulated AHL activates LuxR, which induces a killer gene that raises death rate — a density-dependent negative-feedback loop that holds the population at a programmed set-point (You, Cox, Weiss & Arnold 2004). Class II.",
        "description": "An engineered population-control circuit. Each cell makes the autoinducer AHL via LuxI; as density rises AHL accumulates and, through LuxR, induces the killer protein CcdB. Higher density therefore raises the death rate, a negative feedback that stabilizes the population below the carrying capacity at a programmable set-point.",
        "scientificAccuracy": "Ground-truth circuit. Built and characterized in E. coli by You, Cox, Weiss & Arnold (2004).",
        "nodes": [
            ("A", "[Cell density]", "red"),
            ("B", "[LuxI makes AHL]", "green"),
            ("C", "[AHL accumulates]", "blue"),
            ("D", "[LuxR-AHL]", "yellow"),
            ("E", "[Killer gene CcdB expressed]", "green"),
            ("F", "[/Cell death lowers density/]", "green"),
            ("G", "(Steady-state population set-point)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "F", ""), ("F", "A", "⊣ feedback"),
            ("D", "G", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Programmed population control by cell-cell communication and regulated killing", "authors": "You L, Cox RS 3rd, Weiss R, Arnold FH", "journal": "Nature", "year": 2004, "volume": "428", "pages": "868-871", "pmid": "15064770", "doi": "10.1038/nature02491"},
        ],
        "keywords": ["population control", "quorum sensing", "LuxR", "LuxI", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["synthetic_negative_autoregulation"],
        "notes": "Ground-truth Class II circuit: density-dependent negative feedback (one feedback edge).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Plux (killer-gene promoter)", "boundFactor": "LuxR-AHL", "operator": "IF", "effect": "activation of CcdB at high density", "sequenceMotif": "ACCTGTAGGATCGTACAGGT (lux box)", "note": "couples density to death rate -> negative feedback on population"},
            ],
            "derivedLogic": "death_rate = LuxR-AHL = f(density)  -> negative feedback set-point",
            "references": ["You et al. 2004"],
        },
    },
    # ---------------------------------------------------------------- Class III
    {
        "id": "synthetic_crispri_toggle",
        "name": "CRISPRi Mutual-Repression Toggle",
        "circuitClass": "III",
        "topologyType": "mutual_repression_bistable_crispri",
        "rationale": "Two sgRNAs guide dCas9 to repress each other's promoters; the double-negative loop is bistable with two stable states, a CRISPRi implementation of the toggle switch (Santos-Moreno et al. 2020; Zhang & Voigt 2018). Class III.",
        "description": "A bistable toggle built with CRISPR interference instead of protein repressors. Two single-guide RNAs each direct catalytically dead Cas9 (dCas9) to silence the promoter expressing the other sgRNA. The mutual repression yields two stable states; transient induction flips the latch — a programmable, sequence-addressable memory element.",
        "scientificAccuracy": "Ground-truth circuit. CRISPRi-based bistable toggles and layered logic were demonstrated (Santos-Moreno et al. 2020; Zhang & Voigt 2018).",
        "nodes": [
            ("A", "[Input pulses]", "red"),
            ("B", "[sgRNA-1 + dCas9]", "yellow"),
            ("C", "[sgRNA-2 + dCas9]", "yellow"),
            ("D", "[/sgRNA-1 represses promoter 2/]", "green"),
            ("E", "[/sgRNA-2 represses promoter 1/]", "green"),
            ("F", "(Stable state 1)", "violet"),
            ("G", "(Stable state 2)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("A", "C", ""),
            ("B", "D", ""), ("D", "C", "⊣"),
            ("C", "E", ""), ("E", "B", "⊣"),
            ("B", "F", ""), ("C", "G", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "Multistable and dynamic CRISPRi-based synthetic circuits", "authors": "Santos-Moreno J, Tasiudi E, Stelling J, Schaerli Y", "journal": "Nature Communications", "year": 2020, "volume": "11", "pages": "2746", "pmid": "32488086", "doi": "10.1038/s41467-020-16574-1"},
        ],
        "keywords": ["CRISPRi", "dCas9", "toggle switch", "bistable", "mutual repression", "Class III", "ground truth"],
        "relatedProcesses": ["synthetic_toggle_switch"],
        "notes": "Ground-truth Class III bistable toggle (CRISPRi): two mutual repressions (2 NOT).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "promoter 1 (sgRNA-2 target)", "boundFactor": "dCas9-sgRNA2", "operator": "NOT", "effect": "CRISPRi repression", "sequenceMotif": "20-nt protospacer + NGG PAM", "note": "guide programmable; blocks transcription"},
                {"name": "promoter 2 (sgRNA-1 target)", "boundFactor": "dCas9-sgRNA1", "operator": "NOT", "effect": "CRISPRi repression", "sequenceMotif": "20-nt protospacer + NGG PAM", "note": ""},
            ],
            "derivedLogic": "sgRNA1 = NOT sgRNA2 ; sgRNA2 = NOT sgRNA1  -> two stable states",
            "references": ["Santos-Moreno et al. 2020"],
        },
    },
    # ----------------------------------------------------------------- Class IV
    {
        "id": "synthetic_metabolator",
        "name": "Metabolator (synthetic metabolic oscillator)",
        "circuitClass": "IV",
        "topologyType": "metabolic_delayed_negative_feedback_oscillator",
        "rationale": "A metabolic intermediate (acetyl-phosphate) drives expression of enzymes that both produce and consume it, with a delay; the resulting delayed negative feedback produces sustained oscillations in metabolite and gene expression (Fung, Wong, Suen, Bulter, Lee & Liao 2005). Class IV.",
        "description": "A synthetic oscillator wired through metabolism rather than pure transcription. Glycolytic flux feeds an acetyl-phosphate pool that transcriptionally activates Pta (which makes more acetyl-phosphate, positive arm) and Acs (which consumes it, delayed negative arm). The delayed negative feedback drives sustained oscillations in metabolite and reporter levels.",
        "scientificAccuracy": "Ground-truth circuit. The metabolator was built and shown to oscillate by Fung et al. (2005).",
        "nodes": [
            ("A", "[Glycolytic flux input]", "red"),
            ("B", "[Acetyl-phosphate pool]", "blue"),
            ("C", "[Activates Pta promoter]", "green"),
            ("D", "[\\Pta makes more AcP/]", "green"),
            ("E", "[/Acs consumes AcP, delayed/]", "green"),
            ("F", "(Metabolite / reporter oscillation)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""),
            ("C", "D", ""), ("D", "B", "+"),
            ("B", "E", ""), ("E", "B", "⊣ delayed"),
            ("B", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "A synthetic gene-metabolic oscillator", "authors": "Fung E, Wong WW, Suen JK, Bulter T, Lee SG, Liao JC", "journal": "Nature", "year": 2005, "volume": "435", "pages": "118-122", "pmid": "15875027", "doi": "10.1038/nature03508"},
        ],
        "keywords": ["metabolator", "metabolic oscillator", "acetyl-phosphate", "delayed negative feedback", "Class IV", "ground truth"],
        "relatedProcesses": ["synthetic_repressilator", "human_circadian_clock"],
        "notes": "Ground-truth Class IV oscillator coupling metabolism and gene expression (delayed negative feedback).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Pta/Acs promoter (AcP-responsive)", "boundFactor": "acetyl-phosphate-responsive regulator", "operator": "IF / delayed NOT", "effect": "activation of producing + consuming enzymes", "sequenceMotif": "(AcP-responsive promoter)", "note": "couples metabolite level to enzyme expression with delay"},
            ],
            "derivedLogic": "Pta = AcP (positive) ; Acs = AcP (delayed negative) -> oscillation",
            "references": ["Fung et al. 2005"],
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
    print(f"Wrote {len(rows)} synthetic Batch-2 process files -> {OUT_DIR}\n")
    print(f"{'id':<40} {'cls':<4} {'nodes':<6} {'edges':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<40} {r[1]:<4} {r[2]:<6} {r[3]:<6} {r[4]:<6} {r[5]}")


if __name__ == "__main__":
    main()
