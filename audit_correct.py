#!/usr/bin/env python3
"""Correct GLMP Audit - Proper Mermaid Syntax"""

import json
import re
import urllib.request

def audit_process(process):
    """Audit with CORRECT Mermaid syntax."""
    name = process.get('name', 'Unknown')
    process_id = process.get('id', 'unknown')
    
    # Get Mermaid from individual process file
    organism = process_id.split('_')[0]
    url = f'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/{organism}/{process_id}.json'
    
    try:
        with urllib.request.urlopen(url) as response:
            process_data = json.loads(response.read())
        mermaid = process_data.get('mermaid', '')
    except:
        return None
    
    # Count visual gates with CORRECT syntax
    # OR gates: Single curly {...} (diamond)
    or_count = len(re.findall(r'\w+\{[^{]', mermaid))
    # AND gates: Double curly {{...}} (hexagon)
    and_count = len(re.findall(r'\w+\{\{', mermaid))
    # NOT gates: [/.../] (trapezoid)  
    not_count = len(re.findall(r'\w+\[/', mermaid))
    
    # Get metadata claims
    gates = process.get('logicGates', {})
    claimed_or = gates.get('or', 0)
    claimed_and = gates.get('and', 0)
    claimed_not = gates.get('not', 0) or 0
    
    # Check mismatches
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

print("🔍 Auditing first 10 processes with CORRECT Mermaid syntax...")
print()

url = 'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/metadata.json'
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())

processes = data.get('processes', [])[:10]  # First 10 for testing

for p in processes:
    result = audit_process(p)
    if result:
        status = "✅" if result['valid'] else "❌"
        print(f"{status} {result['name'][:50]}")
        if result['issues']:
            for issue in result['issues']:
                print(f"     {issue}")
