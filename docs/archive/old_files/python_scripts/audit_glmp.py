#!/usr/bin/env python3
"""Quick GLMP Audit - Count visual gates vs metadata"""

import json
import re
import sys

def audit_process(process):
    """Audit single process for gate count accuracy."""
    name = process.get('name', 'Unknown')
    process_id = process.get('id', 'unknown')
    mermaid = process.get('mermaid', '')
    
    # Count visual gates
    or_count = len(re.findall(r'\w+\{\{', mermaid))
    and_count = len(re.findall(r'\w+\[\[\[', mermaid))
    not_count = len(re.findall(r'\w+\[/', mermaid))
    
    # Get metadata claims
    gates = process.get('logicGates', {})
    claimed_or = gates.get('or', 0)
    claimed_and = gates.get('and', 0)
    claimed_not = gates.get('not', 0)
    
    # Check for mismatches
    issues = []
    if or_count != claimed_or:
        issues.append(f"OR: claimed {claimed_or}, visual {or_count}")
    if and_count != claimed_and:
        issues.append(f"AND: claimed {claimed_and}, visual {and_count}")
    if not_count != claimed_not:
        issues.append(f"NOT: claimed {claimed_not}, visual {not_count}")
    
    return {
        'id': process_id,
        'name': name,
        'valid': len(issues) == 0,
        'issues': issues,
        'visual': {'or': or_count, 'and': and_count, 'not': not_count},
        'claimed': {'or': claimed_or, 'and': claimed_and, 'not': claimed_not}
    }

# Fetch metadata
import urllib.request
url = 'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/metadata.json'
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())

processes = data.get('processes', [])
print(f"🔍 Auditing {len(processes)} processes...")
print()

results = [audit_process(p) for p in processes]

# Count issues
invalid = [r for r in results if not r['valid']]
print(f"✅ Valid: {len(results) - len(invalid)}")
print(f"❌ Invalid: {len(invalid)}")
print()

if invalid:
    print("=" * 80)
    print("PROCESSES WITH GATE COUNT DISCREPANCIES:")
    print("=" * 80)
    print()
    for r in invalid[:10]:  # Show first 10
        print(f"{r['name']} ({r['id']})")
        for issue in r['issues']:
            print(f"  • {issue}")
        print()

