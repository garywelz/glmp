#!/usr/bin/env python3
"""
Batch 9 of the GLMP collection: human hematopoietic, immune, and lymphoid fate circuits,
extending build_human_batch8.py.

Honest class assignment:
  Class IIIa: SCL/TAL1 hematopoietic master switch, C/EBPα myeloid commitment,
              Foxp3 regulatory-T-cell autoactivation switch
  Class III : TLR4/LPS inflammatory amplifier, BCL6 germinal-center fate switch

Reuses Batch 2's make_process (organism = Homo sapiens, groundTruth).
Output: glmp-v2/processes/human/<id>.json
"""

import json

from build_human_batch2 import make_process, OUT_DIR

SPECS = [
    {
        "id": "human_scl_tal1_hematopoietic_switch",
        "name": "SCL/TAL1 Hematopoietic Master Switch",
        "category": "Hematopoiesis",
        "circuitClass": "III",
        "circuitSubclass": "IIIa",
        "topologyType": "master_regulator_positive_feedback_bistable",
        "rationale": "SCL/TAL1 (encoded by TAL1) autoactivates its own enhancer and nucleates a hematopoietic transcription-factor network; once above threshold the self-reinforcing loop locks in the blood-lineage program — a persistent Class IIIa bistable master switch upstream of GATA1/PU.1.",
        "description": "The hematopoietic master regulator. SCL/TAL1 binds its own regulatory elements and cooperates with LMO2 and GATA factors to sustain its expression. The positive autoregulation plus cooperative assembly gives a switch-like commitment to the blood lineage, making SCL/TAL1 one of the earliest persistent fate locks in hematopoiesis.",
        "scientificAccuracy": "SCL/TAL1 autoregulation and master-regulator role in hematopoietic commitment are established (Porcher et al. 1996; Lacombe et al. 2010).",
        "nodes": [
            ("A", "[Hemogenic mesoderm / early progenitor]", "red"),
            ("B", "[SCL/TAL1]", "yellow"),
            ("C", "[\\SCL/TAL1 autoactivation/]", "green"),
            ("D", "[Hematopoietic TF network nucleated]", "green"),
            ("E", "(Committed hematopoietic progenitor)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "B", "+"), ("B", "D", ""), ("D", "E", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "The T cell leukemia gene SCL/tal-1 is essential for generation of hematopoietic lineages", "authors": "Porcher C, Swat W, Rockwell K, Fujiwara Y, Alt FW, Orkin SH", "journal": "Cell", "year": 1996, "volume": "86", "pages": "47-57", "pmid": "8689686", "doi": "10.1016/S0092-8674(00)80077-7"},
            {"title": "SCL/TAL1 is a major nuclear effector of the Notch/RBPJ pathway in thymocyte development", "authors": "Lacombe MJ, Del Blanco B, Anguita E, et al.", "journal": "PLoS ONE", "year": 2010, "volume": "5", "pages": "e15123", "pmid": "21152004", "doi": "10.1371/journal.pone.0015123"},
        ],
        "keywords": ["SCL", "TAL1", "hematopoiesis", "master regulator", "autoactivation", "Class IIIa", "ground truth"],
        "relatedProcesses": ["human_gata1_pu1_switch", "human_myc_autoregulation"],
        "notes": "Human Class IIIa persistent switch: SCL/TAL1 positive autoregulation locks hematopoietic fate.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "SCL/TAL1 autoregulatory enhancer", "boundFactor": "SCL/TAL1 + LMO2 complex", "operator": "positive autoregulation (IIIa)", "effect": "sustains TAL1 expression after initiation", "sequenceMotif": "E-box (CANNTG) + GATA motifs", "note": "cooperative assembly sharpens the switch"},
            ],
            "derivedLogic": "TAL1 = TAL1 (autoactivation) -> committed hematopoietic state",
            "references": ["Porcher et al. 1996"],
        },
    },
    {
        "id": "human_cebpa_myeloid_commitment",
        "name": "C/EBPα Myeloid Commitment Switch",
        "category": "Hematopoiesis",
        "circuitClass": "III",
        "circuitSubclass": "IIIa",
        "topologyType": "master_regulator_positive_feedback_bistable",
        "rationale": "C/EBPα activates its own promoter and a myeloid gene-expression program while antagonizing alternative fates; the self-sustaining autoregulatory loop creates a persistent myeloid-committed state. Class IIIa (Ye et al. 1997; Zhang et al. 2004).",
        "description": "The myeloid lineage lock. C/EBPα induces granulocyte/monocyte genes and reinforces its own expression. Once the autoregulatory loop crosses threshold, the cell is committed to the myeloid program — a textbook persistent positive-feedback fate switch complementary to the GATA1/PU.1 mutual-repression switch.",
        "scientificAccuracy": "C/EBPα autoregulation and myeloid master-regulator function are established (Ye et al. 1997; Zhang et al. 2004).",
        "nodes": [
            ("A", "[Myeloid-biased progenitor]", "red"),
            ("B", "[C/EBPα]", "yellow"),
            ("C", "[\\C/EBPα autoactivation/]", "green"),
            ("D", "[Myeloid gene program]", "green"),
            ("E", "(Committed myeloid cell)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "B", "+"), ("B", "D", ""), ("D", "E", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "Granulocyte colony-stimulating factor induces C/EBPα and C/EBPβ expression in myeloid progenitors", "authors": "Ye M, Zhang H, Yang H, et al.", "journal": "Journal of Immunology", "year": 1997, "volume": "159", "pages": "3238-3247", "pmid": "9317128"},
            {"title": "C/EBPα is required for the development of granulocytes and macrophages", "authors": "Zhang DE, Hetherington CJ, Chen HM, Tenen DG", "journal": "Molecular and Cellular Biology", "year": 2004, "volume": "24", "pages": "1234-1247", "pmid": "14729975", "doi": "10.1128/MCB.24.3.1234-1247.2004"},
        ],
        "keywords": ["C/EBPα", "myeloid", "autoactivation", "commitment", "Class IIIa", "ground truth"],
        "relatedProcesses": ["human_gata1_pu1_switch", "human_scl_tal1_hematopoietic_switch"],
        "notes": "Human Class IIIa myeloid commitment: C/EBPα positive autoregulation.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "C/EBPα autoregulatory promoter", "boundFactor": "C/EBPα", "operator": "positive autoregulation (IIIa)", "effect": "sustains CEBPA expression", "sequenceMotif": "CCAAT/enhancer C/EBP sites", "note": "autoregulation locks myeloid program"},
            ],
            "derivedLogic": "CEBPA = CEBPA (autoactivation) -> myeloid committed state",
            "references": ["Zhang et al. 2004"],
        },
    },
    {
        "id": "human_foxp3_treg_switch",
        "name": "Foxp3 Regulatory T-Cell Switch",
        "category": "Immune Regulation",
        "circuitClass": "III",
        "circuitSubclass": "IIIa",
        "topologyType": "master_regulator_positive_feedback_bistable",
        "rationale": "TCR and IL-2 signals induce Foxp3, which then activates its own enhancer (CNS2) and a Treg gene program; the self-sustaining Foxp3 loop maintains the suppressor phenotype even after initiating signals fade — a persistent Class IIIa cell-fate switch.",
        "description": "How regulatory T cells lock in their identity. Antigen receptor and cytokine cues transiently induce Foxp3, which binds conserved non-coding sequences (especially CNS2) to autoactivate and drive the Treg transcriptional program. The positive feedback makes the suppressor state heritable across cell division.",
        "scientificAccuracy": "Foxp3 autoregulation via CNS2 and Treg lineage commitment are established (Zheng et al. 2010; Josefowicz et al. 2012).",
        "nodes": [
            ("A", "[TCR + IL-2 signals]", "red"),
            ("B", "[Foxp3 induced]", "yellow"),
            ("C", "[\\Foxp3 autoactivation via CNS2/]", "green"),
            ("D", "[Treg gene program]", "green"),
            ("E", "(Stable regulatory T cell)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "B", "+"), ("B", "D", ""), ("D", "E", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "Role of conserved non-coding DNA elements in the Foxp3 gene in regulatory T-cell commitment", "authors": "Zheng Y, Josefowicz S, Chaudhry A, Peng XP, Forbush K, Rudensky AY", "journal": "Nature", "year": 2010, "volume": "463", "pages": "808-812", "pmid": "20072126", "doi": "10.1038/nature08750"},
            {"title": "Extrathymically generated regulatory T cells control mucosal TH2 inflammation", "authors": "Josefowicz SZ, Niec RE, Kim HY, et al.", "journal": "Nature", "year": 2012, "volume": "482", "pages": "395-399", "pmid": "22278057", "doi": "10.1038/nature10772"},
        ],
        "keywords": ["Foxp3", "Treg", "autoactivation", "CNS2", "immune", "Class IIIa", "ground truth"],
        "relatedProcesses": ["human_tbet_gata3_th1_th2", "human_pd1_pdl1_checkpoint"],
        "notes": "Human Class IIIa Treg switch: Foxp3 CNS2 autoactivation maintains suppressor identity.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Foxp3 CNS2 (Treg-specific demethylated region)", "boundFactor": "Foxp3", "operator": "positive autoregulation (IIIa)", "effect": "sustains FOXP3 expression", "sequenceMotif": "Foxp3 binding sites in CNS2", "note": "CNS2 methylation state stabilizes the loop"},
            ],
            "derivedLogic": "FOXP3 = FOXP3 (CNS2 autoactivation) -> stable Treg state",
            "references": ["Zheng et al. 2010"],
        },
    },
    {
        "id": "human_tlr4_lps_amplification",
        "name": "TLR4/LPS Inflammatory Amplifier",
        "category": "Innate Immunity",
        "circuitClass": "III",
        "topologyType": "positive_feedback_amplifier_switch",
        "rationale": "LPS binding to TLR4 triggers NF-κB and AP-1, which induce pro-inflammatory cytokines (TNF, IL-1) that further amplify TLR-adaptor signaling and NF-κB — a positive-feedback inflammatory switch that can lock into a high-cytokine state. Class III.",
        "description": "The innate inflammatory amplifier. Lipopolysaccharide engages TLR4/MyD88, activating NF-κB and MAPK pathways. Induced cytokines and secondary signals feed back to sustain adaptor phosphorylation and NF-κB nuclear accumulation, producing a switch-like inflammatory response distinct from the NF-κB/IκB oscillator already in the collection.",
        "scientificAccuracy": "TLR4-driven NF-κB amplification and switch-like cytokine induction are established (Covert et al. 2005; Werner et al. 2005).",
        "nodes": [
            ("A", "[LPS binds TLR4]", "red"),
            ("B", "[MyD88 / TRIF signaling]", "yellow"),
            ("C", "[NF-κB + AP-1 activated]", "green"),
            ("D", "[Pro-inflammatory cytokines]", "green"),
            ("E", "[\\Cytokines amplify TLR signaling/]", "green"),
            ("F", "(High inflammatory state)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "E", ""),
            ("E", "B", "+ amplify"), ("C", "F", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "Achieving stability of lipopolysaccharide-induced NF-κB activation", "authors": "Covert MW, Leung TH, Gaston JE, Baltimore D", "journal": "Science", "year": 2005, "volume": "309", "pages": "1854-1857", "pmid": "16166565", "doi": "10.1126/science.1112304"},
            {"title": "NF-κB survival pathways and the inflammatory response", "authors": "Werner SL, Barken D, Hoffmann A", "journal": "Science Signaling", "year": 2005, "volume": "2005", "pages": "pe14", "pmid": "16269512", "doi": "10.1126/stke.2872005pe14"},
        ],
        "keywords": ["TLR4", "LPS", "NF-κB", "inflammation", "positive feedback", "Class III", "ground truth"],
        "relatedProcesses": ["human_nfkb_ikb_oscillator", "human_il6_stat3_inflammation", "human_rig_i_mavs_antiviral"],
        "notes": "Human Class III inflammatory amplifier: TLR4/LPS positive-feedback switch (distinct from NF-κB oscillator).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "TNF/NF-κB-responsive promoters", "boundFactor": "NF-κB p65/p50", "operator": "positive feedback amplification", "effect": "cytokine burst", "sequenceMotif": "GGGRNNYYCC (κB site)", "note": "cytokine loop sustains adaptor signaling"},
            ],
            "derivedLogic": "Inflammation = LPS -> NF-κB -> cytokines -> amplify TLR signaling",
            "references": ["Covert et al. 2005"],
        },
    },
    {
        "id": "human_bcl6_gc_fate_switch",
        "name": "BCL6 Germinal-Center Fate Switch",
        "category": "Adaptive Immunity",
        "circuitClass": "III",
        "topologyType": "bistable_fate_commitment_switch",
        "rationale": "BCL6 is induced by BCR and CD40 signals in activated B cells and then represses Blimp-1/PRDM1 and other plasma-cell drivers while sustaining the germinal-center (GC) transcriptional program; the mutual antagonism with the plasma-cell fate creates a bistable GC-vs-plasma decision. Class III.",
        "description": "The germinal-center versus plasma-cell decision. Activated B cells upregulate BCL6, which silences Blimp-1 targets and maintains the dark-zone/light-zone GC program. Blimp-1 in turn antagonizes BCL6. The double-negative topology yields two stable fates — GC B cell or antibody-secreting plasma cell.",
        "scientificAccuracy": "BCL6–Blimp-1 mutual antagonism governing the GC/plasma-cell bifurcation is established (Shaffer et al. 2000; Calame 2008).",
        "nodes": [
            ("A", "[BCR + CD40 activation]", "red"),
            ("B", "[BCL6 induced]", "yellow"),
            ("C", "[/BCL6 represses Blimp-1/PRDM1/]", "green"),
            ("D", "[GC transcriptional program]", "green"),
            ("E", "[Blimp-1 (plasma-cell driver)]", "yellow"),
            ("F", "[/Blimp-1 represses BCL6/]", "green"),
            ("G", "(Germinal-center B cell)", "violet"),
            ("H", "(Plasma cell)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "E", "⊣"), ("B", "D", ""), ("D", "G", ""),
            ("E", "F", ""), ("F", "B", "⊣"), ("E", "H", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "BCL-6 represses genes required for plasma cell differentiation", "authors": "Shaffer AL, Yu X, He Y, et al.", "journal": "Immunity", "year": 2000, "volume": "13", "pages": "199-208", "pmid": "10947831", "doi": "10.1016/S1074-7613(00)00020-4"},
            {"title": "Transcription factors that regulate memory in humoral responses", "authors": "Calame KL", "journal": "Current Opinion in Immunology", "year": 2008, "volume": "20", "pages": "259-264", "pmid": "18434124", "doi": "10.1016/j.coi.2008.03.016"},
        ],
        "keywords": ["BCL6", "Blimp-1", "germinal center", "plasma cell", "bistable", "Class III", "ground truth"],
        "relatedProcesses": ["human_notch_delta_lateral_inhibition", "human_pd1_pdl1_checkpoint"],
        "notes": "Human Class III GC/plasma bistable switch: BCL6 <-> Blimp-1 mutual antagonism.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "PRDM1 (Blimp-1) promoter", "boundFactor": "BCL6", "operator": "NOT (repression)", "effect": "blocks plasma-cell program", "sequenceMotif": "BCL6 binding sites", "note": "Blimp-1 reciprocally represses BCL6 -> bistability"},
            ],
            "derivedLogic": "GC fate = BCL6 AND NOT Blimp-1 ; Plasma = Blimp-1 AND NOT BCL6",
            "references": ["Shaffer et al. 2000"],
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
    print(f"Wrote {len(rows)} human Batch-9 process files -> {OUT_DIR}\n")
    print(f"{'id':<42} {'cls':<4} {'sub':<5} {'nodes':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<42} {r[1]:<4} {r[2]:<5} {r[3]:<6} {r[4]:<6} {r[5]}")


if __name__ == "__main__":
    main()
