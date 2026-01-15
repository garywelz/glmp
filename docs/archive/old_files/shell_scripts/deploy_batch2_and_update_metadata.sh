#!/bin/bash
# Deploys 6 new processes (Batch 2) and updates metadata to 70 total
# Run from: /home/gdubs/glmp

cd /home/gdubs/glmp

echo "=========================================="
echo "BATCH 2: Core Molecular Processes (6 new)"
echo "=========================================="
echo ""

# Fetch from GitHub
echo "Step 1: Fetching from GitHub..."
git fetch origin cursor/continue-frozen-deploy-glmp-conversation-0c90

# Create the 6 files
echo "Step 2: Creating 6 process files..."
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/ecoli/ecoli_translation_elongation.json > v2-development/processes/ecoli/ecoli_translation_elongation.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/ecoli/ecoli_translation_termination.json > v2-development/processes/ecoli/ecoli_translation_termination.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/ecoli/ecoli_transcription_elongation.json > v2-development/processes/ecoli/ecoli_transcription_elongation.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/ecoli/ecoli_transcription_termination.json > v2-development/processes/ecoli/ecoli_transcription_termination.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/ecoli/ecoli_homologous_recombination.json > v2-development/processes/ecoli/ecoli_homologous_recombination.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/ecoli/ecoli_cell_division.json > v2-development/processes/ecoli/ecoli_cell_division.json

echo "✅ Created 6 files!"
echo ""

# Upload to GCS
echo "Step 3: Uploading to GCS..."
gsutil -m cp \
  v2-development/processes/ecoli/ecoli_translation_elongation.json \
  v2-development/processes/ecoli/ecoli_translation_termination.json \
  v2-development/processes/ecoli/ecoli_transcription_elongation.json \
  v2-development/processes/ecoli/ecoli_transcription_termination.json \
  v2-development/processes/ecoli/ecoli_homologous_recombination.json \
  v2-development/processes/ecoli/ecoli_cell_division.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/

echo "✅ Uploaded 6 processes to GCS!"
echo ""

# Update metadata
echo "Step 4: Updating metadata.json..."

cat > /tmp/update_metadata_70.py << 'PYTHON'
import json

with open('v2-development/data/metadata.json', 'r') as f:
    metadata = json.load(f)

# Add 6 new processes
new_processes = [
    {
        "id": "ecoli_translation_elongation",
        "name": "Translation Elongation",
        "organism": "E. coli",
        "category": "Protein Synthesis",
        "description": "EF-Tu/EF-G-driven peptide chain extension with dual proofreading at tRNA selection and peptidyl transfer. Achieves 15-20 aa/sec with 10^-4 error rate.",
        "verified": True,
        "created": "2025-10-15",
        "citations": 4,
        "complexity": "detailed",
        "nodes": 78,
        "logicGates": {"or": 6, "and": 5, "total": 11}
    },
    {
        "id": "ecoli_translation_termination",
        "name": "Translation Termination and Ribosome Recycling",
        "organism": "E. coli",
        "category": "Protein Synthesis",
        "description": "RF1/RF2 recognize stop codons and catalyze peptide release. RF3-GTP promotes RF1/RF2 dissociation. RRF and EF-G split 70S into subunits for recycling.",
        "verified": True,
        "created": "2025-10-15",
        "citations": 4,
        "complexity": "detailed",
        "nodes": 72,
        "logicGates": {"or": 7, "and": 4, "total": 11}
    },
    {
        "id": "ecoli_transcription_elongation",
        "name": "Transcription Elongation",
        "organism": "E. coli",
        "category": "Gene Expression",
        "description": "RNAP processively synthesizes RNA at 40-50 nt/sec. GreA/GreB rescue backtracked complexes. NusG suppresses pausing. Coordinated with translation via coupling.",
        "verified": True,
        "created": "2025-10-15",
        "citations": 4,
        "complexity": "detailed",
        "nodes": 75,
        "logicGates": {"or": 8, "and": 4, "total": 12}
    },
    {
        "id": "ecoli_transcription_termination",
        "name": "Transcription Termination",
        "organism": "E. coli",
        "category": "Gene Expression",
        "description": "Intrinsic termination via RNA hairpin + U-tract destabilizes hybrid. Rho-dependent termination requires Rho helicase translocation and RNAP catching at pause sites.",
        "verified": True,
        "created": "2025-10-15",
        "citations": 4,
        "complexity": "detailed",
        "nodes": 68,
        "logicGates": {"or": 7, "and": 5, "total": 12}
    },
    {
        "id": "ecoli_homologous_recombination",
        "name": "Homologous Recombination",
        "organism": "E. coli",
        "category": "DNA Repair",
        "description": "RecBCD processes DSBs until Chi site, loads RecA on 3' overhang. RecA invades homolog forming D-loop. RuvABC or RecG resolve Holliday junctions.",
        "verified": True,
        "created": "2025-10-15",
        "citations": 4,
        "complexity": "detailed",
        "nodes": 82,
        "logicGates": {"or": 9, "and": 6, "total": 15}
    },
    {
        "id": "ecoli_cell_division",
        "name": "Cell Division and FtsZ Ring Assembly",
        "organism": "E. coli",
        "category": "Cell Division",
        "description": "FtsZ Z-ring assembles at midcell (Min system and nucleoid occlusion). Divisome recruits 30+ proteins hierarchically. Septal synthesis and constriction produce daughters.",
        "verified": True,
        "created": "2025-10-15",
        "citations": 4,
        "complexity": "detailed",
        "nodes": 79,
        "logicGates": {"or": 7, "and": 8, "total": 15}
    }
]

