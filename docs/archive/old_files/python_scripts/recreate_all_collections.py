#!/usr/bin/env python3
"""
Recreate all yeast and E. coli collection files with the working template.
This script will systematically recreate all files with proper Mermaid syntax.
"""

import os
import glob
from pathlib import Path

def create_html_template(title, intro_text, processes, collection_type):
    """Create a complete HTML file with proper Mermaid syntax."""
    
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Programming Framework Analysis</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, 'Arial Unicode MS', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5rem;
            font-weight: 300;
        }}
        .content {{
            padding: 2rem;
        }}
        .intro {{
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 8px;
            margin-bottom: 2rem;
        }}
        .toc {{
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 8px;
            margin-bottom: 2rem;
        }}
        .toc ul {{
            list-style: none;
            padding: 0;
        }}
        .toc li {{
            margin: 0.5rem 0;
        }}
        .toc a {{
            color: #007bff;
            text-decoration: none;
            font-weight: 500;
        }}
        .process-item {{
            margin: 2rem 0;
            padding: 1.5rem;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            background: #fafafa;
        }}
        .process-item h3 {{
            color: #495057;
            margin-bottom: 1rem;
        }}
        .mermaid-container {{
            background: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            overflow-x: auto;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 2rem;
            text-align: center;
            border-top: 1px solid #dee2e6;
            margin-top: 2rem;
        }}
        .color-legend {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 0.5rem 1rem;
            margin: 1rem 0 0;
            font-size: 10pt;
            color: #333;
        }}
        .color-box {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 2px;
            margin-right: 4px;
            border: 1px solid rgba(0,0,0,.15);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>Programming Framework Analysis - {collection_type} Processes</p>
        </div>
        <div class="content">
            <div class="intro">
                <h2>{title}</h2>
                <p>{intro_text}</p>
            </div>
            
            <div class="toc">
                <h2>📋 Table of Contents</h2>
                <ul>
'''
    
    # Add table of contents
    for i, process in enumerate(processes, 1):
        process_id = process['id']
        process_name = process['name']
        html_template += f'                    <li><a href="#{process_id}">{i}. {process_name}</a></li>\n'
    
    html_template += '''                </ul>
            </div>
            
'''
    
    # Add each process
    for i, process in enumerate(processes, 1):
        process_id = process['id']
        process_name = process['name']
        process_desc = process['description']
        mermaid_code = process['mermaid']
        
        html_template += f'''            <!-- Process {i}: {process_name} -->
            <div class="process-item" id="{process_id}">
                <h3>{i}. {process_name}</h3>
                <p>{process_desc}</p>
                <div class="mermaid-container">
                    <div class="mermaid">
{mermaid_code}
                    </div>
                    <div class="color-legend">
                        <span><span class="color-box" style="background:#ff6b6b;"></span>Triggers & Conditions</span>
                        <span><span class="color-box" style="background:#ffd43b;"></span>Catalysts & Enzymes</span>
                        <span><span class="color-box" style="background:#51cf66;"></span>Chemical Processing</span>
                        <span><span class="color-box" style="background:#74c0fc;"></span>Intermediates</span>
                        <span><span class="color-box" style="background:#b197fc;"></span>Products</span>
                    </div>
                </div>
            </div>

'''
    
    html_template += '''            <div class="footer">
                <p><strong>Generated using the Programming Framework methodology</strong></p>
                <p>This analysis demonstrates the computational nature of biological systems</p>
                <p>Each flowchart preserves maximum detail through optimized Mermaid configuration</p>
            </div>
        </div>
    </div>
    
    <script>
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            flowchart: {
                useMaxWidth: false,
                htmlLabels: true,
                curve: 'linear',
                nodeSpacing: 30,
                rankSpacing: 40,
                padding: 10
            },
            themeVariables: {
                fontFamily: 'Arial, sans-serif',
                fontSize: '14px',
                primaryColor: '#ff6b6b',
                lineColor: '#333333',
                secondaryColor: '#feca57',
                tertiaryColor: '#4ecdc4'
            }
        });
    </script>
