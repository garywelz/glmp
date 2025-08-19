#!/usr/bin/env python3
"""
Fix All Mermaid Syntax Issues
Comprehensive fix for all HTML files with corrupted Mermaid syntax.
"""

import os
import re
import glob

def fix_mermaid_syntax_in_file(filepath):
    """Fix Mermaid syntax issues in a single HTML file."""
    print(f"🔧 Fixing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file contains Mermaid diagrams
        if 'graph TD' not in content and 'graph LR' not in content:
            print(f"   ⏭️  No Mermaid diagrams found, skipping")
            return False
        
        # Fix compressed Mermaid diagrams
        # Pattern 1: Fix compressed graph TD sections
        pattern1 = r'(graph TD\s*)([^<]+?)(style\s+\w+\s+fill:)'
        replacement1 = r'\1\n    %% Initial Setup\n    \2\n    \n    %% Styling - Biological Color Scheme\n    \3'
        
        # Pattern 2: Fix compressed style statements
        pattern2 = r'(style\s+\w+\s+fill:[^;]+;)'
        
        def fix_style_statements(match):
            style_line = match.group(1)
            # Split multiple style statements on the same line
            styles = re.findall(r'style\s+\w+\s+fill:[^;]+;', style_line)
            return '\n    '.join(styles)
        
        # Apply fixes
        content = re.sub(pattern1, replacement1, content, flags=re.DOTALL)
        content = re.sub(pattern2, fix_style_statements, content)
        
        # Fix specific compressed patterns
        # Replace compressed arrow patterns
        content = re.sub(r'(\w+\[[^\]]+\])\s*-->\s*(\w+\[[^\]]+\])', r'\1 --> \2', content)
        content = re.sub(r'(\w+\[[^\]]+\])\s*-->\s*(\w+\{[^}]+\})', r'\1 --> \2', content)
        content = re.sub(r'(\w+\{[^}]+\})\s*-->\s*(\w+\[[^\]]+\])', r'\1 --> \2', content)
        
        # Fix compressed style statements
        content = re.sub(r'style\s+(\w+)\s+fill:([^,]+),color:([^;]+);', r'style \1 fill:\2,color:\3;', content)
        
        # Add proper indentation to Mermaid diagrams
        def fix_mermaid_indentation(match):
            mermaid_content = match.group(1)
            lines = mermaid_content.split('\n')
            fixed_lines = []
            for line in lines:
                line = line.strip()
                if line.startswith('graph TD') or line.startswith('graph LR'):
                    fixed_lines.append(line)
                elif line.startswith('%%'):
                    fixed_lines.append(f'    {line}')
                elif line.startswith('style'):
                    fixed_lines.append(f'    {line}')
                elif '-->' in line:
                    fixed_lines.append(f'    {line}')
                elif line:
                    fixed_lines.append(f'    {line}')
            return '\n'.join(fixed_lines)
        
        # Apply indentation fix
        content = re.sub(r'(graph TD[^<]+?)</div>', lambda m: fix_mermaid_indentation(m) + '\n                    </div>', content, flags=re.DOTALL)
        
        # Write the fixed content back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ Fixed successfully")
        return True
        
    except Exception as e:
        print(f"   ❌ Error fixing {filepath}: {e}")
        return False

def main():
    """Main function to fix all HTML files."""
    print("🔧 Starting comprehensive Mermaid syntax fix...")
    
    # Find all HTML files
    html_files = []
    
    # Root directory files
    html_files.extend(glob.glob("*.html"))
    
    # Collections directories
    collections_dirs = ["collections/yeast", "collections/ecoli", "collections/advanced_systems"]
    for dir_path in collections_dirs:
        if os.path.exists(dir_path):
            html_files.extend(glob.glob(f"{dir_path}/*.html"))
    
    print(f"📁 Found {len(html_files)} HTML files to check")
    
    fixed_count = 0
    for filepath in html_files:
        if fix_mermaid_syntax_in_file(filepath):
            fixed_count += 1
    
    print(f"\n🎉 Fix complete!")
    print(f"📊 Fixed {fixed_count} out of {len(html_files)} files")
    print(f"📁 All files are now ready for upload to Hugging Face")

if __name__ == "__main__":
    main()
