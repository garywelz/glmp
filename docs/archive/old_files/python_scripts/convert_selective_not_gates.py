#!/usr/bin/env python3
"""
Option A: Selective NOT Gate Conversion

Converts nodes to red trapezoids if they represent:
1. Active repression/inhibition (Repressor blocks, Inhibitor prevents, etc.)
2. Process termination outcomes (Process terminates, Pathway ends, etc.)
3. Explicit negative branch outcomes (No expression, Blocked, Silenced, etc.)

Does NOT convert passive states like "Inactive form" or "Absent"
"""
import json
import re
import urllib.request
import time
import os

class NOTGateIdentifier:
    """Identifies nodes that should be NOT gates."""
    
    # Strong indicators - definitely NOT gates
    STRONG_NOT_PATTERNS = [
        r'(?:NOT|NOT:)',
        r'(?:Repress|repress|Repression|repression)',
        r'(?:Inhibit|inhibit|Inhibition|inhibition)',
        r'(?:Block|block|Blocked|blocked)',
        r'(?:Silenc|silenc)',
        r'(?:Prevent|prevent)',
        r'(?:Stop|stop|Halt|halt)',
        r'(?:Terminat|terminat)',  # Process terminates, Transcription terminates
        r'(?:No\s+(?:gene|expression|transcription|translation|synthesis|production))',
        r'(?:Inactive\s+(?:repressor|inhibitor))',  # Inactive repressor (double negative = NOT gate)
        r'(?:Pathway\s+(?:end|stop|terminat|halt))',
        r'(?:Process\s+(?:end|stop|terminat|halt))',
    ]
    
    # Moderate indicators - likely NOT gates in context
    MODERATE_NOT_PATTERNS = [
        r'(?:Degraded|degrad)',
        r'(?:Removed|removed)',
        r'(?:Unavailable|unavailable)',
        r'(?:Depleted|depleted)',
        r'(?:Weak|weak|Low|low)\s+(?:transcription|expression|activity)',
    ]
    
    # Exclude patterns - NOT NOT gates (passive states)
    EXCLUDE_PATTERNS = [
        r'^(?:Inactive|inactive)\s+(?:form|state)',  # "Inactive form" is passive
        r'^(?:Absent|absent)$',  # Just "Absent" is passive
        r'^(?:No\s+)?(?:product|molecule|protein)$',  # Just describing absence
    ]
    
    @classmethod
    def should_be_not_gate(cls, label):
        """Determine if a node label indicates it should be a NOT gate."""
        # Check exclusions first
        for pattern in cls.EXCLUDE_PATTERNS:
            if re.search(pattern, label, re.IGNORECASE):
                return False, "excluded_passive_state"
        
        # Check strong indicators
        for pattern in cls.STRONG_NOT_PATTERNS:
            if re.search(pattern, label, re.IGNORECASE):
                return True, "strong_not_indicator"
        
        # Check moderate indicators
        for pattern in cls.MODERATE_NOT_PATTERNS:
            if re.search(pattern, label, re.IGNORECASE):
                return True, "moderate_not_indicator"
        
        return False, "no_indicator"

def extract_all_nodes(mermaid):
    """Extract all node IDs and their labels from mermaid code."""
    nodes = {}
    
    # All possible node syntaxes
    patterns = [
        (r'(\w+)\[/([^/]+)/\]', 'trapezoid'),
        (r'(\w+)\{{{{([^}}]+)\}}}}', 'hexagon'),
        (r'(\w+)\{{([^{{}}]+)\}}', 'diamond'),
        (r'(\w+)\[([^\[/\\][^\]]*)\]', 'rectangle'),
        (r'(\w+)\(([^)]+)\)', 'rounded'),
    ]
    
    for pattern, shape in patterns:
        for match in re.finditer(pattern, mermaid):
            node_id = match.group(1)
            label = match.group(2)
            if node_id not in nodes:
                nodes[node_id] = {
                    'label': label,
                    'shape': shape,
                    'definition': match.group(0)
                }
    
    return nodes

def get_node_color(mermaid, node_id):
    """Get the current color of a node."""
    match = re.search(rf'style\s+{node_id}\s+fill:(#[0-9a-fA-F]{{6}})', mermaid)
    return match.group(1) if match else None

