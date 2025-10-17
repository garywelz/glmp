#!/usr/bin/env python3
"""
Rebuild metadata.json to include all 100 processes
Scans all JSON files in gcs-processes/ and builds complete metadata
"""

import json
import os
from pathlib import Path
from collections import defaultdict

def scan_processes():
    """Scan all process JSON files and extract metadata"""
    processes = []
    base_dir = Path('/workspace/gcs-processes')
    
    # Track counts
    organism_counts = defaultdict(int)
    category_counts = defaultdict(int)
    total_citations = 0
    total_nodes = 0
    total_or_gates = 0
    total_and_gates = 0
    verified_count = 0
    
    # Scan all organisms
    for organism_dir in ['ecoli', 'yeast', 'bacillus']:
        organism_path = base_dir / organism_dir
        if not organism_path.exists():
            continue
            
        for json_file in sorted(organism_path.glob('*.json')):
            if json_file.name == 'metadata.json':
                continue
                
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                # Extract process info with full logic gate breakdown
                logic_gates = data["complexity"]["logicGates"]
                process_entry = {
                    "id": data["id"],
                    "name": data["name"],
                    "organism": data["organism"],
                    "category": data["category"],
                    "nodes": data["complexity"]["nodes"],
                    "logicGates": {
                        "or": logic_gates.get("orGates", 0),
                        "and": logic_gates.get("andGates", 0),
                        "total": logic_gates.get("total", 0)
                    },
                    "verified": data.get("verified", False),
                    "created": data.get("created", "2025-10-15")
                }
                
                processes.append(process_entry)
                
                # Update counts
                organism_counts[data["organism"]] += 1
                category_counts[data["category"]] += 1
                total_citations += len(data.get("sources", []))
                total_nodes += data["complexity"]["nodes"]
                total_or_gates += data["complexity"]["logicGates"].get("orGates", 0)
                total_and_gates += data["complexity"]["logicGates"].get("andGates", 0)
                if data.get("verified", False):
                    verified_count += 1
                    
                print(f"✓ {data['id']}")
                
            except Exception as e:
                print(f"✗ Error reading {json_file.name}: {e}")
    
    return processes, {
        'organism_counts': organism_counts,
        'category_counts': category_counts,
        'total_citations': total_citations,
        'total_nodes': total_nodes,
        'total_or_gates': total_or_gates,
        'total_and_gates': total_and_gates,
        'verified_count': verified_count
    }

def build_metadata(processes, stats):
    """Build complete metadata.json structure"""
    
    # Map organism names to standardized format
    organism_map = {
        "E. coli": "E. coli",
        "S. cerevisiae": "S. cerevisiae",
        "Bacillus subtilis": "B. subtilis"
    }
    
    # Build organisms array
    organisms = []
    for org_name, count in stats['organism_counts'].items():
        standardized_name = organism_map.get(org_name, org_name)
        organisms.append({
            "name": standardized_name,
            "processCount": count
        })
    
    # Build categories array
    categories = []
    for cat_name, count in stats['category_counts'].items():
        categories.append({
            "name": cat_name,
            "processCount": count
        })
    
    # Sort
    organisms.sort(key=lambda x: x['processCount'], reverse=True)
    categories.sort(key=lambda x: x['processCount'], reverse=True)
    processes.sort(key=lambda x: (x['organism'], x['id']))
    
    metadata = {
        "version": "2.0",
        "generated": "2025-10-15",
        "totalProcesses": len(processes),
        "lastUpdated": "2025-10-15",
        "description": "GLMP v2: Genome Logic Modeling Project with 100 publication-quality biological processes",
        "organisms": organisms,
        "categories": categories,
        "statistics": {
            "totalCitations": stats['total_citations'],
            "verifiedProcesses": stats['verified_count'],
            "totalNodes": stats['total_nodes'],
            "totalLogicGates": stats['total_or_gates'] + stats['total_and_gates'],
            "orGates": stats['total_or_gates'],
            "andGates": stats['total_and_gates'],
            "orAndRatio": round(stats['total_or_gates'] / stats['total_and_gates'], 2) if stats['total_and_gates'] > 0 else 0
        },
        "processes": processes
    }
    
    return metadata

def main():
    print("🔄 Rebuilding metadata.json for 100 processes...\n")
    
    # Scan all processes
    processes, stats = scan_processes()
    
    print(f"\n📊 Found {len(processes)} processes!")
    print(f"   E. coli: {stats['organism_counts'].get('E. coli', 0)}")
    print(f"   S. cerevisiae: {stats['organism_counts'].get('S. cerevisiae', 0)}")
    print(f"   Bacillus subtilis: {stats['organism_counts'].get('Bacillus subtilis', 0)}")
    print(f"\n   Total nodes: {stats['total_nodes']}")
    print(f"   OR gates: {stats['total_or_gates']}")
    print(f"   AND gates: {stats['total_and_gates']}")
    print(f"   OR:AND ratio: {stats['total_or_gates'] / stats['total_and_gates']:.2f}" if stats['total_and_gates'] > 0 else "   OR:AND ratio: N/A")
    
    # Build metadata
    metadata = build_metadata(processes, stats)
    
    # Save to both locations
    output_paths = [
        '/workspace/gcs-processes/metadata.json',
        '/workspace/metadata_100_complete.json'
    ]
    
    for output_path in output_paths:
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"\n✅ Saved to: {output_path}")
    
    print("\n🎉 Metadata rebuild complete!")
    print(f"   Total processes in array: {len(metadata['processes'])}")
    print("\nNext step: Upload to GCS with:")
    print("   gsutil cp metadata_100_complete.json gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/data/metadata.json")

if __name__ == '__main__':
    main()
