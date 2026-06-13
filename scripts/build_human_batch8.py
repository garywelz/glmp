#!/usr/bin/env python3
"""
Batch 8 of the GLMP collection: human innate-immunity, stress, and cell-fate circuits,
extending build_human_batch7.py.

Honest class assignment:
  Class II  : cGAS-STING antiviral induction, PERK-ATF4 integrated stress response
  Class III : RIG-I/MAVS antiviral all-or-none switch, NLRP3 inflammasome,
              TNF survival-vs-death decision
  Class IV  : pancreatic beta-cell glucose-insulin / Ca-metabolic oscillator

Reuses Batch 2's make_process (organism = Homo sapiens, groundTruth).
Output: glmp-v2/processes/human/<id>.json
"""

import json

from build_human_batch2 import make_process, OUT_DIR

SPECS = [
    {
        "id": "human_rig_i_mavs_antiviral",
        "name": "RIG-I/MAVS Antiviral Switch",
        "category": "Innate Immunity",
        "circuitClass": "III",
        "topologyType": "feedback_amplified_all_or_none_switch",
        "rationale": "Viral RNA activates RIG-I, which nucleates MAVS into self-propagating prion-like filaments that amplify IRF3/NF-κB signaling; the cooperative filament assembly plus type-I-IFN feed-forward gives a sharp, all-or-none antiviral commitment. Class III switch.",
        "description": "Cytosolic sensing of viral RNA. RIG-I binds short 5'-triphosphate dsRNA and oligomerizes on the adaptor MAVS, which forms self-templating aggregates on mitochondria; this digital amplification drives IRF3 and NF-κB to induce type-I interferon, converting a few sensed RNA molecules into a switch-like antiviral state.",
        "scientificAccuracy": "Prion-like MAVS filament amplification and switch-like IFN induction are established (Hou et al. 2011; Seth et al. 2005).",
        "nodes": [
            ("A", "[Viral 5'-ppp RNA]", "red"),
            ("B", "[RIG-I activated]", "yellow"),
            ("C", "[\\Nucleates MAVS prion-like filaments/]", "green"),
            ("D", "[IRF3 + NF-κB activated]", "green"),
            ("E", "[Type-I interferon induced]", "green"),
            ("F", "(All-or-none antiviral state)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "C", "+ amplify"), ("D", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "MAVS forms functional prion-like aggregates to activate and propagate antiviral innate immune response", "authors": "Hou F, Sun L, Zheng H, Skaug B, Jiang QX, Chen ZJ", "journal": "Cell", "year": 2011, "volume": "146", "pages": "448-461", "pmid": "21782231", "doi": "10.1016/j.cell.2011.06.041"},
            {"title": "Identification and characterization of MAVS, a mitochondrial antiviral signaling protein that activates NF-κB and IRF3", "authors": "Seth RB, Sun L, Ea CK, Chen ZJ", "journal": "Cell", "year": 2005, "volume": "122", "pages": "669-682", "pmid": "16125763", "doi": "10.1016/j.cell.2005.08.012"},
        ],
        "keywords": ["RIG-I", "MAVS", "interferon", "antiviral", "prion-like", "switch", "Class III", "ground truth"],
        "relatedProcesses": ["human_irf7_interferon", "human_nfkb_oscillator"],
        "notes": "Human Class III antiviral switch: cooperative MAVS filament amplification gives all-or-none IFN induction.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "IFNB1 enhanceosome", "boundFactor": "IRF3/IRF7 + NF-κB + ATF2/c-Jun", "operator": "AND (cooperative)", "effect": "switch-like IFN-β induction", "sequenceMotif": "PRDI-IV enhanceosome", "note": "MAVS filament amplification upstream sharpens the switch"},
            ],
            "derivedLogic": "IFN-β = IRF3 AND NF-κB ; MAVS positive amplification -> all-or-none",
            "references": ["Hou et al. 2011"],
        },
    },
    {
        "id": "human_cgas_sting_dna_sensing",
        "name": "cGAS–STING Cytosolic DNA Sensing",
        "category": "Innate Immunity",
        "circuitClass": "II",
        "topologyType": "induction_with_negative_feedback",
        "rationale": "Cytosolic DNA activates cGAS to make cGAMP, which activates STING→TBK1→IRF3 to induce type-I interferon; STING is then trafficked and degraded and negative regulators (e.g., induced by IFN) terminate signaling — an inducible response with negative feedback that resolves. Class II.",
        "description": "Detection of mislocalized DNA. cGAS binds cytosolic dsDNA and synthesizes the second messenger 2'3'-cGAMP, which activates STING at the ER; STING recruits TBK1 to phosphorylate IRF3, inducing interferon. STING is subsequently degraded after trafficking to lysosomes, and IFN-induced regulators feed back to terminate the response.",
        "scientificAccuracy": "cGAS-cGAMP-STING-TBK1-IRF3 signaling and STING-degradation-based termination are established (Sun et al. 2013; Ishikawa & Barber 2008).",
        "nodes": [
            ("A", "[Cytosolic dsDNA]", "red"),
            ("B", "[cGAS makes cGAMP]", "green"),
            ("C", "[STING-TBK1 activate IRF3]", "green"),
            ("D", "[Type-I interferon induced]", "blue"),
            ("E", "[/STING degraded; feedback terminates/]", "green"),
            ("F", "(Resolved antiviral response)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "C", "⊣ feedback"), ("D", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Cyclic GMP-AMP synthase is a cytosolic DNA sensor that activates the type I interferon pathway", "authors": "Sun L, Wu J, Du F, Chen X, Chen ZJ", "journal": "Science", "year": 2013, "volume": "339", "pages": "786-791", "pmid": "23258413", "doi": "10.1126/science.1232458"},
            {"title": "STING is an endoplasmic reticulum adaptor that facilitates innate immune signalling", "authors": "Ishikawa H, Barber GN", "journal": "Nature", "year": 2008, "volume": "455", "pages": "674-678", "pmid": "18724357", "doi": "10.1038/nature07317"},
        ],
        "keywords": ["cGAS", "STING", "cGAMP", "interferon", "DNA sensing", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_rig_i_mavs_antiviral", "human_irf7_interferon"],
        "notes": "Human Class II inducible antiviral response (cGAS-STING) with STING-degradation/IFN feedback termination.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "IFN/ISG promoters (ISRE)", "boundFactor": "IRF3 (via STING-TBK1)", "operator": "IF", "effect": "interferon induction by cytosolic DNA", "sequenceMotif": "ISRE (A/G NGAAANNGAAACT)", "note": "STING turnover provides negative feedback"},
            ],
            "derivedLogic": "IFN = IF cytosolic-DNA (cGAS->STING->IRF3) ; STING degradation -| signal",
            "references": ["Sun et al. 2013"],
        },
    },
    {
        "id": "human_nlrp3_inflammasome",
        "name": "NLRP3 Inflammasome All-or-None Switch",
        "category": "Innate Immunity / Inflammation",
        "circuitClass": "III",
        "topologyType": "nucleation_cooperative_all_or_none_switch",
        "rationale": "A priming signal licenses NLRP3; a second danger signal triggers NLRP3 to nucleate ASC into a single self-propagating speck that activates caspase-1; the cooperative, prion-like ASC polymerization makes pyroptotic activation digital and effectively irreversible. Class III switch.",
        "description": "The inflammasome converts danger signals into an all-or-none death/inflammation response. Priming (NF-κB) raises NLRP3 and pro-IL-1β; a second signal (K+ efflux, crystals, ATP) activates NLRP3 to seed ASC into one micron-scale speck whose self-templating polymerization recruits and activates caspase-1, driving IL-1β maturation and pyroptosis in a switch-like, single-cell manner.",
        "scientificAccuracy": "Prion-like ASC speck nucleation and digital caspase-1 activation are established (Cai et al. 2014; Lu et al. 2014).",
        "nodes": [
            ("A", "[Priming + danger signal]", "red"),
            ("B", "[NLRP3 activated]", "yellow"),
            ("C", "[\\Nucleates one ASC speck/]", "green"),
            ("D", "[Caspase-1 activated]", "green"),
            ("E", "[IL-1β maturation + pyroptosis]", "green"),
            ("F", "(All-or-none inflammasome firing)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "C", "+ self-template"), ("D", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "Prion-like polymerization underlies signal transduction in antiviral immune defense and inflammasome activation", "authors": "Cai X, Chen J, Xu H, et al.", "journal": "Cell", "year": 2014, "volume": "156", "pages": "1207-1222", "pmid": "24630723", "doi": "10.1016/j.cell.2014.01.063"},
            {"title": "Unified polymerization mechanism for the assembly of ASC-dependent inflammasomes", "authors": "Lu A, Magupalli VG, Ruan J, et al.", "journal": "Cell", "year": 2014, "volume": "156", "pages": "1193-1206", "pmid": "24630722", "doi": "10.1016/j.cell.2014.02.008"},
        ],
        "keywords": ["NLRP3", "inflammasome", "ASC speck", "caspase-1", "pyroptosis", "all-or-none", "Class III", "ground truth"],
        "relatedProcesses": ["human_caspase_apoptosis", "human_nfkb_oscillator"],
        "notes": "Human Class III digital switch: prion-like ASC nucleation gives all-or-none caspase-1/pyroptosis.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "NLRP3 / IL1B promoters (priming)", "boundFactor": "NF-κB", "operator": "IF (priming) AND danger-signal", "effect": "licenses then triggers the switch", "sequenceMotif": "κB sites", "note": "ASC self-polymerization makes firing digital"},
            ],
            "derivedLogic": "firing = priming AND danger ; ASC nucleation -> all-or-none caspase-1",
            "references": ["Cai et al. 2014", "Lu et al. 2014"],
        },
    },
    {
        "id": "human_perk_atf4_isr",
        "name": "PERK–ATF4 Integrated Stress Response",
        "category": "Proteostasis / Stress",
        "circuitClass": "II",
        "topologyType": "translational_negative_feedback_homeostat",
        "rationale": "Stress activates PERK to phosphorylate eIF2α, halting bulk translation while inducing ATF4; ATF4 drives GADD34, which dephosphorylates eIF2α to restore translation — a negative-feedback homeostat that adapts to stress. Class II.",
        "description": "A branch of the integrated stress response. ER or other stress activates the kinase PERK, which phosphorylates eIF2α to suppress global translation while selectively translating ATF4. ATF4 induces GADD34 (PP1 targeting subunit) that dephosphorylates eIF2α, restoring translation — negative feedback that resolves the stress program.",
        "scientificAccuracy": "PERK-eIF2α-ATF4-GADD34 negative feedback in the ISR is established (Harding et al. 2003; Walter & Ron 2011).",
        "nodes": [
            ("A", "[Stress: ER / amino-acid / heme]", "red"),
            ("B", "[PERK phosphorylates eIF2α]", "green"),
            ("C", "[Bulk translation down; ATF4 up]", "yellow"),
            ("D", "[ATF4 induces GADD34]", "green"),
            ("E", "[/GADD34 dephosphorylates eIF2α/]", "green"),
            ("F", "(Translation restored, adapted)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "B", "⊣ feedback"), ("C", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "An integrated stress response regulates amino acid metabolism and resistance to oxidative stress", "authors": "Harding HP, Zhang Y, Zeng H, et al.", "journal": "Molecular Cell", "year": 2003, "volume": "11", "pages": "619-633", "pmid": "12667446", "doi": "10.1016/S1097-2765(03)00105-9"},
        ],
        "keywords": ["PERK", "eIF2alpha", "ATF4", "GADD34", "integrated stress response", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_ire1_xbp1_upr", "human_hsf1_heat_shock"],
        "notes": "Human Class II translational homeostat (ISR): ATF4-GADD34 feedback restores eIF2α/translation.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "ATF4 uORFs (5'UTR) + CARE/AARE targets", "boundFactor": "ATF4 (translationally controlled)", "operator": "IF p-eIF2α", "effect": "selective ATF4 translation then GADD34 feedback", "sequenceMotif": "uORF1/uORF2; C/EBP-ATF (CARE)", "note": "GADD34-PP1 dephosphorylates eIF2α"},
            ],
            "derivedLogic": "ATF4 = IF p-eIF2α(stress) ; ATF4->GADD34 -| p-eIF2α (negative feedback)",
            "references": ["Harding et al. 2003"],
        },
    },
    {
        "id": "human_tnf_survival_death_decision",
        "name": "TNF Survival-vs-Death Decision Switch",
        "category": "Cell-Fate Signaling",
        "circuitClass": "III",
        "topologyType": "bistable_competing_outputs_decision",
        "rationale": "TNF engages a complex that both activates pro-survival NF-κB (complex I) and, if NF-κB-induced survival genes are insufficient, assembles a death complex (complex II) driving apoptosis/necroptosis; the competition between the two arms is a bistable life-or-death decision. Class III.",
        "description": "One ligand, two fates. TNF binding first nucleates complex I that activates NF-κB and pro-survival genes (cFLIP, cIAPs); if NF-κB output is too low or delayed, the receptor complex converts to the cytosolic death-inducing complex II that triggers caspase-8 apoptosis or RIPK3/MLKL necroptosis. The opposing arms make the outcome a switch-like decision.",
        "scientificAccuracy": "The NF-κB-survival vs complex-II-death checkpoint downstream of TNF is established (Micheau & Tschopp 2003).",
        "nodes": [
            ("A", "[TNF binds TNFR1]", "red"),
            ("B", "[Complex I: NF-κB survival]", "green"),
            ("C", "{survival genes sufficient?}", "blue"),
            ("D", "[Pro-survival cFLIP/cIAP]", "green"),
            ("E", "[Complex II: caspase-8 / RIPK3]", "green"),
            ("F", "(Survival)", "violet"),
            ("G", "(Apoptosis / necroptosis)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", "Yes"), ("D", "F", ""),
            ("D", "E", "⊣"), ("C", "E", "No"), ("E", "G", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Induction of TNF receptor I-mediated apoptosis via two sequential signaling complexes", "authors": "Micheau O, Tschopp J", "journal": "Cell", "year": 2003, "volume": "114", "pages": "181-190", "pmid": "12887920", "doi": "10.1016/S0092-8674(03)00521-X"},
        ],
        "keywords": ["TNF", "NF-κB", "complex II", "apoptosis", "necroptosis", "decision", "bistable", "Class III", "ground truth"],
        "relatedProcesses": ["human_caspase_apoptosis", "human_nfkb_oscillator", "human_p53_apoptosis_decision"],
        "notes": "Human Class III life-or-death decision: NF-κB survival arm vs complex-II death arm downstream of TNF.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "NF-κB survival targets (CFLAR, BIRC)", "boundFactor": "NF-κB", "operator": "IF / NOT(death)", "effect": "cFLIP/cIAP suppress complex II", "sequenceMotif": "κB sites GGGRNNYYCC", "note": "insufficient survival output -> death arm wins"},
            ],
            "derivedLogic": "fate = IF NF-κB-survival>θ THEN live ELSE die (bistable)",
            "references": ["Micheau & Tschopp 2003"],
        },
    },
    {
        "id": "human_beta_cell_insulin_oscillator",
        "name": "Pancreatic β-Cell Glucose–Insulin Oscillator",
        "category": "Endocrine / Metabolic Signaling",
        "circuitClass": "IV",
        "topologyType": "metabolic_electrical_oscillator",
        "rationale": "Glucose metabolism raises ATP/ADP, closing K-ATP channels and depolarizing the β-cell; Ca²⁺ influx triggers insulin release but also activates K-Ca/metabolic negative feedback that repolarizes — the coupled fast-electrical and slow-metabolic feedback generates bursting Ca²⁺/insulin oscillations. Class IV.",
        "description": "Pulsatile insulin secretion arises from β-cell oscillations. Glucose raises the ATP/ADP ratio, closing K-ATP channels and depolarizing the membrane; voltage-gated Ca²⁺ entry triggers insulin exocytosis. Ca²⁺- and metabolism-dependent currents then repolarize the cell, and the interplay of fast electrical and slower metabolic feedback produces robust bursting and oscillatory insulin output.",
        "scientificAccuracy": "Bursting Ca²⁺/insulin oscillations from coupled electrical-metabolic feedback are established (Bertram, Sherman & Satin 2007; Tornheim 1997).",
        "nodes": [
            ("A", "[Glucose: ATP/ADP up]", "red"),
            ("B", "[K-ATP closes; depolarization]", "green"),
            ("C", "[\\Ca²⁺ influx triggers insulin/]", "green"),
            ("D", "[Cytosolic Ca²⁺ rise]", "blue"),
            ("E", "[/K-Ca + metabolic feedback repolarize/]", "green"),
            ("F", "(Bursting Ca²⁺ / pulsatile insulin)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""), ("D", "C", "+"),
            ("D", "E", ""), ("E", "B", "⊣ delayed"), ("D", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Metabolic and electrical oscillations: partners in controlling pulsatile insulin secretion", "authors": "Bertram R, Sherman A, Satin LS", "journal": "American Journal of Physiology - Endocrinology and Metabolism", "year": 2007, "volume": "293", "pages": "E890-E900", "pmid": "17666486", "doi": "10.1152/ajpendo.00359.2007"},
        ],
        "keywords": ["beta cell", "insulin", "calcium oscillation", "K-ATP", "bursting", "oscillator", "Class IV", "ground truth"],
        "relatedProcesses": ["human_calcium_oscillator", "human_insulin_akt_foxo"],
        "notes": "Human Class IV oscillator: coupled fast-electrical (Ca²⁺) and slow-metabolic feedback drive pulsatile insulin.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "(electro-metabolic, not cis-DNA)", "boundFactor": "ATP/ADP, Ca²⁺ on channels", "operator": "positive then delayed NOT", "effect": "depolarize/secrete then repolarize", "sequenceMotif": "(channel/metabolite level)", "note": "insulin granule exocytosis is the oscillatory output"},
            ],
            "derivedLogic": "depol = +ATP ; Ca²⁺ +trigger AND delayed NOT(K-Ca) -> bursting insulin",
            "references": ["Bertram et al. 2007"],
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
    print(f"Wrote {len(rows)} human Batch-8 process files -> {OUT_DIR}\n")
    print(f"{'id':<42} {'cls':<4} {'sub':<5} {'nodes':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<42} {r[1]:<4} {r[2]:<5} {r[3]:<6} {r[4]:<6} {r[5]}")


if __name__ == "__main__":
    main()
