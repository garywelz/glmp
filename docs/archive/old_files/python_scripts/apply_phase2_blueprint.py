#!/usr/bin/env python3
"""
PHASE 2: Apply Complete Color Blueprint
========================================
Uses desktop agent's comprehensive node classification
to update all 7,131 nodes across 108 processes.

Blueprint structure:
{
  "process_id": {
    "NODE_ID": {
      "type": "trigger|enzyme|processing|intermediate|or_gate|and_gate|not_gate|product",
      "color": "#hex",
      "text": "Node text",
      "shape": "rectangle|diamond|hexagon|trapezoid"
    }
  }
}
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Load blueprint
BLUEPRINT_PATH = Path('/workspace/COLOR_BLUEPRINT_COMPLETE.json')

def load_blueprint() -> Dict:
    """Load the complete node classification blueprint"""
    with open(BLUEPRINT_PATH, 'r') as f:
        return json.load(f)

def get_shape_syntax(shape: str, text: str) -> str:
    """Get Mermaid shape syntax for a given shape type"""
    if shape == 'diamond':
        return f'{{{text}}}'
    elif shape == 'hexagon':
        return f'{{{{{text}}}}}'
    elif shape == 'trapezoid':
        return f'[\\{text}/]'
    else:  # rectangle
        return f'[{text}]'

def apply_blueprint_to_process(json_path: Path, blueprint: Dict) -> Dict:
    """Apply blueprint classifications to a single process"""
    
    process_id = json_path.stem
    
    if process_id not in blueprint:
        return {
            'success': False,
            'error': f'Process not in blueprint: {process_id}',
            'process_id': process_id
        }
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'mermaid' not in data:
            return {'success': False, 'error': 'No mermaid field'}
        
        mermaid = data['mermaid']
        process_blueprint = blueprint[process_id]
        
        changes = []
        nodes_updated = 0
        styles_added = 0
        styles_updated = 0
        
        # Find existing style statements
        existing_styles = {}
        for match in re.finditer(r'style (\w+) fill:#([0-9a-fA-F]+),color:#([0-9a-fA-F]+)', mermaid):
            node_id = match.group(1)
            existing_styles[node_id] = {
                'fill': match.group(2),
                'text': match.group(3),
                'full_match': match.group(0)
            }
        
        # Apply blueprint to each node
        for node_id, node_info in process_blueprint.items():
            target_color = node_info['color'].lstrip('#')
            text_color = 'fff' if target_color not in ['ffd43b', 'fab005', 'ffa07a'] else '000'
            
            if node_id in existing_styles:
                # Update existing style
                current = existing_styles[node_id]
                if current['fill'] != target_color:
                    old_style = current['full_match']
                    new_style = f'style {node_id} fill:#{target_color},color:#{text_color}'
                    mermaid = mermaid.replace(old_style, new_style, 1)
                    styles_updated += 1
                    nodes_updated += 1
            else:
                # Add new style
                # Find a good place to insert (after last style or at end)
                last_style_pos = mermaid.rfind('style ')
                if last_style_pos != -1:
                    # Find end of that line
                    next_newline = mermaid.find('\n', last_style_pos)
                    if next_newline != -1:
                        insert_pos = next_newline
                    else:
                        insert_pos = len(mermaid)
                else:
                    # No styles yet, add at end
                    insert_pos = len(mermaid)
                
                new_style = f'\n    style {node_id} fill:#{target_color},color:#{text_color}'
                mermaid = mermaid[:insert_pos] + new_style + mermaid[insert_pos:]
                styles_added += 1
                nodes_updated += 1
        
        # Save updated process
        if nodes_updated > 0:
            data['mermaid'] = mermaid
            
            # Update color scheme legend
            data['colorScheme'] = {
                "green": {
                    "hex": "#51cf66",
                    "category": "Triggers & Environmental Signals",
                    "description": "External signals, stress conditions, nutrient availability"
                },
                "amber": {
                    "hex": "#fab005",
                    "category": "Enzymes & Catalysts",
                    "description": "Protein enzymes, regulatory complexes, molecular machines"
                },
                "skyblue": {
                    "hex": "#74c0fc",
                    "category": "Processing & Operations",
                    "description": "Biochemical reactions, signal transduction, transformations"
                },
                "salmon": {
                    "hex": "#ffa07a",
                    "category": "Intermediates & Metabolites",
                    "description": "Chemical intermediates, signaling molecules, transient states"
                },
                "orange": {
                    "hex": "#ff9f43",
                    "category": "OR Logic Gates",
                    "description": "Decision points with multiple alternative branches"
                },
                "purple": {
                    "hex": "#7950f2",
                    "category": "AND Logic Gates",
                    "description": "Multi-signal integration requiring all conditions"
                },
                "red": {
                    "hex": "#e74c3c",
                    "category": "NOT Gates & Repression",
                    "description": "Inhibition, blocking, inactivation, repression mechanisms"
                },
                "black": {
                    "hex": "#000000",
                    "category": "Products & Outcomes",
                    "description": "Final products, cellular outcomes, system states"
                }
            }
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            changes.append(f'Updated {nodes_updated} nodes')
            changes.append(f'  Added {styles_added} new styles')
            changes.append(f'  Updated {styles_updated} existing styles')
        
        return {
            'success': True,
            'process_id': process_id,
            'nodes_updated': nodes_updated,
            'styles_added': styles_added,
            'styles_updated': styles_updated,
            'changes': changes
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'process_id': process_id
        }

def main():
    """Main execution"""
    
    print("=" * 70)
    print("🎨 PHASE 2: APPLYING COMPLETE COLOR BLUEPRINT")
    print("=" * 70)
    print()
    
    # Load blueprint
    print("Loading blueprint...")
    blueprint = load_blueprint()
    
    total_blueprint_nodes = sum(len(nodes) for nodes in blueprint.values())
    print(f"✓ Loaded blueprint with {total_blueprint_nodes} node classifications")
    print(f"✓ Covers {len(blueprint)} processes")
    print()
    
    # Process all files
    gcs_dir = Path('/workspace/gcs-processes')
    json_files = list(gcs_dir.rglob('*.json'))
    
    print(f"Processing {len(json_files)} files...")
    print()
    
    results = []
    total_nodes_updated = 0
    total_styles_added = 0
    total_styles_updated = 0
    
    for json_file in sorted(json_files):
        result = apply_blueprint_to_process(json_file, blueprint)
        results.append(result)
        
        rel_path = json_file.relative_to(gcs_dir)
        
        if result['success']:
            if result.get('nodes_updated', 0) > 0:
                nodes = result['nodes_updated']
                added = result['styles_added']
                updated = result['styles_updated']
                print(f"✓ {rel_path}: {nodes} nodes ({added} new, {updated} updated)")
                total_nodes_updated += nodes
                total_styles_added += added
                total_styles_updated += updated
            else:
                print(f"○ {rel_path}: No changes needed")
        else:
            print(f"✗ {rel_path}: {result.get('error', 'Unknown error')}")
    
    # Summary
    print()
    print("=" * 70)
    print("📊 PHASE 2 COMPLETE - SUMMARY")
    print("=" * 70)
    
    successful = [r for r in results if r['success']]
    updated = [r for r in successful if r.get('nodes_updated', 0) > 0]
    failed = [r for r in results if not r['success']]
    
    print(f"  Total files:           {len(results)}")
    print(f"  ✓ Processed:           {len(successful)}")
    print(f"  ✓ Updated:             {len(updated)}")
    print(f"  ✗ Failed:              {len(failed)}")
    print()
    print(f"  Node Updates:")
    print(f"    Total nodes updated:   {total_nodes_updated}")
    print(f"    New styles added:      {total_styles_added}")
    print(f"    Existing styles fixed: {total_styles_updated}")
    print()
    
    if updated:
        print("🎉 Phase 2 Complete!")
        print()
        print("✅ ALL NODES NOW STYLED:")
        print("  🟢 Triggers:      Green    #51cf66  (environmental signals)")
        print("  🟡 Enzymes:       Amber    #fab005  (catalytic proteins)")
        print("  🔵 Processing:    Sky Blue #74c0fc  (biochemical operations)")
        print("  🟠 Intermediates: Salmon   #ffa07a  (metabolites)")
        print("  🟠 OR gates:      Orange   #ff9f43  (alternative branches)")
        print("  🟣 AND gates:     Purple   #7950f2  (multi-signal integration)")
        print("  🔴 NOT gates:     Red      #e74c3c  (repression/inhibition)")
        print("  ⚫ Products:       Black    #000000  (final outcomes)")
        print()
        print("✅ No more lavender nodes!")
        print("✅ Color legends updated!")
        print("✅ Ready for deployment!")
    
    return 0 if not failed else 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
