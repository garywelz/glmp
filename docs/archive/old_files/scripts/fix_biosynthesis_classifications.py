#!/usr/bin/env python3
"""
Fix Classification Errors in Biosynthesis Pathways
Distinguish enzymatic reactions from enzyme proteins
"""

import json
import re
from glob import glob

# Patterns that indicate enzymatic REACTIONS (should be processing/sky blue)
# These are actions, not objects
REACTION_KEYWORDS = [
    'synthase', 'kinase', 'phosphatase', 'reductase', 'oxidase', 'hydrolase',
    'transferase', 'isomerase', 'dehydrogenase', 'carboxylase', 'decarboxylase',
    'ligase', 'lyase', 'mutase', 'cyclase', 'methylase', 'demethylase',
    'acetylase', 'deacetylase', 'hydroxylase', 'aminotransferase',
    'transaminase', 'protease', 'nuclease', 'polymerase', 'helicase',
    'topoisomerase', 'recombinase'
]

# Patterns that indicate enzyme PROTEINS (should be amber)
ENZYME_PROTEIN_PATTERNS = [
    r'\bArg[A-Z]\s+Enzyme\b',
    r'\bTrp[A-Z]\s+Enzyme\b',
    r'\b[A-Z][a-z]+[A-Z]\s+Enzyme\b',
    r'\b[A-Z][a-z]+[A-Z]\s+Protein\b',
    r'\bEnzyme\s+[A-Z]',
]

def is_enzymatic_reaction(text):
    """Check if text describes an enzymatic reaction (action)"""
    text_lower = text.lower()
    
    # If it explicitly says "Enzyme" or "Protein" it's an object
    if re.search(r'\benzyme\b|\bprotein\b', text_lower):
        # But check if it matches enzyme protein patterns
        for pattern in ENZYME_PROTEIN_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return False  # It's an enzyme protein
        # If no protein pattern match, might be something else
        if 'enzyme' in text_lower and 'synthesis' not in text_lower:
            return False  # Likely enzyme protein
    
    # Check for reaction keywords
    for keyword in REACTION_KEYWORDS:
        if keyword in text_lower:
            # Make sure it's not "X Enzyme" format
            if not re.search(rf'{keyword}\s+enzyme', text_lower):
                return True  # It's a reaction
    
    return False

def should_be_product(text):
    """Check if node should be a product (black)"""
    text_lower = text.lower()
    
    product_keywords = [
        'product', 'outcome', 'equilibrium', 'homeostasis',
        'final', 'terminal', 'complete', 'end state',
        'system state', 'established', 'maintained'
    ]
    
    # Check for product keywords
    for keyword in product_keywords:
        if keyword in text_lower:
            return True
    
    # Check for specific product patterns
    if re.search(r'l-\w+\s+product', text_lower):  # e.g., "L-Arginine Product"
        return True
    
    return False

print("🔧 FIXING CLASSIFICATION ERRORS")
print("=" * 80)
print()

files = sorted(glob('gcs-processes/*/*.json'))
total_fixes = 0
processes_fixed = []

for filepath in files:
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        process_id = data['id']
        mermaid = data['mermaid']
        lines = mermaid.split('\n')
        
        fixes_in_this_process = 0
        new_styles = {}
        
        # Parse existing nodes and their text
        node_texts = {}
        for line in lines:
            # Extract node definitions
            # Pattern: NODEID[Text] or NODEID{Text} etc.
            patterns = [
                (r'([A-Z][A-Z0-9]*)\s*\[([^\]\\]+)\]', 'rectangle'),
                (r'([A-Z][A-Z0-9]*)\s*\{([^\}]+)\}', 'diamond'),
                (r'([A-Z][A-Z0-9]*)\s*\{\{([^\}]+)\}\}', 'hexagon'),
                (r'([A-Z][A-Z0-9]*)\s*\(([^\)]+)\)', 'rounded'),
                (r'([A-Z][A-Z0-9]*)\s*\(\[([^\]]+)\]\)', 'stadium'),
            ]
            
            for pattern, shape in patterns:
                matches = re.findall(pattern, line)
                for node_id, text in matches:
                    if node_id not in node_texts:
                        clean_text = text.replace('<br/>', ' ').replace('\\n', ' ').strip()
                        node_texts[node_id] = clean_text
        
        # Check for misclassifications
        for line in lines:
            if line.strip().startswith('style '):
                match = re.match(r'\s*style\s+([A-Z][A-Z0-9]*)\s+fill:(#[0-9a-fA-F]+)', line)
                if match:
                    node_id = match.group(1)
                    current_color = match.group(2)
                    
                    if node_id in node_texts:
                        text = node_texts[node_id]
                        
                        # Check if it's an enzymatic reaction misclassified as enzyme
                        if current_color == '#ffa726' and is_enzymatic_reaction(text):
                            new_styles[node_id] = '#42a5f5'  # Change to processing blue
                            fixes_in_this_process += 1
                            print(f"  {process_id}: {node_id} [{text[:40]}...] enzyme→processing")
                        
                        # Check if it should be a product
                        elif current_color in ['#b3e5fc', '#ffa726', '#42a5f5'] and should_be_product(text):
                            new_styles[node_id] = '#000000'  # Change to product black
                            fixes_in_this_process += 1
                            print(f"  {process_id}: {node_id} [{text[:40]}...] →product")
        
        # Apply fixes if any
        if fixes_in_this_process > 0:
            new_lines = []
            for line in lines:
                updated = False
                for node_id, new_color in new_styles.items():
                    if line.strip().startswith(f'style {node_id} '):
                        text_color = '#fff' if new_color in ['#51cf66', '#ffa726', '#42a5f5', '#7950f2', '#e74c3c', '#000000'] else '#000'
                        new_lines.append(f'    style {node_id} fill:{new_color},color:{text_color}')
                        updated = True
                        break
                if not updated:
                    new_lines.append(line)
            
            data['mermaid'] = '\n'.join(new_lines)
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            total_fixes += fixes_in_this_process
            processes_fixed.append(process_id)
    
    except Exception as e:
        print(f"✗ Error: {filepath}: {e}")

print()
print("=" * 80)
print(f"✅ CLASSIFICATION FIXES COMPLETE")
print("=" * 80)
print(f"Total fixes applied: {total_fixes}")
print(f"Processes updated: {len(processes_fixed)}")
if processes_fixed:
    print(f"\nProcesses fixed:")
    for proc in processes_fixed:
        print(f"  - {proc}")
print("=" * 80)

