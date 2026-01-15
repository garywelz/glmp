#!/usr/bin/env python3
"""
Add Conditionals Count to Metadata
Calculate conditionals as: total nodes - (OR + AND + NOT gates)
"""

import json
from glob import glob

print("📊 CALCULATING CONDITIONALS FOR ALL PROCESSES")
print("=" * 80)
print()

# Load metadata
with open('gcs-processes/metadata.json', 'r') as f:
    metadata = json.load(f)

print(f"Loaded {len(metadata['processes'])} processes")
print()

updated_count = 0

for proc in metadata['processes']:
    proc_id = proc['id']
    nodes = proc.get('nodes', 0)
    or_gates = proc.get('logicGates', {}).get('or', 0)
    and_gates = proc.get('logicGates', {}).get('and', 0)
    not_gates = proc.get('notGates', 0)
    
    # Calculate conditionals: all other nodes that aren't logic gates
    conditionals = nodes - (or_gates + and_gates + not_gates)
    
    # Add to process
    proc['conditionals'] = conditionals
    updated_count += 1
    
    print(f"  {proc_id}: {conditionals} conditionals (nodes={nodes}, OR={or_gates}, AND={and_gates}, NOT={not_gates})")

print()
print("=" * 80)

# Calculate totals
total_nodes = sum(p.get('nodes', 0) for p in metadata['processes'])
total_conditionals = sum(p.get('conditionals', 0) for p in metadata['processes'])
total_or = sum(p.get('logicGates', {}).get('or', 0) for p in metadata['processes'])
total_and = sum(p.get('logicGates', {}).get('and', 0) for p in metadata['processes'])
total_not = sum(p.get('notGates', 0) for p in metadata['processes'])

print(f"📊 TOTALS:")
print(f"  Total Nodes: {total_nodes}")
print(f"  Conditionals: {total_conditionals} ({total_conditionals/total_nodes*100:.1f}%)")
print(f"  OR Gates: {total_or} ({total_or/total_nodes*100:.1f}%)")
print(f"  AND Gates: {total_and} ({total_and/total_nodes*100:.1f}%)")
print(f"  NOT Gates: {total_not} ({total_not/total_nodes*100:.1f}%)")
print()
print(f"  Average per process:")
print(f"    Conditionals: {total_conditionals/len(metadata['processes']):.1f}")
print(f"    OR: {total_or/len(metadata['processes']):.1f}")
print(f"    AND: {total_and/len(metadata['processes']):.1f}")
print(f"    NOT: {total_not/len(metadata['processes']):.1f}")
print()
print(f"  Ratio (normalized to 100 conditionals):")
avg_cond = total_conditionals / len(metadata['processes'])
avg_or = total_or / len(metadata['processes'])
avg_and = total_and / len(metadata['processes'])
avg_not = total_not / len(metadata['processes'])

norm_or = round((avg_or / avg_cond) * 100) if avg_cond > 0 else 0
norm_and = round((avg_and / avg_cond) * 100) if avg_cond > 0 else 0
norm_not = round((avg_not / avg_cond) * 100) if avg_cond > 0 else 0

print(f"    100:{norm_or}:{norm_and}:{norm_not}")
print("=" * 80)

# Save updated metadata
with open('gcs-processes/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(f"✅ Updated {updated_count} processes")
print("✅ Saved to gcs-processes/metadata.json")
print("=" * 80)

