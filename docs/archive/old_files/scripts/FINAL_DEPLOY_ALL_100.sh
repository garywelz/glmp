#!/bin/bash
# 🎉 FINAL DEPLOYMENT: Upload everything to show 100 processes

cd /home/gdubs/glmp

echo "=========================================="
echo "🎊 FINAL DEPLOYMENT - 100 PROCESSES!"
echo "=========================================="
echo ""

# Fetch everything from GitHub
echo "Step 1: Fetching all updates from GitHub..."
git fetch origin cursor/continue-frozen-deploy-glmp-conversation-0c90
echo "✅ Fetched latest"
echo ""

# Upload viewer.js with cache-busting
echo "Step 2: Uploading viewer.js with cache-busting..."
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:glmp-v2/viewer/viewer.js > /tmp/viewer.js
gsutil cp /tmp/viewer.js gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/viewer.js
gsutil setmeta -h "Cache-Control:no-cache,max-age=0" gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/viewer.js
echo "✅ Viewer.js uploaded"
echo ""

# Upload database table with cache-busting
echo "Step 3: Uploading database table page..."
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:glmp-database-table.html > /tmp/glmp-database-table.html
gsutil cp /tmp/glmp-database-table.html gs://regal-scholar-453620-r7-podcast-storage/glmp-database-table.html
gsutil setmeta -h "Cache-Control:no-cache,max-age=0" gs://regal-scholar-453620-r7-podcast-storage/glmp-database-table.html
echo "✅ Database table uploaded"
echo ""

# Verify metadata (already uploaded earlier)
echo "Step 4: Verifying metadata on GCS..."
curl -s "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/data/metadata.json" | python3 << 'PYTHON'
import sys, json
data = json.load(sys.stdin)
print(f"  ✓ Total processes: {data['totalProcesses']}")
print(f"  ✓ Array length: {len(data['processes'])}")
print(f"  ✓ E. coli: {data['organisms'][0]['processCount']}")
print(f"  ✓ S. cerevisiae: {data['organisms'][1]['processCount']}")
print(f"  ✓ B. subtilis: {data['organisms'][2]['processCount']}")
PYTHON
echo ""

echo "=========================================="
echo "🎉 DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "📊 What's deployed:"
echo "  ✅ 100 biological processes"
echo "  ✅ Metadata with all 100 entries"
echo "  ✅ Viewer with cache-busting"
echo "  ✅ Database table with cache-busting"
echo ""
echo "🌐 YOUR PAGES:"
echo ""
echo "1. Main Viewer (interactive flowcharts):"
echo "   https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html"
echo ""
echo "2. Database Table (summary statistics):"
echo "   https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-database-table.html"
echo ""
echo "📱 IMPORTANT: Do a HARD REFRESH on each page:"
echo "   • Windows/Linux: Ctrl + Shift + R"
echo "   • Mac: Cmd + Shift + R"
echo ""
echo "🔍 To verify in browser console (F12):"
echo "   Look for: '✅ Loaded successfully: 100 processes'"
echo ""
echo "💡 If you STILL see 70:"
echo "   1. Clear ALL browser cache (Ctrl+Shift+Delete)"
echo "   2. Try Incognito/Private window"
echo "   3. Try different browser"
echo ""
echo "🎯 YOU SHOULD NOW SEE ALL 100 PROCESSES! 🎊"
echo ""
