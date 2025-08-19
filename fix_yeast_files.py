#!/usr/bin/env python3

import re

def fix_yeast_files():
    """Fix the malformed Mermaid diagrams in yeast files"""
    
    # Fix Yeast_Processes_as_Programs.html
    with open('collections/yeast/Yeast_Processes_as_Programs.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix fermentation diagram styling
    fermentation_styling = '''    %% Styling
    style A fill:#ff6b6b,color:#fff
    style E fill:#b197fc,color:#fff
    style F fill:#74c0fc,color:#fff
    style H fill:#b197fc,color:#fff
    style K fill:#51cf66,color:#fff
    style L fill:#51cf66,color:#fff
    style O fill:#b197fc,color:#fff
    
    style B fill:#ffd43b,color:#000
    style D fill:#ffd43b,color:#000
    style M fill:#ffd43b,color:#000
    style P fill:#ffd43b,color:#000
    style Q fill:#ffd43b,color:#000
    style R fill:#ffd43b,color:#000
    style S fill:#ffd43b,color:#000
    
    style C fill:#74c0fc,color:#fff
    style G fill:#74c0fc,color:#fff
    style I fill:#74c0fc,color:#fff
    style J fill:#74c0fc,color:#fff
    style N fill:#74c0fc,color:#fff
    style T fill:#74c0fc,color:#fff
    style U fill:#74c0fc,color:#fff'''
    
    # Replace malformed styling
    content = re.sub(
        r'style\s+fill:#ff6b6b,color:#fff\s+style\s+fill:#ffd43b,color:#000.*?style\s+fill:#ffd43b,color:#000',
        fermentation_styling,
        content,
        flags=re.DOTALL
    )
    
    # Fix DNA replication diagram styling
    dna_replication_styling = '''    %% Styling
    style A fill:#ff6b6b,color:#fff
    style G fill:#b197fc,color:#fff
    style I fill:#b197fc,color:#fff
    style R fill:#b197fc,color:#fff
    
    style B fill:#ffd43b,color:#000
    style C fill:#ffd43b,color:#000
    style D fill:#ffd43b,color:#000
    style E fill:#ffd43b,color:#000
    style F fill:#ffd43b,color:#000
    style K fill:#ffd43b,color:#000
    style L fill:#ffd43b,color:#000
    style M fill:#ffd43b,color:#000
    style N fill:#ffd43b,color:#000
    style O fill:#ffd43b,color:#000
    style P fill:#ffd43b,color:#000
    style Q fill:#ffd43b,color:#000
    style V fill:#ffd43b,color:#000
    style W fill:#ffd43b,color:#000
    style X fill:#ffd43b,color:#000
    style Y fill:#ffd43b,color:#000
    style Z fill:#ffd43b,color:#000
    style AA fill:#ffd43b,color:#000
    style BB fill:#ffd43b,color:#000
    style CC fill:#ffd43b,color:#000
    style DD fill:#ffd43b,color:#000
    
    style H fill:#74c0fc,color:#fff
    style J fill:#74c0fc,color:#fff
    style S fill:#74c0fc,color:#fff
    style T fill:#74c0fc,color:#fff
    style U fill:#74c0fc,color:#fff'''
    
    # Replace DNA replication styling
    content = re.sub(
        r'style\s+fill:#ff6b6b,color:#fff\s+style\s+fill:#ffd43b,color:#000.*?style\s+D fill:#ffd43b,color:#000',
        dna_replication_styling,
        content,
        flags=re.DOTALL
    )
    
    with open('collections/yeast/Yeast_Processes_as_Programs.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Fix yeast_top_10_processes.html
    with open('collections/yeast/yeast_top_10_processes.html', 'r', encoding='utf-8') as f:
        content2 = f.read()
    
    # Add missing Mermaid diagrams for processes 4-10
    autophagy_diagram = '''graph TD
    %% Autophagy Initiation
    A[Nutrient Deprivation] --> B[TORC1 Inhibition]
    B --> C[Atg1 Complex Activation]
    C --> D[Phosphorylation of Atg13]
    D --> E[Atg1-Atg13 Complex Formation]
    E --> F[Vps34 Complex Activation]
    F --> G[PI3P Production]
    G --> H[Phagophore Formation]
    H --> I[Atg8 Conjugation]
    I --> J[Autophagosome Formation]
    J --> K[Cargo Degradation]
    
    %% Styling
    style A fill:#ff6b6b,color:#fff
    style K fill:#b197fc,color:#fff
    
    style B fill:#ffd43b,color:#000
    style C fill:#ffd43b,color:#000
    style D fill:#ffd43b,color:#000
    style F fill:#ffd43b,color:#000
    style I fill:#ffd43b,color:#000
    
    style E fill:#74c0fc,color:#fff
    style G fill:#74c0fc,color:#fff
    style H fill:#74c0fc,color:#fff
    style J fill:#74c0fc,color:#fff'''
    
    upr_diagram = '''graph TD
    %% Unfolded Protein Response
    A[ER Stress] --> B[Unfolded Proteins]
    B --> C[BiP Release]
    C --> D[IRE1 Activation]
    C --> E[PERK Activation]
    D --> F[XBP1 Splicing]
    E --> G[eIF2α Phosphorylation]
    F --> H[UPR Target Genes]
    G --> I[Translation Inhibition]
    H --> J[ER Chaperone Synthesis]
    I --> K[Protein Load Reduction]
    J --> L[ER Stress Resolution]
    K --> L
    
    %% Styling
    style A fill:#ff6b6b,color:#fff
    style L fill:#b197fc,color:#fff
    
    style B fill:#74c0fc,color:#fff
    style D fill:#ffd43b,color:#000
    style E fill:#ffd43b,color:#000
    style F fill:#ffd43b,color:#000
    style G fill:#ffd43b,color:#000
    style H fill:#ffd43b,color:#000
    style I fill:#ffd43b,color:#000
    style J fill:#ffd43b,color:#000
    style K fill:#ffd43b,color:#000
    
    style C fill:#74c0fc,color:#fff'''
    
    g1s_diagram = '''graph TD
    %% G1/S Transition
    A[Growth Signals] --> B[Cyclin D Synthesis]
    B --> C[CDK4/6 Activation]
    C --> D[Rb Phosphorylation]
    D --> E[E2F Release]
    E --> F[Cyclin E Synthesis]
    F --> G[CDK2 Activation]
    G --> H[G1/S Transition]
    H --> I[DNA Replication]
    
    %% Styling
    style A fill:#ff6b6b,color:#fff
    style I fill:#b197fc,color:#fff
    
    style B fill:#b197fc,color:#fff
    style C fill:#ffd43b,color:#000
    style D fill:#ffd43b,color:#000
    style F fill:#b197fc,color:#fff
    style G fill:#ffd43b,color:#000
    
    style E fill:#74c0fc,color:#fff
    style H fill:#b197fc,color:#fff'''
    
    respiration_diagram = '''graph TD
    %% Mitochondrial Respiration Control
    A[Oxygen Availability] --> B{Oxygen Present?}
    B -->|Yes| C[Respiration Pathway]
    B -->|No| D[Fermentation Pathway]
    C --> E[Pyruvate Oxidation]
    E --> F[TCA Cycle]
    F --> G[Electron Transport Chain]
    G --> H[ATP Production]
    D --> I[Pyruvate Reduction]
    I --> J[Ethanol Production]
    J --> K[NAD+ Regeneration]
    
    %% Styling
    style A fill:#ff6b6b,color:#fff
    style H fill:#b197fc,color:#fff
    
    style B fill:#74c0fc,color:#fff
    style C fill:#ffd43b,color:#000
    style D fill:#ffd43b,color:#000
    style E fill:#ffd43b,color:#000
    style F fill:#ffd43b,color:#000
    style G fill:#ffd43b,color:#000
    style I fill:#ffd43b,color:#000
    style J fill:#b197fc,color:#fff
    style K fill:#74c0fc,color:#fff'''
    
    amino_acid_diagram = '''graph TD
    %% Amino Acid Biosynthesis Regulation
    A[Amino Acid Starvation] --> B[Uncharged tRNA]
    B --> C[GCN2 Activation]
    C --> D[eIF2α Phosphorylation]
    D --> E[Translation Inhibition]
    E --> F[GCN4 Translation]
    F --> G[GCN4 Transcription Factor]
    G --> H[Amino Acid Biosynthetic Genes]
    H --> I[Amino Acid Synthesis]
    I --> J[Cell Survival]
    
    %% Styling
    style A fill:#ff6b6b,color:#fff
    style J fill:#b197fc,color:#fff
    
    style B fill:#74c0fc,color:#fff
    style C fill:#ffd43b,color:#000
    style D fill:#ffd43b,color:#000
    style F fill:#b197fc,color:#fff
    style G fill:#b197fc,color:#fff
    style H fill:#ffd43b,color:#000
    style I fill:#b197fc,color:#fff
    
    style E fill:#b197fc,color:#fff'''
    
    gluconeogenesis_diagram = '''graph TD
    %% Gluconeogenesis
    A[Pyruvate] --> B[Pyruvate Carboxylase]
    B --> C[Oxaloacetate]
    C --> D[PEP Carboxykinase]
    D --> E[Phosphoenolpyruvate]
    E --> F[Gluconeogenic Enzymes]
    F --> G[Fructose-1,6-Bisphosphate]
    G --> H[Fructose-1,6-Bisphosphatase]
    H --> I[Fructose-6-Phosphate]
    I --> J[Glucose-6-Phosphatase]
    J --> K[Glucose]
    
    %% Styling
    style A fill:#ff6b6b,color:#fff
    style K fill:#b197fc,color:#fff
    
    style B fill:#ffd43b,color:#000
    style D fill:#ffd43b,color:#000
    style F fill:#ffd43b,color:#000
    style H fill:#ffd43b,color:#000
    style J fill:#ffd43b,color:#000
    
    style C fill:#74c0fc,color:#fff
    style E fill:#74c0fc,color:#fff
    style G fill:#74c0fc,color:#fff
    style I fill:#74c0fc,color:#fff'''
    
    fermentation_diagram = '''graph TD
    %% Alcoholic Fermentation
    A[Pyruvate] --> B[Pyruvate Decarboxylase]
    B --> C[Acetaldehyde]
    C --> D[Alcohol Dehydrogenase]
    D --> E[Ethanol]
    E --> F[NAD+ Regeneration]
    F --> G[Glycolysis Continuation]
    G --> H[ATP Production]
    
    %% Styling
    style A fill:#ff6b6b,color:#fff
    style H fill:#b197fc,color:#fff
    
    style B fill:#ffd43b,color:#000
    style D fill:#ffd43b,color:#000
    style G fill:#ffd43b,color:#000
    
    style C fill:#74c0fc,color:#fff
    style E fill:#b197fc,color:#fff
    style F fill:#74c0fc,color:#fff'''
    
    # Replace empty Mermaid containers with actual diagrams
    content2 = content2.replace('<div class="mermaid" id="autophagy">\n        \n    </div>', f'<div class="mermaid">\n{autophagy_diagram}\n    </div>')
    content2 = content2.replace('<div class="mermaid" id="upr">\n        \n    </div>', f'<div class="mermaid">\n{upr_diagram}\n    </div>')
    content2 = content2.replace('<div class="mermaid" id="g1s">\n        \n    </div>', f'<div class="mermaid">\n{g1s_diagram}\n    </div>')
    content2 = content2.replace('<div class="mermaid" id="respiration">\n        \n    </div>', f'<div class="mermaid">\n{respiration_diagram}\n    </div>')
    content2 = content2.replace('<div class="mermaid" id="amino_acid">\n        \n    </div>', f'<div class="mermaid">\n{amino_acid_diagram}\n    </div>')
    content2 = content2.replace('<div class="mermaid" id="gluconeogenesis">\n        \n    </div>', f'<div class="mermaid">\n{gluconeogenesis_diagram}\n    </div>')
    content2 = content2.replace('<div class="mermaid" id="fermentation">\n        \n    </div>', f'<div class="mermaid">\n{fermentation_diagram}\n    </div>')
    
    with open('collections/yeast/yeast_top_10_processes.html', 'w', encoding='utf-8') as f:
        f.write(content2)
    
    print("Fixed both yeast files")

if __name__ == "__main__":
    fix_yeast_files()
