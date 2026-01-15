#!/usr/bin/env python3
"""
Fix Programming Framework Article - Final Version
Replace incorrect color keys with discipline-specific ones for each case study.
"""

import re

def fix_programming_framework_article():
    """Fix the programming framework article with correct discipline-specific color keys."""
    file_path = "programming_framework_article.html"
    
    print(f"Processing: {file_path}")
    
    # Read file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the correct color keys for each discipline
    color_keys = {
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
        
        'computer_science': '''<div style="display: grid; grid-template-columns: repeat(auto-fit,minmax(140px,1fr)); gap: .5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#ff6b6b;"></span>Inputs & Data
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#ffd43b;"></span>Algorithms & Functions
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#51cf66;"></span>Processing Steps
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#74c0fc;"></span>Intermediate States
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#b197fc;"></span>Outputs & Results
        </div></div>''',
        
        'chemistry': '''<div style="display: grid; grid-template-columns: repeat(auto-fit,minmax(140px,1fr)); gap: .5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#ff6b6b;"></span>Reactants & Conditions
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#ffd43b;"></span>Catalysts & Enzymes
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#51cf66;"></span>Chemical Reactions
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
        </div></div>''',
        
        'mathematics': '''<div style="display: grid; grid-template-columns: repeat(auto-fit,minmax(140px,1fr)); gap: .5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#ff6b6b;"></span>Axioms & Assumptions
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#ffd43b;"></span>Theorems & Methods
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#51cf66;"></span>Logical Steps
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#74c0fc;"></span>Intermediate Results
        </div>
        <div style="display:inline-flex; align-items:center; gap:.5rem; padding:.25rem .5rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background:#fff;">
          <span style="width: 12px; height: 12px; border-radius: 2px; border:1px solid rgba(0,0,0,.15); background:#b197fc;"></span>Conclusions
        </div></div>'''
    }
    
    # Find and replace color keys for each case study section
    replacements_made = 0
    
    # 1. β-Galactosidase Analysis (Biology)
    biology_pattern = r'(Case Study: β-Galactosidase Analysis \(2025\)</h3>.*?)(<div style="display: grid; grid-template-columns: repeat\(auto-fit,minmax\(140px,1fr\)\); gap: \.5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">.*?</div>)'
    content, count = re.subn(biology_pattern, r'\1' + color_keys['biology'], content, flags=re.DOTALL)
    replacements_made += count
    print(f"  Biology section: {count} replacements")
    
    # 2. Algorithm Execution Analysis (Computer Science)
    cs_pattern = r'(Case Study: Algorithm Execution Analysis</h3>.*?)(<div style="display: grid; grid-template-columns: repeat\(auto-fit,minmax\(140px,1fr\)\); gap: \.5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">.*?</div>)'
    content, count = re.subn(cs_pattern, r'\1' + color_keys['computer_science'], content, flags=re.DOTALL)
    replacements_made += count
    print(f"  Computer Science section: {count} replacements")
    
    # 3. Water Electrolysis Analysis (Chemistry)
    chemistry_pattern = r'(Case Study: Water Electrolysis Analysis</h3>.*?)(<div style="display: grid; grid-template-columns: repeat\(auto-fit,minmax\(140px,1fr\)\); gap: \.5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">.*?</div>)'
    content, count = re.subn(chemistry_pattern, r'\1' + color_keys['chemistry'], content, flags=re.DOTALL)
    replacements_made += count
    print(f"  Chemistry section: {count} replacements")
    
    # 4. Quantum Tunneling Analysis (Physics) - This one should keep physics keys
    physics_pattern = r'(Case Study: Quantum Tunneling Analysis</h3>.*?)(<div style="display: grid; grid-template-columns: repeat\(auto-fit,minmax\(140px,1fr\)\); gap: \.5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">.*?</div>)'
    content, count = re.subn(physics_pattern, r'\1' + color_keys['physics'], content, flags=re.DOTALL)
    replacements_made += count
    print(f"  Physics section: {count} replacements")
    
    # 5. Mathematical Proof Tree Analysis (Mathematics)
    math_pattern = r'(Case Study: Mathematical Proof Tree Analysis</h3>.*?)(<div style="display: grid; grid-template-columns: repeat\(auto-fit,minmax\(140px,1fr\)\); gap: \.5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">.*?</div>)'
    content, count = re.subn(math_pattern, r'\1' + color_keys['mathematics'], content, flags=re.DOTALL)
    replacements_made += count
    print(f"  Mathematics section: {count} replacements")
    
    print(f"Total replacements made: {replacements_made}")
    
    # Write the corrected content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed: {file_path}")

if __name__ == "__main__":
    fix_programming_framework_article()




