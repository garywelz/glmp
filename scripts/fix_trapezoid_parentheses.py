#!/usr/bin/env python3
"""
Fix parentheses inside trapezoid labels - replace with brackets
Mermaid parser can't handle (2Fe-2S) inside [/.../] syntax
"""

import json
import re
import sys

def fix_trapezoid_parentheses(mermaid_text):
    """Remove brackets and parentheses from inside trapezoid labels"""
    # Pattern to match trapezoid labels: [/...content.../]
    def replacer(match):
        label_content = match.group(1)
        # Remove brackets: [2Fe-2S] -> 2Fe-2S
        # Remove parentheses: (2Fe-2S) -> 2Fe-2S
        fixed = re.sub(r'[\[\]()]', '', label_content)
        return f'[/{fixed}/]'
    
    # Pattern: [/...content.../]
    pattern = r'\[/([^/]+)/\]'
    fixed = re.sub(pattern, replacer, mermaid_text)
    return fixed

def main():
    if len(sys.argv) < 2:
        print("Usage: fix_trapezoid_parentheses.py <json_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    print(f"📝 Reading {file_path}...")
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    original = data['mermaid']
    fixed = fix_trapezoid_parentheses(original)
    
    # Count changes
    original_traps = re.findall(r'\[/[^/]+/\]', original)
    fixed_traps = re.findall(r'\[/[^/]+/\]', fixed)
    
    changes = 0
    for orig, fix in zip(original_traps, fixed_traps):
        if orig != fix:
            changes += 1
    
    if changes == 0:
        print("✅ No parentheses found in trapezoid labels - no changes needed")
        return
    
    print(f"🔧 Found {changes} trapezoid labels with parentheses")
    print(f"   Will replace ( ) with [ ] inside trapezoid labels")
    
    # Show examples
    print("\n📋 Examples of changes:")
    for match in re.finditer(r'\[/.*[()].*/\]', original):
        original_line = match.group(0)
        fixed_line = fix_trapezoid_parentheses(original_line)
        if original_line != fixed_line:
            print(f"  {original_line[:80]}")
            print(f"  → {fixed_line[:80]}")
            print()
    
    # Apply fix
    data['mermaid'] = fixed
    
    # Backup original
    backup_path = file_path + '.backup2'
    print(f"💾 Creating backup: {backup_path}")
    with open(backup_path, 'w') as f:
        json.dump(json.load(open(file_path)), f, indent=2)
    
    # Write fixed version
    print(f"✏️  Writing fixed version to {file_path}...")
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Fixed {changes} trapezoid labels")
    print(f"✅ File updated: {file_path}")

if __name__ == '__main__':
    main()

