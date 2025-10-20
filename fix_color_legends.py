#!/usr/bin/env python3
"""
Fix Color Legends in All Process Files
=======================================
Updates the colorScheme field to reflect the new Phase 2 colors
"""

import json
from pathlib import Path

# New color scheme (Phase 2)
NEW_COLOR_SCHEME = {
    "green": {
        "hex": "#51cf66",
        "category": "Triggers & Environmental Signals",
        "description": "External signals, stress conditions, nutrient availability, cell states"
    },
    "amber": {
        "hex": "#fab005",
        "category": "Enzymes & Catalysts",
        "description": "Protein enzymes, regulatory complexes, molecular machines"
    },
    "skyblue": {
        "hex": "#74c0fc",
        "category": "Processing & Operations",
        "description": "Biochemical reactions, signal transduction, molecular transformations"
    },
    "salmon": {
        "hex": "#ffa07a",
        "category": "Intermediates & Metabolites",
        "description": "Chemical intermediates, signaling molecules, transient states"
    },
    "orange": {
        "hex": "#ff9f43",
        "category": "OR Logic Gates",
        "description": "Decision points with multiple alternative branches"
    },
    "purple": {
        "hex": "#7950f2",
        "category": "AND Logic Gates",
        "description": "Multi-signal integration requiring all conditions"
    },
    "red": {
        "hex": "#e74c3c",
        "category": "NOT Gates & Repression",
        "description": "Inhibition, blocking, inactivation, repression mechanisms"
    },
    "black": {
        "hex": "#000000",
        "category": "Products & Outcomes",
        "description": "Final products, cellular outcomes, system states"
    }
}

def update_color_legend(json_path: Path) -> bool:
    """Update color legend in a process file"""
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Update colorScheme
        data['colorScheme'] = NEW_COLOR_SCHEME
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        print(f"Error updating {json_path}: {e}")
        return False

def main():
    """Main execution"""
    
    print("=" * 70)
    print("📋 FIXING COLOR LEGENDS")
    print("=" * 70)
    print()
    print("Updating colorScheme field in all process files...")
    print()
    
    # Find all process files
    gcs_dir = Path('/workspace/gcs-processes')
    json_files = list(gcs_dir.rglob('*.json'))
    
    updated = 0
    failed = 0
    
    for json_file in sorted(json_files):
        rel_path = json_file.relative_to(gcs_dir)
        if update_color_legend(json_file):
            print(f"✓ {rel_path}")
            updated += 1
        else:
            print(f"✗ {rel_path}")
            failed += 1
    
    # Summary
    print()
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"  Updated: {updated}")
    print(f"  Failed:  {failed}")
    print()
    
    if failed == 0:
        print("✅ All color legends updated!")
        print()
        print("New legend:")
        for key, val in NEW_COLOR_SCHEME.items():
            print(f"  {val['hex']} - {val['category']}")
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
