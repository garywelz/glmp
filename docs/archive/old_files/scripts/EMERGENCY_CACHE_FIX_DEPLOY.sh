#!/bin/bash
# EMERGENCY: Fix Viewer Cache Issues
# Issue: viewer.js pointed to wrong metadata.json path
# Created: $(date)

set -e

echo "=================================================="
echo "🚨 EMERGENCY CACHE FIX DEPLOYMENT"
echo "=================================================="
echo ""
echo "Issue: Viewer was loading glmp-v2/data/metadata.json (24 processes)"
echo "Fix: Changed to glmp-v2/metadata.json (108 processes)"
echo ""

BUCKET="gs://regal-scholar-453620-r7-podcast-storage"

echo "1️⃣  Deploying FIXED viewer.js with correct metadata path..."
gsutil -h "Cache-Control:no-cache, no-store, must-revalidate" \
       -h "Content-Type:application/javascript" \
       cp glmp-v2/viewer/viewer.js "$BUCKET/glmp-v2/viewer/viewer.js"

echo "2️⃣  Updating cache headers on metadata.json (no-cache for development)..."
gsutil setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" \
       "$BUCKET/glmp-v2/metadata.json"

echo "3️⃣  Updating cache headers on viewer files..."
gsutil setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" \
       "$BUCKET/glmp-v2/viewer/index.html"

gsutil setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" \
       "$BUCKET/glmp-v2/viewer/styles.css"

echo "4️⃣  Updating cache headers on database table..."
gsutil setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" \
       "$BUCKET/glmp-database-table.html"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "=================================================="
echo "🧪 VERIFICATION STEPS"
echo "=================================================="
echo ""
echo "1. Open browser in INCOGNITO/PRIVATE mode (mandatory!)"
echo ""
echo "2. Visit viewer:"
echo "   https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html"
echo ""
echo "3. Open browser console (F12) and look for:"
echo "   '🔄 Loading GLMP processes from: ...glmp-v2/metadata.json'"
echo "   '✅ Loaded successfully: 108 processes'"
echo ""
echo "4. Check process list table:"
echo "   - Should show all 108 processes"
echo "   - Scroll to bottom to verify"
echo ""
echo "5. Visit database table:"
echo "   https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-database-table.html"
echo ""
echo "6. Verify 108 rows appear"
echo ""
echo "=================================================="
echo "📊 EXPECTED RESULTS"
echo "=================================================="
echo ""
echo "✅ Viewer console log shows:"
echo "   'Loaded successfully: 108 processes'"
echo ""
echo "✅ Process list shows 108 rows (not 24!)"
echo ""
echo "✅ Database table shows 108 rows"
echo ""
echo "✅ No errors in browser console"
echo ""
echo "=================================================="
echo "🔧 IF STILL NOT WORKING"
echo "=================================================="
echo ""
echo "1. Clear ALL browser data (Ctrl+Shift+Delete)"
echo "   - Time range: All time"
echo "   - Check: Cached images and files"
echo ""
echo "2. Try different browser (Edge, Firefox, etc.)"
echo ""
echo "3. Check GCS metadata directly:"
echo "   curl 'https://storage.googleapis.com/.../glmp-v2/metadata.json' | jq '.processes | length'"
echo "   Expected: 108"
echo ""
echo "4. Check viewer.js deployed correctly:"
echo "   curl 'https://storage.googleapis.com/.../glmp-v2/viewer/viewer.js' | grep metadataPath"
echo "   Should see: glmp-v2/metadata.json (NOT glmp-v2/data/metadata.json)"
echo ""
echo "=================================================="
echo "🚀 Deploy completed! Test in incognito mode now!"
echo "=================================================="
