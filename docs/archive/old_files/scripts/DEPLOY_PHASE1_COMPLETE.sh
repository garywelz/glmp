#!/bin/bash
#
# DEPLOY PHASE 1 COMPLETE: Logic Gates + Products
# ================================================
# Deploys all 109 updated processes to GCS
#

set -e

echo "========================================================================"
echo "🚀 DEPLOYING PHASE 1 COMPLETE: LOGIC GATES + PRODUCTS"
echo "========================================================================"
echo ""
echo "Updates being deployed:"
echo "  ✓ Phase 1A: 68 processes - AND gates → Purple hexagons"
echo "  ✓ Phase 1B: 54 processes - NOT gates → Red trapezoids"  
echo "  ✓ Phase 1C: 30 processes - Products → True black"
echo ""
echo "Visual system:"
echo "  🟠 OR gates:  Orange diamond ◆    (#ff9f43)"
echo "  🟣 AND gates: Purple hexagon ⬡    (#7950f2)"
echo "  🔴 NOT gates: Red trapezoid ⏷     (#e74c3c)"
echo "  ⚫ Products:   True black         (#000000)"
echo ""
echo "Total gates visualized:"
echo "  • 636 OR gates  (100 processes)"
echo "  • 352 AND gates (68 processes)"
echo "  • 129 NOT gates (54 processes)"
echo "  • 48 products   (30 processes)"
echo ""
echo "========================================================================"
echo ""

# 1. Fetch latest from GitHub
echo "📥 Step 1: Fetching latest from GitHub..."
git fetch origin
git checkout cursor/continue-frozen-deploy-glmp-conversation-0c90
git pull origin cursor/continue-frozen-deploy-glmp-conversation-0c90
echo "✓ Git sync complete"
echo ""

# 2. Upload all process files
echo "📤 Step 2: Uploading all 109 processes to GCS..."
gsutil -m cp -r /workspace/gcs-processes/* \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/
echo "✓ Processes uploaded"
echo ""

# 3. Set public access
echo "🔓 Step 3: Setting public read access..."
gsutil -m acl ch -r -u AllUsers:R \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/
echo "✓ Public access configured"
echo ""

# 4. Set cache headers (5 minutes)
echo "⚡ Step 4: Setting cache headers..."
gsutil -m setmeta -h "Cache-Control:public, max-age=300" \
  -r gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/
echo "✓ Cache headers set"
echo ""

echo "========================================================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "========================================================================"
echo ""
echo "🎨 Your processes now feature:"
echo "  • Unique shapes for all 3 logic gate types"
echo "  • Color-coded computational elements"
echo "  • True black for final outcomes/products"
echo "  • Color-blind accessible design"
echo ""
echo "📊 Paper visualization ready:"
echo "  • 100:12:6:2 computational architecture"
echo "  • 1,117 total logic gates across 108 processes"
echo "  • Publication-quality flowcharts"
echo ""
echo "🌐 View at:"
echo "  https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html"
echo ""
echo "💡 Next step: Hard refresh your browser (Ctrl+Shift+R / Cmd+Shift+R)"
echo "    to see the new logic gate visualizations!"
echo ""
echo "========================================================================"
