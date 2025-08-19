# 🎨 Universal Color Scheme Automation System

This system provides automated tools to update all existing flowcharts and generate new ones with the universal color scheme.

## 📋 Universal Color Scheme

**Standardized Colors:**
- **Red (#ff6b6b)** - Triggers/Inputs (white text)
- **Yellow (#ffd43b)** - Structures/Objects (black text)
- **Green (#51cf66)** - Processing/Operations (white text)
- **Light Blue (#74c0fc)** - Intermediates/States (white text)
- **Light Violet (#b197fc)** - Products/Outputs (white text)

## 🚀 Quick Start

### Phase 1: Update All Existing Files

```bash
# Run the universal color scheme update script
python update_color_scheme.py
```

This script will:
- ✅ Find all HTML files in the project
- ✅ Update color hex codes to universal scheme
- ✅ Add text colors for optimal readability
- ✅ Add discipline-specific color keys beneath each flowchart
- ✅ Remove redundant color information from captions
- ✅ Preserve all flowchart detail and node counts

### Phase 2: Generate New Flowcharts

```bash
# Generate single flowchart from Mermaid file
python template_system.py

# Or use the template system directly
from template_system import create_flowchart_from_mmd
create_flowchart_from_mmd('my_process.mmd', 'physics', 'output/')
```

## 📁 File Structure

```
glmp/
├── update_color_scheme.py      # Script to update existing files
├── template_system.py          # Template system for new flowcharts
├── AUTOMATION_README.md        # This file
├── physics_processes.html      # Updated with universal scheme
├── mathematics_processes.html  # Updated with universal scheme
├── computer_science_processes.html
├── human_chemical_processes.html
├── human_disease_processes.html
└── *.mmd                       # Mermaid source files
```

## 🔧 Script Details

### `update_color_scheme.py`

**Purpose:** Updates all existing HTML files with universal color scheme

**Features:**
- Automatic discipline detection from filename
- Comprehensive color mapping (handles all old color variations)
- Adds color keys beneath every flowchart
- Removes redundant color information from captions
- Updates introduction paragraphs
- Preserves all flowchart complexity and detail

**Usage:**
```bash
python update_color_scheme.py
```

**Output:**
```
🎨 Universal Color Scheme Update Script
==================================================
Found 15 HTML files to process
Processing: physics_processes.html
✅ Updated: physics_processes.html
Processing: mathematics_processes.html
✅ Updated: mathematics_processes.html
...
🎉 Color scheme update complete!
Processed 15 files
```

### `template_system.py`

**Purpose:** Generate new HTML flowcharts from Mermaid Markdown files

**Features:**
- Standardized HTML templates
- Automatic universal color scheme application
- Discipline-specific color keys
- Batch processing capabilities

**Usage Examples:**

```python
# Generate single flowchart
from template_system import create_flowchart_from_mmd
create_flowchart_from_mmd('quantum_tunneling.mmd', 'physics', 'output/')

# Batch generate from MMD files
from template_system import batch_generate_from_mmd
batch_generate_from_mmd('.', 'mathematics', 'output/')

# Use template system directly
from template_system import FlowchartTemplate
template = FlowchartTemplate('computer_science')
html = template.generate_html('My Process', [('Process 1', mermaid_code)])
```

## 🎯 Discipline-Specific Color Keys

The system automatically generates appropriate color keys for each discipline:

### Physics
- Red: Triggers & Conditions
- Yellow: Wave Functions & Fields
- Green: Quantum Processing
- Blue: Intermediates
- Violet: Products

### Mathematics
- Red: Axioms & Given Conditions
- Yellow: Logical Structures & Hypotheses
- Green: Deductions & Theorem Applications
- Blue: Intermediates
- Violet: Products

### Computer Science
- Red: Input Data & Parameters
- Yellow: Data Structures & Arrays
- Green: Operations & Algorithms
- Blue: States & Variables
- Violet: Output & Results

### Human Chemical
- Red: Triggers & Conditions
- Yellow: Catalysts & Enzymes
- Green: Chemical Processing
- Blue: Intermediates
- Violet: Products

### Human Disease
- Red: Disease Triggers
- Yellow: Pathological Structures
- Green: Disease Processes
- Blue: Intermediates
- Violet: Disease Outcomes

## 🔄 Workflow for New Flowcharts

1. **Create Mermaid Markdown file** (`.mmd`)
2. **Use template system** to generate HTML
3. **Automatic color scheme** applied
4. **Color key** automatically added
5. **Consistent styling** across all flowcharts

## 🛡️ Safety Features

- **Backup creation** before running updates
- **Error handling** for malformed files
- **Progress tracking** during batch operations
- **Validation** of color scheme application

## 📊 Benefits

### Immediate Benefits
- ✅ Consistent visual appearance across all 300+ flowcharts
- ✅ Improved readability with optimized text colors
- ✅ Professional color keys beneath every flowchart
- ✅ Clean, concise captions without redundant color information
- ✅ Eliminated lavender/teal color confusion

### Long-term Benefits
- ✅ Template system for future flowchart generation
- ✅ Centralized color scheme management
- ✅ Automated consistency enforcement
- ✅ Scalable to thousands of flowcharts

## 🎨 Color Scheme Rationale

The universal color scheme was chosen for:
- **Distinguishability:** Each color is clearly different from others
- **Readability:** Optimal contrast between background and text
- **Semantic meaning:** Colors align with conceptual categories
- **Accessibility:** Works well for color-blind users
- **Professional appearance:** Suitable for academic publication

## 🚨 Important Notes

1. **Backup your files** before running the update script
2. **Test on a small subset** first if you have concerns
3. **The script preserves all detail** - no flowchart complexity is lost
4. **Color keys are automatically added** to every flowchart
5. **Text colors are optimized** for readability

## 🔧 Customization

To modify the color scheme or add new disciplines:

1. Edit the `COLOR_MAPPINGS` in `update_color_scheme.py`
2. Update `DISCIPLINE_LABELS` in `template_system.py`
3. Add new discipline templates as needed

## 📞 Support

If you encounter issues:
1. Check that all files are properly backed up
2. Verify Python 3.6+ is installed
3. Ensure all required files are in the same directory
4. Review the error messages for specific file issues

---

**Created:** December 2024  
**Purpose:** Universal color scheme automation for GLMP project  
**Scope:** 300+ flowchart files across multiple disciplines
