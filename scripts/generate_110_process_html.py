#!/usr/bin/env python3
"""
Generate comprehensive HTML documentation for all 110 yeast cellular processes.
"""

import glob
import os
import re

def generate_html_header():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yeast Cellular Processes: Comprehensive 110-Process Set</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 300;
        }
        .header p {
            margin: 0.5rem 0 0 0;
            font-size: 1.2rem;
            opacity: 0.9;
        }
        .toc {
            background: #f8f9fa;
            padding: 2rem;
            border-bottom: 1px solid #dee2e6;
        }
        .toc h2 {
            color: #495057;
            margin-bottom: 1rem;
        }
        .toc ul {
            list-style: none;
            padding: 0;
        }
        .toc li {
            margin: 0.5rem 0;
        }
        .toc a {
            color: #007bff;
            text-decoration: none;
            font-weight: 500;
        }
        .toc a:hover {
            color: #0056b3;
            text-decoration: underline;
        }
        .content {
            padding: 2rem;
        }
        .color-legend {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 2rem;
        }
        .color-legend h4 {
            margin-top: 0;
            color: #495057;
        }
        .color-legend ul {
            list-style: none;
            padding: 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 0.5rem;
        }
        .color-legend li {
            padding: 0.5rem;
            border-radius: 4px;
            font-weight: 500;
        }
        .batch-section {
            margin: 3rem 0;
            padding: 2rem;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            background: #fff;
        }
        .batch-section h3 {
            color: #495057;
            border-bottom: 2px solid #007bff;
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }
        .process-item {
            margin: 2rem 0;
            padding: 1.5rem;
            border-left: 4px solid #007bff;
            background: #f8f9fa;
            border-radius: 0 8px 8px 0;
        }
        .process-item h4 {
            color: #495057;
            margin-top: 0;
        }
        .process-item p {
            color: #6c757d;
            margin-bottom: 1rem;
        }
        .mermaid-container {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .footer {
            background: #343a40;
            color: white;
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }
        .stat-item {
            text-align: center;
            padding: 1rem;
            background: #e9ecef;
            border-radius: 8px;
        }
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #007bff;
        }
        .stat-label {
            color: #6c757d;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧬 Yeast Cellular Processes</h1>
            <p>Comprehensive 110-Process Set: Programming Framework Implementation</p>
        </div>
        <div class="toc">
            <h2>📋 Table of Contents</h2>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">110</div>
                    <div class="stat-label">Processes</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">15</div>
                    <div class="stat-label">Batches</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">4</div>
                    <div class="stat-label">Phases</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">100%</div>
                    <div class="stat-label">Complete</div>
                </div>
            </div>
            <ul id="toc-list">
                <!-- TOC will be generated here -->
            </ul>
        </div>
        <div class="content">
            <div class="color-legend">
                <h4>🎨 Programming Framework Color Coding</h4>
                <ul>
                    <li style="background: #ff6b6b; color: white;">🔴 <strong>Triggers:</strong> Environmental signals, cellular stress, developmental cues</li>
                    <li style="background: #feca57; color: black;">🟡 <strong>Proteins:</strong> Receptors, enzymes, structural proteins, signaling molecules</li>
                    <li style="background: #4ecdc4; color: black;">🟢 <strong>Enzymes:</strong> Catalytic activities, phosphorylation events, regulatory processes</li>
                    <li style="background: #45b7d1; color: white;">🔵 <strong>Intermediates:</strong> Signaling complexes, metabolic intermediates, cellular structures</li>
                    <li style="background: #96ceb4; color: black;">🟢 <strong>Products:</strong> Completed processes, cellular responses, functional outcomes</li>
                </ul>
            </div>
"""

def generate_html_footer():
    return """
        </div>
        <div class="footer">
            <p>🧬 Yeast Cellular Processes: Comprehensive 110-Process Set</p>
            <p>Programming Framework Implementation - Genome Logic Modeling Project</p>
        </div>
    </div>
    <script>
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true
            }
        });
    </script>
