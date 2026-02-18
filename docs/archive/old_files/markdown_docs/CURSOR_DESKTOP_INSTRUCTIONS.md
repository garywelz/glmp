# Instructions for Desktop Cursor Agent

## 🎯 Your Role: Local Development & Analysis Assistant

**Project:** GLMP - Genome Logic Mapping Project  
**Principal Investigator:** Gary Welz  
**Your Mission:** Clean up project, analyze data, support research

---

## 📁 Your Working Directory

```bash
cd ~/glmp-clean
```

**Current Structure:**
```
~/glmp-clean/
├── glmp-v2/              # Main GLMP project (deployed to GCS)
│   ├── viewer/           # Interactive web viewer
│   ├── processes/        # 14 biological process JSON files
│   └── data/             # Metadata
├── glmp-cloud-service/   # Cloud Run service (deployed)
└── [old files to clean]  # Your cleanup target
```

---

## 🧹 TASK 1: Project Cleanup

### **Clean Main Directory**

```bash
cd ~/glmp-clean

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete
find . -name ".DS_Store" -delete

# Remove old batch files (superseded by individual process files)
mkdir -p archive/old-batch-files
mv ecoli_batch*.html archive/old-batch-files/ 2>/dev/null
mv yeast_batch*.html archive/old-batch-files/ 2>/dev/null
mv *_batch*.html archive/old-batch-files/ 2>/dev/null

# Remove old Python scripts (superseded by Cloud Run service)
mkdir -p archive/old-scripts
mv add_*.py archive/old-scripts/ 2>/dev/null
mv create_*.py archive/old-scripts/ 2>/dev/null
mv fix_*.py archive/old-scripts/ 2>/dev/null
mv *_analysis.py archive/old-scripts/ 2>/dev/null

# Remove temporary/test files
rm -f test_*.html test_*.py 2>/dev/null

# Organize documentation
mkdir -p docs/architecture docs/deployment docs/analysis
mv DEPLOY_*.md docs/deployment/ 2>/dev/null
mv *_ANALYSIS.md docs/analysis/ 2>/dev/null
mv *_ARCHITECTURE.md docs/architecture/ 2>/dev/null

echo "✓ Cleanup complete!"
```

### **Create Clean Project Structure**

```bash
# After cleanup, your structure should be:
~/glmp-clean/
├── glmp-v2/              # Active GLMP project
├── glmp-cloud-service/   # Active cloud service
├── docs/                 # All documentation
├── archive/              # Old files (not deleted, just archived)
└── README.md             # Project overview
```

---

## 📊 TASK 2: Analyze All 14 Processes

### **Create Analysis Script**

Create: `~/glmp-clean/analyze_current_processes.py`

```python
"""
Analyze all 14 current processes and generate statistics
"""

import json
import os
from pathlib import Path

def load_processes():
    """Load all process JSON files"""
    processes = []
    process_dir = Path('glmp-v2/processes')
    
    for json_file in process_dir.rglob('*.json'):
        with open(json_file, 'r') as f:
            process = json.load(f)
            processes.append(process)
    
    return processes

def analyze_gates(processes):
    """Extract gate counts from all processes"""
    results = []
    
    for proc in processes:
        complexity = proc.get('complexity', {})
        gates = complexity.get('logicGates', {})
        
        results.append({
            'id': proc.get('id'),
            'name': proc.get('name'),
            'organism': proc.get('organism'),
            'nodes': complexity.get('nodes', 0),
            'or_gates': gates.get('orGates', 0),
            'and_gates': gates.get('andGates', 0),
            'total_gates': gates.get('total', 0),
            'citations': len(proc.get('sources', []))
        })
    
    return results

def generate_statistics(results):
    """Generate summary statistics"""
    total = len(results)
    
    stats = {
        'total_processes': total,
        'total_nodes': sum(r['nodes'] for r in results),
        'total_or_gates': sum(r['or_gates'] for r in results),
        'total_and_gates': sum(r['and_gates'] for r in results),
        'total_gates': sum(r['total_gates'] for r in results),
        'total_citations': sum(r['citations'] for r in results),
        
        'avg_nodes': round(sum(r['nodes'] for r in results) / total, 1),
        'avg_gates': round(sum(r['total_gates'] for r in results) / total, 1),
        'avg_citations': round(sum(r['citations'] for r in results) / total, 1),
        
        'organisms': list(set(r['organism'] for r in results))
    }
    
    return stats

def export_to_csv(results, stats):
    """Export to CSV for analysis"""
    import csv
    
    # Export individual processes
    with open('process_analysis.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    # Export statistics
    with open('process_statistics.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    print("✓ Exported to process_analysis.csv")
    print("✓ Exported to process_statistics.json")

if __name__ == '__main__':
    processes = load_processes()
    print(f"Loaded {len(processes)} processes")
    
    results = analyze_gates(processes)
    stats = generate_statistics(results)
    
    print("\n=== STATISTICS ===")
    print(json.dumps(stats, indent=2))
    
    export_to_csv(results, stats)
```

