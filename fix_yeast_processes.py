#!/usr/bin/env python3

import re

def fix_yeast_processes():
    """Fix the malformed Mermaid diagrams in Yeast_Processes_as_Programs.html"""
    
    # Read the file
    with open('collections/yeast/Yeast_Processes_as_Programs.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Fermentation diagram
    fermentation_diagram = '''        graph TD
    A[Pyruvate from Glycolysis] --> B[Pyruvate Decarboxylase PDC1]
    B --> C[Acetaldehyde]
    C --> D[Alcohol Dehydrogenase ADH1]
    D --> E[Ethanol]
    E --> F[NAD+ Regeneration]
    F --> G[Glycolysis Continuation]
    G --> H[ATP Production]
    
    %% Feedback regulation
    H --> I[Energy Status Monitoring]
    I --> J{Energy Sufficient?}
    J -->|No| K[Continue Fermentation]
    J -->|Yes| L[Reduce Fermentation]
    
    %% Alternative pathways
    C --> M[Acetaldehyde Dehydrogenase]
    M --> N[Acetic Acid]
    N --> O[Acetate Production]
    
    %% Key proteins and regulation
    P[PDC1] --> B
    Q[PDC5] --> B
    R[ADH1] --> D
    S[ADH2] --> D
    T[NAD+] --> F
    U[ATP] --> H
    
    %% Styling
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
    
    # Fix 2: DNA Replication diagram
    dna_replication_diagram = '''        graph TD
    A[Cell Cycle G1 Phase] --> B[Origin Recognition Complex ORC]
    B --> C[ORC Binding to Origins]
    C --> D[Cdc6 Recruitment]
    D --> E[Cdt1 Loading]
    E --> F[Pre-Replicative Complex Pre-RC]
    F --> G[Licensing Complete]
    G --> H{Cell Cycle Checkpoint?}
    H -->|No| I[G1/S Transition]
    H -->|Yes| J[G1 Arrest]
    I --> K[Cdc7-Dbf4 Activation]
    K --> L[S-Cdk Activation]
    L --> M[Pre-RC Phosphorylation]
    M --> N[Helicase Activation]
    N --> O[DNA Unwinding]
    O --> P[Replication Fork Formation]
    P --> Q[DNA Polymerase Loading]
    Q --> R[Replication Elongation]
    
    %% Feedback regulation
    R --> S[Replication Stress]
    S --> T[Checkpoint Activation]
    T --> U[Replication Slowdown]
    
    %% Key proteins
    V[ORC1-6] --> B
    W[Cdc6] --> D
    X[Cdt1] --> E
    Y[Mcm2-7] --> F
    Z[Cdc7] --> K
    AA[Dbf4] --> K
    BB[S-Cdk] --> L
    CC[Mcm10] --> N
    DD[Cdc45] --> N
    
    %% Styling
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
    
    # Fix 3: G1/S Transition diagram
    g1s_transition_diagram = '''        graph TD
    A[Growth Signals] --> B[Cyclin D Synthesis]
    B --> C[CDK4/6 Activation]
    C --> D[Rb Phosphorylation]
    D --> E[E2F Release]
    E --> F[S-Phase Gene Expression]
    F --> G[Cyclin E Synthesis]
    G --> H[CDK2 Activation]
    H --> I[G1/S Transition]
    I --> J[DNA Replication Initiation]
    
    %% Checkpoint mechanisms
    K[DNA Damage] --> L[p53 Activation]
    L --> M[p21 Induction]
    M --> N[CDK Inhibition]
    N --> O[G1 Arrest]
    
    %% Growth factor dependency
    P[Growth Factor Withdrawal] --> Q[Cyclin D Degradation]
    Q --> R[CDK Inactivation]
    R --> S[Rb Hypophosphorylation]
    S --> T[E2F Sequestration]
    T --> U[Cell Cycle Exit]
    
    %% Quality control
    J --> V[Replication Licensing Check]
    V --> W{All Origins Licensed?}
    W -->|Yes| X[Proceed to S Phase]
    W -->|No| Y[Licensing Repair]
    Y --> V
    
    %% Key regulators
    Z[Cyclin D] --> B
    AA[CDK4/6] --> C
    BB[Rb] --> D
    CC[E2F] --> E
    DD[p53] --> L
    EE[p21] --> M
    
    %% Styling
    style A fill:#ff6b6b,color:#fff
    style I fill:#b197fc,color:#fff
    style J fill:#b197fc,color:#fff
    style X fill:#b197fc,color:#fff
    
    style B fill:#ffd43b,color:#000
    style C fill:#ffd43b,color:#000
    style D fill:#ffd43b,color:#000
    style F fill:#ffd43b,color:#000
    style G fill:#ffd43b,color:#000
    style H fill:#ffd43b,color:#000
    style L fill:#ffd43b,color:#000
    style M fill:#ffd43b,color:#000
    style N fill:#ffd43b,color:#000
    style Q fill:#ffd43b,color:#000
    style R fill:#ffd43b,color:#000
    style S fill:#ffd43b,color:#000
    style T fill:#ffd43b,color:#000
    style Y fill:#ffd43b,color:#000
    style Z fill:#ffd43b,color:#000
    style AA fill:#ffd43b,color:#000
    style BB fill:#ffd43b,color:#000
    style CC fill:#ffd43b,color:#000
    style DD fill:#ffd43b,color:#000
    style EE fill:#ffd43b,color:#000
    
    style E fill:#74c0fc,color:#fff
    style O fill:#74c0fc,color:#fff
    style U fill:#74c0fc,color:#fff
    style V fill:#74c0fc,color:#fff
    style W fill:#74c0fc,color:#fff
    style K fill:#ff6b6b,color:#fff
    style P fill:#ff6b6b,color:#fff'''
    
    # Replace the diagrams
    content = re.sub(
        r'graph TD\s+A\[Pyruvate from Glycolysis\].*?style.*?fill:#ffd43b,color:#000',
        fermentation_diagram,
        content,
        flags=re.DOTALL
    )
    
    content = re.sub(
        r'graph TD\s+A\[Cell Cycle G1 Phase\].*?style.*?fill:#ffd43b,color:#000',
        dna_replication_diagram,
        content,
        flags=re.DOTALL
    )
    
    content = re.sub(
        r'graph TD\s+A\[Growth Signals\].*?style.*?fill:#ffd43b,color:#000',
        g1s_transition_diagram,
        content,
        flags=re.DOTALL
    )
    
    # Write the fixed content back
    with open('collections/yeast/Yeast_Processes_as_Programs.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed Yeast_Processes_as_Programs.html")

if __name__ == "__main__":
    fix_yeast_processes()