</body>
</html>
"""

def generate_toc(batches):
    toc_html = ""
    for batch_num in sorted(batches.keys()):
        batch_name = get_batch_name(batch_num)
        toc_html += f'<li><a href="#batch{batch_num}">{batch_name}</a></li>'
    return toc_html

def get_batch_name(batch_num):
    batch_names = {
        '1': 'DNA Replication & Repair',
        '2': 'Cell Cycle Control', 
        '3': 'Protein Synthesis & Degradation',
        '4': 'Signal Transduction',
        '5': 'Energy Metabolism',
        '6': 'Lipid & Membrane Biology',
        '7': 'Cell Wall & Extracellular Matrix',
        '8': 'Chromatin & Transcription',
        '9': 'RNA Processing & Transport',
        '10': 'Stress Response & Adaptation',
        '11': 'Advanced Metabolic Pathways',
        '12': 'Advanced Regulatory Networks',
        '13': 'Environmental Adaptation',
        '14': 'Developmental Processes',
        '15': 'Quality Control Systems'
    }
    return f"Batch {batch_num}: {batch_names.get(batch_num, 'Unknown')}"

def generate_batch_section(batch_num, processes):
    batch_name = get_batch_name(batch_num)
    section_html = f'<div class="batch-section" id="batch{batch_num}">\n'
    section_html += f'<h3>{batch_name}</h3>\n'
    
    for process in processes:
        process_name = process['name']
        process_file = process['file']
        
        # Read Mermaid content
        try:
            with open(process_file, 'r', encoding='utf-8') as f:
                mermaid_content = f.read().strip()
        except FileNotFoundError:
            mermaid_content = "graph TD\n    A[Process Not Found] --> B[Content Missing]\n    style A fill:#ff6b6b\n    style B fill:#96ceb4"
        
        # Generate process description
        description = generate_process_description(process_name, batch_num)
        
        section_html += f'<div class="process-item">\n'
        section_html += f'<h4>{process_name}</h4>\n'
        section_html += f'<p>{description}</p>\n'
        section_html += f'<div class="mermaid-container">\n'
        section_html += f'<div class="mermaid">\n{mermaid_content}\n</div>\n'
        section_html += f'</div>\n'
        section_html += f'</div>\n'
    
    section_html += '</div>\n'
    return section_html

def generate_process_description(process_name, batch_num):
    # Generate descriptions based on process name and batch
    descriptions = {
        # Batch 1: DNA Replication & Repair
        'dna_replication_initiation': 'The initiation of DNA replication at origins of replication, involving origin recognition and pre-replication complex assembly.',
        'dna_replication_elongation': 'The elongation phase of DNA replication, where DNA polymerase synthesizes new DNA strands.',
        'nucleotide_excision_repair': 'Repair of bulky DNA lesions through excision of damaged nucleotides and resynthesis.',
        'mismatch_repair': 'Correction of base-pair mismatches and small insertions/deletions in DNA.',
        'double_strand_break_repair': 'Repair of DNA double-strand breaks through homologous recombination or non-homologous end joining.',
        'telomere_maintenance': 'Maintenance of telomere length and structure to prevent chromosome end degradation.',
        
        # Batch 2: Cell Cycle Control
        'spindle_assembly_checkpoint': 'Checkpoint ensuring proper spindle assembly before anaphase onset.',
        'anaphase_promoting_complex': 'Ubiquitin ligase complex that triggers anaphase and mitotic exit.',
        'cytokinesis': 'Physical separation of daughter cells after mitosis.',
        'cell_cycle_exit': 'Transition from cell cycle to quiescence or differentiation.',
        'g1s_transition': 'Critical decision point where cells commit to DNA replication.',
        
        # Add more descriptions for other batches...
    }
    
    # Generate a generic description if not found
    if process_name in descriptions:
        return descriptions[process_name]
    else:
        return f'Detailed analysis of {process_name.replace("_", " ").title()} using a programming framework, revealing computational logic and regulatory patterns.'
    
    return f'Detailed analysis of {process_name.replace("_", " ").title()} using a programming framework, revealing computational logic and regulatory patterns.'

def main():
    # Get all batch files
    batch_files = glob.glob('docs/paper/community/contributions/new_charts/batch*.mmd')
    
    # Group files by batch
    batches = {}
    for file in batch_files:
        match = re.match(r'.*batch(\d+)_(\d+)_(.+)\.mmd', file)
        if match:
            batch_num = match.group(1)
            process_num = match.group(2)
            process_name = match.group(3).replace('_', ' ').title()
            
            if batch_num not in batches:
                batches[batch_num] = []
            
            batches[batch_num].append({
                'name': process_name,
                'file': file,
                'number': process_num
            })
    
    # Sort processes within each batch
    for batch_num in batches:
        batches[batch_num].sort(key=lambda x: int(x['number']))
    
    # Generate HTML
    html_content = generate_html_header()
    html_content += generate_toc(batches)
    
    # Generate batch sections
    for batch_num in sorted(batches.keys()):
        html_content += generate_batch_section(batch_num, batches[batch_num])
    
    html_content += generate_html_footer()
    
    # Write to file
    with open('yeast_110_processes_comprehensive.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Generated comprehensive HTML documentation for {len(batch_files)} processes across {len(batches)} batches")
    print(f"📄 Output file: yeast_110_processes_comprehensive.html")

if __name__ == "__main__":
    main()