**Run it:**
```bash
cd ~/glmp-clean
python3 analyze_current_processes.py
```

**Expected Output:**
- `process_analysis.csv` - Individual process data
- `process_statistics.json` - Summary statistics

---

## 📈 TASK 3: Create Visualizations

### **Create Visualization Script**

Create: `~/glmp-clean/visualize_processes.py`

```python
"""
Create visualizations of process data
Requires: matplotlib, seaborn
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns

# Load analysis results
with open('process_analysis.csv', 'r') as f:
    import csv
    reader = csv.DictReader(f)
    data = list(reader)

# Convert to numeric
for row in data:
    row['nodes'] = int(row['nodes'])
    row['or_gates'] = int(row['or_gates'])
    row['and_gates'] = int(row['and_gates'])
    row['total_gates'] = int(row['total_gates'])

# Plot 1: Gate distribution
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# OR vs AND gates
or_counts = [r['or_gates'] for r in data]
and_counts = [r['and_gates'] for r in data]
names = [r['name'][:20] for r in data]

axes[0, 0].bar(range(len(data)), or_counts, label='OR Gates', alpha=0.7)
axes[0, 0].bar(range(len(data)), and_counts, bottom=or_counts, label='AND Gates', alpha=0.7)
axes[0, 0].set_title('Logic Gate Distribution')
axes[0, 0].set_xlabel('Process')
axes[0, 0].set_ylabel('Gate Count')
axes[0, 0].legend()

# Complexity (nodes vs gates)
nodes = [r['nodes'] for r in data]
gates = [r['total_gates'] for r in data]

axes[0, 1].scatter(nodes, gates, s=100, alpha=0.6)
axes[0, 1].set_title('Complexity: Nodes vs Gates')
axes[0, 1].set_xlabel('Node Count')
axes[0, 1].set_ylabel('Total Gates')

# Organism distribution
from collections import Counter
org_counts = Counter(r['organism'] for r in data)
axes[1, 0].pie(org_counts.values(), labels=org_counts.keys(), autopct='%1.1f%%')
axes[1, 0].set_title('Processes by Organism')

# Gate ratio (OR/AND)
ratios = [r['or_gates'] / max(r['and_gates'], 1) for r in data]
axes[1, 1].hist(ratios, bins=10, edgecolor='black', alpha=0.7)
axes[1, 1].set_title('OR/AND Gate Ratio Distribution')
axes[1, 1].set_xlabel('OR/AND Ratio')
axes[1, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.savefig('process_analysis_visualizations.png', dpi=300)
print("✓ Saved visualizations to process_analysis_visualizations.png")
```

---

## 🔬 TASK 4: Prepare HuggingFace Dataset

### **Create Export Script**

Create: `~/glmp-clean/export_for_huggingface.py`

```python
"""
Export GLMP dataset for HuggingFace
"""

import json
import shutil
from pathlib import Path

def create_hf_dataset():
    """Package dataset for HuggingFace"""
    
    # Create export directory
    export_dir = Path('glmp-dataset-export')
    export_dir.mkdir(exist_ok=True)
    
    # Copy process files
    (export_dir / 'processes').mkdir(exist_ok=True)
    shutil.copytree('glmp-v2/processes', export_dir / 'processes', dirs_exist_ok=True)
    
    # Copy metadata
    shutil.copy('glmp-v2/data/metadata.json', export_dir / 'metadata.json')
    
    # Copy analysis results
    shutil.copy('process_analysis.csv', export_dir / 'process_analysis.csv')
    shutil.copy('process_statistics.json', export_dir / 'statistics.json')
    
    # Create README
    readme = """# GLMP Dataset - Biological Processes as Computational Programs

## Overview
Systematic analysis of biological processes represented as logic circuits.

## Contents
- `processes/` - 14 biological process JSON files
- `metadata.json` - Process catalog
- `process_analysis.csv` - Quantitative analysis
- `statistics.json` - Summary statistics

## Citation
Gary Welz (2025). "Genome Logic Mapping Project: Biological Processes as Boolean Programs"

## License
CC BY 4.0
"""
    
    with open(export_dir / 'README.md', 'w') as f:
        f.write(readme)
    
    print(f"✓ Dataset exported to {export_dir}")
    print("✓ Ready to upload to HuggingFace!")

if __name__ == '__main__':
    create_hf_dataset()
```

