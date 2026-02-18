#!/usr/bin/env python3
"""
Dynamically rebuild metadata.json from all process JSON files
Extracts real statistics from the actual process data
"""

import json
import os
from pathlib import Path
from collections import defaultdict

def scan_all_processes():
    """Scan all process JSON files and extract real statistics"""
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
    
    print("🔍 Scanning all process files...")
    
    # Scan all organisms
    for organism_dir in ['ecoli', 'yeast', 'bacillus']:
        organism_path = base_dir / organism_dir
        if not organism_path.exists():
            print(f"  ⚠️  Directory {organism_dir} not found")
            continue
            
        print(f"  📁 Scanning {organism_dir}...")
        file_count = 0
        
        for json_file in organism_path.glob('*.json'):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                # Extract metadata with proper structure
                complexity = data.get('complexity', {})
                logic_gates = complexity.get('logicGates', {})
                
                # Get nodes count
                nodes = complexity.get('nodes', 0)
                
                # Get logic gates (handle different possible field names)
                or_gates = logic_gates.get('orGates', logic_gates.get('or', 0))
                and_gates = logic_gates.get('andGates', logic_gates.get('and', 0))
                not_gates = logic_gates.get('notGates', logic_gates.get('not', 0))
                total_gates = logic_gates.get('total', or_gates + and_gates + not_gates)
                
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
                    'nodes': nodes,
                    'logicGates': {
                        'or': or_gates,
                        'and': and_gates,
                        'not': not_gates,
                        'total': total_gates
                    }
                }
                
                processes.append(process_info)
                file_count += 1
                
                # Update counts
                organism_counts[process_info['organism']] += 1
                category_counts[process_info['category']] += 1
                total_citations += process_info['citations']
                total_nodes += nodes
                total_or_gates += or_gates
                total_and_gates += and_gates
                total_not_gates += not_gates
                
                if process_info['verified']:
                    verified_count += 1
                    
                # Debug output for first few files
                if file_count <= 3:
                    print(f"    📄 {json_file.name}: {or_gates} OR, {and_gates} AND, {not_gates} NOT, {nodes} nodes")
                    
            except Exception as e:
                print(f"    ❌ Error processing {json_file}: {e}")
        
        print(f"  ✅ {organism_dir}: {file_count} files processed")
    
    print(f"\n📊 SUMMARY:")
    print(f"  Total Processes: {len(processes)}")
    print(f"  Total Nodes: {total_nodes}")
    print(f"  OR Gates: {total_or_gates}")
    print(f"  AND Gates: {total_and_gates}")
    print(f"  NOT Gates: {total_not_gates}")
    print(f"  Total Gates: {total_or_gates + total_and_gates + total_not_gates}")
    print(f"  Avg Nodes: {total_nodes / len(processes) if processes else 0:.1f}")
    print(f"  Avg Gates: {(total_or_gates + total_and_gates + total_not_gates) / len(processes) if processes else 0:.1f}")
    
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

def create_dynamic_metadata():
    """Create complete metadata.json with real data"""
    processes, stats = scan_all_processes()
    
    # Calculate architecture pattern
    total_gates = stats['total_or_gates'] + stats['total_and_gates'] + stats['total_not_gates']
    if total_gates > 0:
        or_ratio = (stats['total_or_gates'] / total_gates) * 100
        and_ratio = (stats['total_and_gates'] / total_gates) * 100
        not_ratio = (stats['total_not_gates'] / total_gates) * 100
        architecture = f"100:{and_ratio:.0f}:{or_ratio:.0f}:{not_ratio:.0f}"
    else:
        architecture = "100:11:6:2"
    
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
                "total": total_gates
            },
            "architecture": architecture,
            "avgGates": round(total_gates / len(processes), 1) if processes else 0
        },
        "processes": processes
    }
    
    return metadata

def main():
    print("🔧 DYNAMICALLY REBUILDING METADATA FROM ACTUAL PROCESS FILES")
    print("=" * 60)
    
    metadata = create_dynamic_metadata()
    
    # Write to glmp-v2/data/metadata.json
    output_path = "glmp-v2/data/metadata.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✅ CREATED {output_path}")
    print(f"   Total Processes: {metadata['totalProcesses']}")
    print(f"   Logic Gates: OR={metadata['statistics']['logicGates']['OR']}, AND={metadata['statistics']['logicGates']['AND']}, NOT={metadata['statistics']['logicGates']['NOT']}")
    print(f"   Architecture: {metadata['statistics']['architecture']}")
    print(f"   File Size: {os.path.getsize(output_path) / 1024:.1f} KB")

if __name__ == "__main__":
    main()
