# GLMP v2 - Genome Logic Modeling Project (Clean Slate)

## Overview

A clean, modular system for visualizing biological processes with proper scientific citations.

**Version 2.0** - Complete rebuild with:
- ✅ Individual process files (one per biological process)
- ✅ Standalone viewer (loads any process dynamically)
- ✅ Proper citations (PubMed, DOI, sources)
- ✅ Scientific rigor and verification
- ✅ Clean, maintainable architecture

## Architecture

```
glmp-v2/
├── viewer/                 # Standalone HTML/JS viewer
│   ├── index.html         # Main viewer interface
│   ├── viewer.js          # Process loader and renderer
│   └── styles.css         # Responsive styling
├── processes/             # Individual process files (JSON)
│   ├── ecoli/            # E. coli processes
│   └── yeast/            # Yeast processes
├── data/                  # Metadata and citations
│   ├── metadata.json     # Process catalog
│   └── sources.json      # Citation database
└── docs/                  # Documentation
    └── process_template.md

```

## Process File Format

Each process is a JSON file with complete metadata:

```json
{
  "id": "ecoli_lac_operon",
  "name": "Lac Operon Regulation",
  "organism": "E. coli",
  "category": "Gene Regulation",
  "description": "...",
  "mermaid": "graph TD...",
  "sources": [
    {
      "title": "...",
      "authors": "Jacob F, Monod J",
      "journal": "...",
      "year": 1961,
      "pmid": "13718526",
      "doi": "10.1016/..."
    }
  ],
  "created": "2025-10-08",
  "verified": true
}
```

## Usage

### Local Development

```bash
cd glmp-v2
python3 -m http.server 8000
# Open: http://localhost:8000/viewer/
```

### View a Process

```
http://localhost:8000/viewer/?process=ecoli_lac_operon
```

### Deploy to GCS

```bash
gsutil -m cp -r viewer gs://your-bucket/glmp/viewer/
gsutil -m cp -r processes gs://your-bucket/glmp/processes/
gsutil -m acl ch -r -u AllUsers:R gs://your-bucket/glmp/
```

## Technology Stack

- **Frontend:** HTML5, Vanilla JavaScript, CSS3
- **Diagrams:** Mermaid.js (via CDN)
- **Data:** JSON files
- **Hosting:** Google Cloud Storage (static)
- **No backend required** - pure static site

## Quality Standards

Every process must have:
- ✅ Verified accuracy
- ✅ Proper citations (minimum 2 sources)
- ✅ PubMed ID or DOI
- ✅ Clear description
- ✅ Working Mermaid diagram
- ✅ Multiple detail levels (when applicable)

## Deployment

Production URL (after deployment):
```
https://storage.googleapis.com/your-bucket/glmp/viewer/
```

## Archive

Previous versions archived at:
- Branch: `archive-2025-10-06-old-batch-files`
- HuggingFace: Backup available

## License

[Your License Here]

## Contact

[Your Contact Info]

---

**Built with scientific rigor and proper citations for academic sharing and publication.**
