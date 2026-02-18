#!/usr/bin/env python3
import re
import os

def fix_mermaid_diagrams(file_path):
    """Fix comprehensive Mermaid syntax issues."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all mermaid diagrams
        mermaid_pattern = r'<div class="mermaid">(.*?)</div>'
        
        def fix_diagram(match):
            diagram = match.group(1)
            
            # Remove any HTML entities and normalize whitespace
            diagram = re.sub(r'\s+', ' ', diagram).strip()
            
            # Split into lines and fix each line
            lines = diagram.split(' ')
            fixed_lines = []
            node_counter = 0
            node_map = {}
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Handle graph TD declaration
                if line == 'graph' or line == 'TD':
                    fixed_lines.append(line)
                    continue
                
                # Handle comments
                if line.startswith('%%'):
                    fixed_lines.append('\n' + line)
                    continue
                
                # Handle node definitions (A[text])
                if re.match(r'^[A-Z]\[.*\]$', line):
                    # Extract the text content
                    text_match = re.match(r'^[A-Z]\[(.*)\]$', line)
                    if text_match:
                        text_content = text_match.group(1)
                        # Create unique node name
                        node_name = chr(65 + node_counter)  # A, B, C, etc.
                        node_counter += 1
                        node_map[line[0]] = node_name
                        fixed_lines.append('\n' + node_name + '[' + text_content + ']')
                    continue
                
                # Handle arrows (-->)
                if line in ['-->', '--', '==>', '==', '->']:
                    fixed_lines.append('\n  ' + line)
                    continue
                
                # Handle style definitions
                if line.startswith('style'):
                    fixed_lines.append('\n  ' + line)
                    continue
                
                # Handle other content
                fixed_lines.append(line)
            
            # Join lines and fix node references in arrows
            fixed_content = ' '.join(fixed_lines)
            
            # Fix node references in arrows (replace old node names with new ones)
            for old_name, new_name in node_map.items():
                fixed_content = re.sub(r'\b' + old_name + r'\b(?!\[)', new_name, fixed_content)
            
            # Remove duplicate legend sections
            legend_pattern = r'<div style="display: grid; grid-template-columns: repeat\(auto-fit,minmax\(140px,1fr\)\); gap: \.5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">.*?</div>'
            legends = re.findall(legend_pattern, content, re.DOTALL)
            if len(legends) > 1:
                # Keep only the first legend
                content = re.sub(legend_pattern, legends[0], content, flags=re.DOTALL)
            
            return f'<div class="mermaid">\n{fixed_content}\n</div>'
        
        # Apply the fix
        fixed_content = re.sub(mermaid_pattern, fix_diagram, content, flags=re.DOTALL)
        
        # Remove duplicate legend sections from the entire content
        legend_pattern = r'<div style="display: grid; grid-template-columns: repeat\(auto-fit,minmax\(140px,1fr\)\); gap: \.5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">.*?</div>'
        legends = re.findall(legend_pattern, fixed_content, re.DOTALL)
        if len(legends) > 1:
            # Keep only the first legend and remove duplicates
            first_legend = legends[0]
            fixed_content = re.sub(legend_pattern, '', fixed_content, flags=re.DOTALL)
            # Insert the first legend back
            fixed_content = fixed_content.replace('</div>', first_legend + '\n</div>', 1)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"Fixed comprehensive Mermaid syntax for: {file_path}")
        return True
        
    except Exception as e:
        print(f"Error fixing Mermaid in {file_path}: {e}")
        return False

def main():
    """Main function to fix all HTML files with Mermaid diagrams."""
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Found {len(html_files)} HTML files to process")
    
    fixed_count = 0
    for html_file in html_files:
        # Check if file contains mermaid diagrams
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if '<div class="mermaid">' in content:
                print(f"Processing: {html_file}")
                if fix_mermaid_diagrams(html_file):
                    fixed_count += 1
    
    print(f"Successfully fixed {fixed_count} HTML files")

if __name__ == "__main__":
    main()