</body>
</html>'''
    
    return html_template

def create_yeast_batch03():
    """Create yeast batch 03: Protein Synthesis & Degradation"""
    processes = [
        {
            'id': 'translation-initiation',
            'name': 'Translation Initiation',
            'description': 'Detailed analysis of Translation Initiation using the Programming Framework, revealing computational logic and regulatory patterns.',
            'mermaid': '''graph TD
    A[mRNA Recognition] --> B[eIF4E Binding]
    B --> C[eIF4G Recruitment]
    C --> D[43S Complex Loading]
    D --> E[Start Codon Scanning]
    E --> F[60S Subunit Joining]
    F --> G[Translation Initiation]
    G --> H[Protein Synthesis]
    
    style A fill:#ff6b6b,color:#fff
    style B fill:#ffd43b,color:#000
    style C fill:#ffd43b,color:#000
    style D fill:#51cf66,color:#fff
    style E fill:#74c0fc,color:#fff
    style F fill:#51cf66,color:#fff
    style G fill:#b197fc,color:#fff
    style H fill:#b197fc,color:#fff'''
        },
        {
            'id': 'translation-elongation',
            'name': 'Translation Elongation',
            'description': 'Detailed analysis of Translation Elongation using the Programming Framework, revealing computational logic and regulatory patterns.',
            'mermaid': '''graph TD
    A[Peptidyl Transfer] --> B[tRNA Translocation]
    B --> C[mRNA Movement]
    C --> D[Next Codon Reading]
    D --> E[Amino Acid Addition]
    E --> F[Peptide Bond Formation]
    F --> G[Elongation Cycle]
    G --> H[Protein Chain Growth]
    
    style A fill:#ff6b6b,color:#fff
    style B fill:#ffd43b,color:#000
    style C fill:#51cf66,color:#fff
    style D fill:#74c0fc,color:#fff
    style E fill:#ffd43b,color:#000
    style F fill:#51cf66,color:#fff
    style G fill:#74c0fc,color:#fff
    style H fill:#b197fc,color:#fff'''
        },
        {
            'id': 'translation-termination',
            'name': 'Translation Termination',
            'description': 'Detailed analysis of Translation Termination using the Programming Framework, revealing computational logic and regulatory patterns.',
            'mermaid': '''graph TD
    A[Stop Codon Recognition] --> B[Release Factor Binding]
    B --> C[Peptide Release]
    C --> D[Ribosome Dissociation]
    D --> E[Protein Folding]
    E --> F[Post-translational Modification]
    F --> G[Protein Maturation]
    G --> H[Functional Protein]
    
    style A fill:#ff6b6b,color:#fff
    style B fill:#ffd43b,color:#000
    style C fill:#51cf66,color:#fff
    style D fill:#74c0fc,color:#fff
    style E fill:#51cf66,color:#fff
    style F fill:#ffd43b,color:#000
    style G fill:#74c0fc,color:#fff
    style H fill:#b197fc,color:#fff'''
        },
        {
            'id': 'protein-degradation',
            'name': 'Protein Degradation',
            'description': 'Detailed analysis of Protein Degradation using the Programming Framework, revealing computational logic and regulatory patterns.',
            'mermaid': '''graph TD
    A[Protein Damage] --> B[Ubiquitin Recognition]
    B --> C[E3 Ligase Activity]
    C --> D[Polyubiquitination]
    D --> E[Proteasome Targeting]
    E --> F[Protein Unfolding]
    F --> G[Peptide Cleavage]
    G --> H[Amino Acid Recycling]
    
    style A fill:#ff6b6b,color:#fff
    style B fill:#ffd43b,color:#000
    style C fill:#ffd43b,color:#000
    style D fill:#51cf66,color:#fff
    style E fill:#ffd43b,color:#000
    style F fill:#51cf66,color:#fff
    style G fill:#51cf66,color:#fff
    style H fill:#b197fc,color:#fff'''
        }
    ]
    
    return create_html_template(
        "🧬 Yeast Batch 03: Protein Synthesis & Degradation",
        "Protein synthesis and degradation systems demonstrating sophisticated biological programming with quality control and regulatory mechanisms.",
        processes,
        "Protein"
    )

