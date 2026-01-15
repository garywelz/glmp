#!/usr/bin/env python3
"""
Validate Logic Gate Counts in GLMP Process JSON Files

This script ensures that metadata counts match actual visual counts
in Mermaid flowcharts. Critical for data integrity and user verification.

Usage:
    python3 validate_logic_gates.py <json_file>
    python3 validate_logic_gates.py --fix <json_file>  # Auto-correct metadata
"""

import json
import re
import sys
from pathlib import Path

def count_logic_gates(mermaid_code):
    """
    Count actual logic gates in Mermaid flowchart by parsing node shapes.
    
    OR gates: {{...}} (diamonds)
    AND gates: [[[...]]] (hexagons)  
    NOT gates: [/.../] (inverted trapezoids)
    """
    # Count OR gates (diamond nodes {{...}})
    or_gates = len(re.findall(r'\w+\{\{', mermaid_code))
    
    # Count AND gates (hexagon nodes [[[...]]])
    # Note: Must escape [ and ] in regex
    and_gates = len(re.findall(r'\w+\[\[\[', mermaid_code))
    
    # Count NOT gates (inverted trapezoid nodes [/.../])
    not_gates = len(re.findall(r'\w+\[/', mermaid_code))
    
    return {
        'or': or_gates,
        'and': and_gates,
        'not': not_gates
    }

def get_gate_node_names(mermaid_code):
    """Extract names of all logic gate nodes for detailed reporting."""
    or_nodes = re.findall(r'(\w+)\{\{', mermaid_code)
    and_nodes = re.findall(r'(\w+)\[\[\[', mermaid_code)
    not_nodes = re.findall(r'(\w+)\[/', mermaid_code)
    
    return {
        'or': or_nodes,
        'and': and_nodes,
        'not': not_nodes
    }

def validate_process(json_file, fix=False):
    """
    Validate a process JSON file.
    
    Args:
        json_file: Path to JSON file
        fix: If True, auto-correct metadata to match visual count
    
    Returns:
        dict with validation results
    """
    with open(json_file) as f:
        data = json.load(f)
    
    # Get metadata claims
    metadata_gates = data.get('logicGates', {})
    claimed_or = metadata_gates.get('or', 0)
    claimed_and = metadata_gates.get('and', 0)
    claimed_not = metadata_gates.get('not', 0)
    
    # Count actual gates in Mermaid
    mermaid = data.get('mermaid', '')
    actual_gates = count_logic_gates(mermaid)
    gate_nodes = get_gate_node_names(mermaid)
    
    # Check for discrepancies
    discrepancies = []
    if claimed_or != actual_gates['or']:
        discrepancies.append(f"OR gates: claimed {claimed_or}, actual {actual_gates['or']}")
    if claimed_and != actual_gates['and']:
        discrepancies.append(f"AND gates: claimed {claimed_and}, actual {actual_gates['and']}")
    if claimed_not != actual_gates['not']:
        discrepancies.append(f"NOT gates: claimed {claimed_not}, actual {actual_gates['not']}")
    
    result = {
        'file': str(json_file),
        'process_name': data.get('name', 'Unknown'),
        'valid': len(discrepancies) == 0,
        'claimed': {
            'or': claimed_or,
            'and': claimed_and,
            'not': claimed_not
        },
        'actual': actual_gates,
        'discrepancies': discrepancies,
        'gate_nodes': gate_nodes
    }
    
    # Fix if requested
    if fix and not result['valid']:
        data['logicGates'] = actual_gates
        
        # Recalculate conditionals
        total_gates = actual_gates['or'] + actual_gates['and'] + actual_gates['not']
        total_nodes = data.get('nodes', 0)
        data['conditionals'] = total_nodes - total_gates
        
        # Write back
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        result['fixed'] = True
    
    return result

def print_validation_report(result):
    """Print a nice validation report."""
    print("=" * 70)
    print(f"📄 File: {Path(result['file']).name}")
    print(f"🧬 Process: {result['process_name']}")
    print("=" * 70)
    
    if result['valid']:
        print("✅ VALIDATION PASSED - Counts match!")
        print()
        print(f"  OR Gates:  {result['actual']['or']}")
        print(f"  AND Gates: {result['actual']['and']}")
        print(f"  NOT Gates: {result['actual']['not']}")
    else:
        print("❌ VALIDATION FAILED - Discrepancies found!")
        print()
        for disc in result['discrepancies']:
            print(f"  ⚠️  {disc}")
        print()
        print("Claimed:")
        print(f"  OR: {result['claimed']['or']}, AND: {result['claimed']['and']}, NOT: {result['claimed']['not']}")
        print()
        print("Actual (visual count):")
        print(f"  OR: {result['actual']['or']}, AND: {result['actual']['and']}, NOT: {result['actual']['not']}")
    
    # Show gate node names
    if result['gate_nodes']['or'] or result['gate_nodes']['and'] or result['gate_nodes']['not']:
        print()
        print("Gate Nodes:")
        if result['gate_nodes']['or']:
            print(f"  OR ({len(result['gate_nodes']['or'])}):", ', '.join(result['gate_nodes']['or']))
        if result['gate_nodes']['and']:
            print(f"  AND ({len(result['gate_nodes']['and'])}):", ', '.join(result['gate_nodes']['and']))
        if result['gate_nodes']['not']:
            print(f"  NOT ({len(result['gate_nodes']['not'])}):", ', '.join(result['gate_nodes']['not']))
    
    if result.get('fixed'):
        print()
        print("✅ FIXED - Metadata updated to match visual count")
    
    print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 validate_logic_gates.py <json_file>")
        print("       python3 validate_logic_gates.py --fix <json_file>")
        sys.exit(1)
    
    fix_mode = False
    if sys.argv[1] == '--fix':
        fix_mode = True
        json_file = sys.argv[2]
    else:
        json_file = sys.argv[1]
    
    result = validate_process(json_file, fix=fix_mode)
    print_validation_report(result)
    
    # Exit code: 0 if valid, 1 if invalid
    sys.exit(0 if result['valid'] else 1)
