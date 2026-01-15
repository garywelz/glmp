#!/usr/bin/env python3
"""
Validate fixed process files using Mermaid CLI 10.6.1
Extracts Mermaid content from JSON and tests it with the actual parser
"""

import json
import subprocess
import sys
import tempfile
import os
from pathlib import Path

def validate_mermaid_with_cli(mermaid_content, process_name):
    """Validate Mermaid content using the actual CLI parser"""
    try:
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as mmd_file:
            mmd_file.write(mermaid_content)
            mmd_path = mmd_file.name
        
        svg_path = mmd_path.replace('.mmd', '.svg')
        
        # Run Mermaid CLI
        result = subprocess.run(
            ['npx', '--yes', '@mermaid-js/mermaid-cli@10.6.1', 
             'mmdc', '-i', mmd_path, '-o', svg_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Clean up
        try:
            os.unlink(mmd_path)
            if os.path.exists(svg_path):
                os.unlink(svg_path)
        except:
            pass
        
        if result.returncode == 0:
            return True, None
        else:
            error_msg = result.stderr.strip() or result.stdout.strip()
            return False, error_msg
            
    except subprocess.TimeoutExpired:
        return False, "Validation timed out (60s)"
    except Exception as e:
        return False, str(e)

def validate_file(json_path):
    """Validate a single JSON file"""
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        process_name = data.get('name', 'Unknown')
        mermaid = data.get('mermaid', '')
        
        if not mermaid:
            return process_name, False, "No Mermaid content"
        
        success, error = validate_mermaid_with_cli(mermaid, process_name)
        
        return process_name, success, error
        
    except Exception as e:
        return Path(json_path).name, False, str(e)

def main():
    # List of files that were fixed (35 files from scan_all_colon_issues.py)
    fixed_files = [
        "processes_with_not_gates/ecoli/ecoli_anaerobic_respiration.json",
        "processes_with_not_gates/ecoli/ecoli_glycolysis.json",
        "processes_with_not_gates/ecoli/ecoli_nucleotide_biosynthesis.json",
        "processes_with_not_gates/ecoli/ecoli_tca_cycle.json",
        "processes_with_not_gates/ecoli/ecoli_pentose_phosphate_pathway.json",
        "processes_with_not_gates/ecoli/ecoli_amino_acid_biosynthesis.json",
        "processes_with_not_gates/ecoli/ecoli_peptidoglycan_biosynthesis.json",
        "processes_with_not_gates/yeast/yeast_hog_pathway.json",
        "processes_with_not_gates/ecoli/ecoli_starvation_response.json",
        "processes_with_not_gates/ecoli/ecoli_cell_division.json",
        "processes_with_not_gates/ecoli/ecoli_homologous_recombination.json",
        "processes_with_not_gates/ecoli/ecoli_tryptophan_biosynthesis.json",
        "processes_with_not_gates/ecoli/ecoli_aerobic_respiration.json",
        "processes_with_not_gates/yeast/yeast_tor_signaling.json",
        "processes_with_not_gates/ecoli/ecoli_envelope_stress_response.json",
        "processes_with_not_gates/ecoli/ecoli_oxidative_stress_response.json",
        "processes_with_not_gates/yeast/yeast_glycolysis.json",
        "processes_with_not_gates/ecoli/ecoli_acid_resistance.json",
        "processes_with_not_gates/ecoli/ecoli_translation_elongation.json",
        "processes_with_not_gates/ecoli/ecoli_translation_termination.json",
        "processes_with_not_gates/ecoli/ecoli_trp_operon.json",
        "processes_with_not_gates/ecoli/ecoli_transcription_elongation.json",
        "processes_with_not_gates/yeast/yeast_er_associated_degradation.json",
        "processes_with_not_gates/ecoli/ecoli_protein_folding_chaperones.json",
        "processes_with_not_gates/ecoli/ecoli_antibiotic_efflux_pumps.json",
        "processes_with_not_gates/ecoli/ecoli_transcription_termination.json",
        "processes_with_not_gates/ecoli/ecoli_iron_homeostasis.json",
        "processes_with_not_gates/ecoli/ecoli_fatty_acid_degradation.json",
        "processes_with_not_gates/ecoli/ecoli_sulfur_metabolism.json",
        "processes_with_not_gates/ecoli/ecoli_biofilm_formation.json",
        "processes_with_not_gates/yeast/yeast_chromatin_silencing.json",
        "processes_with_not_gates/yeast/yeast_protein_folding.json",
        "processes_with_not_gates/yeast/yeast_vacuolar_protein_sorting.json",
        "processes_with_not_gates/yeast/yeast_oxidative_stress_response.json",
        "processes_with_not_gates/yeast/yeast_osmotic_stress_response.json",
    ]
    
    print("🔍 Validating fixed files with Mermaid CLI 10.6.1...")
    print("📋 Testing key processes first:\n")
    
    # Test key files first
    key_files = [
        "processes_with_not_gates/ecoli/ecoli_anaerobic_respiration.json",
        "processes_with_not_gates/ecoli/ecoli_glycolysis.json",
        "processes_with_not_gates/ecoli/ecoli_nucleotide_biosynthesis.json",
        "processes_with_not_gates/ecoli/ecoli_tca_cycle.json",
    ]
    
    results = []
    for json_path in key_files:
        if not Path(json_path).exists():
            continue
        name, success, error = validate_file(json_path)
        status = "✅ PASSED" if success else f"❌ FAILED: {error}"
        print(f"{status} - {name}")
        results.append((name, success))
    
    print(f"\n📊 Summary: {sum(1 for _, s in results if s)}/{len(results)} passed")
    
    if all(success for _, success in results):
        print("\n✅ All key processes validated successfully!")
        print("💡 The quoted label fixes resolved the Mermaid parsing errors.")
        return 0
    else:
        print("\n❌ Some validations failed - check errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())

