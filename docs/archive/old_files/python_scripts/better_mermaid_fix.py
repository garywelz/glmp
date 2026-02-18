#!/usr/bin/env python3
import re
import os

def fix_mermaid_formatting(file_path):
    """Better fix: properly format Mermaid diagrams with correct line breaks."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all mermaid diagrams
        mermaid_pattern = r'<div class="mermaid">(.*?)</div>'
        
        def fix_diagram(match):
            diagram = match.group(1)
            
            # Normalize whitespace first
            diagram = re.sub(r'\s+', ' ', diagram).strip()
            
            # Split into parts
            parts = diagram.split(' ')
            formatted_parts = []
            
            for i, part in enumerate(parts):
                part = part.strip()
                if not part:
                    continue
                
                # Handle graph TD declaration
                if part == 'graph' or part == 'TD':
                    formatted_parts.append(part)
                    if part == 'TD':
                        formatted_parts.append('\n')
                    continue
                
                # Handle node definitions (A[text])
                if re.match(r'^[A-Z]\[.*\]$', part):
                    formatted_parts.append('\n' + part)
                    continue
                
                # Handle arrows (-->)
                if part in ['-->', '--', '==>', '==', '->']:
                    formatted_parts.append('\n  ' + part)
                    continue
                
                # Handle conditional arrows (-->|text|)
                if part.startswith('-->|') or part.startswith('--|'):
                    formatted_parts.append('\n  ' + part)
                    continue
                
                # Handle style definitions
                if part.startswith('style'):
                    formatted_parts.append('\n' + part)
                    continue
                
                # Handle comments
                if part.startswith('%%'):
                    formatted_parts.append('\n' + part)
                    continue
                
                # Handle other content (node names, etc.)
                formatted_parts.append(part)
            
            # Join and clean up
            formatted_diagram = ' '.join(formatted_parts)
            
            # Clean up extra spaces and ensure proper formatting
            formatted_diagram = re.sub(r'\n\s+', '\n', formatted_diagram)
            formatted_diagram = re.sub(r'\s+\n', '\n', formatted_diagram)
            
            return f'<div class="mermaid">\n{formatted_diagram}\n</div>'
        
        # Apply the fix
        fixed_content = re.sub(mermaid_pattern, fix_diagram, content, flags=re.DOTALL)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"Fixed formatting in: {file_path}")
        return True
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Fix all HTML files with Mermaid diagrams."""
    # Focus on the problematic files first
    target_files = [
        'phage_lambda_decision_switch.html',
        'phage_t7_time_cascade.html', 
        'b_subtilis_sporulation.html'
    ]
    
    print("Fixing target files...")
    for file_path in target_files:
        if os.path.exists(file_path):
            fix_mermaid_formatting(file_path)
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    main()