def create_yeast_batch04():
    """Create yeast batch 04: Signal Transduction"""
    processes = [
        {
            'id': 'receptor-activation',
            'name': 'Receptor Activation',
            'description': 'Detailed analysis of Receptor Activation using the Programming Framework, revealing computational logic and regulatory patterns.',
            'mermaid': '''graph TD
    A[Ligand Binding] --> B[Receptor Dimerization]
    B --> C[Conformational Change]
    C --> D[Kinase Activation]
    D --> E[Phosphorylation Cascade]
    E --> F[Signal Amplification]
    F --> G[Downstream Activation]
    G --> H[Cellular Response]
    
    style A fill:#ff6b6b,color:#fff
    style B fill:#ffd43b,color:#000
    style C fill:#51cf66,color:#fff
    style D fill:#ffd43b,color:#000
    style E fill:#51cf66,color:#fff
    style F fill:#74c0fc,color:#fff
    style G fill:#51cf66,color:#fff
    style H fill:#b197fc,color:#fff'''
        },
        {
            'id': 'map-kinase-cascade',
            'name': 'MAP Kinase Cascade',
            'description': 'Detailed analysis of MAP Kinase Cascade using the Programming Framework, revealing computational logic and regulatory patterns.',
            'mermaid': '''graph TD
    A[Signal Reception] --> B[Ras Activation]
    B --> C[Raf Phosphorylation]
    C --> D[MEK Activation]
    D --> E[ERK Phosphorylation]
    E --> F[Transcription Factor Activation]
    F --> G[Gene Expression]
    G --> H[Cellular Response]
    
    style A fill:#ff6b6b,color:#fff
    style B fill:#ffd43b,color:#000
    style C fill:#ffd43b,color:#000
    style D fill:#ffd43b,color:#000
    style E fill:#ffd43b,color:#000
    style F fill:#51cf66,color:#fff
    style G fill:#74c0fc,color:#fff
    style H fill:#b197fc,color:#fff'''
        },
        {
            'id': 'g-protein-signaling',
            'name': 'G Protein Signaling',
            'description': 'Detailed analysis of G Protein Signaling using the Programming Framework, revealing computational logic and regulatory patterns.',
            'mermaid': '''graph TD
    A[GPCR Activation] --> B[G Protein Exchange]
    B --> C[GTP Binding]
    C --> D[Effector Activation]
    D --> E[Second Messenger Production]
    E --> F[Signal Transduction]
    F --> G[Cellular Response]
    G --> H[Signal Termination]
    
    style A fill:#ff6b6b,color:#fff
    style B fill:#ffd43b,color:#000
    style C fill:#51cf66,color:#fff
    style D fill:#ffd43b,color:#000
    style E fill:#51cf66,color:#fff
    style F fill:#74c0fc,color:#fff
    style G fill:#b197fc,color:#fff
    style H fill:#ff6b6b,color:#fff'''
        },
        {
            'id': 'calcium-signaling',
            'name': 'Calcium Signaling',
            'description': 'Detailed analysis of Calcium Signaling using the Programming Framework, revealing computational logic and regulatory patterns.',
            'mermaid': '''graph TD
    A[Calcium Release] --> B[IP3 Receptor Activation]
    B --> C[ER Calcium Release]
    C --> D[Calcium Binding Proteins]
    D --> E[Enzyme Activation]
    E --> F[Signal Amplification]
    F --> G[Cellular Response]
    G --> H[Calcium Reuptake]
    
    style A fill:#ff6b6b,color:#fff
    style B fill:#ffd43b,color:#000
    style C fill:#51cf66,color:#fff
    style D fill:#ffd43b,color:#000
    style E fill:#51cf66,color:#fff
    style F fill:#74c0fc,color:#fff
    style G fill:#b197fc,color:#fff
    style H fill:#ff6b6b,color:#fff'''
        }
    ]
    
    return create_html_template(
        "🧬 Yeast Batch 04: Signal Transduction",
        "Signal transduction systems demonstrating sophisticated biological programming with receptor activation and cascading responses.",
        processes,
        "Signal"
    )

