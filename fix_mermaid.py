#!/usr/bin/env python3
import re
import os

def fix_mermaid_diagrams(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find all mermaid diagrams and add line breaks
    def fix_diagram(match):
        diagram = match.group(1)
        # Add line breaks after key elements
        diagram = re.sub(r'(graph TD)', r'\1\n', diagram)
        diagram = re.sub(r'([A-Z]\[[^\]]*\])', r'\n\1', diagram)
        diagram = re.sub(r'(-->|--|==>)', r'\n\1', diagram)
        diagram = re.sub(r'(style [^}]*})', r'\n\1', diagram)
        return f'<div class="mermaid">\n{diagram}\n</div>'
    
    # Apply the fix
    fixed_content = re.sub(r'<div class="mermaid">(.*?)</div>', fix_diagram, content, flags=re.DOTALL)
    
    with open(file_path, 'w') as f:
        f.write(fixed_content)
    
    print(f"Fixed {file_path}")

# Find all HTML files and fix them
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            # Check if file contains mermaid diagrams
            with open(file_path, 'r') as f:
                content = f.read()
                if '<div class="mermaid">' in content:
                    fix_mermaid_diagrams(file_path)
