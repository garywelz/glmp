#!/bin/bash

# Deploy ALL 18 Fixed Processes (Complete Deployment)
# Includes: 2 user-reported + 16 Phase 1 auto-fixed

set -e

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║           🚀 DEPLOYING ALL 18 FIXED PROCESSES (COMPLETE)                     ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
GCS_BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
PROCESS_DIR="/workspace/processes_with_not_gates"

echo "📦 COMPLETE DEPLOYMENT MANIFEST"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  🎯 USER-REPORTED PROCESSES (3):"
echo "    1. ecoli_amino_acid_biosynthesis (6 logic fixes)"
echo "    2. ecoli_anaerobic_respiration (4 syntax fixes)"
echo "    3. ecoli_biofilm_formation (1 syntax fix)"
echo ""
echo "  🔧 PHASE 1 AUTO-FIXED PROCESSES (16):"
echo ""
echo "  E. coli (8):"
echo "    3. fatty_acid_degradation"
echo "    4. fatty_acid_synthesis"
echo "    5. homologous_recombination"
echo "    6. outer_membrane_assembly"
echo "    7. transcription_elongation"
echo "    8. transcription_termination"
echo "    9. translation_elongation"
echo "    10. translation_termination"
echo ""
echo "  Yeast (8):"
echo "    11. chromatin_silencing"
echo "    12. er_stress_response"
echo "    13. gcn4_starvation"
echo "    14. nitrogen_metabolism"
echo "    15. pka_pathway"
echo "    16. rna_splicing"
echo "    17. snf1_pathway"
echo "    18. vesicle_trafficking"
echo ""
echo "  TOTAL: 18 processes with all fixes"
echo ""

read -p "🔐 Deploy all 18 processes? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📤 PART 1: Deploying User-Reported Processes (2)"
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
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📤 PART 2: Deploying E. coli Phase 1 Processes (8)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

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

counter=3
for process in "${ecoli_processes[@]}"; do
    echo "📁 ${counter}. ${process}.json..."
    gsutil cp "$PROCESS_DIR/ecoli/${process}.json" \
      "$GCS_BUCKET/glmp-v2/processes/ecoli/${process}.json"
    counter=$((counter + 1))
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📤 PART 3: Deploying Yeast Phase 1 Processes (8)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

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

counter=11
for process in "${yeast_processes[@]}"; do
    echo "📁 ${counter}. ${process}.json..."
    gsutil cp "$PROCESS_DIR/yeast/${process}.json" \
      "$GCS_BUCKET/glmp-v2/processes/yeast/${process}.json"
    counter=$((counter + 1))
done

echo ""
echo "🔄 Setting cache-control headers (AGGRESSIVE - force refresh)..."
gsutil -m setmeta -h "Cache-Control:no-cache, no-store, must-revalidate, max-age=0" \
    -h "Pragma:no-cache" \
    -h "Expires:0" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_amino_acid_biosynthesis.json" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_anaerobic_respiration.json" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_biofilm_formation.json" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_fatty_acid_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_homologous_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_outer_membrane_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_transcript*.json" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_translat*.json" \
    "$GCS_BUCKET/glmp-v2/processes/yeast/yeast_chromatin_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/yeast/yeast_er_stress_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/yeast/yeast_gcn4_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/yeast/yeast_nitrogen_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/yeast/yeast_pka_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/yeast/yeast_rna_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/yeast/yeast_snf1_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/yeast/yeast_vesicle_*.json"

echo ""
echo "✅ All 18 processes deployed successfully!"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ COMPLETE DEPLOYMENT FINISHED!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 DEPLOYED:"
echo "  ✅ 19 total processes"
echo "  ✅ 3 user-reported (amino_acid_biosynthesis, anaerobic_respiration, biofilm_formation)"
echo "  ✅ 16 Phase 1 auto-fixed"
echo ""
echo "  🔧 Fixes included:"
echo "    • 20 bracket conflicts resolved"
echo "    • 23 wrong trapezoid syntax corrected"
echo "    • 6 logic gate errors fixed (amino_acid_biosynthesis)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 VERIFICATION (After 5 min + Hard Refresh)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Test these critical processes:"
echo "    1. Amino Acid Biosynthesis - should show new OR/AND gates"
echo "    2. Anaerobic Respiration - should render without syntax errors"
echo "    3. Transcription Termination - should work (6 errors fixed)"
echo "    4. PKA Pathway - should work (6 errors fixed)"
echo ""
echo "  If still seeing errors:"
echo "    • Clear browser cache completely"
echo "    • Try incognito/private window"
echo "    • Wait 10 minutes for CDN propagation"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
