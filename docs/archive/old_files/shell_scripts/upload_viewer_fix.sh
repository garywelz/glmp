#!/bin/bash
# Upload viewer.js with cache-busting fix

cd /home/gdubs/glmp

echo "=========================================="
echo "🔧 UPLOADING VIEWER.JS WITH CACHE FIX"
echo "=========================================="
echo ""

# Get the fixed viewer.js from GitHub
echo "Step 1: Fetching updated viewer.js from GitHub..."
git fetch origin cursor/continue-frozen-deploy-glmp-conversation-0c90
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:glmp-v2/viewer/viewer.js > v2-development/viewer/viewer.js

echo "✅ Downloaded updated viewer.js"
echo ""

# Upload to GCS
echo "Step 2: Uploading to GCS..."
gsutil cp v2-development/viewer/viewer.js gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/viewer.js

echo ""
echo "Step 3: Setting cache headers to force refresh..."
gsutil setmeta -h "Cache-Control:no-cache,max-age=0" gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/viewer.js

echo ""
echo "=========================================="
echo "✅ VIEWER.JS UPDATED WITH CACHE FIX!"
echo "=========================================="
echo ""
echo "The viewer now has:"
echo "  • Cache-busting query parameter (?v=timestamp)"
echo "  • cache: 'no-store' header on fetch"
echo "  • Forces fresh metadata load every time"
echo ""
echo "🌐 NOW OPEN THE VIEWER:"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html"
echo ""
echo "📱 DO A HARD REFRESH:"
echo "  • Windows/Linux: Ctrl + Shift + R (or Ctrl + F5)"
echo "  • Mac: Cmd + Shift + R"
echo ""
echo "You should now see all 100 processes! 🎉"
echo ""
echo "If you STILL don't see 100:"
echo "1. Clear ALL browser cache (Ctrl+Shift+Delete)"
echo "2. Try in Incognito/Private window"
echo "3. Try a different browser"
echo ""
