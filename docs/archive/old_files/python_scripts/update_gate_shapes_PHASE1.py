#!/usr/bin/env python3
"""
PHASE 1: Update Logic Gate Shapes and Colors ONLY
==================================================
Safe, targeted update:
- AND gates: Diamond {} → Hexagon {{}} + Purple #7950f2
- NOT gates: Add trapezoid shape [\Text/] + Red #e74c3c  
- Products: Violet → Black #000000

Does NOT touch other node colors (triggers, enzymes, processing, intermediates)
Those will be updated in Phase 2 after semantic analysis.

Uses exact NOT gate counts from desktop agent.
"""

import json
import re
from pathlib import Path
from typing import Dict, List

# NOT gate counts from desktop agent
NOT_GATE_COUNTS = {
    # High NOT (6-8)
    "yeast_tor_signaling": 8,
    "yeast_hog_pathway": 6,
    "yeast_pka_pathway": 6,
    "yeast_snf1_pathway": 6,
    
    # Moderate NOT (4-5)
    "ecoli_fatty_acid_degradation": 5,
    "yeast_gal_regulation": 5,
    "ecoli_catabolite_repression": 4,
    "ecoli_e._coli_acid_resistance": 4,
    "ecoli_lac_operon": 4,
    "ecoli_transcription_regulation": 4,
    "yeast_autophagy": 4,
    
    # Low NOT (2-3)
    "ecoli_anaerobic_respiration": 3,
    "ecoli_dna_damage_checkpoint": 3,
    "ecoli_e._coli_two_component_signaling": 3,
    "ecoli_heavy_metal_resistance": 3,
    "ecoli_sulfur_metabolism": 3,
    "ecoli_translation_initiation": 3,
    "ecoli_trp_operon": 3,
    "ecoli_two_component_signaling": 3,
    "yeast_chromatin_silencing": 3,
    "yeast_mapk_mating": 3,
    
    "bacillus_biofilm_formation": 2,
    "ecoli_ara_operon": 2,
    "ecoli_cold_shock_response": 2,
    "ecoli_dna_replication_termination": 2,
    "ecoli_pentose_phosphate_pathway": 2,
    "ecoli_pho_regulon": 2,
    "ecoli_phosphate_regulation": 2,
    "ecoli_transcription_termination": 2,
    "ecoli_tryptophan_biosynthesis": 2,
    "ecoli_type_iii_secretion": 2,
    "yeast_cell_wall_integrity": 2,
    "yeast_mating_type_switching": 2,
    "yeast_meiosis_regulation": 2,
    "yeast_nitrogen_metabolism": 2,
    "yeast_unfolded_protein_response": 2,
    "yeast_vesicle_trafficking": 2,
    
    # Single NOT (1)
    "bacillus_competence_development": 1,
    "ecoli_arginine_biosynthesis": 1,
    "ecoli_base_excision_repair": 1,
    "ecoli_biofilm_formation": 1,
    "ecoli_cell_division": 1,
    "ecoli_fatty_acid_synthesis": 1,
    "ecoli_iron_homeostasis": 1,
    "ecoli_outer_membrane_assembly": 1,
    "ecoli_oxidative_stress_response": 1,
    "ecoli_periplasmic_stress": 1,
    "ecoli_phosphate_transport": 1,
    "ecoli_rna_polymerase_recycling": 1,
    "ecoli_sigma_factor_competition": 1,
    "ecoli_e._coli_sos_response": 1,
    "ecoli_starvation_response": 1,
    "yeast_gcn4_starvation": 1,
    "yeast_mating_response": 1,
    "yeast_mitochondrial_biogenesis": 1,
    "yeast_osmotic_stress_response": 1,
}

