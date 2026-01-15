#!/usr/bin/env python3
"""
Process Gate Blueprint - Exact counts for all 100 processes
Based on desktop agent analysis and glmp-database-table.html
"""

PROCESS_GATES = {
    # Bacillus subtilis (3 processes)
    "bacillus_biofilm_formation": {"nodes": 71, "or": 10, "and": 5, "not": 2},
    "bacillus_competence_development": {"nodes": 53, "or": 3, "and": 2, "not": 1},
    "bacillus_sporulation_initiation": {"nodes": 64, "or": 4, "and": 2, "not": 0},
    
    # E. coli (64 processes)
    "ecoli_amino_acid_biosynthesis": {"nodes": 75, "or": 11, "and": 2, "not": 0},
    "ecoli_anaerobic_respiration": {"nodes": 76, "or": 9, "and": 5, "not": 3},
    "ecoli_antibiotic_efflux_pumps": {"nodes": 79, "or": 5, "and": 1, "not": 0},
    "ecoli_ara_operon": {"nodes": 38, "or": 2, "and": 2, "not": 2},
    "ecoli_arginine_biosynthesis": {"nodes": 52, "or": 2, "and": 1, "not": 1},
    "ecoli_base_excision_repair": {"nodes": 71, "or": 6, "and": 3, "not": 1},
    "ecoli_biofilm_formation": {"nodes": 62, "or": 6, "and": 4, "not": 1},
    "ecoli_catabolite_repression": {"nodes": 33, "or": 2, "and": 2, "not": 4},
    "ecoli_cell_division": {"nodes": 79, "or": 7, "and": 8, "not": 1},
    "ecoli_chemotaxis": {"nodes": 65, "or": 7, "and": 4, "not": 0},
    "ecoli_cold_shock_response": {"nodes": 84, "or": 4, "and": 1, "not": 2},
    "ecoli_dna_damage_checkpoint": {"nodes": 77, "or": 9, "and": 7, "not": 3},
    "ecoli_dna_replication_elongation": {"nodes": 68, "or": 4, "and": 3, "not": 0},
    "ecoli_dna_replication_initiation": {"nodes": 24, "or": 1, "and": 0, "not": 0},
    "ecoli_dna_replication_termination": {"nodes": 62, "or": 5, "and": 2, "not": 2},
    "ecoli_e._coli_acid_resistance": {"nodes": 60, "or": 13, "and": 1, "not": 4},
    "ecoli_e._coli_envelope_stress_response": {"nodes": 81, "or": 8, "and": 2, "not": 0},
    "ecoli_e._coli_flagellar_assembly": {"nodes": 88, "or": 12, "and": 4, "not": 0},
    "ecoli_e._coli_heat_shock_response": {"nodes": 10, "or": 1, "and": 1, "not": 0},
    "ecoli_e._coli_osmotic_stress_response": {"nodes": 87, "or": 12, "and": 2, "not": 0},
    "ecoli_e._coli_stringent_response": {"nodes": 64, "or": 14, "and": 0, "not": 0},
    "ecoli_e._coli_two_component_signaling": {"nodes": 20, "or": 8, "and": 0, "not": 3},
    "ecoli_fatty_acid_degradation": {"nodes": 68, "or": 7, "and": 3, "not": 5},
    "ecoli_fatty_acid_synthesis": {"nodes": 58, "or": 2, "and": 2, "not": 1},
    "ecoli_flagellar_assembly": {"nodes": 62, "or": 3, "and": 3, "not": 0},
    "ecoli_glycolysis": {"nodes": 74, "or": 8, "and": 3, "not": 0},
    "ecoli_heat_shock_response": {"nodes": 38, "or": 2, "and": 2, "not": 0},
    "ecoli_heavy_metal_resistance": {"nodes": 74, "or": 8, "and": 6, "not": 3},
    "ecoli_homologous_recombination": {"nodes": 82, "or": 9, "and": 6, "not": 0},
    "ecoli_iron_homeostasis": {"nodes": 72, "or": 6, "and": 1, "not": 1},
    "ecoli_lac_operon": {"nodes": 63, "or": 5, "and": 2, "not": 4},
    "ecoli_mal_regulon": {"nodes": 40, "or": 2, "and": 3, "not": 0},
    "ecoli_mismatch_repair": {"nodes": 76, "or": 6, "and": 5, "not": 0},
    "ecoli_nitrogen_assimilation": {"nodes": 43, "or": 2, "and": 3, "not": 0},
    "ecoli_nucleotide_biosynthesis": {"nodes": 72, "or": 9, "and": 3, "not": 0},
    "ecoli_nucleotide_excision_repair": {"nodes": 74, "or": 5, "and": 4, "not": 0},
    "ecoli_outer_membrane_assembly": {"nodes": 72, "or": 5, "and": 9, "not": 1},
    "ecoli_oxidative_stress_response": {"nodes": 83, "or": 11, "and": 4, "not": 1},
    "ecoli_pentose_phosphate_pathway": {"nodes": 66, "or": 9, "and": 2, "not": 2},
    "ecoli_periplasmic_stress": {"nodes": 71, "or": 10, "and": 4, "not": 1},
    "ecoli_phage_defense": {"nodes": 73, "or": 10, "and": 6, "not": 0},
    "ecoli_pho_regulon": {"nodes": 42, "or": 2, "and": 2, "not": 2},
    "ecoli_phosphate_regulation": {"nodes": 79, "or": 6, "and": 0, "not": 2},
    "ecoli_phosphate_transport": {"nodes": 58, "or": 4, "and": 6, "not": 1},
    "ecoli_protein_folding_chaperones": {"nodes": 78, "or": 22, "and": 1, "not": 0},
    "ecoli_e._coli_quorum_sensing": {"nodes": 58, "or": 5, "and": 3, "not": 0},
    "ecoli_ribosome_assembly": {"nodes": 52, "or": 3, "and": 2, "not": 0},
    "ecoli_rna_polymerase_recycling": {"nodes": 48, "or": 4, "and": 2, "not": 1},
    "ecoli_sigma_factor_competition": {"nodes": 62, "or": 6, "and": 2, "not": 1},
    "ecoli_e._coli_sos_response": {"nodes": 68, "or": 8, "and": 4, "not": 1},
    "ecoli_starvation_response": {"nodes": 81, "or": 13, "and": 3, "not": 1},
    "ecoli_stringent_response": {"nodes": 40, "or": 2, "and": 2, "not": 0},
    "ecoli_sulfur_metabolism": {"nodes": 70, "or": 8, "and": 3, "not": 3},
    "ecoli_tca_cycle": {"nodes": 79, "or": 7, "and": 4, "not": 0},
    "ecoli_transcription_elongation": {"nodes": 75, "or": 8, "and": 4, "not": 0},
    "ecoli_transcription_regulation": {"nodes": 25, "or": 2, "and": 0, "not": 4},
    "ecoli_transcription_termination": {"nodes": 68, "or": 7, "and": 5, "not": 2},
    "ecoli_translation_elongation": {"nodes": 78, "or": 6, "and": 5, "not": 0},
    "ecoli_translation_initiation": {"nodes": 69, "or": 5, "and": 4, "not": 3},
    "ecoli_translation_termination": {"nodes": 72, "or": 7, "and": 4, "not": 0},
    "ecoli_trp_operon": {"nodes": 45, "or": 3, "and": 2, "not": 3},
    "ecoli_tryptophan_biosynthesis": {"nodes": 64, "or": 4, "and": 5, "not": 2},
    "ecoli_two_component_signaling": {"nodes": 35, "or": 2, "and": 1, "not": 3},
    "ecoli_type_iii_secretion": {"nodes": 60, "or": 6, "and": 3, "not": 2},
    
    # S. cerevisiae (33 processes)
    "yeast_autophagy": {"nodes": 70, "or": 7, "and": 5, "not": 4},
    "yeast_cell_cycle_control": {"nodes": 30, "or": 3, "and": 0, "not": 0},
    "yeast_cell_wall_integrity": {"nodes": 87, "or": 8, "and": 0, "not": 2},
    "yeast_chromatin_silencing": {"nodes": 68, "or": 4, "and": 10, "not": 3},
    "yeast_er_stress_response": {"nodes": 74, "or": 6, "and": 8, "not": 0},
    "yeast_gal_regulation": {"nodes": 58, "or": 3, "and": 2, "not": 5},
    "yeast_gcn4_starvation": {"nodes": 71, "or": 7, "and": 4, "not": 1},
    "yeast_glycolysis": {"nodes": 56, "or": 3, "and": 2, "not": 0},
    "yeast_heat_shock_response": {"nodes": 73, "or": 12, "and": 0, "not": 0},
    "yeast_hog_pathway": {"nodes": 91, "or": 5, "and": 11, "not": 6},
    "yeast_mapk_mating": {"nodes": 84, "or": 4, "and": 10, "not": 3},
    "yeast_mating_response": {"nodes": 75, "or": 8, "and": 6, "not": 1},
    "yeast_mating_type_switching": {"nodes": 55, "or": 2, "and": 3, "not": 2},
    "yeast_meiosis_regulation": {"nodes": 57, "or": 4, "and": 3, "not": 2},
    "yeast_mitochondrial_biogenesis": {"nodes": 73, "or": 5, "and": 8, "not": 1},
    "yeast_mitochondrial_protein_import": {"nodes": 72, "or": 8, "and": 5, "not": 0},
    "yeast_nitrogen_metabolism": {"nodes": 67, "or": 9, "and": 4, "not": 2},
    "yeast_ner_pathway": {"nodes": 55, "or": 4, "and": 3, "not": 0},
    "yeast_osmotic_stress_response": {"nodes": 77, "or": 3, "and": 0, "not": 1},
    "yeast_oxidative_stress_response": {"nodes": 67, "or": 12, "and": 1, "not": 0},
    "yeast_pka_pathway": {"nodes": 77, "or": 6, "and": 8, "not": 6},
    "yeast_protein_folding": {"nodes": 72, "or": 22, "and": 0, "not": 0},
    "yeast_rna_splicing": {"nodes": 82, "or": 3, "and": 12, "not": 0},
    "yeast_snf1_pathway": {"nodes": 69, "or": 5, "and": 7, "not": 6},
    "yeast_tor_signaling": {"nodes": 86, "or": 6, "and": 9, "not": 8},
    "yeast_ubiquitin_proteasome": {"nodes": 58, "or": 5, "and": 3, "not": 0},
    "yeast_unfolded_protein_response": {"nodes": 68, "or": 7, "and": 5, "not": 2},
    "yeast_vesicle_trafficking": {"nodes": 79, "or": 4, "and": 13, "not": 2},
    "yeast_yeast_cell_polarity": {"nodes": 65, "or": 14, "and": 0, "not": 0},
    "yeast_yeast_er_associated_degradation": {"nodes": 54, "or": 3, "and": 5, "not": 0},
    "yeast_yeast_glycolysis_regulation": {"nodes": 67, "or": 2, "and": 1, "not": 0},
    "yeast_yeast_peroxisome_biogenesis": {"nodes": 79, "or": 12, "and": 0, "not": 0},
    "yeast_yeast_vacuolar_protein_sorting": {"nodes": 70, "or": 6, "and": 1, "not": 0},
}

