#!/usr/bin/env python3
"""
Batch 7 of the GLMP collection: human signaling / disease circuits, extending
build_human_batch6.py. Energy and stress homeostats, a decision switch, an
inflammatory positive-feedback bistable, and an iron homeostat.

Honest class assignment:
  Class II  : AMPK energy homeostat, iron IRP/IRE homeostat, cAMP/PKA GPCR
              desensitization, glucocorticoid HPA-axis feedback
  Class III : p53 arrest-vs-apoptosis decision switch
  Class IIIa: IL-6/STAT3 inflammatory positive-feedback bistable

Reuses Batch 2's make_process (organism = Homo sapiens, groundTruth).
Output: glmp-v2/processes/human/<id>.json
"""

import json

from build_human_batch2 import make_process, OUT_DIR

SPECS = [
    {
        "id": "human_ampk_energy_homeostat",
        "name": "AMPK Energy-Charge Homeostat",
        "category": "Metabolic Signaling",
        "circuitClass": "II",
        "topologyType": "energy_negative_feedback_homeostat",
        "rationale": "Rising AMP/ADP (low energy) activates AMPK, which switches on catabolism and off anabolism to regenerate ATP; restored ATP then inactivates AMPK — a negative-feedback homeostat that holds cellular energy charge. Class II.",
        "description": "The cell's fuel gauge. A falling ATP:AMP ratio activates AMPK, which promotes ATP-producing catabolism and shuts down ATP-consuming anabolism; as ATP is restored, AMP/ADP fall and AMPK switches off — classic negative feedback that stabilizes energy charge.",
        "scientificAccuracy": "AMPK activation by AMP/ADP and its restoration of energy charge are established (Hardie, Ross & Hawley 2012).",
        "nodes": [
            ("A", "[Low energy: high AMP/ADP]", "red"),
            ("B", "[AMPK activated]", "green"),
            ("C", "[Catabolism up, anabolism down]", "green"),
            ("D", "[ATP regenerated]", "blue"),
            ("E", "[/Rising ATP inactivates AMPK/]", "green"),
            ("F", "(Stable energy charge)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "B", "⊣ feedback"), ("D", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "AMPK: a nutrient and energy sensor that maintains energy homeostasis", "authors": "Hardie DG, Ross FA, Hawley SA", "journal": "Nature Reviews Molecular Cell Biology", "year": 2012, "volume": "13", "pages": "251-262", "pmid": "22436748", "doi": "10.1038/nrm3311"},
        ],
        "keywords": ["AMPK", "energy charge", "ATP", "metabolism", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_mtor_ulk1_autophagy", "human_mtorc1_nutrient"],
        "notes": "Human Class II energy homeostat: AMPK senses AMP/ADP and feeds back via restored ATP.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "AMPK targets (metabolic enzymes)", "boundFactor": "AMPK (AMP/ADP-activated)", "operator": "IF low-energy", "effect": "phosphorylation toggles catabolism/anabolism", "sequenceMotif": "(allosteric/phospho, not cis-DNA)", "note": "ATP output feeds back to switch AMPK off"},
            ],
            "derivedLogic": "AMPK = IF (AMP/ADP high) ; AMPK -> ATP -| AMPK (negative feedback)",
            "references": ["Hardie et al. 2012"],
        },
    },
    {
        "id": "human_p53_apoptosis_decision",
        "name": "p53 Arrest-vs-Apoptosis Decision Switch",
        "category": "DNA Damage Response",
        "circuitClass": "III",
        "topologyType": "threshold_bistable_decision",
        "rationale": "Sustained or high p53 activity crosses a threshold that commits cells from reversible cell-cycle arrest to irreversible apoptosis (PUMA/BAX), an all-or-none, effectively irreversible decision driven by feed-forward and feedback among p53 targets. Class III bistable/threshold switch (distinct from the p53–MDM2 oscillator).",
        "description": "How p53 chooses cell fate. Low or pulsatile p53 favors reversible arrest (p21); strong, sustained p53 induces apoptotic effectors (PUMA, BAX) past a commitment threshold, after which MOMP makes death irreversible. The downstream arrest-vs-death decision is a bistable switch, complementing the upstream p53–MDM2 oscillator already in the collection.",
        "scientificAccuracy": "Threshold/irreversible commitment from p53 dynamics to apoptosis is established (Purvis et al. 2012; Kracikova et al. 2013).",
        "nodes": [
            ("A", "[DNA damage: p53 active]", "red"),
            ("B", "{p53 above death threshold?}", "blue"),
            ("C", "[p21: reversible arrest]", "green"),
            ("D", "[PUMA/BAX induced]", "green"),
            ("E", "[\\MOMP commits to death/]", "green"),
            ("F", "(Reversible arrest)", "violet"),
            ("G", "(Irreversible apoptosis)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", "No / low"), ("C", "F", ""),
            ("B", "D", "Yes / high"), ("D", "E", ""), ("E", "D", "+"), ("E", "G", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "p53 dynamics control cell fate", "authors": "Purvis JE, Karhohs KW, Mock C, et al.", "journal": "Science", "year": 2012, "volume": "336", "pages": "1440-1444", "pmid": "22700930", "doi": "10.1126/science.1218351"},
            {"title": "A threshold mechanism mediates p53 cell fate decision between growth arrest and apoptosis", "authors": "Kracikova M, Akiri G, George A, Sachidanandam R, Aaronson SA", "journal": "Cell Death & Differentiation", "year": 2013, "volume": "20", "pages": "576-588", "pmid": "23306555", "doi": "10.1038/cdd.2012.155"},
        ],
        "keywords": ["p53", "apoptosis", "decision", "threshold", "bistable", "PUMA", "BAX", "Class III", "ground truth"],
        "relatedProcesses": ["human_p53_mdm2_oscillator", "human_caspase_apoptosis", "human_bcl2_bax_momp"],
        "notes": "Human Class III decision switch (arrest vs apoptosis); complements the p53-MDM2 Class IV oscillator.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "p53 response elements (CDKN1A vs BBC3/BAX)", "boundFactor": "p53", "operator": "threshold IF", "effect": "low->p21 arrest, high->PUMA/BAX death", "sequenceMotif": "RRRCWWGYYY x2 (p53 RE)", "note": "promoter affinity + dynamics set the threshold"},
            ],
            "derivedLogic": "fate = IF p53>θ THEN apoptosis ELSE arrest (bistable commitment)",
            "references": ["Purvis et al. 2012", "Kracikova et al. 2013"],
        },
    },
    {
        "id": "human_il6_stat3_inflammation",
        "name": "IL-6/STAT3 Inflammatory Positive-Feedback Switch",
        "category": "Inflammatory Signaling",
        "circuitClass": "III", "circuitSubclass": "IIIa",
        "topologyType": "positive_feedback_bistable_inflammation",
        "rationale": "IL-6 activates STAT3, which (with NF-κB) drives more IL-6; the cytokine positive-feedback loop can latch cells into a self-sustaining inflammatory/transformed state — a persistent (IIIa) bistable switch underlying chronic inflammation and cancer.",
        "description": "A self-amplifying inflammatory loop. IL-6 signals through JAK to activate STAT3; STAT3 cooperates with NF-κB to induce IL-6 itself, so transient stimulation can lock cells into a persistent inflammatory program. The positive feedback gives bistable, hysteretic behavior linked to chronic inflammation and tumor promotion.",
        "scientificAccuracy": "The IL-6/STAT3/NF-κB positive-feedback loop and its bistable inflammatory/transformation role are established (Iliopoulos, Hirsch & Struhl 2009; Grivennikov & Karin 2010).",
        "nodes": [
            ("A", "[Inflammatory trigger]", "red"),
            ("B", "[IL-6]", "yellow"),
            ("C", "[JAK-STAT3 active]", "green"),
            ("D", "[\\STAT3 + NF-κB induce IL-6/]", "green"),
            ("E", "[Inflammatory gene program]", "green"),
            ("F", "(Self-sustaining inflammation)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "B", "+"), ("C", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "An epigenetic switch involving NF-κB, Lin28, let-7 and IL6 links inflammation to transformation", "authors": "Iliopoulos D, Hirsch HA, Struhl K", "journal": "Cell", "year": 2009, "volume": "139", "pages": "693-706", "pmid": "19878981", "doi": "10.1016/j.cell.2009.10.014"},
            {"title": "Dangerous liaisons: STAT3 and NF-κB collaboration and crosstalk in cancer", "authors": "Grivennikov SI, Karin M", "journal": "Cytokine & Growth Factor Reviews", "year": 2010, "volume": "21", "pages": "11-19", "pmid": "20018552", "doi": "10.1016/j.cytogfr.2009.11.005"},
        ],
        "keywords": ["IL-6", "STAT3", "NF-κB", "positive feedback", "inflammation", "bistable", "Class IIIa", "ground truth"],
        "relatedProcesses": ["human_jak_stat_socs", "human_nfkb_oscillator"],
        "notes": "Human Class IIIa inflammatory switch: IL-6/STAT3/NF-κB positive feedback latches an inflammatory state.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "IL6 promoter", "boundFactor": "STAT3 + NF-κB", "operator": "AND / positive feedback", "effect": "cytokine self-amplification", "sequenceMotif": "TTCnnnGAA (STAT) + GGGRNNYYCC (κB)", "note": "loop closes IL-6 -> STAT3 -> IL-6"},
            ],
            "derivedLogic": "IL-6 = STAT3 AND NF-κB ; positive feedback -> bistable inflammation",
            "references": ["Iliopoulos et al. 2009"],
        },
    },
    {
        "id": "human_iron_irp_ire",
        "name": "IRP/IRE Iron Homeostat",
        "category": "Metal Homeostasis",
        "circuitClass": "II",
        "topologyType": "post_transcriptional_negative_feedback",
        "rationale": "When iron is low, iron-regulatory proteins (IRP1/2) bind IRE stem-loops to stabilize transferrin-receptor mRNA (more uptake) and block ferritin translation (less storage); rising iron inactivates the IRPs — a post-transcriptional negative-feedback homeostat for cellular iron. Class II.",
        "description": "Cellular iron is held constant by RNA-binding feedback. Under iron scarcity, IRP1/2 bind iron-responsive elements: at the transferrin-receptor mRNA they block degradation (boosting uptake), at ferritin/ferroportin mRNAs they block translation (cutting storage/export). Iron repletion converts IRP1 to aconitase and degrades IRP2, releasing the IREs — negative feedback on iron.",
        "scientificAccuracy": "IRP/IRE post-transcriptional control of iron homeostasis is established (Hentze, Muckenthaler & Andrews 2010).",
        "nodes": [
            ("A", "[Low cellular iron]", "red"),
            ("B", "[IRP1/2 bind IRE elements]", "green"),
            ("C", "[Transferrin-receptor mRNA stabilized]", "green"),
            ("D", "[/Ferritin translation blocked/]", "green"),
            ("E", "[Iron uptake rises]", "blue"),
            ("F", "[/Rising iron inactivates IRPs/]", "green"),
            ("G", "(Iron homeostasis)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("B", "D", ""),
            ("C", "E", ""), ("E", "F", ""), ("F", "B", "⊣ feedback"), ("E", "G", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Two to tango: regulation of mammalian iron metabolism", "authors": "Hentze MW, Muckenthaler MU, Galy B, Camaschella C", "journal": "Cell", "year": 2010, "volume": "142", "pages": "24-38", "pmid": "20603012", "doi": "10.1016/j.cell.2010.06.028"},
        ],
        "keywords": ["IRP", "IRE", "iron", "ferritin", "transferrin receptor", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_nrf2_keap1", "human_vhl_hif"],
        "notes": "Human Class II post-transcriptional homeostat (iron); IRP-IRE binding tuned by iron level.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "IREs (TfR1 3'UTR, ferritin 5'UTR)", "boundFactor": "IRP1/IRP2", "operator": "IF low-iron", "effect": "stabilize uptake mRNA, block storage mRNA", "sequenceMotif": "CAGUGH stem-loop (IRE)", "note": "iron level sets IRP RNA-binding -> feedback"},
            ],
            "derivedLogic": "IRP-bound = NOT iron ; uptake up & storage down -> iron restored -| IRP",
            "references": ["Hentze et al. 2010"],
        },
    },
    {
        "id": "human_camp_pka_desensitization",
        "name": "cAMP/PKA GPCR Desensitization",
        "category": "GPCR Signaling",
        "circuitClass": "II",
        "topologyType": "receptor_desensitization_negative_feedback",
        "rationale": "Agonist-bound GPCR raises cAMP and activates PKA; PKA and GRK-driven β-arrestin recruitment phosphorylate and desensitize the receptor while PDEs degrade cAMP — negative feedback that adapts the response. Class II.",
        "description": "GPCR signaling adapts to sustained stimulation. Agonist binding activates Gαs and adenylyl cyclase, raising cAMP and activating PKA; PKA and GPCR kinases phosphorylate the receptor, recruiting β-arrestin to uncouple it, while phosphodiesterases degrade cAMP. The combined negative feedback desensitizes the pathway.",
        "scientificAccuracy": "GPCR desensitization by GRK/β-arrestin and PDE-mediated cAMP turnover are established (Lefkowitz 2004).",
        "nodes": [
            ("A", "[Agonist binds GPCR]", "red"),
            ("B", "[cAMP rises, PKA active]", "green"),
            ("C", "[Cellular response]", "blue"),
            ("D", "[/GRK + β-arrestin desensitize receptor/]", "green"),
            ("E", "[/PDE degrades cAMP/]", "green"),
            ("F", "(Adapted GPCR response)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("B", "D", ""),
            ("D", "A", "⊣ feedback"), ("B", "E", ""), ("E", "B", "⊣"), ("C", "F", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "Historical review: a brief history and personal retrospective of seven-transmembrane receptors", "authors": "Lefkowitz RJ", "journal": "Trends in Pharmacological Sciences", "year": 2004, "volume": "25", "pages": "413-422", "pmid": "15276710", "doi": "10.1016/j.tips.2004.06.006"},
        ],
        "keywords": ["GPCR", "cAMP", "PKA", "beta-arrestin", "desensitization", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_insulin_akt_foxo"],
        "notes": "Human Class II adaptation homeostat: GPCR desensitization + cAMP degradation feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "receptor C-tail (GRK/PKA sites)", "boundFactor": "GRK / β-arrestin", "operator": "NOT", "effect": "phospho-desensitization", "sequenceMotif": "(protein-level)", "note": "PDE turnover of cAMP adds second negative arm"},
            ],
            "derivedLogic": "response = agonist AND NOT desensitized ; PDE -| cAMP (negative feedback)",
            "references": ["Lefkowitz 2004"],
        },
    },
    {
        "id": "human_glucocorticoid_hpa_axis",
        "name": "Glucocorticoid HPA-Axis Feedback",
        "category": "Endocrine Signaling",
        "circuitClass": "II",
        "topologyType": "endocrine_negative_feedback_homeostat",
        "rationale": "Stress drives CRH→ACTH→cortisol; cortisol acts back on the pituitary and hypothalamus through the glucocorticoid receptor to suppress CRH/ACTH — the textbook endocrine negative-feedback homeostat that sets circulating cortisol. Class II.",
        "description": "The hypothalamic-pituitary-adrenal stress axis. Hypothalamic CRH stimulates pituitary ACTH, which drives adrenal cortisol; cortisol binds the glucocorticoid receptor in the pituitary and hypothalamus to inhibit CRH and ACTH — long-loop negative feedback that stabilizes cortisol and terminates the stress response.",
        "scientificAccuracy": "Glucocorticoid negative feedback on the HPA axis is a textbook endocrine homeostat (Herman et al. 2016).",
        "nodes": [
            ("A", "[Stress]", "red"),
            ("B", "[Hypothalamus: CRH]", "green"),
            ("C", "[Pituitary: ACTH]", "green"),
            ("D", "[Adrenal: cortisol]", "yellow"),
            ("E", "[/Cortisol-GR suppresses CRH + ACTH/]", "green"),
            ("F", "(Cortisol set-point restored)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "B", "⊣ feedback"), ("E", "C", "⊣"), ("D", "F", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "Regulation of the hypothalamic-pituitary-adrenocortical stress response", "authors": "Herman JP, McKlveen JM, Ghosal S, et al.", "journal": "Comprehensive Physiology", "year": 2016, "volume": "6", "pages": "603-621", "pmid": "27065163", "doi": "10.1002/cphy.c150015"},
        ],
        "keywords": ["HPA axis", "cortisol", "glucocorticoid receptor", "CRH", "ACTH", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_insulin_akt_foxo"],
        "notes": "Human Class II endocrine homeostat: glucocorticoid long-loop negative feedback on the HPA axis.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "CRH / POMC promoters (nGRE)", "boundFactor": "glucocorticoid receptor (cortisol)", "operator": "NOT", "effect": "transcriptional repression of CRH/ACTH", "sequenceMotif": "negative GRE", "note": "closes the long-loop feedback"},
            ],
            "derivedLogic": "cortisol -| (CRH, ACTH) -> cortisol set-point (negative feedback)",
            "references": ["Herman et al. 2016"],
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
    print(f"Wrote {len(rows)} human Batch-7 process files -> {OUT_DIR}\n")
    print(f"{'id':<40} {'cls':<4} {'sub':<5} {'nodes':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<40} {r[1]:<4} {r[2]:<5} {r[3]:<6} {r[4]:<6} {r[5]}")


if __name__ == "__main__":
    main()