def convert_to_red_trapezoid(mermaid, node_id, current_def, label):
    """Convert a node to red trapezoid."""
    new_def = f'{node_id}[/{label}/]'
    
    # Replace definition
    mermaid = mermaid.replace(current_def, new_def, 1)
    
    # Update or add color
    color_pattern = rf'style\s+{node_id}\s+fill:#[0-9a-fA-F]{{6}}'
    if re.search(color_pattern, mermaid):
        mermaid = re.sub(color_pattern, f'style {node_id} fill:#e74c3c', mermaid)
    else:
        # Add color style at the end
        mermaid += f'\n    style {node_id} fill:#e74c3c,color:#fff'
    
    return mermaid

def process_single_file(process_data):
    """Convert NOT gates in a single process."""
    mermaid = process_data['mermaid']
    
    # Extract all nodes
    nodes = extract_all_nodes(mermaid)
    
    # Identify which should be NOT gates
    conversions = []
    
    for node_id, node_info in nodes.items():
        label = node_info['label']
        current_color = get_node_color(mermaid, node_id)
        
        # Skip if already red trapezoid
        if current_color == '#e74c3c' and node_info['shape'] == 'trapezoid':
            continue
        
        # Check if should be NOT gate
        should_convert, reason = NOTGateIdentifier.should_be_not_gate(label)
        
        if should_convert:
            # Convert to red trapezoid
            mermaid = convert_to_red_trapezoid(
                mermaid, 
                node_id, 
                node_info['definition'],
                label
            )
            conversions.append({
                'node_id': node_id,
                'label': label[:60],
                'reason': reason,
                'was_color': current_color,
                'was_shape': node_info['shape']
            })
    
    if conversions:
        process_data['mermaid'] = mermaid
    
    return process_data, conversions

# Main execution
print("🔧 OPTION A: SELECTIVE NOT GATE CONVERSION")
print("=" * 80)
print()
print("Converting nodes with active repression/inhibition logic to red trapezoids")
print()

# Fetch metadata
url = 'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/metadata.json'
with urllib.request.urlopen(url) as r:
    metadata = json.loads(r.read())

processes = metadata['processes']
print(f"Processing {len(processes)} processes...\n")

# Create output directories
os.makedirs('/workspace/processes_with_not_gates/ecoli', exist_ok=True)
os.makedirs('/workspace/processes_with_not_gates/yeast', exist_ok=True)
os.makedirs('/workspace/processes_with_not_gates/bacillus', exist_ok=True)

converted_processes = []
total_conversions = 0

for i, proc in enumerate(processes, 1):
    pid = proc['id']
    org = pid.split('_')[0]
    purl = f'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/{org}/{pid}.json'
    
    try:
        # Fetch original
        with urllib.request.urlopen(purl) as r:
            pdata = json.loads(r.read())
        
        # Convert NOT gates
        pdata_converted, conversions = process_single_file(pdata)
        
        if conversions:
            converted_processes.append({
                'id': pid,
                'name': proc['name'],
                'conversions': conversions,
                'count': len(conversions)
            })
            total_conversions += len(conversions)
            
            if len(converted_processes) <= 15:
                print(f"✅ {pid}: {len(conversions)} nodes converted")
                for conv in conversions[:3]:  # Show first 3
                    print(f"   • {conv['node_id']}: {conv['label'][:50]} ({conv['reason']})")
        
        # Save
        output_path = f'/workspace/processes_with_not_gates/{org}/{pid}.json'
        with open(output_path, 'w') as f:
            json.dump(pdata_converted, f, indent=2)
        
        if i % 20 == 0:
            print(f"\n   Progress: {i}/{len(processes)}...")
            time.sleep(0.2)
    
    except Exception as e:
        print(f"❌ Error with {pid}: {e}")

print()
print("=" * 80)
print(f"✅ COMPLETE: {len(converted_processes)} processes updated")
print(f"   Total conversions: {total_conversions} nodes")
print("=" * 80)
print()

# Save report
with open('/workspace/NOT_GATE_CONVERSIONS_REPORT.json', 'w') as f:
    json.dump(converted_processes, f, indent=2)

# Summary stats
if converted_processes:
    print("Conversion breakdown by reason:")
    from collections import Counter
    reasons = []
    for proc in converted_processes:
        for conv in proc['conversions']:
            reasons.append(conv['reason'])
    
    reason_counts = Counter(reasons)
    for reason, count in reason_counts.most_common():
        print(f"  {reason}: {count} nodes")
    
    print()
    print(f"📄 Detailed report: NOT_GATE_CONVERSIONS_REPORT.json")
    print(f"📁 Converted files: /workspace/processes_with_not_gates/")
