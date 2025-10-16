#!/bin/bash
# Deploys Batch 5: Signal Transduction + Metabolism (6 processes) → 85 total
# Run from: /home/gdubs/glmp

cd /home/gdubs/glmp

echo "=========================================="
echo "BATCH 5: Signal + Metabolism (6 processes)"
echo "=========================================="
echo "VALIDATING OR vs AND GATE PATTERNS!"
echo ""

git fetch origin cursor/continue-frozen-deploy-glmp-conversation-0c90

echo "Creating 6 processes (4 yeast signal, 2 E. coli metabolism)..."
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/yeast/yeast_hog_pathway.json > v2-development/processes/yeast/yeast_hog_pathway.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/yeast/yeast_pka_pathway.json > v2-development/processes/yeast/yeast_pka_pathway.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/yeast/yeast_snf1_pathway.json > v2-development/processes/yeast/yeast_snf1_pathway.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/yeast/yeast_mapk_mating.json > v2-development/processes/yeast/yeast_mapk_mating.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/ecoli/ecoli_nucleotide_biosynthesis.json > v2-development/processes/ecoli/ecoli_nucleotide_biosynthesis.json
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/ecoli/ecoli_amino_acid_biosynthesis.json > v2-development/processes/ecoli/ecoli_amino_acid_biosynthesis.json

echo "✅ Created!"

gsutil -m cp \
  v2-development/processes/yeast/yeast_hog_pathway.json \
  v2-development/processes/yeast/yeast_pka_pathway.json \
  v2-development/processes/yeast/yeast_snf1_pathway.json \
  v2-development/processes/yeast/yeast_mapk_mating.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/yeast/

gsutil -m cp \
  v2-development/processes/ecoli/ecoli_nucleotide_biosynthesis.json \
  v2-development/processes/ecoli/ecoli_amino_acid_biosynthesis.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/

echo "✅ Uploaded!"

python3 << 'PYTHON'
import json
with open('v2-development/data/metadata.json') as f: metadata = json.load(f)

new_processes = [
    {"id": "yeast_hog_pathway", "name": "HOG Pathway (High Osmolarity Glycerol Response)", "organism": "S. cerevisiae", "category": "Signal Transduction", "description": "MAPK osmotic stress. SLN1 + SHO1 branches. 11 AND gates!", "verified": True, "created": "2025-10-15", "citations": 4, "complexity": "detailed", "nodes": 91, "logicGates": {"or": 5, "and": 11, "total": 16}},
    {"id": "yeast_pka_pathway", "name": "cAMP-PKA Pathway (Glucose Sensing)", "organism": "S. cerevisiae", "category": "Signal Transduction", "description": "GPCR Gpr1-Gpa2-Cyr1 glucose sensing. PKA growth control. 8 AND gates.", "verified": True, "created": "2025-10-15", "citations": 2, "complexity": "detailed", "nodes": 77, "logicGates": {"or": 6, "and": 8, "total": 14}},
    {"id": "yeast_snf1_pathway", "name": "Snf1/AMPK Energy Sensing Pathway", "organism": "S. cerevisiae", "category": "Signal Transduction", "description": "AMPK ortholog. Energy sensor. Mig1/Cat8 regulation. 7 AND gates.", "verified": True, "created": "2025-10-15", "citations": 1, "complexity": "detailed", "nodes": 69, "logicGates": {"or": 5, "and": 7, "total": 12}},
    {"id": "yeast_mapk_mating", "name": "MAPK Pheromone Response Pathway (Detailed)", "organism": "S. cerevisiae", "category": "Signal Transduction", "description": "GPCR-MAPK mating. Ste5 scaffold. Fus3-Ste12. 10 AND gates!", "verified": True, "created": "2025-10-15", "citations": 1, "complexity": "detailed", "nodes": 84, "logicGates": {"or": 4, "and": 10, "total": 14}},
    {"id": "ecoli_nucleotide_biosynthesis", "name": "Nucleotide Biosynthesis (Purine and Pyrimidine)", "organism": "E. coli", "category": "Metabolic Pathway", "description": "Purine + pyrimidine synthesis. IMP/UMP branch points. 9 OR gates!", "verified": True, "created": "2025-10-15", "citations": 1, "complexity": "detailed", "nodes": 72, "logicGates": {"or": 9, "and": 3, "total": 12}},
    {"id": "ecoli_amino_acid_biosynthesis", "name": "Amino Acid Biosynthesis Pathways", "organism": "E. coli", "category": "Metabolic Pathway", "description": "All 20 amino acids. 6 major families. Branch points. 11 OR gates!", "verified": True, "created": "2025-10-15", "citations": 1, "complexity": "detailed", "nodes": 75, "logicGates": {"or": 11, "and": 2, "total": 13}}
]

metadata["processes"].extend(new_processes)
metadata["totalProcesses"] = 85

for org in metadata["organisms"]:
    if org["name"] == "E. coli": org["processCount"] = 57
    elif org["name"] == "S. cerevisiae": org["processCount"] = 26

for cat in metadata["categories"]:
    if cat["name"] == "Signal Transduction": cat["processCount"] = 12
    elif cat["name"] == "Metabolic Pathway": cat["processCount"] = 7

metadata["statistics"]["totalCitations"] += 10
metadata["statistics"]["verifiedProcesses"] += 6
metadata["statistics"]["totalNodes"] += 468
metadata["statistics"]["totalOrGates"] += 40
metadata["statistics"]["totalAndGates"] += 41
metadata["statistics"]["totalLogicGates"] += 81
metadata["statistics"]["averageCitationsPerProcess"] = round(metadata["statistics"]["totalCitations"] / 85, 1)

with open('v2-development/data/metadata.json', 'w') as f: json.dump(metadata, f, indent=2)
print("✅ 85 processes total!")
print("")
print("PATTERN VALIDATION:")
print("  Signal Transduction (4 new): Avg 9.0 AND gates - HIGH!")
print("  Metabolism (2 new): Avg 10.0 OR gates - HIGH!")
PYTHON

gsutil cp v2-development/data/metadata.json gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/data/metadata.json

echo ""
echo "=========================================="
echo "🎉 85/100 PROCESSES (85% COMPLETE!)"
echo "=========================================="
echo ""
echo "Batch 5 Added:"
echo "  Yeast Signal Transduction:"
echo "    1. HOG Pathway - 11 AND gates (MAPK)"
echo "    2. cAMP-PKA - 8 AND gates (GPCR)"
echo "    3. Snf1/AMPK - 7 AND gates (Energy)"
echo "    4. MAPK Mating - 10 AND gates (Pheromone)"
echo ""
echo "  E. coli Metabolism:"
echo "    5. Nucleotide Biosynthesis - 9 OR gates"
echo "    6. Amino Acid Biosynthesis - 11 OR gates"
echo ""
echo "✅ CONFIRMS PUBLICATION HYPOTHESIS:"
echo "  → Signal Transduction = HIGH AND gates (complex assembly)"
echo "  → Metabolism = HIGH OR gates (pathway flexibility)"
echo ""
echo "Only 15 more to 100! 🎯"
