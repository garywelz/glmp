#!/usr/bin/env python3
"""
Audit NOT Gates for Misuse
Check if trapezoids are truly blocking/inhibiting or just "inactive states"
"""

import json
import re
from glob import glob

print("🔍 AUDITING NOT GATES (TRAPEZOIDS)")
print("=" * 80)
print()
print("Checking for trapezoids with outgoing flows (potential misuse)...")
print()

files = sorted(glob('gcs-processes/*/*.json'))
suspicious_traps = []
valid_traps = []

for filepath in files:
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        process_id = data['id']
        mermaid = data['mermaid']
        lines = mermaid.split('\n')
        
        # Find all trapezoid nodes
        trap_nodes = {}
        for line in lines:
            # Pattern: NODEID[\Text/]
            matches = re.findall(r'([A-Z][A-Z0-9]*)\s*\[\\([^\]]+)/\]', line)
            for node_id, text in matches:
                clean_text = text.replace('<br/>', ' ').replace('\\n', ' ').strip()
                trap_nodes[node_id] = clean_text
        
        if not trap_nodes:
            continue
        
        # Find all edges
        edges = {}
        for line in lines:
            # Match arrows: NODEID1 --> NODEID2 or NODEID1 -->|label| NODEID2
            arrow_matches = re.findall(r'([A-Z][A-Z0-9]*)\s*-->[^\n]*?([A-Z][A-Z0-9]*)', line)
            for from_node, to_node in arrow_matches:
                if from_node not in edges:
                    edges[from_node] = []
                edges[from_node].append(to_node)
        
        # Check each trapezoid
        for trap_id, trap_text in trap_nodes.items():
            has_outgoing = trap_id in edges and len(edges[trap_id]) > 0
            
            # Keywords that suggest it's a valid NOT gate (blocking/inhibiting)
            blocking_keywords = [
                'repression', 'repressor', 'inhibit', 'block', 'prevent',
                'suppress', 'silence', 'inactive complex', 'degraded',
                'no synthesis', 'no expression', 'no production',
                'cannot', 'unable', 'arrested', 'stalled'
            ]
            
            # Keywords that suggest it's misused (just an inactive state)
            inactive_keywords = [
                'inactive form', 'apo-form', 'unbound', 'free',
                'inactive state', 'dormant', 'resting'
            ]
            
            text_lower = trap_text.lower()
            is_blocking = any(kw in text_lower for kw in blocking_keywords)
            is_inactive_state = any(kw in text_lower for kw in inactive_keywords)
            
            if has_outgoing:
                # Trapezoid with outgoing edges - suspicious unless it's a clear NOT gate
                if not is_blocking or is_inactive_state:
                    suspicious_traps.append({
                        'process': process_id,
                        'node': trap_id,
                        'text': trap_text,
                        'outgoing': edges[trap_id],
                        'reason': 'Has outgoing flow but not clearly blocking'
                    })
                else:
                    valid_traps.append({
                        'process': process_id,
                        'node': trap_id,
                        'text': trap_text,
                        'type': 'conditional_block'
                    })
            else:
                # No outgoing edges - terminal
                if is_blocking:
                    valid_traps.append({
                        'process': process_id,
                        'node': trap_id,
                        'text': trap_text,
                        'type': 'terminal_block'
                    })
                else:
                    suspicious_traps.append({
                        'process': process_id,
                        'node': trap_id,
                        'text': trap_text,
                        'outgoing': [],
                        'reason': 'Terminal but not clearly blocking'
                    })
    
    except Exception as e:
        print(f"✗ Error: {filepath}: {e}")

print("=" * 80)
print(f"📊 AUDIT RESULTS")
print("=" * 80)
print(f"Valid NOT gates: {len(valid_traps)}")
print(f"Suspicious trapezoids: {len(suspicious_traps)}")
print()

if suspicious_traps:
    print("⚠️  SUSPICIOUS TRAPEZOIDS (may need fixing):")
    print("-" * 80)
    for trap in suspicious_traps[:20]:  # Show first 20
        print(f"\n{trap['process']}")
        print(f"  Node: {trap['node']}")
        print(f"  Text: {trap['text'][:60]}...")
        print(f"  Outgoing: {trap['outgoing']}")
        print(f"  Reason: {trap['reason']}")
    
    if len(suspicious_traps) > 20:
        print(f"\n... and {len(suspicious_traps) - 20} more")

print()
print("=" * 80)
print(f"✅ AUDIT COMPLETE")
print("=" * 80)
print()
print("RECOMMENDATION:")
if len(suspicious_traps) < 10:
    print("  Few suspicious cases - review manually")
elif len(suspicious_traps) < 30:
    print("  Moderate number - may want to fix the most obvious ones")
else:
    print("  Many suspicious cases - consider systematic review")
print()
print("Valid NOT gates represent:")
print("  - Terminal blocking (e.g., 'Arginine Biosynthesis OFF')")
print("  - Conditional blocking with alternative paths")
print("=" * 80)

# Save detailed report
with open('NOT_GATE_AUDIT_REPORT.json', 'w') as f:
    json.dump({
        'valid_not_gates': valid_traps,
        'suspicious_trapezoids': suspicious_traps,
        'summary': {
            'total_valid': len(valid_traps),
            'total_suspicious': len(suspicious_traps),
            'percent_valid': round(len(valid_traps) / (len(valid_traps) + len(suspicious_traps)) * 100, 1) if (len(valid_traps) + len(suspicious_traps)) > 0 else 0
        }
    }, f, indent=2)

print(f"\nDetailed report saved to: NOT_GATE_AUDIT_REPORT.json")

