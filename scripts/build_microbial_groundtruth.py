#!/usr/bin/env python3
"""
Ground-truth microbial / phage circuits added to the existing organism directories.
These are textbook circuits whose topology and dynamics are not in doubt, filling
gaps on the ladder — especially a genuine biological Class V (epigenetic prion memory).

  yeast_gal_bistable_switch  -> III (IIIa)  galactose network hysteresis (Acar et al. 2005)
  yeast_whi5_sbf_start       -> III (IIIa)  Start commitment switch (Skotheim et al. 2008)
  ecoli_lambda_switch        -> III (IIIa)  phage lambda CI/Cro lysis-lysogeny (Ptashne)
  yeast_sup35_prion          -> V           [PSI+] prion epigenetic memory (Shorter & Lindquist)

Marked groundTruth=true so scripts/apply_circuit_classes.py leaves their authored class
alone. Files are written into glmp-v2/processes/{yeast,ecoli}/ by id prefix.
Run scripts/integrate_microbial_groundtruth.py afterward to index them.
"""

import json
from pathlib import Path

from build_synthetic_batch1 import COLOR_SCHEME, CLASS_NAME, build_mermaid, compute_stats

BASE = Path("glmp-v2/processes")


def out_dir_for(pid):
    if pid.startswith("yeast_"):
        return BASE / "yeast"
    if pid.startswith("ecoli_"):
        return BASE / "ecoli"
    if pid.startswith("bacillus_"):
        return BASE / "bacillus"
    raise ValueError(f"unknown organism prefix: {pid}")


def make_process(spec):
    nodes, edges = spec["nodes"], spec["edges"]
    stats = compute_stats(nodes, edges)
    or_g, and_g, not_g = spec["gates"]
    cls = spec["circuitClass"]
    return {
        "id": spec["id"],
        "name": spec["name"],
        "organism": spec["organism"],
        "category": spec["category"],
        "description": spec["description"],
        "scientificAccuracy": spec["scientificAccuracy"],
        "complexity": {
            "nodes": stats["nodes"],
            "uniqueIdentifiers": True,
            "colorCoded": True,
            "detailLevel": "curated",
            "logicGates": {"orGates": or_g, "andGates": and_g, "total": or_g + and_g},
        },
        "colorScheme": COLOR_SCHEME,
        "mermaid": build_mermaid(nodes, edges),
        "sources": spec["sources"],
        "keywords": spec["keywords"],
        "relatedProcesses": spec.get("relatedProcesses", []),
        "created": "2026-06-12",
        "lastUpdated": "2026-06-12",
        "verified": True,
        "verifiedBy": "Curated from primary literature (textbook ground-truth circuit)",
        "notes": spec["notes"],
        "sequenceAnnotation": spec["sequenceAnnotation"],
        "logicGates": {"or": or_g, "and": and_g, "not": not_g},
        "notGates": not_g,
        "conditionals": stats["conditionals"],
        "totalNodes": stats["nodes"],
        "edges": stats["edges"],
        "loops": stats["loops"],
        "circuitClass": cls,
        "circuitClassName": CLASS_NAME[cls],
        "topologyType": spec["topologyType"],
        "circuitClassConfidence": "high",
        "circuitClassNeedsReview": False,
        "circuitClassRationale": spec["rationale"],
        "circuitClassEvidence": "curated_literature",
        "groundTruth": True,
        "circuitSubclass": spec.get("circuitSubclass"),
    }


