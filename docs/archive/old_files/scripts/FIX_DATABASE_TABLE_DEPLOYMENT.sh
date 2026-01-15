#!/bin/bash
# Fix Database Table - Deploy Corrected Version
# Issue: Logic gates showing as 0 because wrong metadata.json path
# Created: $(date)

set -e

echo "=========================================================="
echo "🔧 FIXING DATABASE TABLE - METADATA PATH"
echo "=========================================================="
echo ""
echo "Issue: Database table was loading wrong metadata.json"
echo "  ❌ OLD: glmp-v2/data/metadata.json (incomplete gate data)"
echo "  ✅ NEW: glmp-v2/metadata.json (complete gate data)"
echo ""

BUCKET="gs://regal-scholar-453620-r7-podcast-storage"

echo "📤 Deploying fixed database table..."
gsutil -h "Cache-Control:no-cache, no-store, must-revalidate" \
       -h "Content-Type:text/html" \
       cp glmp-database-table.html "$BUCKET/glmp-database-table.html"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "=========================================================="
echo "🧪 VERIFICATION STEPS"
echo "=========================================================="
echo ""
echo "IMPORTANT: Clear browser cache or use Incognito mode!"
echo ""
echo "1. Open in Incognito: https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-database-table.html"
echo ""
echo "2. Check statistics cards at top:"
echo "   ✅ Should show: ~85 OR gates, ~53 AND gates, ~127 NOT gates"
echo "   ❌ NOT: All zeros"
echo ""
echo "3. Check table rows:"
echo "   ✅ Each process should show logic gate counts"
echo "   Example: Biofilm Formation should show OR: 10, AND: 5"
echo ""
echo "4. Check browser console (F12):"
echo "   ✅ Should see: 'Data loaded successfully: 108 processes'"
echo "   ✅ Metadata URL should be: .../glmp-v2/metadata.json (NOT /data/metadata.json)"
echo ""
echo "=========================================================="
echo "📊 WHAT WAS WRONG"
echo "=========================================================="
echo ""
echo "Same issue as viewer had:"
echo "  • Database table pointed to glmp-v2/data/metadata.json"
echo "  • That file has LESS DETAILED gate data"
echo "  • Correct file is glmp-v2/metadata.json"
echo "  • Now both viewer AND database use same correct file"
echo ""
echo "Why it happened:"
echo "  • Desktop agent previously deployed partial metadata to /data/"
echo "  • Database table was never updated to use new location"
echo "  • Viewer was fixed yesterday, database table wasn't"
echo ""
echo "=========================================================="
echo "✅ FIX DEPLOYED - TEST IN INCOGNITO MODE"
echo "=========================================================="
