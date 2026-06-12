#!/usr/bin/env python3
"""
Batch 4 of the GLMP collection: human disease / signaling circuits, extending
build_human_batch3.py. Emphasis on growth, survival, metabolic, and immune
signaling — the circuits most relevant to the Perturb-seq / disease-modeling work.

Honest class assignment:
  Class II  (negative feedback / homeostat): Hippo-YAP, JAK-STAT/SOCS, mTORC1, AKT-FOXO
  Class III (bistable switch):               p16-Rb senescence (IIIa, irreversible),
                                             BCL-2/BAX MOMP, IRF7 interferon amplifier
Reuses Batch 2's make_process (organism = Homo sapiens, groundTruth).
Output: glmp-v2/processes/human/<id>.json
"""

import json

from build_human_batch2 import make_process, OUT_DIR

SPECS = [
    # ───────────────────────── Class II — negative-feedback signaling ─────────────────────────
    {
        "id": "human_hippo_yap",
        "name": "Hippo–YAP/TAZ Growth-Control Pathway",
        "category": "Growth Control Signaling",
        "circuitClass": "II",
        "topologyType": "kinase_cascade_negative_feedback",
        "rationale": "At high cell density the MST–LATS kinase cascade phosphorylates YAP/TAZ, retaining them in the cytoplasm and blocking growth; YAP/TAZ targets feed back on pathway regulators — a negative-feedback growth homeostat. Class II.",
        "description": "The Hippo pathway scales organ size and enforces contact inhibition. At high density the MST1/2–LATS1/2 kinase cascade phosphorylates YAP/TAZ, sequestering them in the cytoplasm; at low density YAP/TAZ enter the nucleus, partner with TEAD, and drive proliferative targets that also feed back on pathway components.",
        "scientificAccuracy": "Hippo kinase regulation of YAP/TAZ and density-dependent growth control are established (Zhao et al. 2007; Yu, Zhao & Guan 2015).",
        "nodes": [
            ("A", "[Cell density / mechanical cues]", "red"),
            ("B", "{High density?}", "blue"),
            ("C", "[MST-LATS kinases active]", "green"),
            ("D", "[/LATS phosphorylates YAP-TAZ/]", "green"),
            ("E", "[YAP-TAZ retained in cytoplasm]", "blue"),
            ("F", "[YAP-TAZ nuclear + TEAD]", "yellow"),
            ("G", "[Target transcription: CTGF, CYR61]", "green"),
            ("H", "[/Feedback on pathway regulators/]", "green"),
            ("I", "(Contact inhibition vs growth)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", "Yes"), ("C", "D", ""), ("D", "E", ""),
            ("B", "F", "No"), ("F", "G", ""), ("G", "I", ""),
            ("G", "H", ""), ("H", "C", "+ feedback"),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Inactivation of YAP oncoprotein by the Hippo pathway is involved in cell contact inhibition", "authors": "Zhao B, Wei X, Li W, et al.", "journal": "Genes & Development", "year": 2007, "volume": "21", "pages": "2747-2761", "pmid": "17974916", "doi": "10.1101/gad.1602907"},
            {"title": "The Hippo pathway: regulators and regulations", "authors": "Yu FX, Zhao B, Guan KL", "journal": "Cell", "year": 2015, "volume": "163", "pages": "811-828", "pmid": "26544935", "doi": "10.1016/j.cell.2015.10.044"},
        ],
        "keywords": ["Hippo", "YAP", "TAZ", "LATS", "TEAD", "contact inhibition", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_wnt_beta_catenin"],
        "notes": "Human Class II growth homeostat: LATS-mediated repression of YAP/TAZ with target feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "TEAD binding site", "boundFactor": "YAP/TAZ-TEAD", "operator": "IF / NOT(LATS)", "effect": "activation when YAP nuclear", "sequenceMotif": "GGAATG (MCAT)", "note": "LATS phosphorylation gates YAP nuclear access -> negative control"},
            ],
            "derivedLogic": "YAP-targets = NOT(high-density LATS) ; feedback re-tunes set-point",
            "references": ["Yu et al. 2015"],
        },
    },
    {
        "id": "human_jak_stat_socs",
        "name": "JAK–STAT Signaling with SOCS Feedback",
        "category": "Cytokine Signaling",
        "circuitClass": "II",
        "topologyType": "socs_negative_feedback",
        "rationale": "Cytokine-activated JAK phosphorylates STAT, which transcribes targets including SOCS; SOCS then inhibits JAK — a delayed negative-feedback loop that makes cytokine signaling transient and adaptive. Class II.",
        "description": "Cytokine binding activates receptor-associated JAK kinases, which phosphorylate STAT transcription factors. Nuclear STAT dimers drive target genes including the SOCS family, which bind and inhibit JAK — closing a negative-feedback loop that limits the duration of cytokine signaling.",
        "scientificAccuracy": "JAK-STAT activation and SOCS-mediated negative feedback are established (Alexander & Hilton 2004; Yoshimura, Naka & Kubo 2007).",
        "nodes": [
            ("A", "[Cytokine: e.g. IL-6 / IFN]", "red"),
            ("B", "[JAK kinase active]", "green"),
            ("C", "[STAT phosphorylated, dimerized]", "yellow"),
            ("D", "[Nuclear STAT target transcription]", "green"),
            ("E", "[SOCS induced]", "yellow"),
            ("F", "[/SOCS inhibits JAK/]", "green"),
            ("G", "(Transient adaptive response)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "F", ""), ("F", "B", "⊣ feedback"),
            ("D", "G", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "The role of suppressors of cytokine signalling (SOCS) proteins in regulation of the immune response", "authors": "Alexander WS, Hilton DJ", "journal": "Annual Review of Immunology", "year": 2004, "volume": "22", "pages": "503-529", "pmid": "15032587", "doi": "10.1146/annurev.immunol.22.091003.090312"},
        ],
        "keywords": ["JAK", "STAT", "SOCS", "cytokine", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_irf7_interferon_amplifier"],
        "notes": "Human Class II circuit: STAT induces SOCS which inhibits JAK (delayed negative feedback).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "GAS / ISRE element (incl. SOCS promoters)", "boundFactor": "STAT dimer", "operator": "IF", "effect": "activation (incl. its own inhibitor SOCS)", "sequenceMotif": "TTCNNNGAA (GAS)", "note": "induces SOCS -> negative feedback on JAK"},
            ],
            "derivedLogic": "targets, SOCS = STAT ; JAK = NOT SOCS(t-τ) -> adaptive response",
            "references": ["Alexander & Hilton 2004"],
        },
    },
    {
        "id": "human_mtorc1_nutrient",
        "name": "mTORC1 Nutrient Homeostat with S6K Feedback",
        "category": "Metabolic Signaling",
        "circuitClass": "II",
        "topologyType": "s6k_irs_negative_feedback",
        "rationale": "Amino acids and growth factors activate mTORC1, which drives growth via S6K1/4E-BP1; activated S6K1 phosphorylates and inhibits IRS-1, dampening upstream PI3K input — a negative-feedback loop tuning growth signaling. Class II.",
        "description": "mTORC1 integrates amino-acid and growth-factor inputs to drive protein synthesis through S6K1 and 4E-BP1. Active S6K1 phosphorylates IRS-1, attenuating upstream insulin/PI3K signaling — a well-characterized negative-feedback loop (the basis of rapamycin's paradoxical AKT activation).",
        "scientificAccuracy": "mTORC1 control of growth and S6K1–IRS-1 negative feedback are established (Harrington et al. 2004; Saxton & Sabatini 2017).",
        "nodes": [
            ("A", "[Amino acids + growth factors]", "red"),
            ("B", "[mTORC1 active]", "yellow"),
            ("C", "[S6K1 / 4E-BP1]", "green"),
            ("D", "[Protein synthesis / growth]", "green"),
            ("E", "[/S6K1 inhibits IRS-1/]", "green"),
            ("F", "(Growth homeostasis)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("C", "E", ""), ("E", "A", "⊣ feedback"), ("D", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "The TSC1-2 tumor suppressor controls insulin-PI3K signaling via regulation of IRS proteins", "authors": "Harrington LS, Findlay GM, Gray A, et al.", "journal": "Journal of Cell Biology", "year": 2004, "volume": "166", "pages": "213-223", "pmid": "15249583", "doi": "10.1083/jcb.200403069"},
            {"title": "mTOR signaling in growth, metabolism, and disease", "authors": "Saxton RA, Sabatini DM", "journal": "Cell", "year": 2017, "volume": "168", "pages": "960-976", "pmid": "28283069", "doi": "10.1016/j.cell.2017.02.004"},
        ],
        "keywords": ["mTORC1", "S6K1", "IRS-1", "nutrient sensing", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_akt_foxo_insulin"],
        "notes": "Human Class II nutrient homeostat: S6K1-IRS-1 negative feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "mTORC1 signaling (post-translational)", "boundFactor": "S6K1 -> IRS-1", "operator": "NOT", "effect": "inhibitory phosphorylation of IRS-1", "sequenceMotif": "(protein-level)", "note": "feedback realized in phosphorylation, not cis-DNA"},
            ],
            "derivedLogic": "growth = mTORC1(nutrients) ; PI3K input = NOT S6K1 -> homeostat",
            "references": ["Saxton & Sabatini 2017"],
        },
    },
    {
        "id": "human_akt_foxo_insulin",
        "name": "Insulin–AKT–FOXO Metabolic Homeostat",
        "category": "Metabolic Signaling",
        "circuitClass": "II",
        "topologyType": "foxo_negative_feedback_homeostat",
        "rationale": "Insulin activates PI3K-AKT, which phosphorylates FOXO and excludes it from the nucleus; nuclear FOXO drives gluconeogenic/stress genes plus feedback regulators of the pathway — a negative-feedback metabolic homeostat switch-like in insulin. Class II.",
        "description": "Insulin signaling through PI3K-AKT phosphorylates FOXO transcription factors, excluding them from the nucleus and shutting off gluconeogenic and stress-resistance genes. When insulin is low, FOXO enters the nucleus and activates those programs, including feedback regulators of the insulin pathway — a homeostatic loop balancing glucose and stress responses.",
        "scientificAccuracy": "AKT phosphorylation/nuclear exclusion of FOXO and its transcriptional feedback are established (Brunet et al. 1999; Manning & Toker 2017).",
        "nodes": [
            ("A", "[Insulin signal]", "red"),
            ("B", "{Insulin high?}", "blue"),
            ("C", "[PI3K-AKT active]", "green"),
            ("D", "[/AKT excludes FOXO from nucleus/]", "green"),
            ("E", "[FOXO nuclear active]", "yellow"),
            ("F", "[Targets: G6Pase, SOD2, feedback]", "green"),
            ("G", "[/Feedback regulators on PI3K/]", "green"),
            ("H", "(Glucose / stress homeostasis)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", "Yes"), ("C", "D", ""), ("D", "E", "⊣"),
            ("B", "E", "No"), ("E", "F", ""), ("F", "H", ""),
            ("F", "G", ""), ("G", "C", "⊣ feedback"),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "Akt promotes cell survival by phosphorylating and inhibiting a Forkhead transcription factor", "authors": "Brunet A, Bonni A, Zigmond MJ, et al.", "journal": "Cell", "year": 1999, "volume": "96", "pages": "857-868", "pmid": "10102273", "doi": "10.1016/S0092-8674(00)80595-4"},
            {"title": "AKT/PKB signaling: navigating the network", "authors": "Manning BD, Toker A", "journal": "Cell", "year": 2017, "volume": "169", "pages": "381-405", "pmid": "28431241", "doi": "10.1016/j.cell.2017.04.001"},
        ],
        "keywords": ["insulin", "AKT", "FOXO", "PI3K", "negative feedback", "metabolism", "Class II", "ground truth"],
        "relatedProcesses": ["human_mtorc1_nutrient"],
        "notes": "Human Class II metabolic homeostat: AKT-FOXO with transcriptional feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "FOXO response element (DBE)", "boundFactor": "FOXO1/3", "operator": "IF / NOT(AKT)", "effect": "activation when insulin low", "sequenceMotif": "TTGTTTAC", "note": "AKT phosphorylation excludes FOXO from nucleus"},
            ],
            "derivedLogic": "FOXO-targets = NOT insulin(AKT) ; feedback regulators -> homeostat",
            "references": ["Brunet et al. 1999"],
        },
    },
    # ───────────────────────── Class III — bistable / all-or-none switches ─────────────────────────
    {
        "id": "human_p16_rb_senescence",
        "name": "p16–Rb Senescence Commitment Switch",
        "category": "Senescence",
        "circuitClass": "III", "circuitSubclass": "IIIa",
        "topologyType": "positive_feedback_irreversible_senescence",
        "rationale": "Oncogenic/replicative stress induces p16INK4a, which inhibits CDK4/6 and activates Rb; active Rb represses proliferative E2F targets and reinforces p16, a positive-feedback loop that locks cells into a stable, irreversible senescent state — a persistent (IIIa) switch.",
        "description": "Sustained oncogenic or replicative stress drives p16INK4a, which inhibits CDK4/6 so Rb stays hypophosphorylated and active. Active Rb represses E2F proliferation genes and reinforces the senescence program, a positive-feedback loop that makes senescence a stable, essentially irreversible cell-fate decision.",
        "scientificAccuracy": "Oncogene-induced senescence and the p16-Rb stable-arrest circuit are established (Serrano et al. 1997; Narita et al. 2003).",
        "nodes": [
            ("A", "[Oncogenic / replicative stress]", "red"),
            ("B", "[p16INK4a]", "yellow"),
            ("C", "[/Inhibits CDK4/6/]", "green"),
            ("D", "[Rb hypophosphorylated, active]", "yellow"),
            ("E", "[/Rb represses E2F proliferation/]", "green"),
            ("F", "[\\Reinforces p16 program/]", "green"),
            ("G", "(Irreversible senescence: stable arrest)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("D", "F", ""), ("F", "B", "+"),
            ("D", "G", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "Oncogenic ras provokes premature cell senescence associated with accumulation of p53 and p16INK4a", "authors": "Serrano M, Lin AW, McCurrach ME, Beach D, Lowe SW", "journal": "Cell", "year": 1997, "volume": "88", "pages": "593-602", "pmid": "9054499", "doi": "10.1016/S0092-8674(00)81902-9"},
        ],
        "keywords": ["p16", "Rb", "senescence", "bistable", "positive feedback", "irreversible", "Class IIIa", "ground truth"],
        "relatedProcesses": ["human_rb_e2f_restriction_point"],
        "notes": "Human Class IIIa irreversible commitment switch (senescence) via p16-Rb positive feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "E2F site (repressed in senescence)", "boundFactor": "Rb-E2F", "operator": "NOT", "effect": "stable repression of proliferation genes", "sequenceMotif": "TTTSSCGC", "note": "locked OFF in senescent state; reinforced by p16"},
            ],
            "derivedLogic": "proliferation = NOT(p16 -> Rb) ; positive feedback -> stable senescent state",
            "references": ["Serrano et al. 1997"],
        },
    },
    {
        "id": "human_bcl2_bax_momp",
        "name": "BCL-2/BAX Mitochondrial Apoptosis Switch",
        "category": "Apoptosis",
        "circuitClass": "III",
        "topologyType": "positive_feedback_momp_bistable",
        "rationale": "BH3-only proteins neutralize anti-apoptotic BCL-2/BCL-xL, freeing BAX/BAK; activated BAX recruits and activates more BAX (positive feedback), driving all-or-none mitochondrial outer-membrane permeabilization — a bistable Class III commitment switch upstream of caspases.",
        "description": "The mitochondrial apoptosis decision. BH3-only proteins inhibit anti-apoptotic BCL-2/BCL-xL, releasing BAX/BAK; active BAX auto-amplifies its own activation and oligomerizes in the outer mitochondrial membrane, producing all-or-none MOMP. The positive feedback makes commitment switch-like and upstream of the caspase cascade.",
        "scientificAccuracy": "BCL-2-family regulation of BAX/BAK and bistable, all-or-none MOMP are established (Chipuk & Green 2008; Tait & Green 2010).",
        "nodes": [
            ("A", "[Apoptotic stress: BH3-only]", "red"),
            ("B", "[/Inhibits BCL-2 / BCL-xL/]", "green"),
            ("C", "[BAX/BAK activated]", "yellow"),
            ("D", "[\\BAX auto-amplifies activation/]", "green"),
            ("E", "[MOMP: all-or-none]", "blue"),
            ("F", "(Commitment to apoptosis)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "C", "+"), ("C", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "How cells die: apoptosis pathways", "authors": "Chipuk JE, Green DR", "journal": "Journal of Allergy and Clinical Immunology", "year": 2008, "volume": "121", "pages": "S87-S92", "pmid": "18505631", "doi": "10.1016/j.jaci.2007.10.026"},
            {"title": "Mitochondria and cell death: outer membrane permeabilization and beyond", "authors": "Tait SW, Green DR", "journal": "Nature Reviews Molecular Cell Biology", "year": 2010, "volume": "11", "pages": "621-632", "pmid": "20683470", "doi": "10.1038/nrm2952"},
        ],
        "keywords": ["BCL-2", "BAX", "MOMP", "apoptosis", "bistable", "positive feedback", "Class III", "ground truth"],
        "relatedProcesses": ["human_apoptosis_caspase_switch"],
        "notes": "Human Class III bistable MOMP switch (upstream of caspase switch); BAX positive feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "BAX activation (protein-protein)", "boundFactor": "BH3-only / BCL-2 / BAX", "operator": "NOT / positive feedback", "effect": "membrane permeabilization", "sequenceMotif": "(protein-level: BH3 groove)", "note": "switch implemented in protein interactions, not cis-DNA"},
            ],
            "derivedLogic": "MOMP = NOT BCL-2 AND positive-feedback(BAX) -> all-or-none",
            "references": ["Tait & Green 2010"],
        },
    },
    {
        "id": "human_irf7_interferon_amplifier",
        "name": "IRF7 Type-I Interferon Amplification Switch",
        "category": "Innate Immunity",
        "circuitClass": "III",
        "topologyType": "positive_feedback_antiviral_switch",
        "rationale": "Viral sensing activates IRF3/7 to make IFN-β; secreted IFN signals through JAK-STAT to induce more IRF7, a positive-feedback amplifier that converts graded viral input into an all-or-none antiviral state. Class III.",
        "description": "Detection of viral nucleic acids activates IRF3/IRF7 to produce type-I interferon. Secreted IFN acts back through the JAK-STAT-ISGF3 pathway to induce more IRF7, a positive-feedback loop that sharply amplifies the response and commits the cell (and its neighbors) to an all-or-none antiviral state.",
        "scientificAccuracy": "IRF7 positive-feedback amplification of the type-I interferon response is established (Honda et al. 2005; Ivashkiv & Donlin 2014).",
        "nodes": [
            ("A", "[Viral RNA / PAMP]", "red"),
            ("B", "[IRF3 / IRF7 activated]", "yellow"),
            ("C", "[IFN-β secreted]", "green"),
            ("D", "[JAK-STAT-ISGF3]", "green"),
            ("E", "[\\Induces more IRF7/]", "green"),
            ("F", "[Antiviral ISG program]", "green"),
            ("G", "(All-or-none antiviral state)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "B", "+"), ("D", "F", ""), ("F", "G", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "IRF-7 is the master regulator of type-I interferon-dependent immune responses", "authors": "Honda K, Yanai H, Negishi H, et al.", "journal": "Nature", "year": 2005, "volume": "434", "pages": "772-777", "pmid": "15800576", "doi": "10.1038/nature03464"},
            {"title": "Regulation of type I interferon responses", "authors": "Ivashkiv LB, Donlin LT", "journal": "Nature Reviews Immunology", "year": 2014, "volume": "14", "pages": "36-49", "pmid": "24362405", "doi": "10.1038/nri3581"},
        ],
        "keywords": ["IRF7", "interferon", "antiviral", "positive feedback", "bistable", "Class III", "ground truth"],
        "relatedProcesses": ["human_jak_stat_socs"],
        "notes": "Human Class III antiviral commitment switch via IRF7 positive feedback (counterbalanced in vivo by SOCS/USP18).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "ISRE (incl. IRF7 promoter)", "boundFactor": "ISGF3 / IRF7", "operator": "IF", "effect": "activation (incl. more IRF7)", "sequenceMotif": "GAAANNGAAA (ISRE)", "note": "IFN induces IRF7 -> positive feedback amplification"},
            ],
            "derivedLogic": "IFN -> IRF7 -> IFN (positive feedback) -> all-or-none antiviral commitment",
            "references": ["Honda et al. 2005"],
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
    print(f"Wrote {len(rows)} human Batch-4 process files -> {OUT_DIR}\n")
    print(f"{'id':<42} {'cls':<4} {'sub':<5} {'nodes':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<42} {r[1]:<4} {r[2]:<5} {r[3]:<6} {r[4]:<6} {r[5]}")


if __name__ == "__main__":
    main()
