#!/usr/bin/env python3
import re
import os

def fix_mermaid_line_breaks(file_path):
    """Simple fix: just add line breaks to compressed Mermaid diagrams."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all mermaid diagrams
        mermaid_pattern = r'<div class="mermaid">(.*?)</div>'
        
        def fix_diagram(match):
            diagram = match.group(1)
            
            # Normalize whitespace first
            diagram = re.sub(r'\s+', ' ', diagram).strip()
            
            # Add line breaks after key elements
            diagram = re.sub(r'(graph TD)', r'\1\n', diagram)
            diagram = re.sub(r'([A-Z]\[[^\]]*\])', r'\n\1', diagram)
            diagram = re.sub(r'(-->|--|==>|==|->)', r'\n\1', diagram)
            diagram = re.sub(r'(style [^}]*})', r'\n\1', diagram)
            diagram = re.sub(r'(%%[^}]*})', r'\n\1', diagram)
            
            return f'<div class="mermaid">\n{diagram}\n</div>'
        
        # Apply the fix
        fixed_content = re.sub(mermaid_pattern, fix_diagram, content, flags=re.DOTALL)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"Fixed line breaks in: {file_path}")
        return True
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Fix all HTML files with Mermaid diagrams."""
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Found {len(html_files)} HTML files")
    
    fixed_count = 0
    for file_path in html_files:
        if fix_mermaid_line_breaks(file_path):
            fixed_count += 1
    
    print(f"Fixed {fixed_count} files")

if __name__ == "__main__":
    main()


