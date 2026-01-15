#!/bin/bash

# Deploy Syntax Error Fixes for 2 Processes
# Fixes the Mermaid rendering issues

set -e

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║              🔧 DEPLOYING SYNTAX ERROR FIXES                                 ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
GCS_BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
PROCESS_DIR="./processes_with_not_gates"

echo "📦 DEPLOYMENT PLAN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Process 1: Amino Acid Biosynthesis"
echo "    • Removed invalid AND gate (1 input)"
echo "    • Fixed 3 trapezoid sequences (last node only)"
echo "    • Added 2 missing AND/OR gates"
echo ""
echo "  Process 2: Anaerobic Respiration"
echo "    • Fixed bracket conflict in trapezoid label"
echo "    • Fixed wrong trapezoid syntax (3 nodes)"
echo "    • Graph should now render without syntax errors!"
echo ""

read -p "🔐 Ready to deploy? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📤 Deploying Fixed Process Files"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Deploy Amino Acid Biosynthesis
echo "📁 Uploading ecoli_amino_acid_biosynthesis.json..."
gsutil cp "$PROCESS_DIR/ecoli/ecoli_amino_acid_biosynthesis.json" \
  "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_amino_acid_biosynthesis.json"

# Deploy Anaerobic Respiration
echo "📁 Uploading ecoli_anaerobic_respiration.json..."
gsutil cp "$PROCESS_DIR/ecoli/ecoli_anaerobic_respiration.json" \
  "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_anaerobic_respiration.json"

# Set cache control headers
echo "🔄 Setting cache-control headers (no-cache)..."
gsutil setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_amino_acid_biosynthesis.json" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_anaerobic_respiration.json"

echo ""
echo "✅ Syntax fixes deployed successfully!"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ DEPLOYMENT COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 WHAT WAS DEPLOYED:"
echo ""
echo "  Amino Acid Biosynthesis:"
echo "    ✅ Invalid AND gate removed"
echo "    ✅ 3 trapezoid sequences fixed"
echo "    ✅ 2 OR gates added (Threonine, Valine)"
echo "    ✅ 1 AND gate added (Aromatic Family)"
echo ""
echo "  Anaerobic Respiration:"
echo "    ✅ Bracket conflict fixed: [2Fe-2S] → (2Fe-2S)"
echo "    ✅ Wrong trapezoid syntax fixed: [\Label/] → [/Label/]"
echo "    ✅ 3 nodes corrected (A13, A30, A59)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 VERIFICATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Wait 5 minutes for GCS propagation, then:"
echo ""
echo "  1. Amino Acid Biosynthesis:"
echo "     • Visit the viewer"
echo "     • Graph should render completely"
echo "     • Check for yellow OR diamonds after Threonine and Valine"
echo "     • Check for purple AND hexagon at Aromatic Family"
echo ""
echo "  2. Anaerobic Respiration:"
echo "     • Visit the viewer"
echo "     • Graph should render WITHOUT syntax errors"
echo "     • No 'Syntax Error in text' message"
echo "     • All red trapezoids should display correctly"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎉 Ready to verify!"
echo ""
