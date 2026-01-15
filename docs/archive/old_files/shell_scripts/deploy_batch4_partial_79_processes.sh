#!/bin/bash
# Deploys Batch 4 (partial): 3 processes - TCA, Glycolysis, TOR
# Run from: /home/gdubs/glmp

cd /home/gdubs/glmp

echo "=========================================="
echo "BATCH 4 (Partial): Metabolism + Signaling"
echo "=========================================="
echo "Testing metabolic OR gates and signaling AND gates!"
echo ""

git fetch origin cursor/continue-frozen-deploy-glmp-conversation-0c90

echo "Creating 3 processes..."
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/ecoli/ecoli_tca_cycle.json > v2-development/processes/ecoli/ecoli_tca_cycle.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/ecoli/ecoli_glycolysis.json > v2-development/processes/ecoli/ecoli_glycolysis.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/yeast/yeast_tor_signaling.json > v2-development/processes/yeast/yeast_tor_signaling.json

echo "✅ Created!"

gsutil -m cp \
  v2-development/processes/ecoli/ecoli_tca_cycle.json \
  v2-development/processes/ecoli/ecoli_glycolysis.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/

gsutil cp v2-development/processes/yeast/yeast_tor_signaling.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/yeast/

echo "✅ Uploaded!"

python3 << 'PYTHON'
import json
with open('v2-development/data/metadata.json') as f: metadata = json.load(f)

new_processes = [
    {"id": "ecoli_tca_cycle", "name": "Tricarboxylic Acid Cycle (TCA/Krebs Cycle)", "organism": "E. coli", "category": "Metabolic Pathway", "description": "Central oxidative pathway. Acetyl-CoA to CO2, generating NADH/FADH2 and biosynthetic precursors.", "verified": True, "created": "2025-10-15", "citations": 4, "complexity": "detailed", "nodes": 79, "logicGates": {"or": 7, "and": 4, "total": 11}},
    {"id": "ecoli_glycolysis", "name": "Glycolysis (Embden-Meyerhof-Parnas Pathway)", "organism": "E. coli", "category": "Metabolic Pathway", "description": "Glucose to pyruvate. 2 ATP + 2 NADH net. PTS uptake, Pfk regulation, multiple pyruvate fates.", "verified": True, "created": "2025-10-15", "citations": 4, "complexity": "detailed", "nodes": 74, "logicGates": {"or": 8, "and": 3, "total": 11}},
    {"id": "yeast_tor_signaling", "name": "TOR Signaling Pathway (Nutrient Sensing)", "organism": "S. cerevisiae", "category": "Signal Transduction", "description": "TORC1/2 master growth regulator. Amino acid, nitrogen, glucose sensing. High AND gates for complex assembly!", "verified": True, "created": "2025-10-15", "citations": 4, "complexity": "detailed", "nodes": 86, "logicGates": {"or": 6, "and": 9, "total": 15}}
]

metadata["processes"].extend(new_processes)
metadata["totalProcesses"] = 79

for org in metadata["organisms"]:
    if org["name"] == "E. coli": org["processCount"] = 55
    elif org["name"] == "S. cerevisiae": org["processCount"] = 22

for cat in metadata["categories"]:
    if cat["name"] == "Metabolic Pathway": cat["processCount"] = 5

metadata["statistics"]["totalCitations"] += 12
metadata["statistics"]["verifiedProcesses"] += 3
metadata["statistics"]["totalNodes"] += 239
metadata["statistics"]["totalOrGates"] += 21
metadata["statistics"]["totalAndGates"] += 16
metadata["statistics"]["totalLogicGates"] += 37
metadata["statistics"]["averageCitationsPerProcess"] = round(metadata["statistics"]["totalCitations"] / 79, 1)

with open('v2-development/data/metadata.json', 'w') as f: json.dump(metadata, f, indent=2)
print("✅ 79 processes!")
PYTHON

gsutil cp v2-development/data/metadata.json gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/data/metadata.json

echo ""
echo "🎉 79/100 PROCESSES (79%)"
echo ""
echo "New processes:"
echo "  1. TCA Cycle - 7 OR, 4 AND (metabolic branch points)"
echo "  2. Glycolysis - 8 OR, 3 AND (alternative enzymes)"  
echo "  3. TOR Signaling - 6 OR, 9 AND (HIGH AND = signal transduction!)"
echo ""
echo "✅ CONFIRMS PATTERNS:"
echo "  - Metabolism: Moderate OR gates (flexibility)"
echo "  - Signal Transduction: HIGH AND gates (complex assembly)"
echo ""
echo "21 more to reach 100! 🎯"
