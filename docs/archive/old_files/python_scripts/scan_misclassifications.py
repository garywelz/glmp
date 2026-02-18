#!/usr/bin/env python3
"""
Scan All Processes for Color Misclassifications
================================================
Identifies nodes that appear to be misclassified based on their text content
"""

import json
import re
from pathlib import Path
from collections import defaultdict

# Expected colors for each category
EXPECTED_COLORS = {
    'trigger': 'f51cf66',
    'enzyme': 'fab005',
    'processing': '74c0fc',
    'intermediate': 'ffa07a',
    'or_gate': 'ff9f43',
    'and_gate': '7950f2',
    'not_gate': 'e74c3c',
    'product': '000000'
}

# Keywords to identify node types
ENZYME_KEYWORDS = [
    'ase', 'kinase', 'synthase', 'polymerase', 'ligase', 'transferase',
    'dehydrogenase', 'isomerase', 'lyase', 'hydrolase', 'oxidase',
    'reductase', 'mutase', 'enzyme', 'protease', 'nuclease', 'peptidase'
]

TRIGGER_KEYWORDS = [
    'signal', 'stress', 'starvation', 'damage', 'shock', 'depletion',
    'present', 'absent', 'high', 'low', 'temperature', 'ph', 'nutrient',
    'oxygen', 'glucose', 'limitation', 'abundance', 'external'
]

PROCESSING_KEYWORDS = [
    'phosphorylation', 'transcription', 'translation', 'binding',
    'activation', 'cleavage', 'oxidation', 'reduction', 'methylation',
    'acetylation', 'ubiquitination', 'assembly', 'degradation',
    'transport', 'export', 'import', 'replication', 'repair'
]

def classify_by_text(text):
    """Classify node type based on text content"""
    text_lower = text.lower()
    
    # Check for enzymes (highest priority)
    for keyword in ENZYME_KEYWORDS:
        if keyword in text_lower:
            return 'enzyme'
    
    # Check for triggers
    trigger_count = sum(1 for kw in TRIGGER_KEYWORDS if kw in text_lower)
    if trigger_count >= 1:
        return 'trigger'
    
    # Check for processing
    for keyword in PROCESSING_KEYWORDS:
        if keyword in text_lower:
            return 'processing'
    
    return None  # Unknown

def scan_process(json_path):
    """Scan a process file for misclassifications"""
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        mermaid = data.get('mermaid', '')
        process_id = json_path.stem
        
        # Find all styles
        styles = dict(re.findall(r'style (\w+) fill:#([0-9a-fA-F]+)', mermaid))
        
        issues = []
        
        # Check each styled node
        for node_id, color in styles.items():
            # Get node text
            patterns = [
                rf'{node_id}\[([^\]]+)\]',
                rf'{node_id}\{{{{([^}}]+)\}}}}',  # Hexagon
                rf'{node_id}\{{([^}}]+)\}}',      # Diamond
                rf'{node_id}\[\\.([^/]+)/\]',     # Trapezoid
            ]
            
            node_text = None
            for pattern in patterns:
                match = re.search(pattern, mermaid)
                if match:
                    node_text = match.group(1)
                    break
            
            if not node_text:
                continue
            
            # Skip logic gates (they have unique shapes, already correct)
            if color in ['ff9f43', '7950f2', 'e74c3c', '000000']:
                continue
            
            # Classify based on text
            expected_type = classify_by_text(node_text)
            
            if expected_type == 'enzyme' and color != 'fab005':
                issues.append({
                    'node_id': node_id,
                    'text': node_text,
                    'current_color': color,
                    'expected_color': 'fab005',
                    'type': 'enzyme',
                    'severity': 'high'
                })
            elif expected_type == 'trigger' and color not in ['51cf66', 'ff6b6b']:
                # Allow old red triggers too
                if 'signal' in node_text.lower() or 'stress' in node_text.lower():
                    issues.append({
                        'node_id': node_id,
                        'text': node_text,
                        'current_color': color,
                        'expected_color': '51cf66',
                        'type': 'trigger',
                        'severity': 'medium'
                    })
            elif expected_type == 'processing' and color != '74c0fc':
                if 'phosphorylation' in node_text.lower() or 'transcription' in node_text.lower():
                    issues.append({
                        'node_id': node_id,
                        'text': node_text,
                        'current_color': color,
                        'expected_color': '74c0fc',
                        'type': 'processing',
                        'severity': 'low'
                    })
        
        return {
            'process_id': process_id,
            'issues': issues
        }
        
    except Exception as e:
        return {
            'process_id': json_path.stem,
            'error': str(e)
        }