SPECS = [
    {
        "id": "yeast_gal_bistable_switch",
        "name": "Galactose Network Bistable Switch (GAL)",
        "organism": "S. cerevisiae",
        "category": "Carbon Metabolism / Bistability",
        "circuitClass": "III", "circuitSubclass": "IIIa",
        "topologyType": "positive_feedback_bistable_hysteresis",
        "rationale": "Galactose activates Gal3p, which sequesters the repressor Gal80p and frees the activator Gal4p; Gal4p induces GAL3 and the transporter GAL2, a positive-feedback loop that makes GAL induction bistable and hysteretic — a persistent (IIIa) switch with memory of past galactose exposure (Acar, Becskei & van Oudenaarden 2005).",
        "description": "The yeast galactose-utilization network behaves as a bistable switch. Galactose-bound Gal3p sequesters the repressor Gal80p, releasing the activator Gal4p; Gal4p then induces GAL3 and the galactose permease GAL2, positive feedback that produces history-dependent (hysteretic) ON/OFF states across a population.",
        "scientificAccuracy": "Bistability and hysteresis of the GAL network were demonstrated quantitatively in single cells (Acar, Becskei & van Oudenaarden 2005).",
        "nodes": [
            ("A", "[Galactose]", "red"),
            ("B", "[Gal3p activated]", "yellow"),
            ("C", "[/Sequesters Gal80p repressor/]", "green"),
            ("D", "[Gal4p activator freed]", "yellow"),
            ("E", "[GAL gene transcription]", "green"),
            ("F", "[\\Induces GAL3 + GAL2 feedback/]", "green"),
            ("G", "(Bistable GAL-ON state, hysteresis)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", "⊣ Gal80"),
            ("D", "E", ""), ("E", "F", ""), ("F", "B", "+"), ("D", "G", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Enhancement of cellular memory by reducing stochastic transitions", "authors": "Acar M, Becskei A, van Oudenaarden A", "journal": "Nature", "year": 2005, "volume": "435", "pages": "228-232", "pmid": "15889097", "doi": "10.1038/nature03524"},
        ],
        "keywords": ["GAL", "galactose", "Gal4", "Gal80", "Gal3", "bistable", "hysteresis", "positive feedback", "Class IIIa", "ground truth"],
        "relatedProcesses": ["yeast_gal_regulation", "synthetic_positive_autoregulation"],
        "notes": "Ground-truth yeast Class IIIa bistable switch (galactose memory); positive feedback via GAL3/GAL2.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "UAS_GAL", "boundFactor": "Gal4p (gated by Gal80p)", "operator": "IF / NOT(Gal80)", "effect": "activation when galactose present", "sequenceMotif": "CGGN11CCG (Gal4 UAS)", "note": "Gal3p-galactose sequesters Gal80p to free Gal4p; GAL3/GAL2 induction closes the positive loop"},
            ],
            "derivedLogic": "GAL genes = Gal4 AND NOT Gal80 ; Gal3/Gal2 feedback -> bistable",
            "references": ["Acar et al. 2005"],
        },
    },
    {
        "id": "yeast_whi5_sbf_start",
        "name": "Whi5–SBF Start Commitment Switch",
        "organism": "S. cerevisiae",
        "category": "Cell Cycle",
        "circuitClass": "III", "circuitSubclass": "IIIa",
        "topologyType": "double_negative_positive_feedback_bistable",
        "rationale": "Cln3-Cdk1 phosphorylates the inhibitor Whi5 to activate SBF; SBF drives CLN1/2, whose Cdk1 complexes further phosphorylate Whi5 — positive feedback (through a double-negative) that makes passage through Start a bistable, irreversible commitment (Skotheim et al. 2008). Persistent (IIIa).",
        "description": "The budding-yeast Start transition, the functional analogue of the mammalian restriction point. Cln3-Cdk1 begins phosphorylating the SBF inhibitor Whi5; once SBF fires, CLN1/2-Cdk1 hyperphosphorylates Whi5 and exports it from the nucleus, a positive-feedback loop that converts gradual growth into a rapid, all-or-none, irreversible commitment to division.",
        "scientificAccuracy": "Coherent feedback and bistable, switch-like Start activation were demonstrated by Skotheim, Di Talia, Siggia & Cross (2008).",
        "nodes": [
            ("A", "[Cell growth: Cln3-Cdk1]", "red"),
            ("B", "[/Phosphorylates Whi5/]", "green"),
            ("C", "[Whi5 exits nucleus]", "blue"),
            ("D", "[SBF active]", "yellow"),
            ("E", "[CLN1/2 transcription]", "green"),
            ("F", "[\\Cln1/2-Cdk1 hyperphosphorylates Whi5/]", "green"),
            ("G", "(Irreversible Start commitment)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "F", ""), ("F", "B", "+"), ("D", "G", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Positive feedback of G1 cyclins ensures coherent cell cycle entry", "authors": "Skotheim JM, Di Talia S, Siggia ED, Cross FR", "journal": "Nature", "year": 2008, "volume": "454", "pages": "291-296", "pmid": "18633409", "doi": "10.1038/nature07118"},
        ],
        "keywords": ["Whi5", "SBF", "Cln3", "CLN1/2", "Start", "bistable", "positive feedback", "Class IIIa", "ground truth"],
        "relatedProcesses": ["human_rb_e2f_restriction_point", "yeast_cell_cycle_control"],
        "notes": "Ground-truth yeast Class IIIa Start switch (the yeast counterpart of human Rb-E2F).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "SCB / MCB elements (CLN1/2, CLN2 promoter)", "boundFactor": "SBF (Swi4-Swi6), gated by Whi5", "operator": "IF / NOT(Whi5)", "effect": "activation when Whi5 phosphorylated out", "sequenceMotif": "CACGAAA (SCB)", "note": "CLN1/2 feedback hyperphosphorylates Whi5"},
            ],
            "derivedLogic": "CLN1/2 = SBF AND NOT Whi5 ; CLN1/2 -| Whi5 (positive feedback) -> bistable Start",
            "references": ["Skotheim et al. 2008"],
        },
    },
    {
        "id": "ecoli_lambda_switch",
        "name": "Bacteriophage λ CI/Cro Lysis–Lysogeny Switch",
        "organism": "Bacteriophage lambda",
        "category": "Phage Developmental Switch",
        "circuitClass": "III", "circuitSubclass": "IIIa",
        "topologyType": "mutual_repression_bistable_genetic_switch",
        "rationale": "CI and Cro repress each other's promoters at the OR operator (CI also activates its own PRM); mutual repression yields two stable states — lysogeny (CI high) and lysis (Cro high) — the archetypal natural bistable genetic switch (Ptashne, A Genetic Switch).",
        "description": "The decision between lysogeny and lysis in phage λ. The CI repressor and Cro protein bind the same OR operator region and repress each other's promoters, while CI also activates its own promoter PRM. The double-negative-plus-autoactivation topology is bistable: CI-high lysogeny is stably maintained until DNA damage triggers CI cleavage and a switch to Cro-high lysis.",
        "scientificAccuracy": "The CI/Cro bistable switch is the textbook natural genetic switch (Ptashne 2004; Arkin, Ross & McAdams 1998).",
        "nodes": [
            ("A", "[Infection / UV stress]", "red"),
            ("B", "[CI repressor]", "yellow"),
            ("C", "[Cro repressor]", "yellow"),
            ("D", "[\\CI activates own PRM/]", "green"),
            ("E", "[/CI represses PR Cro/]", "green"),
            ("F", "[/Cro represses PRM CI/]", "green"),
            ("G", "(Lysogeny: CI high)", "violet"),
            ("H", "(Lysis: Cro high)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("A", "C", ""),
            ("B", "D", ""), ("D", "B", "+"),
            ("B", "E", ""), ("E", "C", "⊣"),
            ("C", "F", ""), ("F", "B", "⊣"),
            ("B", "G", ""), ("C", "H", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "A Genetic Switch: Phage Lambda Revisited (3rd ed.)", "authors": "Ptashne M", "journal": "Cold Spring Harbor Laboratory Press", "year": 2004, "volume": "", "pages": "", "pmid": "", "doi": ""},
            {"title": "Stochastic kinetic analysis of developmental pathway bifurcation in phage lambda-infected Escherichia coli cells", "authors": "Arkin A, Ross J, McAdams HH", "journal": "Genetics", "year": 1998, "volume": "149", "pages": "1633-1648", "pmid": "9691025", "doi": "10.1093/genetics/149.4.1633"},
        ],
        "keywords": ["lambda", "CI", "Cro", "lysogeny", "lysis", "bistable", "genetic switch", "mutual repression", "Class IIIa", "ground truth"],
        "relatedProcesses": ["synthetic_toggle_switch", "human_gata1_pu1_switch"],
        "notes": "Ground-truth Class IIIa natural genetic switch (phage λ); two cross-repressions + CI autoactivation. Loads from the ecoli/ directory (host context).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "OR1/OR2 (PRM)", "boundFactor": "CI dimer", "operator": "IF (self) / NOT (Cro)", "effect": "CI autoactivation; represses PR", "sequenceMotif": "TACCTCTGGCGGTGATAA", "note": "lambda right operator consensus half-site"},
                {"name": "OR3 (PR)", "boundFactor": "Cro", "operator": "NOT", "effect": "represses PRM (CI)", "sequenceMotif": "TATCACCGCCAGAGGTA", "note": "Cro preference for OR3"},
            ],
            "derivedLogic": "CI = CI AND NOT Cro ; Cro = NOT CI -> bistable lysogeny/lysis",
            "references": ["Ptashne 2004"],
        },
    },
    {
        "id": "yeast_sup35_prion",
        "name": "[PSI+] Sup35 Prion Epigenetic Memory",
        "organism": "S. cerevisiae",
        "category": "Epigenetic Inheritance",
        "circuitClass": "V",
        "topologyType": "self_templating_conformational_memory",
        "rationale": "Sup35 can adopt a self-templating amyloid conformation ([PSI+]) that converts newly made soluble Sup35 to the same prion state; the heritable, protein-only, conformation-based change of state is a genuine biological Class V self-modifying / epigenetic memory (Shorter & Lindquist 2005).",
        "description": "A protein-based epigenetic switch. The translation-termination factor Sup35 can convert from a soluble functional form into a self-propagating amyloid ([PSI+]). The prion conformation templates conversion of newly synthesized Sup35, causing nonsense readthrough; the state is inherited through cell division without any DNA change — heredity carried by protein conformation.",
        "scientificAccuracy": "Self-templating prion conversion and cytoplasmic, protein-based inheritance of [PSI+] are established (Shorter & Lindquist 2005; True & Lindquist 2000).",
        "nodes": [
            ("A", "[Stress / stochastic nucleation]", "red"),
            ("B", "[Sup35 soluble, functional]", "yellow"),
            ("C", "[\\Prion seed templates conversion/]", "green"),
            ("D", "[Sup35 amyloid, PSI+]", "blue"),
            ("E", "[Nonsense readthrough phenotype]", "green"),
            ("F", "(Heritable epigenetic state PSI+)", "violet"),
        ],
        "edges": [
            ("A", "C", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "C", "+ self-template"), ("D", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "Prions as adaptive conduits of memory and inheritance", "authors": "Shorter J, Lindquist S", "journal": "Nature Reviews Genetics", "year": 2005, "volume": "6", "pages": "435-450", "pmid": "15931169", "doi": "10.1038/nrg1616"},
            {"title": "A yeast prion provides a mechanism for genetic variation and phenotypic diversity", "authors": "True HL, Lindquist SL", "journal": "Nature", "year": 2000, "volume": "407", "pages": "477-483", "pmid": "11028992", "doi": "10.1038/35035005"},
        ],
        "keywords": ["prion", "Sup35", "PSI+", "epigenetic", "self-templating", "protein inheritance", "Class V", "ground truth"],
        "relatedProcesses": ["synthetic_integrase_memory", "yeast_chromatin_silencing"],
        "notes": "Ground-truth biological Class V: conformation-based, self-modifying epigenetic memory (no cis-DNA change).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Sup35 N-domain (prion-forming)", "boundFactor": "Sup35 prion conformer", "operator": "SELF-MODIFY", "effect": "self-templating conformational conversion", "sequenceMotif": "QN-rich PrD (oligopeptide repeats)", "note": "protein-level state change; inherited cytoplasmically, not via DNA"},
            ],
            "derivedLogic": "Sup35_state := template(Sup35_state) -> heritable [PSI+]/[psi-] (self-modifying)",
            "references": ["Shorter & Lindquist 2005"],
        },
    },
]


def main():
    rows = []
    for spec in SPECS:
        proc = make_process(spec)
        d = out_dir_for(spec["id"])
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"{spec['id']}.json"
        with open(path, "w") as fh:
            json.dump(proc, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        rows.append((proc["id"], proc["organism"], proc["circuitClass"],
                     proc.get("circuitSubclass") or "-", proc["totalNodes"],
                     proc["loops"], proc["logicGates"]))
    print(f"Wrote {len(rows)} microbial ground-truth files\n")
    print(f"{'id':<30} {'organism':<22} {'cls':<4} {'sub':<5} {'nodes':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<30} {r[1]:<22} {r[2]:<4} {r[3]:<5} {r[4]:<6} {r[5]:<6} {r[6]}")


if __name__ == "__main__":
    main()
