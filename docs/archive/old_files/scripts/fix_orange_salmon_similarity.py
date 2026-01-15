#!/usr/bin/env python3
"""
Fix Orange/Salmon Color Similarity
===================================
Updates OR gates to darker orange for better distinction from salmon intermediates

Issue: #ff9f43 (orange) too similar to #ffa07a (salmon)
Solution: Change OR gates to #ff8c1a (darker orange with better contrast)
"""

import json
import re
from pathlib import Path

OLD_OR_COLOR = 'ff9f43'
NEW_OR_COLOR = 'ff8c1a'  # Darker orange

def update_or_gate_color(json_path: Path) -> dict:
    """Update OR gate color in a process"""
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        mermaid = data['mermaid']
        
        # Find OR gate nodes (diamonds)
        # Look for style statements with old orange color
        pattern = rf'style (\w+) fill:#{OLD_OR_COLOR}'
        matches = list(re.finditer(pattern, mermaid))
        
        if not matches:
            return {'success': True, 'changes': 0, 'process_id': json_path.stem}
        
        # Verify these are actually OR gates (diamonds)
        or_gates_updated = 0
        for match in matches:
            node_id = match.group(1)
            
            # Check if this node is a diamond (OR gate)
            diamond_pattern = rf'{node_id}\{{[^}}]+\}}'
            if re.search(diamond_pattern, mermaid):
                # This is an OR gate, update its color
                old_style = f'style {node_id} fill:#{OLD_OR_COLOR}'
                new_style = f'style {node_id} fill:#{NEW_OR_COLOR}'
                mermaid = mermaid.replace(old_style, new_style, 1)
                or_gates_updated += 1
        
        if or_gates_updated > 0:
            data['mermaid'] = mermaid
            
            # Update color legend
            if 'colorScheme' in data and 'orange' in data['colorScheme']:
                data['colorScheme']['orange']['hex'] = f'#{NEW_OR_COLOR}'
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        return {
            'success': True,
            'changes': or_gates_updated,
            'process_id': json_path.stem
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'process_id': json_path.stem
        }

def main():
    """Main execution"""
    
    print("=" * 70)
    print("🎨 FIXING ORANGE/SALMON COLOR SIMILARITY")
    print("=" * 70)
    print()
    print("Issue: OR gates (orange) too similar to intermediates (salmon)")
    print()
    print(f"Solution: Change OR gates from #{OLD_OR_COLOR} to #{NEW_OR_COLOR}")
    print("  (Darker orange with better contrast)")
    print()
    print("=" * 70)
    print()
    
    # Find all process files
    gcs_dir = Path('/workspace/gcs-processes')
    json_files = list(gcs_dir.rglob('*.json'))
    
    results = []
    total_updated = 0
    
    for json_file in sorted(json_files):
        result = update_or_gate_color(json_file)
        results.append(result)
        
        if result['success'] and result['changes'] > 0:
            rel_path = json_file.relative_to(gcs_dir)
            print(f"✓ {rel_path}: {result['changes']} OR gates updated")
            total_updated += result['changes']
    
    # Summary
    print()
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    
    updated = [r for r in results if r['success'] and r['changes'] > 0]
    failed = [r for r in results if not r['success']]
    
    print(f"  Processes updated:    {len(updated)}")
    print(f"  Total OR gates:       {total_updated}")
    print(f"  Failed:               {len(failed)}")
    print()
    
    if total_updated > 0:
        print("✅ Color similarity issue fixed!")
        print()
        print("New color scheme:")
        print(f"  🟠 OR gates:      Darker Orange #{NEW_OR_COLOR}")
        print(f"  🟠 Intermediates: Salmon        #ffa07a")
        print()
        print("Much better visual distinction! 🎨")
    
    return 0 if not failed else 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
