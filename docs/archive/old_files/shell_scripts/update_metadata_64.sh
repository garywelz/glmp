#!/bin/bash
# Updates metadata.json to include 6 new processes
# Run from: /home/gdubs/glmp

cd /home/gdubs/glmp

# Create Python script to update metadata
cat > /tmp/update_metadata.py << 'PYTHON_SCRIPT'
import json

# Load current metadata
with open('v2-development/data/metadata.json', 'r') as f:
    metadata = json.load(f)

# Add 6 new processes
new_processes = [
    {
        "id": "ecoli_dna_replication_elongation",
        "name": "DNA Replication Elongation",
        "organism": "E. coli",
        "category": "DNA Replication",
        "description": "DNA replication elongation in E. coli is performed by the highly processive DNA polymerase III holoenzyme. The replisome coordinates synthesis on leading and lagging strands with continuous proofreading.",
        "verified": True,
        "created": "2025-10-15",
        "citations": 4,
        "complexity": "detailed",
        "nodes": 68,
        "logicGates": {"or": 4, "and": 3, "total": 7}
    },
    {
        "id": "ecoli_dna_replication_termination",
        "name": "DNA Replication Termination",
        "organism": "E. coli",
        "category": "DNA Replication",
        "description": "DNA replication termination occurs at ter sites bound by Tus protein. Converging forks are arrested, replisomes disassembled, DNA decatenated by topoisomerase IV, and dimers resolved.",
        "verified": True,
        "created": "2025-10-15",
        "citations": 4,
        "complexity": "detailed",
        "nodes": 62,
        "logicGates": {"or": 5, "and": 2, "total": 7}
    },
    {
        "id": "ecoli_base_excision_repair",
        "name": "Base Excision Repair (BER)",
        "organism": "E. coli",
        "category": "DNA Repair",
        "description": "BER corrects non-bulky base lesions via DNA glycosylases, AP endonucleases, DNA polymerase I, and ligase. Includes both short-patch and long-patch repair mechanisms.",
        "verified": True,
        "created": "2025-10-15",
        "citations": 4,
        "complexity": "detailed",
        "nodes": 71,
        "logicGates": {"or": 6, "and": 3, "total": 9}
    },
    {
        "id": "ecoli_nucleotide_excision_repair",
        "name": "Nucleotide Excision Repair (NER)",
        "organism": "E. coli",
        "category": "DNA Repair",
        "description": "NER removes bulky DNA lesions via UvrABC system. Includes damage recognition, dual incision, 12-13 nt excision, gap filling, and ligation. Critical for UV survival.",
        "verified": True,
        "created": "2025-10-15",
        "citations": 4,
        "complexity": "detailed",
        "nodes": 74,
        "logicGates": {"or": 5, "and": 4, "total": 9}
    },
    {
        "id": "ecoli_mismatch_repair",
        "name": "DNA Mismatch Repair (MMR)",
        "organism": "E. coli",
        "category": "DNA Repair",
        "description": "MMR corrects replication errors via MutHLS system. Strand discrimination uses Dam methylation. Increases fidelity 1000-fold. Nobel Prize-winning pathway paradigm.",
        "verified": True,
        "created": "2025-10-15",
        "citations": 4,
        "complexity": "detailed",
        "nodes": 76,
        "logicGates": {"or": 6, "and": 5, "total": 11}
    },
    {
        "id": "ecoli_translation_initiation",
        "name": "Translation Initiation",
        "organism": "E. coli",
        "category": "Protein Synthesis",
        "description": "Translation initiation assembles 70S ribosome on mRNA via IF1/IF2/IF3, Shine-Dalgarno recognition, and fMet-tRNA recruitment. Multiple fidelity checkpoints ensure correct start.",
        "verified": True,
        "created": "2025-10-15",
        "citations": 4,
        "complexity": "detailed",
        "nodes": 69,
        "logicGates": {"or": 5, "and": 4, "total": 9}
    }
]

# Append to processes list
metadata["processes"].extend(new_processes)

# Update counts
metadata["totalProcesses"] = 64
metadata["lastUpdated"] = "2025-10-15"

# Update organism count for E. coli
for org in metadata["organisms"]:
    if org["name"] == "E. coli":
        org["processCount"] = 41  # was 35, now +6 = 41

# Update category counts
category_updates = {
    "DNA Replication": 3,  # was 1, +2 = 3
    "DNA Repair": 4,  # was 1, +3 = 4
    "Protein Synthesis": 1  # new category
}

for cat in metadata["categories"]:
    if cat["name"] in category_updates:
        cat["processCount"] = category_updates[cat["name"]]

# Add Protein Synthesis category if not exists
if not any(c["name"] == "Protein Synthesis" for c in metadata["categories"]):
    metadata["categories"].append({
        "name": "Protein Synthesis",
        "processCount": 1
    })

# Update statistics
new_nodes = 68 + 62 + 71 + 74 + 76 + 69  # = 420
new_or_gates = 4 + 5 + 6 + 5 + 6 + 5  # = 31
new_and_gates = 3 + 2 + 3 + 4 + 5 + 4  # = 21
new_total_gates = 7 + 7 + 9 + 9 + 11 + 9  # = 52

metadata["statistics"]["totalCitations"] += 24  # 6 processes * 4 citations
metadata["statistics"]["verifiedProcesses"] += 6
metadata["statistics"]["totalNodes"] += new_nodes
metadata["statistics"]["totalOrGates"] += new_or_gates
metadata["statistics"]["totalAndGates"] += new_and_gates
metadata["statistics"]["totalLogicGates"] += new_total_gates
metadata["statistics"]["averageCitationsPerProcess"] = round(
    metadata["statistics"]["totalCitations"] / metadata["totalProcesses"], 1
)
metadata["statistics"]["totalCategories"] = len(metadata["categories"])

# Save updated metadata
with open('v2-development/data/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("✅ Updated metadata.json:")
print(f"  Total processes: {metadata['totalProcesses']}")
print(f"  E. coli: 41")
print(f"  Total nodes: {metadata['statistics']['totalNodes']}")
print(f"  Total logic gates: {metadata['statistics']['totalLogicGates']}")
PYTHON_SCRIPT

# Run the Python script
python3 /tmp/update_metadata.py

# Upload to GCS
echo "Uploading updated metadata to GCS..."
gsutil cp v2-development/data/metadata.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/data/metadata.json

echo ""
echo "🎉 SUCCESS! Metadata updated and deployed."
echo "Now refresh the viewer to see 64 processes!"
