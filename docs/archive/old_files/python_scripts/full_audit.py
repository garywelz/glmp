#!/usr/bin/env python3
import json, re, urllib.request, time
from collections import defaultdict

def identify_method(mermaid):
    """Identify which method was used."""
    has_shapes = bool(re.search(r'\{[^{]|\{\{|\[/', mermaid))
    has_colors = any(c in mermaid for c in ['#ffd600', '#7950f2', '#e74c3c'])
    has_labels = bool(re.search(r'(OR:|AND:|NOT:)', mermaid, re.I))
    
    methods = []
    if has_shapes: methods.append('shape')
    if has_colors: methods.append('color')
    if has_labels: methods.append('label')
    return '+'.join(methods) if methods else 'none'

def count_gates(mermaid):
    """Count gates using all three methods."""
    # Shape-based
    or_shape = re.findall(r'(\w+)\{[^{]', mermaid)
    and_shape = re.findall(r'(\w+)\{\{', mermaid)
    not_shape = re.findall(r'(\w+)\[/', mermaid)
    
    # Color-based
    or_color, and_color, not_color = [], [], []
    for match in re.findall(r'style\s+(\w+)\s+fill:(#[0-9a-fA-F]{6})', mermaid):
        node, color = match
        if color == '#ffd600': or_color.append(node)
        elif color == '#7950f2': and_color.append(node)
        elif color == '#e74c3c': not_color.append(node)
    
    # Label-based
    or_label = re.findall(r'(\w+)[\[{]+[^}\]]*OR:', mermaid, re.I)
    and_label = re.findall(r'(\w+)[\[{]+[^}\]]*AND:', mermaid, re.I)
    not_label = re.findall(r'(\w+)[\[{]+[^}\]]*NOT:', mermaid, re.I)
    
    return {
        'shape': {'or': len(or_shape), 'and': len(and_shape), 'not': len(not_shape)},
        'color': {'or': len(or_color), 'and': len(and_color), 'not': len(not_color)},
        'label': {'or': len(or_label), 'and': len(and_label), 'not': len(not_label)}
    }

print("🔍 Auditing all 108 processes...")
print()

# Fetch metadata
url = 'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/metadata.json'
with urllib.request.urlopen(url) as r:
    metadata = json.loads(r.read())

processes = metadata['processes']
print(f"Found {len(processes)} processes\n")

results = []
for i, proc in enumerate(processes, 1):
    organism = proc['id'].split('_')[0]
    proc_url = f'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/{organism}/{proc["id"]}.json'
    
    try:
        with urllib.request.urlopen(proc_url) as r:
            proc_data = json.loads(r.read())
        
        mermaid = proc_data.get('mermaid', '')
        method = identify_method(mermaid)
        counts = count_gates(mermaid)
        
        # Get claimed counts
        gates = proc.get('logicGates', {})
        claimed = {'or': gates.get('or', 0), 'and': gates.get('and', 0), 'not': gates.get('not', 0) or 0}
        
        # Determine best matching method
        best_method = 'color'  # Default to color (Phase 2)
        visual = counts['color']
        
        if counts['shape']['or'] == claimed['or'] and counts['shape']['and'] == claimed['and']:
            best_method = 'shape'
            visual = counts['shape']
        elif counts['label']['or'] == claimed['or'] and counts['label']['and'] == claimed['and']:
            best_method = 'label'
            visual = counts['label']
        
        # Check validity
        issues = []
        if visual['or'] != claimed['or']:
            issues.append(f"OR: claimed {claimed['or']}, visual {visual['or']}")
        if visual['and'] != claimed['and']:
            issues.append(f"AND: claimed {claimed['and']}, visual {visual['and']}")
        if visual['not'] != claimed['not']:
            issues.append(f"NOT: claimed {claimed['not']}, visual {visual['not']}")
        
        results.append({
            'id': proc['id'],
            'name': name,
            'method': method,
            'best_match': best_method,
            'valid': len(issues) == 0,
            'issues': issues,
            'claimed': claimed,
            'visual': visual,
            'all_counts': counts
        })
        
        if i % 10 == 0:
            print(f"Processed {i}/{len(processes)}...")
            time.sleep(0.3)
    
    except Exception as e:
        results.append({'id': proc['id'], 'name': proc.get('name'), 'error': str(e)})

print("\n✅ Complete!\n")

# Summary
valid = sum(1 for r in results if r.get('valid', False))
print(f"Valid: {valid}/{len(results)} ({valid/len(results)*100:.1f}%)")
print(f"Invalid: {len(results)-valid}/{len(results)}\n")

# Method breakdown
methods = defaultdict(int)
for r in results:
    methods[r.get('best_match', 'error')] += 1

print("Best Matching Method:")
for m, c in sorted(methods.items(), key=lambda x: -x[1]):
    print(f"  {m}: {c}")

# Save
with open('/workspace/FULL_AUDIT_REPORT.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n📄 Saved to: FULL_AUDIT_REPORT.json")
