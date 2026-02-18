#!/usr/bin/env python3
"""
Universal Color Scheme Update Script
Updates all HTML files in the GLMP project with the standardized color scheme.

Universal Color Scheme:
- Red (#ff6b6b) - Triggers/Inputs (white text)
- Yellow (#ffd43b) - Structures/Objects (black text)
- Green (#51cf66) - Processing/Operations (white text)
- Light Blue (#74c0fc) - Intermediates/States (white text)
- Light Violet (#b197fc) - Products/Outputs (white text)
"""

import os
import re
import glob
from pathlib import Path

# Universal Color Scheme Mapping
COLOR_MAPPINGS = {
    # Old colors to new colors with text colors
    '#ff6b6b': '#ff6b6b,color:#fff',  # Red stays red, add white text
    '#fd7e14': '#ffd43b,color:#000',  # Orange -> Yellow with black text
    '#ffd43b': '#ffd43b,color:#000',  # Yellow stays yellow, add black text
    '#20c997': '#51cf66,color:#fff',  # Teal -> Green with white text
    '#51cf66': '#51cf66,color:#fff',  # Green stays green, add white text
    '#4dabf7': '#74c0fc,color:#fff',  # Blue -> Light Blue with white text
    '#8b5cf6': '#b197fc,color:#fff',  # Violet -> Light Violet with white text
    '#4ecdc4': '#ffd43b,color:#000',  # Teal -> Yellow with black text
    '#45b7d1': '#74c0fc,color:#fff',  # Blue -> Light Blue with white text
    '#96ceb4': '#b197fc,color:#fff',  # Green -> Light Violet with white text
    '#feca57': '#ffd43b,color:#000',  # Yellow -> Yellow with black text
}

# Color key template for different disciplines
COLOR_KEYS = {
    'physics': [
        ('Triggers & Conditions', '#ff6b6b'),
        ('Wave Functions & Fields', '#ffd43b'),
        ('Quantum Processing', '#51cf66'),
        ('Intermediates', '#74c0fc'),
        ('Products', '#b197fc')
    ],
    'mathematics': [
        ('Axioms & Given Conditions', '#ff6b6b'),
        ('Logical Structures & Hypotheses', '#ffd43b'),
        ('Deductions & Theorem Applications', '#51cf66'),
        ('Intermediates', '#74c0fc'),
        ('Products', '#b197fc')
    ],
    'computer_science': [
        ('Input Data & Parameters', '#ff6b6b'),
        ('Data Structures & Arrays', '#ffd43b'),
        ('Operations & Algorithms', '#51cf66'),
        ('States & Variables', '#74c0fc'),
        ('Output & Results', '#b197fc')
    ],
    'human_chemical': [
        ('Triggers & Conditions', '#ff6b6b'),
        ('Catalysts & Enzymes', '#ffd43b'),
        ('Chemical Processing', '#51cf66'),
        ('Intermediates', '#74c0fc'),
        ('Products', '#b197fc')
    ],
    'human_disease': [
        ('Disease Triggers', '#ff6b6b'),
        ('Pathological Structures', '#ffd43b'),
        ('Disease Processes', '#51cf66'),
        ('Intermediates', '#74c0fc'),
        ('Disease Outcomes', '#b197fc')
    ],
    'chemistry': [
        ('Triggers & Conditions', '#ff6b6b'),
        ('Catalysts & Enzymes', '#ffd43b'),
        ('Chemical Processing', '#51cf66'),
        ('Intermediates', '#74c0fc'),
        ('Products', '#b197fc')
    ]
}

def generate_color_key(discipline):
    """Generate HTML color key for a specific discipline."""
    if discipline not in COLOR_KEYS:
        discipline = 'physics'  # Default fallback
    
    key_html = '<div style="display: grid; grid-template-columns: repeat(auto-fit,minmax(140px,1fr)); gap: .5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">'
    
    for label, color in COLOR_KEYS[discipline]:
        key_html += f'''
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:{color};"></span>{label}
        </div>'''
    
    key_html += '</div>'
    return key_html

def update_introduction_paragraph(content, discipline):
    """Update the introduction paragraph with universal color scheme."""
    new_intro = f"""    <p>This document presents {discipline.replace('_', ' ')} processes analyzed using the Programming Framework methodology. Each process is represented as a computational flowchart with standardized color coding: Red for triggers/inputs, Yellow for structures/objects, Green for processing/operations, Blue for intermediates/states, and Violet for products/outputs. Yellow nodes use black text for optimal readability, while all other colors use white text.</p>"""
    
    # Find and replace the introduction paragraph
    pattern = r'<p>This document presents.*?</p>'
    return re.sub(pattern, new_intro, content, flags=re.DOTALL)

