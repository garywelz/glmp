#!/usr/bin/env python3
"""
Create a vertical flowchart that closely matches the original Mermaid layout.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Set up the figure with vertical layout
fig, ax = plt.subplots(1, 1, figsize=(10, 14), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis('off')

# Professional color scheme
colors = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e', 
    'success': '#2ca02c',
    'light_primary': '#e6f3ff',
    'light_secondary': '#fff4e6',
    'light_success': '#e6ffe6',
    'text': '#2c3e50',
    'arrow': '#34495e'
}

# Define nodes in vertical layout (like original Mermaid)
nodes = [
    # (x, y, width, height, text_lines, fill_color, edge_color)
    (4, 12.5, 2.5, 0.8, ['Glucose Uptake', '(Transport into cell)'], colors['light_primary'], colors['primary']),
    (4, 11.5, 2.5, 0.8, ['Hexokinase', 'Glucose → G6P'], colors['light_primary'], colors['primary']),
    (4, 10.5, 2.5, 0.8, ['Isomerase', 'G6P → F6P'], colors['light_primary'], colors['primary']),
    (4, 9.5, 2.5, 0.8, ['Phosphofructokinase (PFK)', 'F6P → F1,6BP'], colors['light_primary'], colors['primary']),
    
    # Branch - split into two columns
    (2, 8.5, 2.5, 0.8, ['DHAP', '(Dihydroxyacetone phosphate)'], colors['light_secondary'], colors['secondary']),
    (6, 8.5, 2.5, 0.8, ['G3P', '(Glyceraldehyde‑3‑phosphate)'], colors['light_secondary'], colors['secondary']),
    
    # Continue from G3P
    (4, 7.5, 2.5, 0.8, ['G3P Oxidation & Phosphorylation', '(NADH + ATP yield)'], colors['light_primary'], colors['primary']),
    (4, 6.5, 2.5, 0.8, ['Phosphoglycerate Mutase & Enolase', '→ PEP'], colors['light_primary'], colors['primary']),
    (4, 5.5, 2.5, 0.8, ['Pyruvate Kinase', 'PEP → Pyruvate + ATP'], colors['light_primary'], colors['primary']),
    (4, 4.5, 2.5, 0.8, ['End Product:', '2 Pyruvate Molecules'], colors['light_success'], colors['success']),
]

# Draw nodes with clear, readable text
for x, y, w, h, text_lines, fill_color, edge_color in nodes:
    # Create rounded rectangle
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", 
                         facecolor=fill_color, edgecolor=edge_color, linewidth=2)
    ax.add_patch(box)
    
    # Add text with larger, clearer font
    for i, line in enumerate(text_lines):
        fontsize = 11 if len(text_lines) == 2 else 10
        ax.text(x + w/2, y + h - 0.1 - i*0.15, line, 
                ha='center', va='top', fontsize=fontsize, fontweight='bold',
                color=colors['text'])

# Define arrows for vertical flow
arrows = [
    # Main vertical pathway
    ((5.25, 12.5), (5.25, 11.7)),  # Glucose Uptake to Hexokinase
    ((5.25, 11.5), (5.25, 10.7)),  # Hexokinase to Isomerase
    ((5.25, 10.5), (5.25, 9.7)),   # Isomerase to PFK
    
    # Branch from PFK
    ((4, 9.5), (2, 8.5)),          # PFK to DHAP
    ((4, 9.5), (6, 8.5)),          # PFK to G3P
    
    # TPI connections (bidirectional)
    ((3.25, 8.9), (5.75, 8.9)),    # DHAP to G3P (TPI forward)
    ((5.75, 8.9), (3.25, 8.9)),    # G3P to DHAP (TPI reverse)
    
    # Continue from G3P
    ((6, 8.5), (5.25, 7.7)),       # G3P to Oxidation
    ((5.25, 7.5), (5.25, 6.7)),    # Oxidation to Mutase
    ((5.25, 6.5), (5.25, 5.7)),    # Mutase to Pyruvate Kinase
    ((5.25, 5.5), (5.25, 4.7)),    # Pyruvate Kinase to End Product
]

# Draw arrows
for start, end in arrows:
    arrow = FancyArrowPatch(start, end,
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=colors['arrow'], ec=colors['arrow'], 
                          linewidth=2)
    ax.add_patch(arrow)

# Add title
ax.text(5, 13.5, 'Glycolysis Pathway in Yeast', ha='center', va='center', 
        fontsize=16, fontweight='bold', color=colors['primary'])

# Add TPI labels
ax.text(4.5, 8.7, 'TPI forward', ha='center', va='center', 
        fontsize=10, color=colors['primary'], fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9, edgecolor=colors['primary']))
ax.text(4.5, 8.3, 'TPI reverse', ha='center', va='center', 
        fontsize=10, color=colors['primary'], fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9, edgecolor=colors['primary']))

# Add phase labels
ax.text(1, 9.2, 'Branch Phase', ha='center', va='center', 
        fontsize=12, fontweight='bold', color=colors['secondary'],
        bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['light_secondary'], alpha=0.8))

ax.text(7, 7.2, 'Payoff Phase', ha='center', va='center', 
        fontsize=12, fontweight='bold', color=colors['primary'],
        bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['light_primary'], alpha=0.8))

plt.tight_layout()
plt.savefig('glycolysis_flowchart_vertical.svg', format='svg', bbox_inches='tight', dpi=300)
plt.savefig('glycolysis_flowchart_vertical.png', format='png', bbox_inches='tight', dpi=300)
plt.close()

print("Vertical flowchart created:")
print("- glycolysis_flowchart_vertical.svg")
print("- glycolysis_flowchart_vertical.png") 