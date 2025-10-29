#!/bin/bash

# Deploy ONLY the 3 user-reported processes
# Quick deployment to fix syntax errors

set -e

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║           🚀 DEPLOYING 3 USER-REPORTED PROCESSES (SYNTAX FIXES)              ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
GCS_BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
PROCESS_DIR="./processes_with_not_gates"

echo "📦 DEPLOYMENT MANIFEST"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  🎯 3 USER-REPORTED PROCESSES:"
echo "    1. ecoli_amino_acid_biosynthesis (6 logic fixes)"
echo "    2. ecoli_anaerobic_respiration (ALL bracket conflicts now fixed)"
echo "    3. ecoli_biofilm_formation (1 syntax fix)"
echo ""

read -p "🔐 Deploy these 3 processes? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📤 DEPLOYING USER-REPORTED PROCESSES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📁 1. ecoli_amino_acid_biosynthesis.json..."
gsutil cp "$PROCESS_DIR/ecoli/ecoli_amino_acid_biosynthesis.json" \
  "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_amino_acid_biosynthesis.json"

echo "📁 2. ecoli_anaerobic_respiration.json..."
gsutil cp "$PROCESS_DIR/ecoli/ecoli_anaerobic_respiration.json" \
  "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_anaerobic_respiration.json"

echo "📁 3. ecoli_biofilm_formation.json..."
gsutil cp "$PROCESS_DIR/ecoli/ecoli_biofilm_formation.json" \
  "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_biofilm_formation.json"

echo ""
echo "🔄 Setting cache-control headers (AGGRESSIVE - force refresh)..."
gsutil -m setmeta -h "Cache-Control:no-cache, no-store, must-revalidate, max-age=0" \
    -h "Pragma:no-cache" \
    -h "Expires:0" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_amino_acid_biosynthesis.json" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_anaerobic_respiration.json" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_biofilm_formation.json"

echo ""
echo "✅ All 3 processes deployed successfully!"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ DEPLOYMENT COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 DEPLOYED:"
echo "  ✅ 3 user-reported processes"
echo ""
echo "  🔧 Fixes included:"
echo "    • Amino Acid: 6 logic gate errors (AND/OR gates, trapezoid sequences)"
echo "    • Anaerobic: ALL bracket conflicts ([4Fe-4S] → (4Fe-4S))"
echo "    • Biofilm: 1 wrong trapezoid syntax ([\\Label/] → [/Label/])"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 VERIFICATION (CRITICAL - Cache Issues)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  🚨 AGGRESSIVE CACHE CLEARING REQUIRED:"
echo ""
echo "  1. Close ALL browser windows"
echo "  2. Clear ALL browser data (history, cache, cookies)"
echo "  3. Wait 5 minutes for GCS/CDN propagation"
echo "  4. Open browser in INCOGNITO/PRIVATE mode"
echo "  5. Test these 3 processes"
echo ""
echo "  OR use direct GCS links (bypasses CDN/HuggingFace):"
echo "  https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_amino_acid_biosynthesis"
echo "  https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_anaerobic_respiration"
echo "  https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_biofilm_formation"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
