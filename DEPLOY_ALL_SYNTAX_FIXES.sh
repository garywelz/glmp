#!/bin/bash

# Deploy All Syntax Error Fixes - Phase 1
# Fixes Mermaid rendering issues in 16 processes

set -e

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║              🔧 DEPLOYING ALL SYNTAX ERROR FIXES (PHASE 1)                   ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
GCS_BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
PROCESS_DIR="/workspace/processes_with_not_gates"

echo "📦 DEPLOYMENT SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Processes Fixed: 16"
echo "  Bracket Conflicts Resolved: 20"
echo "  Wrong Syntax Corrected: 23"
echo ""
echo "  Fixes Applied:"
echo "    • Replaced [brackets] with (parentheses) inside trapezoid labels"
echo "    • Fixed wrong trapezoid syntax: [\\Label/] → [/Label/]"
echo ""
echo "  E. coli Processes (8):"
echo "    - fatty_acid_degradation"
echo "    - fatty_acid_synthesis"
echo "    - homologous_recombination"
echo "    - outer_membrane_assembly"
echo "    - transcription_elongation"
echo "    - transcription_termination"
echo "    - translation_elongation"
echo "    - translation_termination"
echo ""
echo "  Yeast Processes (8):"
echo "    - chromatin_silencing"
echo "    - er_stress_response"
echo "    - gcn4_starvation"
echo "    - nitrogen_metabolism"
echo "    - pka_pathway"
echo "    - rna_splicing"
echo "    - snf1_pathway"
echo "    - vesicle_trafficking"
echo ""

read -p "🔐 Ready to deploy all 16 fixed processes? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📤 Deploying E. coli Processes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# E. coli processes
ecoli_processes=(
    "ecoli_fatty_acid_degradation"
    "ecoli_fatty_acid_synthesis"
    "ecoli_homologous_recombination"
    "ecoli_outer_membrane_assembly"
    "ecoli_transcription_elongation"
    "ecoli_transcription_termination"
    "ecoli_translation_elongation"
    "ecoli_translation_termination"
)

for process in "${ecoli_processes[@]}"; do
    echo "📁 Uploading ${process}.json..."
    gsutil cp "$PROCESS_DIR/ecoli/${process}.json" \
      "$GCS_BUCKET/glmp-v2/processes/ecoli/${process}.json"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📤 Deploying Yeast Processes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Yeast processes
yeast_processes=(
    "yeast_chromatin_silencing"
    "yeast_er_stress_response"
    "yeast_gcn4_starvation"
    "yeast_nitrogen_metabolism"
    "yeast_pka_pathway"
    "yeast_rna_splicing"
    "yeast_snf1_pathway"
    "yeast_vesicle_trafficking"
)

for process in "${yeast_processes[@]}"; do
    echo "📁 Uploading ${process}.json..."
    gsutil cp "$PROCESS_DIR/yeast/${process}.json" \
      "$GCS_BUCKET/glmp-v2/processes/yeast/${process}.json"
done

echo ""
echo "🔄 Setting cache-control headers (no-cache)..."
gsutil -m setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_fatty_acid_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_homologous_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_outer_membrane_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_transcript*.json" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_translat*.json" \
    "$GCS_BUCKET/glmp-v2/processes/yeast/yeast_*.json"

echo ""
echo "✅ All syntax fixes deployed successfully!"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ PHASE 1 DEPLOYMENT COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 WHAT WAS DEPLOYED:"
echo ""
echo "  ✅ 16 processes with syntax errors fixed"
echo "  ✅ 20 bracket conflicts resolved"
echo "  ✅ 23 wrong trapezoid syntax corrected"
echo ""
echo "  All these processes should now render without Mermaid errors!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 VERIFICATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Wait 5 minutes for GCS propagation, then:"
echo ""
echo "  1. Visit any of the 16 fixed processes in the viewer"
echo "  2. Verify graphs render WITHOUT 'Syntax Error in text' message"
echo "  3. All red trapezoids should display correctly"
echo "  4. No broken/missing nodes"
echo ""
echo "  Test these first:"
echo "    - ecoli_transcription_termination (had 4 bracket conflicts)"
echo "    - yeast_pka_pathway (had 6 syntax errors)"
echo "    - yeast_chromatin_silencing (had 2 brackets + 3 syntax)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎉 Phase 1 complete! All syntax errors fixed."
echo "📋 Ready for Phase 2: Logic gate fixes (21 errors in 7 processes)"
echo ""
