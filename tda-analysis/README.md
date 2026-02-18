# TDA Analysis of GLMP Biological Processes

Topological data analysis (TDA) on 108 genetic regulatory circuits from the [Genome Logic Modeling Project](https://github.com/garywelz/glmp). Uses persistent homology (Vietoris-Rips, Ripser) to detect structural patterns—notably, that feedback circuits (lac operon, two-component signaling, SOS response) appear in the most persistent H1 loops.

**Collaboration:** Dr. Mikael Vejdemo-Johansson, CUNY Graduate Center. Part of the CopernicusAI / NSF CISE proposal.

## Quick Start

```bash
# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run pipeline
python fetch_glmp_data.py      # Fetches metadata, produces glmp_features.csv
python compute_persistence.py  # Ripser, produces glmp_persistence_diagram.png
python generate_report.py     # HTML report

# H1 loop analysis (maps loops to specific processes)
python analyze_h1_loops.py     # Produces h1_loop_results.json
```

## Outputs

| File | Description |
|------|-------------|
| `glmp_features.csv` | 108 processes, feature matrix (nodes, conditionals, gates) |
| `glmp_persistence_diagram.png` | Persistence diagram (H0, H1, H2) |
| `glmp_tda_report.html` | Summary report |
| `H1_LOOP_ANALYSIS.pdf` | Top 5 H1 loops mapped to biological processes |
| `BIOLOGICAL_COHERENCE_CHECK.pdf` | Does topology capture known feedback circuits? |
| `ADDENDUM_FOR_VEJDEMO_JOHANSSON.pdf` | Methods, persistence values, discussion questions |
| `ONE_PAGE_SUMMARY.pdf` | One-page overview |

## Key Finding

The most persistent H1 loop (persistence = 0.330) includes ara operon, SOS response, stringent response, catabolite repression, Pho regulon, quorum sensing. Loop #3 contains **lac operon**; Loop #5 contains **two-component EnvZ-OmpR signaling**. This suggests TDA on structural features detects regulatory architecture.

## Regenerating PDFs

```bash
./make_pdfs.sh
```

Requires `pandoc` and `pdflatex`.

## Data Source

GLMP metadata: `https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/data/metadata.json`
