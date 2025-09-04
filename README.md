# GLMP Biological Processes Dataset

## Overview
This dataset contains 732 biological processes with computational pattern analysis for the GLMP (Gene Logic Modeling Project).

**⚠️ Important**: This dataset uses the pattern audit table as the baseline to avoid double-counting processes that appear in both batch files and articles.

## Dataset Information
- **Version**: 2
- **Last Updated**: 2025-09-04 15:07:07
- **Total Processes**: 732
- **License**: CC BY 4.0
- **Paper**: Process Visualization in Biology: A Programming Framework for Systematic Analysis of Complex Systems

## Files

### Core Data Files
- `process_inventory.csv` - Clean inventory of 732 biological processes (no duplicates)
- `pattern_audit_table.html` - Interactive audit table for manual pattern verification
- `simple_process_list.html` - Simplified process list organized by kingdom
- `process_summary.txt` - Text summary of all processes

### Metadata
- `dataset_info.json` - Structured metadata about the dataset
- `README.md` - This file

## Computational Patterns Analyzed
- **OR Gates**: Alternative pathway activation mechanisms
- **AND Gates**: Multiple signal requirement systems  
- **NOT Gates**: Inhibitory regulatory mechanisms
- **Feedback Loops**: Positive and negative feedback systems
- **State Machines**: Developmental and cell cycle processes
- **Decision Trees**: Immune response and adaptation systems

## Data Quality
- **Baseline**: Pattern audit table (avoids double-counting)
- **Scope**: Only processes in batch files (not articles/index pages)
- **Deduplication**: Removes duplicates from Hugging Face articles
- **Anchors**: Direct links to specific processes within HTML files

## Usage
This dataset is designed for:
- Computational biology research
- Pattern analysis in biological systems
- Educational purposes
- Reproducible research verification

## Citation
If you use this dataset, please cite:
```
Welz, G. (2025). Process Visualization in Biology: A Programming Framework for Systematic Analysis of Complex Systems. [Journal TBD]
```

## Contact
For questions about this dataset, contact: gwelz@jjay.cuny.edu
