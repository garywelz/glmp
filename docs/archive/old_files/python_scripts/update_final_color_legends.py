#!/usr/bin/env python3
"""
Update colorScheme legends with FINAL refined colors
"""

import json
from glob import glob

# FINAL COLOR SCHEME METADATA
FINAL_COLOR_SCHEME = {
    "green": {
        "hex": "#51cf66",
        "category": "Environmental Triggers",
        "description": "External signals, nutrient availability, environmental conditions, initial states"
    },
    "amber": {
        "hex": "#ffa726",
        "category": "Enzymes & Proteins",
        "description": "Catalysts, regulatory proteins, molecular machines, receptors"
    },
    "darkSkyBlue": {
        "hex": "#42a5f5",
        "category": "Processing & Operations",
        "description": "Biochemical reactions, transport, modifications, transcription, translation"
    },
    "lightCyan": {
        "hex": "#b3e5fc",
        "category": "Intermediates & States",
        "description": "Metabolites, molecular complexes, cellular states, compounds"
    },
    "yellow": {
        "hex": "#ffd600",
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

print("🎨 UPDATING COLOR LEGENDS")
print("=" * 80)
print()

files = glob('gcs-processes/*/*.json')
updated = 0

for filepath in files:
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Update colorScheme
        data['colorScheme'] = FINAL_COLOR_SCHEME
        
        # Write back
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        updated += 1
        print(f"✓ {data['id']}")
        
    except Exception as e:
        print(f"✗ Error: {filepath}: {e}")

print()
print("=" * 80)
print(f"✅ Updated {updated} process files with final color legend")
print("=" * 80)

