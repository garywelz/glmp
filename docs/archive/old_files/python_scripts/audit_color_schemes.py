#!/usr/bin/env python3
"""
Audit Color Schemes and Legends
Check for missing colors in legends and color assignment errors
"""

import json
import re
from glob import glob
from collections import defaultdict

print("🎨 AUDITING COLOR SCHEMES AND LEGENDS")
print("=" * 80)
print()

# Expected colors from final scheme
EXPECTED_COLORS = {
    'green': {'hex': '#51cf66', 'category': 'Environmental Triggers'},
    'amber': {'hex': '#ffa726', 'category': 'Enzymes & Proteins'},
    'skyBlue': {'hex': '#42a5f5', 'category': 'Processing & Operations'},
    'salmon': {'hex': '#b3e5fc', 'category': 'Intermediates & States'},
    'orange': {'hex': '#ffd600', 'category': 'OR Logic Gates'},
    'purple': {'hex': '#7950f2', 'category': 'AND Logic Gates'},
    'red': {'hex': '#e74c3c', 'category': 'NOT Logic Gates'},
    'black': {'hex': '#000000', 'category': 'Final Products'}
}

issues = []
processes_checked = 0

files = sorted(glob('gcs-processes/*/*.json'))

for filepath in files:
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        process_id = data['id']
        processes_checked += 1
        
        # Check 1: Does colorScheme exist?
        if 'colorScheme' not in data:
            issues.append({
                'process': process_id,
                'type': 'MISSING_COLOR_SCHEME',
                'severity': 'HIGH',
                'message': 'No colorScheme field in JSON'
            })
            continue
        
        color_scheme = data['colorScheme']
        
        # Check 2: Are all 8 expected colors present?
        missing_colors = []
        for color_key in EXPECTED_COLORS.keys():
            if color_key not in color_scheme:
                missing_colors.append(color_key)
        
        if missing_colors:
            issues.append({
                'process': process_id,
                'type': 'INCOMPLETE_LEGEND',
                'severity': 'MEDIUM',
                'message': f'Missing colors in legend: {", ".join(missing_colors)}'
            })
        
        # Check 3: Do legend colors match expected hex values?
        wrong_hex = []
        for color_key, expected in EXPECTED_COLORS.items():
            if color_key in color_scheme:
                actual_hex = color_scheme[color_key].get('hex', '')
                if actual_hex.lower() != expected['hex'].lower():
                    wrong_hex.append(f"{color_key}: {actual_hex} (expected {expected['hex']})")
        
        if wrong_hex:
            issues.append({
                'process': process_id,
                'type': 'WRONG_HEX_VALUES',
                'severity': 'MEDIUM',
                'message': f'Incorrect hex values: {"; ".join(wrong_hex)}'
            })
        
        # Check 4: Extract all style directives from Mermaid code
        mermaid = data.get('mermaid', '')
        style_colors = defaultdict(int)
        
        # Find all style directives
        style_pattern = r'style\s+([A-Z][A-Z0-9]*)\s+fill:(#[0-9a-fA-F]{6})'
        for match in re.finditer(style_pattern, mermaid):
            node_id, color = match.groups()
            style_colors[color.lower()] += 1
        
        # Check 5: Are there any unexpected colors in the Mermaid code?
        expected_hex_values = set(c['hex'].lower() for c in EXPECTED_COLORS.values())
        unexpected_colors = []
        
        for color, count in style_colors.items():
            if color not in expected_hex_values:
                unexpected_colors.append(f"{color} (used {count}x)")
        
        if unexpected_colors:
            issues.append({
                'process': process_id,
                'type': 'UNEXPECTED_COLORS',
                'severity': 'HIGH',
                'message': f'Unexpected colors in Mermaid: {"; ".join(unexpected_colors)}'
            })
        
        # Check 6: Are there unstyled nodes?
        # Extract all node IDs
        all_nodes = set()
        node_patterns = [
            r'([A-Z][A-Z0-9]*)\s*\[',  # rectangles
            r'([A-Z][A-Z0-9]*)\s*\{',  # diamonds
            r'([A-Z][A-Z0-9]*)\s*\(',  # rounded/stadium
        ]
        
        for pattern in node_patterns:
            for match in re.finditer(pattern, mermaid):
                all_nodes.add(match.group(1))
        
        # Extract styled nodes
        styled_nodes = set()
        for match in re.finditer(r'style\s+([A-Z][A-Z0-9]*)', mermaid):
            styled_nodes.add(match.group(1))
        
        unstyled = all_nodes - styled_nodes
        if unstyled:
            issues.append({
                'process': process_id,
                'type': 'UNSTYLED_NODES',
                'severity': 'HIGH',
                'message': f'{len(unstyled)} unstyled nodes: {", ".join(sorted(list(unstyled))[:5])}{"..." if len(unstyled) > 5 else ""}'
            })
    
    except Exception as e:
        issues.append({
            'process': filepath,
            'type': 'ERROR',
            'severity': 'CRITICAL',
            'message': f'Error reading file: {str(e)}'
        })

print(f"Checked {processes_checked} processes")
print()
print("=" * 80)
print(f"📊 AUDIT RESULTS")
print("=" * 80)
print()

# Group by severity
critical = [i for i in issues if i['severity'] == 'CRITICAL']
high = [i for i in issues if i['severity'] == 'HIGH']
medium = [i for i in issues if i['severity'] == 'MEDIUM']

print(f"🔴 CRITICAL: {len(critical)} issues")
print(f"🟠 HIGH: {len(high)} issues")
print(f"🟡 MEDIUM: {len(medium)} issues")
print(f"✅ TOTAL CLEAN: {processes_checked - len(set(i['process'] for i in issues))} processes")
print()

if critical:
    print("=" * 80)
    print("🔴 CRITICAL ISSUES")
    print("=" * 80)
    for issue in critical:
        print(f"\n{issue['process']}")
        print(f"  Type: {issue['type']}")
        print(f"  {issue['message']}")

if high:
    print()
    print("=" * 80)
    print("🟠 HIGH PRIORITY ISSUES")
    print("=" * 80)
    for issue in high[:20]:  # Show first 20
        print(f"\n{issue['process']}")
        print(f"  Type: {issue['type']}")
        print(f"  {issue['message']}")
    
    if len(high) > 20:
        print(f"\n... and {len(high) - 20} more HIGH priority issues")

if medium:
    print()
    print("=" * 80)
    print("🟡 MEDIUM PRIORITY ISSUES")
    print("=" * 80)
    print(f"\nTotal: {len(medium)} processes with legend/hex issues")
    print("(These are mostly cosmetic - legends incomplete but colors correct)")

# Save detailed report
with open('COLOR_AUDIT_REPORT.json', 'w') as f:
    json.dump({
        'summary': {
            'total_processes': processes_checked,
            'critical': len(critical),
            'high': len(high),
            'medium': len(medium),
            'clean': processes_checked - len(set(i['process'] for i in issues))
        },
        'issues': issues
    }, f, indent=2)

print()
print("=" * 80)
print(f"✅ Detailed report saved to COLOR_AUDIT_REPORT.json")
print("=" * 80)

