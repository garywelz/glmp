#!/usr/bin/env python3
"""
Fix gate shapes to match gate colors - CORRECT VERSION

Only fixes nodes that have gate COLORS (yellow/purple/red) to have correct SHAPES.
Does NOT touch nodes that have gate shapes but non-gate colors.
"""
import json
import re
import urllib.request
import time
import os

def fix_gate_shapes_in_process(mermaid):
    """Fix shapes for nodes that have gate colors."""
    
    # Step 1: Find all nodes with gate colors
    gate_nodes = {}
    for match in re.finditer(r'style\s+(\w+)\s+fill:(#[0-9a-fA-F]{6})', mermaid):
        node_id = match.group(1)
        color = match.group(2)
        if color in ['#ffd600', '#7950f2', '#e74c3c']:
            gate_nodes[node_id] = color
    
    if not gate_nodes:
        return mermaid, []
    
    # Step 2: For each gate node, ensure correct shape
    fixes = []
    for node_id, color in gate_nodes.items():
        # Find current node definition (any shape)
        current_def = None
        label = None
        
        # Try all possible Mermaid shape syntaxes
        patterns = [
            (rf'{node_id}\[/([^/]+)/\]', 'trapezoid'),      # [/label/]
            (rf'{node_id}\{{{{([^}}]+)\}}}}', 'hexagon'),   # {{label}}
            (rf'{node_id}\{{([^{{}}]+)\}}', 'diamond'),     # {label}
            (rf'{node_id}\[([^\[/\\][^\]]*)\]', 'rectangle'), # [label]
            (rf'{node_id}\\?\[([^/\]]+)/?\]', 'slanted'),   # [\label/] or [label/]
            (rf'{node_id}\(([^)]+)\)', 'rounded'),          # (label)
        ]
        
        for pattern, shape in patterns:
            match = re.search(pattern, mermaid)
            if match:
                current_def = match.group(0)
                label = match.group(1).strip('\\/')
                break
        
        if not current_def or not label:
            continue
        
        # Determine correct shape based on color
        if color == '#ffd600':  # Yellow = OR = Diamond
            correct_def = f'{node_id}{{{label}}}'
        elif color == '#7950f2':  # Purple = AND = Hexagon
            correct_def = f'{node_id}{{{{{label}}}}}'
        elif color == '#e74c3c':  # Red = NOT = Trapezoid
            correct_def = f'{node_id}[/{label}/]'
        
        # Replace if different
        if current_def != correct_def:
            mermaid = mermaid.replace(current_def, correct_def, 1)
            fixes.append(node_id)
    
    return mermaid, fixes

# Main execution
print("🔧 FIXING GATE SHAPES TO MATCH GATE COLORS")
print("=" * 80)
print("Only modifying nodes with gate colors (#ffd600, #7950f2, #e74c3c)")
print("=" * 80)
print()

# Fetch metadata
url = 'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/metadata.json'
with urllib.request.urlopen(url) as r:
    metadata = json.loads(r.read())

processes = metadata['processes']
print(f"Processing {len(processes)} processes...\n")

os.makedirs('/workspace/fixed_processes_final/ecoli', exist_ok=True)
os.makedirs('/workspace/fixed_processes_final/yeast', exist_ok=True)
os.makedirs('/workspace/fixed_processes_final/bacillus', exist_ok=True)

fixed_count = 0
total_fixes = 0
fix_report = []

for i, proc in enumerate(processes, 1):
    pid = proc['id']
    org = pid.split('_')[0]
    purl = f'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/{org}/{pid}.json'
    
    try:
        # Fetch original
        with urllib.request.urlopen(purl) as r:
            pdata = json.loads(r.read())
        
        # Fix gate shapes
        mermaid_fixed, fixes = fix_gate_shapes_in_process(pdata['mermaid'])
        
        if fixes:
            pdata['mermaid'] = mermaid_fixed
            fixed_count += 1
            total_fixes += len(fixes)
            fix_report.append({
                'id': pid,
                'name': proc['name'],
                'nodes_fixed': fixes
            })
            if fixed_count <= 10:
                print(f"✅ {pid}: {len(fixes)} gate nodes fixed")
        
        # Save
        output_path = f'/workspace/fixed_processes_final/{org}/{pid}.json'
        with open(output_path, 'w') as f:
            json.dump(pdata, f, indent=2)
        
        if i % 20 == 0:
            print(f"   Progress: {i}/{len(processes)}...")
            time.sleep(0.2)
    
    except Exception as e:
        print(f"❌ Error with {pid}: {e}")

print()
print("=" * 80)
print(f"✅ COMPLETE: Fixed {fixed_count} processes ({total_fixes} gate nodes)")
print("=" * 80)

# Save report
with open('/workspace/GATE_SHAPE_FIX_REPORT.json', 'w') as f:
    json.dump(fix_report, f, indent=2)

print(f"\n📄 Report saved to: GATE_SHAPE_FIX_REPORT.json")
