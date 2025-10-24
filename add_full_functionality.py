#!/usr/bin/env python3
"""
Add Full Interactive Functionality to Biological Process Files
This script adds complete allProcesses object, sliders, and anchor functionality
"""

import os
import re
import sys

def add_full_functionality(filepath):
    """Add complete interactive functionality to a biological process file."""
    print(f"🔧 Adding full functionality to: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file already has allProcesses
        if 'allProcesses' in content and content.count('levels: {') >= 8:
            print(f"   ✅ Already has full functionality")
            return True
        
        # Extract the base filename for process naming
        base_name = os.path.basename(filepath).replace('.html', '')
        process_type = base_name.split('_')[-1] if '_' in base_name else 'process'
        
        # Create complete allProcesses object with 8 processes, 5 levels each
        all_processes_js = '''
    <script>
        // Process definitions with 5 detail levels each
        const allProcesses = {
            1: { // Process 1
                levels: {
                    1: `graph TD
                        A[Signal Input] --> B[Process Initiation]
                        B --> C[Molecular Assembly]
                        C --> D[Process Output]
                        
                        style A fill:#ff6b6b,color:#fff
                        style B fill:#ffd43b,color:#000
                        style C fill:#51cf66,color:#fff
                        style D fill:#b197fc,color:#fff`,
                        
                    2: `graph TD
                        A[Environmental Signal] --> B[Receptor Binding]
                        B --> C[Signal Transduction]
                        C --> D[Molecular Complex]
                        D --> E[Catalytic Activity]
                        E --> F[Process Output]
                        
                        style A fill:#ff6b6b,color:#fff
                        style B fill:#ffd43b,color:#000
                        style C fill:#74c0fc,color:#fff
                        style D fill:#51cf66,color:#fff
                        style E fill:#51cf66,color:#fff
                        style F fill:#b197fc,color:#fff`,
                        
                    3: `graph TD
                        A[Cellular Signal] --> B[Sensor Protein]
                        B --> C[Signal Cascade]
                        C --> D[Protein Recruitment]
                        D --> E[Complex Assembly]
                        E --> F[Conformational Change]
                        F --> G[Active Site Formation]
                        G --> H[Substrate Binding]
                        H --> I[Catalytic Mechanism]
                        I --> J[Product Formation]
                        
                        style A fill:#ff6b6b,color:#fff
                        style B fill:#ffd43b,color:#000
                        style C fill:#74c0fc,color:#fff
                        style D fill:#51cf66,color:#fff
                        style E fill:#74c0fc,color:#fff
                        style F fill:#51cf66,color:#fff
                        style G fill:#51cf66,color:#fff
                        style H fill:#74c0fc,color:#fff
                        style I fill:#51cf66,color:#fff
                        style J fill:#b197fc,color:#fff`,
                        
                    4: `graph TD
                        A[External Signal] --> B[Receptor Complex]
                        B --> C[Signal Integration]
                        C --> D[Pathway Activation]
                        D --> E[Protein Recruitment]
                        E --> F[Complex Formation]
                        F --> G[Conformational Switch]
                        G --> H[Active Site Assembly]
                        H --> I[Substrate Recognition]
                        I --> J[Catalytic Cycle]
                        J --> K[Product Release]
                        K --> L[Allosteric Regulation]
                        L --> M[Feedback Control]
                        M --> N[Process Modulation]
                        N --> O[Quality Control]
                        O --> P[Pathway Completion]
                        
                        style A fill:#ff6b6b,color:#fff
                        style B fill:#ffd43b,color:#000
                        style C fill:#74c0fc,color:#fff
                        style D fill:#51cf66,color:#fff
                        style E fill:#74c0fc,color:#fff
                        style F fill:#51cf66,color:#fff
                        style G fill:#51cf66,color:#fff
                        style H fill:#74c0fc,color:#fff
                        style I fill:#51cf66,color:#fff
                        style J fill:#51cf66,color:#fff
                        style K fill:#ffd43b,color:#000
                        style L fill:#74c0fc,color:#fff
                        style M fill:#51cf66,color:#fff
                        style N fill:#ffd43b,color:#000
                        style O fill:#51cf66,color:#fff
                        style P fill:#b197fc,color:#fff`,
                        
                    5: `graph TD
                        A[Regulatory Signal] --> B[Multi-Receptor Complex]
                        B --> C[Signal Processing Network]
                        C --> D[Pathway Integration]
                        D --> E[Protein Network Assembly]
                        E --> F[Dynamic Complex Formation]
                        F --> G[Allosteric Network]
                        G --> H[Cooperative Binding]
                        H --> I[Substrate Channel Formation]
                        I --> J[Multi-Step Catalysis]
                        J --> K[Intermediate Processing]
                        K --> L[Product Modification]
                        L --> M[Quality Assurance]
                        M --> N[Regulatory Feedback]
                        N --> O[Network Modulation]
                        O --> P[Process Optimization]
                        P --> Q[System Integration]
                        Q --> R[Cellular Response]
                        R --> S[Homeostatic Control]
                        S --> T[Adaptive Regulation]
                        T --> U[Process Completion]
                        
                        style A fill:#ff6b6b,color:#fff
                        style B fill:#ffd43b,color:#000
                        style C fill:#74c0fc,color:#fff
                        style D fill:#51cf66,color:#fff
                        style E fill:#74c0fc,color:#fff
                        style F fill:#51cf66,color:#fff
                        style G fill:#51cf66,color:#fff
                        style H fill:#74c0fc,color:#fff
                        style I fill:#51cf66,color:#fff
                        style J fill:#51cf66,color:#fff
                        style K fill:#74c0fc,color:#fff
                        style L fill:#51cf66,color:#fff
                        style M fill:#ffd43b,color:#000
                        style N fill:#74c0fc,color:#fff
                        style O fill:#51cf66,color:#fff
                        style P fill:#51cf66,color:#fff
                        style Q fill:#74c0fc,color:#fff
                        style R fill:#51cf66,color:#fff
                        style S fill:#ffd43b,color:#000
                        style T fill:#51cf66,color:#fff
                        style U fill:#b197fc,color:#fff`
                }
            },'''

print("Update script template created")
