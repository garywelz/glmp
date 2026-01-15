#!/usr/bin/env python3
import re
import os

def fix_file(file_path):
    """Fix a single HTML file with duplicate legends and Mermaid syntax issues."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove all duplicate legend sections
        legend_pattern = r'<div style="display: grid; grid-template-columns: repeat\(auto-fit,minmax\(140px,1fr\)\); gap: \.5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">.*?</div>'
        
        # Find all legends
        legends = re.findall(legend_pattern, content, re.DOTALL)
        
        if len(legends) > 1:
            # Keep only the first legend and remove all others
            first_legend = legends[0]
            content = re.sub(legend_pattern, '', content, flags=re.DOTALL)
            
            # Insert the first legend back after the first mermaid diagram
            mermaid_end_pattern = r'(</div>\s*<div style="display: grid)'
            content = re.sub(mermaid_end_pattern, r'\1' + first_legend + r'\1', content, count=1)
        
        # Fix Mermaid syntax by ensuring unique node names
        mermaid_pattern = r'<div class="mermaid">(.*?)</div>'
        
        def fix_mermaid_diagram(match):
            diagram = match.group(1)
            
            # Normalize whitespace
            diagram = re.sub(r'\s+', ' ', diagram).strip()
            
            # Split into components
            parts = diagram.split(' ')
            fixed_parts = []
            node_counter = 0
            node_map = {}
            
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                
                # Handle graph TD
                if part in ['graph', 'TD']:
                    fixed_parts.append(part)
                    continue
                
                # Handle comments
                if part.startswith('%%'):
                    fixed_parts.append('\n' + part)
                    continue
                
                # Handle node definitions A[text]
                if re.match(r'^[A-Z]\[.*\]$', part):
                    text_match = re.match(r'^[A-Z]\[(.*)\]$', part)
                    if text_match:
                        text_content = text_match.group(1)
                        # Create unique node name
                        node_name = chr(65 + node_counter)  # A, B, C, etc.
                        node_counter += 1
                        old_name = part[0]
                        node_map[old_name] = node_name
                        fixed_parts.append('\n' + node_name + '[' + text_content + ']')
                    continue
                
                # Handle arrows
                if part in ['-->', '--', '==>', '==', '->']:
                    fixed_parts.append('\n  ' + part)
                    continue
                
                # Handle style definitions
                if part.startswith('style'):
                    fixed_parts.append('\n  ' + part)
                    continue
                
                # Handle other content
                fixed_parts.append(part)
            
            # Join and fix node references
            fixed_diagram = ' '.join(fixed_parts)
            
            # Replace old node names with new ones in arrows
            for old_name, new_name in node_map.items():
                fixed_diagram = re.sub(r'\b' + old_name + r'\b(?!\[)', new_name, fixed_diagram)
            
            return f'<div class="mermaid">\n{fixed_diagram}\n</div>'
        
        # Apply the fix
        content = re.sub(mermaid_pattern, fix_mermaid_diagram, content, flags=re.DOTALL)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed {file_path}")
        return True
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Main function to fix all HTML files with duplicate legends."""
    # List of files that need fixing based on the grep results
    files_to_fix = [
        'physics_processes.html',
        'mathematics_processes.html',
        'human_chemical_processes.html',
        'computer_science_processes.html',
        'docs/paper/genome-logic-modeling-publication.html'
    ]
    
    print(f"Found {len(files_to_fix)} files to fix")
    
    fixed_count = 0
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            if fix_file(file_path):
                fixed_count += 1
        else:
            print(f"File not found: {file_path}")
    
    print(f"Successfully fixed {fixed_count} files")

if __name__ == "__main__":
    main()



