#!/bin/bash
# Upload corrected viewer index.html with 100:11:6:2 pattern

cd /home/gdubs/glmp

echo "=========================================="
echo "🔧 UPLOADING CORRECTED VIEWER INDEX.HTML"
echo "=========================================="
echo ""

# Upload the corrected index.html to GCS
echo "Step 1: Uploading corrected viewer index.html..."
gsutil cp glmp-v2/viewer/index.html gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html

echo "✅ Uploaded corrected index.html"
echo ""

echo "Step 2: Setting cache headers to force refresh..."
gsutil setmeta -h "Cache-Control:no-cache,max-age=0" gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html

echo ""
echo "=========================================="
echo "✅ VIEWER INDEX.HTML UPDATED WITH 100:11:6:2 PATTERN!"
echo "=========================================="
echo ""
echo "The viewer now shows:"
echo "  • Corrected 100:11:6:2 computational architecture"
echo "  • Updated pattern matching the paper"
echo "  • Cache-busting headers for immediate refresh"
echo ""
echo "🌐 VIEWER URL:"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html"
echo ""
echo "📱 DO A HARD REFRESH:"
echo "  • Windows/Linux: Ctrl + Shift + R (or Ctrl + F5)"
echo "  • Mac: Cmd + Shift + R"
echo ""
echo "You should now see the correct 100:11:6:2 pattern! 🎉"
echo ""
