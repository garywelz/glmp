#!/bin/bash

echo "=========================================="
echo "🎨 DEPLOYING 25 COLOR-FIXED PROCESSES"
echo "=========================================="
echo ""
echo "This will upload all 25 processes with corrected colors:"
echo "  • All style statements now include text colors"
echo "  • Red/Green/Blue/Orange/Lavender/Violet → white text"
echo "  • Yellow → black text (better contrast)"
echo ""

# Pull latest from GitHub
echo "Step 1: Pulling latest fixes from GitHub..."
git fetch origin cursor/continue-frozen-deploy-glmp-conversation-0c90
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:fix_all_25_processes.sh > /tmp/fix_list.sh
chmod +x /tmp/fix_list.sh
echo "✅ Latest code fetched!"
echo ""

# Extract process list
PROCESSES=(
    "bacillus/bacillus_biofilm_formation"
    "yeast/yeast_mitochondrial_biogenesis"
    "yeast/yeast_er_stress_response"
    "ecoli/ecoli_pentose_phosphate_pathway"
    "ecoli/ecoli_phage_defense"
    "yeast/yeast_chromatin_silencing"
    "yeast/yeast_vesicle_trafficking"
    "yeast/yeast_rna_splicing"
    "yeast/yeast_nitrogen_metabolism"
    "ecoli/ecoli_fatty_acid_degradation"
    "ecoli/ecoli_sulfur_metabolism"
    "ecoli/ecoli_outer_membrane_assembly"
    "ecoli/ecoli_amino_acid_biosynthesis"
    "ecoli/ecoli_nucleotide_biosynthesis"
    "yeast/yeast_mapk_mating"
    "yeast/yeast_pka_pathway"
    "yeast/yeast_snf1_pathway"
    "yeast/yeast_gcn4_starvation"
    "yeast/yeast_cell_wall_integrity"
    "ecoli/ecoli_tryptophan_biosynthesis"
    "ecoli/ecoli_phosphate_transport"
    "ecoli/ecoli_heat_shock_response"
    "ecoli/ecoli_e._coli_acid_resistance"
    "ecoli/ecoli_two_component_signaling"
    "ecoli/ecoli_anaerobic_respiration"
)

# Extract and upload each process
echo "Step 2: Extracting and uploading fixed processes..."
mkdir -p /tmp/glmp-fixed-colors

UPLOADED=0
for process in "${PROCESSES[@]}"; do
    FILE="${process}.json"
    TEMP_FILE="/tmp/glmp-fixed-colors/$(basename $FILE)"
    
    echo "  📤 ${process}..."
    
    # Extract from GitHub
    git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/${FILE} > "$TEMP_FILE"
    
    if [ $? -ne 0 ]; then
        echo "    ⚠️  Failed to extract from GitHub"
        continue
    fi
    
    # Upload to GCS
    gsutil cp "$TEMP_FILE" "gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/${FILE}"
    
    if [ $? -eq 0 ]; then
        ((UPLOADED++))
    else
        echo "    ❌ Upload failed"
    fi
done

echo ""
echo "Step 3: Setting cache control headers..."
gsutil -m setmeta -h "Cache-Control:no-cache, max-age=0" \
  "gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/**/*.json"

echo ""
echo "=========================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "📊 Results:"
echo "  • Uploaded: $UPLOADED / ${#PROCESSES[@]} processes"
echo ""
echo "🔍 Test these processes:"
echo "  • bacillus_biofilm_formation"
echo "  • ecoli_amino_acid_biosynthesis"
echo "  • ecoli_anaerobic_respiration (syntax fix)"
echo ""
echo "Expected: All nodes show CORRECT colors (not all lavender!)"
echo ""
echo "View at:"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html"
echo ""
echo "⚠️  Remember to hard refresh (Ctrl+Shift+R or Cmd+Shift+R)!"
echo ""
