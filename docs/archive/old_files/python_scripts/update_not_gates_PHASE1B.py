#!/usr/bin/env python3
"""
PHASE 1B: Add NOT Gate Visualization
=====================================
Using exact node IDs from desktop agent analysis.

Updates:
- Convert specific NOT gate nodes to inverted trapezoid shape
- Apply red color (#e74c3c) with white text
- Uses precise node IDs, no keyword guessing
"""

import json
from pathlib import Path

# Load NOT gate node IDs
with open('/workspace/not_gate_node_ids.json', 'r') as f:
    NOT_GATE_NODES = json.load(f)

def update_not_gate_nodes(json_path: Path) -> dict:
    """Update NOT gate nodes in a process to red trapezoids"""
    
    process_id = json_path.stem
    
    # Check if this process has NOT gates
    not_node_ids = NOT_GATE_NODES.get(process_id, [])
    
    if not not_node_ids:
        return {'success': True, 'changes': [], 'process_id': process_id}
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'mermaid' not in data:
            return {'success': False, 'error': 'No mermaid field'}
        
        mermaid = data['mermaid']
        changes = []
        
        # For each NOT gate node ID, convert to trapezoid and add red style
        for node_id in not_node_ids:
            # Find and replace node definition
            # Try different shapes: [Text], {Text}, (Text), ((Text))
            
            # Rectangle: A[Text]
            import re
            rect_pattern = rf'({node_id})\[([^\]]+)\]'
            rect_match = re.search(rect_pattern, mermaid)
            if rect_match:
                full_match = rect_match.group(0)
                text = rect_match.group(2)
                replacement = f'{node_id}[\\{text}/]'
                mermaid = mermaid.replace(full_match, replacement, 1)
                changes.append(f'NOT {node_id} → trapezoid')
            
            # Diamond: A{Text}
            diamond_pattern = rf'({node_id})\{{([^}}]+)\}}'
            diamond_match = re.search(diamond_pattern, mermaid)
            if diamond_match:
                full_match = diamond_match.group(0)
                text = diamond_match.group(2)
                replacement = f'{node_id}[\\{text}/]'
                mermaid = mermaid.replace(full_match, replacement, 1)
                changes.append(f'NOT {node_id} → trapezoid')
            
            # Add or update style to red
            style_pattern = rf'style {node_id} fill:#[0-9a-fA-F]+,color:#[0-9a-fA-F]+'
            if re.search(style_pattern, mermaid):
                # Update existing style
                mermaid = re.sub(style_pattern, f'style {node_id} fill:#e74c3c,color:#fff', mermaid)
                changes.append(f'NOT {node_id} → red')
            else:
                # Add new style
                # Find last style statement
                last_style = mermaid.rfind('style ')
                if last_style != -1:
                    # Find end of that line
                    next_newline = mermaid.find('\n', last_style)
                    if next_newline != -1:
                        mermaid = mermaid[:next_newline] + f'\n    style {node_id} fill:#e74c3c,color:#fff' + mermaid[next_newline:]
                    else:
                        mermaid += f'\n    style {node_id} fill:#e74c3c,color:#fff'
                else:
                    # No existing styles, add at end
                    mermaid += f'\n    style {node_id} fill:#e74c3c,color:#fff'
                changes.append(f'NOT {node_id} → red (new style)')
        
        # Save if changed
        if changes:
            data['mermaid'] = mermaid
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        return {'success': True, 'changes': changes, 'process_id': process_id, 'not_count': len(not_node_ids)}
        
    except Exception as e:
        return {'success': False, 'error': str(e), 'process_id': process_id}

def main():
    """Main execution"""
    
    print("=" * 70)
    print("🔴 PHASE 1B: NOT GATE VISUALIZATION")
    print("=" * 70)
    print()
    print("Using exact node IDs from desktop agent analysis")
    print()
    print("Updates:")
    print("  Shape: [Text] or {Text} → [\\Text/] (inverted trapezoid)")
    print("  Color: Any → Red #e74c3c")
    print("  Text: White #fff")
    print()
    print(f"Processes with NOT gates: {len(NOT_GATE_NODES)}")
    print()
    print("=" * 70)
    print()
    
    # Find all process files
    gcs_dir = Path('/workspace/gcs-processes')
    json_files = list(gcs_dir.rglob('*.json'))
    
    results = []
    for json_file in sorted(json_files):
        result = update_not_gate_nodes(json_file)
        results.append(result)
        
        rel_path = json_file.relative_to(gcs_dir)
        if result['success']:
            if result['changes']:
                not_count = result.get('not_count', 0)
                print(f"✓ {rel_path} ({not_count} NOT gates)")
                for change in result['changes']:
                    print(f"  → {change}")
            # Don't print "no changes" to keep output clean
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
    
    print(f"  Total files:           {len(results)}")
    print(f"  ✓ NOT gates added:     {len(updated)}")
    print(f"  ⊘ No NOT gates:        {len(unchanged)}")
    print(f"  ✗ Failed:              {len(failed)}")
    print()
    
    if updated:
        total_not_gates = sum(r.get('not_count', 0) for r in updated)
        print(f"  Total NOT gates visualized: {total_not_gates}")
        print()
        print("🎉 Phase 1B complete!")
        print()
        print("All 3 logic gate types now have unique shapes:")
        print("  🟠 OR gates:  Orange diamond ◆")
        print("  🟣 AND gates: Purple hexagon ⬡")
        print("  🔴 NOT gates: Red trapezoid ⏷")
        print()
        print("Next: Review changes, commit, and proceed to Phase 1C (products → black)")
    
    return 0 if not failed else 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
