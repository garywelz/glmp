#!/usr/bin/env python3
"""
Fix Color-Shape Mismatches in All 108 GLMP Processes

Ensures:
- Yellow (#ffd600) nodes → Diamond {...}
- Purple (#7950f2) nodes → Hexagon {{...}}
- Red (#e74c3c) nodes → Trapezoid [/.../]
"""
import json
import re
import urllib.request
import time
import os

def extract_node_colors(mermaid):
    """Extract all node colors from style statements."""
    colors = {}
    for match in re.finditer(r'style\s+(\w+)\s+fill:(#[0-9a-fA-F]{6})', mermaid):
        colors[match.group(1)] = match.group(2)
    return colors

def extract_node_label(mermaid, node_id):
    """Extract the label for a specific node."""
    # Try all shape patterns
    patterns = [
        rf'{node_id}\{{{{([^}}]+)\}}}}',  # Hexagon
        rf'{node_id}\{{([^{{}}]+)\}}',     # Diamond
        rf'{node_id}\[/([^/]+)/\]',        # Trapezoid
        rf'{node_id}\[([^\[/\]]+)\]',      # Rectangle
        rf'{node_id}\(([^)]+)\)',          # Rounded
    ]
    
    for pattern in patterns:
        match = re.search(pattern, mermaid)
        if match:
            return match.group(1)
    
    return None

def get_current_shape_syntax(mermaid, node_id):
    """Get the current shape syntax for a node."""
    patterns = [
        (rf'{node_id}\{{{{[^}}]+\}}}}', 'hexagon'),
        (rf'{node_id}\{{[^{{}}]+\}}', 'diamond'),
        (rf'{node_id}\[/[^/]+/\]', 'trapezoid'),
        (rf'{node_id}\[[^\[/\]]+\]', 'rectangle'),
    ]
    
    for pattern, shape in patterns:
        if re.search(pattern, mermaid):
            return shape
    
    return None

def fix_node_shape(mermaid, node_id, color):
    """Fix a single node's shape to match its color."""
    label = extract_node_label(mermaid, node_id)
    if not label:
        return mermaid, False
    
    current_shape = get_current_shape_syntax(mermaid, node_id)
    if not current_shape:
        return mermaid, False
    
    # Determine correct shape for color
    if color == '#ffd600':  # Yellow = OR = Diamond
        target_shape = 'diamond'
        new_syntax = f'{node_id}{{{label}}}'
    elif color == '#7950f2':  # Purple = AND = Hexagon
        target_shape = 'hexagon'
        new_syntax = f'{node_id}{{{{{label}}}}}'
    elif color == '#e74c3c':  # Red = NOT = Trapezoid
        target_shape = 'trapezoid'
        new_syntax = f'{node_id}[/{label}/]'
    else:
        return mermaid, False
    
    # If already correct, skip
    if current_shape == target_shape:
        return mermaid, False
    
    # Find and replace old syntax
    old_patterns = [
        rf'{node_id}\{{{{[^}}]+\}}}}',  # Hexagon
        rf'{node_id}\{{[^{{}}]+\}}',     # Diamond
        rf'{node_id}\[/[^/]+/\]',        # Trapezoid
        rf'{node_id}\[[^\[/\]]+\]',      # Rectangle
    ]
    
    for pattern in old_patterns:
        match = re.search(pattern, mermaid)
        if match:
            old_syntax = match.group(0)
            mermaid = mermaid.replace(old_syntax, new_syntax, 1)
            return mermaid, True
    
    return mermaid, False

def fix_process(process_data):
    """Fix all mismatches in a single process."""
    mermaid = process_data.get('mermaid', '')
    colors = extract_node_colors(mermaid)
    
    fixes = []
    for node_id, color in colors.items():
        # Only fix gate colors
        if color in ['#ffd600', '#7950f2', '#e74c3c']:
            mermaid_new, fixed = fix_node_shape(mermaid, node_id, color)
            if fixed:
                fixes.append(node_id)
                mermaid = mermaid_new
    
    if fixes:
        process_data['mermaid'] = mermaid
    
    return process_data, fixes

# Main execution
print("🔧 FIXING COLOR-SHAPE MISMATCHES IN ALL 108 PROCESSES")
print("=" * 80)
print()

# Fetch metadata
metadata_url = 'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/metadata.json'
with urllib.request.urlopen(metadata_url) as r:
    metadata = json.loads(r.read())

processes = metadata['processes']
print(f"Processing {len(processes)} processes...\n")

# Create directories
os.makedirs('/workspace/fixed_processes/ecoli', exist_ok=True)
os.makedirs('/workspace/fixed_processes/yeast', exist_ok=True)
os.makedirs('/workspace/fixed_processes/bacillus', exist_ok=True)

fixed_count = 0
fix_report = []

for i, proc in enumerate(processes, 1):
    pid = proc['id']
    org = pid.split('_')[0]
    purl = f'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/{org}/{pid}.json'
    
    try:
        # Fetch process
        with urllib.request.urlopen(purl) as r:
            pdata = json.loads(r.read())
        
        # Fix mismatches
        pdata_fixed, fixes = fix_process(pdata)
        
        if fixes:
            fixed_count += 1
            fix_report.append({
                'id': pid,
                'name': proc['name'],
                'nodes_fixed': fixes,
                'count': len(fixes)
            })
            print(f"✅ Fixed {pid}: {len(fixes)} nodes")
        
        # Save fixed version
        output_path = f'/workspace/fixed_processes/{org}/{pid}.json'
        with open(output_path, 'w') as f:
            json.dump(pdata_fixed, f, indent=2)
        
        if i % 10 == 0:
            print(f"   Progress: {i}/{len(processes)}...")
            time.sleep(0.2)
    
    except Exception as e:
        print(f"❌ Error with {pid}: {e}")

print()
print("=" * 80)
print(f"✅ COMPLETE: Fixed {fixed_count} processes")
print("=" * 80)
print()

# Save fix report
with open('/workspace/SHAPE_FIX_REPORT.json', 'w') as f:
    json.dump(fix_report, f, indent=2)

if fix_report:
    print(f"Sample fixes (first 10):\n")
    for item in fix_report[:10]:
        print(f"{item['name'][:60]}")
        print(f"  Fixed {item['count']} nodes: {', '.join(item['nodes_fixed'][:5])}")
        print()

print(f"📄 Full report saved to: SHAPE_FIX_REPORT.json")
print(f"📁 Fixed processes saved to: /workspace/fixed_processes/")
