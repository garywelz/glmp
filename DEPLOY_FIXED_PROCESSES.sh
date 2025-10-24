#!/bin/bash
# Deploy all 108 fixed GLMP processes with correct color-shape alignment

echo "🚀 DEPLOYING 108 FIXED GLMP PROCESSES"
echo "======================================"
echo ""

# Upload all fixed processes
echo "📤 Uploading E. coli processes..."
gsutil -m cp /workspace/fixed_processes_final/ecoli/*.json     gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/

echo "📤 Uploading Yeast processes..."
gsutil -m cp /workspace/fixed_processes_final/yeast/*.json     gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/yeast/

echo "📤 Uploading Bacillus processes..."
gsutil -m cp /workspace/fixed_processes_final/bacillus/*.json     gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/bacillus/

echo ""
echo "🔧 Setting cache headers..."
gsutil -m setmeta -h "Cache-Control:no-cache, no-store, must-revalidate"     gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/**/*.json

echo ""
echo "======================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "======================================"
echo ""
echo "All 108 processes now have:"
echo "  ✅ Yellow nodes = Diamonds"
echo "  ✅ Purple nodes = Hexagons"
echo "  ✅ Red nodes = Trapezoids"
echo ""
echo "Pattern: 347:444:127"
echo ""
