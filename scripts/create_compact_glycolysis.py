#!/usr/bin/env python3
"""
Create a compact, readable flowchart with better focus on the branch phase.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Set up the figure with compact layout
fig, ax = plt.subplots(1, 1, figsize=(8, 11), dpi=300)
ax.set_xlim(0, 8)
ax.set_ylim(0, 11)
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

# Define nodes with better spacing
nodes = [
    # (x, y, width, height, text_lines, fill_color, edge_color)
    (3, 9.5, 2, 0.6, ['Glucose Uptake', '(Transport into cell)'], colors['light_primary'], colors['primary']),
    (3, 8.7, 2, 0.6, ['Hexokinase', 'Glucose → G6P'], colors['light_primary'], colors['primary']),
    (3, 7.9, 2, 0.6, ['Isomerase', 'G6P → F6P'], colors['light_primary'], colors['primary']),
    (3, 7.1, 2, 0.6, ['Phosphofructokinase (PFK)', 'F6P → F1,6BP'], colors['light_primary'], colors['primary']),
    
    # Branch - more space around this section
    (1, 6, 1.8, 0.6, ['DHAP', '(Dihydroxyacetone', 'phosphate)'], colors['light_secondary'], colors['secondary']),
    (5, 6, 1.8, 0.6, ['G3P', '(Glyceraldehyde‑3‑', 'phosphate)'], colors['light_secondary'], colors['secondary']),
    
    # Continue from G3P - more space after branch
    (3, 4.8, 2, 0.6, ['G3P Oxidation & Phosphorylation', '(NADH + ATP yield)'], colors['light_primary'], colors['primary']),
    (3, 4, 2, 0.6, ['Phosphoglycerate Mutase & Enolase', '→ PEP'], colors['light_primary'], colors['primary']),
    (3, 3.2, 2, 0.6, ['Pyruvate Kinase', 'PEP → Pyruvate + ATP'], colors['light_primary'], colors['primary']),
    (3, 2.4, 2, 0.6, ['End Product:', '2 Pyruvate Molecules'], colors['light_success'], colors['success']),
]

# Draw nodes with smaller, more readable text
for x, y, w, h, text_lines, fill_color, edge_color in nodes:
    # Create rounded rectangle
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", 
                         facecolor=fill_color, edgecolor=edge_color, linewidth=1.5)
    ax.add_patch(box)
    
    # Add text with better sizing for readability
    for i, line in enumerate(text_lines):
        fontsize = 9 if len(text_lines) == 2 else 8
        ax.text(x + w/2, y + h - 0.05 - i*0.12, line, 
                ha='center', va='top', fontsize=fontsize, fontweight='bold',
                color=colors['text'])

# Define arrows with updated positions
arrows = [
    # Main vertical pathway
    ((4, 9.5), (4, 9.3)),      # Glucose Uptake to Hexokinase
    ((4, 8.7), (4, 8.5)),      # Hexokinase to Isomerase
    ((4, 7.9), (4, 7.7)),      # Isomerase to PFK
    
    # Branch from PFK - more visible
    ((3, 7.1), (1.9, 6.6)),    # PFK to DHAP
    ((3, 7.1), (5.1, 6.6)),    # PFK to G3P
    
    # TPI connections - more prominent and better spaced
    ((2.8, 6.3), (5.2, 6.3)),    # DHAP to G3P (TPI forward)
    ((5.2, 6.3), (2.8, 6.3)),    # G3P to DHAP (TPI reverse)
    
    # Continue from G3P
    ((5, 6), (4, 5.4)),        # G3P to Oxidation
    ((4, 4.8), (4, 4.6)),        # Oxidation to Mutase
    ((4, 4), (4, 3.8)),          # Mutase to Pyruvate Kinase
    ((4, 3.2), (4, 3)),          # Pyruvate Kinase to End Product
]

# Draw arrows
for start, end in arrows:
    arrow = FancyArrowPatch(start, end,
                          arrowstyle="->", shrinkA=3, shrinkB=3,
                          mutation_scale=15, fc=colors['arrow'], ec=colors['arrow'], 
                          linewidth=1.5)
    ax.add_patch(arrow)

# Add title with more space
ax.text(4, 10.3, 'Glycolysis Pathway in Yeast', ha='center', va='center', 
        fontsize=14, fontweight='bold', color=colors['primary'])

# Add TPI labels - better positioned with more space
ax.text(4, 6.1, 'TPI forward', ha='center', va='center', 
        fontsize=10, color=colors['primary'], fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.4", facecolor='white', alpha=0.95, edgecolor=colors['primary'], linewidth=1))
ax.text(4, 5.7, 'TPI reverse', ha='center', va='center', 
        fontsize=10, color=colors['primary'], fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.4", facecolor='white', alpha=0.95, edgecolor=colors['primary'], linewidth=1))

# Add phase labels - better positioned
ax.text(0.5, 6.6, 'Branch\nPhase', ha='center', va='center', 
        fontsize=10, fontweight='bold', color=colors['secondary'],
        bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['light_secondary'], alpha=0.8))

ax.text(6.5, 4.4, 'Payoff\nPhase', ha='center', va='center', 
        fontsize=10, fontweight='bold', color=colors['primary'],
        bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['light_primary'], alpha=0.8))

plt.tight_layout()
plt.savefig('glycolysis_flowchart_compact.svg', format='svg', bbox_inches='tight', dpi=300)
plt.savefig('glycolysis_flowchart_compact.png', format='png', bbox_inches='tight', dpi=300)
plt.close()

print("Compact flowchart created:")
print("- glycolysis_flowchart_compact.svg")
print("- glycolysis_flowchart_compact.png") 