metadata["processes"].extend(new_processes)
metadata["totalProcesses"] = 70
metadata["lastUpdated"] = "2025-10-15"

# Update E. coli count: was 41, now 47
for org in metadata["organisms"]:
    if org["name"] == "E. coli":
        org["processCount"] = 47

# Update category counts
category_updates = {
    "Protein Synthesis": 3,  # was 1, +2 = 3
    "Gene Expression": 4,     # was 2, +2 = 4
    "DNA Repair": 5,          # was 4, +1 = 5
}

for cat in metadata["categories"]:
    if cat["name"] in category_updates:
        cat["processCount"] = category_updates[cat["name"]]

# Add Cell Division category if not exists
if not any(c["name"] == "Cell Division" for c in metadata["categories"]):
    metadata["categories"].append({"name": "Cell Division", "processCount": 1})

# Update statistics
metadata["statistics"]["totalCitations"] += 24  # 6 * 4
metadata["statistics"]["verifiedProcesses"] += 6
metadata["statistics"]["totalNodes"] += 454     # sum of nodes
metadata["statistics"]["totalOrGates"] += 44    # sum of OR gates
metadata["statistics"]["totalAndGates"] += 32   # sum of AND gates
metadata["statistics"]["totalLogicGates"] += 76 # sum of total gates
metadata["statistics"]["averageCitationsPerProcess"] = round(metadata["statistics"]["totalCitations"] / 70, 1)
metadata["statistics"]["totalCategories"] = len(metadata["categories"])

with open('v2-development/data/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("✅ Updated metadata.json:")
print(f"  Total processes: {metadata['totalProcesses']}")
print(f"  E. coli: {metadata['statistics']['totalNodes']} total nodes")
print(f"  Total logic gates: {metadata['statistics']['totalLogicGates']}")
PYTHON

python3 /tmp/update_metadata_70.py

echo ""
echo "Step 5: Uploading metadata to GCS..."
gsutil cp v2-development/data/metadata.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/data/metadata.json

echo ""
echo "=========================================="
echo "🎉 SUCCESS! Deployment Complete"
echo "=========================================="
echo ""
echo "New Processes Added:"
echo "  1. Translation Elongation (78 nodes, 11 gates)"
echo "  2. Translation Termination (72 nodes, 11 gates)"
echo "  3. Transcription Elongation (75 nodes, 12 gates)"
echo "  4. Transcription Termination (68 nodes, 12 gates)"
echo "  5. Homologous Recombination (82 nodes, 15 gates)"
echo "  6. Cell Division (79 nodes, 15 gates)"
echo ""
echo "Total Processes: 70 (was 64)"
echo "E. coli Processes: 47 (was 41)"
echo "Progress to 100: 70%"
echo ""
echo "Refresh viewer: https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html"
