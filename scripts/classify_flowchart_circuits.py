#!/usr/bin/env python3
"""
Classify the GLMP flowchart collection into the five-class complexity ladder
(Paper I / Paper III) from circuit topology.

The 108 flowcharts in glmp-v2/processes/ are bacterial / yeast *processes*, not
the human K562 genes in gene_circuit_classes.tsv, so they cannot be joined by
gene name. Instead this mirrors the strategy of k562-empirical-sequel/classify_circuits.py:

  1. Curated literature layer  -> well-characterized circuits, HIGH confidence
  2. Category default heuristic -> MEDIUM confidence
  3. Fallback (feed-forward)    -> LOW confidence
  4. Mermaid cycle detection    -> supporting topology signal (recorded, not decisive,
     because most charts are drawn as feed-forward DAGs even when the biology has feedback)

Every row carries an evidence_source, a confidence, and a needs_review flag.
needs_review = True for anything not in the curated high-confidence layer — that
set is the validation worklist for Prof. Krampis.

Class definitions (Paper III, Sec. 4):
  I   Feed-forward cascade, no cycle (execution pathway; response determined by input)
  II  Negative feedback (homeostatic / self-correcting)
  III Bistable switch: positive feedback, mutual repression, or autoactivation
  IV  Delayed negative feedback -> sustained oscillation (e.g. cell cycle, circadian)
  V   Self-modifying chromatin / epigenetic (circuit rewrites its own architecture)

Output: collaborations/krampis-virtual-cell/flowchart-circuit-classes.tsv
"""

import csv
import glob
import json
import re
from collections import defaultdict
from pathlib import Path

PROCESS_GLOB = "glmp-v2/processes/**/*.json"
OUTPUT_TSV = Path("collaborations/krampis-virtual-cell/flowchart-circuit-classes.tsv")

