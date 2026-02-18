# E. coli File Renumbering Plan

## Current Problem
Multiple files have the same batch numbers but different topics, creating confusion and broken links.

## New Sequential Numbering Scheme

### Core Central Dogma (Batches 01-05)
1. ✅ `ecoli_batch01_dna_replication_repair.html` (DONE - Interactive)
2. ✅ `ecoli_batch02_transcription_regulation.html` (DONE - Interactive)
3. 📋 `ecoli_batch03_translation_protein_synthesis.html` (EXISTS - Need Interactive)
4. 📋 `ecoli_batch04_metabolic_pathways.html` (EXISTS - Need Interactive)
5. 📋 `ecoli_batch05_central_metabolism.html` (EXISTS - Need Interactive)

### Cell Structure & Division (Batches 06-10)
6. 📋 `ecoli_batch06_cell_division_segregation.html` (RENAME from batch02_cell_division)
7. 📋 `ecoli_batch07_transport_membrane.html` (EXISTS - Need Interactive)
8. 📋 `ecoli_batch08_motility_chemotaxis.html` (EXISTS - Need Interactive)
9. 📋 `ecoli_batch09_respiration_energy.html` (RENAME from batch06_respiration)
10. 📋 `ecoli_batch10_protein_synthesis_quality.html` (RENAME from batch04_protein_quality)

### Regulation & Control (Batches 11-15)
11. 📋 `ecoli_batch11_gene_regulation_transcription.html` (RENAME from batch03_gene_regulation)
12. 📋 `ecoli_batch12_stress_response.html` (RENAME from batch06_stress_response)
13. 📋 `ecoli_batch13_environmental_adaptation.html` (EXISTS - Need Interactive)
14. 📋 `ecoli_batch14_specialized_metabolism.html` (EXISTS - Need Interactive)
15. 📋 `ecoli_batch15_iron_homeostasis.html` (RENAME from batch10_iron_homeostasis)

### Advanced Systems (Batches 16-25)
16. 📋 `ecoli_batch16_antibiotic_resistance.html` (RENAME from batch09_antibiotic)
17. 📋 `ecoli_batch17_biofilm_formation.html` (RENAME from batch08_biofilm)
18. 📋 `ecoli_batch18_phage_defense.html` (RENAME from batch12_phage_defense)
19. 📋 `ecoli_batch19_quorum_sensing.html` (RENAME from batch07_quorum_sensing)
20. 📋 `ecoli_batch20_evolutionary_adaptation.html` (RENAME from batch10_evolutionary)
21. 📋 `ecoli_batch21_cell_division_alt.html` (RENAME from batch05_cell_division)
22. 📋 `ecoli_batch22_biofilm_formation_alt.html` (RENAME from batch11_biofilm)
23. 📋 `ecoli_batch23_stress_response_alt.html` (RENAME from batch09_stress_response)
24. 📋 `ecoli_batch24_quorum_sensing_alt.html` (RENAME from batch15_quorum_sensing)

### Special Collections:
- 📋 `ecoli_lac_operon_beta_galactosidase.html` (RENAME from ecoli_beta_galactosidase_lac_operon)
- 📋 `ecoli_overview_top_10_processes.html` (RENAME from ecoli_10_processes)

## Implementation Strategy

### Phase 1: Fix Current Files (Priority)
1. ✅ Fix slider issue in batch02_transcription_regulation.html
2. 📋 Continue with clean files (batch03, batch04, batch05)
3. 📋 Convert to interactive versions

### Phase 2: Rename Duplicates (Later)
1. 📋 Rename all duplicate files according to new scheme
2. 📋 Update database URLs
3. 📋 Convert renamed files to interactive

### Phase 3: Database Coordination
1. 📋 Provide complete URL mapping for database updates
2. 📋 Test all anchor links
3. 📋 Verify no broken links

## Immediate Action: Continue with Clean Files

To avoid confusion, let's continue with the files that don't have naming conflicts:
- `ecoli_batch03_translation_protein_synthesis.html`
- `ecoli_batch04_metabolic_pathways.html` 
- `ecoli_batch05_central_metabolism.html`

Then address the renaming later as a separate task.