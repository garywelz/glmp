#!/usr/bin/env python3
import re
import os

def fix_mermaid_manually(file_path):
    """Manual fix for specific Mermaid syntax issues."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all mermaid diagrams
        mermaid_pattern = r'<div class="mermaid">(.*?)</div>'
        
        def fix_diagram(match):
            diagram = match.group(1)
            
            # Normalize whitespace first
            diagram = re.sub(r'\s+', ' ', diagram).strip()
            
            # Fix specific problematic patterns
            # Fix: A[text] --> B[text] (nodes connected by arrows)
            diagram = re.sub(r'([A-Z]\[[^\]]*\]) --> ([A-Z]\[[^\]]*\]|{[^}]*})', r'\1 --> \2', diagram)
            
            # Fix: A[text] -->|text| B[text] (conditional arrows)
            diagram = re.sub(r'([A-Z]\[[^\]]*\]) -->\|([^|]*)\| ([A-Z]\[[^\]]*\]|{[^}]*})', r'\1 -->|\2| \3', diagram)
            
            # Fix: A[text] B[text] (nodes without arrows)
            diagram = re.sub(r'([A-Z]\[[^\]]*\]) ([A-Z]\[[^\]]*\]|{[^}]*})', r'\1\n\2', diagram)
            
            # Add line breaks after graph TD
            diagram = re.sub(r'(graph TD)', r'\1\n', diagram)
            
            # Add line breaks before style statements
            diagram = re.sub(r'(style [^}]*})', r'\n\1', diagram)
            
            # Clean up multiple spaces and ensure proper formatting
            diagram = re.sub(r' +', ' ', diagram)
            diagram = re.sub(r'\n +', '\n', diagram)
            diagram = re.sub(r' +\n', '\n', diagram)
            
            return f'<div class="mermaid">\n{diagram.strip()}\n</div>'
        
        # Apply the fix
        fixed_content = re.sub(mermaid_pattern, fix_diagram, content, flags=re.DOTALL)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"Manually fixed: {file_path}")
        return True
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Fix the problematic files manually."""
    target_files = [
        'phage_lambda_decision_switch.html',
        'phage_t7_time_cascade.html', 
        'b_subtilis_sporulation.html'
    ]
    
    print("Applying manual Mermaid fix...")
    for file_path in target_files:
        if os.path.exists(file_path):
            fix_mermaid_manually(file_path)
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    main()


