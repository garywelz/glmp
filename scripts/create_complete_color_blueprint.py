#!/usr/bin/env python3
"""
Create Complete Color Blueprint for Phase 2
Classifies EVERY node in EVERY process semantically
Output: JSON blueprint for cursor.com agent to apply
"""

import json
import re
from glob import glob
from collections import defaultdict

# New color scheme
COLOR_MAP = {
    'trigger': '#51cf66',      # Green (was red)
    'enzyme': '#fab005',        # Amber (slightly warmer than old yellow)
    'processing': '#74c0fc',    # Sky Blue (was green)
    'intermediate': '#ffa07a',  # Light Salmon (was blue)
    'product': '#000000',       # Black (was violet)
    'or_gate': '#ff9f43',       # Orange (keep)
    'and_gate': '#7950f2',      # Purple (updated from lavender)
    'not_gate': '#e74c3c'       # Red (new)
}

def extract_all_nodes(mermaid_code):
    """Extract all node IDs and their definitions"""
    nodes = {}
    lines = mermaid_code.split('\n')
    
    for line in lines:
        if line.strip().startswith('%%') or line.strip().startswith('style'):
            continue
        
        # Find all node definitions
        # Patterns: A[Text], B{Text}, C{{Text}}, D[\Text/], E(Text), F([Text])
        
        # First check for trapezoids (NOT gates): [\Text/]
        trap_matches = re.findall(r'([A-Z][A-Z0-9]*)\s*\[\\([^\]]+)/\]', line)
        for node_id, text in trap_matches:
            if node_id not in nodes:
                nodes[node_id] = {
                    'text': text.replace('<br/>', ' ').replace('\\n', ' ').strip(),
                    'shape': 'trapezoid'
                }
        
        # Then check for hexagons: {{Text}}
        hex_matches = re.findall(r'([A-Z][A-Z0-9]*)\s*\{\{([^\}]+)\}\}', line)
        for node_id, text in hex_matches:
            if node_id not in nodes:
                nodes[node_id] = {
                    'text': text.replace('<br/>', ' ').replace('\\n', ' ').strip(),
                    'shape': 'hexagon'
                }
        
        # Then other patterns
        patterns = [
            (r'([A-Z][A-Z0-9]*)\s*\{([^\}]+)\}', 'diamond'),        # {Text}
            (r'([A-Z][A-Z0-9]*)\s*\[([^\]\\]+)\]', 'rectangle'),    # [Text] (not trapezoid)
            (r'([A-Z][A-Z0-9]*)\s*\(([^\)]+)\)', 'rounded'),        # (Text)
            (r'([A-Z][A-Z0-9]*)\s*\(\[([^\]]+)\]\)', 'stadium'),    # ([Text])
        ]
        
        for pattern, shape in patterns:
            matches = re.findall(pattern, line)
            for node_id, text in matches:
                if node_id not in nodes:
                    nodes[node_id] = {
                        'text': text.replace('<br/>', ' ').replace('\\n', ' ').strip(),
                        'shape': shape
                    }
    
    return nodes

def classify_node_semantic(node_id, node_info):
    """Classify node based on text, shape, and biological meaning"""
    text = node_info['text'].lower()
    shape = node_info['shape']
    
    # Logic gates by shape
    if shape == 'hexagon':
        return 'and_gate'
    elif shape == 'diamond':
        return 'or_gate'
    elif shape == 'trapezoid':
        return 'not_gate'
    
    # Triggers - environmental inputs (usually first nodes: A, B, C, etc.)
    trigger_keywords = [
        'environment', 'external', 'input', 'signal',
        'nutrient', 'stress', 'damage', 'depletion',
        'lactose in', 'glucose in', 'present', 'limitation',
        'low energy', 'starvation', 'shock'
    ]
    if any(kw in text for kw in trigger_keywords):
        return 'trigger'
    
    # First few nodes (A-E) often triggers
    if node_id in ['A', 'B', 'C', 'D', 'E'] and len(text) < 50:
        if 'synthesis' not in text and 'complex' not in text:
            return 'trigger'
    
    # Enzymes - proteins with names
    enzyme_keywords = [
        'kinase', 'phosphatase', 'polymerase', 'ligase', 'helicase',
        'synthetase', 'synthase', 'reductase', 'oxidase', 'hydrolase',
        'transferase', 'isomerase', 'protease', 'nuclease',
        'repressor', 'activator', 'protein', 'enzyme', 'factor',
        'dnaa', 'dnab', 'dnac', 'rpoa', 'rpob', 'laci', 'trpr'
    ]
    if any(kw in text for kw in enzyme_keywords):
        return 'enzyme'
    
    # Processing - actions/operations
    processing_keywords = [
        'synthesis', 'transport', 'binding', 'assembly', 'cleavage',
        'processing', 'modification', 'phosphorylation', 'activation',
        'transcription', 'translation', 'replication', 'repair',
        'degradation', 'hydrolysis', 'import', 'export'
    ]
    if any(kw in text for kw in processing_keywords):
        return 'processing'
    
    # Products - final outputs (often stadium shape or last nodes)
    product_keywords = [
        'production', 'output', 'growth', 'survival', 'adaptation',
        'complete', 'equilibrium', 'homeostasis', 'cell', 'energy',
        'response', 'repair complete', 'cycle complete'
    ]
    if any(kw in text for kw in product_keywords) or shape == 'stadium':
        return 'product'
    
    # Intermediates - molecular states, compounds (default for most)
    # Keywords: ATP, metabolites, complexes, states
    return 'intermediate'

