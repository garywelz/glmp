#!/usr/bin/env python3
"""
Create simple placeholder images for missing GLMP paper figures.
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Set up output directory
output_dir = "docs/paper/figures"
os.makedirs(f"{output_dir}/modern", exist_ok=True)
os.makedirs(f"{output_dir}/contemporary", exist_ok=True)

def create_simple_circos():
    """Create a simple Circos placeholder."""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Create a simple circular layout
    circle = plt.Circle((0, 0), 1, fill=False, color='black', linewidth=2)
    ax.add_patch(circle)
    
    # Add some data points
    angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
    for angle in angles:
        x = 0.7 * np.cos(angle)
        y = 0.7 * np.sin(angle)
        ax.scatter(x, y, c='blue', s=50)
    
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Circos Genome Visualization (2009)\nMartin Krzywinski', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/modern/circos_2009.png', dpi=150, bbox_inches='tight')
    plt.close()

def create_simple_biomedical():
    """Create a simple biomedical data visualization."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create simple heatmap
    data = np.random.rand(10, 10)
    im = ax.imshow(data, cmap='viridis')
    
    ax.set_title('Biomedical Data Visualization (2018)\nO\'Donoghue et al.', fontsize=12, fontweight='bold')
    plt.colorbar(im)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/modern/odonoghue_2018.png', dpi=150, bbox_inches='tight')
    plt.close()

def create_simple_color_vision():
    """Create a simple color vision genetics placeholder."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create a simple pattern
    x = np.linspace(0, 10, 50)
    y = np.linspace(0, 6, 30)
    X, Y = np.meshgrid(x, y)
    pattern = np.sin(X) * np.cos(Y)
    
    im = ax.imshow(pattern, cmap='RdYlBu', extent=[0, 10, 0, 6])
    
    ax.set_title('Color Vision Genetics (2021)\nJacobs & Elmer', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/contemporary/color_vision_2021.png', dpi=150, bbox_inches='tight')
    plt.close()

def create_simple_networks():
    """Create a simple genetic networks placeholder."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create simple network
    np.random.seed(42)
    positions = np.random.rand(8, 2) * 6
    
    # Draw nodes
    ax.scatter(positions[:, 0], positions[:, 1], c='blue', s=100)
    
    # Draw some connections
    for i in range(8):
        for j in range(i+1, 8):
            if np.random.random() < 0.4:
                ax.plot([positions[i, 0], positions[j, 0]], 
                       [positions[i, 1], positions[j, 1]], 'r-', alpha=0.6)
    
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-0.5, 6.5)
    ax.set_title('Contemporary Genetic Networks (2024)\nMulti-scale Systems', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/contemporary/genetic_networks_2024.png', dpi=150, bbox_inches='tight')
    plt.close()

def main():
    """Generate all simple placeholder images."""
    print("Creating simple placeholder images...")
    
    create_simple_circos()
    print("✓ Created Circos placeholder")
    
    create_simple_biomedical()
    print("✓ Created biomedical visualization placeholder")
    
    create_simple_color_vision()
    print("✓ Created color vision genetics placeholder")
    
    create_simple_networks()
    print("✓ Created genetic networks placeholder")
    
    print("\nAll placeholder images created successfully!")

if __name__ == "__main__":
    main()