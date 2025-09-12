#!/usr/bin/env python3
"""
Generate standardized batch files using the template
"""

import os
import re

def create_batch_file(batch_config):
    """Create a batch file from the template and configuration"""
    
    # Read the template
    with open('/workspace/standard_batch_template.html', 'r') as f:
        template = f.read()
    
    # Replace all placeholders
    content = template
    for placeholder, value in batch_config.items():
        content = content.replace(f'[{placeholder}]', str(value))
    
    # Generate the JavaScript for all 8 processes
    js_processes = generate_javascript_processes(batch_config)
    content = content.replace('// TEMPLATE CONTINUES FOR PROCESSES 2-8 WITH SAME STRUCTURE', js_processes)
    
    # Generate the captions
    js_captions = generate_captions(batch_config)
    content = content.replace('// TEMPLATE CONTINUES FOR PROCESSES 2-8', js_captions)
    
    return content

def generate_javascript_processes(config):
    """Generate JavaScript for processes 2-8"""
    js_code = ""
    
    for i in range(2, 9):  # Processes 2-8
        process_name = config.get(f'PROCESS_{i}_NAME', f'Process {i}')
        
        js_code += f"""
            {i}: {{
                levels: {{
                    1: `graph TD
                        P{i}A[{config.get(f'PROCESS_{i}_L1_NODE_1', 'Signal Input')}] --> P{i}B[{config.get(f'PROCESS_{i}_L1_NODE_2', process_name + ' Initiation')}]
                        P{i}B --> P{i}C[{config.get(f'PROCESS_{i}_L1_NODE_3', 'Basic Response')}]
                        P{i}C --> P{i}D[{config.get(f'PROCESS_{i}_L1_NODE_4', 'Process Output')}]
                        
                        style P{i}A fill:#ff6b6b,color:#fff
                        style P{i}B fill:#ffd43b,color:#000
                        style P{i}C fill:#51cf66,color:#fff
                        style P{i}D fill:#b197fc,color:#fff`,
                        
                    2: `graph TD
                        P{i}E[{config.get(f'PROCESS_{i}_L2_NODE_1', 'Signal Input')}] --> P{i}F[{config.get(f'PROCESS_{i}_L2_NODE_2', 'Receptor Recognition')}]
                        P{i}F --> P{i}G[{config.get(f'PROCESS_{i}_L2_NODE_3', process_name + ' Activation')}]
                        P{i}G --> P{i}H[{config.get(f'PROCESS_{i}_L2_NODE_4', 'Molecular Assembly')}]
                        P{i}H --> P{i}I[{config.get(f'PROCESS_{i}_L2_NODE_5', 'Catalytic Activity')}]
                        P{i}I --> P{i}J[{config.get(f'PROCESS_{i}_L2_NODE_6', 'Process Output')}]
                        
                        style P{i}E fill:#ff6b6b,color:#fff
                        style P{i}F fill:#ffd43b,color:#000
                        style P{i}G fill:#74c0fc,color:#fff
                        style P{i}H fill:#51cf66,color:#fff
                        style P{i}I fill:#51cf66,color:#fff
                        style P{i}J fill:#b197fc,color:#fff`,
                        
                    3: `graph TD
                        P{i}K[{config.get(f'PROCESS_{i}_L3_NODE_1', 'Environmental Signal')}] --> P{i}L[{config.get(f'PROCESS_{i}_L3_NODE_2', 'Sensor Protein')}]
                        P{i}L --> P{i}M[{config.get(f'PROCESS_{i}_L3_NODE_3', 'Signal Transduction')}]
                        P{i}M --> P{i}N[{config.get(f'PROCESS_{i}_L3_NODE_4', process_name + ' Complex')}]
                        P{i}N --> P{i}O[{config.get(f'PROCESS_{i}_L3_NODE_5', 'Substrate Binding')}]
                        P{i}O --> P{i}P[{config.get(f'PROCESS_{i}_L3_NODE_6', 'Enzymatic Activity')}]
                        P{i}P --> P{i}Q[{config.get(f'PROCESS_{i}_L3_NODE_7', 'Product Formation')}]
                        P{i}Q --> P{i}R[{config.get(f'PROCESS_{i}_L3_NODE_8', 'Regulatory Feedback')}]
                        P{i}R --> P{i}S[{config.get(f'PROCESS_{i}_L3_NODE_9', 'Process Completion')}]
                        
                        style P{i}K fill:#ff6b6b,color:#fff
                        style P{i}L fill:#ffd43b,color:#000
                        style P{i}M fill:#74c0fc,color:#fff
                        style P{i}N fill:#51cf66,color:#fff
                        style P{i}O fill:#74c0fc,color:#fff
                        style P{i}P fill:#51cf66,color:#fff
                        style P{i}Q fill:#51cf66,color:#fff
                        style P{i}R fill:#ffd43b,color:#000
                        style P{i}S fill:#b197fc,color:#fff`,
                        
                    4: `graph TD
                        P{i}T[{config.get(f'PROCESS_{i}_L4_NODE_1', 'Cellular Signal')}] --> P{i}U[{config.get(f'PROCESS_{i}_L4_NODE_2', 'Receptor Complex')}]
                        P{i}U --> P{i}V[{config.get(f'PROCESS_{i}_L4_NODE_3', 'Signal Cascade')}]
                        P{i}V --> P{i}W[{config.get(f'PROCESS_{i}_L4_NODE_4', 'Protein Recruitment')}]
                        P{i}W --> P{i}X[{config.get(f'PROCESS_{i}_L4_NODE_5', process_name + ' Assembly')}]
                        P{i}X --> P{i}Y[{config.get(f'PROCESS_{i}_L4_NODE_6', 'Conformational Change')}]
                        P{i}Y --> P{i}Z[{config.get(f'PROCESS_{i}_L4_NODE_7', 'Active Site Formation')}]
                        P{i}Z --> P{i}AA[{config.get(f'PROCESS_{i}_L4_NODE_8', 'Substrate Recognition')}]
                        P{i}AA --> P{i}BB[{config.get(f'PROCESS_{i}_L4_NODE_9', 'Catalytic Mechanism')}]
                        P{i}BB --> P{i}CC[{config.get(f'PROCESS_{i}_L4_NODE_10', 'Product Release')}]
                        P{i}CC --> P{i}DD[{config.get(f'PROCESS_{i}_L4_NODE_11', 'Allosteric Regulation')}]
                        P{i}DD --> P{i}EE[{config.get(f'PROCESS_{i}_L4_NODE_12', 'Process Completion')}]
                        
                        style P{i}T fill:#ff6b6b,color:#fff
                        style P{i}U fill:#ffd43b,color:#000
                        style P{i}V fill:#74c0fc,color:#fff
                        style P{i}W fill:#51cf66,color:#fff
                        style P{i}X fill:#74c0fc,color:#fff
                        style P{i}Y fill:#51cf66,color:#fff
                        style P{i}Z fill:#51cf66,color:#fff
                        style P{i}AA fill:#74c0fc,color:#fff
                        style P{i}BB fill:#51cf66,color:#fff
                        style P{i}CC fill:#51cf66,color:#fff
                        style P{i}DD fill:#ffd43b,color:#000
                        style P{i}EE fill:#b197fc,color:#fff`,
                        
                    5: `graph TD
                        P{i}FF[{config.get(f'PROCESS_{i}_L5_NODE_1', 'Extracellular Signal')}] --> P{i}GG[{config.get(f'PROCESS_{i}_L5_NODE_2', 'Membrane Receptor')}]
                        P{i}GG --> P{i}HH[{config.get(f'PROCESS_{i}_L5_NODE_3', 'Conformational Activation')}]
                        P{i}HH --> P{i}II[{config.get(f'PROCESS_{i}_L5_NODE_4', 'Intracellular Domain')}]
                        P{i}II --> P{i}JJ[{config.get(f'PROCESS_{i}_L5_NODE_5', 'Second Messenger System')}]
                        P{i}JJ --> P{i}KK[{config.get(f'PROCESS_{i}_L5_NODE_6', 'Kinase Cascade')}]
                        P{i}KK --> P{i}LL[{config.get(f'PROCESS_{i}_L5_NODE_7', 'Protein Phosphorylation')}]
                        P{i}LL --> P{i}MM[{config.get(f'PROCESS_{i}_L5_NODE_8', process_name + ' Activation')}]
                        P{i}MM --> P{i}NN[{config.get(f'PROCESS_{i}_L5_NODE_9', 'Substrate Specificity')}]
                        P{i}NN --> P{i}OO[{config.get(f'PROCESS_{i}_L5_NODE_10', 'Enzyme-Substrate Complex')}]
                        P{i}OO --> P{i}PP[{config.get(f'PROCESS_{i}_L5_NODE_11', 'Transition State')}]
                        P{i}PP --> P{i}QQ[{config.get(f'PROCESS_{i}_L5_NODE_12', 'Catalytic Conversion')}]
                        P{i}QQ --> P{i}RR[{config.get(f'PROCESS_{i}_L5_NODE_13', 'Product Formation')}]
                        P{i}RR --> P{i}SS[{config.get(f'PROCESS_{i}_L5_NODE_14', 'Regulatory Network')}]
                        P{i}SS --> P{i}TT[{config.get(f'PROCESS_{i}_L5_NODE_15', 'System Balance')}]
                        
                        style P{i}FF fill:#ff6b6b,color:#fff
                        style P{i}GG fill:#ffd43b,color:#000
                        style P{i}HH fill:#51cf66,color:#fff
                        style P{i}II fill:#74c0fc,color:#fff
                        style P{i}JJ fill:#ffd43b,color:#000
                        style P{i}KK fill:#74c0fc,color:#fff
                        style P{i}LL fill:#51cf66,color:#fff
                        style P{i}MM fill:#ffd43b,color:#000
                        style P{i}NN fill:#74c0fc,color:#fff
                        style P{i}OO fill:#51cf66,color:#fff
                        style P{i}PP fill:#51cf66,color:#fff
                        style P{i}QQ fill:#51cf66,color:#fff
                        style P{i}RR fill:#51cf66,color:#fff
                        style P{i}SS fill:#74c0fc,color:#fff
                        style P{i}TT fill:#b197fc,color:#fff`
                }}
            }},"""
    
    return js_code

