#!/bin/bash

echo "=========================================="
echo "🚀 DEPLOYING ENHANCED VIEWER"
echo "=========================================="
echo ""

# Deploy enhanced index.html
echo "1️⃣  Deploying enhanced index.html..."
gsutil -h "Cache-Control:no-cache, max-age=0" \
       -h "Content-Type:text/html" \
       cp glmp-v2/viewer/index.html \
       gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html
echo "   ✅ Enhanced index.html deployed"
echo ""

# Deploy updated database table with back link
echo "2️⃣  Deploying database table with back link..."
gsutil -h "Cache-Control:no-cache, max-age=0" \
       -h "Content-Type:text/html" \
       cp glmp-database-table.html \
       gs://regal-scholar-453620-r7-podcast-storage/glmp-database-table.html
echo "   ✅ Database table deployed"
echo ""

echo "=========================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "CHANGES DEPLOYED:"
echo "  ✅ Removed 'Database Table' from navigation"
echo "  ✅ Added project introduction and description"
echo "  ✅ Added color legend on home page"
echo "  ✅ Added featured Lac Operon example"
echo "  ✅ Added 'Coming Soon' notice for chart generator"
echo "  ✅ Added back link from database table to viewer"
echo "  ✅ Enhanced overall presentation"
echo ""
echo "TEST IN INCOGNITO MODE:"
echo "  Viewer: https://storage.googleapis.com/.../glmp-v2/viewer/index.html"
echo "  Database: https://storage.googleapis.com/.../glmp-database-table.html"
echo ""