# Validation
total_nodes = sum(p["nodes"] for p in PROCESS_GATES.values())
total_or = sum(p["or"] for p in PROCESS_GATES.values())
total_and = sum(p["and"] for p in PROCESS_GATES.values())
total_not = sum(p["not"] for p in PROCESS_GATES.values())

print(f"Blueprint Summary:")
print(f"  Total processes: {len(PROCESS_GATES)}")
print(f"  Total nodes: {total_nodes}")
print(f"  OR gates: {total_or} ({total_or/total_nodes*100:.1f}%)")
print(f"  AND gates: {total_and} ({total_and/total_nodes*100:.1f}%)")
print(f"  NOT gates: {total_not} ({total_not/total_nodes*100:.1f}%)")
print(f"  Logic gates: {total_or + total_and + total_not} ({(total_or + total_and + total_not)/total_nodes*100:.1f}%)")
print(f"  Sequential: {total_nodes - total_or - total_and - total_not} ({(total_nodes - total_or - total_and - total_not)/total_nodes*100:.1f}%)")
print()
print(f"  OR:AND ratio: {total_or/total_and:.2f}:1")
print()
print(f"100:12:6:2 verification:")
sequential = total_nodes - total_or - total_and - total_not
print(f"  For every 100 sequential nodes:")
print(f"    OR gates: {total_or/sequential*100:.1f}")
print(f"    AND gates: {total_and/sequential*100:.1f}")
print(f"    NOT gates: {total_not/sequential*100:.1f}")