def create_blueprint():
    """Create complete color blueprint for all processes"""
    print("🎨 CREATING COMPLETE COLOR BLUEPRINT")
    print("=" * 80)
    print()
    print("This will classify EVERY node in EVERY process...")
    print("Estimated time: 2-3 minutes")
    print()
    
    blueprint = {}
    stats = defaultdict(int)
    unstyled_nodes = []
    
    files = sorted(glob('gcs-processes/*/*.json'))
    
    for i, filepath in enumerate(files, 1):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            process_id = data.get('id', '')
            process_name = data.get('name', '')
            mermaid = data.get('mermaid', '')
            
            # Extract all nodes
            nodes = extract_all_nodes(mermaid)
            
            # Classify each node
            blueprint[process_id] = {}
            
            for node_id, node_info in nodes.items():
                classification = classify_node_semantic(node_id, node_info)
                color = COLOR_MAP[classification]
                
                blueprint[process_id][node_id] = {
                    'type': classification,
                    'color': color,
                    'text': node_info['text'][:60],
                    'shape': node_info['shape']
                }
                
                stats[classification] += 1
            
            # Track unstyled in original
            current_styles = len(re.findall(r'style [A-Z]', mermaid))
            if current_styles < len(nodes):
                unstyled_nodes.append({
                    'process': process_name,
                    'total': len(nodes),
                    'styled': current_styles,
                    'unstyled': len(nodes) - current_styles
                })
            
            if i % 10 == 0:
                print(f"  Processed {i}/{len(files)} files...")
                
        except Exception as e:
            print(f"  ⚠️  Error in {filepath}: {e}")
    
    print()
    print("=" * 80)
    print("📊 CLASSIFICATION STATISTICS")
    print("=" * 80)
    
    for node_type, count in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {node_type:<15s}: {count:,} nodes")
    
    total_nodes = sum(stats.values())
    print(f"\n  TOTAL: {total_nodes:,} nodes classified")
    
    # Show processes with most unstyled nodes
    print()
    print("=" * 80)
    print("🎯 PROCESSES WITH MOST UNSTYLED NODES (Top 10)")
    print("=" * 80)
    
    for proc in sorted(unstyled_nodes, key=lambda x: -x['unstyled'])[:10]:
        pct = proc['unstyled'] / proc['total'] * 100
        print(f"  {proc['process']:<50s}: {proc['unstyled']:3d} unstyled ({pct:.0f}%)")
    
    # Save blueprint
    output_file = 'COLOR_BLUEPRINT_COMPLETE.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(blueprint, f, indent=2, ensure_ascii=False)
    
    print()
    print("=" * 80)
    print(f"✅ BLUEPRINT SAVED: {output_file}")
    print("=" * 80)
    print()
    print("📦 READY FOR CURSOR.COM AGENT")
    print()
    print("This blueprint contains:")
    print(f"  • {len(blueprint)} processes")
    print(f"  • {total_nodes:,} nodes classified")
    print(f"  • Complete color assignments")
    print(f"  • Node types and shapes")
    print()
    print("Cursor.com agent can now apply these colors systematically!")
    print("=" * 80)

if __name__ == "__main__":
    create_blueprint()

