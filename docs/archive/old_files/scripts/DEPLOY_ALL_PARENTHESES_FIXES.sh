#!/bin/bash
# Deploy all files fixed for parentheses issues

BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
BASE_DIR="processes_with_not_gates"

# Files that were fixed (from the scan results)
FIXED_FILES=(
    "ecoli/ecoli_protein_folding_chaperones.json"
    "ecoli/ecoli_envelope_stress_response.json"
    "ecoli/ecoli_e._coli_stringent_response.json"
    "ecoli/ecoli_iron_homeostasis.json"
    "ecoli/ecoli_e._coli_flagellar_assembly.json"
    "ecoli/ecoli_oxidative_stress_response.json"
    "ecoli/ecoli_phosphate_regulation.json"
    "ecoli/ecoli_cold_shock_response.json"
    "ecoli/ecoli_antibiotic_efflux_pumps.json"
    "yeast/yeast_yeast_cell_polarity.json"
    "yeast/yeast_yeast_er_associated_degradation.json"
    "yeast/yeast_protein_folding.json"
    "yeast/yeast_heat_shock_response.json"
    "yeast/yeast_yeast_vacuolar_protein_sorting.json"
    "yeast/yeast_yeast_peroxisome_biogenesis.json"
    "yeast/yeast_oxidative_stress_response.json"
    "yeast/yeast_osmotic_stress_response.json"
    "yeast/yeast_yeast_glycolysis_regulation.json"
)

echo "🚀 Deploying ${#FIXED_FILES[@]} fixed files..."
echo ""

COUNT=0
for file in "${FIXED_FILES[@]}"; do
    LOCAL_FILE="${BASE_DIR}/${file}"
    GCS_PATH="glmp-v2/processes/${file}"
    
    if [ -f "$LOCAL_FILE" ]; then
        COUNT=$((COUNT + 1))
        echo "[$COUNT/${#FIXED_FILES[@]}] Deploying ${file##*/}..."
        gsutil -h "Cache-Control:no-cache, no-store, must-revalidate, max-age=0" \
            cp "$LOCAL_FILE" "${BUCKET}/${GCS_PATH}"
    else
        echo "⚠️  File not found: $LOCAL_FILE"
    fi
done

echo ""
echo "✅ Deployed $COUNT files"
echo ""
echo "🧪 Test URLs:"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_antibiotic_efflux_pumps"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_phosphate_regulation"

