#!/usr/bin/env python3
"""
Batch 6 of the GLMP collection: human signaling / disease circuits, extending
build_human_batch5.py. Immune checkpoint, proteostasis, autophagy, tumor-suppressor
feedback, a hormone-receptor bistable switch, and a calcium oscillator.

Honest class assignment:
  Class II  : PD-1/PD-L1 checkpoint, IRE1-XBP1 UPR, mTOR-ULK1 autophagy, PTEN-PI3K-AKT
  Class IIIa: estrogen-receptor positive-autoregulation switch
  Class IV  : IP3/Ca2+ oscillator (CICR)

Reuses Batch 2's make_process (organism = Homo sapiens, groundTruth).
Output: glmp-v2/processes/human/<id>.json
"""

import json

from build_human_batch2 import make_process, OUT_DIR

SPECS = [
    {
        "id": "human_pd1_pdl1_checkpoint",
        "name": "PD-1/PD-L1 Immune Checkpoint",
        "category": "Immune Checkpoint",
        "circuitClass": "II",
        "topologyType": "inhibitory_negative_feedback",
        "rationale": "T-cell activation and IFN-γ induce PD-L1 on target cells; PD-L1 engages PD-1, recruiting SHP-2 to dephosphorylate TCR-proximal signaling — a negative-feedback loop that dampens the response (and is hijacked by tumors). Class II.",
        "description": "The adaptive immune brake exploited in cancer. Activated T cells secrete IFN-γ, which induces PD-L1 on tumor/antigen-presenting cells; PD-L1 binding PD-1 recruits the SHP-2 phosphatase that dephosphorylates TCR signaling components, feeding back to suppress T-cell activation. Checkpoint-blockade antibodies cut this negative loop.",
        "scientificAccuracy": "IFN-γ-induced PD-L1 and PD-1/SHP-2 inhibition of TCR signaling are established (Sharpe & Pauken 2018).",
        "nodes": [
            ("A", "[T-cell activation: TCR + IFN-γ]", "red"),
            ("B", "[Target cell induces PD-L1]", "yellow"),
            ("C", "[PD-L1 engages PD-1]", "green"),
            ("D", "[/SHP-2 dephosphorylates TCR signaling/]", "green"),
            ("E", "[/Dampens T-cell activation/]", "green"),
            ("F", "(T-cell tolerance / exhaustion)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "A", "⊣ feedback"), ("D", "F", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "The diverse functions of the PD1 inhibitory pathway", "authors": "Sharpe AH, Pauken KE", "journal": "Nature Reviews Immunology", "year": 2018, "volume": "18", "pages": "153-167", "pmid": "28990585", "doi": "10.1038/nri.2017.108"},
        ],
        "keywords": ["PD-1", "PD-L1", "checkpoint", "SHP-2", "negative feedback", "immunotherapy", "Class II", "ground truth"],
        "relatedProcesses": ["human_jak_stat_socs"],
        "notes": "Human Class II inhibitory feedback (immune checkpoint); target of checkpoint-blockade therapy.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "CD274/PD-L1 promoter (IRF1/GAS)", "boundFactor": "IRF1 / STAT1 (IFN-γ)", "operator": "IF", "effect": "IFN-γ-induced PD-L1", "sequenceMotif": "GAS / IRF-E", "note": "links T-cell activity to its own brake"},
            ],
            "derivedLogic": "PD-L1 = IFN-γ ; TCR-signal = NOT PD-1 (negative feedback)",
            "references": ["Sharpe & Pauken 2018"],
        },
    },
    {
        "id": "human_ire1_xbp1_upr",
        "name": "IRE1–XBP1 Unfolded Protein Response",
        "category": "Proteostasis",
        "circuitClass": "II",
        "topologyType": "upr_negative_feedback_homeostat",
        "rationale": "ER stress activates IRE1, which splices XBP1 mRNA to make XBP1s; XBP1s induces chaperones and ERAD that reduce the unfolded-protein load, relieving IRE1 — a negative-feedback proteostasis homeostat. Class II.",
        "description": "The most conserved arm of the unfolded-protein response. Accumulated misfolded proteins activate the ER kinase/endonuclease IRE1, which excises an intron from XBP1 mRNA; the resulting XBP1s transcription factor induces chaperones and ER-associated degradation that restore folding capacity and shut IRE1 back off — negative feedback on ER stress.",
        "scientificAccuracy": "IRE1-mediated XBP1 splicing and the UPR negative-feedback homeostat are established (Walter & Ron 2011).",
        "nodes": [
            ("A", "[ER stress: unfolded proteins]", "red"),
            ("B", "[IRE1 activated]", "green"),
            ("C", "[\\Splices XBP1 mRNA/]", "green"),
            ("D", "[XBP1s transcription factor]", "yellow"),
            ("E", "[Chaperones + ERAD genes]", "green"),
            ("F", "[/Restores folding, lowers stress/]", "green"),
            ("G", "(ER proteostasis restored)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "F", ""), ("F", "A", "⊣ feedback"), ("E", "G", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "The unfolded protein response: from stress pathway to homeostatic regulation", "authors": "Walter P, Ron D", "journal": "Science", "year": 2011, "volume": "334", "pages": "1081-1086", "pmid": "22116877", "doi": "10.1126/science.1209038"},
        ],
        "keywords": ["IRE1", "XBP1", "UPR", "ER stress", "proteostasis", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_hsf1_heat_shock", "human_nrf2_keap1"],
        "notes": "Human Class II proteostasis homeostat (UPR); XBP1s output relieves the stress that triggered it.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "UPRE / ERSE (chaperone, ERAD promoters)", "boundFactor": "XBP1s", "operator": "IF", "effect": "activation of folding/degradation capacity", "sequenceMotif": "TGACGTGG (UPRE)", "note": "output reduces unfolded-protein load -> negative feedback"},
                {"name": "XBP1 mRNA stem-loop", "boundFactor": "IRE1 endonuclease", "operator": "IF (splice)", "effect": "non-canonical splicing to XBP1s", "sequenceMotif": "dual stem-loops (26-nt intron)", "note": "RNA-level activation step"},
            ],
            "derivedLogic": "XBP1s = IRE1(ER-stress) ; chaperones -| ER-stress (negative feedback)",
            "references": ["Walter & Ron 2011"],
        },
    },
    {
        "id": "human_mtor_ulk1_autophagy",
        "name": "mTOR–ULK1 Autophagy Homeostat",
        "category": "Metabolic Signaling",
        "circuitClass": "II",
        "topologyType": "autophagy_negative_feedback_homeostat",
        "rationale": "When nutrients are high, mTORC1 phosphorylates and inhibits ULK1, blocking autophagy; starvation releases ULK1 to drive autophagy, which recycles nutrients and reactivates mTORC1 — a negative-feedback metabolic homeostat. Class II.",
        "description": "Autophagy is governed by a nutrient-sensing feedback loop. Active mTORC1 phosphorylates ULK1 to suppress autophagosome formation; on starvation mTORC1 is inhibited, ULK1 fires, and autophagy degrades cellular material to regenerate nutrients — which reactivates mTORC1, closing a homeostatic negative-feedback loop.",
        "scientificAccuracy": "mTORC1 inhibition of ULK1 and autophagy-mediated nutrient feedback are established (Kim et al. 2011; Rabinowitz & White 2010).",
        "nodes": [
            ("A", "[Nutrient / energy status]", "red"),
            ("B", "{Nutrients high?}", "blue"),
            ("C", "[mTORC1 active]", "yellow"),
            ("D", "[/mTORC1 inhibits ULK1/]", "green"),
            ("E", "[ULK1 active: autophagy]", "green"),
            ("F", "[Autophagy recycles nutrients]", "green"),
            ("G", "[/Restored nutrients reactivate mTORC1/]", "green"),
            ("H", "(Metabolic homeostasis)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", "Yes"), ("C", "D", ""), ("D", "E", "⊣"),
            ("B", "E", "No: starvation"), ("E", "F", ""), ("F", "H", ""),
            ("F", "G", ""), ("G", "C", "+ feedback"),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "AMPK and mTOR regulate autophagy through direct phosphorylation of Ulk1", "authors": "Kim J, Kundu M, Viollet B, Guan KL", "journal": "Nature Cell Biology", "year": 2011, "volume": "13", "pages": "132-141", "pmid": "21258367", "doi": "10.1038/ncb2152"},
        ],
        "keywords": ["mTOR", "ULK1", "autophagy", "nutrient sensing", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_mtorc1_nutrient", "human_akt_foxo_insulin"],
        "notes": "Human Class II autophagy homeostat: mTORC1-ULK1 with nutrient-recycling feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "ULK1 regulation (post-translational)", "boundFactor": "mTORC1 (Ser757)", "operator": "NOT", "effect": "inhibitory phosphorylation of ULK1", "sequenceMotif": "(protein-level)", "note": "autophagy feedback realized in metabolite/phospho state"},
            ],
            "derivedLogic": "autophagy = NOT mTORC1(nutrients) ; autophagy -> nutrients -> mTORC1",
            "references": ["Kim et al. 2011"],
        },
    },
    {
        "id": "human_pten_pi3k_akt",
        "name": "PTEN–PI3K–AKT Tumor-Suppressor Homeostat",
        "category": "Growth Factor Signaling",
        "circuitClass": "II",
        "topologyType": "pten_negative_feedback_homeostat",
        "rationale": "PI3K produces PIP3 to activate AKT; the tumor suppressor PTEN dephosphorylates PIP3, opposing the pathway, and downstream feedback regulates PTEN — a negative-feedback set-point for growth/survival signaling. Class II.",
        "description": "The PI3K-AKT growth/survival axis is held in check by PTEN. Growth-factor-activated PI3K makes PIP3, recruiting and activating AKT; PTEN hydrolyzes PIP3 back to PIP2, directly opposing PI3K. Downstream signaling feeds back on PTEN level/activity, setting a homeostatic balance whose loss (PTEN mutation) drives cancer.",
        "scientificAccuracy": "PTEN antagonism of PI3K-AKT and its tumor-suppressor feedback role are established (Song, Salmena & Pandolfi 2012).",
        "nodes": [
            ("A", "[Growth factor: PI3K active]", "red"),
            ("B", "[PIP3]", "blue"),
            ("C", "[/PTEN dephosphorylates PIP3/]", "green"),
            ("D", "[AKT activated]", "yellow"),
            ("E", "[Survival / growth targets]", "green"),
            ("F", "[/Feedback regulates PTEN/]", "green"),
            ("G", "(Tumor-suppressive set-point)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "D", ""), ("C", "B", "⊣"),
            ("D", "E", ""), ("E", "F", ""), ("F", "C", "+ feedback"), ("D", "G", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "The functions and regulation of the PTEN tumour suppressor", "authors": "Song MS, Salmena L, Pandolfi PP", "journal": "Nature Reviews Molecular Cell Biology", "year": 2012, "volume": "13", "pages": "283-296", "pmid": "22473468", "doi": "10.1038/nrm3330"},
        ],
        "keywords": ["PTEN", "PI3K", "AKT", "PIP3", "tumor suppressor", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_akt_foxo_insulin", "human_mtorc1_nutrient"],
        "notes": "Human Class II homeostat: PTEN opposes PI3K-AKT with downstream feedback on PTEN.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "PTEN regulation (p53/feedback at PTEN promoter)", "boundFactor": "p53 / EGR1 (context)", "operator": "IF", "effect": "induces PTEN to oppose PI3K", "sequenceMotif": "p53 RE in PTEN promoter", "note": "lipid-phosphatase feedback sets the AKT set-point"},
            ],
            "derivedLogic": "AKT = PI3K AND NOT PTEN ; feedback on PTEN -> homeostat",
            "references": ["Song et al. 2012"],
        },
    },
    {
        "id": "human_estrogen_receptor_switch",
        "name": "Estrogen-Receptor Positive-Autoregulation Switch",
        "category": "Hormone Signaling",
        "circuitClass": "III", "circuitSubclass": "IIIa",
        "topologyType": "positive_autoregulation_bistable",
        "rationale": "Estrogen-bound ERα activates the ESR1 gene (positive autoregulation) and proliferative targets; the positive feedback supports a bistable, self-sustaining luminal/ER+ identity — a persistent (IIIa) switch relevant to breast-cancer cell state (Carroll et al. 2006).",
        "description": "In luminal breast epithelium, estrogen-activated ERα binds estrogen-response elements at proliferative target genes and at the ESR1 locus itself, reinforcing its own expression. The positive autoregulation can latch cells into a self-sustaining ER+ state — the molecular logic behind hormone-dependent identity and endocrine-therapy resistance.",
        "scientificAccuracy": "ERα genome-wide target binding and autoregulation of ESR1 are established (Carroll et al. 2006); positive feedback supports bistable interpretation.",
        "nodes": [
            ("A", "[Estrogen]", "red"),
            ("B", "[ERα activated]", "yellow"),
            ("C", "[\\ERα activates ESR1 gene/]", "green"),
            ("D", "[Proliferative ERE target genes]", "green"),
            ("E", "(Bistable ER+ luminal state)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "B", "+"), ("B", "D", ""), ("D", "E", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "Genome-wide analysis of estrogen receptor binding sites", "authors": "Carroll JS, Meyer CA, Song J, et al.", "journal": "Nature Genetics", "year": 2006, "volume": "38", "pages": "1289-1297", "pmid": "17013392", "doi": "10.1038/ng1901"},
        ],
        "keywords": ["estrogen receptor", "ESR1", "positive autoregulation", "bistable", "breast cancer", "Class IIIa", "ground truth"],
        "relatedProcesses": ["synthetic_positive_autoregulation", "human_myod_myogenesis"],
        "notes": "Human Class IIIa hormone-receptor switch via ERα positive autoregulation.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "ERE (incl. ESR1 enhancer)", "boundFactor": "ERα (estrogen-bound)", "operator": "IF / positive feedback", "effect": "activation of targets and own gene", "sequenceMotif": "AGGTCAnnnTGACCT (ERE palindrome)", "note": "autoregulation supports bistable ER+ state"},
            ],
            "derivedLogic": "ERα = IF estrogen AND ERα(t-τ) (positive feedback) -> latched ER+ state",
            "references": ["Carroll et al. 2006"],
        },
    },
    {
        "id": "human_calcium_oscillator",
        "name": "IP3/Ca²⁺ Oscillator (CICR)",
        "category": "Calcium Signaling",
        "circuitClass": "IV",
        "topologyType": "cicr_pos_neg_feedback_oscillator",
        "rationale": "IP3 opens IP3 receptors to release Ca²⁺; cytosolic Ca²⁺ both potentiates further release (CICR positive feedback) and, at higher levels with a delay, inhibits the receptor and is pumped back — the combination produces Ca²⁺ oscillations whose frequency is decoded by NFAT. Class IV.",
        "description": "Calcium signaling is encoded in oscillation frequency. Receptor-generated IP3 opens IP3 receptors to release ER Ca²⁺; released Ca²⁺ first amplifies its own release (calcium-induced calcium release) then, with delay, inactivates the receptor while pumps refill the store. The coupled fast-positive / slow-negative feedback gives repetitive Ca²⁺ spikes that transcription factors such as NFAT decode.",
        "scientificAccuracy": "CICR-based Ca²⁺ oscillations and frequency decoding are established (Berridge, Lipp & Bootman 2000; Dolmetsch et al. 1998).",
        "nodes": [
            ("A", "[Receptor: IP3 produced]", "red"),
            ("B", "[IP3R releases Ca²⁺]", "green"),
            ("C", "[\\Ca²⁺ amplifies release CICR/]", "green"),
            ("D", "[Cytosolic Ca²⁺ rise]", "blue"),
            ("E", "[/Ca²⁺ inactivates IP3R + pump uptake/]", "green"),
            ("F", "(Ca²⁺ oscillations; NFAT decoding)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "C", "+"),
            ("D", "E", ""), ("E", "B", "⊣ delayed"), ("D", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "The versatility and universality of calcium signalling", "authors": "Berridge MJ, Lipp P, Bootman MD", "journal": "Nature Reviews Molecular Cell Biology", "year": 2000, "volume": "1", "pages": "11-21", "pmid": "11413485", "doi": "10.1038/35036035"},
        ],
        "keywords": ["calcium", "IP3", "CICR", "oscillator", "NFAT", "frequency decoding", "Class IV", "ground truth"],
        "relatedProcesses": ["human_hes1_oscillator", "synthetic_metabolator"],
        "notes": "Human Class IV oscillator: fast CICR positive feedback + delayed negative feedback on the IP3 receptor.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "IP3R Ca²⁺ regulation (channel-level)", "boundFactor": "Ca²⁺ (biphasic on IP3R)", "operator": "positive then delayed NOT", "effect": "fast activation, slow inactivation", "sequenceMotif": "(channel-level, not cis-DNA)", "note": "frequency read out downstream by NFAT at NFAT sites GGAAA"},
            ],
            "derivedLogic": "Ca²⁺ = +CICR AND delayed NOT(IP3R) -> oscillation; NFAT decodes frequency",
            "references": ["Berridge et al. 2000"],
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
    print(f"Wrote {len(rows)} human Batch-6 process files -> {OUT_DIR}\n")
    print(f"{'id':<40} {'cls':<4} {'sub':<5} {'nodes':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<40} {r[1]:<4} {r[2]:<5} {r[3]:<6} {r[4]:<6} {r[5]}")


if __name__ == "__main__":
    main()
