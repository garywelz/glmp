#!/bin/bash
# GLMP Viewer UI Improvements Deployment
# Phases 1-3: Loading fix, Navigation, Database links
# Created: $(date)

set -e  # Exit on error

echo "=================================================="
echo "🚀 GLMP VIEWER UI IMPROVEMENTS DEPLOYMENT"
echo "=================================================="
echo ""
echo "Deploying:"
echo "  ✅ Phase 1: Loading spinner and error handling"
echo "  ✅ Phase 2: Updated navigation (removed Process List, added Database Table)"
echo "  ✅ Phase 3: Database table links on Home and About pages"
echo ""

# Set GCS paths
BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
VIEWER_PATH="$BUCKET/glmp-v2/viewer"

# Deploy viewer files
echo "📤 Deploying viewer files..."
echo ""

echo "1️⃣  Deploying viewer.js..."
gsutil cp glmp-v2/viewer/viewer.js "$VIEWER_PATH/viewer.js"

echo "2️⃣  Deploying index.html..."
gsutil cp glmp-v2/viewer/index.html "$VIEWER_PATH/index.html"

echo "3️⃣  Deploying styles.css..."
gsutil cp glmp-v2/viewer/styles.css "$VIEWER_PATH/styles.css"

echo ""
echo "🔧 Setting cache headers (5-minute cache for quick updates)..."
gsutil setmeta -h "Cache-Control:public, max-age=300" "$VIEWER_PATH/viewer.js"
gsutil setmeta -h "Cache-Control:public, max-age=300" "$VIEWER_PATH/index.html"
gsutil setmeta -h "Cache-Control:public, max-age=300" "$VIEWER_PATH/styles.css"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "=================================================="
echo "📋 VERIFICATION STEPS"
echo "=================================================="
echo ""
echo "1. Clear browser cache completely (Ctrl+Shift+Delete)"
echo "   OR use Incognito/Private mode"
echo ""
echo "2. Visit: https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html"
echo ""
echo "3. Verify:"
echo "   ✅ Loading spinner appears briefly while loading processes"
echo "   ✅ Process list loads automatically (no manual reload needed)"
echo "   ✅ Navigation shows: Home | About | Database Table"
echo "   ✅ 'Database Table' button opens in new tab"
echo "   ✅ Home page has gradient box linking to database table"
echo "   ✅ About page has Resources section with database link"
echo ""
echo "4. Test error handling:"
echo "   - Disconnect internet → reload page → should see error message with retry button"
echo ""
echo "=================================================="
echo "🎯 WHAT'S FIXED"
echo "=================================================="
echo ""
echo "PHASE 1 - CRITICAL LOADING FIX:"
echo "  ❌ Before: Blank page on first visit, required manual reload"
echo "  ✅ After:  Loading spinner → process list loads automatically"
echo ""
echo "PHASE 2 - NAVIGATION CLEANUP:"
echo "  ❌ Before: Home | Process List | About (redundant)"
echo "  ✅ After:  Home | About | Database Table (streamlined)"
echo ""
echo "PHASE 3 - DATABASE ACCESS:"
echo "  ❌ Before: No easy way to access database table from viewer"
echo "  ✅ After:  Prominent links on Home, About, and Navigation"
echo ""
echo "=================================================="
echo "🚀 Deployment completed successfully!"
echo "=================================================="