def generate_captions(config):
    """Generate captions for processes 2-8"""
    captions_code = ""
    
    for i in range(2, 9):
        captions_code += f"""
            {i}: {{
                1: "{config.get(f'PROCESS_{i}_CAPTION_L1', f'Level 1: Basic overview of {config.get(f"PROCESS_{i}_NAME", f"Process {i}")}').lower()}',
                2: "{config.get(f'PROCESS_{i}_CAPTION_L2', f'Level 2: Detailed {config.get(f"PROCESS_{i}_NAME", f"Process {i}")} mechanism').lower()}',
                3: "{config.get(f'PROCESS_{i}_CAPTION_L3', f'Level 3: Comprehensive {config.get(f"PROCESS_{i}_NAME", f"Process {i}")} pathway').lower()}',
                4: "{config.get(f'PROCESS_{i}_CAPTION_L4', f'Level 4: Advanced {config.get(f"PROCESS_{i}_NAME", f"Process {i}")} regulation').lower()}',
                5: "{config.get(f'PROCESS_{i}_CAPTION_L5', f'Level 5: Complete molecular detail of {config.get(f"PROCESS_{i}_NAME", f"Process {i}")}').lower()}'
            }},"""
    
    return captions_code

# Example configuration for E. coli Batch 02
ecoli_batch02_config = {
    'SPECIES': 'E. coli',
    'SPECIES_EMOJI': '🦠',
    'SPECIES_LOWER': 'E. coli',
    'BATCH_NUMBER': '02',
    'BATCH_TITLE': 'Cell Division & Segregation',
    'CATEGORY': 'Cell Division',
    'CATEGORY_LOWER': 'cell division',
    'DESCRIPTION_EMOJI': '🧬',
    'SPECIFIC_FEATURES': 'septum formation, chromosome segregation, and cytokinesis mechanisms',
    
    # Process Names
    'PROCESS_1_NAME': 'FtsZ Ring Assembly',
    'PROCESS_2_NAME': 'Septum Formation',
    'PROCESS_3_NAME': 'Chromosome Segregation',
    'PROCESS_4_NAME': 'Cell Wall Synthesis',
    'PROCESS_5_NAME': 'Membrane Division',
    'PROCESS_6_NAME': 'Cytokinesis',
    'PROCESS_7_NAME': 'Daughter Cell Separation',
    'PROCESS_8_NAME': 'Cell Cycle Completion',
    
    # Process Descriptions
    'PROCESS_1_DESCRIPTION': 'cytoskeletal ring formation and contractile machinery assembly',
    'PROCESS_2_DESCRIPTION': 'septal peptidoglycan synthesis and membrane invagination',
    'PROCESS_3_DESCRIPTION': 'chromosome partitioning and nucleoid segregation',
    'PROCESS_4_DESCRIPTION': 'peptidoglycan synthesis and cell wall remodeling',
    'PROCESS_5_DESCRIPTION': 'membrane constriction and lipid distribution',
    'PROCESS_6_DESCRIPTION': 'cellular division and compartmentalization',
    'PROCESS_7_DESCRIPTION': 'final separation and cell wall completion',
    'PROCESS_8_DESCRIPTION': 'cell cycle checkpoint completion and division termination',
    
    # Level 1 Captions
    'PROCESS_1_CAPTION_L1': 'Level 1: Basic FtsZ ring assembly and contractile machinery formation',
    'PROCESS_2_CAPTION_L1': 'Level 1: Basic septum formation with peptidoglycan synthesis',
    'PROCESS_3_CAPTION_L1': 'Level 1: Basic chromosome segregation and nucleoid partitioning',
    'PROCESS_4_CAPTION_L1': 'Level 1: Basic cell wall synthesis and peptidoglycan assembly',
    'PROCESS_5_CAPTION_L1': 'Level 1: Basic membrane division and lipid redistribution',
    'PROCESS_6_CAPTION_L1': 'Level 1: Basic cytokinesis and cellular compartmentalization',
    'PROCESS_7_CAPTION_L1': 'Level 1: Basic daughter cell separation and wall completion',
    'PROCESS_8_CAPTION_L1': 'Level 1: Basic cell cycle completion and division checkpoint',
    
    # Sources
    'PRIMARY_SOURCES': 'Molecular Biology of the Cell (Alberts et al., 6th Ed.), Bacterial Cell Division (Lutkenhaus et al.), EcoCyc Database (ecocyc.org)',
    'KEY_RESEARCH_PAPERS': 'Lutkenhaus et al. (2012) Nature Rev. Microbiol. - FtsZ dynamics; Typas et al. (2011) Nature Rev. Microbiol. - peptidoglycan synthesis; Sherratt (2003) Nature Rev. Mol. Cell Biol. - chromosome segregation',
    'DATABASES_USED': 'UniProt, NCBI Gene, EcoCyc, KEGG Pathway Database'
}

def main():
    """Generate E. coli Batch 02 as an example"""
    
    # Generate the file
    content = create_batch_file(ecoli_batch02_config)
    
    # Save the file
    with open('/workspace/ecoli_batch02_cell_division_segregation_NEW.html', 'w') as f:
        f.write(content)
    
    print("Generated: ecoli_batch02_cell_division_segregation_NEW.html")
    print("Template system ready for generating all remaining batches!")

if __name__ == '__main__':
    main()