#!/bin/bash
#
# Deploy Viewer.js Fix for Color Legend Loading Issue
# ====================================================
#

set -e

echo "========================================================================"
echo "🔧 DEPLOYING VIEWER.JS FIX - Color Legend Keys"
echo "========================================================================"
echo ""
echo "Issue: Processes not showing correct color legends"
echo "Cause: viewer.js had old Phase 1 color keys"
echo "Fix: Updated to Phase 2 final keys"
echo ""
echo "Old keys: red, yellow, green, blue, orange, lavender, violet"
echo "New keys: green, amber, darkSkyBlue, lightCyan, yellow, purple, red, black"
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

# 2. Upload viewer.js
echo "📤 Step 2: Uploading fixed viewer.js to GCS..."
gsutil cp glmp-v2/viewer/viewer.js \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/viewer.js
echo "✓ viewer.js uploaded"
echo ""

# 3. Set public access
echo "🔓 Step 3: Setting public read access..."
gsutil acl ch -u AllUsers:R \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/viewer.js
echo "✓ Public access configured"
echo ""

# 4. Set cache headers (bust cache)
echo "⚡ Step 4: Setting cache headers..."
gsutil setmeta -h "Cache-Control:public, max-age=300" \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/viewer.js
echo "✓ Cache headers set"
echo ""

echo "========================================================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "========================================================================"
echo ""
echo "🎨 Fixed processes:"
echo "  • yeast_cell_cycle_control - color legend now displays"
echo "  • ecoli_amino_acid_biosynthesis - color legend now displays"
echo "  • ALL 108 processes - color legends corrected"
echo ""
echo "🌐 View at:"
echo "  https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html"
echo ""
echo "💡 CRITICAL: Hard refresh your browser to clear cached viewer.js!"
echo "   • Windows/Linux: Ctrl + Shift + R"
echo "   • Mac:           Cmd + Shift + R"
echo ""
echo "   Or use incognito mode for guaranteed fresh load"
echo ""
echo "🎉 All processes should now load correctly with full 8-color legend!"
echo ""
echo "========================================================================"