def update_and_gates_to_hexagons(mermaid: str) -> tuple:
    """Convert AND gate diamonds to hexagons: {Text} → {{Text}}"""
    
    # Find all diamond nodes with AND gate colors (lavender/purple)
    and_count = 0
    
    # Pattern: NODEID{Text with AND in it}
    and_pattern = r'(\w+)\{([^}]*(?:AND|All.*(?:Present|Required)|Multi|Complex)[^}]*)\}'
    
    def replace_and(match):
        nonlocal and_count
        node_id = match.group(1)
        text = match.group(2)
        and_count += 1
        return f'{node_id}{{{{{text}}}}}'  # {{ }} for hexagon
    
    updated = re.sub(and_pattern, replace_and, mermaid, flags=re.IGNORECASE)
    
    return updated, and_count

def update_and_gate_colors(mermaid: str) -> tuple:
    """Update AND gate colors from lavender to deep purple"""
    
    count = 0
    
    # Update lavender to deep purple
    lavender_colors = ['#b4b4dc', '#b197fc']
    for old_color in lavender_colors:
        if f'fill:{old_color}' in mermaid:
            mermaid = mermaid.replace(f'fill:{old_color}', 'fill:#7950f2')
            count += 1
    
    return mermaid, count

def add_not_gate_visualization(mermaid: str, process_id: str) -> tuple:
    """Add NOT gate nodes as red inverted trapezoids"""
    
    # Check if this process has NOT gates
    expected_not_count = NOT_GATE_COUNTS.get(process_id, 0)
    
    if expected_not_count == 0:
        return mermaid, 0
    
    # Find nodes with NOT/repression keywords
    not_keywords = [
        r'\brepressor\b', r'\brepressed\b', r'\brepression\b',
        r'\bblocked?\b', r'\bblocking\b',
        r'\binhibit\w*\b', r'\bprevent\w*\b',
        r'\binactive\b', r'\bsuppress\w*\b',
        r'\bNOT:', r'\bnot\s'
    ]
    
    # Find node IDs with these keywords
    not_nodes = []
    for line in mermaid.split('\n'):
        for keyword_pattern in not_keywords:
            if re.search(keyword_pattern, line, re.IGNORECASE):
                # Extract node ID from line
                match = re.match(r'\s*(\w+)[\[{]', line)
                if match:
                    node_id = match.group(1)
                    if node_id not in not_nodes:
                        not_nodes.append(node_id)
                        if len(not_nodes) >= expected_not_count:
                            break
        if len(not_nodes) >= expected_not_count:
            break
    
    # Convert these nodes to trapezoids and add red styling
    for node_id in not_nodes[:expected_not_count]:
        # Find the node definition
        rect_pattern = rf'{node_id}\[([^\]]+)\]'
        diamond_pattern = rf'{node_id}\{{([^}}]+)\}}'
        
        # Try to replace with trapezoid
        rect_match = re.search(rect_pattern, mermaid)
        diamond_match = re.search(diamond_pattern, mermaid)
        
        if rect_match:
            text = rect_match.group(1)
            mermaid = mermaid.replace(
                f'{node_id}[{text}]',
                f'{node_id}[\\{text}/]'
            )
        elif diamond_match:
            text = diamond_match.group(1)
            mermaid = mermaid.replace(
                f'{node_id}{{{text}}}',
                f'{node_id}[\\{text}/]'
            )
        
        # Add or update style to red
        if f'style {node_id}' in mermaid:
            mermaid = re.sub(
                rf'style {node_id} fill:#[0-9a-fA-F]+,color:#[0-9a-fA-F]+',
                f'style {node_id} fill:#e74c3c,color:#fff',
                mermaid
            )
        else:
            # Add new style
            mermaid += f'\n    style {node_id} fill:#e74c3c,color:#fff'
    
    return mermaid, len(not_nodes[:expected_not_count])

def update_product_colors(mermaid: str) -> tuple:
    """Update product/output nodes from violet to black"""
    
    count = 0
    
    # Update violet variants to black
    violet_colors = ['#9775fa', '#b197fc']
    for old_color in violet_colors:
        if f'fill:{old_color}' in mermaid:
            mermaid = mermaid.replace(f'fill:{old_color}', 'fill:#000000')
            count += 1
    
    return mermaid, count

