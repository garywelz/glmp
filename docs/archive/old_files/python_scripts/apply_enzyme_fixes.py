#!/usr/bin/env python3
"""
Apply Enzyme Misclassification Fixes
=====================================
Updates enzyme nodes to amber color based on enzyme_fixes.json
"""

import json
import re
from pathlib import Path

def apply_fixes_to_process(json_path, fixes):
    """Apply color fixes to a process file"""
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        mermaid = data['mermaid']
        changes = 0
        
        for fix in fixes:
            node_id = fix['node_id']
            old_color = fix['current']
            new_color = fix['new']
            
            # Find and replace style statement
            old_style = f'style {node_id} fill:#{old_color}'
            new_style = f'style {node_id} fill:#{new_color}'
            
            if old_style in mermaid:
                mermaid = mermaid.replace(old_style, new_style, 1)
                changes += 1
            else:
                # Try with color variations (with/without text color)
                pattern = rf'style {node_id} fill:#{old_color}[^,\n]*'
                if re.search(pattern, mermaid):
                    mermaid = re.sub(pattern, new_style + ',color:#000', mermaid, count=1)
                    changes += 1
        
        if changes > 0:
            data['mermaid'] = mermaid
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        return {
            'success': True,
            'changes': changes,
            'expected': len(fixes)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Main execution"""
    
    print("=" * 70)
    print("🔧 APPLYING ENZYME FIXES")
    print("=" * 70)
    print()
    
    # Load fixes
    fixes_path = Path('/workspace/enzyme_fixes.json')
    if not fixes_path.exists():
        print("❌ enzyme_fixes.json not found!")
        print("Make sure you're in the right directory.")
        return 1
    
    with open(fixes_path, 'r') as f:
        all_fixes = json.load(f)
    
    total_fixes = sum(len(fixes) for fixes in all_fixes.values())
    print(f"Loaded fixes for {len(all_fixes)} processes")
    print(f"Total enzyme nodes to fix: {total_fixes}")
    print()
    
    # Apply fixes
    gcs_dir = Path('/workspace/gcs-processes')
    
    results = []
    total_applied = 0
    
    for process_id, fixes in sorted(all_fixes.items()):
        # Find the process file
        json_files = list(gcs_dir.rglob(f'{process_id}.json'))
        
        if not json_files:
            print(f"⚠️  {process_id}: File not found")
            continue
        
        json_path = json_files[0]
        result = apply_fixes_to_process(json_path, fixes)
        
        if result['success']:
            changes = result['changes']
            expected = result['expected']
            total_applied += changes
            
            if changes == expected:
                print(f"✓ {process_id}: {changes} enzymes fixed")
            else:
                print(f"⚠️  {process_id}: {changes}/{expected} fixes applied")
        else:
            print(f"✗ {process_id}: {result['error']}")
        
        results.append(result)
    
    # Summary
    print()
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"  Processes processed: {len(results)}")
    print(f"  Total fixes applied: {total_applied}/{total_fixes}")
    print()
    
    if total_applied == total_fixes:
        print("✅ All enzyme fixes applied successfully!")
        print()
        print("Next steps:")
        print("1. Review a few processes in viewer (before deploying)")
        print("2. Deploy to GCS:")
        print("   gsutil -m cp -r gcs-processes/* \\")
        print("     gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/")
        print("3. Hard refresh browser to see changes")
    else:
        print(f"⚠️  {total_fixes - total_applied} fixes not applied")
        print("Review the warnings above")
    
    return 0 if total_applied == total_fixes else 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
