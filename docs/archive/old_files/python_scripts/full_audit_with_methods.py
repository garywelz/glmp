#!/usr/bin/env python3
"""
Full GLMP Audit - All 108 Processes
Identifies method used for each process and validates accordingly
"""

import json
import re
import urllib.request
import time
from collections import defaultdict

class MethodIdentifier:
    """Identifies which method was used to create a process."""
    
    @staticmethod
    def identify_method(mermaid):
        """Determine creation method for this process."""
        methods = []
        
        # Check for shape-based (Mermaid shapes)
        has_diamonds = bool(re.search(r'\w+\{[^{]', mermaid))  # {...}
        has_hexagons = bool(re.search(r'\w+\{\{', mermaid))    # {{...}}
        has_trapezoids = bool(re.search(r'\w+\[/', mermaid))   # [/.../]
        
        if has_diamonds or has_hexagons or has_trapezoids:
            methods.append('shape-based')
        
        # Check for color-based (style statements)
        has_yellow_styles = '#ffd600' in mermaid or 'yellow' in mermaid
        has_purple_styles = '#7950f2' in mermaid or 'purple' in mermaid
        has_red_styles = '#e74c3c' in mermaid or 'red' in mermaid
        
        if has_yellow_styles or has_purple_styles or has_red_styles:
            methods.append('color-based')
        
        # Check for label-based (text in nodes)
        has_or_labels = bool(re.search(r'OR:', mermaid, re.IGNORECASE))
        has_and_labels = bool(re.search(r'AND:', mermaid, re.IGNORECASE))
        has_not_labels = bool(re.search(r'NOT:', mermaid, re.IGNORECASE))
        
        if has_or_labels or has_and_labels or has_not_labels:
            methods.append('label-based')
        
        if not methods:
            return 'unknown'
        elif len(methods) == 1:
            return methods[0]
        else:
            return 'hybrid-' + '+'.join(methods)
    
    @staticmethod
    def count_by_shapes(mermaid):
        """Count gates using Mermaid shape syntax."""
        # OR: {...} (single curly, diamond)
        or_gates = re.findall(r'(\w+)\{[^{]', mermaid)
        # AND: {{...}} (double curly, hexagon)
        and_gates = re.findall(r'(\w+)\{\{', mermaid)
        # NOT: [/.../] (trapezoid)
        not_gates = re.findall(r'(\w+)\[/', mermaid)
        
        return {
            'or': len(or_gates),
            'and': len(and_gates),
            'not': len(not_gates),
            'or_nodes': or_gates,
            'and_nodes': and_gates,
            'not_nodes': not_gates
        }
    
    @staticmethod
    def count_by_colors(mermaid):
        """Count gates using color styling."""
        gates = {'or': [], 'and': [], 'not': []}
        
        # Extract style statements
        style_pattern = r'style\s+(\w+)\s+fill:(#[0-9a-fA-F]{6}|[a-z]+)'
        styles = re.findall(style_pattern, mermaid)
        
        for node_id, color in styles:
            color_lower = color.lower()
            if color == '#ffd600' or 'yellow' in color_lower:
                gates['or'].append(node_id)
            elif color == '#7950f2' or 'purple' in color_lower:
                gates['and'].append(node_id)
            elif color == '#e74c3c' or 'red' in color_lower:
                gates['not'].append(node_id)
        
        return {
            'or': len(gates['or']),
            'and': len(gates['and']),
            'not': len(gates['not']),
            'or_nodes': gates['or'],
            'and_nodes': gates['and'],
            'not_nodes': gates['not']
        }
    
    @staticmethod
    def count_by_labels(mermaid):
        """Count gates using text labels."""
        gates = {'or': [], 'and': [], 'not': []}
        
        # Find nodes with OR: in label
        or_matches = re.findall(r'(\w+)[\[{]+[^}\]]*OR:', mermaid, re.IGNORECASE)
        gates['or'] = or_matches
        
        # Find nodes with AND: in label
        and_matches = re.findall(r'(\w+)[\[{]+[^}\]]*AND:', mermaid, re.IGNORECASE)
        gates['and'] = and_matches
        
        # Find nodes with NOT: in label
        not_matches = re.findall(r'(\w+)[\[{]+[^}\]]*NOT:', mermaid, re.IGNORECASE)
        gates['not'] = not_matches
        
        return {
            'or': len(gates['or']),
            'and': len(gates['and']),
            'not': len(gates['not']),
            'or_nodes': gates['or'],
            'and_nodes': gates['and'],
            'not_nodes': gates['not']
        }

