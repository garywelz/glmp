#!/usr/bin/env python3
"""
Biological Process HTML Generator
Generates interactive HTML files for biological processes using the Programming Framework template.
Supports 5-level detail sliders with proper Mermaid.js integration and database anchor linking.
"""

import json
import os
import re
from typing import Dict, List, Any

class BiologicalProcessHTMLGenerator:
    def __init__(self, template_path: str = "biological_process_template.html"):
        """Initialize the generator with the HTML template."""
        self.template_path = template_path
        self.template_content = self._load_template()
        
        # Canonical color scheme for Programming Framework
        self.colors = {
            'triggers': '#ff6b6b',      # Red - Triggers & Conditions
            'catalysts': '#ffd43b',     # Yellow - Catalysts & Enzymes  
            'processing': '#51cf66',    # Green - Chemical Processing
            'intermediates': '#74c0fc', # Blue - Intermediates
            'products': '#b197fc'       # Violet - Products
        }
    
    def _load_template(self) -> str:
        """Load the HTML template file."""
        with open(self.template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _create_process_section(self, process_id: int, process_name: str, process_description: str, anchor_id: str) -> str:
        """Create a single process section HTML."""
        return f'''
            <!-- Process {process_id}: {process_name} -->
            <div class="process-item" id="{anchor_id}">
                <h3><a href="#{anchor_id}" class="anchor-link">{process_id}. {process_name}</a></h3>
                <p>{process_description}</p>
                <div class="slider-container">
                    <label for="slider-{process_id}">Detail Level: <span id="level-{process_id}">1</span></label>
                    <input type="range" id="slider-{process_id}" class="slider" min="1" max="5" value="1" oninput="updateFlowchart({process_id}, this.value)">
                    <div class="slider-labels">
                        <span>Basic</span><span>Detailed</span><span>Complex</span><span>Advanced</span><span>Complete</span>
                    </div>
                </div>
                <div class="mermaid-container">
                    <div class="mermaid" id="chart-{process_id}">
                        <!-- Chart will be populated by JavaScript -->
                    </div>
                </div>
                <div class="color-legend">
                    <span><span class="color-box" style="background:{self.colors['triggers']};"></span>Triggers & Conditions</span>
                    <span><span class="color-box" style="background:{self.colors['catalysts']};"></span>Catalysts & Enzymes</span>
                    <span><span class="color-box" style="background:{self.colors['processing']};"></span>Chemical Processing</span>
                    <span><span class="color-box" style="background:{self.colors['intermediates']};"></span>Intermediates</span>
                    <span><span class="color-box" style="background:{self.colors['products']};"></span>Products</span>
                </div>
            </div>'''
    
    def _create_toc_item(self, process_id: int, process_name: str, anchor_id: str) -> str:
        """Create a table of contents item."""
        return f'<li><a href="#{anchor_id}">{process_id}. {process_name}</a></li>'
    
    def _validate_mermaid_syntax(self, mermaid_code: str) -> bool:
        """Basic validation of Mermaid syntax."""
        # Check for basic graph structure
        if not re.search(r'graph\s+(TD|LR|TB|RL)', mermaid_code):
            return False
        
        # Check for balanced brackets and quotes
        open_brackets = mermaid_code.count('[')
        close_brackets = mermaid_code.count(']')
        if open_brackets != close_brackets:
            return False
            
        return True
    
    def generate_html(self, config: Dict[str, Any], output_path: str) -> None:
        """
        Generate HTML file from configuration.
        
        Args:
            config: Configuration dictionary containing organism info and processes
            output_path: Path where the HTML file will be saved
        """
        # Extract configuration
        organism_name = config.get('organism_name', 'Unknown Organism')
        organism_icon = config.get('organism_icon', '🧬')
        batch_name = config.get('batch_name', 'Batch 01')
        category = config.get('category', 'Biological Processes')
        batch_description = config.get('batch_description', 'Interactive biological process analysis.')
        process_type = config.get('process_type', 'Biological')
        processes = config.get('processes', [])
        
        process_count = len(processes)
        
        # Generate TOC items
        toc_items = []
        process_sections = []
        process_data = {}
        
        for i, process in enumerate(processes, 1):
            process_name = process.get('name', f'Process {i}')
            process_description = process.get('description', 'Process description not provided.')
            anchor_id = process.get('anchor_id', process_name.lower().replace(' ', '-').replace('&', 'and'))
            levels = process.get('levels', {})
            
            # Validate Mermaid syntax for each level
            validated_levels = {}
            for level, mermaid_code in levels.items():
                if self._validate_mermaid_syntax(mermaid_code):
                    validated_levels[level] = mermaid_code
                else:
                    print(f"Warning: Invalid Mermaid syntax for Process {i}, Level {level}")
                    validated_levels[level] = f'''graph TD
                        A[Error: Invalid Mermaid Syntax] --> B[Please check the configuration]
                        style A fill:#ff6b6b,color:#fff
                        style B fill:#ffd43b,color:#000'''
            
            # Create TOC item and process section
            toc_items.append(self._create_toc_item(i, process_name, anchor_id))
            process_sections.append(self._create_process_section(i, process_name, process_description, anchor_id))
            process_data[i] = {'levels': validated_levels}
        
        # Replace template placeholders
        html_content = self.template_content
        replacements = {
            '{{ORGANISM_NAME}}': organism_name,
            '{{ORGANISM_ICON}}': organism_icon,
            '{{BATCH_NAME}}': batch_name,
            '{{CATEGORY}}': category,
            '{{BATCH_DESCRIPTION}}': batch_description,
            '{{PROCESS_COUNT}}': str(process_count),
            '{{PROCESS_TYPE}}': process_type,
            '{{TOC_ITEMS}}': '\n                    '.join(toc_items),
            '{{PROCESS_SECTIONS}}': '\n            '.join(process_sections),
            '{{PROCESS_DATA}}': json.dumps(process_data, indent=12)
        }
        
        for placeholder, value in replacements.items():
            html_content = html_content.replace(placeholder, value)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        
        # Write HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Generated HTML file: {output_path}")
        print(f"Processes: {process_count}")
        print(f"Direct link format: {os.path.basename(output_path)}#<process-anchor-id>")

def create_example_config():
    """Create an example configuration for D. melanogaster processes."""
    return {
        "organism_name": "D. melanogaster",
        "organism_icon": "🦟",
        "batch_name": "Batch 01",
        "category": "Development & Genetics",
        "batch_description": "This enhanced version features interactive sliders allowing you to explore each developmental process at 5 different detail levels, revealing the computational logic of Drosophila development.",
        "process_type": "Eukaryotic",
        "processes": [
            {
                "name": "Embryonic Patterning",
                "anchor_id": "embryonic-patterning",
                "description": "Interactive analysis of D. melanogaster embryonic patterning with 5 detail levels showing the computational logic of early development.",
                "levels": {
                    "1": """graph TD
                        A[Maternal Factors] --> B[Axis Formation]
                        B --> C[Pattern Establishment]
                        C --> D[Embryonic Pattern]
                        
                        style A fill:#ff6b6b,color:#fff
                        style B fill:#ffd43b,color:#000
                        style C fill:#51cf66,color:#fff
                        style D fill:#b197fc,color:#fff""",
                    "2": """graph TD
                        A[Maternal Factors] --> B[Bicoid mRNA]
                        A --> C[Nanos mRNA]
                        B --> D[Anterior-Posterior Axis]
                        C --> D
                        D --> E[Gap Gene Expression]
                        E --> F[Segment Formation]
                        F --> G[Embryonic Pattern]
                        
                        style A fill:#ff6b6b,color:#fff
                        style B fill:#ffd43b,color:#000
                        style C fill:#ffd43b,color:#000
                        style D fill:#51cf66,color:#fff
                        style E fill:#74c0fc,color:#fff
                        style F fill:#51cf66,color:#fff
                        style G fill:#b197fc,color:#fff""",
                    # Additional levels would be added here
                }
            },
            {
                "name": "Segmentation",
                "anchor_id": "segmentation", 
                "description": "Interactive analysis of D. melanogaster segmentation with 5 detail levels showing the computational logic of segment formation.",
                "levels": {
                    "1": """graph TD
                        A[Gap Gene Expression] --> B[Segment Formation]
                        B --> C[Segment Boundaries]
                        C --> D[Body Segmentation]
                        
                        style A fill:#ff6b6b,color:#fff
                        style B fill:#ffd43b,color:#000
                        style C fill:#51cf66,color:#fff
                        style D fill:#b197fc,color:#fff""",
                    # Additional levels would be added here
                }
            }
            # Additional processes would be added here
        ]
    }

if __name__ == "__main__":
    # Example usage
    generator = BiologicalProcessHTMLGenerator()
    
    # Create example configuration
    config = create_example_config()
    
    # Generate HTML file
    output_path = "collections/eukaryotic/d_melanogaster_batch01_development_genetics_generated.html"
    generator.generate_html(config, output_path)
    
    print("\nExample configuration created. To customize:")
    print("1. Modify the config dictionary with your organism and process data")
    print("2. Add complete Mermaid diagrams for all 5 detail levels")
    print("3. Ensure anchor_id values match your database links")
    print("4. Run the generator to create your HTML file")