#!/usr/bin/env python3
"""
Quick Mermaid Syntax Fix
Simple fix for compressed Mermaid syntax in HTML files.
"""

import os
import re
import glob

def fix_compressed_mermaid(content):
    """Fix compressed Mermaid syntax by separating statements."""
    
    # Find all Mermaid diagram sections
    def fix_mermaid_section(match):
        mermaid_content = match.group(1)
        
        # Split compressed statements
        lines = mermaid_content.split('\n')
        fixed_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('graph TD'):
                fixed_lines.append(line)
                continue
                
            if line.startswith('%%'):
                fixed_lines.append(line)
                continue
                
            if line.startswith('style'):
                # Split multiple style statements
                styles = re.findall(r'style\s+\w+\s+fill:[^;]+;', line)
                for style in styles:
                    fixed_lines.append(f'    {style}')
                continue
            
            # Split compressed arrow statements
            if '-->' in line:
                # Split by arrow but preserve the arrow
                parts = re.split(r'(\s*-->\s*)', line)
                current_statement = ''
                for i, part in enumerate(parts):
                    if '-->' in part:
                        current_statement += part
                        if current_statement.strip():
                            fixed_lines.append(f'    {current_statement.strip()}')
                        current_statement = ''
                    else:
                        current_statement += part
                
                if current_statement.strip():
                    fixed_lines.append(f'    {current_statement.strip()}')
                continue
            
            # Regular line
            fixed_lines.append(f'    {line}')
        
        return '\n'.join(fixed_lines)
    
    # Apply the fix to all Mermaid sections
    pattern = r'(graph TD[^<]+?)</div>'
    return re.sub(pattern, lambda m: fix_mermaid_section(m) + '\n                    </div>', content, flags=re.DOTALL)

def main():
    """Main function to fix all HTML files."""
    print("🔧 Quick Mermaid syntax fix...")
    
    # Find all HTML files
    html_files = []
    html_files.extend(glob.glob("*.html"))
    
    collections_dirs = ["collections/yeast", "collections/ecoli", "collections/advanced_systems"]
    for dir_path in collections_dirs:
        if os.path.exists(dir_path):
            html_files.extend(glob.glob(f"{dir_path}/*.html"))
    
    print(f"📁 Found {len(html_files)} HTML files")
    
    fixed_count = 0
    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'graph TD' in content:
                print(f"🔧 Fixing: {filepath}")
                fixed_content = fix_compressed_mermaid(content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                fixed_count += 1
                print(f"   ✅ Fixed")
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🎉 Fixed {fixed_count} files!")

if __name__ == "__main__":
    main()
