#!/bin/bash
# DEPLOY ALL VIEWER FIXES - Complete Update
# Includes: Path fix + UI improvements + Loading spinner + Database links
# Created: $(date)

set -e

echo "=========================================================="
echo "🚀 DEPLOYING ALL VIEWER FIXES"
echo "=========================================================="
echo ""
echo "This deploys:"
echo "  ✅ Metadata path fix (glmp-v2/data → glmp-v2)"
echo "  ✅ Loading spinner for better UX"
echo "  ✅ Removed redundant 'Process List' button"
echo "  ✅ Added 'Database Table' button to navigation"
echo "  ✅ Database links on Home and About pages"
echo "  ✅ Improved error handling"
echo "  ✅ Cache-busting and no-cache headers"
echo ""

BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
VIEWER_PATH="$BUCKET/glmp-v2/viewer"

# Check files exist
echo "🔍 Checking local files..."
if [ ! -f "glmp-v2/viewer/index.html" ]; then
    echo "❌ ERROR: glmp-v2/viewer/index.html not found!"
    echo "Make sure you're in ~/glmp directory"
    exit 1
fi

if [ ! -f "glmp-v2/viewer/viewer.js" ]; then
    echo "❌ ERROR: glmp-v2/viewer/viewer.js not found!"
    exit 1
fi

if [ ! -f "glmp-v2/viewer/styles.css" ]; then
    echo "❌ ERROR: glmp-v2/viewer/styles.css not found!"
    exit 1
fi

echo "✅ All local files found"
echo ""

# Deploy viewer files with no-cache headers
echo "=========================================================="
echo "📤 DEPLOYING VIEWER FILES"
echo "=========================================================="
echo ""

echo "1️⃣  Deploying index.html (updated navigation, database links)..."
gsutil -h "Cache-Control:no-cache, no-store, must-revalidate" \
       -h "Content-Type:text/html" \
       cp glmp-v2/viewer/index.html "$VIEWER_PATH/index.html"
echo "   ✅ index.html deployed"

echo ""
echo "2️⃣  Deploying viewer.js (fixed path, loading spinner, database button)..."
gsutil -h "Cache-Control:no-cache, no-store, must-revalidate" \
       -h "Content-Type:application/javascript" \
       cp glmp-v2/viewer/viewer.js "$VIEWER_PATH/viewer.js"
echo "   ✅ viewer.js deployed"

echo ""
echo "3️⃣  Deploying styles.css (spinner animation, new styling)..."
gsutil -h "Cache-Control:no-cache, no-store, must-revalidate" \
       -h "Content-Type:text/css" \
       cp glmp-v2/viewer/styles.css "$VIEWER_PATH/styles.css"
echo "   ✅ styles.css deployed"

echo ""
echo "4️⃣  Updating metadata.json cache headers..."
gsutil setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" \
       "$BUCKET/glmp-v2/metadata.json"
echo "   ✅ metadata.json cache headers updated"

echo ""
echo "=========================================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=========================================================="
echo ""

# Verification
echo "=========================================================="
echo "🧪 VERIFICATION STEPS"
echo "=========================================================="
echo ""
echo "IMPORTANT: Use INCOGNITO/PRIVATE mode to bypass cache!"
echo ""
echo "1. Open browser in Incognito mode (Ctrl+Shift+N)"
echo ""
echo "2. Visit viewer:"
echo "   https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html"
echo ""
echo "3. Check navigation buttons:"
echo "   ✅ Should see: Home | About | Database Table"
echo "   ❌ Should NOT see: Process List button"
echo ""
echo "4. Check loading behavior:"
echo "   ✅ Should see loading spinner briefly"
echo "   ✅ Process list loads automatically"
echo "   ✅ All 108 processes visible"
echo ""
echo "5. Check Home page:"
echo "   ✅ Purple gradient box with 'Open Database Table' button"
echo ""
echo "6. Check About page:"
echo "   ✅ Resources section with database link"
echo ""
echo "7. Test Database Table button:"
echo "   ✅ Clicks open database in new tab"
echo ""
echo "8. Check browser console (F12):"
echo "   ✅ Should see: 'Loaded successfully: 108 processes'"
echo "   ❌ Should NOT see any red errors"
echo ""
echo "=========================================================="
echo "📊 EXPECTED RESULTS"
echo "=========================================================="
echo ""
echo "Navigation:"
echo "  BEFORE: [Home] [Process List] [About]"
echo "  AFTER:  [Home] [About] [Database Table]"
echo ""
echo "Loading:"
echo "  BEFORE: Blank page → manual reload needed"
echo "  AFTER:  Spinner → smooth loading → 108 processes"
echo ""
echo "Database Access:"
echo "  BEFORE: No easy way to access database"
echo "  AFTER:  3 ways (nav button, home box, about link)"
echo ""
echo "Process Count:"
echo "  BEFORE: 24 processes (wrong metadata path)"
echo "  AFTER:  108 processes (correct metadata path)"
echo ""
echo "=========================================================="
echo "🔧 TROUBLESHOOTING"
echo "=========================================================="
echo ""
echo "If you still see old navigation:"
echo "  1. Close ALL browser windows"
echo "  2. Clear browser cache completely (Ctrl+Shift+Delete)"
echo "  3. Reopen in Incognito mode"
echo "  4. Try different browser (Edge, Firefox, etc.)"
echo ""
echo "If still not working:"
echo "  1. Check browser console for errors (F12)"
echo "  2. Check Network tab for failed requests"
echo "  3. Verify deployment:"
echo ""
echo "     curl 'https://storage.googleapis.com/.../glmp-v2/viewer/index.html' | grep 'Process List'"
echo ""
echo "     Should return 0 results (button removed)"
echo ""
echo "=========================================================="
echo "🎉 DEPLOYMENT SUCCESSFUL!"
echo "=========================================================="
echo ""
echo "All viewer improvements are now live!"
echo "Test in Incognito mode to verify."
echo ""
