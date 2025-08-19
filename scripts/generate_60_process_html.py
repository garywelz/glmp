#!/usr/bin/env python3
"""
Generate comprehensive HTML documentation for 60 yeast cellular processes.
This script reads all batch*.mmd files and creates a complete HTML document
with embedded Mermaid diagrams and professional styling.
"""

import os
import glob
import re
from pathlib import Path

def read_mermaid_file(filename):
    """Read Mermaid flowchart content from file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return f"<!-- Mermaid diagram not found: {filename} -->"

def get_process_name(filename):
    """Extract process name from filename."""
    # Remove batch prefix and .mmd extension
    name = filename.replace('batch', '').replace('.mmd', '')
    # Convert to readable format
    parts = name.split('_')
    if len(parts) >= 3:
        return ' '.join(parts[2:]).title()
    return name

def get_batch_info(batch_num):
    """Get batch information based on batch number."""
    batch_info = {
        '1': {'name': 'DNA Replication & Repair', 'icon': '🧬', 'count': 8, 'description': 'DNA replication, repair mechanisms, and genome maintenance'},
        '2': {'name': 'Cell Cycle Control', 'icon': '🔄', 'count': 7, 'description': 'Cell cycle progression, checkpoints, and division control'},
        '3': {'name': 'Protein Synthesis & Degradation', 'icon': '🧬', 'count': 10, 'description': 'Translation, protein folding, degradation, and quality control'},
        '4': {'name': 'Signal Transduction', 'icon': '📡', 'count': 9, 'description': 'Cellular signaling pathways and communication systems'},
        '5': {'name': 'Energy Metabolism', 'icon': '⚡', 'count': 11, 'description': 'Energy production, metabolism, and nutrient utilization'},
        '6': {'name': 'Lipid & Membrane Biology', 'icon': '🛢️', 'count': 6, 'description': 'Lipid synthesis, membrane dynamics, and cellular architecture'},
        '7': {'name': 'Cell Wall & Extracellular Matrix', 'icon': '🏗️', 'count': 4, 'description': 'Cell wall synthesis, remodeling, and extracellular structures'},
        '8': {'name': 'Chromatin & Transcription', 'icon': '📊', 'count': 6, 'description': 'Chromatin dynamics, transcription, and gene regulation'},
        '9': {'name': 'RNA Processing & Transport', 'icon': '🧬', 'count': 4, 'description': 'RNA processing, modification, and nuclear transport'},
        '10': {'name': 'Stress Response & Adaptation', 'icon': '🛡️', 'count': 5, 'description': 'Stress responses, adaptation mechanisms, and survival strategies'}
    }
    return batch_info.get(str(batch_num), {'name': f'Batch {batch_num}', 'icon': '📋', 'count': 0, 'description': 'Cellular processes'})

def generate_html():
    """Generate the complete HTML documentation."""
    
    # Find all batch files
    batch_files = glob.glob('batch*.mmd')
    batch_files.sort()
    
    # Group files by batch
    batches = {}
    for filename in batch_files:
        match = re.match(r'batch(\d+)_(\d+)_(.+)\.mmd', filename)
        if match:
            batch_num = match.group(1)
            process_num = match.group(2)
            process_name = match.group(3).replace('_', ' ').title()
            
            if batch_num not in batches:
                batches[batch_num] = []
            
            batches[batch_num].append({
                'filename': filename,
                'process_num': process_num,
                'process_name': process_name,
                'mermaid_content': read_mermaid_file(filename)
            })
    
    # Generate HTML content
    html_content = generate_html_header()
    
    # Add table of contents
    html_content += generate_toc(batches)
    
    # Add color legend
    html_content += generate_color_legend()
    
    # Add batch sections
    for batch_num in sorted(batches.keys()):
        html_content += generate_batch_section(batch_num, batches[batch_num])
    
    html_content += generate_html_footer()
    
    # Write to file
    with open('yeast_60_processes_comprehensive.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Generated comprehensive HTML documentation with {len(batch_files)} processes")
    print(f"📁 Output file: yeast_60_processes_comprehensive.html")

def generate_html_header():
    """Generate HTML header with styling."""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yeast Cellular Processes: Comprehensive 60-Process Set</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            background: rgba(255,255,255,0.1);
            padding: 20px;
            margin: 20px 0;
            border-radius: 10px;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            display: block;
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .toc {
            background: #f8f9fa;
            padding: 30px;
            border-bottom: 1px solid #e9ecef;
        }
        
        .toc h2 {
            color: #495057;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        
        .batch-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .batch-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .batch-card:hover {
            transform: translateY(-5px);
        }
        
        .batch-card h3 {
            color: #495057;
            margin: 0 0 15px 0;
            font-size: 1.3em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .process-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .process-list li {
            padding: 8px 0;
            border-bottom: 1px solid #f1f3f4;
            color: #666;
        }
        
        .process-list li:last-child {
            border-bottom: none;
        }
        
        .content {
            padding: 40px;
        }
        
        .batch-section {
            margin-bottom: 60px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .batch-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .batch-header h2 {
            margin: 0;
            font-size: 2em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .batch-header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .process-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 30px;
            padding: 30px;
        }
        
        .process-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .process-card h3 {
            color: #495057;
            margin: 0 0 20px 0;
            font-size: 1.4em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .process-description {
            color: #666;
            margin-bottom: 20px;
            line-height: 1.6;
        }
        
        .mermaid {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }
        
        .color-legend {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            border-left: 4px solid #667eea;
        }
        
        .color-legend h4 {
            margin: 0 0 15px 0;
            color: #495057;
        }
        
        .color-item {
            display: flex;
            align-items: center;
            margin: 8px 0;
        }
        
        .color-box {
            width: 20px;
            height: 20px;
            border-radius: 3px;
            margin-right: 10px;
        }
        
        .footer {
            background: #495057;
            color: white;
            text-align: center;
            padding: 30px;
            margin-top: 40px;
        }
        
        .footer p {
            margin: 0;
            opacity: 0.8;
        }
        
        @media (max-width: 768px) {
            .process-grid {
                grid-template-columns: 1fr;
            }
            
            .batch-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧬 Yeast Cellular Processes</h1>
            <p>Comprehensive 60-Process Set: Canvas Framework Implementation</p>
            <div class="stats">
                <div class="stat">
                    <span class="stat-number">60</span>
                    <span class="stat-label">Processes</span>
                </div>
                <div class="stat">
                    <span class="stat-number">10</span>
                    <span class="stat-label">Batches</span>
                </div>
                <div class="stat">
                    <span class="stat-number">100%</span>
                    <span class="stat-label">Complete</span>
                </div>
            </div>
        </div>'''

def generate_toc(batches):
    """Generate table of contents."""
    toc = '''
        <div class="toc">
            <h2>📋 Table of Contents</h2>
            <div class="batch-grid">'''
    
    for batch_num in sorted(batches.keys()):
        batch_info = get_batch_info(batch_num)
        toc += f'''
                <div class="batch-card">
                    <h3>{batch_info["icon"]} Batch {batch_num}: {batch_info["name"]}</h3>
                    <ul class="process-list">'''
        
        for process in batches[batch_num]:
            toc += f'''
                        <li>{process["process_name"]}</li>'''
        
        toc += '''
                    </ul>
                </div>'''
    
    toc += '''
            </div>
        </div>'''
    
    return toc

def generate_color_legend():
    """Generate color legend section."""
    return '''
            <div class="color-legend">
                <h4>🎨 Canvas Framework Color Coding</h4>
                <div class="color-item">
                    <div class="color-box" style="background: #ff6b6b;"></div>
                    <span><strong>Triggers:</strong> Environmental signals, cellular stress, developmental cues</span>
                </div>
                <div class="color-item">
                    <div class="color-box" style="background: #feca57;"></div>
                    <span><strong>Proteins:</strong> Receptors, enzymes, structural proteins, signaling molecules</span>
                </div>
                <div class="color-item">
                    <div class="color-box" style="background: #4ecdc4;"></div>
                    <span><strong>Enzymes:</strong> Catalytic activities, phosphorylation events, regulatory processes</span>
                </div>
                <div class="color-item">
                    <div class="color-box" style="background: #45b7d1;"></div>
                    <span><strong>Intermediates:</strong> Signaling complexes, metabolic intermediates, cellular structures</span>
                </div>
                <div class="color-item">
                    <div class="color-box" style="background: #96ceb4;"></div>
                    <span><strong>Products:</strong> Completed processes, cellular responses, functional outcomes</span>
                </div>
            </div>
            
            <div class="content">'''

def generate_batch_section(batch_num, processes):
    """Generate a batch section with all its processes."""
    batch_info = get_batch_info(batch_num)
    
    section = f'''
            <!-- Batch {batch_num}: {batch_info["name"]} -->
            <div class="batch-section">
                <div class="batch-header">
                    <h2>{batch_info["icon"]} Batch {batch_num}: {batch_info["name"]}</h2>
                    <p>{batch_info["count"]} processes covering {batch_info["description"]}</p>
                </div>
                
                <div class="process-grid">'''
    
    for process in processes:
        section += f'''
                    <div class="process-card">
                        <h3>{process["process_name"]}</h3>
                        <div class="process-description">
                            Detailed flowchart showing the computational logic and regulatory steps of {process["process_name"].lower()}.
                        </div>
                        <div class="mermaid">
{process["mermaid_content"]}
                        </div>
                    </div>'''
    
    section += '''
                </div>
            </div>'''
    
    return section

def generate_html_footer():
    """Generate HTML footer with scripts."""
    return '''
        </div>
        
        <div class="footer">
            <p>🧬 Yeast Cellular Processes: Comprehensive 60-Process Set</p>
            <p>Canvas Framework Implementation - Genome Logic Modeling Project</p>
        </div>
    </div>
    
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true
            }}
        }});
    </script>
</body>
</html>'''

if __name__ == "__main__":
    generate_html()
