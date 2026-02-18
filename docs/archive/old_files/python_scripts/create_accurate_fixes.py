#!/usr/bin/env python3
"""
Create Accurate Fix List for Desktop Agent
===========================================
Filters out false positives and creates actionable fix list
"""

import json
import re
from pathlib import Path

# Load the scan results
with open('/workspace/misclassification_report.json', 'r') as f:
    scan_data = json.load(f)

# Filter for REAL enzymes (not false positives)
REAL_ENZYME_PATTERNS = [
    r'\bkinase\b',
    r'\bsynthase\b',
    r'\bpolymerase\b',
    r'\bligase\b',
    r'\btransferase\b',
    r'\bdehydrogenase\b',
    r'\bisomerase\b',
    r'\bhydrolase\b',
    r'\boxidase\b',
    r'\breductase\b',
    r'\bmutase\b',
    r'\bprotease\b',
    r'\bnuclease\b',
    r'\bpeptidase\b',
    r'\baconitase\b',
    r'\bcatalase\b',
    r'\bpermeases\b',
    r'\batpase\b',
    r'\bendonuclease\b',
    r'\bexonuclease\b',
]

def is_real_enzyme(text):
    """Check if text really describes an enzyme"""
    text_lower = text.lower()
    for pattern in REAL_ENZYME_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False

# Filter enzyme issues
real_enzyme_issues = []
for issue in scan_data['detailed_issues']['enzyme']:
    if is_real_enzyme(issue['text']):
        real_enzyme_issues.append(issue)

print("=" * 70)
print("🎯 ACCURATE MISCLASSIFICATION REPORT")
print("=" * 70)
print()
print(f"Total enzyme flags: {len(scan_data['detailed_issues']['enzyme'])}")
print(f"False positives:    {len(scan_data['detailed_issues']['enzyme']) - len(real_enzyme_issues)}")
print(f"REAL enzymes:       {len(real_enzyme_issues)}")
print()

# Group by process
by_process = {}
for issue in real_enzyme_issues:
    proc = issue['process']
    if proc not in by_process:
        by_process[proc] = []
    by_process[proc].append(issue)

print(f"Processes affected: {len(by_process)}")
print()

# Show top processes with most issues
print("Top processes with enzyme misclassifications:")
sorted_procs = sorted(by_process.items(), key=lambda x: -len(x[1]))
for proc, issues in sorted_procs[:15]:
    print(f"  {proc:50s}: {len(issues):3d} issues")
print()

# Create fix commands for desktop agent
print("=" * 70)
print("🔧 FIX COMMANDS FOR DESKTOP AGENT")
print("=" * 70)
print()

fixes_by_process = {}
for proc, issues in sorted_procs:
    fixes = []
    for issue in issues:
        fixes.append({
            'node_id': issue['node_id'],
            'current': issue['current_color'],
            'new': 'fab005',
            'reason': f"Enzyme: {issue['text'][:60]}"
        })
    fixes_by_process[proc] = fixes

# Save fix file
with open('/workspace/enzyme_fixes.json', 'w') as f:
    json.dump(fixes_by_process, f, indent=2)

print("✅ Created enzyme_fixes.json")
print()
print(f"Contains fixes for {len(fixes_by_process)} processes")
print(f"Total fixes: {len(real_enzyme_issues)}")
print()

# Show sample fixes
print("Sample fixes needed:")
print("-" * 70)
for proc, fixes in list(sorted_procs)[:5]:
    print(f"\n{proc}:")
    for fix in fixes[:3]:
        print(f"  Node {fix['node_id']}: #{fix['current']} → #{fix['new']}")
        print(f"    {fix['reason']}")

