#!/usr/bin/env python3
import re
import os

def fix_mermaid_diagrams(file_path):
    """Fix Mermaid syntax issues in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all mermaid diagrams
        mermaid_pattern = r'<div class="mermaid">(.*?)</div>'
        
        def fix_diagram(match):
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
        fixed_content = re.sub(mermaid_pattern, fix_diagram, content, flags=re.DOTALL)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"Fixed {file_path}")
        return True
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Main function to fix all HTML files in collections directories."""
    # Directories to process
    collections_dirs = [
        'collections/yeast',
        'collections/ecoli', 
        'collections/advanced_systems',
        'collections/featured_papers'
    ]
    
    total_fixed = 0
    
    for directory in collections_dirs:
        if os.path.exists(directory):
            print(f"\nProcessing directory: {directory}")
            
            # Find all HTML files in this directory
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.html'):
                        file_path = os.path.join(root, file)
                        
                        # Check if file contains mermaid diagrams
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if '<div class="mermaid">' in content:
                                print(f"Found Mermaid diagrams in: {file_path}")
                                if fix_mermaid_diagrams(file_path):
                                    total_fixed += 1
        else:
            print(f"Directory not found: {directory}")
    
    print(f"\nSuccessfully fixed {total_fixed} files")

if __name__ == "__main__":
    main()
