#!/usr/bin/env python3
"""Clean audit script for all 108 GLMP processes"""
import json
import re
import urllib.request
import time

def audit_single_process(proc_metadata):
    """Audit one process - returns result dict."""
    proc_id = proc_metadata['id']
    proc_name = proc_metadata['name']
    organism = proc_id.split('_')[0]
    
    # Fetch individual process JSON
    url = f'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/{organism}/{proc_id}.json'
    
    try:
        with urllib.request.urlopen(url) as response:
            process_file = json.loads(response.read())
    except Exception as e:
        return {'id': proc_id, 'name': proc_name, 'error': f'Fetch failed: {e}'}
    
    mermaid = process_file.get('mermaid', '')
    
    # Count gates using all three methods
    # Shape-based: {...}, {{...}}, [/.../]
    shape_or = len(re.findall(r'\w+\{[^{]', mermaid))
    shape_and = len(re.findall(r'\w+\{\{', mermaid))
    shape_not = len(re.findall(r'\w+\[/', mermaid))
    
    # Color-based: style statements
    color_or = len(re.findall(r'style\s+\w+\s+fill:#ffd600', mermaid))
    color_and = len(re.findall(r'style\s+\w+\s+fill:#7950f2', mermaid))
    color_not = len(re.findall(r'style\s+\w+\s+fill:#e74c3c', mermaid))
    
    # Label-based: "OR:", "AND:", "NOT:" in text
    label_or = len(re.findall(r'OR:', mermaid, re.IGNORECASE))
    label_and = len(re.findall(r'AND:', mermaid, re.IGNORECASE))
    label_not = len(re.findall(r'NOT:|Repressor|Inhibit', mermaid, re.IGNORECASE))
    
    # Get metadata claims
    claimed_gates = proc_metadata.get('logicGates', {})
    claimed_or = claimed_gates.get('or', 0)
    claimed_and = claimed_gates.get('and', 0)
    claimed_not = claimed_gates.get('not', 0) or 0
    
    # Determine which method matches best
    method_used = 'unknown'
    visual_counts = {'or': 0, 'and': 0, 'not': 0}
    
    if color_or == claimed_or and color_and == claimed_and:
        method_used = 'color-based'
        visual_counts = {'or': color_or, 'and': color_and, 'not': color_not}
    elif shape_or == claimed_or and shape_and == claimed_and:
        method_used = 'shape-based'
        visual_counts = {'or': shape_or, 'and': shape_and, 'not': shape_not}
    elif label_or == claimed_or and label_and == claimed_and:
        method_used = 'label-based'
        visual_counts = {'or': label_or, 'and': label_and, 'not': label_not}
    else:
        # Default to color (Phase 2 standard)
        method_used = 'color-mismatch'
        visual_counts = {'or': color_or, 'and': color_and, 'not': color_not}
    
    # Check if valid
    is_valid = (visual_counts['or'] == claimed_or and 
                visual_counts['and'] == claimed_and and
                visual_counts['not'] == claimed_not)
    
    return {
        'id': proc_id,
        'name': proc_name,
        'organism': proc_metadata.get('organism'),
        'method': method_used,
        'valid': is_valid,
        'claimed': {'or': claimed_or, 'and': claimed_and, 'not': claimed_not},
        'visual': visual_counts,
        'all_methods': {
            'shape': {'or': shape_or, 'and': shape_and, 'not': shape_not},
            'color': {'or': color_or, 'and': color_and, 'not': color_not},
            'label': {'or': label_or, 'and': label_and, 'not': label_not}
        }
    }

# Main execution
if __name__ == '__main__':
    print("🔍 COMPREHENSIVE AUDIT: All 108 GLMP Processes")
    print("=" * 80)
    print()
    
    # Fetch metadata
    metadata_url = 'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/metadata.json'
    print("Fetching metadata...")
    with urllib.request.urlopen(metadata_url) as response:
        metadata = json.loads(response.read())
    
    all_processes = metadata['processes']
    print(f"Found {len(all_processes)} processes\n")
    print("Auditing each process (this takes ~2 minutes)...\n")
    
    audit_results = []
    for i, proc in enumerate(all_processes, 1):
        result = audit_single_process(proc)
        audit_results.append(result)
        
        if i % 10 == 0:
            print(f"  Progress: {i}/{len(all_processes)}...")
            time.sleep(0.2)
    
    print("\n✅ Audit Complete!\n")
    
    # Save full results
    with open('/workspace/FULL_AUDIT_RESULTS.json', 'w') as f:
        json.dump(audit_results, f, indent=2)
    
    # Generate summary
    valid_count = sum(1 for r in audit_results if r.get('valid', False))
    invalid_count = len(audit_results) - valid_count
    errors = sum(1 for r in audit_results if 'error' in r)
    
    print("=" * 80)
    print("📊 AUDIT SUMMARY")
    print("=" * 80)
    print()
    print(f"Total Processes: {len(audit_results)}")
    print(f"✅ Valid: {valid_count} ({valid_count/len(audit_results)*100:.1f}%)")
    print(f"❌ Invalid: {invalid_count} ({invalid_count/len(audit_results)*100:.1f}%)")
    print(f"⚠️  Errors: {errors}")
    print()
    
    # Method breakdown
    from collections import Counter
    methods_counter = Counter(r.get('method', 'unknown') for r in audit_results if 'error' not in r)
    
    print("Methods Used:")
    for method, count in methods_counter.most_common():
        print(f"  {method}: {count} processes")
    print()
    
    # Show sample discrepancies
    invalid_samples = [r for r in audit_results if not r.get('valid', False) and 'error' not in r]
    
    if invalid_samples:
        print("=" * 80)
        print(f"SAMPLE DISCREPANCIES (First 10 of {len(invalid_samples)}):")
        print("=" * 80)
        print()
        
        for r in invalid_samples[:10]:
            print(f"📋 {r['name']}")
            print(f"   ID: {r['id']}")
            print(f"   Method: {r['method']}")
            print(f"   Claimed: OR={r['claimed']['or']}, AND={r['claimed']['and']}, NOT={r['claimed']['not']}")
            print(f"   Visual:  OR={r['visual']['or']}, AND={r['visual']['and']}, NOT={r['visual']['not']}")
            print(f"   Shape:   OR={r['all_methods']['shape']['or']}, AND={r['all_methods']['shape']['and']}, NOT={r['all_methods']['shape']['not']}")
            print(f"   Color:   OR={r['all_methods']['color']['or']}, AND={r['all_methods']['color']['and']}, NOT={r['all_methods']['color']['not']}")
            print(f"   Label:   OR={r['all_methods']['label']['or']}, AND={r['all_methods']['label']['and']}, NOT={r['all_methods']['label']['not']}")
            print()
    
    print(f"📄 Full detailed results saved to: FULL_AUDIT_RESULTS.json")