def create_ecoli_batch01():
    """Create E. coli batch 01: DNA Replication & Repair"""
    processes = [
        {
            'id': 'dna-replication-initiation',
            'name': 'DNA Replication Initiation',
            'description': 'Detailed analysis of E. coli DNA Replication Initiation using the Programming Framework, revealing computational logic and regulatory patterns.',
            'mermaid': '''graph TD
    A[oriC Recognition] --> B[DnaA Binding]
    B --> C[DNA Unwinding]
    C --> D[DnaB Helicase Loading]
    D --> E[Primosome Assembly]
    E --> F[DNA Polymerase III Loading]
    F --> G[Replication Fork Formation]
    G --> H[Bidirectional Replication]
    
    style A fill:#ff6b6b,color:#fff
    style B fill:#ffd43b,color:#000
    style C fill:#51cf66,color:#fff
    style D fill:#ffd43b,color:#000
    style E fill:#51cf66,color:#fff
    style F fill:#ffd43b,color:#000
    style G fill:#74c0fc,color:#fff
    style H fill:#b197fc,color:#fff'''
        },
        {
            'id': 'dna-repair',
            'name': 'DNA Repair',
            'description': 'Detailed analysis of E. coli DNA Repair using the Programming Framework, revealing computational logic and regulatory patterns.',
            'mermaid': '''graph TD
    A[DNA Damage Detection] --> B[UvrA-UvrB Recognition]
    B --> C[UvrC Recruitment]
    C --> D[Excision Repair]
    D --> E[DNA Polymerase I]
    E --> F[DNA Ligase Activity]
    F --> G[Repair Completion]
    G --> H[Cell Survival]
    
    style A fill:#ff6b6b,color:#fff
    style B fill:#ffd43b,color:#000
    style C fill:#ffd43b,color:#000
    style D fill:#51cf66,color:#fff
    style E fill:#ffd43b,color:#000
    style F fill:#ffd43b,color:#000
    style G fill:#b197fc,color:#fff
    style H fill:#b197fc,color:#fff'''
        }
    ]
    
    return create_html_template(
        "🦠 E. coli Batch 01: DNA Replication & Repair",
        "E. coli DNA replication and repair systems demonstrating sophisticated biological programming with error correction and quality control.",
        processes,
        "DNA"
    )

def main():
    """Main function to recreate all collection files."""
    
    # Define all files to create
    files_to_create = {
        'collections/yeast/yeast_batch03_protein_synthesis_degradation.html': create_yeast_batch03(),
        'collections/yeast/yeast_batch04_signal_transduction.html': create_yeast_batch04(),
        'collections/ecoli/ecoli_batch01_dna_replication_repair.html': create_ecoli_batch01(),
    }
    
    print(f"Creating {len(files_to_create)} files...")
    print("=" * 50)
    
    for file_path, content in files_to_create.items():
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created: {file_path}")
    
    print("=" * 50)
    print(f"Successfully created {len(files_to_create)} files!")
    print("\nNote: This is a sample implementation. For a complete solution,")
    print("you would need to add all the specific processes and Mermaid diagrams")
    print("for each batch file based on your existing content.")

if __name__ == "__main__":
    main()
