#!/usr/bin/env python3
"""
Batch 5 of the GLMP collection: human developmental / disease circuits, extending
build_human_batch4.py. Emphasis on EMT bistable switches (cancer-relevant IIIa),
morphogen signaling, and a delayed-feedback ultradian oscillator.

Honest class assignment:
  Class IIIa : EMT ZEB/miR-200 double-negative bistable switch
  Class III  : SNAIL/miR-34 EMT switch
  Class IV   : HES1 delayed negative-autoregulation oscillator
  Class II   : SHH-GLI (PTCH1 feedback), NRF2-KEAP1, HSF1 heat-shock

Reuses Batch 2's make_process (organism = Homo sapiens, groundTruth).
Output: glmp-v2/processes/human/<id>.json
"""

import json

from build_human_batch2 import make_process, OUT_DIR

SPECS = [
    {
        "id": "human_emt_zeb_mir200",
        "name": "EMT ZEB/miR-200 Bistable Switch",
        "category": "EMT / Cancer",
        "circuitClass": "III", "circuitSubclass": "IIIa",
        "topologyType": "double_negative_feedback_bistable",
        "rationale": "ZEB1/2 and the miR-200 family repress each other; the double-negative loop is bistable, latching cells into either an epithelial (high miR-200) or mesenchymal (high ZEB) state — a persistent (IIIa) switch central to metastasis (Lu et al. 2013; Tian et al. 2013).",
        "description": "The core EMT decision circuit. ZEB1/2 transcription factors and the miR-200 microRNA family mutually repress each other, while ZEB also represses E-cadherin. The double-negative feedback is bistable (with a hybrid intermediate), locking cells into epithelial or mesenchymal identity — the switch that drives metastatic plasticity.",
        "scientificAccuracy": "ZEB/miR-200 mutual repression and its bistable EMT interpretation are established (Burk et al. 2008; Lu et al. 2013; Tian et al. 2013).",
        "nodes": [
            ("A", "[EMT signal: TGF-β / hypoxia]", "red"),
            ("B", "[ZEB1/2]", "yellow"),
            ("C", "[miR-200 family]", "yellow"),
            ("D", "[/ZEB represses miR-200/]", "green"),
            ("E", "[/miR-200 represses ZEB/]", "green"),
            ("F", "[/ZEB represses E-cadherin/]", "green"),
            ("G", "(Mesenchymal state: migratory)", "violet"),
            ("H", "(Epithelial state: E-cadherin+)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "D", ""), ("D", "C", "⊣"),
            ("C", "E", ""), ("E", "B", "⊣"),
            ("B", "F", ""), ("F", "G", ""), ("C", "H", ""),
        ],
        "gates": (0, 0, 3),
        "sources": [
            {"title": "MicroRNA-based regulation of epithelial-hybrid-mesenchymal fate determination", "authors": "Lu M, Jolly MK, Levine H, Onuchic JN, Ben-Jacob E", "journal": "PNAS", "year": 2013, "volume": "110", "pages": "18144-18149", "pmid": "24154725", "doi": "10.1073/pnas.1318192110"},
            {"title": "Coupled reversible and irreversible bistable switches underlying TGF-β-induced EMT", "authors": "Tian XJ, Zhang H, Xing J", "journal": "Biophysical Journal", "year": 2013, "volume": "105", "pages": "1079-1089", "pmid": "23972859", "doi": "10.1016/j.bpj.2013.07.011"},
        ],
        "keywords": ["EMT", "ZEB", "miR-200", "bistable", "double-negative feedback", "metastasis", "Class IIIa", "ground truth"],
        "relatedProcesses": ["human_snail_mir34_emt", "synthetic_toggle_switch"],
        "notes": "Human Class IIIa EMT switch: ZEB/miR-200 double-negative bistability (3 repressions).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "ZEB E-box (CDH1, miR-200 promoters)", "boundFactor": "ZEB1/2", "operator": "NOT", "effect": "repression of miR-200 and E-cadherin", "sequenceMotif": "CACCTG (Z-box)", "note": "ZEB binds Z-box E-boxes"},
                {"name": "miR-200 target sites in ZEB 3'UTR", "boundFactor": "miR-200", "operator": "NOT", "effect": "post-transcriptional repression of ZEB", "sequenceMotif": "CAGUGUU (miR-200 seed match)", "note": "closes the double-negative loop"},
            ],
            "derivedLogic": "ZEB = NOT miR-200 ; miR-200 = NOT ZEB -> bistable epithelial/mesenchymal",
            "references": ["Lu et al. 2013"],
        },
    },
    {
        "id": "human_snail_mir34_emt",
        "name": "SNAIL/miR-34 EMT Switch",
        "category": "EMT / Cancer",
        "circuitClass": "III",
        "topologyType": "double_negative_feedback_bistable",
        "rationale": "SNAIL and miR-34 repress each other (and SNAIL represses E-cadherin); the double-negative loop is bistable and, coupled to ZEB/miR-200, forms the cascade of switches that times EMT (Siemens et al. 2011). Class III.",
        "description": "A second, upstream EMT switch. SNAIL represses miR-34, and miR-34 (a p53 target) represses SNAIL; SNAIL also represses E-cadherin to drive the mesenchymal program. The double-negative feedback is bistable and feeds the ZEB/miR-200 switch, giving EMT its staged, hysteretic dynamics.",
        "scientificAccuracy": "SNAIL/miR-34 double-negative feedback and its EMT-switch role are established (Siemens et al. 2011; Kim et al. 2011).",
        "nodes": [
            ("A", "[EMT trigger: TGF-β / p53 loss]", "red"),
            ("B", "[SNAIL]", "yellow"),
            ("C", "[miR-34]", "yellow"),
            ("D", "[/SNAIL represses miR-34/]", "green"),
            ("E", "[/miR-34 represses SNAIL/]", "green"),
            ("F", "[/SNAIL represses E-cadherin/]", "green"),
            ("G", "(EMT commitment)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "D", ""), ("D", "C", "⊣"),
            ("C", "E", ""), ("E", "B", "⊣"),
            ("B", "F", ""), ("F", "G", ""), ("B", "G", ""),
        ],
        "gates": (0, 0, 3),
        "sources": [
            {"title": "miR-34 and SNAIL form a double-negative feedback loop to regulate epithelial-mesenchymal transition", "authors": "Siemens H, Jackstadt R, Hünten S, et al.", "journal": "Cell Cycle", "year": 2011, "volume": "10", "pages": "4256-4271", "pmid": "22134354", "doi": "10.4161/cc.10.24.18552"},
        ],
        "keywords": ["EMT", "SNAIL", "miR-34", "p53", "bistable", "double-negative feedback", "Class III", "ground truth"],
        "relatedProcesses": ["human_emt_zeb_mir200", "human_p53_mdm2"],
        "notes": "Human Class III EMT switch (SNAIL/miR-34 double-negative); upstream partner of ZEB/miR-200.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "SNAIL E-box (CDH1, miR-34 promoters)", "boundFactor": "SNAIL", "operator": "NOT", "effect": "repression", "sequenceMotif": "CAGGTG (E-box)", "note": ""},
                {"name": "miR-34 site in SNAIL 3'UTR", "boundFactor": "miR-34", "operator": "NOT", "effect": "post-transcriptional repression", "sequenceMotif": "(miR-34 seed match)", "note": "p53 induces miR-34"},
            ],
            "derivedLogic": "SNAIL = NOT miR-34 ; miR-34 = NOT SNAIL -> bistable EMT",
            "references": ["Siemens et al. 2011"],
        },
    },
    {
        "id": "human_hes1_oscillator",
        "name": "HES1 Ultradian Oscillator",
        "category": "Developmental Signaling",
        "circuitClass": "IV",
        "topologyType": "delayed_negative_autoregulation_oscillator",
        "rationale": "HES1 represses its own promoter; transcription/translation delay turns this single negative-autoregulation loop into a ~2 h ultradian oscillator (Hirata et al. 2002) that times somite segmentation and neural progenitor dynamics. Class IV.",
        "description": "HES1, a bHLH repressor downstream of Notch, binds and represses its own promoter. The delay between transcription, translation, and protein turnover converts this negative-autoregulation loop into a ~2 hour ultradian oscillator that paces the segmentation clock and neural-progenitor cell-fate timing.",
        "scientificAccuracy": "HES1 delayed negative-autoregulation oscillations are directly measured (Hirata et al. 2002; Lewis 2003).",
        "nodes": [
            ("A", "[Notch / signaling input]", "red"),
            ("B", "[HES1 transcription]", "green"),
            ("C", "[HES1 protein]", "yellow"),
            ("D", "[/HES1 represses own promoter/]", "green"),
            ("E", "(~2 h ultradian oscillation)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "B", "⊣ delayed"), ("C", "E", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Oscillatory expression of the bHLH factor Hes1 regulated by a negative feedback loop", "authors": "Hirata H, Yoshiura S, Ohtsuka T, et al.", "journal": "Science", "year": 2002, "volume": "298", "pages": "840-843", "pmid": "12399594", "doi": "10.1126/science.1074560"},
        ],
        "keywords": ["HES1", "oscillator", "negative autoregulation", "segmentation clock", "delay", "Class IV", "ground truth"],
        "relatedProcesses": ["human_circadian_clock", "synthetic_negative_autoregulation"],
        "notes": "Human Class IV oscillator: single delayed negative-autoregulation loop (the human analogue of synthetic NAR pushed into oscillation by delay).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "HES1 promoter N-box", "boundFactor": "HES1", "operator": "NOT", "effect": "autorepression", "sequenceMotif": "CACNAG (N-box)", "note": "HES1 represses its own promoter with delay"},
            ],
            "derivedLogic": "HES1 = NOT HES1(t-τ) -> ~2 h oscillation",
            "references": ["Hirata et al. 2002"],
        },
    },
    {
        "id": "human_shh_gli",
        "name": "Sonic Hedgehog–GLI Morphogen Pathway",
        "category": "Developmental Signaling",
        "circuitClass": "II",
        "topologyType": "ptch1_negative_feedback_morphogen",
        "rationale": "SHH relieves PTCH1 inhibition of SMO, activating GLI; GLI induces PTCH1, which re-inhibits the pathway — a negative-feedback loop shaping the morphogen response. Class II (with a GLI activator/repressor gradient readout).",
        "description": "Hedgehog signaling patterns tissues as a morphogen. Without SHH, PTCH1 inhibits SMO and GLI is processed to a repressor; SHH binding PTCH1 releases SMO, so GLI activator drives targets including PTCH1 itself — a negative-feedback loop that sharpens and limits the graded response.",
        "scientificAccuracy": "PTCH1-mediated negative feedback and GLI activator/repressor gradients are established (Briscoe & Thérond 2013).",
        "nodes": [
            ("A", "[Sonic hedgehog ligand]", "red"),
            ("B", "{SHH present?}", "blue"),
            ("C", "[PTCH1 inhibits SMO]", "green"),
            ("D", "[GLI3 repressor form]", "yellow"),
            ("E", "[SMO active]", "green"),
            ("F", "[GLI activator]", "yellow"),
            ("G", "[Targets: GLI1, PTCH1]", "green"),
            ("H", "[/PTCH1 feedback inhibits SMO/]", "green"),
            ("I", "(Morphogen-graded output)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", "No"), ("C", "D", ""),
            ("B", "E", "Yes"), ("E", "F", ""), ("F", "G", ""),
            ("G", "I", ""), ("G", "H", ""), ("H", "E", "⊣ feedback"),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "The mechanisms of Hedgehog signalling and its roles in development and disease", "authors": "Briscoe J, Thérond PP", "journal": "Nature Reviews Molecular Cell Biology", "year": 2013, "volume": "14", "pages": "416-429", "pmid": "23719536", "doi": "10.1038/nrm3598"},
        ],
        "keywords": ["Sonic hedgehog", "GLI", "PTCH1", "SMO", "morphogen", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_wnt_beta_catenin"],
        "notes": "Human Class II morphogen pathway with PTCH1 negative feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "GLI binding site (incl. PTCH1 promoter)", "boundFactor": "GLI activator/repressor", "operator": "IF / NOT", "effect": "graded activation; induces PTCH1", "sequenceMotif": "GACCACCCA", "note": "PTCH1 induction closes negative feedback"},
            ],
            "derivedLogic": "GLI-targets = SHH(-|PTCH1->SMO) ; PTCH1 = GLI-target -| pathway",
            "references": ["Briscoe & Thérond 2013"],
        },
    },
    {
        "id": "human_nrf2_keap1",
        "name": "NRF2–KEAP1 Oxidative-Stress Homeostat",
        "category": "Stress Response",
        "circuitClass": "II",
        "topologyType": "keap1_negative_feedback_homeostat",
        "rationale": "Under basal conditions KEAP1 targets NRF2 for degradation; oxidative/electrophilic stress modifies KEAP1 to stabilize NRF2, which drives antioxidant (ARE) genes and feedback regulators — a negative-feedback redox homeostat. Class II.",
        "description": "The master antioxidant response. KEAP1 normally ubiquitinates NRF2 for degradation; reactive electrophiles modify KEAP1 cysteines, stabilizing NRF2, which enters the nucleus and activates ARE-driven antioxidant and detoxification genes, including feedback regulators that restore the redox set-point.",
        "scientificAccuracy": "KEAP1-NRF2 stress sensing and ARE-driven negative feedback are established (Itoh et al. 1999; Suzuki & Yamamoto 2015).",
        "nodes": [
            ("A", "[Oxidative / electrophilic stress]", "red"),
            ("B", "{Stress present?}", "blue"),
            ("C", "[KEAP1 active]", "green"),
            ("D", "[/NRF2 degraded/]", "green"),
            ("E", "[NRF2 stabilized]", "yellow"),
            ("F", "[ARE targets: antioxidants]", "green"),
            ("G", "[/Feedback regulators/]", "green"),
            ("H", "(Redox homeostasis)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", "No"), ("C", "D", ""),
            ("B", "E", "Yes"), ("E", "F", ""), ("F", "H", ""),
            ("F", "G", ""), ("G", "C", "+ feedback"),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Keap1 represses nuclear activation of antioxidant responsive elements by Nrf2 through binding to the amino-terminal Neh2 domain", "authors": "Itoh K, Wakabayashi N, Katoh Y, et al.", "journal": "Genes & Development", "year": 1999, "volume": "13", "pages": "76-86", "pmid": "9887101", "doi": "10.1101/gad.13.1.76"},
        ],
        "keywords": ["NRF2", "KEAP1", "ARE", "oxidative stress", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_vhl_hif_oxygen_sensing"],
        "notes": "Human Class II redox homeostat: KEAP1-NRF2 with ARE-driven feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "ARE (antioxidant response element)", "boundFactor": "NRF2-sMAF", "operator": "IF / NOT(KEAP1)", "effect": "activation when NRF2 stabilized", "sequenceMotif": "TGACnnnGC", "note": "KEAP1 gates NRF2 stability"},
            ],
            "derivedLogic": "ARE-targets = NOT(basal KEAP1) ; feedback regulators -> homeostat",
            "references": ["Itoh et al. 1999"],
        },
    },
    {
        "id": "human_hsf1_heat_shock",
        "name": "HSF1 Heat-Shock Response with HSP70 Feedback",
        "category": "Stress Response",
        "circuitClass": "II",
        "topologyType": "hsp70_negative_feedback_homeostat",
        "rationale": "Proteotoxic stress frees and trimerizes HSF1, which induces chaperones (HSP70/90); accumulated HSP70 binds and inactivates HSF1 — a negative-feedback proteostasis homeostat. Class II.",
        "description": "The cytoprotective heat-shock response. Misfolded proteins titrate chaperones away from HSF1, allowing HSF1 to trimerize and induce HSP70/HSP90. As chaperones refold the proteome, free HSP70 rebinds and inactivates HSF1 — a negative-feedback loop that scales the response to the folding load.",
        "scientificAccuracy": "HSF1 activation and HSP70-mediated negative feedback are established (Anckar & Sistonen 2011).",
        "nodes": [
            ("A", "[Heat / proteotoxic stress]", "red"),
            ("B", "[HSF1 trimerizes, active]", "yellow"),
            ("C", "[Chaperone transcription: HSP70/90]", "green"),
            ("D", "[Chaperones refold proteins]", "green"),
            ("E", "[/HSP70 binds, inactivates HSF1/]", "green"),
            ("F", "(Proteostasis restored)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "B", "⊣ feedback"), ("D", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Regulation of the heat shock response in eukaryotes", "authors": "Anckar J, Sistonen L", "journal": "Annual Review of Biochemistry", "year": 2011, "volume": "80", "pages": "1089-1115", "pmid": "21417720", "doi": "10.1146/annurev-biochem-060809-095203"},
        ],
        "keywords": ["HSF1", "HSP70", "heat shock", "proteostasis", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_nrf2_keap1"],
        "notes": "Human Class II proteostasis homeostat: HSP70 negative feedback on HSF1.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Heat-shock element (HSE)", "boundFactor": "HSF1 trimer", "operator": "IF", "effect": "activation of chaperones", "sequenceMotif": "nGAAn-nTTCn-nGAAn (inverted repeats)", "note": "HSP70 product feeds back to inactivate HSF1"},
            ],
            "derivedLogic": "chaperones = HSF1 ; HSF1 = NOT HSP70 (negative feedback) -> proteostasis",
            "references": ["Anckar & Sistonen 2011"],
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
    print(f"Wrote {len(rows)} human Batch-5 process files -> {OUT_DIR}\n")
    print(f"{'id':<40} {'cls':<4} {'sub':<5} {'nodes':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<40} {r[1]:<4} {r[2]:<5} {r[3]:<6} {r[4]:<6} {r[5]}")


if __name__ == "__main__":
    main()
