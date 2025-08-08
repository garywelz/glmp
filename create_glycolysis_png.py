#!/usr/bin/env python3
"""
Create a PNG version of the glycolysis flowchart using matplotlib.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# Set up the figure
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')

# Colors
blue = '#0277bd'
orange = '#f57c00'
green = '#388e3c'
light_blue = '#e1f5fe'
light_orange = '#fff3e0'
light_green = '#e8f5e8'

# Define node positions and content
nodes = [
    # (x, y, width, height, text_lines, color, edge_color)
    (1, 6.5, 1.5, 0.8, ['Glucose Uptake', '(Transport into cell)'], light_blue, blue),
    (3, 6.5, 1.5, 0.8, ['Hexokinase', 'Glucose → G6P'], light_blue, blue),
    (5, 6.5, 1.5, 0.8, ['Isomerase', 'G6P → F6P'], light_blue, blue),
    (7, 6.5, 1.5, 0.8, ['Phosphofructokinase', 'F6P → F1,6BP'], light_blue, blue),
    
    # Branch nodes
    (1, 4.5, 1.5, 0.8, ['DHAP', '(Dihydroxyacetone', 'phosphate)'], light_orange, orange),
    (3, 4.5, 1.5, 0.8, ['G3P', '(Glyceraldehyde‑3‑', 'phosphate)'], light_orange, orange),
    
    # Payoff phase
    (5, 4.5, 1.5, 0.8, ['G3P Oxidation &', 'Phosphorylation', '(NADH + ATP yield)'], light_blue, blue),
    (7, 4.5, 1.5, 0.8, ['Phosphoglycerate', 'Mutase & Enolase', '→ PEP'], light_blue, blue),
    
    # Final steps
    (5, 2.5, 1.5, 0.8, ['Pyruvate Kinase', 'PEP → Pyruvate + ATP'], light_blue, blue),
    (7, 2.5, 1.5, 0.8, ['End Product:', '2 Pyruvate', 'Molecules'], light_green, green),
]

# Draw nodes
for x, y, w, h, text_lines, fill_color, edge_color in nodes:
    # Create rounded rectangle
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", 
                         facecolor=fill_color, edgecolor=edge_color, linewidth=2)
    ax.add_patch(box)
    
    # Add text
    for i, line in enumerate(text_lines):
        ax.text(x + w/2, y + h - 0.1 - i*0.15, line, 
                ha='center', va='top', fontsize=9, fontweight='bold')

# Draw arrows
arrows = [
    # Main pathway
    ((2.5, 6.9), (3, 6.9)),
    ((4.5, 6.9), (5, 6.9)),
    ((6.5, 6.9), (7, 6.9)),
    
    # Branch from PFK
    ((7.75, 6.5), (7.75, 5.5)),
    ((7.75, 5.5), (1.75, 5.5)),
    ((1.75, 5.5), (1.75, 5.3)),
    
    ((7.75, 5.5), (3.75, 5.5)),
    ((3.75, 5.5), (3.75, 5.3)),
    
    # TPI connections
    ((2.5, 4.9), (3, 4.9)),
    ((3.5, 4.9), (4, 4.9)),
    
    # Continue to payoff
    ((4.5, 4.9), (5, 4.9)),
    ((6.5, 4.9), (7, 4.9)),
    
    # To final steps
    ((7.75, 4.5), (7.75, 3.5)),
    ((7.75, 3.5), (5.75, 3.5)),
    ((5.75, 3.5), (5.75, 3.3)),
    
    # Final arrow
    ((6.5, 2.9), (7, 2.9)),
]

for start, end in arrows:
    arrow = ConnectionPatch(start, end, "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=blue, ec=blue, linewidth=2)
    ax.add_patch(arrow)

# Add labels
ax.text(5, 7.5, 'Glycolysis Pathway in Yeast', ha='center', va='center', 
        fontsize=16, fontweight='bold', color=blue)

# Add TPI labels
ax.text(2.75, 4.7, 'TPI forward', ha='center', va='center', 
        fontsize=8, color=blue, fontweight='bold')
ax.text(3.75, 4.7, 'TPI reverse', ha='center', va='center', 
        fontsize=8, color=blue, fontweight='bold')

plt.tight_layout()
plt.savefig('glycolysis_flowchart.png', dpi=300, bbox_inches='tight')
plt.close()

print("PNG file created: glycolysis_flowchart.png") 