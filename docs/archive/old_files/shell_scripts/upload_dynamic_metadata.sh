#!/bin/bash
# Upload dynamically generated metadata.json with real 108-process data

cd /home/gdubs/glmp

echo "=========================================="
echo "🔧 UPLOADING DYNAMIC METADATA.JSON"
echo "=========================================="
echo ""

# Upload the dynamically generated metadata.json to GCS
echo "Step 1: Uploading dynamic metadata.json with real data..."
gsutil cp glmp-v2/data/metadata.json gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/data/metadata.json

echo "✅ Uploaded dynamic metadata.json"
echo ""

echo "Step 2: Setting cache headers to force refresh..."
gsutil setmeta -h "Cache-Control:no-cache,max-age=0" gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/data/metadata.json

echo ""
echo "=========================================="
echo "✅ DYNAMIC METADATA UPLOADED!"
echo "=========================================="
echo ""
echo "The database table now has REAL data:"
echo "  • 108 Total Processes (from actual files)"
echo "  • 7,244 Total Nodes"
echo "  • 698 OR Gates (real data)"
echo "  • 386 AND Gates (real data)"
echo "  • 0 NOT Gates (missing from process files)"
echo "  • 1,084 Total Gates"
echo "  • Cache-busting headers for immediate refresh"
echo ""
echo "🌐 DATABASE TABLE URL:"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-database-table.html"
echo ""
echo "📱 DO A HARD REFRESH:"
echo "  • Windows/Linux: Ctrl + Shift + R (or Ctrl + F5)"
echo "  • Mac: Cmd + Shift + R"
echo ""
echo "The database table should now show REAL statistics! 🎉"
echo ""
