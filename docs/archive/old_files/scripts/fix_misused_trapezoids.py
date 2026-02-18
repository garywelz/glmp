#!/usr/bin/env python3
"""
Fix Misused Trapezoids
Convert trapezoids that aren't true NOT gates into rectangles (intermediates)
"""

import json
import re
from glob import glob

# Load the audit report
with open('NOT_GATE_AUDIT_REPORT.json', 'r') as f:
    audit = json.load(f)

print("🔧 FIXING MISUSED TRAPEZOIDS")
print("=" * 80)
print()

# Focus on suspicious ones with specific patterns
CLEAR_MISUSE_PATTERNS = [
    'inactive state',
    'apo-form',
    'reversible state',
    'free form',
    'unbound form',
    'dormant',
    'resting state',
    'inactive form',
    'wait for'
]

fixes_to_apply = []
for trap in audit['suspicious_trapezoids']:
    text_lower = trap['text'].lower()
    if any(pattern in text_lower for pattern in CLEAR_MISUSE_PATTERNS):
        # Also check if it has outgoing edges (flow continues)
        if trap['outgoing']:
            fixes_to_apply.append(trap)

print(f"Found {len(fixes_to_apply)} clear misuses to fix")
print()

total_fixes = 0
processes_fixed = []

for fix in fixes_to_apply:
    process_id = fix['process']
    node_id = fix['node']
    text = fix['text']
    
    # Find the file
    filepath = None
    for f in glob('gcs-processes/*/*.json'):
        with open(f, 'r') as fh:
            data = json.load(fh)
            if data['id'] == process_id:
                filepath = f
                break
    
    if not filepath:
        print(f"✗ Could not find file for {process_id}")
        continue
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        mermaid = data['mermaid']
        lines = mermaid.split('\n')
        new_lines = []
        fixed = False
        
        for line in lines:
            # Look for the trapezoid definition: NODEID[\Text/]
            if f'{node_id}[\\' in line and '/]' in line:
                # Convert to rectangle: NODEID[Text]
                # Extract the text content
                match = re.search(rf'{node_id}\s*\[\\([^\]]+)/\]', line)
                if match:
                    content = match.group(1)
                    # Replace with rectangle
                    new_line = line.replace(f'{node_id}[\\{content}/]', f'{node_id}[{content}]')
                    new_lines.append(new_line)
                    fixed = True
                    print(f"  {process_id}: {node_id} trapezoid→rectangle [{text[:40]}...]")
                else:
                    new_lines.append(line)
            
            # Update style from red to salmon (intermediate state)
            elif line.strip().startswith(f'style {node_id} ') and 'fill:#e74c3c' in line:
                new_lines.append(f'    style {node_id} fill:#b3e5fc,color:#000')
                print(f"    └─ Style: red→light cyan")
            else:
                new_lines.append(line)
        
        if fixed:
            data['mermaid'] = '\n'.join(new_lines)
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            total_fixes += 1
            if process_id not in processes_fixed:
                processes_fixed.append(process_id)
    
    except Exception as e:
        print(f"✗ Error fixing {process_id} node {node_id}: {e}")

print()
print("=" * 80)
print(f"✅ TRAPEZOID FIXES COMPLETE")
print("=" * 80)
print(f"Total nodes fixed: {total_fixes}")
print(f"Processes updated: {len(processes_fixed)}")
if processes_fixed:
    print(f"\nProcesses fixed:")
    for proc in sorted(processes_fixed):
        print(f"  - {proc}")
print("=" * 80)

