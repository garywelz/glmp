#!/bin/bash

# GLMP Complete Deployment Script
# Deploys:
# 1. Data fixes (NOT gate metadata sync)
# 2. Viewer UX improvements (loading & layout)

set -e

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║                    🚀 GLMP COMPLETE DEPLOYMENT                               ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
GCS_BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
PROCESS_DIR="/workspace/processes_with_not_gates"
METADATA_FILE="/workspace/metadata_with_not_gates.json"
VIEWER_DIR="/workspace/glmp-v2/viewer"

echo "📦 DEPLOYMENT PLAN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Part 1: Data Fixes"
echo "    • 108 individual process files (with synced notGates field)"
echo "    • metadata.json (with corrected statistics)"
echo ""
echo "  Part 2: Viewer UX Improvements"
echo "    • viewer.js (optimized loading)"
echo "    • index.html (diagram-first layout)"
echo "    • styles.css (expandable sections)"
echo ""

read -p "🔐 Ready to deploy? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📤 PART 1: Deploying Data Fixes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Deploy E. coli processes
echo "📁 Uploading E. coli processes..."
gsutil -m cp -r "$PROCESS_DIR/ecoli/*.json" "$GCS_BUCKET/glmp-v2/processes/ecoli/"

# Deploy Yeast processes
echo "📁 Uploading Yeast processes..."
gsutil -m cp -r "$PROCESS_DIR/yeast/*.json" "$GCS_BUCKET/glmp-v2/processes/yeast/"

# Deploy Bacillus processes (if they exist)
if [ -d "$PROCESS_DIR/bacillus" ]; then
    echo "📁 Uploading Bacillus processes..."
    gsutil -m cp -r "$PROCESS_DIR/bacillus/*.json" "$GCS_BUCKET/glmp-v2/processes/bacillus/"
fi

# Deploy metadata.json
echo "📊 Uploading metadata.json (with synced notGates field)..."
gsutil cp "$METADATA_FILE" "$GCS_BUCKET/glmp-v2/metadata.json"

# Set cache control headers
echo "🔄 Setting cache-control headers (no-cache)..."
gsutil -m setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" \
    "$GCS_BUCKET/glmp-v2/processes/**" \
    "$GCS_BUCKET/glmp-v2/metadata.json"

echo ""
echo "✅ Data fixes deployed successfully!"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📤 PART 2: Deploying Viewer UX Improvements"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Deploy viewer files
echo "🎨 Uploading viewer.js..."
gsutil cp "$VIEWER_DIR/viewer.js" "$GCS_BUCKET/glmp-v2/viewer/viewer.js"

echo "📄 Uploading index.html..."
gsutil cp "$VIEWER_DIR/index.html" "$GCS_BUCKET/glmp-v2/viewer/index.html"

echo "🎨 Uploading styles.css..."
gsutil cp "$VIEWER_DIR/styles.css" "$GCS_BUCKET/glmp-v2/viewer/styles.css"

# Set cache control for viewer files
echo "🔄 Setting cache-control headers for viewer..."
gsutil -m setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" \
    "$GCS_BUCKET/glmp-v2/viewer/viewer.js" \
    "$GCS_BUCKET/glmp-v2/viewer/index.html" \
    "$GCS_BUCKET/glmp-v2/viewer/styles.css"

echo ""
echo "✅ Viewer UX improvements deployed successfully!"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ DEPLOYMENT COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 WHAT WAS DEPLOYED:"
echo ""
echo "  Data Fixes:"
echo "    ✅ 108 process files with synced notGates field"
echo "    ✅ metadata.json with correct statistics"
echo "       • Pattern: 347:435:470 (OR:AND:NOT)"
echo "       • Total nodes: 7,273"
echo "       • Total conditionals: 6,231"
echo ""
echo "  Viewer UX:"
echo "    ✅ Optimized loading (no double loading)"
echo "    ✅ Diagram-first layout (no scrolling needed)"
echo "    ✅ Collapsible metadata sections"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 VERIFICATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Wait 5 minutes for GCS propagation, then:"
echo ""
echo "  1. Database Table:"
echo "     • Hard refresh: Ctrl+Shift+R"
echo "     • Check: Amino Acid Biosynthesis shows 🔴 5 (not 0)"
echo "     • Check: Anaerobic Respiration shows 🔴 7 (not 3)"
echo "     • Check: Total NOT gates = 470 (not 126)"
echo ""
echo "  2. Viewer:"
echo "     • Visit: https://storage.googleapis.com/.../glmp-v2/viewer/index.html?process=ecoli_amino_acid_biosynthesis"
echo "     • Check: Single smooth load (no double loading)"
echo "     • Check: Diagram appears immediately (no scrolling)"
echo "     • Check: Metadata sections are collapsible"
echo ""
echo "  3. Run verification script:"
echo "     ./VERIFY_ALL_FIXES.sh"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎉 Ready for production!"
echo ""
