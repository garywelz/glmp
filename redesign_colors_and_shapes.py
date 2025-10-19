#!/usr/bin/env python3
"""
Complete GLMP Color & Shape Redesign Script
============================================
Updates all 108 processes with:
- New color scheme (Option C: Green triggers, black outputs, purple AND gates)
- Shape differentiation (OR=diamond, AND=hexagon, NOT=inverted trapezoid)
- Proper text colors for contrast
- Light salmon intermediates distinct from orange

Author: GLMP Project
Date: 2025-01-16
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# ============================================================================
# COLOR SCHEME DEFINITIONS
# ============================================================================

NEW_COLORS = {
    'triggers': {
        'fill': '#51cf66',   # Bright green (GO!)
        'text': '#fff'
    },
    'enzymes': {
        'fill': '#fab005',   # Amber/gold (TRANSFORM)
        'text': '#000'       # Black text on yellow
    },
    'processing': {
        'fill': '#74c0fc',   # Sky blue (WORKFLOW)
        'text': '#fff'
    },
    'intermediates': {
        'fill': '#ffa07a',   # Light salmon (TRANSIENT)
        'text': '#000'       # Black text on light salmon
    },
    'or_gates': {
        'fill': '#ff9f43',   # Orange (ALTERNATIVES)
        'text': '#fff'
    },
    'and_gates': {
        'fill': '#7950f2',   # Deep purple (INTEGRATION)
        'text': '#fff'
    },
    'not_gates': {
        'fill': '#e74c3c',   # Crimson red (BLOCKING)
        'text': '#fff'
    },
    'products': {
        'fill': '#000000',   # True black (FINAL)
        'text': '#fff'
    }
}

# Old color to new color mapping
COLOR_REPLACEMENTS = {
    '#ff6b6b': '#51cf66',  # Triggers: red → bright green
    '#ffd43b': '#fab005',  # Enzymes: yellow → amber
    '#51cf66': '#74c0fc',  # Processing: green → sky blue
    '#74c0fc': '#ffa07a',  # Intermediates: blue → light salmon (if needed)
    '#b4b4dc': '#7950f2',  # AND gates: lavender → deep purple
    '#9775fa': '#000000',  # Products: violet → true black
    '#b197fc': '#000000',  # Products alt: violet → true black
}

# Keywords to identify NOT gates
NOT_GATE_KEYWORDS = [
    'repressor', 'repressed', 'repression', 'repress',
    'blocked', 'blocks', 'blocking', 'block',
    'inhibit', 'inhibited', 'inhibition', 'inhibits',
    'prevent', 'prevents', 'prevented', 'preventing',
    'suppress', 'suppressed', 'suppression',
    'inactive', 'inactivate', 'inactivated',
    'not:', 'not ', '¬', 'NOT:'
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def identify_node_type(node_text: str, is_diamond: bool, style_color: str) -> str:
    """Identify what type of node this is based on text and styling"""
    
    node_lower = node_text.lower()
    
    # Check for logic gates by shape and color
    if is_diamond:
        if style_color in ['#ff9f43']:  # Orange
            return 'or_gate'
        elif style_color in ['#b4b4dc', '#9775fa', '#7950f2']:  # Purple variants
            return 'and_gate'
        # Check for NOT gates - only if diamond AND has NOT keywords
        elif any(keyword in node_lower for keyword in NOT_GATE_KEYWORDS):
            return 'not_gate'
    
    # Check for other node types by current color
    if style_color in ['#ff6b6b']:
        return 'trigger'
    elif style_color in ['#ffd43b', '#fab005']:
        return 'enzyme'
    elif style_color in ['#51cf66']:
        return 'processing'
    elif style_color in ['#74c0fc', '#ffa07a']:
        return 'intermediate'
    elif style_color in ['#9775fa', '#b197fc', '#000000']:
        return 'product'
    
    return 'unknown'

def extract_node_definitions(mermaid: str) -> Dict[str, Tuple[str, bool]]:
    """Extract all node IDs and their definitions, noting if they're diamonds"""
    nodes = {}
    
    # Match node definitions: A[Text] or A{Text?}
    # Rectangles: A[Text]
    rect_pattern = r'(\w+)\[([^\]]+)\]'
    for match in re.finditer(rect_pattern, mermaid):
        node_id = match.group(1)
        node_text = match.group(2)
        nodes[node_id] = (node_text, False)  # Not a diamond
    
    # Diamonds: A{Text?}
    diamond_pattern = r'(\w+)\{([^}]+)\}'
    for match in re.finditer(diamond_pattern, mermaid):
        node_id = match.group(1)
        node_text = match.group(2)
        nodes[node_id] = (node_text, True)  # Is a diamond
    
    return nodes

