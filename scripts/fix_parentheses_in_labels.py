#!/usr/bin/env python3
"""
Fix parentheses with commas in node labels by quote-wrapping them.
Mermaid parser has issues with (e.g., ...) patterns in unquoted labels.
"""

import json
import re
import sys

def fix_parentheses_in_labels(mermaid_text):
    """Quote-wrap node labels containing parentheses with commas"""
    def quote_wrapper(match):
        node_id = match.group(1)
        label = match.group(2)
        
        # Skip if already quoted or is an edge label
        if label.startswith('"') or label.startswith('|'):
            return match.group(0)
        
        # Check if label has parentheses with commas (e.g., pattern)
        if re.search(r'\([^)]*,[^)]*\)', label):
            label_escaped = label.replace('"', '\\"')
            return f'{node_id}["{label_escaped}"]'
        
        return match.group(0)
    
    # Match node definitions with parentheses containing commas
    # Pattern: nodeId[label with (e.g., something) inside]
    pattern = r'(\w+)\[([^\]]*\([^)]*,[^)]*\)[^\]]*)\]'
    return re.sub(pattern, quote_wrapper, mermaid_text)

def main():
    if len(sys.argv) < 2:
        print("Usage: fix_parentheses_in_labels.py <json_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    original = data['mermaid']
    fixed = fix_parentheses_in_labels(original)
    
    if original == fixed:
        print(f"✓ No changes needed: {file_path}")
        return
    
    # Count changes
    original_count = len(re.findall(r'\[[^"]*\([^)]*,[^)]*\)[^"]*\]', original))
    fixed_count = len(re.findall(r'\["[^"]*\([^)]*,[^)]*\)[^"]*"\]', fixed))
    
    print(f"🔧 Fixing {file_path}")
    print(f"   Found {original_count} labels with parentheses+commas")
    
    # Backup
    backup_path = file_path + '.backup'
    with open(backup_path, 'w') as f:
        json.dump(json.load(open(file_path)), f, indent=2)
    
    # Apply fix
    data['mermaid'] = fixed
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Fixed and saved")

if __name__ == '__main__':
    main()