---

## 🧪 TASK 5: Quality Control

### **Validate All Processes**

Create: `~/glmp-clean/validate_all_processes.py`

```python
"""
Validate all processes meet GLMP standards
"""

import json
from pathlib import Path

REQUIRED_FIELDS = [
    'id', 'name', 'organism', 'category', 'description',
    'mermaid', 'sources', 'colorScheme', 'complexity',
    'scientificAccuracy'
]

REQUIRED_COLORS = ['red', 'yellow', 'green', 'blue', 'orange', 'lavender', 'violet']

def validate_process(process, filename):
    """Validate a single process"""
    errors = []
    warnings = []
    
    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in process:
            errors.append(f"Missing required field: {field}")
    
    # Check color scheme
    if 'colorScheme' in process:
        for color in REQUIRED_COLORS:
            if color not in process['colorScheme']:
                warnings.append(f"Missing color: {color}")
    
    # Check citations
    if len(process.get('sources', [])) < 3:
        warnings.append(f"Only {len(process.get('sources', []))} citations (recommend 4+)")
    
    # Check logic gates are documented
    complexity = process.get('complexity', {})
    gates = complexity.get('logicGates', {})
    if not gates:
        errors.append("No logic gates documented")
    
    return {
        'file': filename,
        'id': process.get('id'),
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }

def validate_all():
    """Validate all processes"""
    results = []
    
    for json_file in Path('glmp-v2/processes').rglob('*.json'):
        with open(json_file, 'r') as f:
            process = json.load(f)
        
        result = validate_process(process, str(json_file))
        results.append(result)
        
        print(f"\n{result['id']}:")
        if result['valid']:
            print("  ✓ Valid")
        else:
            print(f"  ✗ {len(result['errors'])} errors")
            for err in result['errors']:
                print(f"    - {err}")
        
        if result['warnings']:
            print(f"  ⚠ {len(result['warnings'])} warnings")
            for warn in result['warnings']:
                print(f"    - {warn}")
    
    # Summary
    valid_count = sum(1 for r in results if r['valid'])
    print(f"\n{'='*60}")
    print(f"VALIDATION SUMMARY: {valid_count}/{len(results)} processes valid")
    print(f"{'='*60}")
    
    return results

if __name__ == '__main__':
    results = validate_all()
```

---

## 🎨 TASK 6: Generate Process Report

Create: `~/glmp-clean/generate_report.py`

```python
"""
Generate comprehensive report for research
"""

import json
from pathlib import Path
from datetime import datetime

def generate_markdown_report():
    """Generate detailed markdown report"""
    
    # Load analysis
    with open('process_analysis.csv', 'r') as f:
        import csv
        reader = csv.DictReader(f)
        processes = list(reader)
    
    with open('process_statistics.json', 'r') as f:
        stats = json.load(f)
    
    # Generate report
    report = f"""# GLMP Process Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Summary Statistics

- **Total Processes:** {stats['total_processes']}
- **Total Nodes:** {stats['total_nodes']}
- **Total Logic Gates:** {stats['total_gates']}
  - OR Gates: {stats['total_or_gates']}
  - AND Gates: {stats['total_and_gates']}
- **Total Citations:** {stats['total_citations']}

## Averages

- **Nodes per Process:** {stats['avg_nodes']}
- **Gates per Process:** {stats['avg_gates']}
- **Citations per Process:** {stats['avg_citations']}

## Process Inventory

| ID | Name | Organism | Nodes | OR | AND | Total Gates |
|----|------|----------|-------|----|----|-------------|
"""
    
    for p in processes:
        report += f"| {p['id'][:20]} | {p['name'][:30]} | {p['organism']} | {p['nodes']} | {p['or_gates']} | {p['and_gates']} | {p['total_gates']} |\n"
    
    report += f"""

## Logic Gate Analysis

### Distribution
- **OR Gates:** {stats['total_or_gates']} ({stats['total_or_gates']/stats['total_gates']*100:.1f}%)
- **AND Gates:** {stats['total_and_gates']} ({stats['total_and_gates']/stats['total_gates']*100:.1f}%)

### Observations
1. Biological processes use both OR and AND logic
2. OR gates (binary decisions) are slightly more common
3. AND gates (multi-signal integration) indicate complex regulation

## Next Steps
1. Expand to 100 processes
2. Identify gate composition patterns
3. Compare across organisms
4. Publish findings

---

**Generated by GLMP Analysis Pipeline**
"""
    
    with open('PROCESS_REPORT.md', 'w') as f:
        f.write(report)
    
    print("✓ Report generated: PROCESS_REPORT.md")

if __name__ == '__main__':
    generate_markdown_report()
```

