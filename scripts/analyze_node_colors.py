#!/usr/bin/env python3
"""
Analyze current node colors and create semantic classification
Helps identify which nodes should be which colors in new scheme
"""

import json
import re
from glob import glob
from collections import defaultdict

def extract_node_info(mermaid_code):
    """Extract nodes with their current colors and text"""
    nodes = {}
    
    lines = mermaid_code.split('\n')
    
    # Extract node definitions with their text
    for line in lines:
        # Skip comments and styling
        if line.strip().startswith('%%') or line.strip().startswith('style'):
            continue
        
        # Look for node definitions: A[Text], B{Text}, C{{Text}}, D[\Text/]
        # Patterns: NodeID[...] or NodeID{...} or NodeID{{...}} or NodeID[\.../]
        matches = re.findall(r'([A-Z][A-Z0-9]*)\s*[\[\{]([^\]\}]+)[\]\}]', line)
        for node_id, text in matches:
            if node_id not in nodes:
                nodes[node_id] = {
                    'text': text.replace('<br/>', ' ').strip()[:80],
                    'line': line.strip()[:100],
                    'color': None
                }
    
    # Extract styling
    for line in lines:
        if line.strip().startswith('style '):
            # Extract: style A fill:#ff6b6b,color:#fff
            match = re.search(r'style\s+([A-Z][A-Z0-9]*)\s+fill:(#[0-9a-fA-F]{6})', line)
            if match:
                node_id, color = match.groups()
                if node_id in nodes:
                    nodes[node_id]['color'] = color
    
    return nodes

def classify_node(node_info):
    """Classify node based on text and current color"""
    text = node_info['text'].lower()
    current_color = node_info['color']
    
    # Logic gates (by shape in Mermaid)
    if '{' in node_info['line'] or '{{' in node_info['line']:
        if 'and' in text:
            return 'and_gate'
        elif 'or' in text:
            return 'or_gate'
        else:
            return 'or_gate'  # Default for diamonds
    
    if '[\\' in node_info['line']:
        return 'not_gate'
    
    # Triggers/inputs - look for keywords
    trigger_keywords = ['environment', 'external', 'signal', 'start', 'input', 
                       'glucose in', 'lactose in', 'nutrient', 'stress', 'damage']
    if any(kw in text for kw in trigger_keywords):
        return 'trigger'
    
    # Current red nodes are often triggers
    if current_color == '#ff6b6b':
        return 'trigger'
    
    # Enzymes - look for keywords and protein names
    enzyme_keywords = ['kinase', 'ase', 'synthase', 'polymerase', 'ligase', 
                      'helicase', 'repressor', 'activator', 'protein']
    if any(kw in text for kw in enzyme_keywords):
        return 'enzyme'
    
    # Current yellow nodes are enzymes
    if current_color == '#ffd43b':
        return 'enzyme'
    
    # Processing - action verbs
    process_keywords = ['synthesis', 'transport', 'binding', 'assembly', 
                       'processing', 'modification', 'phosphorylation']
    if any(kw in text for kw in process_keywords):
        return 'processing'
    
    # Current green nodes are processing
    if current_color == '#51cf66':
        return 'processing'
    
    # Intermediates - metabolites, states
    intermediate_keywords = ['complex', 'intermediate', 'state', '-p ', 'atp', 
                            'adp', 'gtp', 'gdp', 'camp']
    if any(kw in text for kw in intermediate_keywords):
        return 'intermediate'
    
    # Current blue nodes are intermediates
    if current_color == '#74c0fc':
        return 'intermediate'
    
    # Products - look for final outputs
    product_keywords = ['production', 'output', 'growth', 'survival', 'response',
                       'adaptation', 'repair complete', 'synthesis complete']
    if any(kw in text for kw in product_keywords):
        return 'product'
    
    # Current violet/purple nodes
    if current_color in ['#b197fc', '#9775fa', '#000000']:
        return 'product'
    
    # Default: intermediate (most common)
    return 'intermediate'

def main():
    print("🎨 ANALYZING NODE COLORS FOR SEMANTIC CLASSIFICATION")
    print("=" * 70)
    print()
    
    # Analyze first 5 processes in detail
    files = sorted(glob('gcs-processes/*/*.json'))[:5]
    
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            process_name = data.get('name', 'Unknown')
            nodes = extract_node_info(data.get('mermaid', ''))
            
            print(f"\n{'='*70}")
            print(f"Process: {process_name}")
            print(f"Total nodes: {len(nodes)}")
            print("-" * 70)
            
            # Classify each node
            classifications = defaultdict(list)
            for node_id, info in sorted(nodes.items())[:15]:  # First 15 nodes
                node_type = classify_node(info)
                classifications[node_type].append(node_id)
                
                color_display = info['color'] if info['color'] else 'NO COLOR'
                print(f"  {node_id:<4s} | {color_display:<8s} | {node_type:<12s} | {info['text'][:40]}")
            
            if len(nodes) > 15:
                print(f"  ... and {len(nodes) - 15} more nodes")
            
            print(f"\n  Summary:")
            for node_type, node_list in sorted(classifications.items()):
                print(f"    {node_type}: {len(node_list)} nodes")
                
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 70)
    print("This analysis helps create the blueprint for color redesign")
    print("=" * 70)

if __name__ == "__main__":
    main()

