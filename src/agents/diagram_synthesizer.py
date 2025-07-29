#!/usr/bin/env python3
"""
Diagram Synthesizer AI Agent for GLMP
Task: Convert logic into standardized flowcharts
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon
import numpy as np

@dataclass
class FlowchartElement:
    """Represents a flowchart element."""
    element_id: str
    element_type: str  # 'start', 'end', 'decision', 'process', 'input', 'output'
    label: str
    position: Tuple[float, float]
    size: Tuple[float, float] = (1.0, 0.5)
    style: Dict[str, Any] = None

@dataclass
class FlowchartConnection:
    """Represents a connection between flowchart elements."""
    from_element: str
    to_element: str
    label: str = ""
    condition: str = ""
    style: str = "solid"  # 'solid', 'dashed', 'dotted'

@dataclass
class Flowchart:
    """Complete flowchart representation."""
    title: str
    elements: List[FlowchartElement]
    connections: List[FlowchartConnection]
    metadata: Dict[str, Any]

class DiagramSynthesizer:
    """AI agent for converting logic into standardized flowcharts."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.element_styles = self._initialize_styles()
        
    def _initialize_styles(self) -> Dict[str, Dict[str, Any]]:
        """Initialize styles for different flowchart elements."""
        return {
            'start': {
                'shape': 'oval',
                'color': '#90EE90',  # Light green
                'edgecolor': '#228B22',
                'linewidth': 2
            },
            'end': {
                'shape': 'oval',
                'color': '#FFB6C1',  # Light red
                'edgecolor': '#DC143C',
                'linewidth': 2
            },
            'decision': {
                'shape': 'diamond',
                'color': '#87CEEB',  # Light blue
                'edgecolor': '#4169E1',
                'linewidth': 2
            },
            'process': {
                'shape': 'rectangle',
                'color': '#F0F8FF',  # Light cyan
                'edgecolor': '#4682B4',
                'linewidth': 1.5
            },
            'input': {
                'shape': 'parallelogram',
                'color': '#E6E6FA',  # Light purple
                'edgecolor': '#9370DB',
                'linewidth': 1.5
            },
            'output': {
                'shape': 'parallelogram',
                'color': '#FFFACD',  # Light yellow
                'edgecolor': '#DAA520',
                'linewidth': 1.5
            }
        }
    
    def synthesize_from_logic(self, logic_elements: List[Dict], title: str = "Biological Logic Flowchart") -> Flowchart:
        """Convert logic elements into a flowchart."""
        elements = []
        connections = []
        
        # Create start element
        start_element = FlowchartElement(
            element_id="start",
            element_type="start",
            label="Start",
            position=(0, 0)
        )
        elements.append(start_element)
        
        current_y = -1.5
        element_id_counter = 1
        
        # Process each logic element
        for logic_elem in logic_elements:
            element_type = logic_elem.get('element_type', 'process')
            description = logic_elem.get('description', '')
            
            # Determine flowchart element type based on logic type
            flowchart_type = self._map_logic_to_flowchart_type(element_type, description)
            
            # Create element
            element = FlowchartElement(
                element_id=f"elem_{element_id_counter}",
                element_type=flowchart_type,
                label=self._create_element_label(description, flowchart_type),
                position=(0, current_y)
            )
            elements.append(element)
            
            # Create connection from previous element
            if element_id_counter == 1:
                connections.append(FlowchartConnection(
                    from_element="start",
                    to_element=element.element_id
                ))
            else:
                prev_element = elements[element_id_counter - 1]
                connections.append(FlowchartConnection(
                    from_element=prev_element.element_id,
                    to_element=element.element_id
                ))
            
            current_y -= 1.5
            element_id_counter += 1
        
        # Create end element
        end_element = FlowchartElement(
            element_id="end",
            element_type="end",
            label="End",
            position=(0, current_y)
        )
        elements.append(end_element)
        
        # Connect last element to end
        if elements:
            last_element = elements[-2]  # -2 because -1 is the end element
            connections.append(FlowchartConnection(
                from_element=last_element.element_id,
                to_element="end"
            ))
        
        # Create metadata
        metadata = {
            'total_elements': len(elements),
            'logic_elements_processed': len(logic_elements),
            'element_types': self._count_element_types(elements),
            'generation_method': 'logic_synthesis'
        }
        
        return Flowchart(
            title=title,
            elements=elements,
            connections=connections,
            metadata=metadata
        )
    
    def _map_logic_to_flowchart_type(self, logic_type: str, description: str) -> str:
        """Map logic element type to flowchart element type."""
        description_lower = description.lower()
        
        if logic_type == 'conditional':
            return 'decision'
        elif logic_type == 'trigger':
            return 'input'
        elif logic_type == 'state':
            return 'process'
        elif logic_type == 'loop':
            # Check for loop indicators in description
            if any(word in description_lower for word in ['loop', 'cycle', 'repeat', 'iterative']):
                return 'process'  # Represent as process with loop annotation
            else:
                return 'process'
        elif logic_type == 'subroutine':
            return 'process'
        else:
            return 'process'
    
    def _create_element_label(self, description: str, element_type: str) -> str:
        """Create a clean label for flowchart element."""
        # Clean up the description
        label = description.strip()
        
        # Remove common prefixes
        prefixes_to_remove = ['if ', 'when ', 'provided that ', 'conditional on ']
        for prefix in prefixes_to_remove:
            if label.lower().startswith(prefix.lower()):
                label = label[len(prefix):]
        
        # Truncate if too long
        if len(label) > 50:
            label = label[:47] + "..."
        
        # Add type-specific formatting
        if element_type == 'decision':
            if not label.lower().startswith(('is ', 'are ', 'has ', 'have ')):
                label = f"Is {label}?"
        
        return label
    
    def _count_element_types(self, elements: List[FlowchartElement]) -> Dict[str, int]:
        """Count elements by type."""
        counts = {}
        for elem in elements:
            counts[elem.element_type] = counts.get(elem.element_type, 0) + 1
        return counts
    
    def render_flowchart(self, flowchart: Flowchart, output_path: str, 
                        figsize: Tuple[int, int] = (12, 16)):
        """Render flowchart to image file."""
        fig, ax = plt.subplots(figsize=figsize)
        
        # Set up the plot
        ax.set_xlim(-5, 5)
        ax.set_ylim(-20, 2)
        ax.axis('off')
        
        # Draw title
        ax.text(0, 1.5, flowchart.title, fontsize=16, fontweight='bold', 
                ha='center', va='center')
        
        # Draw elements
        element_positions = {}
        for element in flowchart.elements:
            style = self.element_styles[element.element_type]
            x, y = element.position
            
            # Draw the element based on its shape
            if style['shape'] == 'oval':
                self._draw_oval(ax, x, y, element.label, style)
            elif style['shape'] == 'diamond':
                self._draw_diamond(ax, x, y, element.label, style)
            elif style['shape'] == 'rectangle':
                self._draw_rectangle(ax, x, y, element.label, style)
            elif style['shape'] == 'parallelogram':
                self._draw_parallelogram(ax, x, y, element.label, style)
            
            element_positions[element.element_id] = (x, y)
        
        # Draw connections
        for connection in flowchart.connections:
            if connection.from_element in element_positions and connection.to_element in element_positions:
                x1, y1 = element_positions[connection.from_element]
                x2, y2 = element_positions[connection.to_element]
                
                # Draw arrow
                ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                           arrowprops=dict(arrowstyle='->', lw=2, color='black'))
                
                # Add label if present
                if connection.label:
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2
                    ax.text(mid_x, mid_y, connection.label, 
                           fontsize=8, ha='center', va='center',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _draw_oval(self, ax, x, y, label, style):
        """Draw oval element."""
        ellipse = patches.Ellipse((x, y), 2, 0.8, 
                                 facecolor=style['color'], 
                                 edgecolor=style['edgecolor'],
                                 linewidth=style['linewidth'])
        ax.add_patch(ellipse)
        ax.text(x, y, label, ha='center', va='center', fontsize=10, fontweight='bold')
    
    def _draw_diamond(self, ax, x, y, label, style):
        """Draw diamond element."""
        diamond = patches.Polygon([(x, y+0.4), (x+1, y), (x, y-0.4), (x-1, y)],
                                 facecolor=style['color'],
                                 edgecolor=style['edgecolor'],
                                 linewidth=style['linewidth'])
        ax.add_patch(diamond)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold')
    
    def _draw_rectangle(self, ax, x, y, label, style):
        """Draw rectangle element."""
        rect = patches.Rectangle((x-1, y-0.3), 2, 0.6,
                                facecolor=style['color'],
                                edgecolor=style['edgecolor'],
                                linewidth=style['linewidth'])
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold')
    
    def _draw_parallelogram(self, ax, x, y, label, style):
        """Draw parallelogram element."""
        para = patches.Polygon([(x-1, y-0.3), (x-0.3, y+0.3), (x+1, y+0.3), (x+0.3, y-0.3)],
                              facecolor=style['color'],
                              edgecolor=style['edgecolor'],
                              linewidth=style['linewidth'])
        ax.add_patch(para)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold')
    
    def save_flowchart_data(self, flowchart: Flowchart, output_path: str):
        """Save flowchart data to JSON file."""
        data = {
            'title': flowchart.title,
            'metadata': flowchart.metadata,
            'elements': [
                {
                    'element_id': elem.element_id,
                    'element_type': elem.element_type,
                    'label': elem.label,
                    'position': elem.position,
                    'size': elem.size
                }
                for elem in flowchart.elements
            ],
            'connections': [
                {
                    'from_element': conn.from_element,
                    'to_element': conn.to_element,
                    'label': conn.label,
                    'condition': conn.condition,
                    'style': conn.style
                }
                for conn in flowchart.connections
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    """Example usage of the Diagram Synthesizer."""
    synthesizer = DiagramSynthesizer()
    
    # Example logic elements (from Extractor Agent output)
    logic_elements = [
        {
            'element_type': 'conditional',
            'description': 'When lactose is present',
            'confidence': 0.8
        },
        {
            'element_type': 'process',
            'description': 'Repressor protein is inactivated',
            'confidence': 0.9
        },
        {
            'element_type': 'conditional',
            'description': 'If glucose is also present',
            'confidence': 0.7
        },
        {
            'element_type': 'process',
            'description': 'cAMP levels are low',
            'confidence': 0.8
        },
        {
            'element_type': 'loop',
            'description': 'Feedback loop responds to environmental conditions',
            'confidence': 0.6
        }
    ]
    
    # Synthesize flowchart
    flowchart = synthesizer.synthesize_from_logic(logic_elements, "Lac Operon Regulation")
    
    # Render and save
    synthesizer.render_flowchart(flowchart, "lac_operon_flowchart.png")
    synthesizer.save_flowchart_data(flowchart, "lac_operon_flowchart.json")
    
    print("=== Diagram Synthesizer Results ===")
    print(f"Title: {flowchart.title}")
    print(f"Total elements: {flowchart.metadata['total_elements']}")
    print(f"Element types: {flowchart.metadata['element_types']}")
    print("\nFlowchart saved as lac_operon_flowchart.png")
    print("Flowchart data saved as lac_operon_flowchart.json")

if __name__ == "__main__":
    main()