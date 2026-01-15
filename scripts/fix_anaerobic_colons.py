#!/usr/bin/env python3
"""
Fix colons and (4Fe-4S)2+ patterns in Mermaid node labels by wrapping in quotes.

Based on Cursor.com agent findings:
- Colons in node labels break Mermaid 10.6.1 parsing
- Patterns like (4Fe-4S)2+ also need quoting
- Fix: Wrap labels in quotes: A8["label content"]
"""

import json
import re
import sys

def quote_problematic_labels(text):
    """
    Find node labels containing colons or (...)+ patterns and wrap them in quotes.
    
    Pattern: node_id[label with colon or (stuff)+ pattern]
    Replace: node_id["label with colon or (stuff)+ pattern"]
    """
    # Match: node_id[label with colon OR (stuff)+ pattern]
    # Handles: A8[label: text], A10[label with (stuff)2+], etc.
    pattern = r'(\w+)\[([^\]]*(?::|\([^)]+\)\d+\+)[^\]]*)\]'
    
    def replacer(match):
        node_id = match.group(1)
        label = match.group(2)
        # Escape any quotes already in the label
        label_escaped = label.replace('"', '\\"')
        return f'{node_id}["{label_escaped}"]'
    
    return re.sub(pattern, replacer, text)

def main():
    file_path = "processes_with_not_gates/ecoli/ecoli_anaerobic_respiration.json"
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {file_path}: {e}")
        sys.exit(1)
    
    mermaid = data.get('mermaid', '')
    if not mermaid:
        print(f"❌ Error: No 'mermaid' field found in {file_path}")
        sys.exit(1)
    
    print("🔍 Searching for problematic labels...")
    
    # Find all problematic labels BEFORE fix
    problematic_before = []
    for line_num, line in enumerate(mermaid.split('\n'), 1):
        if re.search(r'\[[^\]]*(?::|\([^)]+\)\d+\+)[^\]]*\]', line):
            problematic_before.append((line_num, line.strip()))
    
    if not problematic_before:
        print("✅ No problematic labels found. File may already be fixed.")
        return
    
    print(f"\n📋 Found {len(problematic_before)} problematic label(s):\n")
    print("=== BEFORE ===")
    for line_num, line in problematic_before:
        print(f"Line {line_num}: {line}")
    
    # Apply fix
    fixed_mermaid = quote_problematic_labels(mermaid)
    
    # Verify fixes were applied
    problematic_after = []
    for line_num, line in enumerate(fixed_mermaid.split('\n'), 1):
        # Check for quoted versions of the patterns
        if re.search(r'\["[^"]*(?::|\([^)]+\)\d+\+)[^"]*"\]', line):
            problematic_after.append((line_num, line.strip()))
    
    print("\n=== AFTER ===")
    for line_num, line in problematic_after:
        print(f"Line {line_num}: {line}")
    
    # Save fixed file
    data['mermaid'] = fixed_mermaid
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ Fixed {len(problematic_before)} label(s) and saved to: {file_path}")
    print("\n⚠️  Next steps:")
    print("   1. Test the diagram: Check viewer or run through Mermaid parser")
    print("   2. Deploy: Use gsutil to upload to GCS with no-cache headers")
    print("   3. Verify: Check viewer URL in incognito mode")

if __name__ == "__main__":
    main()

