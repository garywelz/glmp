# E. coli Files Standardization Plan

## Issues Identified:
1. **Missing sliders** - Some files don't have working sliders
2. **Missing charts** - Some files lack expected Mermaid diagrams
3. **Incorrect batch numbers** - Headers/content don't match filenames
4. **Inconsistent formatting** - Different slider implementations

## Standardization Requirements:
Each file should have:
- ✅ **8 biological processes** per file
- ✅ **5 detail levels** per process (sliders 1-5)
- ✅ **Working JavaScript** with proper `allProcesses` object
- ✅ **Correct batch number** matching filename
- ✅ **Canonical colors** (Red, Yellow, Green, Blue, Violet)
- ✅ **Diamond shapes** for OR/AND logic gates
- ✅ **Anchor tags** for direct process linking
- ✅ **Consistent HTML structure**

## Files to Check (21 total):
1. ecoli_batch01_dna_replication_repair.html
2. ecoli_batch02_cell_division_segregation.html
3. ecoli_batch03_translation_protein_synthesis.html
4. ecoli_batch04_protein_synthesis_quality.html
5. ecoli_batch05_cell_division.html
6. ecoli_batch06_respiration_energy.html
7. ecoli_batch07_quorum_sensing.html
8. ecoli_batch08_biofilm_formation.html
9. ecoli_batch09_antibiotic_resistance.html
10. ecoli_batch10_evolutionary_adaptation.html
11. ecoli_batch11_phage_defense.html
12. ecoli_batch12_environmental_adaptation.html
13. ecoli_batch13_specialized_metabolism.html
14. ecoli_batch14_transcription_regulation.html
15. ecoli_batch15_translation_protein_synthesis.html
16. ecoli_batch16_protein_synthesis_quality.html
17. ecoli_batch17_central_metabolism.html
18. ecoli_batch18_stress_response.html
19. ecoli_batch19_transport_membrane.html
20. ecoli_batch20_motility_chemotaxis.html
21. ecoli_batch21_iron_homeostasis.html

## Action Plan:
1. **Audit Phase**: Check each file for issues
2. **Template Creation**: Create standard template with working sliders
3. **Batch Fix**: Apply template to all files systematically
4. **Verification**: Test sliders on each file
5. **Re-upload**: Replace problematic files on Huggingface

## Standard Template Features:
- Proper HTML5 structure
- Working Mermaid.js integration
- 5-level slider functionality
- Consistent CSS styling
- Proper JavaScript error handling
- Canonical color scheme
- Process anchor navigation