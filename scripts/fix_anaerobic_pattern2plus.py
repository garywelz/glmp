#!/usr/bin/env python3
"""
Fix (4Fe-4S)2+ pattern by adding space: (4Fe-4S) 2+
This pattern might confuse Mermaid parser even inside quotes.
"""

import json
import re
import sys

def fix_pattern2plus(mermaid_text):
    """Replace (4Fe-4S)2+ with (4Fe-4S) 2+ (add space before 2+)"""
    # Pattern matches (4Fe-4S)2+ or similar patterns
    fixed = re.sub(r'\(([^)]+)\)(\d+)\+', r'(\1) \2+', mermaid_text)
    return fixed

def main():
    if len(sys.argv) < 2:
        print("Usage: fix_anaerobic_pattern2plus.py <json_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    print(f"📝 Reading {file_path}...")
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    original = data['mermaid']
    fixed = fix_pattern2plus(original)
    
    # Count changes
    original_count = len(re.findall(r'\([^)]+\)\d+\+', original))
    fixed_count = len(re.findall(r'\([^)]+\) \d+\+', fixed))
    
    if original_count == 0:
        print("✅ No (pattern)2+ patterns found - no changes needed")
        return
    
    print(f"🔧 Found {original_count} (pattern)2+ patterns")
    print(f"   Will replace with (pattern) 2+ (add space)")
    
    # Show examples
    print("\n📋 Examples of changes:")
    for match in re.finditer(r'\["[^"]*\([^)]+\)\d+\+[^"]*"\]', original):
        original_line = match.group(0)
        fixed_line = fix_pattern2plus(original_line)
        if original_line != fixed_line:
            print(f"  {original_line[:75]}")
            print(f"  → {fixed_line[:75]}")
            print()
    
    # Apply fix
    data['mermaid'] = fixed
    
    # Backup original
    backup_path = file_path + '.backup'
    print(f"💾 Creating backup: {backup_path}")
    with open(backup_path, 'w') as f:
        json.dump(json.load(open(file_path)), f, indent=2)
    
    # Write fixed version
    print(f"✏️  Writing fixed version to {file_path}...")
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Fixed {original_count} occurrences")
    print(f"✅ File updated: {file_path}")

if __name__ == '__main__':
    main()


