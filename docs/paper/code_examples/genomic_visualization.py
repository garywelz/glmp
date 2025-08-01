"""
Genomic Logic Visualization Examples for GLMP
Demonstrates how to visualize genetic circuits and computational biology data
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
import seaborn as sns

class GenomicVisualizer:
    """Tools for visualizing genomic logic and genetic circuits"""
    
    def __init__(self):
        self.colors = {
            'promoter': '#FFD700',      # Gold
            'operator': '#FF6B6B',      # Red
            'gene': '#4ECDC4',          # Teal
            'protein': '#45B7D1',       # Blue
            'metabolite': '#96CEB4',    # Green
            'inhibitor': '#FFEAA7',     # Yellow
            'activator': '#DDA0DD'      # Plum
        }
    
    def create_gene_network(self, genes, interactions):
        """Create a network visualization of gene interactions"""
        G = nx.DiGraph()
        
        # Add nodes (genes)
        for gene in genes:
            G.add_node(gene['name'], **gene)
        
        # Add edges (interactions)
        for interaction in interactions:
            G.add_edge(interaction['from'], interaction['to'], 
                      **interaction)
        
        return G
    
    def plot_gene_network(self, G, title="Gene Regulatory Network"):
        """Plot a gene regulatory network"""
        plt.figure(figsize=(12, 8))
        
        # Use spring layout for automatic positioning
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, 
                              node_color=[G.nodes[node].get('color', '#4ECDC4') 
                                        for node in G.nodes()],
                              node_size=2000,
                              alpha=0.8)
        
        # Draw edges with different styles for different interaction types
        edge_colors = []
        edge_styles = []
        
        for u, v, data in G.edges(data=True):
            interaction_type = data.get('type', 'regulation')
            if interaction_type == 'activation':
                edge_colors.append('#2ECC71')
                edge_styles.append('->')
            elif interaction_type == 'inhibition':
                edge_colors.append('#E74C3C')
                edge_styles.append('-|>')
            else:
                edge_colors.append('#95A5A6')
                edge_styles.append('->')
        
        nx.draw_networkx_edges(G, pos, 
                              edge_color=edge_colors,
                              arrows=True,
                              arrowsize=20,
                              arrowstyle='->',
                              width=2,
                              alpha=0.7)
        
        # Add labels
        nx.draw_networkx_labels(G, pos, 
                               font_size=10,
                               font_weight='bold')
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        return plt.gcf()
    
    def create_operon_diagram(self, operon_data):
        """Create a detailed operon diagram"""
        fig, ax = plt.subplots(figsize=(15, 6))
        
        # DNA backbone
        ax.plot([0, 14], [2, 2], 'k-', linewidth=3, label='DNA')
        
        # Draw regulatory elements and genes
        elements = operon_data['elements']
        y_pos = 2
        
        for i, element in enumerate(elements):
            x_start = element['position']
            width = element['width']
            element_type = element['type']
            name = element['name']
            
            # Choose color based on element type
            color = self.colors.get(element_type, '#95A5A6')
            
            # Draw element
            rect = Rectangle((x_start, y_pos - 0.3), width, 0.6, 
                           facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(rect)
            
            # Add label
            ax.text(x_start + width/2, y_pos + 0.8, name, 
                   ha='center', va='center', fontsize=10, fontweight='bold')
            
            # Add type label below
            ax.text(x_start + width/2, y_pos - 0.8, element_type, 
                   ha='center', va='center', fontsize=8, style='italic')
        
        # Draw regulatory proteins
        regulators = operon_data.get('regulators', [])
        for regulator in regulators:
            x_pos = regulator['position']
            protein_type = regulator['type']
            name = regulator['name']
            
            # Draw protein as circle
            circle = Circle((x_pos, y_pos + 2), 0.4, 
                          facecolor=self.colors.get(protein_type, '#95A5A6'),
                          edgecolor='black', linewidth=2)
            ax.add_patch(circle)
            
            # Add protein name
            ax.text(x_pos, y_pos + 2.8, name, 
                   ha='center', va='center', fontsize=9, fontweight='bold')
            
            # Draw connection line
            ax.plot([x_pos, x_pos], [y_pos + 1.6, y_pos + 0.3], 
                   'k--', linewidth=1, alpha=0.7)
        
        # Set plot properties
        ax.set_xlim(-1, 15)
        ax.set_ylim(0, 5)
        ax.set_title(operon_data['name'], fontsize=14, fontweight='bold')
        ax.axis('off')
        
        return fig
    
    def plot_expression_heatmap(self, expression_data, time_points, genes):
        """Create a heatmap of gene expression over time"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create heatmap
        sns.heatmap(expression_data, 
                   xticklabels=time_points,
                   yticklabels=genes,
                   cmap='viridis',
                   annot=True,
                   fmt='.2f',
                   cbar_kws={'label': 'Expression Level'})
        
        ax.set_xlabel('Time Points')
        ax.set_ylabel('Genes')
        ax.set_title('Gene Expression Heatmap Over Time')
        
        return fig
    
    def create_boolean_logic_diagram(self, logic_data):
        """Create a diagram showing Boolean logic in genetic circuits"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Draw logic gates
        gates = logic_data['gates']
        for gate in gates:
            x, y = gate['position']
            gate_type = gate['type']
            inputs = gate['inputs']
            output = gate['output']
            
            # Draw gate shape
            if gate_type == 'AND':
                # Draw AND gate (rounded rectangle)
                rect = FancyBboxPatch((x-0.5, y-0.3), 1, 0.6,
                                    boxstyle="round,pad=0.1",
                                    facecolor='lightblue',
                                    edgecolor='black',
                                    linewidth=2)
                ax.add_patch(rect)
                ax.text(x, y, 'AND', ha='center', va='center', fontweight='bold')
            
            elif gate_type == 'OR':
                # Draw OR gate (curved shape)
                rect = FancyBboxPatch((x-0.5, y-0.3), 1, 0.6,
                                    boxstyle="round,pad=0.1",
                                    facecolor='lightgreen',
                                    edgecolor='black',
                                    linewidth=2)
                ax.add_patch(rect)
                ax.text(x, y, 'OR', ha='center', va='center', fontweight='bold')
            
            elif gate_type == 'NOT':
                # Draw NOT gate (triangle)
                triangle = plt.Polygon([[x-0.3, y-0.3], [x+0.3, y], [x-0.3, y+0.3]],
                                     facecolor='lightcoral',
                                     edgecolor='black',
                                     linewidth=2)
                ax.add_patch(triangle)
                ax.text(x, y, 'NOT', ha='center', va='center', fontweight='bold')
            
            # Draw input connections
            for i, input_name in enumerate(inputs):
                input_x = x - 1.5
                input_y = y - 0.2 + i * 0.4
                ax.plot([input_x, x-0.5], [input_y, y], 'k-', linewidth=2)
                ax.text(input_x - 0.3, input_y, input_name, 
                       ha='right', va='center', fontweight='bold')
            
            # Draw output connection
            ax.plot([x+0.5, x+1.5], [y, y], 'k-', linewidth=2)
            ax.text(x + 1.8, y, output, ha='left', va='center', fontweight='bold')
        
        ax.set_xlim(-3, 4)
        ax.set_ylim(-1, 3)
        ax.set_title('Boolean Logic in Genetic Circuits')
        ax.axis('off')
        
        return fig

# Example usage
if __name__ == "__main__":
    print("=== Genomic Visualization Examples ===\n")
    
    visualizer = GenomicVisualizer()
    
    # Example 1: Gene Regulatory Network
    print("1. Creating gene regulatory network...")
    genes = [
        {'name': 'lacI', 'color': '#FFD700'},
        {'name': 'lacZ', 'color': '#4ECDC4'},
        {'name': 'lacY', 'color': '#4ECDC4'},
        {'name': 'lacA', 'color': '#4ECDC4'},
        {'name': 'CAP', 'color': '#45B7D1'}
    ]
    
    interactions = [
        {'from': 'lacI', 'to': 'lacZ', 'type': 'inhibition'},
        {'from': 'lacI', 'to': 'lacY', 'type': 'inhibition'},
        {'from': 'lacI', 'to': 'lacA', 'type': 'inhibition'},
        {'from': 'CAP', 'to': 'lacZ', 'type': 'activation'},
        {'from': 'CAP', 'to': 'lacY', 'type': 'activation'},
        {'from': 'CAP', 'to': 'lacA', 'type': 'activation'}
    ]
    
    G = visualizer.create_gene_network(genes, interactions)
    fig1 = visualizer.plot_gene_network(G, "Lac Operon Regulatory Network")
    plt.savefig('lac_operon_network.png', dpi=150, bbox_inches='tight')
    print("   Network saved as 'lac_operon_network.png'")
    
    # Example 2: Operon Diagram
    print("\n2. Creating operon diagram...")
    operon_data = {
        'name': 'Lac Operon Structure',
        'elements': [
            {'name': 'lacI', 'type': 'gene', 'position': 1, 'width': 1},
            {'name': 'P', 'type': 'promoter', 'position': 3, 'width': 0.5},
            {'name': 'O', 'type': 'operator', 'position': 3.5, 'width': 0.5},
            {'name': 'lacZ', 'type': 'gene', 'position': 4.5, 'width': 1.5},
            {'name': 'lacY', 'type': 'gene', 'position': 6.5, 'width': 1},
            {'name': 'lacA', 'type': 'gene', 'position': 8, 'width': 1}
        ],
        'regulators': [
            {'name': 'Repressor', 'type': 'inhibitor', 'position': 3.75},
            {'name': 'CAP', 'type': 'activator', 'position': 3.25}
        ]
    }
    
    fig2 = visualizer.create_operon_diagram(operon_data)
    plt.savefig('lac_operon_diagram.png', dpi=150, bbox_inches='tight')
    print("   Diagram saved as 'lac_operon_diagram.png'")
    
    # Example 3: Expression Heatmap
    print("\n3. Creating expression heatmap...")
    # Simulate expression data
    time_points = ['T0', 'T1', 'T2', 'T3', 'T4']
    genes = ['lacZ', 'lacY', 'lacA']
    expression_data = np.random.rand(len(genes), len(time_points))
    
    fig3 = visualizer.plot_expression_heatmap(expression_data, time_points, genes)
    plt.savefig('expression_heatmap.png', dpi=150, bbox_inches='tight')
    print("   Heatmap saved as 'expression_heatmap.png'")
    
    print("\n=== Visualization Examples Complete ===") 