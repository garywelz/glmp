#!/bin/bash

echo "=========================================="
echo "🚀 DEPLOYING BATCH 7: 8 NEW PROCESSES"
echo "=========================================="
echo ""
echo "This will upload:"
echo "  1. yeast_alcoholic_fermentation (72 nodes) ⭐"
echo "  2. yeast_aerobic_respiration (79 nodes)"
echo "  3. ecoli_aerobic_respiration (77 nodes)"
echo "  4. yeast_cell_cycle_checkpoints (85 nodes)"
echo "  5. yeast_dna_replication (82 nodes)"
echo "  6. yeast_ribosome_biogenesis (86 nodes)"
echo "  7. bacillus_germination (81 nodes)"
echo "  8. ecoli_peptidoglycan_biosynthesis (92 nodes)"
echo ""
echo "Total: 654 nodes across 8 processes"
echo ""

# Pull latest
echo "Step 1: Pulling latest from GitHub..."
git fetch origin cursor/continue-frozen-deploy-glmp-conversation-0c90
echo "✅ Latest code fetched"
echo ""

# Create temp directory
mkdir -p /tmp/glmp-batch7

# Extract and upload each process
echo "Step 2: Extracting and uploading processes..."

PROCESSES=(
    "yeast/yeast_alcoholic_fermentation"
    "yeast/yeast_aerobic_respiration"
    "ecoli/ecoli_aerobic_respiration"
    "yeast/yeast_cell_cycle_checkpoints"
    "yeast/yeast_dna_replication"
    "yeast/yeast_ribosome_biogenesis"
    "bacillus/bacillus_germination"
    "ecoli/ecoli_peptidoglycan_biosynthesis"
)

UPLOADED=0
for process in "${PROCESSES[@]}"; do
    FILE="${process}.json"
    BASENAME=$(basename $FILE)
    
    echo "  📤 ${process}..."
    
    # Extract from GitHub
    git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:gcs-processes/${FILE} > /tmp/glmp-batch7/$BASENAME
    
    if [ $? -ne 0 ]; then
        echo "    ⚠️  Failed to extract from GitHub"
        continue
    fi
    
    # Upload to GCS
    gsutil cp /tmp/glmp-batch7/$BASENAME gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/${FILE}
    
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
echo "✅ BATCH 7 DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "📊 Results:"
echo "  • Uploaded: $UPLOADED / ${#PROCESSES[@]} processes"
echo ""
echo "🧬 New Dataset Totals:"
echo "  • Total: 108 processes"
echo "  • E. coli: 66"
echo "  • Yeast: 38"
echo "  • Bacillus: 4"
echo ""
echo "🎯 Test the new fermentation process:"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=yeast_alcoholic_fermentation"
echo ""
echo "⚠️  Remember to hard refresh (Ctrl+Shift+R or Cmd+Shift+R)!"
echo ""