# ── Curated literature layer (HIGH confidence) ───────────────────────────────
# (class, topology_type, rationale)
CURATED = {
    # ── Class II — negative feedback / homeostatic ──
    "ecoli_lac_operon":              ("II", "repressor_catabolite_neg_feedback", "LacI repression + CAP activation; allolactose-mediated negative feedback (Jacob-Monod)"),
    "ecoli_trp_operon":              ("II", "repression_attenuation", "Trp repressor + transcriptional attenuation: end-product negative feedback"),
    "ecoli_tryptophan_biosynthesis": ("II", "end_product_feedback_inhibition", "Tryptophan feedback-inhibits its own biosynthetic pathway"),
    "ecoli_arginine_biosynthesis":   ("II", "argR_repression_feedback", "ArgR-mediated end-product repression"),
    "ecoli_amino_acid_biosynthesis": ("II", "end_product_feedback_inhibition", "Branched end-product feedback inhibition of amino-acid biosynthesis"),
    "ecoli_catabolite_repression":   ("II", "global_neg_feedback", "cAMP-CAP global carbon control; homeostatic"),
    "ecoli_chemotaxis":              ("II", "perfect_adaptation_neg_feedback", "Methylation-based perfect adaptation (classic robust negative feedback)"),
    "ecoli_oxidative_stress_response":("II", "oxyR_soxRS_autoregulation", "OxyR / SoxRS negative autoregulation restores redox homeostasis"),
    "ecoli_e._coli_heat_shock_response":("II", "sigma32_neg_feedback", "sigma-32 (RpoH) negative feedback via chaperone titration"),
    "ecoli_heat_shock_response":     ("II", "chaperone_neg_feedback", "Chaperone-mediated negative feedback (protein quality control)"),
    "yeast_heat_shock_response":     ("II", "hsf1_neg_feedback", "Hsf1 negative feedback via chaperone titration"),
    "ecoli_iron_homeostasis":        ("II", "fur_neg_feedback", "Fur-mediated iron homeostasis"),
    "ecoli_nitrogen_assimilation":   ("II", "ntr_homeostasis", "Ntr (NtrBC) nitrogen homeostasis"),
    "ecoli_pho_regulon":             ("II", "phosphate_homeostasis", "PhoBR phosphate-starvation homeostasis"),
    "ecoli_stringent_response":      ("II", "ppGpp_feedback", "ppGpp-mediated growth-rate negative feedback"),
    "ecoli_e._coli_stringent_response":("II", "ppGpp_feedback", "ppGpp-mediated growth-rate negative feedback"),
    "ecoli_starvation_response":     ("II", "rpoS_homeostasis", "RpoS general stress homeostasis"),
    "ecoli_e._coli_two_component_signaling":("II", "envz_ompr_homeostasis", "EnvZ-OmpR two-component homeostatic control"),
    "ecoli_two_component_signaling": ("II", "envz_ompr_homeostasis", "EnvZ-OmpR two-component homeostatic control"),
    "ecoli_anaerobic_respiration":   ("II", "arcAB_fnr_regulation", "ArcAB / FNR redox-responsive homeostatic regulation"),
    "ecoli_envelope_stress_response":("II", "cpx_neg_feedback", "Cpx envelope-stress negative feedback"),
    "ecoli_periplasmic_stress":      ("II", "cpx_neg_feedback", "Cpx periplasmic-stress negative feedback"),
    "ecoli_cold_shock_response":     ("II", "csp_adaptation", "Cold-shock adaptation negative feedback"),
    "ecoli_heavy_metal_resistance":  ("II", "metal_homeostasis", "Cu/Zn efflux homeostasis"),
    "yeast_hog_pathway":             ("II", "hog_osmoadaptation_neg_feedback", "HOG MAPK osmoadaptation with negative feedback"),
    "yeast_osmotic_stress_response": ("II", "osmoadaptation_neg_feedback", "Glycerol-based osmoadaptation negative feedback"),
    "yeast_oxidative_stress_response":("II", "yap1_neg_feedback", "Yap1 redox homeostasis"),
    "yeast_unfolded_protein_response":("II", "ire1_hac1_neg_feedback", "Ire1-Hac1 UPR negative feedback"),
    "yeast_er_stress_response":      ("II", "upr_neg_feedback", "ER-stress UPR negative feedback"),
    "yeast_cell_wall_integrity":     ("II", "cwi_neg_feedback", "Pkc1-CWI homeostatic feedback"),
    "ecoli_e._coli_osmotic_stress_response":("II", "osmoadaptation_neg_feedback", "Osmoadaptation negative feedback"),
    "ecoli_e._coli_acid_resistance": ("II", "acid_homeostasis", "Acid-resistance pH homeostasis"),

    # ── Class III — bistable switch / positive feedback / mutual repression ──
    "ecoli_ara_operon":              ("III", "araC_positive_autoregulation", "AraC positive autoregulation; arabinose-uptake bistability"),
    "bacillus_competence_development":("III", "comK_positive_feedback_bistable", "ComK positive autoregulation: textbook bistable competence switch"),
    "bacillus_sporulation_initiation":("III", "spo0A_phosphorelay_bistable", "Spo0A phosphorelay; bistable sporulation cell-fate decision"),
    "bacillus_biofilm_formation":    ("III", "bistable_developmental", "Bistable matrix-producer vs motile cell-fate decision"),
    "bacillus_germination":          ("III", "germination_switch", "Triggered dormancy-exit switch"),
    "ecoli_biofilm_formation":       ("III", "bistable_developmental", "Bistable biofilm developmental decision"),
    "ecoli_quorum_sensing":          ("III", "autoinducer_positive_feedback", "Autoinducer positive-feedback population switch"),
    "yeast_gal_regulation":          ("III", "gal_positive_feedback_bistable", "Gal3/Gal80 positive feedback; classic bistable GAL switch"),
    "yeast_meiosis_regulation":      ("III", "ime1_commitment_bistable", "IME1 bistable meiotic commitment"),
    "yeast_mating_response":         ("III", "fus3_switch", "Pheromone MAPK mating commitment switch"),
    "yeast_mapk_mating":             ("III", "fus3_switch", "Pheromone MAPK mating commitment switch"),

    # ── Class IV — delayed negative feedback / oscillator ──
    "yeast_cell_cycle_control":      ("IV", "cdk_cyclin_oscillator", "CDK-cyclin oscillator with transcription-degradation delay"),
    "yeast_cell_cycle_checkpoints":  ("IV", "cell_cycle_oscillator_checkpoints", "Cell-cycle oscillator gated by checkpoint feedback"),

    # ── Class V — self-modifying chromatin / epigenetic ──
    "yeast_chromatin_silencing":     ("V", "sir_heterochromatin_self_propagating", "Sir2/3/4 self-propagating heterochromatin; epigenetic memory"),
    "yeast_mating_type_switching":   ("V", "silencing_recombination", "HM-locus epigenetic silencing + HO-directed cassette switching"),

    # ────────────────────────────────────────────────────────────────────────
    # Curated-layer extension (2026-06): promote textbook-unambiguous medium-
    # confidence charts to HIGH, and correct a few category-default misassignments.
    # Conservative: only entries defensible from standard literature are added;
    # genuinely ambiguous charts are left at medium (needs_review) for Krampis.
    # ────────────────────────────────────────────────────────────────────────

    # ── Class I — execution machinery (central dogma / metabolism / transport) ──
    # No regulatory feedback loop in the process itself; the chart is the pathway.
    "ecoli_glycolysis":              ("I", "glycolysis_execution", "Embden-Meyerhof-Parnas glycolysis: linear catabolic execution pathway (allostery noted, no transcriptional feedback loop in chart)"),
    "ecoli_tca_cycle":               ("I", "tca_execution_cycle", "TCA cycle is a metabolic execution cycle (mass flow), not a regulatory feedback circuit"),
    "ecoli_pentose_phosphate_pathway":("I", "ppp_execution", "Pentose phosphate execution pathway"),
    "ecoli_fatty_acid_synthesis":    ("I", "fas_execution", "Type II fatty-acid synthesis execution pathway"),
    "ecoli_fatty_acid_degradation":  ("I", "beta_oxidation_execution", "Fatty-acid β-oxidation execution pathway (FadR regulation handled separately)"),
    "ecoli_aerobic_respiration":     ("I", "etc_execution", "Aerobic respiration / electron-transport execution chain (ArcAB/FNR regulation is a separate circuit)"),
    "ecoli_dna_replication_initiation":("I", "replication_initiation_machinery", "oriC/DnaA replication-initiation execution machinery"),
    "ecoli_dna_replication_elongation":("I", "replication_machinery", "Replisome elongation execution machinery"),
    "ecoli_dna_replication_termination":("I", "replication_termination", "Ter/Tus replication-termination execution"),
    "ecoli_transcription_elongation":("I", "transcription_machinery", "Transcription elongation execution machinery"),
    "ecoli_transcription_termination":("I", "transcription_termination", "Rho-dependent / intrinsic termination execution"),
    "ecoli_translation_initiation":  ("I", "translation_machinery", "Translation initiation execution machinery"),
    "ecoli_translation_elongation":  ("I", "translation_machinery", "Translation elongation execution machinery"),
    "ecoli_translation_termination": ("I", "translation_machinery", "Translation termination & ribosome recycling execution"),
    "ecoli_ribosome_assembly":       ("I", "ribosome_assembly_execution", "Ribosome assembly/maturation execution pathway"),
    "ecoli_rna_polymerase_recycling":("I", "rnap_recycling_execution", "RNA-polymerase recycling/reinitiation execution"),
    "ecoli_base_excision_repair":    ("I", "ber_execution", "Base-excision-repair execution pathway"),
    "ecoli_nucleotide_excision_repair":("I", "ner_execution", "Nucleotide-excision-repair execution pathway"),
    "ecoli_mismatch_repair":         ("I", "mmr_execution", "Methyl-directed mismatch-repair execution pathway"),
    "ecoli_homologous_recombination":("I", "recombination_execution", "RecBCD/RecA homologous-recombination execution pathway"),
    "ecoli_peptidoglycan_biosynthesis":("I", "pg_biosynthesis_execution", "Peptidoglycan biosynthesis execution pathway"),
    "ecoli_outer_membrane_assembly": ("I", "bam_assembly_execution", "BAM-complex outer-membrane-protein assembly execution"),
    "ecoli_type_iii_secretion":      ("I", "t3ss_execution", "Type III secretion assembly/export execution"),
    "ecoli_phosphate_transport":     ("I", "transport_execution", "Pst/Pit phosphate-transport execution"),
    "ecoli_antibiotic_efflux_pumps": ("I", "efflux_execution", "Antibiotic efflux-pump export execution"),
    "ecoli_protein_folding_chaperones":("I", "folding_execution", "Chaperone-assisted protein-folding execution"),
    "ecoli_phage_defense":           ("I", "rm_crispr_execution", "Restriction-modification / CRISPR defense execution pathway"),
    # Feed-forward cascade corrected from a Class III developmental default:
    "ecoli_flagellar_assembly":      ("I", "flhDC_feed_forward_cascade", "Flagellar gene expression is an FlhDC→σ28 temporal feed-forward cascade (just-in-time program; Kalir et al. 2001), not a bistable switch"),
    "ecoli_e._coli_flagellar_assembly":("I", "flhDC_feed_forward_cascade", "Flagellar assembly temporal feed-forward cascade (Kalir et al. 2001)"),
    "yeast_glycolysis":              ("I", "glycolysis_execution", "Glycolysis execution pathway"),
    "yeast_aerobic_respiration":     ("I", "oxphos_execution", "Respiration / oxidative-phosphorylation execution chain"),
    "yeast_alcoholic_fermentation":  ("I", "fermentation_execution", "Alcoholic fermentation execution pathway"),
    "yeast_dna_replication":         ("I", "replication_machinery", "Replication & origin-licensing execution machinery"),
    "yeast_nucleotide_excision_repair":("I", "ner_execution", "NER execution pathway"),
    "yeast_rna_splicing":            ("I", "spliceosome_execution", "Spliceosomal pre-mRNA splicing execution"),
    "yeast_ribosome_biogenesis":     ("I", "ribosome_biogenesis_execution", "Ribosome biogenesis / rRNA-processing execution"),
    "yeast_ubiquitin_proteasome":    ("I", "ups_execution", "Ubiquitin-proteasome degradation execution"),
    "yeast_autophagy":               ("I", "autophagy_execution", "Autophagy execution pathway"),
    "yeast_mitochondrial_import":    ("I", "mito_import_execution", "TOM/TIM mitochondrial-import execution"),
    "yeast_mitochondrial_biogenesis":("I", "mito_biogenesis_execution", "Mitochondrial biogenesis execution (retrograde signaling separate)"),
    "yeast_vesicle_trafficking":     ("I", "copii_execution", "COPII ER-to-Golgi vesicle-trafficking execution"),
    "yeast_protein_folding":         ("I", "folding_execution", "Chaperone-assisted protein-folding execution"),
    "yeast_yeast_er_associated_degradation":("I", "erad_execution", "ER-associated degradation (ERAD) execution"),
    "yeast_yeast_vacuolar_protein_sorting":("I", "vps_execution", "Vacuolar protein sorting execution"),
    "yeast_yeast_peroxisome_biogenesis":("I", "peroxisome_execution", "Peroxisome biogenesis execution"),

    # ── Class II — regulatory negative feedback (promotions + corrections) ──
    "ecoli_sos_response":            ("II", "lexA_recA_neg_feedback", "SOS response: LexA repression with RecA*-coactivated LexA autocleavage; repression restored after repair (negative feedback) — corrected from repair-execution default"),
    "ecoli_dna_damage_checkpoint":   ("II", "sos_sula_checkpoint", "SOS-induced SulA inhibits FtsZ division; negative division control lifted after repair"),
    "ecoli_nucleotide_biosynthesis": ("II", "end_product_feedback_inhibition", "Purine/pyrimidine biosynthesis feedback-inhibited by end-products (ATP/GTP, CTP/UTP) — corrected from pathway default"),
    "ecoli_sulfur_metabolism":       ("II", "cysB_end_product_feedback", "Cysteine biosynthesis: CysB activation with end-product (cysteine) feedback"),
    "ecoli_phosphate_regulation":    ("II", "phoBR_homeostasis", "PhoB/PhoR phosphate-starvation homeostasis"),
    "yeast_pka_pathway":             ("II", "camp_pka_neg_feedback", "Ras-cAMP-PKA growth signaling with PDE-mediated negative feedback"),
    "yeast_snf1_pathway":            ("II", "snf1_energy_homeostasis", "Snf1/AMPK energy-homeostasis negative feedback"),
    "yeast_tor_signaling":           ("II", "tor_nutrient_homeostasis", "TORC1 nutrient-sensing homeostatic feedback"),
    "yeast_nitrogen_metabolism":     ("II", "ncr_torc1_homeostasis", "Nitrogen catabolite repression via TORC1; homeostatic"),
    "yeast_gcn4_starvation":         ("II", "gcn2_eif2a_neg_feedback", "GAAC: Gcn2-eIF2α-Gcn4 amino-acid-starvation negative feedback"),

    # ── Class III — positive feedback / symmetry breaking (correction) ──
    "yeast_yeast_cell_polarity":     ("III", "cdc42_positive_feedback_polarity", "Cdc42 GTPase positive-feedback symmetry breaking (spontaneous polarization; Wedlich-Söldner et al.) — corrected from generic default"),
}

