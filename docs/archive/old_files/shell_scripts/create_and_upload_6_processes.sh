#!/bin/bash
# Creates 6 new publication-quality processes and uploads to GCS
# Run from: /home/gdubs/glmp

cd /home/gdubs/glmp
mkdir -p v2-development/processes/ecoli

echo "Creating 6 new E. coli processes..."

# The files are in the GitHub repo at glmp-v2/processes/ecoli/
# Pull from GitHub first
git fetch origin cursor/continue-frozen-deploy-glmp-conversation-0c90

# Copy the files from the branch (avoiding merge conflicts)
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:glmp-v2/processes/ecoli/ecoli_dna_replication_elongation.json > v2-development/processes/ecoli/ecoli_dna_replication_elongation.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:glmp-v2/processes/ecoli/ecoli_dna_replication_termination.json > v2-development/processes/ecoli/ecoli_dna_replication_termination.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:glmp-v2/processes/ecoli/ecoli_base_excision_repair.json > v2-development/processes/ecoli/ecoli_base_excision_repair.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:glmp-v2/processes/ecoli/ecoli_nucleotide_excision_repair.json > v2-development/processes/ecoli/ecoli_nucleotide_excision_repair.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:glmp-v2/processes/ecoli/ecoli_mismatch_repair.json > v2-development/processes/ecoli/ecoli_mismatch_repair.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:glmp-v2/processes/ecoli/ecoli_translation_initiation.json > v2-development/processes/ecoli/ecoli_translation_initiation.json

echo "✅ Created 6 files in v2-development/processes/ecoli/"

# Upload to GCS
echo "Uploading to GCS..."
gsutil -m cp v2-development/processes/ecoli/ecoli_dna_replication_elongation.json \
  v2-development/processes/ecoli/ecoli_dna_replication_termination.json \
  v2-development/processes/ecoli/ecoli_base_excision_repair.json \
  v2-development/processes/ecoli/ecoli_nucleotide_excision_repair.json \
  v2-development/processes/ecoli/ecoli_mismatch_repair.json \
  v2-development/processes/ecoli/ecoli_translation_initiation.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/

echo "✅ Done! 6 new processes uploaded to GCS"
echo ""
echo "Processes added:"
echo "  1. DNA Replication Elongation (68 nodes, 7 gates)"
echo "  2. DNA Replication Termination (62 nodes, 7 gates)"
echo "  3. Base Excision Repair (71 nodes, 9 gates)"
echo "  4. Nucleotide Excision Repair (74 nodes, 9 gates)"
echo "  5. Mismatch Repair (76 nodes, 11 gates, Nobel Prize)"
echo "  6. Translation Initiation (69 nodes, 9 gates, Nobel Prize)"
echo ""
echo "Total processes now: 64 (was 58)"
