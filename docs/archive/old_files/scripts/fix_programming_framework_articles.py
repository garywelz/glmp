#!/usr/bin/env python3
import re

def fix_programming_framework_articles():
    """Fix the programming framework articles with duplicate legends."""
    files_to_fix = [
        'programming_framework_article.html',
        'programming_framework_article_legacy.html'
    ]
    
    for file_path in files_to_fix:
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
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Fixed {file_path}")
            
        except Exception as e:
            print(f"Error fixing {file_path}: {e}")

if __name__ == "__main__":
    fix_programming_framework_articles()



