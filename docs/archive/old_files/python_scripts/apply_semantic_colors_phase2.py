#!/usr/bin/env python3
"""
Phase 2: Apply Semantic Colors to All Processes
Uses COLOR_BLUEPRINT_COMPLETE.json to update all process files
"""

import json
import os
from glob import glob
from pathlib import Path

# Load the complete blueprint
print("Loading COLOR_BLUEPRINT_COMPLETE.json...")
with open('COLOR_BLUEPRINT_COMPLETE.json', 'r') as f:
    blueprint = json.load(f)

print(f"✓ Blueprint loaded: {len(blueprint)} processes")
print()

# Color scheme with text colors
def get_text_color(fill_color):
    """Return white text for dark backgrounds, black for light"""
    dark_colors = ['#51cf66', '#e74c3c', '#ff9f43', '#7950f2', '#000000']
    return '#fff' if fill_color in dark_colors else '#000'

# Process each file
updated_count = 0
error_count = 0
total_nodes_styled = 0

for process_id, node_classifications in blueprint.items():
    # Find the JSON file
    files = glob(f'gcs-processes/*/{process_id}.json')
    
    if not files:
        print(f"⚠️  Could not find file for: {process_id}")
        error_count += 1
        continue
    
    filepath = files[0]
    
    try:
        # Load process
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        mermaid = data['mermaid']
        lines = mermaid.split('\n')
        
        # Remove old style statements
        non_style_lines = [l for l in lines if not l.strip().startswith('style ')]
        
        # Build new style statements
        new_styles = []
        for node_id, info in node_classifications.items():
            color = info['color']
            text_color = get_text_color(color)
            new_styles.append(f"    style {node_id} fill:{color},color:{text_color}")
        
        # Add styling section
        styled_lines = non_style_lines + ['', '    %% Semantic Color Styling'] + new_styles
        
        # Update mermaid
        data['mermaid'] = '\n'.join(styled_lines)
        
        # Write back
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        updated_count += 1
        total_nodes_styled += len(node_classifications)
        print(f"✓ {process_id}: {len(node_classifications)} nodes styled")
        
    except Exception as e:
        print(f"✗ Error processing {process_id}: {e}")
        error_count += 1

print()
print("=" * 80)
print("PHASE 2 APPLICATION COMPLETE")
print("=" * 80)
print(f"✓ Processes updated: {updated_count}")
print(f"✓ Total nodes styled: {total_nodes_styled}")
print(f"✗ Errors: {error_count}")
print()
print("Next: Deploy to GCS using DEPLOY_PHASE2_COMPLETE.sh")
print("=" * 80)

