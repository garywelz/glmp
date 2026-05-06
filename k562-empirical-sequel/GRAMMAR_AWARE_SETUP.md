# Grammar-Aware Model Setup: CellOracle + STATE

## Overview

Two models to run on the same K562 Perturb-seq benchmark:
- **CellOracle** (grammar-aware): builds GRN, simulates perturbations through network topology
- **STATE/ST-Parse** (grammar-blind but state-of-the-art): transformer on perturbation data

## Step 0: Download K562 Benchmark Data

The CZI Virtual Cells Platform provides the processed K562 Replogle dataset:
- URL: https://virtualcellmodels.cziscience.com/dataset/k562-essential-perturb-seq
- Format: .h5ad (AnnData)
- Also available via scPerturb: https://zenodo.org/records/10044268

```bash
# Create data directory
mkdir -p ~/progframe/benchmark_data

# Option A: Download from scPerturb (Zenodo)
# Navigate to https://zenodo.org/records/10044268 and download
# ReplogleWeissman2022_K562_gwps.h5ad

# Option B: Use cell-load (Arc Institute's data loader)
pip install cell-load
python3 -c "
from cell_load import load
adata = load('k562-essential-perturb-seq')
adata.write('benchmark_data/k562_perturb_seq.h5ad')
"
```

## Step 1: CellOracle (grammar-aware) — runs on laptop

### Install

```bash
conda create -n celloracle_env python=3.10
conda activate celloracle_env
pip install celloracle scanpy
```

### Run

See `run_celloracle_k562.py` in this directory.
Expected runtime: 8–24 hours on laptop (CPU, 16+ GB RAM).

### What it does

1. Loads K562 control cells
2. Builds GRN using built-in human promoter base GRN (no scATAC-seq needed)
3. For each of 780 perturbed genes, simulates knockdown through the GRN
4. Computes predicted expression change vectors
5. Scores predictions against observed changes (Pearson, DEG recovery)

### Output

`results/celloracle_k562_per_gene_scores.tsv` — per-gene Pearson correlation,
same format as scPerturBench results, ready for stratified analysis.

## Step 2: STATE/ST-Parse (grammar-blind SOTA) — needs GPU

### Install

```bash
pip install arc-state cell-eval
```

### Run (on Colab or cloud GPU)

See `run_state_k562.py` in this directory.
Expected runtime: 4–8 hours on A100.

### What it does

1. Loads K562 benchmark data
2. Runs ST-Parse inference on all perturbations
3. Computes per-gene accuracy scores using cell-eval metrics

### Output

`results/state_k562_per_gene_scores.tsv`

## Step 3: Stratified Analysis

Once both models produce per-gene scores, run:

```bash
python3 stratified_analysis_grammar_aware.py
```

This merges CellOracle and STATE scores with gene_circuit_classes.tsv
and tests whether:
- CellOracle outperforms STATE specifically on Class III (bistable) genes
- The accuracy gradient appears for CellOracle but not STATE
- CellOracle's inferred GRN topology agrees with GLMP classification
