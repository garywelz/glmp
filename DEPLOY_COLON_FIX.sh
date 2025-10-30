#!/bin/bash

# Deploy ACTUAL fix for Mermaid syntax error
# ROOT CAUSE: Colons in node labels

set -e

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║         🎯 DEPLOYING ACTUAL MERMAID FIX - COLON REMOVAL                      ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

GCS_BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
LOCAL_FILE="./processes_with_not_gates/ecoli/ecoli_anaerobic_respiration.json"
GCS_PATH="${GCS_BUCKET}/glmp-v2/processes/ecoli/ecoli_anaerobic_respiration.json"

echo "🔬 ROOT CAUSE IDENTIFIED:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  ❌ PROBLEM: Colons (:) in node labels break Mermaid 10.6.1 parser"
echo "     - Mermaid uses colons for special syntax (shapes, classes)"
echo "     - Colons INSIDE labels cause parse conflicts"
echo ""
echo "  🔧 FIXES APPLIED (3 nodes):"
echo "     1. A8:  'conditions: FNR' → 'conditions - FNR'"
echo "     2. A38: 'High O2: quinones' → 'High O2 - quinones'"
echo "     3. A39: 'Low O2: quinones' → 'Low O2 - quinones'"
echo ""
echo "  ✅ VALIDATION: Created test HTML with Mermaid 10.6.1"
echo "     - Parser validation passed locally"
echo "     - This is the ACTUAL syntax error, not a guess"
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

echo "📁 Uploading ecoli_anaerobic_respiration.json..."
gsutil -h "Content-Type:application/json" cp "$LOCAL_FILE" "$GCS_PATH"

echo ""
echo "🔄 Setting cache-control headers..."
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
echo "  2. Verify no colons in node labels:"
echo "     curl -s '$GCS_PATH' | grep -E 'A8\\[|A38\\[|A39\\[' | grep -c ' - '"
echo "     (should return 3)"
echo ""
echo "  3. Test in viewer (FRESH browser, incognito + timestamp):"
echo "     https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_anaerobic_respiration&ts=\$(date +%s)"
echo ""
echo "  ✅ EXPECTED: NO 'Syntax error in text' message"
echo "  ✅ EXPECTED: Full diagram renders correctly"
echo "  ✅ EXPECTED: All node labels display properly"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 NOTE: This is the ACTUAL root cause, validated with Mermaid 10.6.1 parser."
echo "         Previous fixes (brackets, tildes) were not the issue."
echo ""
