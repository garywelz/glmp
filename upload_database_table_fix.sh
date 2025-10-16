#!/bin/bash
# Upload glmp-database-table.html with cache-busting fix

cd /home/gdubs/glmp

echo "=========================================="
echo "🔧 UPLOADING DATABASE TABLE PAGE WITH CACHE FIX"
echo "=========================================="
echo ""

# Get the fixed database table from GitHub
echo "Step 1: Fetching updated database table HTML from GitHub..."
git fetch origin cursor/continue-frozen-deploy-glmp-conversation-0c90
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:glmp-database-table.html > glmp-database-table.html

echo "✅ Downloaded updated glmp-database-table.html"
echo ""

# Upload to GCS
echo "Step 2: Uploading to GCS..."
gsutil cp glmp-database-table.html gs://regal-scholar-453620-r7-podcast-storage/glmp-database-table.html

echo ""
echo "Step 3: Setting cache headers to force refresh..."
gsutil setmeta -h "Cache-Control:no-cache,max-age=0" gs://regal-scholar-453620-r7-podcast-storage/glmp-database-table.html

echo ""
echo "=========================================="
echo "✅ DATABASE TABLE PAGE UPDATED!"
echo "=========================================="
echo ""
echo "The database table now has:"
echo "  • Cache-busting query parameter (?v=timestamp)"
echo "  • cache: 'no-store' header on fetch"
echo "  • Forces fresh metadata load every time"
echo ""
echo "🌐 NOW OPEN THE DATABASE TABLE:"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-database-table.html"
echo ""
echo "📱 DO A HARD REFRESH:"
echo "  • Windows/Linux: Ctrl + Shift + R (or Ctrl + F5)"
echo "  • Mac: Cmd + Shift + R"
echo ""
echo "You should now see all 100 processes! 🎉"
echo ""
echo "If you STILL don't see 100:"
echo "  • Clear browser cache completely"
echo "  • Try Incognito/Private window"
echo "  • Open browser console (F12) to see what's loading"
echo ""
