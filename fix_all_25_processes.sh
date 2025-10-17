#!/bin/bash

echo "=========================================="
echo "🎨 FIXING COLORS IN 25 PROCESSES"
echo "=========================================="
echo ""

# List of 25 processes to fix
PROCESSES=(
    "bacillus/bacillus_biofilm_formation"
    "yeast/yeast_mitochondrial_biogenesis"
    "yeast/yeast_er_stress_response"
    "ecoli/ecoli_pentose_phosphate_pathway"
    "ecoli/ecoli_phage_defense"
    "yeast/yeast_chromatin_silencing"
    "yeast/yeast_vesicle_trafficking"
    "yeast/yeast_rna_splicing"
    "yeast/yeast_nitrogen_metabolism"
    "ecoli/ecoli_fatty_acid_degradation"
    "ecoli/ecoli_sulfur_metabolism"
    "ecoli/ecoli_outer_membrane_assembly"
    "ecoli/ecoli_amino_acid_biosynthesis"
    "ecoli/ecoli_nucleotide_biosynthesis"
    "yeast/yeast_mapk_mating"
    "yeast/yeast_pka_pathway"
    "yeast/yeast_snf1_pathway"
    "yeast/yeast_gcn4_starvation"
    "yeast/yeast_cell_wall_integrity"
    "ecoli/ecoli_tryptophan_biosynthesis"
    "ecoli/ecoli_phosphate_transport"
    "ecoli/ecoli_heat_shock_response"
    "ecoli/ecoli_acid_resistance"
    "ecoli/ecoli_two_component_signaling"
    "ecoli/ecoli_anaerobic_respiration"
)

FIXED=0
FAILED=0

for process in "${PROCESSES[@]}"; do
    FILE="gcs-processes/${process}.json"
    
    if [ ! -f "$FILE" ]; then
        echo "⚠️  SKIPPED: $process (file not found)"
        ((FAILED++))
        continue
    fi
    
    echo "🔧 Fixing: $process"
    python3 fix_process_colors.py "$FILE"
    
    if [ $? -eq 0 ]; then
        ((FIXED++))
    else
        echo "❌ FAILED: $process"
        ((FAILED++))
    fi
done

echo ""
echo "=========================================="
echo "✅ FIXED: $FIXED processes"
if [ $FAILED -gt 0 ]; then
    echo "⚠️  FAILED/SKIPPED: $FAILED processes"
fi
echo "=========================================="