def main():
    """Main execution"""
    
    print("=" * 70)
    print("🔍 SCANNING ALL PROCESSES FOR MISCLASSIFICATIONS")
    print("=" * 70)
    print()
    
    # Find all process files
    gcs_dir = Path('/workspace/gcs-processes')
    json_files = list(gcs_dir.rglob('*.json'))
    
    all_issues = defaultdict(list)
    processes_with_issues = []
    
    print("Scanning...")
    for json_file in sorted(json_files):
        result = scan_process(json_file)
        
        if 'error' in result:
            continue
        
        if result['issues']:
            processes_with_issues.append(result['process_id'])
            for issue in result['issues']:
                all_issues[issue['type']].append({
                    'process': result['process_id'],
                    **issue
                })
    
    print()
    print("=" * 70)
    print("📊 SCAN RESULTS")
    print("=" * 70)
    print()
    
    print(f"Processes scanned: {len(json_files)}")
    print(f"Processes with issues: {len(processes_with_issues)}")
    print()
    
    # Summary by type
    print("Issues by type:")
    for issue_type, issues in sorted(all_issues.items()):
        print(f"  {issue_type:15s}: {len(issues)} issues")
    print()
    
    # Detailed report
    if all_issues:
        print("=" * 70)
        print("🔴 DETAILED ISSUES")
        print("=" * 70)
        print()
        
        # High severity first (enzymes)
        if 'enzyme' in all_issues:
            print(f"HIGH PRIORITY: Enzyme Misclassifications ({len(all_issues['enzyme'])} found)")
            print("-" * 70)
            for issue in all_issues['enzyme'][:20]:  # Show first 20
                print(f"Process: {issue['process']}")
                print(f"  Node {issue['node_id']}: '{issue['text'][:60]}'")
                print(f"  Current:  #{issue['current_color']}")
                print(f"  Expected: #{issue['expected_color']} (amber - enzyme)")
                print()
            
            if len(all_issues['enzyme']) > 20:
                print(f"... and {len(all_issues['enzyme']) - 20} more enzyme issues")
                print()
        
        # Medium severity (triggers)
        if 'trigger' in all_issues:
            print(f"MEDIUM PRIORITY: Trigger Misclassifications ({len(all_issues['trigger'])} found)")
            print("-" * 70)
            for issue in all_issues['trigger'][:10]:  # Show first 10
                print(f"Process: {issue['process']}")
                print(f"  Node {issue['node_id']}: '{issue['text'][:60]}'")
                print(f"  Current:  #{issue['current_color']}")
                print(f"  Expected: #{issue['expected_color']} (green - trigger)")
                print()
            
            if len(all_issues['trigger']) > 10:
                print(f"... and {len(all_issues['trigger']) - 10} more trigger issues")
                print()
        
        # Low severity (processing)
        if 'processing' in all_issues:
            print(f"LOW PRIORITY: Processing Misclassifications ({len(all_issues['processing'])} found)")
            print(f"(Showing first 5 only)")
            print("-" * 70)
            for issue in all_issues['processing'][:5]:
                print(f"Process: {issue['process']}")
                print(f"  Node {issue['node_id']}: '{issue['text'][:60]}'")
                print()
    else:
        print("✅ No obvious misclassifications found!")
    
    # Export to JSON for desktop agent
    if all_issues:
        output = {
            'summary': {
                'total_processes': len(json_files),
                'processes_with_issues': len(processes_with_issues),
                'total_issues': sum(len(issues) for issues in all_issues.values())
            },
            'issues_by_type': {
                issue_type: len(issues) for issue_type, issues in all_issues.items()
            },
            'detailed_issues': dict(all_issues)
        }
        
        with open('/workspace/misclassification_report.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print()
        print("📝 Full report saved to: misclassification_report.json")
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
