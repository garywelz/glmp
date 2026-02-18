#!/usr/bin/env python3
"""
GLMP Logic Gate Counter
Automatically counts OR, AND, NOT gates from Mermaid code in JSON files
"""

import json
import re
import requests
from typing import Dict, List, Tuple
import time

def count_gates_from_mermaid(mermaid_code: str) -> Dict[str, int]:
    """Count logic gates from Mermaid code by analyzing style definitions"""
    
    # Count OR gates (yellow diamonds - #ffd600)
    or_gates = len(re.findall(r'fill:#ffd600', mermaid_code))
    
    # Count AND gates (purple hexagons - #7950f2) 
    and_gates = len(re.findall(r'fill:#7950f2', mermaid_code))
    
    # Count NOT gates (red trapezoids - #e74c3c)
    not_gates = len(re.findall(r'fill:#e74c3c', mermaid_code))
    
    return {
        'orGates': or_gates,
        'andGates': and_gates, 
        'notGates': not_gates
    }

def fetch_process_json(process_id: str) -> Dict:
    """Fetch JSON data for a process from GCS"""
    url = f"https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/{process_id}.json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {process_id}: {e}")
        return None

def analyze_process(process_id: str) -> Dict:
    """Analyze a single process and return corrected counts"""
    print(f"Analyzing {process_id}...")
    
    data = fetch_process_json(process_id)
    if not data:
        return None
    
    # Get Mermaid code
    mermaid_code = data.get('mermaid', '')
    if not mermaid_code:
        print(f"No Mermaid code found for {process_id}")
        return None
    
    # Count gates from Mermaid code
    actual_counts = count_gates_from_mermaid(mermaid_code)
    
    # Get database counts for comparison
    db_counts = data.get('complexity', {}).get('logicGates', {})
    
    return {
        'processId': process_id,
        'name': data.get('name', ''),
        'organism': data.get('organism', ''),
        'category': data.get('category', ''),
        'databaseCounts': {
            'orGates': db_counts.get('orGates', 0),
            'andGates': db_counts.get('andGates', 0),
            'notGates': db_counts.get('notGates', 0)
        },
        'actualCounts': actual_counts,
        'discrepancies': {
            'orGates': actual_counts['orGates'] - db_counts.get('orGates', 0),
            'andGates': actual_counts['andGates'] - db_counts.get('andGates', 0),
            'notGates': actual_counts['notGates'] - db_counts.get('notGates', 0)
        }
    }

def main():
    """Main function to analyze all processes"""
    
    # List of all process IDs (you'll need to provide this)
    # For now, let's test with a few known processes
    test_processes = [
        'ecoli_amino_acid_biosynthesis',
        'ecoli_lac_operon',
        'ecoli_tryptophan_biosynthesis',
        'yeast_cell_cycle',
        'ecoli_dna_replication'
    ]
    
    print("GLMP Logic Gate Counter")
    print("=" * 50)
    
    results = []
    total_discrepancies = {'orGates': 0, 'andGates': 0, 'notGates': 0}
    
    for process_id in test_processes:
        result = analyze_process(process_id)
        if result:
            results.append(result)
            
            # Accumulate discrepancies
            for gate_type in ['orGates', 'andGates', 'notGates']:
                total_discrepancies[gate_type] += result['discrepancies'][gate_type]
            
            print(f"  {result['name']}")
            print(f"    Database: OR={result['databaseCounts']['orGates']}, AND={result['databaseCounts']['andGates']}, NOT={result['databaseCounts']['notGates']}")
            print(f"    Actual:   OR={result['actualCounts']['orGates']}, AND={result['actualCounts']['andGates']}, NOT={result['actualCounts']['notGates']}")
            print(f"    Diff:     OR={result['discrepancies']['orGates']:+, AND={result['discrepancies']['andGates']:+, NOT={result['discrepancies']['notGates']:+}")
            print()
        
        time.sleep(0.5)  # Be nice to the server
    
    print("SUMMARY")
    print("=" * 50)
    print(f"Processes analyzed: {len(results)}")
    print(f"Total discrepancies:")
    print(f"  OR Gates:  {total_discrepancies['orGates']:+}")
    print(f"  AND Gates: {total_discrepancies['andGates']:+}")
    print(f"  NOT Gates: {total_discrepancies['notGates']:+}")
    
    # Save detailed results
    with open('logic_gate_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to logic_gate_analysis.json")

if __name__ == "__main__":
    main()
