#!/usr/bin/env python3
"""
Fix color rendering in GLMP processes by:
1. Adding ,color:#fff or ,color:#000 to all style statements
2. Ensuring every node has a style statement
"""

import json
import re
import sys
from pathlib import Path

# Color map: fill color -> text color
COLOR_TEXT_MAP = {
    '#ff6b6b': '#fff',  # Red (inputs)
    '#ffd43b': '#000',  # Yellow (structures) - black text for contrast
    '#51cf66': '#fff',  # Green (processing)
    '#74c0fc': '#fff',  # Blue (intermediates)
    '#ff9f43': '#fff',  # Orange (OR gates)
    '#b4b4dc': '#fff',  # Lavender (AND gates)
    '#9775fa': '#fff',  # Violet (outputs)
    '#b197fc': '#fff',  # Purple variant
}

def fix_process_colors(json_path):
    """Fix colors in a single process JSON file"""
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    mermaid = data['mermaid']
    lines = mermaid.split('\n')
    
    # Track changes
    fixed_lines = []
    style_updates = 0
    
    for line in lines:
        # Check if this is a style statement
        match = re.match(r'(\s*)style\s+(\w+)\s+fill:(#[0-9a-f]+)(.*)', line, re.IGNORECASE)
        
        if match:
            indent = match.group(1)
            node_id = match.group(2)
            fill_color = match.group(3)
            rest = match.group(4)
            
            # Check if it already has a text color
            if ',color:' in rest.lower():
                # Already has color, keep as is
                fixed_lines.append(line)
            else:
                # Add appropriate text color
                text_color = COLOR_TEXT_MAP.get(fill_color.lower(), '#fff')
                fixed_line = f"{indent}style {node_id} fill:{fill_color},color:{text_color}"
                fixed_lines.append(fixed_line)
                style_updates += 1
        else:
            fixed_lines.append(line)
    
    # Update mermaid
    data['mermaid'] = '\n'.join(fixed_lines)
    
    # Write back
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return style_updates

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fix_process_colors.py <process_json_path>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    
    if not Path(json_path).exists():
        print(f"❌ File not found: {json_path}")
        sys.exit(1)
    
    print(f"🔧 Fixing colors in: {json_path}")
    updates = fix_process_colors(json_path)
    print(f"✅ Updated {updates} style statements")

if __name__ == '__main__':
    main()