# ── Category default heuristic (MEDIUM confidence) ───────────────────────────
CATEGORY_DEFAULT = {
    "Developmental Decision": ("III", "developmental_bistable", "Developmental cell-fate decisions are typically bistable switches"),
    "Developmental Program":  ("III", "developmental_program", "Hierarchical developmental program with commitment"),
    "Cell Cycle":             ("IV",  "cell_cycle_oscillator", "Cell-cycle processes are delayed-feedback oscillators"),
    "Stress Response":        ("II",  "stress_neg_feedback", "Stress responses are predominantly homeostatic negative feedback"),
    "Metabolic Regulation":   ("II",  "metabolic_neg_feedback", "Regulatory metabolic circuits are predominantly negative feedback"),
    "Signal Transduction":    ("II",  "signaling_feedback", "Signaling pathways typically include adaptive negative feedback"),
    "Gene Regulation":        ("II",  "regulatory_feedback", "Regulatory loci typically carry repressive/feedback control"),
    # Execution / machinery categories default to feed-forward (Class I)
    "Metabolic Pathway":      ("I",   "metabolic_feed_forward", "Linear metabolic execution pathway, no regulatory feedback in chart"),
    "DNA Repair":             ("I",   "repair_feed_forward", "Repair execution pathway"),
    "DNA Replication":        ("I",   "replication_feed_forward", "Replication execution machinery"),
    "Protein Synthesis":      ("I",   "translation_feed_forward", "Translation execution machinery"),
    "Translation Machinery":  ("I",   "translation_feed_forward", "Translation machinery assembly"),
    "Gene Expression":        ("I",   "expression_feed_forward", "Transcription/expression execution machinery"),
    "Protein Transport":      ("I",   "transport_feed_forward", "Protein transport/sorting execution pathway"),
    "Protein Quality Control":("I",   "qc_feed_forward", "Protein quality-control execution pathway"),
    "Cell Wall Biogenesis":   ("I",   "biosynthesis_feed_forward", "Cell-wall biosynthesis execution pathway"),
    "Organelle Biology":      ("I",   "organelle_feed_forward", "Organelle biogenesis execution pathway"),
    "Nutrient Transport":     ("I",   "transport_feed_forward", "Nutrient transport execution pathway"),
    "Innate Immunity":        ("I",   "defense_feed_forward", "Defense execution pathway"),
    "Cell Division":          ("I",   "division_feed_forward", "Division execution machinery"),
    "Biological Process":     ("I",   "generic_feed_forward", "Generic execution pathway; no feedback asserted"),
}

