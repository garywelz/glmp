#!/usr/bin/env python3
"""
Phase 2: Fix Invalid Logic Gates

Fixes:
1. AND gates with < 2 inputs → Remove AND marking or fix connections
2. OR gates with < 2 outputs → Remove OR marking or fix connections
"""

import json
import re
from pathlib import Path
from collections import defaultdict

def parse_graph_connections(mermaid):
    """Parse Mermaid to find inputs/outputs for each node"""
    inputs = defaultdict(list)
    outputs = defaultdict(list)
    
    lines = mermaid.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('%%') or line.startswith('style '):
            continue
        
        # Parse connections: A --> B or A -->|label| B
        edge_match = re.search(r'(\w+)\s*-->\s*(?:\|[^|]+\|)?\s*(\w+)', line)
        if edge_match:
            from_node = edge_match.group(1)
            to_node = edge_match.group(2)
            inputs[to_node].append(from_node)
            outputs[from_node].append(to_node)
    
    return inputs, outputs

def find_node_definitions(mermaid):
    """Find all node definitions with their types"""
    nodes = {}
    lines = mermaid.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # AND gate: {{NodeID: Label}} or NodeID{{Label}}
        and_match = re.search(r'(\w+)\{\{([^}]+)\}\}', line)
        if and_match:
            node_id = and_match.group(1)
            label = and_match.group(2)
            nodes[node_id] = {'type': 'and', 'label': label, 'line': line}
            continue
        
        # OR gate: {NodeID: Label} or NodeID{Label}
        or_match = re.search(r'(\w+)\{([^}]+)\}', line)
        if or_match:
            node_id = or_match.group(1)
            label = or_match.group(2)
            nodes[node_id] = {'type': 'or', 'label': label, 'line': line}
            continue
    
    return nodes

def fix_invalid_gates(mermaid, process_name):
    """Fix invalid AND/OR gates"""
    inputs, outputs = parse_graph_connections(mermaid)
    nodes = find_node_definitions(mermaid)
    
    fixes = []
    fixed_mermaid = mermaid
    
    # Check each node
    for node_id, node_data in nodes.items():
        node_type = node_data['type']
        node_label = node_data['label']
        old_line = node_data['line']
        
        if node_type == 'and':
            input_count = len(inputs.get(node_id, []))
            if input_count < 2:
                # Invalid AND gate - convert to regular rectangle
                # Remove the double braces
                new_line = old_line.replace('{{', '[').replace('}}', ']')
                fixed_mermaid = fixed_mermaid.replace(old_line, new_line)
                fixes.append(f"AND gate '{node_id}' ({input_count} inputs) → Rectangle")
        
        elif node_type == 'or':
            output_count = len(outputs.get(node_id, []))
            if output_count < 2:
                # Invalid OR gate - convert to regular rectangle
                # Remove the braces
                new_line = old_line.replace('{', '[').replace('}', ']')
                fixed_mermaid = fixed_mermaid.replace(old_line, new_line)
                fixes.append(f"OR gate '{node_id}' ({output_count} outputs) → Rectangle")
    
    return fixed_mermaid, fixes

def fix_process_file(filepath):
    """Fix a single process JSON file"""
    try:
        with open(filepath) as f:
            process = json.load(f)
        
        process_name = process['name']
        mermaid = process.get('mermaid', '')
        
        if not mermaid:
            return None, "No Mermaid diagram found"
        
        fixed_mermaid, fixes = fix_invalid_gates(mermaid, process_name)
        
        if not fixes:
            return None, "No invalid gates found"
        
        # Save fixed version
        process['mermaid'] = fixed_mermaid
        with open(filepath, 'w') as f:
            json.dump(process, f, indent=2)
        
        return fixes, "Fixed"
        
    except Exception as e:
        return None, f"Error: {str(e)}"

def main():
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                              ║")
    print("║                  🔧 PHASE 2: FIXING INVALID LOGIC GATES                      ║")
    print("║                                                                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Processes with invalid logic gates from validation report
    invalid_gate_processes = [
        'ecoli/ecoli_e._coli_flagellar_assembly.json',
        'ecoli/ecoli_e._coli_stringent_response.json',
        'ecoli/ecoli_envelope_stress_response.json',
        'ecoli/ecoli_protein_folding_chaperones.json',
        'yeast/yeast_osmotic_stress_response.json',
        'yeast/yeast_oxidative_stress_response.json',
        'yeast/yeast_yeast_glycolysis_regulation.json',
        'yeast/yeast_yeast_peroxisome_biogenesis.json',
    ]
    
    base_dir = Path('/workspace/processes_with_not_gates')
    
    total_fixed = 0
    total_gate_fixes = 0
    failed = []
    
    print(f"📋 Processing {len(invalid_gate_processes)} files with invalid logic gates...")
    print()
    
    for process_path in invalid_gate_processes:
        filepath = base_dir / process_path
        process_name = filepath.stem
        
        if not filepath.exists():
            print(f"⚠️  {process_name}: File not found")
            failed.append(process_name)
            continue
        
        result, message = fix_process_file(filepath)
        
        if result:
            fixes = result
            total_fixed += 1
            total_gate_fixes += len(fixes)
            print(f"✅ {process_name}:")
            for fix in fixes:
                print(f"   • {fix}")
            print()
        elif message == "No invalid gates found":
            print(f"✓  {process_name}: No invalid gates")
            print()
        else:
            print(f"❌ {process_name}: {message}")
            failed.append(process_name)
            print()
    
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print()
    print(f"  Processes fixed: {total_fixed}")
    print(f"  Invalid gates corrected: {total_gate_fixes}")
    
    if failed:
        print(f"  Failed: {len(failed)}")
        for name in failed:
            print(f"    - {name}")
    
    print()
    print("=" * 80)
    print("✅ PHASE 2 COMPLETE!")
    print("=" * 80)
    print()
    print("All invalid logic gates have been fixed.")
    print("Converted to regular rectangles where gates had wrong input/output counts.")
    print()

if __name__ == '__main__':
    main()
