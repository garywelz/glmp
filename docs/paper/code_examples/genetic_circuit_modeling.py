"""
Genetic Circuit Modeling Examples for GLMP
Demonstrates how to model biological logic as computational circuits
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

class GeneticCircuit:
    """Base class for modeling genetic circuits as computational logic"""
    
    def __init__(self, name: str, inputs: List[str], outputs: List[str]):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.state = {input_name: 0.0 for input_name in inputs}
        self.output_state = {output_name: 0.0 for output_name in outputs}
    
    def update_state(self, input_values: Dict[str, float]):
        """Update circuit state based on input values"""
        for input_name, value in input_values.items():
            if input_name in self.inputs:
                self.state[input_name] = value
    
    def compute_outputs(self) -> Dict[str, float]:
        """Compute output values based on current state"""
        raise NotImplementedError("Subclasses must implement compute_outputs")
    
    def simulate(self, input_sequence: List[Dict[str, float]]) -> List[Dict[str, float]]:
        """Simulate circuit behavior over time"""
        results = []
        for inputs in input_sequence:
            self.update_state(inputs)
            outputs = self.compute_outputs()
            results.append({**self.state.copy(), **outputs})
        return results

class LacOperonCircuit(GeneticCircuit):
    """Implementation of the Lac Operon as a genetic circuit"""
    
    def __init__(self):
        super().__init__(
            name="Lac Operon",
            inputs=["lactose", "glucose"],
            outputs=["beta_galactosidase", "lac_permease", "transacetylase"]
        )
        # Threshold values for activation
        self.lactose_threshold = 0.5
        self.glucose_threshold = 0.3
    
    def compute_outputs(self) -> Dict[str, float]:
        """Lac operon logic: (lactose present) AND (glucose absent)"""
        lactose_present = self.state["lactose"] > self.lactose_threshold
        glucose_absent = self.state["glucose"] < self.glucose_threshold
        
        # Boolean logic: expression = lactose_present AND glucose_absent
        expression_level = 1.0 if (lactose_present and glucose_absent) else 0.0
        
        return {
            "beta_galactosidase": expression_level,
            "lac_permease": expression_level,
            "transacetylase": expression_level
        }

class PunnettSquareCalculator:
    """Computational implementation of Mendelian inheritance"""
    
    def __init__(self):
        self.dominance_rules = {
            "A": "dominant",
            "a": "recessive"
        }
    
    def calculate_genotypes(self, parent1: str, parent2: str) -> Dict[str, float]:
        """Calculate genotype probabilities for a monohybrid cross"""
        alleles1 = list(parent1)
        alleles2 = list(parent2)
        
        genotypes = {}
        for allele1 in alleles1:
            for allele2 in alleles2:
                # Sort alleles alphabetically for consistent genotype notation
                genotype = ''.join(sorted([allele1, allele2]))
                genotypes[genotype] = genotypes.get(genotype, 0) + 1
        
        # Convert counts to probabilities
        total = sum(genotypes.values())
        return {genotype: count/total for genotype, count in genotypes.items()}
    
    def calculate_phenotypes(self, genotypes: Dict[str, float]) -> Dict[str, float]:
        """Calculate phenotype probabilities based on dominance rules"""
        phenotypes = {"dominant": 0.0, "recessive": 0.0}
        
        for genotype, probability in genotypes.items():
            if "A" in genotype:  # Has dominant allele
                phenotypes["dominant"] += probability
            else:  # aa genotype
                phenotypes["recessive"] += probability
        
        return phenotypes

def visualize_circuit_behavior(circuit: GeneticCircuit, time_steps: int = 10):
    """Create a visualization of circuit behavior over time"""
    # Generate test input sequence
    input_sequence = []
    for t in range(time_steps):
        # Simulate varying lactose and glucose levels
        lactose = np.sin(t * 0.5) * 0.5 + 0.5  # Varying between 0 and 1
        glucose = np.cos(t * 0.3) * 0.5 + 0.5   # Varying between 0 and 1
        input_sequence.append({"lactose": lactose, "glucose": glucose})
    
    # Run simulation
    results = circuit.simulate(input_sequence)
    
    # Create visualization
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    
    # Plot inputs
    time_points = range(len(results))
    axes[0].plot(time_points, [r["lactose"] for r in results], 'b-', label='Lactose', linewidth=2)
    axes[0].plot(time_points, [r["glucose"] for r in results], 'r-', label='Glucose', linewidth=2)
    axes[0].set_ylabel('Concentration')
    axes[0].set_title('Input Signals')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot outputs
    axes[1].plot(time_points, [r["beta_galactosidase"] for r in results], 'g-', 
                label='β-galactosidase', linewidth=2)
    axes[1].set_xlabel('Time Steps')
    axes[1].set_ylabel('Expression Level')
    axes[1].set_title('Gene Expression Output')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

# Example usage and demonstration
if __name__ == "__main__":
    print("=== Genetic Circuit Modeling Examples ===\n")
    
    # Example 1: Lac Operon Circuit
    print("1. Lac Operon Circuit Simulation:")
    lac_circuit = LacOperonCircuit()
    
    # Test different input conditions
    test_conditions = [
        {"lactose": 0.0, "glucose": 1.0},  # No lactose, high glucose
        {"lactose": 1.0, "glucose": 1.0},  # High lactose, high glucose  
        {"lactose": 1.0, "glucose": 0.0},  # High lactose, no glucose
    ]
    
    for i, condition in enumerate(test_conditions):
        lac_circuit.update_state(condition)
        outputs = lac_circuit.compute_outputs()
        print(f"   Condition {i+1}: {condition}")
        print(f"   Output: β-galactosidase = {outputs['beta_galactosidase']:.2f}\n")
    
    # Example 2: Punnett Square Calculator
    print("2. Mendelian Inheritance Calculator:")
    punnett = PunnettSquareCalculator()
    
    # Monohybrid cross: Aa × Aa
    genotypes = punnett.calculate_genotypes("Aa", "Aa")
    phenotypes = punnett.calculate_phenotypes(genotypes)
    
    print(f"   Genotypes: {genotypes}")
    print(f"   Phenotypes: {phenotypes}")
    print(f"   Expected ratio: 3:1 (dominant:recessive)\n")
    
    # Example 3: Circuit Visualization
    print("3. Generating circuit behavior visualization...")
    fig = visualize_circuit_behavior(lac_circuit)
    plt.savefig('lac_operon_simulation.png', dpi=150, bbox_inches='tight')
    print("   Visualization saved as 'lac_operon_simulation.png'")
    
    print("\n=== End of Examples ===") 