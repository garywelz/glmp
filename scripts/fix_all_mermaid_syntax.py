#!/usr/bin/env python3
"""
Comprehensive Mermaid syntax fixer for all GLMP process files.
Fixes all known syntax issues discovered during troubleshooting.

Issues fixed:
1. Colons in node labels -> quote-wrap them
2. (pattern)2+ patterns -> add space: (pattern) 2+
3. Brackets/parentheses in trapezoid labels -> remove them
"""

import json
import re
import sys
import os
from pathlib import Path

def fix_colons_in_labels(mermaid_text):
    """Quote-wrap node labels containing colons or (...)+ patterns"""
    # Pattern: nodeId[label with colon or (pattern)2+]
    # Match: A8[Under aerobic conditions: FNR has...]
    # Or: A10[text with (pattern)2+ more text]
    
    def quote_wrapper(match):
        node_id = match.group(1)
        label = match.group(2)
        
        # Check if label already quoted
        if label.startswith('"') and label.endswith('"'):
            return match.group(0)  # Already quoted
        
        # Check if label needs quoting (has colon or (...)+ pattern)
        if ':' in label or re.search(r'\([^)]+\)\d+\+', label):
            # Escape any existing quotes in the label
            label_escaped = label.replace('"', '\\"')
            return f'{node_id}["{label_escaped}"]'
        
        return match.group(0)  # No change needed
    
    # Match node definitions: nodeId[label content]
    # Exclude already quoted labels and special shapes
    pattern = r'(\w+)\[([^"\]]*(?::|\([^)]+\)\d+\+)[^"\]]*)\]'
    return re.sub(pattern, quote_wrapper, mermaid_text)

def fix_pattern2plus(mermaid_text):
    """Add space in (pattern)2+ patterns: (pattern) 2+"""
    # Replace (4Fe-4S)2+ with (4Fe-4S) 2+
    return re.sub(r'\(([^)]+)\)(\d+)\+', r'(\1) \2+', mermaid_text)

def fix_trapezoid_brackets(mermaid_text):
    """Remove brackets, parentheses, and backslashes from inside trapezoid labels"""
    def replacer(match):
        label_content = match.group(1)
        # Remove all brackets, parentheses, and backslashes
        fixed = re.sub(r'[\[\]()\\]', '', label_content)
        return f'[/{fixed}/]'
    
    # Pattern: [/...content.../]
    pattern = r'\[/([^/]+)/\]'
    fixed = re.sub(pattern, replacer, mermaid_text)
    
    # Also fix malformed patterns: [\{{text}}/] -> [/text/]
    fixed = re.sub(r'\[\\\{\{([^}]+)\}\}/\]', r'[/\1/]', fixed)
    
    # Fix backslash-escaped curly braces in quoted labels: ["\{text"] -> ["{text"]
    fixed = re.sub(r'\["\\\{', r'["{', fixed)
    
    # Fix weird endings: ["text/"] -> ["text"]
    fixed = re.sub(r'\["([^"]+)/"\]', r'["\1"]', fixed)
    
    return fixed

def fix_parentheses_with_commas(mermaid_text):
    """Quote-wrap node labels containing parentheses with commas (e.g., pattern)"""
    def quote_wrapper(match):
        node_id = match.group(1)
        label = match.group(2)
        
        if label.startswith('"') or label.startswith('|'):
            return match.group(0)
        
        if re.search(r'\([^)]*,[^)]*\)', label):
            label_escaped = label.replace('"', '\\"')
            return f'{node_id}["{label_escaped}"]'
        
        return match.group(0)
    
    pattern = r'(\w+)\[([^\]]*\([^)]*,[^)]*\)[^\]]*)\]'
    return re.sub(pattern, quote_wrapper, mermaid_text)

