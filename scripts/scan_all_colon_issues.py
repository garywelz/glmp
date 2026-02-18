#!/usr/bin/env python3
"""
Scan all process JSON files for node labels containing colons or (...)+ patterns
that need to be quote-wrapped.
"""

import json
import re
import os
import sys
from pathlib import Path

def find_problematic_labels(mermaid_text):
    """Find all node labels that contain colons or (...)+ patterns."""
    problematic = []
    
    # Pattern matches: node_id[label with colon OR (stuff)+ pattern]
    pattern = r'(\w+)\[([^\]]*(?::|\([^)]+\)\d+\+)[^\]]*)\]'
    
    for line_num, line in enumerate(mermaid_text.split('\n'), 1):
        matches = re.finditer(pattern, line)
        for match in matches:
            node_id = match.group(1)
            label = match.group(2)
            problematic.append({
                'line': line_num,
                'node_id': node_id,
                'label': label,
                'full_line': line.strip()
            })
    
    return problematic

def scan_file(file_path):
    """Scan a single JSON file for problematic labels."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        mermaid = data.get('mermaid', '')
        if not mermaid:
            return None
        
        problematic = find_problematic_labels(mermaid)
        
        return {
            'file': file_path,
            'name': data.get('name', 'Unknown'),
            'problematic': problematic,
            'count': len(problematic)
        }
    except Exception as e:
        return {
            'file': file_path,
            'error': str(e)
        }

def main():
    processes_dir = Path("processes_with_not_gates")
    
    if not processes_dir.exists():
        print(f"❌ Error: Directory not found: {processes_dir}")
        sys.exit(1)
    
    print("🔍 Scanning all process files for colon and (...)+ patterns...\n")
    
    all_issues = []
    
    # Find all JSON files
    for json_file in processes_dir.rglob("*.json"):
        result = scan_file(json_file)
        if result and 'error' in result:
            print(f"⚠️  Error reading {json_file}: {result['error']}")
        elif result and result['count'] > 0:
            all_issues.append(result)
    
    # Report findings
    if not all_issues:
        print("✅ No problematic labels found in any process files!")
        print("   All node labels are clean (no colons or (...)+ patterns).")
        return
    
    print(f"📊 Found {len(all_issues)} file(s) with problematic labels:\n")
    
    total_issues = 0
    for result in sorted(all_issues, key=lambda x: x['count'], reverse=True):
        print(f"📁 {result['name']}")
        print(f"   File: {result['file']}")
        print(f"   Issues: {result['count']} problematic label(s)")
        print(f"   Details:")
        for issue in result['problematic']:
            print(f"      Line {issue['line']}: {issue['node_id']}[{issue['label'][:60]}...]")
        print()
        total_issues += result['count']
    
    print(f"📈 Summary:")
    print(f"   • Total files with issues: {len(all_issues)}")
    print(f"   • Total problematic labels: {total_issues}")
    print()
    print("💡 Next steps:")
    print("   1. Review the issues above")
    print("   2. Run fix script: python3 scripts/fix_all_colon_issues.py")
    print("   3. Or fix individually: python3 scripts/fix_anaerobic_colons.py <file>")

if __name__ == "__main__":
    main()