def audit_process(process, process_data):
    """Full audit of single process."""
    process_id = process.get('id', 'unknown')
    name = process.get('name', 'Unknown')
    
    mermaid = process_data.get('mermaid', '')
    
    # Identify method
    method = MethodIdentifier.identify_method(mermaid)
    
    # Count using all methods
    shape_count = MethodIdentifier.count_by_shapes(mermaid)
    color_count = MethodIdentifier.count_by_colors(mermaid)
    label_count = MethodIdentifier.count_by_labels(mermaid)
    
    # Get metadata claims
    gates = process.get('logicGates', {})
    claimed = {
        'or': gates.get('or', 0),
        'and': gates.get('and', 0),
        'not': gates.get('not', 0) or 0
    }
    
    # Determine which count method matches best
    shape_match = (shape_count['or'] == claimed['or'] and 
                   shape_count['and'] == claimed['and'] and
                   shape_count['not'] == claimed['not'])
    color_match = (color_count['or'] == claimed['or'] and
                   color_count['and'] == claimed['and'] and
                   color_count['not'] == claimed['not'])
    label_match = (label_count['or'] == claimed['or'] and
                   label_count['and'] == claimed['and'] and
                   label_count['not'] == claimed['not'])
    
    # Determine actual method used
    if shape_match:
        actual_method = 'shape-based'
        visual_count = shape_count
    elif color_match:
        actual_method = 'color-based'
        visual_count = color_count
    elif label_match:
        actual_method = 'label-based'
        visual_count = label_count
    else:
        # Use color as default (Phase 2 standard)
        actual_method = 'unknown-using-color'
        visual_count = color_count
    
    # Check for issues
    issues = []
    if visual_count['or'] != claimed['or']:
        issues.append(f"OR: claimed {claimed['or']}, visual {visual_count['or']}")
    if visual_count['and'] != claimed['and']:
        issues.append(f"AND: claimed {claimed['and']}, visual {visual_count['and']}")
    if visual_count['not'] != claimed['not']:
        issues.append(f"NOT: claimed {claimed['not']}, visual {visual_count['not']}")
    
    return {
        'id': process_id,
        'name': name,
        'organism': process.get('organism', 'Unknown'),
        'method_identified': method,
        'method_used': actual_method,
        'valid': len(issues) == 0,
        'issues': issues,
        'claimed': claimed,
        'visual': {
            'or': visual_count['or'],
            'and': visual_count['and'],
            'not': visual_count['not']
        },
        'all_counts': {
            'shape': shape_count,
            'color': color_count,
            'label': label_count
        }
    }

# Main execution
print("🔍 FULL AUDIT: All 108 GLMP Processes")
print("=" * 80)
print()
print("Fetching metadata...")

url = 'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/metadata.json'
with urllib.request.urlopen(url) as response:
    metadata = json.loads(response.read())

processes = metadata.get('processes', [])
print(f"Found {len(processes)} processes")
print()
print("Starting audit (this will take a few minutes)...")
print()

results = []
for i, proc in enumerate(processes, 1):
    # Fetch individual process file
    organism = proc['id'].split('_')[0]
    proc_url = f'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/{organism}/{proc["id"]}.json'
    
    try:
        with urllib.request.urlopen(proc_url) as response:
            proc_data = json.loads(response.read())
        
        result = audit_process(proc, proc_data)
        results.append(result)
        
        # Progress
        if i % 10 == 0:
            print(f"  Processed {i}/{len(processes)}...")
            time.sleep(0.5)  # Be nice to server
    
    except Exception as e:
        print(f"  ❌ Error with {proc['id']}: {e}")
        results.append({
            'id': proc['id'],
            'name': proc.get('name', 'Unknown'),
            'valid': False,
            'issues': [f'Failed to fetch: {e}'],
            'method_used': 'error'
        })

print()
print("✅ Audit complete!")
print()

# Generate summary
print("=" * 80)
print("📊 AUDIT SUMMARY")
print("=" * 80)
print()

valid_count = sum(1 for r in results if r.get('valid', False))
invalid_count = len(results) - valid_count

print(f"Total Processes: {len(results)}")
print(f"✅ Valid (counts match): {valid_count} ({valid_count/len(results)*100:.1f}%)")
print(f"❌ Invalid (discrepancies): {invalid_count} ({invalid_count/len(results)*100:.1f}%)")
print()

# Method breakdown
method_counts = defaultdict(int)
for r in results:
    method = r.get('method_used', 'unknown')
    method_counts[method] += 1

print("Methods Identified:")
for method, count in sorted(method_counts.items(), key=lambda x: -x[1]):
    print(f"  {method}: {count}")
print()

# Save detailed report
with open('/workspace/FULL_AUDIT_REPORT.json', 'w') as f:
    json.dump(results, f, indent=2)

print("📄 Detailed report saved to: FULL_AUDIT_REPORT.json")
print()

# Show sample issues
print("=" * 80)
print("SAMPLE DISCREPANCIES (First 20):")
print("=" * 80)
print()

invalid_results = [r for r in results if not r.get('valid', False)]
for r in invalid_results[:20]:
    print(f"{r['name'][:60]}")
    print(f"  ID: {r['id']}")
    print(f"  Method: {r.get('method_used', 'N/A')}")
    for issue in r.get('issues', []):
        print(f"  • {issue}")
    print()

print(f"... and {len(invalid_results) - 20} more with issues")
