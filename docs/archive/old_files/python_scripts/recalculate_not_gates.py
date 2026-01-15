#!/usr/bin/env python3
"""
Recalculate NOT gate counts after trapezoid fixes
"""

import json
import re
from glob import glob

print("📊 RECALCULATING NOT GATE COUNTS")
print("=" * 80)
print()

files = sorted(glob('gcs-processes/*/*.json'))
metadata_updates = {}

for filepath in files:
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        process_id = data['id']
        mermaid = data['mermaid']
        lines = mermaid.split('\n')
        
        # Count trapezoids (NOT gates)
        not_count = 0
        for line in lines:
            # Pattern: NODEID[\Text/]
            matches = re.findall(r'([A-Z][A-Z0-9]*)\s*\[\\([^\]]+)/\]', line)
            not_count += len(matches)
        
        metadata_updates[process_id] = not_count
    
    except Exception as e:
        print(f"✗ Error: {filepath}: {e}")

# Update metadata.json
with open('gcs-processes/metadata.json', 'r') as f:
    metadata = json.load(f)

total_before = sum(proc.get('notGates', 0) for proc in metadata['processes'])
total_after = sum(metadata_updates.values())

changed_processes = []
for proc in metadata['processes']:
    proc_id = proc['id']
    if proc_id in metadata_updates:
        old_count = proc.get('notGates', 0)
        new_count = metadata_updates[proc_id]
        
        if old_count != new_count:
            changed_processes.append({
                'id': proc_id,
                'old': old_count,
                'new': new_count
            })
        
        proc['notGates'] = new_count

# Save updated metadata
with open('gcs-processes/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(f"Total NOT gates before: {total_before}")
print(f"Total NOT gates after: {total_after}")
print(f"Reduction: {total_before - total_after}")
print()

if changed_processes:
    print(f"Changed processes ({len(changed_processes)}):")
    for proc in changed_processes:
        print(f"  {proc['id']}: {proc['old']} → {proc['new']}")

print()
print("=" * 80)
print("✅ METADATA UPDATED")
print("=" * 80)

