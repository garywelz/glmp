#!/usr/bin/env python3
"""
Fix Programming Framework Article - Simple Version
Remove all duplicate color keys and ensure each case study has exactly one correct discipline-specific color key.
"""

import re

def fix_programming_framework_article():
    """Fix the programming framework article by removing duplicate color keys."""
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
    
    # First, remove ALL existing color keys
    print("  Removing all existing color keys...")
    
    # Pattern to match any color key div
    color_key_pattern = r'<div style="display: grid; grid-template-columns: repeat\(auto-fit,minmax\(140px,1fr\)\); gap: \.5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">.*?</div>'
    
    # Remove all color keys
    content = re.sub(color_key_pattern, '', content, flags=re.DOTALL)
    
    # Now add the correct color key for each case study
    print("  Adding correct discipline-specific color keys...")
    
    # 1. β-Galactosidase Analysis (Biology)
    biology_pattern = r'(Case Study: β-Galactosidase Analysis \(2025\)</h3>.*?</div>\s*<div class="figure-caption">)'
    content = re.sub(biology_pattern, r'\1\n        ' + color_keys['biology'] + '\n        ', content, flags=re.DOTALL)
    print("    Added biology color key")
    
    # 2. Algorithm Execution Analysis (Computer Science)
    cs_pattern = r'(Case Study: Algorithm Execution Analysis</h3>.*?</div>\s*<div class="figure-caption">)'
    content = re.sub(cs_pattern, r'\1\n        ' + color_keys['computer_science'] + '\n        ', content, flags=re.DOTALL)
    print("    Added computer science color key")
    
    # 3. Water Electrolysis Analysis (Chemistry)
    chemistry_pattern = r'(Case Study: Water Electrolysis Analysis</h3>.*?</div>\s*<div class="figure-caption">)'
    content = re.sub(chemistry_pattern, r'\1\n        ' + color_keys['chemistry'] + '\n        ', content, flags=re.DOTALL)
    print("    Added chemistry color key")
    
    # 4. Quantum Tunneling Analysis (Physics)
    physics_pattern = r'(Case Study: Quantum Tunneling Analysis</h3>.*?</div>\s*<div class="figure-caption">)'
    content = re.sub(physics_pattern, r'\1\n        ' + color_keys['physics'] + '\n        ', content, flags=re.DOTALL)
    print("    Added physics color key")
    
    # 5. Mathematical Proof Tree Analysis (Mathematics)
    math_pattern = r'(Case Study: Mathematical Proof Tree Analysis</h3>.*?</div>\s*<div class="figure-caption">)'
    content = re.sub(math_pattern, r'\1\n        ' + color_keys['mathematics'] + '\n        ', content, flags=re.DOTALL)
    print("    Added mathematics color key")
    
    # Write the corrected content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed: {file_path}")

if __name__ == "__main__":
    fix_programming_framework_article()




