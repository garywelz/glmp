#!/usr/bin/env python3
"""
Create a Medium-friendly simplified β-galactosidase flowchart
"""

import webbrowser
import os

def create_simplified_flowchart():
    """Create a simplified flowchart that works well on Medium"""
    
    # Simplified Mermaid code focused on key computational logic
    simplified_mermaid = '''graph TD
    %% Environmental Inputs
    A[Lactose Present] --> B{Is Lactose Available?}
    C[Glucose Present] --> D{Is Glucose Available?}
    E[Low Energy] --> F{Is Energy Low?}
    
    %% Decision Logic
    B -->|Yes| G[Lac Repressor Inactive]
    B -->|No| H[Lac Repressor Active]
    D -->|Yes| I[Low cAMP]
    D -->|No| J[High cAMP]
    F --> J
    
    %% Regulatory Integration
    G --> K{Operator Free?}
    H --> L[Transcription Blocked]
    I --> M[No CAP Binding]
    J --> N[cAMP-CAP Complex]
    
    %% Transcription Control
    K -->|Yes| O[RNA Polymerase Binding]
    K -->|No| L
    N --> P{CAP Bound?}
    P -->|Yes| O
    P -->|No| Q[Weak Transcription]
    
    %% Gene Expression
    O --> R[Transcription Initiation]
    Q --> R
    R --> S[lacZ mRNA]
    R --> T[lacY mRNA]
    R --> U[lacA mRNA]
    
    %% Protein Production
    S --> V[Beta-Galactosidase]
    T --> W[Lactose Permease]
    U --> X[Galactoside Acetyltransferase]
    
    %% Functional Outputs
    V --> Y[Lactose Hydrolysis]
    W --> Z[Lactose Transport]
    X --> AA[Detoxification]
    
    %% Metabolic Results
    Y --> BB[Glucose + Galactose]
    Z --> CC[Lactose Uptake]
    AA --> DD[Cell Protection]
    
    %% Feedback Loops
    BB --> EE[Energy Production]
    CC --> FF[Lactose Consumption]
    DD --> GG[Cell Survival]
    
    %% System Status
    EE --> HH[Energy Status Improved]
    FF --> II[Lactose Depletion]
    GG --> JJ[Cell Health]
    
    %% Regulatory Feedback
    HH --> KK[Reduced Energy Stress]
    II --> LL[Reduced Lactose Signal]
    JJ --> MM[Maintained Homeostasis]
    
    %% Return to Logic
    KK --> F
    LL --> B
    MM --> NN[System Equilibrium]
    
    %% Color Coding
    style A fill:#ff6b6b,stroke:#a00,stroke-width:2px,color:#000
    style C fill:#ff6b6b,stroke:#a00,stroke-width:2px,color:#000
    style E fill:#ff6b6b,stroke:#a00,stroke-width:2px,color:#000
    style G fill:#4ecdc4,stroke:#2b7a78,stroke-width:2px,color:#000
    style H fill:#4ecdc4,stroke:#2b7a78,stroke-width:2px,color:#000
    style I fill:#4ecdc4,stroke:#2b7a78,stroke-width:2px,color:#000
    style J fill:#4ecdc4,stroke:#2b7a78,stroke-width:2px,color:#000
    style N fill:#4ecdc4,stroke:#2b7a78,stroke-width:2px,color:#000
    style O fill:#4ecdc4,stroke:#2b7a78,stroke-width:2px,color:#000
    style Q fill:#4ecdc4,stroke:#2b7a78,stroke-width:2px,color:#000
    style R fill:#4ecdc4,stroke:#2b7a78,stroke-width:2px,color:#000
    style V fill:#feca57,stroke:#b59d00,stroke-width:2px,color:#000
    style W fill:#feca57,stroke:#b59d00,stroke-width:2px,color:#000
    style X fill:#feca57,stroke:#b59d00,stroke-width:2px,color:#000
    style Y fill:#4ecdc4,stroke:#2b7a78,stroke-width:2px,color:#000
    style Z fill:#4ecdc4,stroke:#2b7a78,stroke-width:2px,color:#000
    style AA fill:#4ecdc4,stroke:#2b7a78,stroke-width:2px,color:#000
    style BB fill:#45b7d1,stroke:#0d47a1,stroke-width:2px,color:#000
    style CC fill:#45b7d1,stroke:#0d47a1,stroke-width:2px,color:#000
    style DD fill:#45b7d1,stroke:#0d47a1,stroke-width:2px,color:#000
    style EE fill:#96ceb4,stroke:#2e7d32,stroke-width:2px,color:#000
    style FF fill:#96ceb4,stroke:#2e7d32,stroke-width:2px,color:#000
    style GG fill:#96ceb4,stroke:#2e7d32,stroke-width:2px,color:#000
    style HH fill:#45b7d1,stroke:#0d47a1,stroke-width:2px,color:#000
    style II fill:#45b7d1,stroke:#0d47a1,stroke-width:2px,color:#000
    style JJ fill:#45b7d1,stroke:#0d47a1,stroke-width:2px,color:#000
    style KK fill:#45b7d1,stroke:#0d47a1,stroke-width:2px,color:#000
    style LL fill:#45b7d1,stroke:#0d47a1,stroke-width:2px,color:#000
    style MM fill:#45b7d1,stroke:#0d47a1,stroke-width:2px,color:#000
    style NN fill:#96ceb4,stroke:#2e7d32,stroke-width:2px,color:#000'''
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medium-Friendly β-Galactosidase Flowchart</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: white;
            font-family: Arial, sans-serif;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }}
        .mermaid {{
            background: white;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .download-btn {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }}
        .download-btn:hover {{
            background: #0056b3;
        }}
        .instructions {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #007bff;
        }}
        .legend {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            text-align: left;
        }}
        h1 {{
            color: #333;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <button class="download-btn" onclick="downloadSVG()">💾 Download SVG</button>
    
    <div class="container">
        <h1>Medium-Friendly β-Galactosidase Flowchart</h1>
        
        <div class="instructions">
            <h3>📋 Instructions for Medium:</h3>
            <ol style="text-align: left;">
                <li><strong>Take a screenshot</strong> of the flowchart below</li>
                <li><strong>Save as PNG</strong> file</li>
                <li><strong>Upload to Medium</strong> as an image</li>
                <li><strong>Add caption</strong>: "The 2025 version: Simplified computational logic of the lac operon"</li>
            </ol>
        </div>
        
        <div class="mermaid">
{simplified_mermaid}
        </div>
        
        <div class="legend">
            <h3>🎨 Programming Framework Color Coding:</h3>
            <ul>
                <li><strong style="color: #ff6b6b;">Red:</strong> Environmental triggers (inputs)</li>
                <li><strong style="color: #4ecdc4;">Teal:</strong> Regulatory processes & enzymes</li>
                <li><strong style="color: #feca57;">Yellow:</strong> Key proteins & enzymes</li>
                <li><strong style="color: #45b7d1;">Blue:</strong> Intermediates & metabolites</li>
                <li><strong style="color: #96ceb4;">Green:</strong> Products & outputs</li>
            </ul>
        </div>
        
        <div style="margin-top: 20px; color: #666;">
            <p><strong>This simplified version captures the essential computational logic</strong> while being readable on Medium.</p>
        </div>
    </div>

    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'linear',
                nodeSpacing: 25,
                rankSpacing: 30
            }},
            themeVariables: {{
                fontFamily: 'Arial, sans-serif',
                fontSize: '12px',
                primaryColor: '#ff6b6b',
                primaryTextColor: '#ffffff',
                primaryBorderColor: '#ff6b6b',
                lineColor: '#333333',
                secondaryColor: '#feca57',
                tertiaryColor: '#4ecdc4'
            }}
        }});
        
        function downloadSVG() {{
            const svgElement = document.querySelector('.mermaid svg');
            if (svgElement) {{
                const svgData = new XMLSerializer().serializeToString(svgElement);
                const svgBlob = new Blob([svgData], {{type: 'image/svg+xml;charset=utf-8'}});
                const svgUrl = URL.createObjectURL(svgBlob);
                const downloadLink = document.createElement('a');
                downloadLink.href = svgUrl;
                downloadLink.download = 'medium_friendly_beta_galactosidase.svg';
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);
                URL.revokeObjectURL(svgUrl);
            }} else {{
                alert('SVG not ready yet. Please wait a moment and try again.');
            }}
        }}
    </script>
</body>
</html>'''
    
    # Write HTML file
    with open('medium_friendly_beta_galactosidase.html', 'w') as f:
        f.write(html_content)
    
    print("✅ Created medium_friendly_beta_galactosidase.html")
    print("🌐 Opening in browser...")
    
    # Open in browser
    webbrowser.open('file://' + os.path.abspath('medium_friendly_beta_galactosidase.html'))
    
    return True

if __name__ == "__main__":
    print("🔄 Creating Medium-friendly β-galactosidase flowchart...")
    success = create_simplified_flowchart()
    
    if success:
        print("\n🎉 Success! The simplified flowchart is now open in your browser.")
        print("📝 This version is:")
        print("   • Optimized for Medium display")
        print("   • Captures key computational logic")
        print("   • Uses readable font sizes")
        print("   • Maintains color coding")
        print("   • Fits in a single screenshot")
        print("\n💡 Take a screenshot and upload to Medium!")
    else:
        print("❌ Failed to create the file.")