CLASS_NAME = {
    "I": "Feed-forward cascade",
    "II": "Negative feedback (homeostatic)",
    "III": "Bistable switch / positive feedback",
    "IV": "Delayed negative feedback (oscillator)",
    "V": "Self-modifying chromatin / epigenetic",
}


def mermaid_has_cycle(mmd: str):
    """Detect a closed directed cycle in the Mermaid graph; return (bool, max_cycle_len)."""
    edges = []
    for line in mmd.split("\n"):
        s = line.strip()
        if not s or s.startswith(("%%", "style", "classDef", "linkStyle")):
            continue
        for m in re.finditer(r"([A-Za-z0-9_]+)\s*[-.]+>\|?[^|>]*\|?\s*([A-Za-z0-9_]+)", s):
            edges.append((m.group(1), m.group(2)))
    graph = defaultdict(list)
    nodes = set()
    for a, b in edges:
        graph[a].append(b)
        nodes.add(a)
        nodes.add(b)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = dict.fromkeys(nodes, WHITE)
    best = [0]
    found = [False]

    def dfs(u, stack):
        color[u] = GRAY
        for v in graph[u]:
            if color[v] == GRAY:
                found[0] = True
                if v in stack:
                    best[0] = max(best[0], len(stack) - stack.index(v))
            elif color[v] == WHITE:
                dfs(v, stack + [v])
        color[u] = BLACK

    import sys
    sys.setrecursionlimit(10000)
    for n in list(nodes):
        if color[n] == WHITE:
            dfs(n, [n])
    return found[0], best[0]