def extract_style_info(mermaid: str) -> Dict[str, str]:
    """Extract style information for each node"""
    styles = {}
    
    # Match: style A fill:#abc123,color:#fff
    style_pattern = r'style\s+(\w+)\s+fill:(#[0-9a-fA-F]{6})(?:,color:(#[0-9a-fA-F]{3,6}))?'
    
    for match in re.finditer(style_pattern, mermaid):
        node_id = match.group(1)
        fill_color = match.group(2).lower()
        styles[node_id] = fill_color
    
    return styles

def update_colors_in_styles(mermaid: str) -> str:
    """Update all color values in style statements"""
    
    # Replace fill colors
    for old_color, new_color in COLOR_REPLACEMENTS.items():
        mermaid = re.sub(
            f'fill:{old_color}',
            f'fill:{new_color}',
            mermaid,
            flags=re.IGNORECASE
        )
    
    return mermaid

def ensure_text_colors(mermaid: str) -> str:
    """Ensure all style statements have proper text colors"""
    
    # Find styles without text color and add appropriate one
    lines = mermaid.split('\n')
    updated_lines = []
    
    for line in lines:
        if line.strip().startswith('style ') and ',color:' not in line:
            # Extract fill color to determine text color
            fill_match = re.search(r'fill:(#[0-9a-fA-F]{6})', line)
            if fill_match:
                fill_color = fill_match.group(1).lower()
                
                # Determine text color based on fill
                if fill_color in ['#fab005', '#ffa07a']:  # Amber, salmon (light colors)
                    text_color = '#000'
                else:
                    text_color = '#fff'
                
                # Add text color
                line = line.rstrip() + f',color:{text_color}'
        
        updated_lines.append(line)
    
    return '\n'.join(updated_lines)

def convert_and_gates_to_hexagons(mermaid: str, node_definitions: Dict, style_info: Dict) -> str:
    """Convert AND gate diamonds to hexagons"""
    
    for node_id, (node_text, is_diamond) in node_definitions.items():
        if not is_diamond:
            continue
        
        fill_color = style_info.get(node_id, '')
        node_type = identify_node_type(node_text, True, fill_color)
        
        if node_type == 'and_gate':
            # Convert {Text} to {{Text}} for hexagon
            # Be careful not to double-convert
            pattern = rf'{node_id}\{{([^}}]+)\}}'
            replacement = rf'{node_id}{{\1}}'
            mermaid = re.sub(pattern, replacement, mermaid)
            
            print(f"  → Converted AND gate {node_id} to hexagon")
    
    return mermaid

def convert_not_gates_to_trapezoids(mermaid: str, node_definitions: Dict, style_info: Dict) -> str:
    """Convert NOT gate nodes to inverted trapezoids and add red styling"""
    
    not_gates_found = []
    
    for node_id, (node_text, is_diamond) in node_definitions.items():
        fill_color = style_info.get(node_id, '')
        node_type = identify_node_type(node_text, is_diamond, fill_color)
        
        if node_type == 'not_gate':
            not_gates_found.append(node_id)
            
            # Convert shape: A[Text] or A{Text} to A[\Text/]
            # Use string replacement instead of regex to avoid backslash issues
            cleaned_text = node_text.strip()
            
            # Try rectangle pattern first
            old_rect = f'{node_id}[{node_text}]'
            new_trap = f'{node_id}[\\{cleaned_text}/]'
            if old_rect in mermaid:
                mermaid = mermaid.replace(old_rect, new_trap)
            
            # Try diamond pattern
            old_diamond = f'{node_id}{{{node_text}}}'
            if old_diamond in mermaid:
                mermaid = mermaid.replace(old_diamond, new_trap)
            
            # Add or update style for NOT gate
            if f'style {node_id}' in mermaid:
                # Update existing style
                mermaid = re.sub(
                    rf'style {node_id}[^\n]+',
                    f'style {node_id} fill:#e74c3c,color:#fff',
                    mermaid
                )
            else:
                # Add new style at the end of styles section
                style_section_end = mermaid.rfind('style ')
                if style_section_end != -1:
                    # Find end of last style line
                    next_newline = mermaid.find('\n', style_section_end)
                    insert_pos = next_newline if next_newline != -1 else len(mermaid)
                    mermaid = (mermaid[:insert_pos] + 
                             f'\n    style {node_id} fill:#e74c3c,color:#fff' + 
                             mermaid[insert_pos:])
            
            print(f"  → Converted NOT gate {node_id} to trapezoid (red)")
    
    if not_gates_found:
        print(f"  ✓ Found {len(not_gates_found)} NOT gates: {', '.join(not_gates_found)}")
    
    return mermaid

