#!/usr/bin/env python3
"""
Create placeholder images for the GLMP paper figures that are missing.
This script generates professional-looking placeholder images for academic figures.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import FancyBboxPatch
import os

# Set up the output directory
output_dir = "docs/paper/figures"
os.makedirs(f"{output_dir}/modern", exist_ok=True)
os.makedirs(f"{output_dir}/contemporary", exist_ok=True)

# Set style for academic figures
plt.style.use('default')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['axes.edgecolor'] = '#333333'

def create_circos_placeholder():
    """Create a placeholder for Circos genome visualization."""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    
    # Create circular layout
    circle = plt.Circle((0, 0), 1, fill=False, color='#2c3e50', linewidth=2)
    ax.add_patch(circle)
    
    # Add concentric circles for different data types
    for radius in [0.3, 0.6, 0.9]:
        circle = plt.Circle((0, 0), radius, fill=False, color='#7f8c8d', linewidth=1, alpha=0.5)
        ax.add_patch(circle)
    
    # Add some data points around the circle
    angles = np.linspace(0, 2*np.pi, 12, endpoint=False)
    for i, angle in enumerate(angles):
        x = 0.8 * np.cos(angle)
        y = 0.8 * np.sin(angle)
        ax.scatter(x, y, c='#3498db', s=50, alpha=0.7)
        
        # Add connecting lines
        if i < len(angles) - 1:
            next_angle = angles[i + 1]
            x2 = 0.8 * np.cos(next_angle)
            y2 = 0.8 * np.sin(next_angle)
            ax.plot([x, x2], [y, y2], color='#e74c3c', alpha=0.6, linewidth=1)
    
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Circos Genome Visualization (2009)\nMartin Krzywinski', 
                 fontsize=12, fontweight='bold', pad=20)
    
    # Add description
    ax.text(0, -1.1, 'Circular layout for comparative genomics\nshowing complex genomic relationships', 
            ha='center', va='center', fontsize=9, style='italic')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/modern/circos_2009.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_phylogenetic_placeholder():
    """Create a placeholder for Höhna's probabilistic phylogenetic networks."""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create a tree-like structure
    def draw_tree(x, y, length, angle, depth):
        if depth > 4:
            return
        
        end_x = x + length * np.cos(angle)
        end_y = y + length * np.sin(angle)
        
        # Draw branch
        ax.plot([x, end_x], [y, end_y], color='#2c3e50', linewidth=2)
        
        # Add uncertainty bands
        uncertainty = 0.1
        ax.fill_between([x, end_x], 
                       [y - uncertainty, end_y - uncertainty],
                       [y + uncertainty, end_y + uncertainty],
                       alpha=0.2, color='#3498db')
        
        # Recursive calls for branches
        if depth < 3:
            draw_tree(end_x, end_y, length * 0.7, angle + 0.5, depth + 1)
            draw_tree(end_x, end_y, length * 0.7, angle - 0.5, depth + 1)
        else:
            # Add leaf nodes
            ax.scatter(end_x, end_y, c='#e74c3c', s=30)
    
    # Start the tree
    draw_tree(0, 0, 2, np.pi/2, 0)
    
    ax.set_xlim(-3, 3)
    ax.set_ylim(-0.5, 4)
    ax.axis('off')
    ax.set_title('Probabilistic Phylogenetic Networks (2014)\nHöhna et al.', 
                 fontsize=12, fontweight='bold', pad=20)
    
    # Add description
    ax.text(0, -0.3, 'Probabilistic graphical models showing\nevolutionary relationships with uncertainty', 
            ha='center', va='center', fontsize=9, style='italic')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/modern/hohna_2014.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_network_placeholder():
    """Create a placeholder for Koutrouli's network visualizations."""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create a network of nodes
    np.random.seed(42)
    n_nodes = 15
    positions = np.random.rand(n_nodes, 2) * 8
    
    # Draw nodes
    for i in range(n_nodes):
        ax.scatter(positions[i, 0], positions[i, 1], 
                  c='#3498db', s=100, alpha=0.8, edgecolors='#2c3e50', linewidth=1)
        ax.text(positions[i, 0], positions[i, 1], f'G{i+1}', 
                ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Draw edges (connections)
    for i in range(n_nodes):
        for j in range(i+1, n_nodes):
            if np.random.random() < 0.3:  # 30% chance of connection
                ax.plot([positions[i, 0], positions[j, 0]], 
                       [positions[i, 1], positions[j, 1]], 
                       color='#e74c3c', alpha=0.6, linewidth=1)
    
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(-0.5, 8.5)
    ax.axis('off')
    ax.set_title('Biological Network Visualization (2020)\nKoutrouli et al.', 
                 fontsize=12, fontweight='bold', pad=20)
    
    # Add description
    ax.text(4, -0.3, 'Gene interaction networks showing\nregulatory relationships and pathways', 
            ha='center', va='center', fontsize=9, style='italic')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/modern/koutrouli_2020.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_biomedical_placeholder():
    """Create a placeholder for O'Donoghue's biomedical data visualization."""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create a heatmap-like visualization
    data = np.random.rand(20, 20)
    # Add some structure to make it look more realistic
    for i in range(20):
        for j in range(20):
            data[i, j] += 0.5 * np.exp(-((i-10)**2 + (j-10)**2) / 50)
    
    im = ax.imshow(data, cmap='viridis', aspect='auto')
    
    # Add some annotations
    ax.set_xticks([0, 5, 10, 15, 19])
    ax.set_xticklabels(['Gene A', 'Gene B', 'Gene C', 'Gene D', 'Gene E'])
    ax.set_yticks([0, 5, 10, 15, 19])
    ax.set_yticklabels(['Sample 1', 'Sample 2', 'Sample 3', 'Sample 4', 'Sample 5'])
    
    # Rotate x-axis labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    
    ax.set_title('Biomedical Data Visualization (2018)\nO\'Donoghue et al.', 
                 fontsize=12, fontweight='bold', pad=20)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Expression Level', rotation=270, labelpad=15)
    
    # Add description
    ax.text(10, -1.5, 'Multi-dimensional biomedical data\nshowing gene expression patterns', 
            ha='center', va='center', fontsize=9, style='italic')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/modern/odonoghue_2018.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_color_vision_placeholder():
    """Create a placeholder for color vision genetics."""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create a color vision test-like pattern
    # Simulate different color perception patterns
    x = np.linspace(0, 10, 100)
    y = np.linspace(0, 8, 80)
    X, Y = np.meshgrid(x, y)
    
    # Create a pattern that simulates color vision differences
    pattern = np.sin(X) * np.cos(Y) + 0.5 * np.sin(2*X) * np.cos(2*Y)
    
    im = ax.imshow(pattern, cmap='RdYlBu', extent=[0, 10, 0, 8], aspect='auto')
    
    # Add some genetic markers
    marker_positions = [(2, 2), (5, 3), (8, 6), (3, 7)]
    for pos in marker_positions:
        ax.scatter(pos[0], pos[1], c='red', s=100, marker='o', edgecolors='black', linewidth=2)
        ax.text(pos[0], pos[1], 'G', ha='center', va='center', fontsize=12, fontweight='bold', color='white')
    
    ax.set_title('Color Vision Genetics (2021)\nJacobs & Elmer', 
                 fontsize=12, fontweight='bold', pad=20)
    
    # Add description
    ax.text(5, -0.5, 'Genetic basis of color vision differences\nshowing gene variants and phenotypes', 
            ha='center', va='center', fontsize=9, style='italic')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/contemporary/color_vision_2021.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_genetic_networks_placeholder():
    """Create a placeholder for contemporary genetic networks."""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create a more complex network with different node types
    np.random.seed(123)
    n_genes = 12
    n_proteins = 8
    n_metabolites = 6
    
    # Position genes
    gene_positions = np.random.rand(n_genes, 2) * 8
    # Position proteins
    protein_positions = np.random.rand(n_proteins, 2) * 8
    # Position metabolites
    metabolite_positions = np.random.rand(n_metabolites, 2) * 8
    
    # Draw genes (blue circles)
    for i in range(n_genes):
        ax.scatter(gene_positions[i, 0], gene_positions[i, 1], 
                  c='#3498db', s=120, alpha=0.8, edgecolors='#2c3e50', linewidth=2)
        ax.text(gene_positions[i, 0], gene_positions[i, 1], f'G{i+1}', 
                ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    
    # Draw proteins (red squares)
    for i in range(n_proteins):
        ax.scatter(protein_positions[i, 0], protein_positions[i, 1], 
                  c='#e74c3c', s=100, alpha=0.8, edgecolors='#2c3e50', linewidth=2, marker='s')
        ax.text(protein_positions[i, 0], protein_positions[i, 1], f'P{i+1}', 
                ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    
    # Draw metabolites (green triangles)
    for i in range(n_metabolites):
        ax.scatter(metabolite_positions[i, 0], metabolite_positions[i, 1], 
                  c='#27ae60', s=80, alpha=0.8, edgecolors='#2c3e50', linewidth=2, marker='^')
        ax.text(metabolite_positions[i, 0], metabolite_positions[i, 1], f'M{i+1}', 
                ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    
    # Draw connections
    all_positions = np.vstack([gene_positions, protein_positions, metabolite_positions])
    for i in range(len(all_positions)):
        for j in range(i+1, len(all_positions)):
            if np.random.random() < 0.25:  # 25% chance of connection
                ax.plot([all_positions[i, 0], all_positions[j, 0]], 
                       [all_positions[i, 1], all_positions[j, 1]], 
                       color='#7f8c8d', alpha=0.5, linewidth=1)
    
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(-0.5, 8.5)
    ax.axis('off')
    ax.set_title('Contemporary Genetic Networks (2024)\nMulti-scale Biological Systems', 
                 fontsize=12, fontweight='bold', pad=20)
    
    # Add legend
    ax.scatter([], [], c='#3498db', s=100, label='Genes')
    ax.scatter([], [], c='#e74c3c', s=100, marker='s', label='Proteins')
    ax.scatter([], [], c='#27ae60', s=100, marker='^', label='Metabolites')
    ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
    
    # Add description
    ax.text(4, -0.3, 'Multi-scale biological networks integrating\ngenes, proteins, and metabolic pathways', 
            ha='center', va='center', fontsize=9, style='italic')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/contemporary/genetic_networks_2024.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Generate all placeholder images."""
    print("Creating placeholder images for GLMP paper...")
    
    create_circos_placeholder()
    print("✓ Created Circos placeholder")
    
    create_phylogenetic_placeholder()
    print("✓ Created phylogenetic networks placeholder")
    
    create_network_placeholder()
    print("✓ Created network visualization placeholder")
    
    create_biomedical_placeholder()
    print("✓ Created biomedical data visualization placeholder")
    
    create_color_vision_placeholder()
    print("✓ Created color vision genetics placeholder")
    
    create_genetic_networks_placeholder()
    print("✓ Created contemporary genetic networks placeholder")
    
    print("\nAll placeholder images created successfully!")
    print(f"Images saved in: {output_dir}/modern/ and {output_dir}/contemporary/")

if __name__ == "__main__":
    main()