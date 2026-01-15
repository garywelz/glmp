#!/usr/bin/env python3
"""
Create metadata.json with 108 processes and correct statistics
"""

import json
import os
from datetime import datetime

# Correct statistics from PHASE1_COMPLETE_SUMMARY.md
CORRECT_STATS = {
    "totalProcesses": 108,
    "organisms": [
        {"name": "E. coli", "processCount": 64},
        {"name": "S. cerevisiae", "processCount": 44}
    ],
    "logicGates": {
        "OR": 636,
        "AND": 352, 
        "NOT": 129,
        "total": 1117
    },
    "architecture": "100:11:6:2",
    "totalNodes": 7152,
    "avgNodes": 66.2,
    "avgGates": 10.3
}

def create_metadata():
    """Create metadata.json with correct 108 process statistics"""
    
    metadata = {
        "name": "GLMP Process Collection",
        "version": "2.1.0",
        "generated": datetime.now().isoformat(),
        "lastUpdated": "2025-10-21",
        "totalProcesses": CORRECT_STATS["totalProcesses"],
        "description": "GLMP v2.1: Genome Logic Modeling Project with 108 publication-quality biological processes",
        "organisms": CORRECT_STATS["organisms"],
        "statistics": {
            "totalProcesses": CORRECT_STATS["totalProcesses"],
            "totalNodes": CORRECT_STATS["totalNodes"],
            "avgNodes": CORRECT_STATS["avgNodes"],
            "logicGates": CORRECT_STATS["logicGates"],
            "architecture": CORRECT_STATS["architecture"],
            "avgGates": CORRECT_STATS["avgGates"]
        },
        "processes": []  # Empty for now - would need to populate from actual process files
    }
    
    return metadata

def main():
    print("🔧 Creating metadata.json with 108 processes...")
    
    metadata = create_metadata()
    
    # Write to glmp-v2/data/metadata.json
    output_path = "glmp-v2/data/metadata.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Created {output_path}")
    print(f"   Total Processes: {metadata['totalProcesses']}")
    print(f"   Logic Gates: OR={metadata['statistics']['logicGates']['OR']}, AND={metadata['statistics']['logicGates']['AND']}, NOT={metadata['statistics']['logicGates']['NOT']}")
    print(f"   Architecture: {metadata['statistics']['architecture']}")

if __name__ == "__main__":
    main()