def classify(proc):
    pid = proc.get("id", "")
    category = proc.get("category", "")
    if pid in CURATED:
        cls, topo, rationale = CURATED[pid]
        return cls, topo, rationale, "curated_literature", "high", False
    if category in CATEGORY_DEFAULT:
        cls, topo, rationale = CATEGORY_DEFAULT[category]
        return cls, topo, rationale, "category_default", "medium", True
    return "I", "default_feed_forward", "No regulatory feedback asserted; default feed-forward", "default", "low", True


def main():
    files = sorted(glob.glob(PROCESS_GLOB, recursive=True))
    rows = []
    class_counts = defaultdict(int)
    conf_counts = defaultdict(int)
    review_count = 0

    for f in files:
        proc = json.load(open(f))
        # Ground-truth batches (synthetic biology, human curated) carry their own
        # authored class and must not be heuristically reclassified.
        if proc.get("groundTruth") or str(proc.get("id", "")).startswith(("synthetic_", "human_")):
            continue
        cls, topo, rationale, source, confidence, needs_review = classify(proc)
        has_cycle, cyc_len = mermaid_has_cycle(proc.get("mermaid", ""))
        rows.append({
            "process_id": proc.get("id", ""),
            "organism": proc.get("organism", ""),
            "category": proc.get("category", ""),
            "name": proc.get("name", ""),
            "circuit_class": cls,
            "class_name": CLASS_NAME[cls],
            "topology_type": topo,
            "rationale": rationale,
            "evidence_source": source,
            "confidence": confidence,
            "needs_review": "yes" if needs_review else "no",
            "has_graph_cycle": "yes" if has_cycle else "no",
            "not_gates": proc.get("notGates", 0),
        })
        class_counts[cls] += 1
        conf_counts[confidence] += 1
        review_count += int(needs_review)

    OUTPUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    fields = ["process_id", "organism", "category", "name", "circuit_class",
              "class_name", "topology_type", "rationale", "evidence_source",
              "confidence", "needs_review", "has_graph_cycle", "not_gates"]
    with open(OUTPUT_TSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    print(f"Classified {len(rows)} flowcharts -> {OUTPUT_TSV}")
    print("\nBy class:")
    for c in ["I", "II", "III", "IV", "V"]:
        print(f"  Class {c:<3} {CLASS_NAME[c]:<40} {class_counts[c]:3d}")
    print("\nBy confidence:")
    for c in ["high", "medium", "low"]:
        print(f"  {c:<8} {conf_counts[c]:3d}")
    print(f"\nneeds_review (for Krampis validation): {review_count}/{len(rows)}")


if __name__ == "__main__":
    main()
