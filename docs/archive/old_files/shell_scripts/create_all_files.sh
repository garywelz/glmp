#!/bin/bash
# Script to create all batch files locally

echo "🧬 Creating all biological process batch files..."

# Create E. coli batches
echo "Creating E. coli batches..."

# Create ecoli batch 02
cat > processes/ecoli/ecoli_batch02_cell_division_segregation_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ecoli Batch 02 - Cell Division & Segregation</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Ecoli Batch 02 - Cell Division & Segregation</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Ecoli Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. FtsZ Ring Assembly</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Septum Formation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Chromosome Segregation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Cell Wall Synthesis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Membrane Division</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Cytokinesis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Daughter Cell Separation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Cell Cycle Completion</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[FtsZ Ring Assembly Check]
                B --> C{FtsZ Ring Assembly Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created ecoli_batch02_cell_division_segregation_UPDATED.html"

# Create ecoli batch 03
cat > processes/ecoli/ecoli_batch03_translation_protein_synthesis_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ecoli Batch 03 - Translation & Protein Synthesis</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Ecoli Batch 03 - Translation & Protein Synthesis</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Ecoli Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Translation Initiation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Ribosome Assembly</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Elongation Complex</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Peptide Bond Formation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Translocation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Termination</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Protein Folding</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Quality Control</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Translation Initiation Check]
                B --> C{Translation Initiation Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created ecoli_batch03_translation_protein_synthesis_UPDATED.html"

# Create ecoli batch 04
cat > processes/ecoli/ecoli_batch04_protein_synthesis_quality_control_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ecoli Batch 04 - Protein Synthesis & Quality Control</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Ecoli Batch 04 - Protein Synthesis & Quality Control</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Ecoli Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Translation Fidelity</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Proofreading Mechanisms</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Chaperone Systems</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Protein Folding</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Misfolding Detection</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Degradation Pathways</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Heat Shock Response</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Quality Assurance</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Translation Fidelity Check]
                B --> C{Translation Fidelity Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created ecoli_batch04_protein_synthesis_quality_control_UPDATED.html"

# Create ecoli batch 05
cat > processes/ecoli/ecoli_batch05_cell_division_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ecoli Batch 05 - Cell Division</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Ecoli Batch 05 - Cell Division</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Ecoli Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Cell Cycle Regulation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. DNA Replication Checkpoint</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. FtsZ Dynamics</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Septum Assembly</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Chromosome Partitioning</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Cytokinesis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Division Completion</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Cell Separation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Cell Cycle Regulation Check]
                B --> C{Cell Cycle Regulation Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created ecoli_batch05_cell_division_UPDATED.html"

# Create ecoli batch 06
cat > processes/ecoli/ecoli_batch06_stress_response_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ecoli Batch 06 - Stress Response</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Ecoli Batch 06 - Stress Response</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Ecoli Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Oxidative Stress</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Heat Shock</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Osmotic Stress</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. pH Stress</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Nutrient Limitation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. DNA Damage Response</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. General Stress</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Stress Recovery</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Oxidative Stress Check]
                B --> C{Oxidative Stress Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created ecoli_batch06_stress_response_UPDATED.html"

# Create ecoli batch 07
cat > processes/ecoli/ecoli_batch07_transport_membrane_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ecoli Batch 07 - Transport & Membrane</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Ecoli Batch 07 - Transport & Membrane</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Ecoli Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. ABC Transporters</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Permease Systems</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Ion Channels</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Membrane Potential</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Proton Gradient</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Substrate Uptake</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Efflux Systems</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Membrane Integrity</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[ABC Transporters Check]
                B --> C{ABC Transporters Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created ecoli_batch07_transport_membrane_UPDATED.html"

# Create ecoli batch 08
cat > processes/ecoli/ecoli_batch08_motility_chemotaxis_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ecoli Batch 08 - Motility & Chemotaxis</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Ecoli Batch 08 - Motility & Chemotaxis</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Ecoli Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Flagellar Assembly</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Motor Function</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Chemoreceptor Arrays</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Signal Transduction</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Methylation Control</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Motor Switching</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Swimming Behavior</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Tumbling Control</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Flagellar Assembly Check]
                B --> C{Flagellar Assembly Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created ecoli_batch08_motility_chemotaxis_UPDATED.html"

# Create ecoli batch 09
cat > processes/ecoli/ecoli_batch09_antibiotic_resistance_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ecoli Batch 09 - Antibiotic Resistance</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Ecoli Batch 09 - Antibiotic Resistance</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Ecoli Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Drug Detection</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Resistance Mechanisms</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Efflux Pumps</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Target Modification</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Enzyme Inactivation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Bypass Pathways</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Resistance Regulation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Fitness Cost Management</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Drug Detection Check]
                B --> C{Drug Detection Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created ecoli_batch09_antibiotic_resistance_UPDATED.html"

# Create ecoli batch 10
cat > processes/ecoli/ecoli_batch10_iron_homeostasis_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ecoli Batch 10 - Iron Homeostasis</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Ecoli Batch 10 - Iron Homeostasis</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Ecoli Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Iron Sensing</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Siderophore Production</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Iron Uptake</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Iron Storage</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Heme Utilization</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Iron Regulation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Oxidative Protection</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Iron Export</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Iron Sensing Check]
                B --> C{Iron Sensing Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created ecoli_batch10_iron_homeostasis_UPDATED.html"

# Create ecoli batch 11
cat > processes/ecoli/ecoli_batch11_biofilm_formation_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ecoli Batch 11 - Biofilm Formation</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Ecoli Batch 11 - Biofilm Formation</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Ecoli Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Surface Attachment</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Initial Adhesion</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Microcolony Formation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. EPS Production</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Matrix Development</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Quorum Sensing</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. 3D Architecture</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Biofilm Maturation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Surface Attachment Check]
                B --> C{Surface Attachment Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created ecoli_batch11_biofilm_formation_UPDATED.html"

# Create ecoli batch 12
cat > processes/ecoli/ecoli_batch12_quorum_sensing_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ecoli Batch 12 - Quorum Sensing</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Ecoli Batch 12 - Quorum Sensing</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Ecoli Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Autoinducer Synthesis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Signal Detection</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Signal Accumulation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Threshold Response</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Gene Regulation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Population Coordination</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Density Assessment</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Group Behavior</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Autoinducer Synthesis Check]
                B --> C{Autoinducer Synthesis Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created ecoli_batch12_quorum_sensing_UPDATED.html"

# Create ecoli batch 13
cat > processes/ecoli/ecoli_batch13_metabolic_pathways_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ecoli Batch 13 - Metabolic Pathways</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Ecoli Batch 13 - Metabolic Pathways</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Ecoli Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Glycolysis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. TCA Cycle</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Electron Transport</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. ATP Synthesis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Gluconeogenesis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Pentose Phosphate</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Fatty Acid Synthesis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Metabolic Regulation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Glycolysis Check]
                B --> C{Glycolysis Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created ecoli_batch13_metabolic_pathways_UPDATED.html"

# Create ecoli batch 14
cat > processes/ecoli/ecoli_batch14_gene_regulation_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ecoli Batch 14 - Gene Regulation</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Ecoli Batch 14 - Gene Regulation</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Ecoli Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Transcriptional Control</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Lac Operon</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Trp Operon</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. CAP-cAMP System</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Sigma Factors</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Two-Component Systems</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Small RNA Regulation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Global Regulators</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Transcriptional Control Check]
                B --> C{Transcriptional Control Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created ecoli_batch14_gene_regulation_UPDATED.html"

# Create ecoli batch 15
cat > processes/ecoli/ecoli_batch15_cellular_communication_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ecoli Batch 15 - Cellular Communication</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Ecoli Batch 15 - Cellular Communication</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Ecoli Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Signal Transduction</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Two-Component Systems</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Phosphorelay</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Sensor Kinases</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Response Regulators</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Signal Integration</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Cross-Talk Prevention</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Network Dynamics</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Signal Transduction Check]
                B --> C{Signal Transduction Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created ecoli_batch15_cellular_communication_UPDATED.html"

# Create yeast batch 01
cat > processes/yeast/yeast_batch01_dna_replication_repair_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Yeast Batch 01 - DNA Replication & Repair</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Yeast Batch 01 - DNA Replication & Repair</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Yeast Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Origin Recognition</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Helicase Loading</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Replication Fork</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Leading Strand Synthesis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Lagging Strand Synthesis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Proofreading</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Repair Mechanisms</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Chromosome Integrity</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Origin Recognition Check]
                B --> C{Origin Recognition Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created yeast_batch01_dna_replication_repair_UPDATED.html"

# Create yeast batch 02
cat > processes/yeast/yeast_batch02_cell_cycle_control_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Yeast Batch 02 - Cell Cycle Control</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Yeast Batch 02 - Cell Cycle Control</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Yeast Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. G1/S Checkpoint</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. S Phase Control</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. G2/M Checkpoint</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Mitotic Entry</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Spindle Checkpoint</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Cytokinesis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Cell Division</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Cycle Coordination</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[G1/S Checkpoint Check]
                B --> C{G1/S Checkpoint Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created yeast_batch02_cell_cycle_control_UPDATED.html"

# Create yeast batch 03
cat > processes/yeast/yeast_batch03_protein_synthesis_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Yeast Batch 03 - Protein Synthesis</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Yeast Batch 03 - Protein Synthesis</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Yeast Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Translation Initiation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Ribosome Assembly</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Elongation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Termination</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Protein Folding</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Quality Control</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Protein Targeting</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Post-translational Modification</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Translation Initiation Check]
                B --> C{Translation Initiation Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created yeast_batch03_protein_synthesis_UPDATED.html"

# Create yeast batch 04
cat > processes/yeast/yeast_batch04_signal_transduction_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Yeast Batch 04 - Signal Transduction</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Yeast Batch 04 - Signal Transduction</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Yeast Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. GPCR Signaling</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. cAMP Pathway</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. MAPK Cascades</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. PKA Signaling</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Calcium Signaling</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Stress Signaling</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Nutrient Sensing</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Signal Integration</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[GPCR Signaling Check]
                B --> C{GPCR Signaling Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created yeast_batch04_signal_transduction_UPDATED.html"

# Create yeast batch 05
cat > processes/yeast/yeast_batch05_energy_metabolism_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Yeast Batch 05 - Energy Metabolism</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Yeast Batch 05 - Energy Metabolism</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Yeast Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Glycolysis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Gluconeogenesis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. TCA Cycle</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Respiratory Chain</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. ATP Synthesis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Fermentation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Metabolic Regulation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Energy Balance</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Glycolysis Check]
                B --> C{Glycolysis Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created yeast_batch05_energy_metabolism_UPDATED.html"

# Create yeast batch 06
cat > processes/yeast/yeast_batch06_lipid_membrane_biology_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Yeast Batch 06 - Lipid & Membrane Biology</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Yeast Batch 06 - Lipid & Membrane Biology</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Yeast Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Lipid Synthesis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Membrane Assembly</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Sterol Metabolism</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Phospholipid Regulation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Membrane Transport</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Organelle Membranes</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Lipid Homeostasis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Membrane Dynamics</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Lipid Synthesis Check]
                B --> C{Lipid Synthesis Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created yeast_batch06_lipid_membrane_biology_UPDATED.html"

# Create yeast batch 07
cat > processes/yeast/yeast_batch07_cell_division_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Yeast Batch 07 - Cell Division</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Yeast Batch 07 - Cell Division</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Yeast Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Bud Formation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Spindle Assembly</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Chromosome Segregation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Nuclear Division</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Cytokinesis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Cell Separation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Division Control</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Size Regulation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Bud Formation Check]
                B --> C{Bud Formation Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created yeast_batch07_cell_division_UPDATED.html"

# Create yeast batch 08
cat > processes/yeast/yeast_batch08_metabolic_regulation_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Yeast Batch 08 - Metabolic Regulation</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Yeast Batch 08 - Metabolic Regulation</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Yeast Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Glucose Repression</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Metabolic Switching</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. Enzyme Regulation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Allosteric Control</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Feedback Inhibition</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Metabolic Flux</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Pathway Coordination</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Homeostatic Control</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Glucose Repression Check]
                B --> C{Glucose Repression Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created yeast_batch08_metabolic_regulation_UPDATED.html"

# Create yeast batch 09
cat > processes/yeast/yeast_batch09_gene_expression_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Yeast Batch 09 - Gene Expression</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Yeast Batch 09 - Gene Expression</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Yeast Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Transcriptional Control</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Chromatin Remodeling</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. RNA Processing</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. mRNA Export</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Translation Control</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. RNA Decay</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Gene Silencing</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Expression Coordination</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Transcriptional Control Check]
                B --> C{Transcriptional Control Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created yeast_batch09_gene_expression_UPDATED.html"

# Create yeast batch 10
cat > processes/yeast/yeast_batch10_protein_folding_quality_control_UPDATED.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Yeast Batch 10 - Protein Folding & Quality Control</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: #333;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95);
            padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: #2c3e50; font-size: 2.5em; }
        .process-card { background: white; margin: 20px 0; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
        .slider-container { margin: 15px 0; text-align: center; }
        .mermaid-container { margin: 20px 0; padding: 20px; background: white; border-radius: 5px; min-height: 300px; }
        .sources-section { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 25px 0; 
                           border-left: 4px solid #ffc107; font-size: 0.9em; }
        .disclaimer { background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; 
                     border-left: 3px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Yeast Batch 10 - Protein Folding & Quality Control</h1>
        
        <div class="sources-section">
            <h4>📚 Scientific Sources & References</h4>
            <p><strong>Primary Sources:</strong> Molecular Biology of the Cell, Yeast Databases</p>
            <div class="disclaimer">
                <strong>⚠️ Scientific Accuracy Disclosure:</strong> Pathways are scientifically accurate based on established literature.
            </div>
        </div>

        <div class="process-card" id="process-1">
            <div class="process-title">1. Chaperone Systems</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(1, this.value)">
                <div>Level: <span id="level-1">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-1"></div>
        </div>
        <div class="process-card" id="process-2">
            <div class="process-title">2. Protein Folding</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(2, this.value)">
                <div>Level: <span id="level-2">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-2"></div>
        </div>
        <div class="process-card" id="process-3">
            <div class="process-title">3. ER Quality Control</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(3, this.value)">
                <div>Level: <span id="level-3">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-3"></div>
        </div>
        <div class="process-card" id="process-4">
            <div class="process-title">4. Unfolded Protein Response</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(4, this.value)">
                <div>Level: <span id="level-4">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-4"></div>
        </div>
        <div class="process-card" id="process-5">
            <div class="process-title">5. Proteasome Degradation</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(5, this.value)">
                <div>Level: <span id="level-5">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-5"></div>
        </div>
        <div class="process-card" id="process-6">
            <div class="process-title">6. Autophagy</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(6, this.value)">
                <div>Level: <span id="level-6">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-6"></div>
        </div>
        <div class="process-card" id="process-7">
            <div class="process-title">7. Stress Response</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(7, this.value)">
                <div>Level: <span id="level-7">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-7"></div>
        </div>
        <div class="process-card" id="process-8">
            <div class="process-title">8. Proteostasis</div>
            <div class="slider-container">
                <label>Detail Level:</label>
                <input type="range" min="1" max="5" value="1" onchange="updateFlowchart(8, this.value)">
                <div>Level: <span id="level-8">1</span></div>
            </div>
            <div class="mermaid-container" id="mermaid-8"></div>
        </div>
    </div>
    <script>
        const allProcesses = {
            1: { levels: { 1: `graph TD
                A[Signal] --> B[Chaperone Systems Check]
                B --> C{Chaperone Systems Ready?}
                C -->|Yes| D[Activation]
                C -->|No| E[Wait]
                E --> C
                D --> F[Output]
                style A fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
                style B fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style C fill:#ffd43b,stroke:#333,stroke-width:2px,color:#000
                style D fill:#51cf66,stroke:#333,stroke-width:2px,color:#fff
                style E fill:#74c0fc,stroke:#333,stroke-width:2px,color:#fff
                style F fill:#b197fc,stroke:#333,stroke-width:2px,color:#fff` } }
        };
        
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        
        function updateFlowchart(processNum, level) {
            const container = document.getElementById(`mermaid-${processNum}`);
            const levelSpan = document.getElementById(`level-${processNum}`);
            if (levelSpan) levelSpan.textContent = level;
            if (allProcesses[processNum]?.levels[level]) {
                container.innerHTML = '';
                const mermaidDiv = document.createElement('div');
                mermaidDiv.className = 'mermaid';
                mermaidDiv.textContent = allProcesses[processNum].levels[level];
                container.appendChild(mermaidDiv);
                mermaid.init(undefined, mermaidDiv);
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => { for(let i=1; i<=8; i++) updateFlowchart(i, 1); }, 100);
        });
    </script>
</body>
</html>
EOF

echo "Created yeast_batch10_protein_folding_quality_control_UPDATED.html"

echo "✅ All batch files created!"
echo "Run: git add . && git commit -m 'Add all batch files' && git push"
