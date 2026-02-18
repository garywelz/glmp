#!/usr/bin/env python3
"""
Simple Logical Structure Analysis for GLMP
Detects key logical structures in biological processes
"""

import os
import re
import json

def analyze_file_for_logic(file_path):
    """Analyze a single HTML file for logical structures"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract filename info
        filename = os.path.basename(file_path)
        organism = "E. coli" if "ecoli" in filename else "Unknown"
        
        # Simple pattern detection
        results = {
            'file': filename,
            'organism': organism,
            'and_gates': len(re.findall(r'{\s*.*?(AND|&|Both|All).*?\s*}', content, re.IGNORECASE)),
            'or_gates': len(re.findall(r'{\s*.*?(OR|\||\?|Either|Alternative).*?\s*}', content, re.IGNORECASE)),
            'feedback_loops': len(re.findall(r'(Feedback|Auto.*regulation|Loop)', content, re.IGNORECASE)),
            'checkpoints': len(re.findall(r'(Checkpoint|Control|Quality.*Control)', content, re.IGNORECASE)),
            'bistable_switches': len(re.findall(r'(Switch|Toggle|Bistable|High.*Low|Active.*Inactive)', content, re.IGNORECASE)),
            'amplification': len(re.findall(r'(Amplification|Enhancement|Accumulation|More|Increased)', content, re.IGNORECASE)),
            'cascades': len(re.findall(r'(Cascade|Sequential|Chain|Step.*[0-9])', content, re.IGNORECASE)),
            'oscillation': len(re.findall(r'(Oscillation|Oscillatory|Cycle|Cycling|Dynamic)', content, re.IGNORECASE))
        }
        
        # Calculate total and complexity
        logic_structures = ['and_gates', 'or_gates', 'feedback_loops', 'checkpoints', 
                          'bistable_switches', 'amplification', 'cascades', 'oscillation']
        
        results['total_logic_structures'] = sum(results[key] for key in logic_structures)
        
        # Complexity weighting
        weights = {
            'and_gates': 1.0, 'or_gates': 1.0, 'feedback_loops': 2.0, 'checkpoints': 1.5,
            'bistable_switches': 3.0, 'amplification': 1.5, 'cascades': 1.0, 'oscillation': 2.5
        }
        
        results['complexity_score'] = sum(results[key] * weights[key] for key in logic_structures)
        
        return results
        
    except Exception as e:
        return {'file': filename, 'error': str(e)}

def main():
    """Analyze all files in the biological_processes structure"""
    base_path = "/workspace/biological_processes"
    
    print("🧬 GLMP Logical Structure Analysis")
    print("=" * 50)
    
    all_results = []
    
    # Analyze each organism folder
    for organism_folder in ['ecoli', 'yeast', 'human']:
        folder_path = os.path.join(base_path, organism_folder)
        
        if not os.path.exists(folder_path):
            continue
            
        print(f"\n🔍 Analyzing {organism_folder.upper()}:")
        
        html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
        
        for html_file in html_files:
            file_path = os.path.join(folder_path, html_file)
            result = analyze_file_for_logic(file_path)
            
            if 'error' not in result:
                all_results.append(result)
                print(f"  📄 {html_file}:")
                print(f"    AND gates: {result['and_gates']}")
                print(f"    OR gates: {result['or_gates']}")
                print(f"    Feedback loops: {result['feedback_loops']}")
                print(f"    Checkpoints: {result['checkpoints']}")
                print(f"    Bistable switches: {result['bistable_switches']}")
                print(f"    Total structures: {result['total_logic_structures']}")
                print(f"    Complexity score: {result['complexity_score']:.1f}")
            else:
                print(f"  ❌ Error analyzing {html_file}: {result['error']}")
    
    # Summary statistics
    if all_results:
        print(f"\n📊 COLLECTION SUMMARY:")
        print(f"Files analyzed: {len(all_results)}")
        total_structures = sum(r['total_logic_structures'] for r in all_results)
        avg_complexity = sum(r['complexity_score'] for r in all_results) / len(all_results)
        print(f"Total logical structures: {total_structures}")
        print(f"Average complexity score: {avg_complexity:.1f}")
        
        # Most common structures
        structure_totals = {}
        for result in all_results:
            for key in ['and_gates', 'or_gates', 'feedback_loops', 'checkpoints', 
                       'bistable_switches', 'amplification', 'cascades', 'oscillation']:
                structure_totals[key] = structure_totals.get(key, 0) + result[key]
        
        print(f"\n🏆 Most Common Logical Structures:")
        sorted_structures = sorted(structure_totals.items(), key=lambda x: x[1], reverse=True)
        for structure, count in sorted_structures[:5]:
            print(f"  {structure.replace('_', ' ').title()}: {count}")
    
    # Save results
    with open('/workspace/biological_processes/logical_analysis_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n✅ Results saved to: biological_processes/logical_analysis_results.json")

if __name__ == "__main__":
    main()