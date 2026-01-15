#!/usr/bin/env python3
"""
Rebuild metadata.json to include all 108 processes
Scans all JSON files in gcs-processes/ and builds complete metadata
"""

import json
import os
from pathlib import Path
from collections import defaultdict

def scan_processes():
    """Scan all process JSON files and extract metadata"""
    processes = []
    base_dir = Path('/home/gdubs/glmp/gcs-processes')
    
    # Track counts
    organism_counts = defaultdict(int)
    category_counts = defaultdict(int)
    total_citations = 0
    total_nodes = 0
    total_or_gates = 0
    total_and_gates = 0
    total_not_gates = 0
    verified_count = 0
    
    # Scan all organisms
    for organism_dir in ['ecoli', 'yeast', 'bacillus']:
        organism_path = base_dir / organism_dir
        if not organism_path.exists():
            continue
            
        print(f"Scanning {organism_dir}...")
        
        for json_file in organism_path.glob('*.json'):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                # Extract metadata
                complexity = data.get('complexity', {})
                logic_gates = complexity.get('logicGates', {})
                
                process_info = {
                    'id': data.get('id', json_file.stem),
                    'name': data.get('name', 'Unknown Process'),
                    'organism': data.get('organism', organism_dir.title()),
                    'category': data.get('category', 'Unknown'),
                    'description': data.get('description', ''),
                    'verified': data.get('verified', False),
                    'created': data.get('created', '2025-10-21'),
                    'citations': len(data.get('citations', [])),
                    'complexity': complexity.get('detailLevel', 'medium'),
                    'nodes': complexity.get('nodes', 0),
                    'logicGates': {
                        'or': logic_gates.get('orGates', 0),
                        'and': logic_gates.get('andGates', 0),
                        'not': logic_gates.get('notGates', 0),
                        'total': logic_gates.get('total', 0)
                    }
                }
                
                processes.append(process_info)
                
                # Update counts
                organism_counts[process_info['organism']] += 1
                category_counts[process_info['category']] += 1
                total_citations += process_info['citations']
                total_nodes += process_info['nodes']
                total_or_gates += process_info['logicGates'].get('or', 0)
                total_and_gates += process_info['logicGates'].get('and', 0)
                total_not_gates += process_info['logicGates'].get('not', 0)
                
                if process_info['verified']:
                    verified_count += 1
                    
            except Exception as e:
                print(f"Error processing {json_file}: {e}")
    
    return processes, {
        'organism_counts': dict(organism_counts),
        'category_counts': dict(category_counts),
        'total_citations': total_citations,
        'total_nodes': total_nodes,
        'total_or_gates': total_or_gates,
        'total_and_gates': total_and_gates,
        'total_not_gates': total_not_gates,
        'verified_count': verified_count
    }

def create_metadata():
    """Create complete metadata.json"""
    processes, stats = scan_processes()
    
    print(f"Found {len(processes)} processes")
    print(f"OR Gates: {stats['total_or_gates']}")
    print(f"AND Gates: {stats['total_and_gates']}")
    print(f"NOT Gates: {stats['total_not_gates']}")
    print(f"Total Gates: {stats['total_or_gates'] + stats['total_and_gates'] + stats['total_not_gates']}")
    
    metadata = {
        "name": "GLMP Process Collection",
        "version": "2.1.0",
        "generated": "2025-10-21",
        "lastUpdated": "2025-10-21",
        "totalProcesses": len(processes),
        "description": f"GLMP v2.1: Genome Logic Modeling Project with {len(processes)} publication-quality biological processes",
        "organisms": [
            {"name": org, "processCount": count}
            for org, count in stats['organism_counts'].items()
        ],
        "statistics": {
            "totalProcesses": len(processes),
            "totalNodes": stats['total_nodes'],
            "avgNodes": round(stats['total_nodes'] / len(processes), 1) if processes else 0,
            "logicGates": {
                "OR": stats['total_or_gates'],
                "AND": stats['total_and_gates'],
                "NOT": stats['total_not_gates'],
                "total": stats['total_or_gates'] + stats['total_and_gates'] + stats['total_not_gates']
            },
            "architecture": "100:11:6:2",
            "avgGates": round((stats['total_or_gates'] + stats['total_and_gates'] + stats['total_not_gates']) / len(processes), 1) if processes else 0
        },
        "processes": processes
    }
    
    return metadata

def main():
    print("🔧 Rebuilding metadata.json with 108 processes...")
    
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
