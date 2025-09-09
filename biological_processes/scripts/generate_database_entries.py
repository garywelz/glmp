#!/usr/bin/env python3
"""
Generate Database Entries with Logical Structure Analysis
Creates database-ready entries for all GLMP biological processes
"""

import os
import json
import csv
from logical_structure_analyzer import BiologicalLogicAnalyzer

def generate_database_csv(folder_path: str, output_file: str = "glmp_processes_with_logic.csv"):
    """
    Generate a CSV file with all processes and their logical structure analysis
    
    Args:
        folder_path: Path to biological_processes folder
        output_file: Output CSV filename
    """
    analyzer = BiologicalLogicAnalyzer()
    
    # CSV headers including logical structure columns
    headers = [
        'process_id', 'kingdom', 'organism', 'batch_name', 'process_name', 
        'process_description', 'html_file_path', 'anchor_id', 'direct_link',
        'conservation_level', 'functional_category', 'complexity_score',
        
        # Logical structure boolean flags
        'has_and_gates', 'has_or_gates', 'has_feedback_loops', 'has_checkpoints',
        'has_bistable_switches', 'has_amplification', 'has_competitive_inhibition',
        'has_cascades', 'has_oscillation',
        
        # Logical structure counts
        'and_gate_count', 'or_gate_count', 'feedback_loop_count', 'checkpoint_count',
        'bistable_switch_count', 'amplification_count', 'competitive_inhibition_count',
        'cascade_count', 'oscillation_count',
        
        # Computed metrics
        'total_logic_structures', 'logic_complexity_score',
        
        # Confidence scores  
        'and_gate_confidence', 'or_gate_confidence', 'feedback_loop_confidence',
        'checkpoint_confidence', 'bistable_switch_confidence', 'amplification_confidence',
        'competitive_inhibition_confidence', 'cascade_confidence', 'oscillation_confidence'
    ]
    
    rows = []
    
    # Process each organism folder
    for organism_folder in ['ecoli', 'yeast', 'human', 'prokaryotes', 'eukaryotes', 'viruses']:
        organism_path = os.path.join(folder_path, organism_folder)
        
        if not os.path.exists(organism_path):
            continue
            
        print(f"\n🔍 Processing {organism_folder}...")
        
        # Analyze all HTML files in organism folder
        html_files = [f for f in os.listdir(organism_path) if f.endswith('.html')]
        
        for html_file in html_files:
            file_path = os.path.join(organism_path, html_file)
            print(f"  Analyzing: {html_file}")
            
            # Analyze the file
            analysis = analyzer.analyze_process_file(file_path)
            
            if "error" in analysis:
                print(f"    Error: {analysis['error']}")
                continue
            
            # Generate database entry
            db_entry = analyzer.generate_database_entry(analysis)
            
            # Extract organism and batch info from filename
            organism_name = organism_folder
            if organism_folder == 'ecoli':
                organism_name = 'Escherichia coli'
            elif organism_folder == 'yeast':
                organism_name = 'Saccharomyces cerevisiae'
            
            # Create base entry
            base_entry = {
                'kingdom': get_kingdom(organism_name),
                'organism': organism_name,
                'batch_name': extract_batch_name(html_file),
                'html_file_path': f"biological_processes/{organism_folder}/{html_file}",
                'conservation_level': 'Universal',  # Default, can be updated
                'functional_category': extract_category(html_file)
            }
            
            # Create entries for each process in the file
            for process_id in range(1, analysis['total_processes'] + 1):
                process_entry = {
                    'process_id': f"{organism_folder}_{extract_batch_name(html_file).lower().replace(' ', '_')}_{process_id:03d}",
                    'process_name': f"Process {process_id}",  # Will be updated with actual names
                    'process_description': f"Process {process_id} from {extract_batch_name(html_file)}",
                    'anchor_id': f"process-{process_id}",  # Will be updated with actual anchors
                    'direct_link': f"https://garywelz-glmp.static.hf.space/biological_processes/{organism_folder}/{html_file}#process-{process_id}",
                    **base_entry,
                    **db_entry
                }
                
                rows.append(process_entry)
    
    # Write CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"\n✅ Database CSV generated: {output_file}")
    print(f"📊 Total entries: {len(rows)}")
    
    return rows

def get_kingdom(organism_name: str) -> str:
    """Determine kingdom from organism name"""
    if organism_name in ['Escherichia coli']:
        return 'Prokaryotes'
    elif organism_name in ['Saccharomyces cerevisiae', 'Homo sapiens']:
        return 'Eukaryotes'
    else:
        return 'Unknown'

def extract_batch_name(filename: str) -> str:
    """Extract batch name from filename"""
    # Remove organism prefix and .html suffix
    name = filename.replace('.html', '')
    if 'batch' in name:
        parts = name.split('batch')[1]
        # Extract descriptive part after batch number
        batch_parts = parts.split('_')[1:]  # Skip batch number
        return ' '.join(word.title() for word in batch_parts)
    return name

def extract_category(filename: str) -> str:
    """Extract functional category from filename"""
    if 'dna_replication' in filename or 'repair' in filename:
        return 'Central Dogma'
    elif 'cell_division' in filename or 'segregation' in filename:
        return 'Cell Structure'
    elif 'translation' in filename or 'transcription' in filename:
        return 'Central Dogma'
    elif 'metabolism' in filename:
        return 'Metabolism'
    elif 'stress' in filename:
        return 'Regulation'
    else:
        return 'Other'

if __name__ == "__main__":
    # Generate database entries for current collection
    entries = generate_database_csv("/workspace/biological_processes/")
    
    print(f"\n🎯 Sample Database Entries:")
    for i, entry in enumerate(entries[:3]):  # Show first 3 entries
        print(f"\nEntry {i+1}:")
        print(f"  Process ID: {entry['process_id']}")
        print(f"  Organism: {entry['organism']}")
        print(f"  Logic Complexity: {entry['logic_complexity_score']}")
        print(f"  Has Feedback Loops: {entry['has_feedback_loops']}")
        print(f"  Total Logic Structures: {entry['total_logic_structures']}")
        print(f"  Direct Link: {entry['direct_link']}")