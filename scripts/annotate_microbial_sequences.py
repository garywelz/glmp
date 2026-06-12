#!/usr/bin/env python3
"""
Task 3: attach a `sequenceAnnotation` block to the well-characterized microbial
circuits — the same schema Batch 1 (synthetic) uses, applied to real regulons whose
cis-regulatory sites are established in the literature.

Each block records, per regulatory region: the bound transcription factor, the site
name, the logical operator it implements (AND / OR / NOT / IF), its effect
(activation / repression), and a representative consensus motif. `derivedLogic` is the
Boolean expression for the controlled gene(s). Motifs are standard published consensus
sequences (cited inline); they are representations for the grammar corpus, not asserted
genomic coordinates.

Writes into glmp-v2/processes/**/<id>.json. Idempotent.
"""

import glob
import json
from pathlib import Path

PROCESS_GLOB = "glmp-v2/processes/**/*.json"
SCHEMA = "0.1"

# id -> {regulatoryRegions:[...], derivedLogic, references:[...]}
ANNOTATIONS = {
    "ecoli_lac_operon": {
        "regulatoryRegions": [
            {"name": "lacO1 operator", "boundFactor": "LacI tetramer", "operator": "NOT", "effect": "repression", "sequenceMotif": "AATTGTGAGCGGATAACAATT", "note": "primary lac operator; LacI occupancy occludes RNAP"},
            {"name": "CAP/CRP site (-61.5)", "boundFactor": "CAP-cAMP", "operator": "IF", "effect": "activation", "sequenceMotif": "TGTGA-N6-TCACA", "note": "class II activation; requires low glucose (high cAMP)"},
        ],
        "derivedLogic": "lacZYA = (NOT LacI[no allolactose]) AND (CAP-cAMP[low glucose])",
        "references": ["Jacob & Monod 1961", "Müller-Hill 1996"],
    },
    "ecoli_trp_operon": {
        "regulatoryRegions": [
            {"name": "trp operator (trpO)", "boundFactor": "TrpR-tryptophan", "operator": "NOT", "effect": "repression", "sequenceMotif": "ACTAGTTAACTAGT", "note": "TrpR is active only when charged with tryptophan (corepressor)"},
            {"name": "trpL attenuator", "boundFactor": "ribosome / leader RNA", "operator": "NOT", "effect": "premature termination", "sequenceMotif": "(trpL 1-2/3-4 hairpins)", "note": "tryptophan-charged tRNA controls terminator vs antiterminator"},
        ],
        "derivedLogic": "trpEDCBA = NOT (tryptophan abundant)  [repression + attenuation]",
        "references": ["Yanofsky 1981"],
    },
    "ecoli_ara_operon": {
        "regulatoryRegions": [
            {"name": "araI1-araI2 + araO2", "boundFactor": "AraC", "operator": "XOR-like", "effect": "repression (loop) / activation (arabinose)", "sequenceMotif": "(araI half-sites)", "note": "AraC represses by DNA looping (araO2-araI1); arabinose switches it to activator at araI1-araI2"},
            {"name": "CAP/CRP site", "boundFactor": "CAP-cAMP", "operator": "AND", "effect": "activation", "sequenceMotif": "TGTGA-N6-TCACA", "note": "needed for full pBAD activation"},
        ],
        "derivedLogic": "araBAD = arabinose AND CAP-cAMP  (AraC flips repressor->activator)",
        "references": ["Schleif 2010"],
    },
    "ecoli_arginine_biosynthesis": {
        "regulatoryRegions": [
            {"name": "ARG box", "boundFactor": "ArgR-arginine hexamer", "operator": "NOT", "effect": "repression", "sequenceMotif": "(ARG box: tandem 18 bp imperfect palindromes)", "note": "ArgR active as corepressor complex with L-arginine"},
        ],
        "derivedLogic": "arg biosynthesis genes = NOT (arginine abundant)",
        "references": ["Maas 1994"],
    },
    "ecoli_sos_response": {
        "regulatoryRegions": [
            {"name": "SOS box (LexA box)", "boundFactor": "LexA dimer", "operator": "NOT", "effect": "repression", "sequenceMotif": "CTGT-N8-ACAG", "note": "RecA*-stimulated LexA autocleavage derepresses; repression restored after repair (negative feedback)"},
        ],
        "derivedLogic": "SOS genes = NOT LexA ; LexA cleaved IF RecA* (ssDNA damage signal)",
        "references": ["Little & Mount 1982", "Walker 1996"],
    },
    "ecoli_pho_regulon": {
        "regulatoryRegions": [
            {"name": "PHO box", "boundFactor": "PhoB~P", "operator": "IF", "effect": "activation", "sequenceMotif": "CTGTCAT-N4-CTGTCAT", "note": "PhoR phosphorylates PhoB under phosphate starvation (two-component)"},
        ],
        "derivedLogic": "pho regulon = IF (Pi limiting -> PhoR~P -> PhoB~P)",
        "references": ["Wanner 1996"],
    },
    "ecoli_two_component_signaling": {
        "regulatoryRegions": [
            {"name": "OmpR boxes (ompF/ompC)", "boundFactor": "OmpR~P", "operator": "IF/NOT", "effect": "activation (ompC) / repression (ompF) by osmolarity", "sequenceMotif": "(tandem OmpR half-sites)", "note": "EnvZ kinase/phosphatase sets OmpR~P level by osmolarity"},
        ],
        "derivedLogic": "ompC = IF high osmolarity ; ompF = NOT high osmolarity (reciprocal)",
        "references": ["Kenney 2002"],
    },
    "ecoli_oxidative_stress_response": {
        "regulatoryRegions": [
            {"name": "OxyR site", "boundFactor": "OxyR (oxidized)", "operator": "IF", "effect": "activation", "sequenceMotif": "(4 ATAG elements)", "note": "H2O2 oxidizes OxyR disulfide -> activator; negative autoregulation restores set-point"},
            {"name": "SoxS site (soxbox)", "boundFactor": "SoxS", "operator": "IF", "effect": "activation", "sequenceMotif": "(soxbox)", "note": "SoxR senses superoxide -> induces soxS"},
        ],
        "derivedLogic": "antioxidant genes = IF (H2O2 -> OxyR-ox) OR (O2- -> SoxRS)",
        "references": ["Storz & Imlay 1999"],
    },
    "yeast_gal_regulation": {
        "regulatoryRegions": [
            {"name": "UAS_G", "boundFactor": "Gal4 dimer", "operator": "IF", "effect": "activation", "sequenceMotif": "CGG-N11-CCG", "note": "Gal4 bound constitutively; Gal80 masks its activation domain"},
            {"name": "Gal80/Gal3 switch", "boundFactor": "Gal80 (inhibitor), Gal3 (galactose sensor)", "operator": "NOT(NOT)", "effect": "de-repression + positive feedback", "sequenceMotif": "(protein-protein)", "note": "galactose+Gal3 sequesters Gal80 -> Gal4 active; GAL3/GAL80 feedback gives bistability"},
        ],
        "derivedLogic": "GAL genes = Gal4 AND (galactose -> Gal3 -| Gal80)  [bistable]",
        "references": ["Johnston 1987", "Acar et al. 2005"],
    },
    "yeast_gcn4_starvation": {
        "regulatoryRegions": [
            {"name": "GCRE (Gcn4 response element)", "boundFactor": "Gcn4", "operator": "IF", "effect": "activation", "sequenceMotif": "TGACTC", "note": "Gcn4 translation up under aa starvation via uORF reinitiation control on GCN4 mRNA"},
        ],
        "derivedLogic": "aa-biosynthesis genes = IF (uncharged tRNA -> Gcn2 -> eIF2alpha-P -> Gcn4 up)",
        "references": ["Hinnebusch 2005"],
    },
    "yeast_oxidative_stress_response": {
        "regulatoryRegions": [
            {"name": "YRE (Yap1 response element)", "boundFactor": "Yap1", "operator": "IF", "effect": "activation", "sequenceMotif": "TTACTAA", "note": "oxidation traps Yap1 in nucleus (Crm1 export blocked); homeostatic"},
        ],
        "derivedLogic": "antioxidant genes = IF (ROS -> Yap1 nuclear)",
        "references": ["Toledano et al. 2003"],
    },
    "yeast_heat_shock_response": {
        "regulatoryRegions": [
            {"name": "HSE (heat shock element)", "boundFactor": "Hsf1 trimer", "operator": "IF", "effect": "activation", "sequenceMotif": "nGAAn-nTTCn-nGAAn", "note": "inverted nGAAn repeats; chaperone titration provides negative feedback"},
        ],
        "derivedLogic": "chaperone genes = IF (unfolded protein -> Hsf1 active) ; NOT (free Hsp70)",
        "references": ["Morimoto 1998"],
    },
}


def main():
    by_id = {Path(f).stem: f for f in glob.glob(PROCESS_GLOB, recursive=True)}
    written, skipped = 0, []
    for pid, ann in ANNOTATIONS.items():
        path = by_id.get(pid)
        if not path:
            skipped.append(pid)
            continue
        proc = json.load(open(path))
        proc["sequenceAnnotation"] = {
            "schemaVersion": SCHEMA,
            "regulatoryRegions": ann["regulatoryRegions"],
            "derivedLogic": ann["derivedLogic"],
            "references": ann.get("references", []),
        }
        with open(path, "w") as fh:
            json.dump(proc, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        written += 1
    print(f"Annotated {written} microbial circuits with sequenceAnnotation")
    if skipped:
        print(f"  (not found, skipped): {skipped}")


if __name__ == "__main__":
    main()
