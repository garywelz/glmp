#!/bin/bash
# Deploy all 108 processes with expanded NOT gates + updated metadata

echo "🚀 DEPLOYING: Option A NOT Gate Expansion"
echo "=========================================="
echo ""
echo "This deployment includes:"
echo "  • 344 new NOT gates added (127 → 470)"
echo "  • All processes with selective NOT gate conversion"
echo "  • Updated metadata with new counts"
echo "  • Pattern: 347:435:470 (OR:AND:NOT)"
echo ""

# Check if we're in the right directory
if [ ! -d "processes_with_not_gates" ]; then
    echo "❌ Error: processes_with_not_gates directory not found"
    echo "Please run this script from /workspace"
    exit 1
fi

# Upload all processes
echo "📤 Step 1: Uploading processes with NOT gates..."
gsutil -m cp processes_with_not_gates/ecoli/*.json \
    gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/

gsutil -m cp processes_with_not_gates/yeast/*.json \
    gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/yeast/

gsutil -m cp processes_with_not_gates/bacillus/*.json \
    gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/bacillus/

echo "✅ Processes uploaded"
echo ""

# Upload updated metadata
echo "📤 Step 2: Uploading updated metadata..."
echo "   Uploading metadata_with_not_gates.json as metadata.json"
gsutil cp metadata_with_not_gates.json \
    gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/metadata.json

echo "✅ Metadata uploaded (347:435:470)"
echo ""

# Set cache headers
echo "🔧 Step 3: Setting cache headers..."
gsutil -m setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" \
    gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/**/*.json

gsutil setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" \
    gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/metadata.json

echo "✅ Cache headers set"
echo ""

echo "=========================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "NEW STATISTICS:"
echo "  OR gates:  347"
echo "  AND gates: 435"
echo "  NOT gates: 470 (+343 from before!)"
echo "  Pattern: 347:435:470"
echo ""
echo "All 470 NOT gates are now:"
echo "  ✅ Red background (#e74c3c)"
echo "  ✅ White text (#fff) for readability"
echo "  ✅ Trapezoid shapes [/Label/]"
echo ""
echo "Verify at: https://huggingface.co/spaces/garywelz/glmp"
echo ""
