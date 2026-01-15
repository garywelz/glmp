#!/bin/bash

# Deploy Phase 2: Invalid Logic Gate Fixes
# Fixes AND/OR gates with wrong input/output counts

set -e

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║              🔧 DEPLOYING PHASE 2: LOGIC GATE FIXES                          ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
GCS_BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
PROCESS_DIR="/workspace/processes_with_not_gates"

echo "📦 DEPLOYMENT SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Processes Fixed: 8"
echo "  Invalid Gates Corrected: 31"
echo ""
echo "  Fixes Applied:"
echo "    • AND gates with < 2 inputs → Converted to rectangles"
echo "    • OR gates with < 2 outputs → Converted to rectangles"
echo ""
echo "  E. coli Processes (4):"
echo "    - flagellar_assembly (6 invalid AND gates)"
echo "    - stringent_response (4 invalid AND gates)"
echo "    - envelope_stress_response (2 invalid AND gates)"
echo "    - protein_folding_chaperones (11 invalid OR gates) ⚠️ MOST ERRORS"
echo ""
echo "  Yeast Processes (4):"
echo "    - osmotic_stress_response (1 invalid OR gate)"
echo "    - oxidative_stress_response (2 invalid OR gates)"
echo "    - glycolysis_regulation (1 invalid AND gate)"
echo "    - peroxisome_biogenesis (4 invalid AND gates)"
echo ""

read -p "🔐 Ready to deploy 8 fixed processes? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📤 Deploying Fixed Processes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# E. coli processes
echo "📁 E. coli processes..."
gsutil cp "$PROCESS_DIR/ecoli/ecoli_e._coli_flagellar_assembly.json" \
  "$GCS_BUCKET/glmp-v2/processes/ecoli/"
  
gsutil cp "$PROCESS_DIR/ecoli/ecoli_e._coli_stringent_response.json" \
  "$GCS_BUCKET/glmp-v2/processes/ecoli/"
  
gsutil cp "$PROCESS_DIR/ecoli/ecoli_envelope_stress_response.json" \
  "$GCS_BUCKET/glmp-v2/processes/ecoli/"
  
gsutil cp "$PROCESS_DIR/ecoli/ecoli_protein_folding_chaperones.json" \
  "$GCS_BUCKET/glmp-v2/processes/ecoli/"

# Yeast processes
echo "📁 Yeast processes..."
gsutil cp "$PROCESS_DIR/yeast/yeast_osmotic_stress_response.json" \
  "$GCS_BUCKET/glmp-v2/processes/yeast/"
  
gsutil cp "$PROCESS_DIR/yeast/yeast_oxidative_stress_response.json" \
  "$GCS_BUCKET/glmp-v2/processes/yeast/"
  
gsutil cp "$PROCESS_DIR/yeast/yeast_yeast_glycolysis_regulation.json" \
  "$GCS_BUCKET/glmp-v2/processes/yeast/"
  
gsutil cp "$PROCESS_DIR/yeast/yeast_yeast_peroxisome_biogenesis.json" \
  "$GCS_BUCKET/glmp-v2/processes/yeast/"

echo ""
echo "🔄 Setting cache-control headers (no-cache)..."
gsutil -m setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_e._coli_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_envelope_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/ecoli/ecoli_protein_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/yeast/yeast_osmotic_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/yeast/yeast_oxidative_*.json" \
    "$GCS_BUCKET/glmp-v2/processes/yeast/yeast_yeast_*.json"

echo ""
echo "✅ All logic gate fixes deployed successfully!"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ PHASE 2 DEPLOYMENT COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 WHAT WAS DEPLOYED:"
echo ""
echo "  ✅ 8 processes with invalid logic gates fixed"
echo "  ✅ 31 invalid gates converted to rectangles"
echo ""
echo "  Invalid gates are now regular nodes (rectangles)"
echo "  Graphs should render with correct logic flow"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 VERIFICATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Wait 5 minutes for GCS propagation, then:"
echo ""
echo "  1. Visit the fixed processes in the viewer"
echo "  2. Verify no invalid logic gates (purple hexagons with 1 input, etc.)"
echo "  3. Check that former invalid gates now show as regular rectangles"
echo ""
echo "  Test these first:"
echo "    - ecoli_protein_folding_chaperones (11 fixes)"
echo "    - ecoli_flagellar_assembly (6 fixes)"
echo "    - yeast_peroxisome_biogenesis (4 fixes)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎉 Phase 2 complete! All invalid logic gates fixed."
echo ""
