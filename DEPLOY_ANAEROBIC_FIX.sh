#!/bin/bash

# Deploy single file fix for ecoli_anaerobic_respiration
# Fixes Mermaid 10.6.1 syntax error caused by tildes

set -e

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║         🔧 DEPLOYING ANAEROBIC RESPIRATION MERMAID SYNTAX FIX               ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
GCS_BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
LOCAL_FILE="./processes_with_not_gates/ecoli/ecoli_anaerobic_respiration.json"
GCS_PATH="${GCS_BUCKET}/glmp-v2/processes/ecoli/ecoli_anaerobic_respiration.json"

echo "📋 FIX APPLIED:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  🐛 PROBLEM: Mermaid 10.6.1 rejects tildes (~) in node labels"
echo "     - Caused 'Syntax error in text'"
echo ""
echo "  🔧 SOLUTION: Replace tildes with hyphens"
echo "     - ArcA~P → ArcA-P (5 occurrences)"
echo "     - ArcB~P → ArcB-P (1 occurrence)"
echo ""
echo "  ✅ SCIENTIFIC ACCURACY MAINTAINED:"
echo "     - Both notations denote phosphorylated forms"
echo "     - Hyphen notation is standard in literature"
echo ""

read -p "🔐 Deploy this fix? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📤 DEPLOYING TO GCS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Upload file
echo "📁 Uploading ecoli_anaerobic_respiration.json..."
gsutil -h "Content-Type:application/json" cp "$LOCAL_FILE" "$GCS_PATH"

echo ""
echo "🔄 Setting aggressive cache-control headers..."
gsutil setmeta \
  -h "Cache-Control:no-cache, no-store, must-revalidate, max-age=0" \
  "$GCS_PATH"

echo ""
echo "✅ Deployment complete!"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 VERIFICATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  1. Wait 2 minutes for GCS propagation"
echo ""
echo "  2. Verify deployed file:"
echo "     curl -s '$GCS_PATH' | grep -c 'ArcA-P'"
echo "     (should return 5)"
echo ""
echo "  3. Test in viewer (INCOGNITO window with timestamp):"
echo "     https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_anaerobic_respiration&ts=\$(date +%s)"
echo ""
echo "  ✅ EXPECTED: No 'Syntax error in text' message"
echo "  ✅ EXPECTED: Graph renders completely"
echo "  ✅ EXPECTED: All phosphorylated forms show as 'ArcA-P', 'ArcB-P'"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