---

## 🔄 TASK 7: Git Management

### **Clean Git History**

```bash
cd ~/glmp-clean

# Check current status
git status

# Stage cleanup changes
git add .
git status

# Commit organization
git commit -m "chore: Organize project structure

- Archive old batch files
- Archive old Python scripts
- Organize documentation into docs/
- Remove temporary test files
- Clean Python cache files

Project now has clear structure:
- glmp-v2/ (active)
- glmp-cloud-service/ (active)
- docs/ (organized)
- archive/ (historical)
"

# Push to GitHub
git push origin main
```

---

## 📤 TASK 8: Prepare for Next 36 Processes

### **Create Process Template**

Create: `~/glmp-clean/new_process_template.json`

```json
{
  "id": "organism_process_name",
  "name": "Process Name",
  "organism": "Organism",
  "category": "Category",
  "description": "Detailed description...",
  "scientificAccuracy": "This flowchart is based on verified research...",
  "complexity": {
    "nodes": 0,
    "uniqueIdentifiers": true,
    "colorCoded": true,
    "detailLevel": "detailed",
    "logicGates": {
      "orGates": 0,
      "andGates": 0,
      "total": 0
    }
  },
  "colorScheme": {
    "red": {"hex": "#ff6b6b", "category": "Triggers & Inputs"},
    "yellow": {"hex": "#ffd43b", "category": "Structures & Objects"},
    "green": {"hex": "#51cf66", "category": "Processing & Operations"},
    "blue": {"hex": "#74c0fc", "category": "Intermediates & States"},
    "orange": {"hex": "#ff9f43", "category": "OR Logic Gates"},
    "lavender": {"hex": "#b4b4dc", "category": "AND Logic Gates"},
    "violet": {"hex": "#b197fc", "category": "Products & Outputs"}
  },
  "mermaid": "graph TD\n...",
  "sources": [],
  "keywords": [],
  "relatedProcesses": [],
  "created": "2025-10-13",
  "lastUpdated": "2025-10-13",
  "verified": true,
  "verifiedBy": "AI + Literature Review",
  "notes": ""
}
```

---

## 🤝 COLLABORATION PROTOCOL

### **With Cloud Cursor Agent (me):**

**I handle:**
- Cloud deployments
- API integrations
- Service management
- AI-powered generation

**You handle:**
- Local analysis
- Data visualization
- File organization
- Quality control

### **Communication:**

**Via Git commits:**
```bash
# You commit your analysis
git commit -m "analysis: Generated statistics for 14 processes - 234 total gates"

# I pull and see your findings
# I commit new processes
git commit -m "feat: Add 10 new E. coli metabolic processes"

# You pull and analyze
```

---

## 📋 IMMEDIATE TASKS (Today)

Run these in order:

```bash
# 1. Clean up
cd ~/glmp-clean
# [Run cleanup commands from TASK 1]

# 2. Analyze
python3 analyze_current_processes.py

# 3. Validate
python3 validate_all_processes.py

# 4. Generate report
python3 generate_report.py

# 5. Commit results
git add process_analysis.csv process_statistics.json PROCESS_REPORT.md
git commit -m "analysis: Initial analysis of 14 GLMP processes"
git push origin main
```

---

## 📊 EXPECTED RESULTS

After running all tasks, you'll have:

- ✅ Clean, organized project structure
- ✅ `process_analysis.csv` - Data for all 14 processes
- ✅ `process_statistics.json` - Summary statistics  
- ✅ `PROCESS_REPORT.md` - Readable report
- ✅ Validation results
- ✅ Ready for expansion to 50+ processes

---

## 🎯 YOUR SUCCESS CRITERIA

- ✅ No unnecessary files in main directory
- ✅ All documentation organized in `docs/`
- ✅ Complete analysis of current 14 processes
- ✅ Statistics ready for research paper
- ✅ Git history clean and organized

---

**You are Gary's local lab assistant. Work methodically, document everything, and prepare the foundation for scaling to 100+ processes.**

**Let me (Cloud Agent) know when you've completed these tasks!** 🚀
