#!/usr/bin/env python3
"""
Fix triple curly braces to double curly braces in Mermaid code
Triple {{{ is invalid, should be double {{
"""

import json
from glob import glob
import re

def fix_process(filepath):
    """Fix triple curly braces in a process file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    mermaid = data.get('mermaid', '')
    original = mermaid
    
    # Replace {{{ with {{
    mermaid = mermaid.replace('{{{', '{{')
    # Replace }}} with }}
    mermaid = mermaid.replace('}}}', '}}')
    
    if mermaid != original:
        data['mermaid'] = mermaid
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    return False

def main():
    print("🔧 Fixing triple curly braces in Mermaid code...")
    print("=" * 70)
    print()
    
    files = glob('gcs-processes/*/*.json')
    fixed_count = 0
    
    for filepath in sorted(files):
        if fix_process(filepath):
            fixed_count += 1
            filename = filepath.split('/')[-1]
            print(f"✓ Fixed: {filename}")
    
    print()
    print("=" * 70)
    print(f"✅ Fixed {fixed_count} files")
    print()
    print("Next: Re-run deployment script to upload fixes")
    print("=" * 70)

if __name__ == "__main__":
    main()

