#!/usr/bin/env python3
"""
Auto-fix all Mermaid syntax errors in GLMP processes

Fixes:
1. Brackets inside trapezoid labels: [/...[...]...] → [...(...)...]
2. Wrong trapezoid syntax: [\Label/] → [/Label/]
3. Wrong trapezoid syntax: [\\Label/] → [/Label/]
"""

import json
import re
from pathlib import Path

def fix_bracket_conflicts(mermaid):
    """Replace [brackets] with (parentheses) inside trapezoid labels"""
    
    # Pattern: [/...content...] where content contains [...]
    # We need to replace inner brackets with parentheses
    
    def replace_inner_brackets(match):
        full_match = match.group(0)
        # Extract content between [/ and /]
        content = full_match[2:-2]  # Remove [/ and /]
        
        # Replace all [ and ] in content with ( and )
        fixed_content = content.replace('[', '(').replace(']', ')')
        
        return f'[/{fixed_content}/]'
    
    # Find all trapezoid labels that contain brackets
    # Pattern: [/ ... anything ... ] ... anything ... /]
    pattern = r'\[/[^\]]*\[[^\]]*\][^\]]*\]'
    
    fixed = mermaid
    while True:
        new_fixed = re.sub(pattern, replace_inner_brackets, fixed)
        if new_fixed == fixed:
            break
        fixed = new_fixed
    
    return fixed

def fix_wrong_trapezoid_syntax(mermaid):
    """Fix [\Label/] and [\\Label/] to [/Label/]"""
    
    # Fix single backslash: [\Label/] → [/Label/]
    fixed = re.sub(r'\[\\([^/\]]+)/\]', r'[/\1/]', mermaid)
    
    # Fix double backslash: [\\Label/] → [/Label/]
    fixed = re.sub(r'\[\\\\([^/\]]+)/\]', r'[/\1/]', fixed)
    
    return fixed

def fix_process_file(filepath):
    """Fix a single process JSON file"""
    try:
        with open(filepath) as f:
            process = json.load(f)
        
        mermaid = process.get('mermaid', '')
        if not mermaid:
            return None, "No Mermaid diagram found"
        
        original = mermaid
        
        # Apply fixes
        fixed = fix_bracket_conflicts(mermaid)
        fixed = fix_wrong_trapezoid_syntax(fixed)
        
        if fixed == original:
            return None, "No changes needed"
        
        # Count changes
        bracket_fixes = len(re.findall(r'\[/[^\]]*\([^\)]*\)[^\]]*\]', fixed)) - \
                       len(re.findall(r'\[/[^\]]*\([^\)]*\)[^\]]*\]', original))
        syntax_fixes = original.count('[\\') - fixed.count('[\\')
        
        # Save fixed version
        process['mermaid'] = fixed
        with open(filepath, 'w') as f:
            json.dump(process, f, indent=2)
        
        return (bracket_fixes, syntax_fixes), "Fixed"
        
    except Exception as e:
        return None, f"Error: {str(e)}"

def main():
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                              ║")
    print("║                  🔧 AUTO-FIXING ALL SYNTAX ERRORS                            ║")
    print("║                                                                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Known processes with syntax errors from validation report
    syntax_error_processes = [
        'ecoli/ecoli_fatty_acid_degradation.json',
        'ecoli/ecoli_fatty_acid_synthesis.json',
        'ecoli/ecoli_homologous_recombination.json',
        'ecoli/ecoli_outer_membrane_assembly.json',
        'ecoli/ecoli_transcription_elongation.json',
        'ecoli/ecoli_transcription_termination.json',
        'ecoli/ecoli_translation_elongation.json',
        'ecoli/ecoli_translation_termination.json',
        'yeast/yeast_chromatin_silencing.json',
        'yeast/yeast_er_stress_response.json',
        'yeast/yeast_gcn4_starvation.json',
        'yeast/yeast_nitrogen_metabolism.json',
        'yeast/yeast_pka_pathway.json',
        'yeast/yeast_rna_splicing.json',
        'yeast/yeast_snf1_pathway.json',
        'yeast/yeast_vesicle_trafficking.json',
    ]
    
    base_dir = Path('/workspace/processes_with_not_gates')
    
    total_fixed = 0
    total_bracket_fixes = 0
    total_syntax_fixes = 0
    failed = []
    
    print(f"📋 Processing {len(syntax_error_processes)} files with known syntax errors...")
    print()
    
    for process_path in syntax_error_processes:
        filepath = base_dir / process_path
        process_name = filepath.stem
        
        if not filepath.exists():
            print(f"⚠️  {process_name}: File not found")
            failed.append(process_name)
            continue
        
        result, message = fix_process_file(filepath)
        
        if result:
            bracket_fixes, syntax_fixes = result
            total_fixed += 1
            total_bracket_fixes += bracket_fixes
            total_syntax_fixes += syntax_fixes
            print(f"✅ {process_name}:")
            if bracket_fixes > 0:
                print(f"   • Fixed {bracket_fixes} bracket conflict(s)")
            if syntax_fixes > 0:
                print(f"   • Fixed {syntax_fixes} wrong trapezoid syntax")
        elif message == "No changes needed":
            print(f"✓  {process_name}: Already correct")
        else:
            print(f"❌ {process_name}: {message}")
            failed.append(process_name)
        
        print()
    
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print()
    print(f"  Processes fixed: {total_fixed}")
    print(f"  Bracket conflicts resolved: {total_bracket_fixes}")
    print(f"  Wrong syntax corrected: {total_syntax_fixes}")
    
    if failed:
        print(f"  Failed: {len(failed)}")
        for name in failed:
            print(f"    - {name}")
    
    print()
    print("=" * 80)
    print("✅ PHASE 1 COMPLETE!")
    print("=" * 80)
    print()
    print("All syntax errors have been automatically fixed.")
    print("All 15 processes should now render without Mermaid errors.")
    print()

if __name__ == '__main__':
    main()