def update_style_statements(content):
    """Update all style statements with universal color scheme."""
    # First, check if the file has already been processed with the universal scheme
    # Look for the presence of the new color format with text colors
    if 'fill:#ff6b6b,color:#fff' in content and 'fill:#ffd43b,color:#000' in content:
        print(f"  ⚠️  File appears to already have universal color scheme - skipping style updates")
        return content
    
    for old_color, new_color in COLOR_MAPPINGS.items():
        # Only update style statements that don't already have color:text
        # This prevents double-processing of already-corrected statements
        pattern = rf'style\s+(\w+)\s+fill:{re.escape(old_color)}(?!,color:)'
        replacement = rf'style \1 fill:{new_color}'
        content = re.sub(pattern, replacement, content)
    
    return content

def add_color_key_to_flowchart(content, discipline):
    """Add color key before each figure caption."""
    color_key = generate_color_key(discipline)
    
    # Check if color key already exists in the content
    if color_key in content:
        print(f"  ⚠️  Color key already exists - skipping color key addition")
        return content
    
    # Find figure captions and add color key before them
    pattern = r'(<div class="figure-caption">)'
    replacement = rf'{color_key}\n      \1'
    content = re.sub(pattern, replacement, content)
    
    return content

def update_captions(content):
    """Remove color information from captions since color keys are now provided."""
    # Remove color descriptions from captions since color keys are now present
    color_patterns = [
        r'\s*\(red\)', r'\s*\(yellow\)', r'\s*\(green\)', r'\s*\(blue\)', r'\s*\(violet\)',
        r'\s*\(orange\)', r'\s*\(teal\)', r'\s*\(light blue\)', r'\s*\(light violet\)',
        r'\s*\(triggers/inputs\)', r'\s*\(structures/objects\)', r'\s*\(processing/operations\)',
        r'\s*\(intermediates/states\)', r'\s*\(products/outputs\)',
        r'\s*\(wave functions and fields\)', r'\s*\(quantum processing\)',
        r'\s*\(axioms and given conditions\)', r'\s*\(logical structures and hypotheses\)',
        r'\s*\(deductions and theorem applications\)', r'\s*\(input data and parameters\)',
        r'\s*\(data structures and arrays\)', r'\s*\(operations and algorithms\)',
        r'\s*\(states and variables\)', r'\s*\(output and results\)',
        r'\s*\(catalysts and enzymes\)', r'\s*\(chemical processing\)',
        r'\s*\(disease triggers\)', r'\s*\(pathological structures\)',
        r'\s*\(disease processes\)', r'\s*\(disease outcomes\)'
    ]
    
    for pattern in color_patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    # Clean up any double spaces or punctuation issues
    content = re.sub(r'\s+', ' ', content)
    content = re.sub(r'\s*,\s*,\s*', ', ', content)
    content = re.sub(r'\s*\.\s*\.\s*', '. ', content)
    
    return content

def process_html_file(file_path):
    """Process a single HTML file with universal color scheme."""
    print(f"Processing: {file_path}")
    
    # Read file content first to check if already processed
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has already been processed with universal color scheme
    if 'fill:#ff6b6b,color:#fff' in content and 'fill:#ffd43b,color:#000' in content:
        print(f"  ⏭️  File already has universal color scheme - skipping")
        return
    
    # Determine discipline from filename
    filename = Path(file_path).stem
    discipline = 'physics'  # Default
    
    if 'physics' in filename:
        discipline = 'physics'
    elif 'mathematics' in filename or 'math' in filename:
        discipline = 'mathematics'
    elif 'computer' in filename or 'cs' in filename:
        discipline = 'computer_science'
    elif 'human_chemical' in filename:
        discipline = 'human_chemical'
    elif 'human_disease' in filename or 'disease' in filename:
        discipline = 'human_disease'
    elif 'chemistry' in filename:
        discipline = 'chemistry'
    
    # Apply updates
    content = update_introduction_paragraph(content, discipline)
    content = update_style_statements(content)
    content = add_color_key_to_flowchart(content, discipline)
    content = update_captions(content)
    
    # Write updated content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated: {file_path}")

def main():
    """Main function to process all HTML files."""
    print("🎨 Universal Color Scheme Update Script")
    print("=" * 50)
    
    # Find all HTML files in the current directory and subdirectories
    html_files = glob.glob("*.html") + glob.glob("*/*.html") + glob.glob("*/*/*.html")
    
    # Filter out any files we don't want to update
    exclude_patterns = ['index.html', 'README.html', 'template.html']
    html_files = [f for f in html_files if not any(pattern in f for pattern in exclude_patterns)]
    
    print(f"Found {len(html_files)} HTML files to process")
    
    # Process each file
    for file_path in html_files:
        try:
            process_html_file(file_path)
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    print("\n🎉 Color scheme update complete!")
    print(f"Processed {len(html_files)} files")

if __name__ == "__main__":
    main()
