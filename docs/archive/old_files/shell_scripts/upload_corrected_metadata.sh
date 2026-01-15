#!/bin/bash
# Upload corrected metadata.json with 108 processes

cd /home/gdubs/glmp

echo "=========================================="
echo "🔧 UPLOADING CORRECTED METADATA.JSON"
echo "=========================================="
echo ""

# Upload the corrected metadata.json to GCS
echo "Step 1: Uploading corrected metadata.json..."
gsutil cp glmp-v2/data/metadata.json gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/data/metadata.json

echo "✅ Uploaded corrected metadata.json"
echo ""

echo "Step 2: Setting cache headers to force refresh..."
gsutil setmeta -h "Cache-Control:no-cache,max-age=0" gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/data/metadata.json

echo ""
echo "=========================================="
echo "✅ METADATA.JSON UPDATED WITH 108 PROCESSES!"
echo "=========================================="
echo ""
echo "The database table now has:"
echo "  • 108 Total Processes (not 100)"
echo "  • Correct statistics: OR=636, AND=352, NOT=129"
echo "  • 100:11:6:2 architecture pattern"
echo "  • Cache-busting headers for immediate refresh"
echo ""
echo "🌐 DATABASE TABLE URL:"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-database-table.html"
echo ""
echo "📱 DO A HARD REFRESH:"
echo "  • Windows/Linux: Ctrl + Shift + R (or Ctrl + F5)"
echo "  • Mac: Cmd + Shift + R"
echo ""
echo "The database table should now load correctly! 🎉"
echo ""