def update_process_gates(json_path: Path) -> dict:
    """Update gate shapes and colors in a single process"""
    
    process_id = json_path.stem
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'mermaid' not in data:
            return {'success': False, 'error': 'No mermaid field'}
        
        mermaid = data['mermaid']
        changes = []
        
        # Update AND gates to hexagons
        mermaid, and_count = update_and_gates_to_hexagons(mermaid)
        if and_count > 0:
            changes.append(f'{and_count} AND→hexagon')
        
        # Update AND gate colors
        mermaid, and_color_count = update_and_gate_colors(mermaid)
        if and_color_count > 0:
            changes.append(f'{and_color_count} AND→purple')
        
        # Add NOT gate visualization
        mermaid, not_count = add_not_gate_visualization(mermaid, process_id)
        if not_count > 0:
            changes.append(f'{not_count} NOT→trapezoid+red')
        
        # Update products to black
        mermaid, prod_count = update_product_colors(mermaid)
        if prod_count > 0:
            changes.append(f'{prod_count} products→black')
        
        # Save if changed
        if changes:
            data['mermaid'] = mermaid
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return {'success': True, 'changes': changes, 'process_id': process_id}
        else:
            return {'success': True, 'changes': [], 'process_id': process_id}
            
    except Exception as e:
        return {'success': False, 'error': str(e), 'process_id': process_id}

def main():
    """Main execution"""
    
    print("=" * 70)
    print("🎨 PHASE 1: LOGIC GATE SHAPES & COLORS UPDATE")
    print("=" * 70)
    print()
    print("Updates:")
    print("  ◆ → ⬡  AND gates: Diamond to Hexagon (purple #7950f2)")
    print("  + ⏷    NOT gates: Add trapezoid shape (red #e74c3c)")
    print("  🟣 → ⬛ Products: Violet to Black (#000000)")
    print()
    print("Does NOT change:")
    print("  - Trigger colors (will do in Phase 2)")
    print("  - Processing colors (will do in Phase 2)")
    print("  - Intermediate colors (will do in Phase 2)")
    print()
    print("=" * 70)
    print()
    
    # Find all process files
    gcs_dir = Path('/workspace/gcs-processes')
    json_files = list(gcs_dir.rglob('*.json'))
    
    print(f"Found {len(json_files)} processes to update")
    print()
    
    results = []
    for json_file in sorted(json_files):
        result = update_process_gates(json_file)
        results.append(result)
        
        rel_path = json_file.relative_to(gcs_dir)
        if result['success']:
            if result['changes']:
                print(f"✓ {rel_path}")
                for change in result['changes']:
                    print(f"  → {change}")
            else:
                print(f"⊘ {rel_path} (no gates to update)")
        else:
            print(f"✗ {rel_path}: {result['error']}")
    
    # Summary
    print()
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    
    updated = [r for r in results if r['success'] and r['changes']]
    unchanged = [r for r in results if r['success'] and not r['changes']]
    failed = [r for r in results if not r['success']]
    
    print(f"  Total files:    {len(results)}")
    print(f"  ✓ Updated:      {len(updated)}")
    print(f"  ⊘ No changes:   {len(unchanged)}")
    print(f"  ✗ Failed:       {len(failed)}")
    print()
    
    if updated:
        print("🎉 Phase 1 complete!")
        print()
        print("Changes made:")
        and_total = sum(1 for r in updated if any('AND' in c for c in r['changes']))
        not_total = sum(1 for r in updated if any('NOT' in c for c in r['changes']))
        prod_total = sum(1 for r in updated if any('products' in c for c in r['changes']))
        
        print(f"  - AND gates converted to hexagons: {and_total} processes")
        print(f"  - NOT gates visualized as trapezoids: {not_total} processes")
        print(f"  - Products updated to black: {prod_total} processes")
        print()
        print("Next: Review with 'git diff', then commit and deploy")
    
    return 0 if not failed else 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
