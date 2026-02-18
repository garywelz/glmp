#!/usr/bin/env python3
"""
Implement Final Color Scheme - Option 2
Updates all nodes with the new refined colors
"""

import json
from glob import glob

# FINAL COLOR SCHEME
FINAL_COLORS = {
    'trigger': '#51cf66',      # Green (unchanged)
    'enzyme': '#ffa726',        # Amber/Gold (NEW - was #fab005)
    'processing': '#42a5f5',    # Dark Sky Blue (NEW - was #74c0fc)
    'intermediate': '#b3e5fc',  # Light Cyan (NEW - was #ffa07a)
    'product': '#000000',       # Black (unchanged)
    'or_gate': '#ffd600',       # Yellow (NEW - was #ff9f43)
    'and_gate': '#7950f2',      # Purple (unchanged)
    'not_gate': '#e74c3c'       # Red (unchanged)
}

# Color mapping for text contrast
def get_text_color(bg_color):
    """Return white for dark backgrounds, black for light"""
    dark_colors = ['#51cf66', '#ffa726', '#42a5f5', '#ffd600', '#7950f2', '#e74c3c', '#000000']
    light_colors = ['#b3e5fc']
    
    if bg_color in dark_colors:
        return '#fff'
    elif bg_color in light_colors:
        return '#000'
    else:
        # Fallback: check if color is dark
        return '#fff' if bg_color in ['#51cf66', '#42a5f5', '#7950f2', '#e74c3c', '#000000'] else '#000'

print("🎨 IMPLEMENTING FINAL COLOR SCHEME")
print("=" * 80)
print()
print("Changes being applied:")
print(f"  Enzymes:        #fab005 → #ffa726 (Amber/Gold)")
print(f"  Processing:     #74c0fc → #42a5f5 (Darker Blue)")
print(f"  Intermediates:  #ffa07a → #b3e5fc (Light Cyan)")
print(f"  OR Gates:       #ff9f43 → #ffd600 (Yellow)")
print()

# Load the blueprint
print("Loading blueprint...")
with open('COLOR_BLUEPRINT_COMPLETE.json', 'r') as f:
    blueprint = json.load(f)

# Update blueprint colors based on type
updated_blueprint = {}
for process_id, nodes in blueprint.items():
    updated_blueprint[process_id] = {}
    for node_id, info in nodes.items():
        node_type = info['type']
        
        # Map type to new color
        if node_type == 'trigger':
            new_color = FINAL_COLORS['trigger']
        elif node_type == 'enzyme':
            new_color = FINAL_COLORS['enzyme']
        elif node_type == 'processing':
            new_color = FINAL_COLORS['processing']
        elif node_type == 'intermediate':
            new_color = FINAL_COLORS['intermediate']
        elif node_type == 'product':
            new_color = FINAL_COLORS['product']
        elif node_type == 'or_gate':
            new_color = FINAL_COLORS['or_gate']
        elif node_type == 'and_gate':
            new_color = FINAL_COLORS['and_gate']
        elif node_type == 'not_gate':
            new_color = FINAL_COLORS['not_gate']
        else:
            new_color = info['color']  # Fallback
        
        updated_blueprint[process_id][node_id] = {
            'type': node_type,
            'color': new_color,
            'text': info['text'],
            'shape': info['shape']
        }

# Save updated blueprint
print("Saving updated blueprint...")
with open('COLOR_BLUEPRINT_COMPLETE.json', 'w') as f:
    json.dump(updated_blueprint, f, indent=2, ensure_ascii=False)

print("✓ Blueprint updated")
print()

# Apply colors to all process files
print("Applying colors to all 108 processes...")
files = sorted(glob('gcs-processes/*/*.json'))
updated_count = 0

for filepath in files:
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        process_id = data['id']
        
        if process_id not in updated_blueprint:
            print(f"⚠️  {process_id}: not in blueprint, skipping")
            continue
        
        mermaid = data['mermaid']
        lines = mermaid.split('\n')
        
        # Remove old style statements
        non_style_lines = [l for l in lines if not l.strip().startswith('style ')]
        
        # Add new style statements
        new_styles = []
        for node_id, info in updated_blueprint[process_id].items():
            color = info['color']
            text_color = get_text_color(color)
            new_styles.append(f"    style {node_id} fill:{color},color:{text_color}")
        
        # Rebuild mermaid
        data['mermaid'] = '\n'.join(non_style_lines) + '\n\n    %% Semantic Color Styling\n' + '\n'.join(new_styles)
        
        # Write back
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        updated_count += 1
        print(f"✓ {process_id}")
        
    except Exception as e:
        print(f"✗ Error: {filepath}: {e}")

print()
print("=" * 80)
print("✅ FINAL COLORS APPLIED!")
print("=" * 80)
print(f"Processes updated: {updated_count}")
print()
print("Next step: Run update_color_legends.py to update color scheme metadata")
print("=" * 80)

