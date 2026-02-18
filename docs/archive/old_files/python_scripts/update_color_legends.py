#!/usr/bin/env python3
"""
Update colorScheme legends in all process JSON files
To reflect new semantic color scheme with NOT gates and black products
"""

import json
from glob import glob

# New color scheme legend
NEW_COLOR_SCHEME = {
    "green": {
        "hex": "#51cf66",
        "category": "Environmental Triggers",
        "description": "External signals, nutrient availability, environmental conditions, initial states"
    },
    "amber": {
        "hex": "#fab005",
        "category": "Enzymes & Proteins",
        "description": "Catalysts, regulatory proteins, molecular machines, receptors"
    },
    "skyBlue": {
        "hex": "#74c0fc",
        "category": "Processing & Operations",
        "description": "Biochemical reactions, transport, modifications, transcription, translation"
    },
    "salmon": {
        "hex": "#ffa07a",
        "category": "Intermediates & States",
        "description": "Metabolites, molecular complexes, cellular states, compounds"
    },
    "orange": {
        "hex": "#ff9f43",
        "category": "OR Logic Gates",
        "description": "Decision points with alternative pathways (yes/no branching)"
    },
    "purple": {
        "hex": "#7950f2",
        "category": "AND Logic Gates",
        "description": "Multi-component requirements, signal integration, convergence points"
    },
    "red": {
        "hex": "#e74c3c",
        "category": "NOT Logic Gates",
        "description": "Repression, inhibition, blocking, negative regulation"
    },
    "black": {
        "hex": "#000000",
        "category": "Final Products & Outcomes",
        "description": "Terminal products, cellular outcomes, equilibrium states, system endpoints"
    }
}

# Process all JSON files
files = glob('gcs-processes/*/*.json')
updated = 0

for filepath in files:
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Update colorScheme
        data['colorScheme'] = NEW_COLOR_SCHEME
        
        # Write back
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        updated += 1
        print(f"✓ Updated: {filepath}")
        
    except Exception as e:
        print(f"✗ Error: {filepath}: {e}")

print()
print("=" * 80)
print(f"✅ Updated {updated} process files with new color legend")
print("=" * 80)

