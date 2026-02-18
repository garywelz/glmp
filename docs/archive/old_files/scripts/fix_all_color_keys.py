#!/usr/bin/env python3
"""
Fix All Color Keys in Programming Framework Article
Comprehensive fix for all incorrect color keys in the programming_framework_article.html file.
"""

import re

def fix_all_color_keys():
    """Fix all incorrect color keys in the programming_framework_article.html file."""
    file_path = "programming_framework_article.html"
    
    print(f"Processing: {file_path}")
    
    # Read file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the correct color keys for each discipline
    correct_color_keys = {
        'biology': '''<div style="display: grid; grid-template-columns: repeat(auto-fit,minmax(140px,1fr)); gap: .5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#ff6b6b;"></span>Triggers & Conditions
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#ffd43b;"></span>Catalysts & Enzymes
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#51cf66;"></span>Chemical Processing
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#74c0fc;"></span>Intermediates
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#b197fc;"></span>Products
        </div></div>''',
        
        'physics': '''<div style="display: grid; grid-template-columns: repeat(auto-fit,minmax(140px,1fr)); gap: .5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#ff6b6b;"></span>Triggers & Conditions
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#ffd43b;"></span>Wave Functions & Fields
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#51cf66;"></span>Quantum Processing
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#74c0fc;"></span>Intermediates
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#b197fc;"></span>Products
        </div></div>'''
    }
    
    # Find all color keys in the file
    color_key_pattern = r'<div style="display: grid; grid-template-columns: repeat\(auto-fit,minmax\(140px,1fr\)\); gap: \.5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">.*?</div>'
    
    all_color_keys = re.findall(color_key_pattern, content, re.DOTALL)
    print(f"Found {len(all_color_keys)} total color keys")
    
    # Check each color key to determine if it's correct
    replacements_made = 0
    
    for i, color_key in enumerate(all_color_keys):
        # Check if this color key contains physics labels (incorrect for most sections)
        if 'Wave Functions & Fields' in color_key and 'Quantum Processing' in color_key:
            # This is a physics color key - check if it should be biology instead
            # Look at the surrounding context to determine the discipline
            
            # Find the position of this color key in the content
            start_pos = content.find(color_key)
            if start_pos != -1:
                # Look at the text before this color key to determine context
                context_start = max(0, start_pos - 1000)
                context = content[context_start:start_pos + len(color_key)]
                
                # Determine discipline based on context
                if any(indicator in context.lower() for indicator in ['beta-galactosidase', 'lac operon', 'gene', 'protein', 'enzyme', 'transcription', 'translation', 'dna', 'rna', 'mrna']):
                    # This should be biology
                    print(f"  Color key {i+1}: Replacing physics with biology color key")
                    content = content.replace(color_key, correct_color_keys['biology'], 1)
                    replacements_made += 1
                elif any(indicator in context.lower() for indicator in ['quantum', 'tunneling', 'wave function', 'particle', 'energy barrier', 'photon', 'electron']):
                    # This should be physics
                    print(f"  Color key {i+1}: Keeping physics color key (correct)")
                else:
                    # Default to biology for biological systems
                    print(f"  Color key {i+1}: Replacing physics with biology color key (default)")
                    content = content.replace(color_key, correct_color_keys['biology'], 1)
                    replacements_made += 1
    
    print(f"Made {replacements_made} replacements")
    
    # Write the corrected content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed: {file_path}")

if __name__ == "__main__":
    fix_all_color_keys()




