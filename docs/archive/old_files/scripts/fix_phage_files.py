#!/usr/bin/env python3
import re

def fix_phage_file(file_path):
    """Fix Mermaid syntax issues in phage HTML files."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all mermaid diagrams
        mermaid_pattern = r'<div class="mermaid">(.*?)</div>'
        
        def fix_diagram(match):
            diagram = match.group(1)
            diagram = re.sub(r'\s+', ' ', diagram).strip()
            parts = diagram.split(' ')
            fixed_parts = []
            node_counter = 0
            node_map = {}
            
            for part in parts:
                part = part.strip()
                if not part: continue
                if part in ['graph', 'TD']: fixed_parts.append(part); continue
                if part.startswith('%%'): fixed_parts.append('\n' + part); continue
                if re.match(r'^[A-Z]\[.*\]$', part):
                    text_match = re.match(r'^[A-Z]\[(.*)\]$', part)
                    if text_match:
                        text_content = text_match.group(1)
                        node_name = chr(65 + node_counter)
                        node_counter += 1
                        old_name = part[0]
                        node_map[old_name] = node_name
                        fixed_parts.append('\n' + node_name + '[' + text_content + ']')
                    continue
                if part in ['-->', '--', '==>', '==', '->']: fixed_parts.append('\n  ' + part); continue
                if part.startswith('style'): fixed_parts.append('\n  ' + part); continue
                fixed_parts.append(part)
            
            fixed_diagram = ' '.join(fixed_parts)
            for old_name, new_name in node_map.items():
                fixed_diagram = re.sub(r'\b' + old_name + r'\b(?!\[)', new_name, fixed_diagram)
            
            return f'<div class="mermaid">\n{fixed_diagram}\n</div>'
        
        fixed_content = re.sub(mermaid_pattern, fix_diagram, content, flags=re.DOTALL)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"Fixed {file_path}")
        return True
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    files_to_fix = [
        'phage_lambda_decision_switch.html',
        'phage_t7_time_cascade.html'
    ]
    
    for file_path in files_to_fix:
        if fix_phage_file(file_path):
            print(f"Successfully fixed {file_path}")
        else:
            print(f"Failed to fix {file_path}")

if __name__ == "__main__":
    main()