def update_process_file(json_path: Path) -> Tuple[bool, str]:
    """Update a single process JSON file with new colors and shapes"""
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'mermaid' not in data:
            return False, "No mermaid field"
        
        original_mermaid = data['mermaid']
        mermaid = original_mermaid
        
        # Step 1: Extract node information
        node_definitions = extract_node_definitions(mermaid)
        style_info = extract_style_info(mermaid)
        
        # Step 2: Update colors
        mermaid = update_colors_in_styles(mermaid)
        
        # Step 3: Ensure text colors
        mermaid = ensure_text_colors(mermaid)
        
        # Step 4: Convert AND gates to hexagons
        mermaid = convert_and_gates_to_hexagons(mermaid, node_definitions, style_info)
        
        # Step 5: Convert NOT gates to trapezoids
        mermaid = convert_not_gates_to_trapezoids(mermaid, node_definitions, style_info)
        
        # Update data
        data['mermaid'] = mermaid
        
        # Write back
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        changes = len(mermaid) != len(original_mermaid)
        return True, "Updated" if changes else "No changes"
        
    except json.JSONDecodeError as e:
        return False, f"JSON error: {e}"
    except Exception as e:
        return False, f"Error: {e}"

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    
    print("=" * 70)
    print("🎨 GLMP COLOR & SHAPE REDESIGN")
    print("=" * 70)
    print()
    print("New Color Scheme (Option C):")
    print("  🟢 Bright Green (#51cf66)    = Triggers & Inputs")
    print("  🟡 Amber/Gold (#fab005)      = Enzymes & Catalysts")
    print("  🔵 Sky Blue (#74c0fc)        = Processing")
    print("  🟧 Light Salmon (#ffa07a)    = Intermediates")
    print("  🟠 Orange (#ff9f43)          = OR Gates (diamond ◆)")
    print("  🟣 Deep Purple (#7950f2)     = AND Gates (hexagon ⬡)")
    print("  🔴 Crimson Red (#e74c3c)     = NOT Gates (trapezoid ⏷)")
    print("  ⬛ True Black (#000000)       = Products & Outputs")
    print()
    print("=" * 70)
    print()
    
    # Find all process files
    gcs_processes = Path('/workspace/gcs-processes')
    
    if not gcs_processes.exists():
        print(f"❌ Directory not found: {gcs_processes}")
        sys.exit(1)
    
    json_files = list(gcs_processes.rglob('*.json'))
    
    if not json_files:
        print(f"❌ No JSON files found in {gcs_processes}")
        sys.exit(1)
    
    print(f"Found {len(json_files)} process files to update")
    print()
    
    # Process each file
    updated = 0
    failed = 0
    skipped = 0
    
    for json_file in sorted(json_files):
        relative_path = json_file.relative_to(gcs_processes)
        print(f"Processing: {relative_path}")
        
        success, message = update_process_file(json_file)
        
        if success:
            if "No changes" in message:
                skipped += 1
                print(f"  ⊘ {message}")
            else:
                updated += 1
                print(f"  ✓ {message}")
        else:
            failed += 1
            print(f"  ✗ {message}")
        
        print()
    
    # Summary
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"  Total files:    {len(json_files)}")
    print(f"  ✓ Updated:      {updated}")
    print(f"  ⊘ No changes:   {skipped}")
    print(f"  ✗ Failed:       {failed}")
    print()
    
    if updated > 0:
        print("🎉 Color and shape redesign complete!")
        print()
        print("Next steps:")
        print("  1. Review changes: git diff gcs-processes/")
        print("  2. Commit: git add gcs-processes/ && git commit -m 'Apply Option C color scheme and gate shapes'")
        print("  3. Deploy: Run deployment script to upload to GCS")
        print()
    else:
        print("⚠️  No files were updated. Check if processes already have new colors.")
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
