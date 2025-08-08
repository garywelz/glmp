#!/usr/bin/env python3
"""
Create a high-quality SVG version of the glycolysis flowchart.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch, FancyArrowPatch
import numpy as np

# Set up the figure with high DPI for crisp output
fig, ax = plt.subplots(1, 1, figsize=(16, 10), dpi=300)
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
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

# Define nodes with better positioning and styling
nodes = [
    # (x, y, width, height, text_lines, fill_color, edge_color, node_type)
    (1, 8.5, 1.8, 0.9, ['Glucose Uptake', '(Transport into cell)'], colors['light_primary'], colors['primary'], 'start'),
    (3.5, 8.5, 1.8, 0.9, ['Hexokinase', 'Glucose → G6P'], colors['light_primary'], colors['primary'], 'process'),
    (6, 8.5, 1.8, 0.9, ['Isomerase', 'G6P → F6P'], colors['light_primary'], colors['primary'], 'process'),
    (8.5, 8.5, 1.8, 0.9, ['Phosphofructokinase', 'F6P → F1,6BP'], colors['light_primary'], colors['primary'], 'process'),
    
    # Branch nodes with better spacing
    (1, 6, 1.8, 0.9, ['DHAP', '(Dihydroxyacetone', 'phosphate)'], colors['light_secondary'], colors['secondary'], 'branch'),
    (3.5, 6, 1.8, 0.9, ['G3P', '(Glyceraldehyde‑3‑', 'phosphate)'], colors['light_secondary'], colors['secondary'], 'branch'),
    
    # Payoff phase
    (6, 6, 1.8, 0.9, ['G3P Oxidation &', 'Phosphorylation', '(NADH + ATP yield)'], colors['light_primary'], colors['primary'], 'process'),
    (8.5, 6, 1.8, 0.9, ['Phosphoglycerate', 'Mutase & Enolase', '→ PEP'], colors['light_primary'], colors['primary'], 'process'),
    
    # Final steps
    (6, 3.5, 1.8, 0.9, ['Pyruvate Kinase', 'PEP → Pyruvate + ATP'], colors['light_primary'], colors['primary'], 'process'),
    (8.5, 3.5, 1.8, 0.9, ['End Product:', '2 Pyruvate', 'Molecules'], colors['light_success'], colors['success'], 'end'),
]

# Draw nodes with improved styling
for x, y, w, h, text_lines, fill_color, edge_color, node_type in nodes:
    # Create rounded rectangle with better styling
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15", 
                         facecolor=fill_color, edgecolor=edge_color, linewidth=2.5)
    ax.add_patch(box)
    
    # Add text with better formatting
    for i, line in enumerate(text_lines):
        fontsize = 10 if len(text_lines) == 2 else 9
        ax.text(x + w/2, y + h - 0.1 - i*0.12, line, 
                ha='center', va='top', fontsize=fontsize, fontweight='bold',
                color=colors['text'])

# Define arrows with better styling
arrows = [
    # Main pathway - horizontal
    ((2.8, 8.95), (3.5, 8.95)),
    ((5.3, 8.95), (6, 8.95)),
    ((7.8, 8.95), (8.5, 8.95)),
    
    # Branch from PFK - vertical and horizontal
    ((9.4, 8.5), (9.4, 7.5)),
    ((9.4, 7.5), (1.9, 7.5)),
    ((1.9, 7.5), (1.9, 6.9)),
    
    ((9.4, 7.5), (4.4, 7.5)),
    ((4.4, 7.5), (4.4, 6.9)),
    
    # TPI connections with labels
    ((2.8, 6.45), (3.5, 6.45)),
    ((4.3, 6.45), (5, 6.45)),
    
    # Continue to payoff
    ((5.8, 6.45), (6, 6.45)),
    ((8.3, 6.45), (8.5, 6.45)),
    
    # To final steps
    ((8.5, 6), (8.5, 4.5)),
    ((8.5, 4.5), (6.9, 4.5)),
    ((6.9, 4.5), (6.9, 4.4)),
    
    # Final arrow
    ((7.8, 3.95), (8.5, 3.95)),
]

# Draw arrows with improved styling
for start, end in arrows:
    arrow = FancyArrowPatch(start, end,
                          arrowstyle="->", shrinkA=8, shrinkB=8,
                          mutation_scale=25, fc=colors['arrow'], ec=colors['arrow'], 
                          linewidth=2.5, alpha=0.8)
    ax.add_patch(arrow)

# Add title with better styling
ax.text(6, 9.5, 'Glycolysis Pathway in Yeast', ha='center', va='center', 
        fontsize=18, fontweight='bold', color=colors['primary'])

# Add TPI labels with better positioning
ax.text(3.15, 6.2, 'TPI forward', ha='center', va='center', 
        fontsize=9, color=colors['primary'], fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8, edgecolor=colors['primary']))
ax.text(4.65, 6.2, 'TPI reverse', ha='center', va='center', 
        fontsize=9, color=colors['primary'], fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8, edgecolor=colors['primary']))

# Add phase labels
ax.text(1, 7.8, 'Branch Phase', ha='center', va='center', 
        fontsize=11, fontweight='bold', color=colors['secondary'],
        bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['light_secondary'], alpha=0.7))

ax.text(6, 7.8, 'Payoff Phase', ha='center', va='center', 
        fontsize=11, fontweight='bold', color=colors['primary'],
        bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['light_primary'], alpha=0.7))

plt.tight_layout()
plt.savefig('glycolysis_flowchart_hq.svg', format='svg', bbox_inches='tight', dpi=300)
plt.savefig('glycolysis_flowchart_hq.png', format='png', bbox_inches='tight', dpi=300)
plt.close()

print("High-quality files created:")
print("- glycolysis_flowchart_hq.svg")
print("- glycolysis_flowchart_hq.png") 