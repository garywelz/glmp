#!/usr/bin/env python3
"""
Batch 3 of the GLMP collection: a broad set of canonical *human* regulatory circuits,
spanning the complexity ladder, each with an authored class and a sequence->logic
annotation. Extends Batch 2 (build_human_batch2.py).

Coverage (honest class assignment from primary literature):
  Cell-fate bistable switches (Class III, persistent = IIIa):
    OCT4/SOX2/NANOG pluripotency, MyoD myogenesis, T-bet/GATA3 (Th1/Th2),
    Rb-E2F restriction point, Cdk1-Cdc25-Wee1 mitotic trigger, caspase apoptosis.
  Oscillators (Class IV): NF-kB/IkB, circadian BMAL1-CLOCK/PER-CRY.
  Negative-feedback signaling (Class II): Wnt/beta-catenin, TGF-beta/SMAD.
  Other bistable signaling (Class III): Notch-Delta lateral inhibition, ERK.

Reuses Batch 2's make_process (organism = Homo sapiens, groundTruth).
Output: glmp-v2/processes/human/<id>.json
"""

import json
from pathlib import Path

from build_human_batch2 import make_process, OUT_DIR

SPECS = [
    # ───────────────────────── Class III / IIIa — cell-fate bistable switches ─────────────────────────
    {
        "id": "human_oct4_sox2_nanog_pluripotency",
        "name": "OCT4–SOX2–NANOG Pluripotency Core",
        "category": "Stem Cell / Pluripotency",
        "circuitClass": "III", "circuitSubclass": "IIIa",
        "topologyType": "interlocked_positive_feedback_bistable",
        "rationale": "OCT4 and SOX2 form a heterodimer that activates NANOG and their own genes; the interlocked positive-feedback core is bistable, locking cells into a self-sustaining pluripotent state — a persistent (IIIa) switch with memory.",
        "description": "The core pluripotency network. An OCT4–SOX2 heterodimer co-activates NANOG and reinforces its own expression at composite octamer–sox enhancers. The interlocked positive feedback makes pluripotency a self-sustaining attractor; collapse of the loop triggers differentiation.",
        "scientificAccuracy": "OCT4/SOX2/NANOG auto- and cross-activation and the bistable interpretation are well established (Boyer et al. 2005; Chickarmane et al. 2006).",
        "nodes": [
            ("A", "[Pluripotency signals: LIF / BMP]", "red"),
            ("B", "[OCT4-SOX2 heterodimer]", "yellow"),
            ("C", "[NANOG]", "yellow"),
            ("D", "[\\OCT4-SOX2 autoactivation/]", "green"),
            ("E", "[/Represses differentiation genes/]", "green"),
            ("F", "(Self-renewing pluripotent state)", "violet"),
            ("G", "(Differentiated state)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "D", ""), ("D", "B", "+"),
            ("B", "C", ""), ("C", "B", "+"),
            ("B", "E", ""), ("E", "G", "⊣"), ("B", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Core transcriptional regulatory circuitry in human embryonic stem cells", "authors": "Boyer LA, Lee TI, Cole MF, et al.", "journal": "Cell", "year": 2005, "volume": "122", "pages": "947-956", "pmid": "16153702", "doi": "10.1016/j.cell.2005.08.020"},
            {"title": "Transcriptional dynamics of the embryonic stem cell switch", "authors": "Chickarmane V, Troein C, Nuber UA, Sauro HM, Peterson C", "journal": "PLoS Computational Biology", "year": 2006, "volume": "2", "pages": "e123", "pmid": "16978048", "doi": "10.1371/journal.pcbi.0020123"},
        ],
        "keywords": ["OCT4", "SOX2", "NANOG", "pluripotency", "bistable", "positive feedback", "Class IIIa", "ground truth"],
        "relatedProcesses": ["human_gata1_pu1_switch", "synthetic_positive_autoregulation"],
        "notes": "Human Class IIIa pluripotency switch: interlocked positive feedback (2 activating loops) + repression of differentiation.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "oct-sox composite element", "boundFactor": "OCT4-SOX2", "operator": "AND", "effect": "activation", "sequenceMotif": "ATGCAAAT + CATTGTT", "note": "adjacent octamer (OCT4) and sox (SOX2) sites; cooperative binding"},
            ],
            "derivedLogic": "NANOG, OCT4, SOX2 = OCT4 AND SOX2 (interlocked positive feedback) -> bistable pluripotency",
            "references": ["Boyer et al. 2005"],
        },
    },
    {
        "id": "human_myod_myogenesis",
        "name": "MyoD Myogenic Determination Switch",
        "category": "Myogenesis",
        "circuitClass": "III", "circuitSubclass": "IIIa",
        "topologyType": "positive_autoregulation_bistable",
        "rationale": "MyoD activates its own promoter (positive autoregulation) and E-box myogenic targets, producing a bistable, self-sustaining commitment to the muscle program — a persistent (IIIa) determination switch.",
        "description": "MyoD is a master myogenic bHLH factor that activates its own gene and the muscle differentiation program through E-box (CANNTG) sites. Positive autoregulation makes myogenic commitment a latching switch: once MyoD passes threshold, the muscle fate is maintained even without the initiating signal.",
        "scientificAccuracy": "MyoD positive autoregulation and E-box-driven myogenic determination are established (Thayer et al. 1989; Weintraub 1993).",
        "nodes": [
            ("A", "[Myogenic signal]", "red"),
            ("B", "[MyoD]", "yellow"),
            ("C", "[\\MyoD positive autoregulation/]", "green"),
            ("D", "[E-box target activation: muscle genes]", "green"),
            ("E", "(Committed myoblast / differentiation)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "B", "+"),
            ("B", "D", ""), ("D", "E", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "Positive autoregulation of the myogenic determination gene MyoD1", "authors": "Thayer MJ, Tapscott SJ, Davis RL, Wright WE, Lassar AB, Weintraub H", "journal": "Cell", "year": 1989, "volume": "58", "pages": "241-248", "pmid": "2546677", "doi": "10.1016/0092-8674(89)90838-6"},
        ],
        "keywords": ["MyoD", "myogenesis", "positive autoregulation", "bistable", "bHLH", "E-box", "Class IIIa", "ground truth"],
        "relatedProcesses": ["synthetic_positive_autoregulation"],
        "notes": "Human Class IIIa determination switch via positive autoregulation (the human analogue of synthetic PAR).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "myogenic E-box (self + targets)", "boundFactor": "MyoD-E2A", "operator": "IF", "effect": "activation", "sequenceMotif": "CANNTG", "note": "MyoD binds its own enhancer (autoactivation) and muscle-gene E-boxes"},
            ],
            "derivedLogic": "MyoD = IF MyoD(t-τ) > threshold (positive autoregulation) -> latched muscle program",
            "references": ["Thayer et al. 1989"],
        },
    },
    {
        "id": "human_tbet_gata3_th1_th2",
        "name": "T-bet–GATA3 Th1/Th2 Lineage Switch",
        "category": "Immune Differentiation",
        "circuitClass": "III", "circuitSubclass": "IIIa",
        "topologyType": "mutual_repression_dual_autoactivation_bistable",
        "rationale": "T-bet and GATA3 cross-antagonize while each autoactivates, the same double-positive/double-negative topology as GATA1/PU.1 — a persistent (IIIa) bistable switch between Th1 and Th2 helper-T fates.",
        "description": "Naive CD4 T cells choose between Th1 and Th2 fates via the master regulators T-bet and GATA3, which repress each other and amplify themselves. The mutual-repression-plus-autoactivation circuit is bistable, committing the cell to IFN-γ (Th1) or IL-4 (Th2) programs.",
        "scientificAccuracy": "T-bet/GATA3 cross-regulation and autoactivation underpinning bistable Th1/Th2 commitment are established (Szabo et al. 2000; Höfer et al. 2002).",
        "nodes": [
            ("A", "[Naive CD4 T cell + cytokines]", "red"),
            ("B", "[T-bet]", "yellow"),
            ("C", "[GATA3]", "yellow"),
            ("D", "[\\T-bet autoactivation/]", "green"),
            ("E", "[\\GATA3 autoactivation/]", "green"),
            ("F", "[/T-bet represses GATA3/]", "green"),
            ("G", "[/GATA3 represses T-bet/]", "green"),
            ("H", "(Th1 fate: IFN-gamma)", "violet"),
            ("I", "(Th2 fate: IL-4)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("A", "C", ""),
            ("B", "D", ""), ("D", "B", "+"),
            ("C", "E", ""), ("E", "C", "+"),
            ("B", "F", ""), ("F", "C", "⊣"),
            ("C", "G", ""), ("G", "B", "⊣"),
            ("B", "H", ""), ("C", "I", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "A novel transcription factor, T-bet, directs Th1 lineage commitment", "authors": "Szabo SJ, Kim ST, Costa GL, Zhang X, Fathman CG, Glimcher LH", "journal": "Cell", "year": 2000, "volume": "100", "pages": "655-669", "pmid": "10761931", "doi": "10.1016/S0092-8674(00)80702-3"},
        ],
        "keywords": ["T-bet", "GATA3", "Th1", "Th2", "bistable", "mutual repression", "Class IIIa", "ground truth"],
        "relatedProcesses": ["human_gata1_pu1_switch", "synthetic_toggle_switch"],
        "notes": "Human Class IIIa immune toggle: 2 cross-repressions + 2 autoactivations.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "T-box site", "boundFactor": "T-bet (TBX21)", "operator": "IF/NOT", "effect": "activation (Th1) / repression (Th2 loci)", "sequenceMotif": "AGGTGTGAAATT", "note": "T-box consensus"},
                {"name": "GATA site", "boundFactor": "GATA3", "operator": "IF/NOT", "effect": "activation (Th2) / repression (Th1 loci)", "sequenceMotif": "WGATAR", "note": ""},
            ],
            "derivedLogic": "T-bet = T-bet AND NOT GATA3 ; GATA3 = GATA3 AND NOT T-bet -> bistable Th1/Th2",
            "references": ["Szabo et al. 2000"],
        },
    },
    {
        "id": "human_rb_e2f_restriction_point",
        "name": "Rb–E2F Restriction-Point Switch",
        "category": "Cell Cycle",
        "circuitClass": "III", "circuitSubclass": "IIIa",
        "topologyType": "double_negative_positive_feedback_bistable",
        "rationale": "Mitogen-driven CDK phosphorylation inactivates Rb, releasing E2F; E2F drives Cyclin E, which further inactivates Rb (positive feedback through a double-negative), making the G1/S restriction point a bistable, irreversible commitment (Yao et al. 2008).",
        "description": "The mammalian restriction point. Mitogens activate Cyclin D-CDK4/6 to phosphorylate (inactivate) Rb, freeing E2F; E2F induces Cyclin E-CDK2 which hyperphosphorylates Rb, a positive-feedback loop that converts graded mitogen input into an all-or-none, memory-bearing commitment to S phase.",
        "scientificAccuracy": "Bistability of the Rb-E2F switch was demonstrated quantitatively at the single-cell level (Yao, Lee, Nevins & You 2008).",
        "nodes": [
            ("A", "[Mitogen: Cyclin D-CDK4/6]", "red"),
            ("B", "[Rb]", "yellow"),
            ("C", "[E2F]", "yellow"),
            ("D", "[/Rb represses E2F/]", "green"),
            ("E", "[\\E2F drives Cyclin E, inactivates Rb/]", "green"),
            ("F", "(Restriction point passed: S phase)", "violet"),
        ],
        "edges": [
            ("A", "B", "⊣ phosphorylate"),
            ("B", "D", ""), ("D", "C", "⊣"),
            ("C", "E", ""), ("E", "B", "⊣ feedback"),
            ("C", "F", ""),
        ],
        "gates": (0, 0, 3),
        "sources": [
            {"title": "A bistable Rb-E2F switch underlies the restriction point", "authors": "Yao G, Lee TJ, Mori S, Nevins JR, You L", "journal": "Nature Cell Biology", "year": 2008, "volume": "10", "pages": "476-482", "pmid": "18364697", "doi": "10.1038/ncb1711"},
        ],
        "keywords": ["Rb", "E2F", "restriction point", "bistable", "positive feedback", "cell cycle", "Class IIIa", "ground truth"],
        "relatedProcesses": ["human_cdk1_mitotic_switch"],
        "notes": "Human Class IIIa bistable switch; positive feedback realized through a double-negative (Rb ⊣ E2F ; CycE ⊣ Rb).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "E2F site", "boundFactor": "E2F-DP (repressed by Rb)", "operator": "IF / NOT(Rb)", "effect": "activation when Rb inactive", "sequenceMotif": "TTTSSCGC", "note": "Rb binds E2F to block activation; CDK phosphorylation of Rb relieves repression"},
            ],
            "derivedLogic": "E2F targets = NOT Rb ; Rb inactivated by mitogen AND by E2F-driven CycE -> bistable",
            "references": ["Yao et al. 2008"],
        },
    },
    {
        "id": "human_cdk1_mitotic_switch",
        "name": "Cdk1–Cdc25–Wee1 Mitotic Trigger",
        "category": "Cell Cycle",
        "circuitClass": "III",
        "topologyType": "interlocked_feedback_bistable_trigger",
        "rationale": "Cdk1-cyclin B activates its activator Cdc25 (positive feedback) and inhibits its inhibitor Wee1 (double-negative), producing a bistable, hysteretic all-or-none trigger for mitotic entry (Novak-Tyson; Sha et al. 2003; Pomerening et al. 2003).",
        "description": "Entry into mitosis is a snap-action switch. Cdk1-cyclin B activates the phosphatase Cdc25 (which activates Cdk1) and inhibits the kinase Wee1 (which inhibits Cdk1). The interlocked positive and double-negative feedback give bistability and hysteresis — mitosis commits in an all-or-none, irreversible step.",
        "scientificAccuracy": "Bistability and hysteresis of the Cdk1 system were demonstrated in Xenopus extracts (Sha et al. 2003; Pomerening et al. 2003); the Novak-Tyson model is the canonical description.",
        "nodes": [
            ("A", "[Cyclin B accumulation]", "red"),
            ("B", "[Cdk1-Cyclin B]", "yellow"),
            ("C", "[Cdc25 phosphatase]", "yellow"),
            ("D", "[Wee1 kinase]", "yellow"),
            ("E", "[\\Cdk1 activates Cdc25, which activates Cdk1/]", "green"),
            ("F", "[/Cdk1 inhibits Wee1, disinhibiting Cdk1/]", "green"),
            ("G", "(Mitotic entry: all-or-none)", "violet"),
        ],
        "edges": [
            ("A", "B", ""),
            ("B", "C", ""), ("C", "E", ""), ("E", "B", "+"),
            ("B", "D", ""), ("D", "F", ""), ("F", "B", "⊣"),
            ("B", "G", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Hysteresis drives cell-cycle transitions in Xenopus laevis egg extracts", "authors": "Sha W, Moore J, Chen K, Lassaletta AD, Yi CS, Tyson JJ, Sible JC", "journal": "PNAS", "year": 2003, "volume": "100", "pages": "975-980", "pmid": "12509509", "doi": "10.1073/pnas.0235349100"},
            {"title": "Building a cell cycle oscillator: hysteresis and bistability in the activation of Cdc2", "authors": "Pomerening JR, Sontag ED, Ferrell JE", "journal": "Nature Cell Biology", "year": 2003, "volume": "5", "pages": "346-351", "pmid": "12629549", "doi": "10.1038/ncb954"},
        ],
        "keywords": ["Cdk1", "Cdc25", "Wee1", "bistable", "hysteresis", "mitosis", "Class III", "ground truth"],
        "relatedProcesses": ["yeast_cell_cycle_control", "human_rb_e2f_restriction_point"],
        "notes": "Human Class III bistable trigger (interlocked positive + double-negative feedback). Within the cell-cycle oscillator (Class IV) this is the switch sub-module.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Cdk1 activity (post-translational)", "boundFactor": "Cdc25 (activator), Wee1 (inhibitor)", "operator": "AND / NOT", "effect": "phospho-activation vs inhibitory phosphorylation", "sequenceMotif": "(protein-level: Tyr15 / Thr14)", "note": "switch implemented in phosphorylation state, not cis-DNA"},
            ],
            "derivedLogic": "Cdk1_active = Cdc25 AND NOT Wee1 ; both controlled by Cdk1 -> bistable",
            "references": ["Pomerening et al. 2003"],
        },
    },
    {
        "id": "human_apoptosis_caspase_switch",
        "name": "Caspase Apoptosis Commitment Switch",
        "category": "Apoptosis",
        "circuitClass": "III",
        "topologyType": "positive_feedback_irreversible_bistable",
        "rationale": "Effector caspase-3 feeds back to amplify its own activation and cleaves the inhibitor XIAP (double-negative), producing an all-or-none, irreversible apoptosis commitment — a bistable Class III switch.",
        "description": "Apoptosis executes as a switch, not a dial. After mitochondrial outer-membrane permeabilization, cytochrome c forms the apoptosome and activates caspase-9, then caspase-3. Caspase-3 amplifies its own activation and cleaves the inhibitor XIAP, positive feedback that makes commitment to death all-or-none and irreversible.",
        "scientificAccuracy": "Bistable, irreversible caspase activation with feedback through XIAP cleavage is established (Legewie, Blüthgen & Herzel 2006; Albeck et al. 2008).",
        "nodes": [
            ("A", "[Death signal / MOMP]", "red"),
            ("B", "[Cytochrome c + apoptosome]", "yellow"),
            ("C", "[Caspase-9 active]", "green"),
            ("D", "[Caspase-3 active]", "yellow"),
            ("E", "[\\Caspase-3 amplifies caspase-9/]", "green"),
            ("F", "[/Cleaves XIAP inhibitor/]", "green"),
            ("G", "(Irreversible apoptosis commitment)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "C", "+"),
            ("D", "F", ""), ("F", "C", "+ disinhibit"),
            ("D", "G", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Mathematical modeling identifies inhibitors of apoptosis as mediators of positive feedback and bistability", "authors": "Legewie S, Blüthgen N, Herzel H", "journal": "PLoS Computational Biology", "year": 2006, "volume": "2", "pages": "e120", "pmid": "16978046", "doi": "10.1371/journal.pcbi.0020120"},
        ],
        "keywords": ["apoptosis", "caspase", "bistable", "positive feedback", "XIAP", "irreversible", "Class III", "ground truth"],
        "relatedProcesses": ["synthetic_positive_autoregulation"],
        "notes": "Human Class III irreversible bistable switch via caspase-3 positive feedback + XIAP cleavage.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "caspase activation (proteolytic)", "boundFactor": "caspase-3 / XIAP", "operator": "positive feedback / NOT", "effect": "self-amplifying proteolysis", "sequenceMotif": "(protein-level: DEVD cleavage)", "note": "switch implemented in proteolytic cascade, not cis-DNA"},
            ],
            "derivedLogic": "Casp3 = Casp9 AND positive-feedback(Casp3) AND NOT XIAP -> irreversible commitment",
            "references": ["Legewie et al. 2006"],
        },
    },
    # ───────────────────────── Class IV — human oscillators ─────────────────────────
    {
        "id": "human_nfkb_ikb_oscillator",
        "name": "NF-κB–IκB Inflammatory Oscillator",
        "category": "Inflammatory Signaling",
        "circuitClass": "IV",
        "topologyType": "delayed_negative_feedback_oscillator",
        "rationale": "NF-κB induces its own inhibitor IκB, which resequesters NF-κB in the cytoplasm — a delayed negative-feedback loop that produces oscillatory nuclear NF-κB after TNF stimulation (Hoffmann et al. 2002; Nelson et al. 2004). Class IV.",
        "description": "On TNF/IL-1 signaling, IKK degrades IκB, freeing NF-κB to enter the nucleus and transcribe inflammatory genes — including IκBα itself, which resequesters NF-κB in the cytoplasm. The transcription-delayed negative feedback drives damped oscillations of nuclear NF-κB whose timing shapes gene expression.",
        "scientificAccuracy": "NF-κB-IκB negative-feedback oscillations are directly measured (Hoffmann et al. 2002; Nelson et al. 2004).",
        "nodes": [
            ("A", "[TNF / IL-1 signal]", "red"),
            ("B", "[IKK active]", "green"),
            ("C", "[/IκB degraded/]", "green"),
            ("D", "[NF-κB nuclear]", "yellow"),
            ("E", "[Inflammatory gene transcription]", "green"),
            ("F", "[IκBα resynthesized]", "yellow"),
            ("G", "[/IκB resequesters NF-κB/]", "green"),
            ("H", "(Oscillatory NF-κB localization)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("D", "F", ""), ("F", "G", ""),
            ("G", "D", "⊣ delayed"), ("E", "H", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "The IκB-NF-κB signaling module: temporal control and selective gene activation", "authors": "Hoffmann A, Levchenko A, Scott ML, Baltimore D", "journal": "Science", "year": 2002, "volume": "298", "pages": "1241-1245", "pmid": "12424381", "doi": "10.1126/science.1071914"},
            {"title": "Oscillations in NF-κB signaling control the dynamics of gene expression", "authors": "Nelson DE, Ihekwaba AE, Elliott M, et al.", "journal": "Science", "year": 2004, "volume": "306", "pages": "704-708", "pmid": "15499023", "doi": "10.1126/science.1099962"},
        ],
        "keywords": ["NF-κB", "IκB", "oscillator", "negative feedback", "inflammation", "Class IV", "ground truth"],
        "relatedProcesses": ["human_p53_mdm2", "synthetic_repressilator"],
        "notes": "Human Class IV oscillator; NF-κB induces its own inhibitor (delayed negative feedback).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "κB site (incl. NFKBIA/IκBα promoter)", "boundFactor": "NF-κB (p65/p50)", "operator": "IF", "effect": "activation (incl. its own inhibitor)", "sequenceMotif": "GGGRNWYYCC", "note": "NF-κB induces IκBα, closing the negative-feedback loop"},
            ],
            "derivedLogic": "targets, IκB = NF-κB ; NF-κB = NOT IκB(t-τ) -> delayed negative feedback -> oscillation",
            "references": ["Hoffmann et al. 2002"],
        },
    },
    {
        "id": "human_circadian_clock",
        "name": "Circadian Clock (BMAL1/CLOCK–PER/CRY)",
        "category": "Circadian Rhythm",
        "circuitClass": "IV",
        "topologyType": "transcription_translation_feedback_oscillator",
        "rationale": "BMAL1-CLOCK activates Per and Cry through E-boxes; PER-CRY complexes then repress BMAL1-CLOCK — a transcription-translation negative-feedback loop with ~24 h delay producing self-sustained oscillations. Class IV.",
        "description": "The mammalian circadian oscillator. The BMAL1-CLOCK activator drives Per and Cry transcription at E-boxes; PER-CRY proteins accumulate, enter the nucleus, and repress BMAL1-CLOCK. The built-in transcription-translation-degradation delay yields a free-running ~24 h rhythm entrained by light/metabolic cues.",
        "scientificAccuracy": "The TTFL architecture of the mammalian clock is established (Reppert & Weaver 2002).",
        "nodes": [
            ("A", "[Light / metabolic cue]", "red"),
            ("B", "[BMAL1-CLOCK]", "yellow"),
            ("C", "[E-box activation: Per, Cry]", "green"),
            ("D", "[PER-CRY complex]", "yellow"),
            ("E", "[/PER-CRY represses BMAL1-CLOCK/]", "green"),
            ("F", "(~24 h oscillation)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "B", "⊣ delayed"), ("B", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Coordination of circadian timing in mammals", "authors": "Reppert SM, Weaver DR", "journal": "Nature", "year": 2002, "volume": "418", "pages": "935-941", "pmid": "12198538", "doi": "10.1038/nature00965"},
        ],
        "keywords": ["circadian", "BMAL1", "CLOCK", "PER", "CRY", "oscillator", "Class IV", "ground truth"],
        "relatedProcesses": ["synthetic_repressilator", "human_nfkb_ikb_oscillator"],
        "notes": "Human Class IV transcription-translation feedback oscillator.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "E-box (Per/Cry promoters)", "boundFactor": "BMAL1-CLOCK", "operator": "IF", "effect": "activation", "sequenceMotif": "CACGTG", "note": "PER-CRY then represses the activator (delayed negative feedback)"},
            ],
            "derivedLogic": "Per,Cry = BMAL1-CLOCK ; BMAL1-CLOCK = NOT PER-CRY(t-τ) -> ~24 h oscillation",
            "references": ["Reppert & Weaver 2002"],
        },
    },
    # ───────────────────────── Class II — human negative-feedback signaling ─────────────────────────
    {
        "id": "human_wnt_beta_catenin",
        "name": "Wnt–β-catenin Destruction-Complex Switch",
        "category": "Developmental Signaling",
        "circuitClass": "II",
        "topologyType": "destruction_complex_negative_feedback",
        "rationale": "Without Wnt, the APC/Axin/GSK3 destruction complex degrades β-catenin; Wnt inhibits the complex so β-catenin accumulates and activates TCF/LEF targets — including Axin2, a negative-feedback brake. Switch-like in Wnt but homeostatic in topology — Class II.",
        "description": "The canonical Wnt pathway. The APC/Axin/GSK3 destruction complex keeps cytoplasmic β-catenin low; Wnt binding inactivates the complex, so β-catenin accumulates, enters the nucleus, and activates TCF/LEF targets such as c-Myc and Axin2. Axin2 reconstitutes the destruction complex, a negative-feedback loop that re-tunes the set-point.",
        "scientificAccuracy": "Destruction-complex regulation and Axin2 negative feedback are established (Clevers & Nusse 2012; Lustig et al. 2002).",
        "nodes": [
            ("A", "[Wnt ligand]", "red"),
            ("B", "{Wnt present?}", "blue"),
            ("C", "[Destruction complex: APC/Axin/GSK3]", "yellow"),
            ("D", "[/β-catenin degraded/]", "green"),
            ("E", "[β-catenin stabilized]", "yellow"),
            ("F", "[TCF/LEF target activation]", "green"),
            ("G", "[/Axin2 reinforces destruction complex/]", "green"),
            ("H", "(Targets: c-Myc, Axin2)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", "No"), ("C", "D", ""),
            ("B", "E", "Yes"), ("E", "F", ""), ("F", "H", ""),
            ("F", "G", ""), ("G", "C", "+ feedback"),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Wnt/β-catenin signaling and disease", "authors": "Clevers H, Nusse R", "journal": "Cell", "year": 2012, "volume": "149", "pages": "1192-1205", "pmid": "22682243", "doi": "10.1016/j.cell.2012.05.012"},
        ],
        "keywords": ["Wnt", "β-catenin", "TCF", "LEF", "Axin2", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_vhl_hif_oxygen_sensing"],
        "notes": "Human Class II circuit; switch-like β-catenin response with Axin2 negative feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "TCF/LEF site", "boundFactor": "β-catenin-TCF/LEF", "operator": "IF", "effect": "activation", "sequenceMotif": "CTTTGWW", "note": "induces Axin2 -> negative feedback on β-catenin"},
            ],
            "derivedLogic": "targets = Wnt (-| destruction complex) ; Axin2 = target -| β-catenin (negative feedback)",
            "references": ["Clevers & Nusse 2012"],
        },
    },
    {
        "id": "human_tgfbeta_smad",
        "name": "TGF-β–SMAD Signaling with SMAD7 Feedback",
        "category": "Developmental Signaling",
        "circuitClass": "II",
        "topologyType": "smad7_negative_feedback",
        "rationale": "TGF-β activates SMAD2/3, which with SMAD4 enter the nucleus and induce targets including the inhibitory SMAD7, which blocks the receptor — a negative-feedback loop that limits and adapts the response. Class II.",
        "description": "TGF-β receptors phosphorylate SMAD2/3, which partner with SMAD4 to drive transcription. Among the targets is inhibitory SMAD7, which binds the receptor and blocks further signaling — a negative-feedback loop giving adaptive, context-dependent TGF-β responses.",
        "scientificAccuracy": "SMAD signaling and SMAD7 negative feedback are established (Massagué 2012).",
        "nodes": [
            ("A", "[TGF-β ligand]", "red"),
            ("B", "[TGF-β receptor active]", "green"),
            ("C", "[SMAD2/3 phosphorylated]", "yellow"),
            ("D", "[SMAD complex + SMAD4 nuclear]", "green"),
            ("E", "[Target transcription]", "green"),
            ("F", "[SMAD7 induced]", "yellow"),
            ("G", "[/SMAD7 inhibits receptor/]", "green"),
            ("H", "(Adaptive context-dependent response)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "H", ""), ("D", "F", ""),
            ("F", "G", ""), ("G", "B", "⊣ feedback"),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "TGFβ signalling in context", "authors": "Massagué J", "journal": "Nature Reviews Molecular Cell Biology", "year": 2012, "volume": "13", "pages": "616-630", "pmid": "22992590", "doi": "10.1038/nrm3434"},
        ],
        "keywords": ["TGF-β", "SMAD", "SMAD7", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_wnt_beta_catenin"],
        "notes": "Human Class II signaling with SMAD7 negative feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "SMAD binding element", "boundFactor": "SMAD3/4", "operator": "IF", "effect": "activation (incl. SMAD7)", "sequenceMotif": "AGAC / GTCT", "note": "induces SMAD7 -> negative feedback on receptor"},
            ],
            "derivedLogic": "targets, SMAD7 = TGF-β ; receptor = NOT SMAD7 (negative feedback)",
            "references": ["Massagué 2012"],
        },
    },
    # ───────────────────────── Class III — other bistable signaling ─────────────────────────
    {
        "id": "human_notch_delta_lateral_inhibition",
        "name": "Notch–Delta Lateral Inhibition Switch",
        "category": "Developmental Patterning",
        "circuitClass": "III",
        "topologyType": "intercellular_mutual_inhibition_bistable",
        "rationale": "Delta on one cell activates Notch on its neighbor, and Notch signaling represses Delta in the receiving cell — an intercellular mutual-inhibition loop that amplifies small differences into a bistable salt-and-pepper pattern (Collier et al. 1996).",
        "description": "Lateral inhibition patterns equivalent cells into alternating fates. Delta ligand on one cell activates Notch on a neighbor; activated Notch represses Delta in that neighbor, so a cell making more Delta forces its neighbors to make less. The intercellular double-negative feedback is bistable and generates fine-grained salt-and-pepper patterns.",
        "scientificAccuracy": "The mutual-inhibition / bistable-patterning model of Notch-Delta lateral inhibition is established (Collier, Monk, Maini & Lewis 1996; Sprinzak et al. 2010).",
        "nodes": [
            ("A", "[Equivalent neighboring cells]", "red"),
            ("B", "[Cell 1: Delta high]", "yellow"),
            ("C", "[Cell 2: Notch active]", "yellow"),
            ("D", "[\\Delta activates Notch in neighbor/]", "green"),
            ("E", "[/Notch represses Delta in that cell/]", "green"),
            ("F", "(Alternating salt-and-pepper fates)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("A", "C", ""),
            ("B", "D", ""), ("D", "C", "+"),
            ("C", "E", ""), ("E", "B", "⊣"),
            ("B", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Pattern formation by lateral inhibition with feedback: a mathematical model of Delta-Notch intercellular signalling", "authors": "Collier JR, Monk NA, Maini PK, Lewis JH", "journal": "Journal of Theoretical Biology", "year": 1996, "volume": "183", "pages": "429-446", "pmid": "9015458", "doi": "10.1006/jtbi.1996.0233"},
        ],
        "keywords": ["Notch", "Delta", "lateral inhibition", "bistable", "patterning", "Class III", "ground truth"],
        "relatedProcesses": ["synthetic_toggle_switch"],
        "notes": "Human Class III intercellular bistable switch (lateral inhibition).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "CSL/RBPJ site (Notch targets, e.g. HES1)", "boundFactor": "NICD-RBPJ", "operator": "IF", "effect": "activation of repressors of Delta", "sequenceMotif": "TGGGAA", "note": "Notch target HES1 represses Delta -> intercellular double-negative"},
            ],
            "derivedLogic": "Notch_cellB = Delta_cellA ; Delta_cellB = NOT Notch_cellB -> bistable pattern",
            "references": ["Collier et al. 1996"],
        },
    },
    {
        "id": "human_erk_bistable_switch",
        "name": "ERK/MAPK Ultrasensitive Bistable Switch",
        "category": "Growth Factor Signaling",
        "circuitClass": "III",
        "topologyType": "ultrasensitive_positive_feedback_bistable",
        "rationale": "The RAF-MEK-ERK cascade is ultrasensitive, and positive feedback from ERK to RAF/SOS can make ERK activation bistable and all-or-none (Ferrell & Machleder 1998; Bhalla et al. 2002). Class III.",
        "description": "Growth-factor signaling through the RAF-MEK-ERK cascade is highly ultrasensitive, and positive feedback from ERK back to RAF/SOS can convert graded input into a bistable, switch-like ERK response that underlies all-or-none cell-fate decisions such as Xenopus oocyte maturation.",
        "scientificAccuracy": "Ultrasensitivity and bistable, all-or-none MAPK activation with feedback are established (Ferrell & Machleder 1998).",
        "nodes": [
            ("A", "[Growth factor: EGF]", "red"),
            ("B", "[RAS-RAF]", "yellow"),
            ("C", "[MEK]", "green"),
            ("D", "[ERK active]", "yellow"),
            ("E", "[\\ERK positive feedback to RAF/SOS/]", "green"),
            ("F", "[Ultrasensitive cascade]", "green"),
            ("G", "(Bistable ERK on/off; cell-fate)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "B", "+"),
            ("B", "F", ""), ("F", "D", ""), ("D", "G", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "The biochemical basis of an all-or-none cell fate switch in Xenopus oocytes", "authors": "Ferrell JE, Machleder EM", "journal": "Science", "year": 1998, "volume": "280", "pages": "895-898", "pmid": "9572732", "doi": "10.1126/science.280.5365.895"},
        ],
        "keywords": ["ERK", "MAPK", "ultrasensitivity", "bistable", "positive feedback", "Class III", "ground truth"],
        "relatedProcesses": ["human_erk_bistable_switch", "synthetic_positive_autoregulation"],
        "notes": "Human Class III bistable switch from cascade ultrasensitivity + positive feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "ERK signaling (post-translational + SRE targets)", "boundFactor": "ERK -> RSK/ELK1 -> SRF (SRE)", "operator": "positive feedback / IF", "effect": "kinase cascade; immediate-early gene activation", "sequenceMotif": "CCWWWWWWGG (SRE/CArG)", "note": "bistability arises in phospho-cascade; transcriptional output at SRE"},
            ],
            "derivedLogic": "ERK = ultrasensitive(RAF-MEK) AND positive-feedback(ERK) -> bistable on/off",
            "references": ["Ferrell & Machleder 1998"],
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
                     proc["totalNodes"], proc["loops"], proc["logicGates"]))
    print(f"Wrote {len(rows)} human Batch-3 process files -> {OUT_DIR}\n")
    print(f"{'id':<42} {'cls':<4} {'sub':<5} {'nodes':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<42} {r[1]:<4} {r[2]:<5} {r[3]:<6} {r[4]:<6} {r[5]}")


if __name__ == "__main__":
    main()