def fix_all_parentheses(mermaid_text):
    """Quote-wrap ALL node labels containing parentheses (not just with commas)"""
    def quote_wrapper(match):
        node_id = match.group(1)
        label = match.group(2)
        
        # Skip if already quoted, is edge label, or is trapezoid
        if label.startswith('"') or label.startswith('|') or label.startswith('/'):
            return match.group(0)
        
        # Check if label has any parentheses (even with style syntax like :::red)
        # Extract the actual label part (before any ::: style syntax)
        label_part = label.split(':::')[0] if ':::' in label else label
        
        if '(' in label_part and ')' in label_part:
            # Preserve style syntax if present
            if ':::' in label:
                style_part = ':::' + label.split(':::', 1)[1]
                label_escaped = label_part.replace('"', '\\"')
                return f'{node_id}["{label_escaped}"]{style_part}'
            else:
                label_escaped = label.replace('"', '\\"')
                return f'{node_id}["{label_escaped}"]'
        
        return match.group(0)
    
    # Match node definitions with parentheses in square brackets (including style syntax)
    pattern = r'(\w+)\[([^\]]*\([^)]+\)[^\]]*)\]'
    fixed = re.sub(pattern, quote_wrapper, mermaid_text)
    
    # Also fix rounded rectangle nodes (nodeId(...)) with parentheses inside
    # Convert to square brackets with quotes: nodeId(...) -> nodeId["..."]
    def fix_rounded_rect(match):
        node_id = match.group(1)
        label = match.group(2)
        if '(' in label and ')' in label:
            label_escaped = label.replace('"', '\\"')
            return f'{node_id}["{label_escaped}"]'
        return match.group(0)
    
    rounded_pattern = r'(\w+)\(([^)]*\([^)]+\)[^)]*)\)'
    fixed = re.sub(rounded_pattern, fix_rounded_rect, fixed)
    
    return fixed

def fix_all_syntax(mermaid_text):
    """Apply all fixes in the correct order"""
    # Order matters:
    # 1. Fix trapezoid brackets first (before other processing)
    # 2. Fix pattern2+ (before quote-wrapping)
    # 3. Fix ALL parentheses (not just with commas - Mermaid has issues with any parentheses)
    # 4. Fix colons (quote-wrap last)
    
    fixed = fix_trapezoid_brackets(mermaid_text)
    fixed = fix_pattern2plus(fixed)
    fixed = fix_all_parentheses(fixed)  # Fix ALL parentheses, not just with commas
    fixed = fix_colons_in_labels(fixed)
    
    return fixed

def process_file(file_path):
    """Process a single JSON file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        if 'mermaid' not in data:
            return {'status': 'skip', 'reason': 'No mermaid field'}
        
        original = data['mermaid']
        fixed = fix_all_syntax(original)
        
        if original == fixed:
            return {'status': 'ok', 'changes': 0}
        
        # Count changes
        changes = {
            'colons': len(re.findall(r'\["[^"]*:[^"]*"\]', fixed)) - len(re.findall(r'\["[^"]*:[^"]*"\]', original)),
            'pattern2plus': len(re.findall(r'\([^)]+\) \d+\+', fixed)) - len(re.findall(r'\([^)]+\) \d+\+', original)),
            'trapezoid_fixes': len(re.findall(r'\[/[^/]*[\[\]()][^/]*/\]', original))
        }
        
        # Create backup
        backup_path = str(file_path) + '.backup'
        with open(backup_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Write fixed version
        data['mermaid'] = fixed
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return {'status': 'fixed', 'changes': changes}
        
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

def main():
    if len(sys.argv) > 1:
        # Process single file
        file_path = Path(sys.argv[1])
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            sys.exit(1)
        
        result = process_file(file_path)
        if result['status'] == 'fixed':
            print(f"✅ Fixed: {file_path}")
            print(f"   Changes: {result['changes']}")
        elif result['status'] == 'ok':
            print(f"✓ No changes needed: {file_path}")
        else:
            print(f"❌ Error: {file_path} - {result.get('error', 'Unknown error')}")
    else:
        # Process all files in processes_with_not_gates
        base_dir = Path('processes_with_not_gates')
        if not base_dir.exists():
            print(f"❌ Directory not found: {base_dir}")
            sys.exit(1)
        
        json_files = list(base_dir.rglob('*.json'))
        print(f"📋 Found {len(json_files)} process files")
        print(f"🔧 Applying syntax fixes...\n")
        
        results = {'fixed': 0, 'ok': 0, 'error': 0, 'skip': 0}
        
        for json_file in json_files:
            result = process_file(json_file)
            results[result['status']] = results.get(result['status'], 0) + 1
            
            if result['status'] == 'fixed':
                print(f"✅ {json_file.name}")
            elif result['status'] == 'error':
                print(f"❌ {json_file.name}: {result.get('error', 'Unknown')}")
        
        print(f"\n📊 Summary:")
        print(f"   ✅ Fixed: {results['fixed']}")
        print(f"   ✓ No changes: {results['ok']}")
        print(f"   ⚠️  Errors: {results['error']}")
        print(f"   ⊘ Skipped: {results['skip']}")

if __name__ == '__main__':
    main()

