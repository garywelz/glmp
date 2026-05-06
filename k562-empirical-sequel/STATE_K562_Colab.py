#!/usr/bin/env python3
"""
STATE K562 Benchmark — Run in Google Colab (Pro recommended for GPU)
====================================================================

Instructions:
1. Open Google Colab (https://colab.research.google.com)
2. Create a new notebook
3. Set Runtime > Change runtime type > T4 GPU
4. Copy each section below into separate Colab cells and run them in order
5. Download the results TSV at the end

Estimated runtime: 1-3 hours on T4 GPU
"""

# ============================================================
# CELL 1: Install dependencies
# ============================================================
# !pip install uv
# !uv tool install arc-state
# !pip install arc-state scanpy anndata scipy huggingface_hub

import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q",
                       "arc-state", "scanpy", "anndata", "scipy",
                       "huggingface_hub", "torch"])
print("Dependencies installed.")

import torch
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)} "
          f"({torch.cuda.get_device_properties(0).total_mem/1e9:.1f} GB)")
else:
    print("WARNING: No GPU detected. This will be very slow.")

# ============================================================
# CELL 2: Download K562 data and ST-Parse model
# ============================================================
import os
from huggingface_hub import snapshot_download

DATA_URL = ("https://zenodo.org/records/7041849/files/"
            "ReplogleWeissman2022_K562_gwps.h5ad?download=1")
DATA_PATH = "ReplogleWeissman2022_K562_essential.h5ad"
MODEL_DIR = "ST-Parse"

# Download K562 data if not present
if not os.path.exists(DATA_PATH):
    print("Downloading K562 Perturb-seq data (1.5 GB)...")
    # Try the essential genes version first (smaller)
    import urllib.request
    try:
        essential_url = ("https://zenodo.org/records/7041849/files/"
                        "ReplogleWeissman2022_K562_essential.h5ad?download=1")
        urllib.request.urlretrieve(essential_url, DATA_PATH)
        print(f"Downloaded {DATA_PATH}")
    except Exception as e:
        print(f"Download failed: {e}")
        print("Please upload ReplogleWeissman2022_K562_essential.h5ad manually")
        print("(from your local benchmark_data/ folder)")

# Download ST-Parse model from HuggingFace
if not os.path.exists(MODEL_DIR):
    print("Downloading ST-Parse model from HuggingFace...")
    snapshot_download("arcinstitute/ST-Parse", local_dir=MODEL_DIR)
    print(f"Model downloaded to {MODEL_DIR}/")

print("Files ready:")
for f in os.listdir(MODEL_DIR):
    print(f"  {MODEL_DIR}/{f}")

# ============================================================
# CELL 3: Preprocess the K562 data for STATE
# ============================================================
import scanpy as sc
import numpy as np

print("Loading K562 data...")
adata = sc.read_h5ad(DATA_PATH)
print(f"  Shape: {adata.shape}")
print(f"  Obs columns: {list(adata.obs.columns)}")

# Identify perturbation column
pert_col = None
for col in ["gene", "perturbation", "guide_id", "condition", "target_gene"]:
    if col in adata.obs.columns:
        pert_col = col
        break
print(f"  Perturbation column: {pert_col}")

# Identify control label
ctrl_label = None
for label in ["non-targeting", "control", "ctrl", "non_targeting"]:
    if label in adata.obs[pert_col].values:
        ctrl_label = label
        break
print(f"  Control label: {ctrl_label}")

# STATE needs: normalized, log1p, HVG features in .obsm["X_hvg"]
print("Preprocessing for STATE...")
adata_proc = adata.copy()
sc.pp.normalize_total(adata_proc, target_sum=1e4)
sc.pp.log1p(adata_proc)
sc.pp.highly_variable_genes(adata_proc, n_top_genes=2000)

# Store HVG matrix in obsm
hvg_idx = np.where(adata_proc.var.highly_variable)[0]
hvg_names = adata_proc.var_names[hvg_idx]
adata_proc.obsm["X_hvg"] = adata_proc.X[:, hvg_idx].toarray() \
    if hasattr(adata_proc.X, 'toarray') else adata_proc.X[:, hvg_idx]

# Save preprocessed data
PROC_PATH = "k562_preprocessed_for_state.h5ad"
adata_proc.write(PROC_PATH)
print(f"  Preprocessed data saved: {PROC_PATH}")
print(f"  HVG shape: {adata_proc.obsm['X_hvg'].shape}")

# ============================================================
# CELL 4: Run STATE inference
# ============================================================
import subprocess, time

OUTPUT_PATH = "state_predictions.h5ad"

# Find the checkpoint file
ckpt_path = None
for root, dirs, files in os.walk(MODEL_DIR):
    for f in files:
        if f.endswith(".ckpt"):
            ckpt_path = os.path.join(root, f)
            break
    if ckpt_path:
        break

if ckpt_path is None:
    # Try .safetensors
    for root, dirs, files in os.walk(MODEL_DIR):
        for f in files:
            if f.endswith(".safetensors") or f.endswith(".pt") or f.endswith(".bin"):
                ckpt_path = os.path.join(root, f)
                break
        if ckpt_path:
            break

print(f"Using checkpoint: {ckpt_path}")
print(f"Running STATE inference (this may take 1-3 hours)...")

t0 = time.time()
cmd = [
    "state", "tx", "infer",
    "--model-dir", MODEL_DIR,
    "--adata", PROC_PATH,
    "--pert-col", pert_col,
    "--embed-key", "X_hvg",
    "--output", OUTPUT_PATH,
]
if ckpt_path:
    cmd.extend(["--checkpoint", ckpt_path])

print(f"Command: {' '.join(cmd)}")
result = subprocess.run(cmd, capture_output=True, text=True)
elapsed_min = (time.time() - t0) / 60

print(f"\nCompleted in {elapsed_min:.1f} minutes")
if result.returncode != 0:
    print(f"STDERR:\n{result.stderr[-2000:]}")
    print("\nIf this failed, try the alternative approach in Cell 4b below.")
else:
    print("Inference succeeded!")
    print(result.stdout[-500:])

# ============================================================
# CELL 4b (ALTERNATIVE): If CLI fails, use Python API directly
# ============================================================
# Uncomment and run this cell ONLY if Cell 4 failed

# try:
#     from state.tx.infer import run_inference
#     print("Attempting Python API inference...")
#     run_inference(
#         model_dir=MODEL_DIR,
#         adata_path=PROC_PATH,
#         pert_col=pert_col,
#         embed_key="X_hvg",
#         output_path=OUTPUT_PATH,
#     )
#     print("Done!")
# except Exception as e:
#     print(f"Python API also failed: {e}")
#     print("Please check the STATE documentation for updated API.")

# ============================================================
# CELL 5: Score predictions — compute per-gene Pearson correlation
# ============================================================
import scanpy as sc
import numpy as np
from scipy import stats
import csv

print("Scoring STATE predictions...")

# Load predictions and observed data
adata_pred = sc.read_h5ad(OUTPUT_PATH)
adata_obs = sc.read_h5ad(DATA_PATH)

# Normalize observed data the same way
sc.pp.normalize_total(adata_obs, target_sum=1e4)
sc.pp.log1p(adata_obs)

print(f"Predictions: {adata_pred.shape}")
print(f"Observed: {adata_obs.shape}")
print(f"Pred obs columns: {list(adata_pred.obs.columns)}")

# Identify shared genes (STATE may predict on HVG subset)
pred_genes = set(adata_pred.var_names)
obs_genes = set(adata_obs.var_names)
shared_genes = sorted(pred_genes & obs_genes)
print(f"Shared genes for scoring: {len(shared_genes)}")

if len(shared_genes) == 0:
    # STATE might store predictions differently
    print("No shared genes found. Checking alternative output formats...")
    print(f"Pred var_names sample: {list(adata_pred.var_names[:5])}")
    print(f"Obs var_names sample: {list(adata_obs.var_names[:5])}")
    print(f"Pred layers: {list(adata_pred.layers.keys())}")
    print(f"Pred obsm: {list(adata_pred.obsm.keys())}")

# Subset to shared genes
adata_pred_s = adata_pred[:, shared_genes] if shared_genes else adata_pred
adata_obs_s = adata_obs[:, shared_genes] if shared_genes else adata_obs

# Compute control mean from observed data
ctrl_mask = adata_obs_s.obs[pert_col] == ctrl_label
ctrl_expr = adata_obs_s[ctrl_mask].X
if hasattr(ctrl_expr, 'toarray'):
    ctrl_expr = ctrl_expr.toarray()
ctrl_mean = ctrl_expr.mean(axis=0)

# Get unique perturbation targets
all_perts = [p for p in adata_obs_s.obs[pert_col].unique()
             if p != ctrl_label and p != "nan"]
print(f"Perturbation targets: {len(all_perts)}")

# Score each perturbation
scores = []
for gene in all_perts:
    try:
        # Observed: mean expression of perturbed cells
        obs_mask = adata_obs_s.obs[pert_col] == gene
        n_obs = obs_mask.sum()
        if n_obs < 5:
            continue
        obs_expr = adata_obs_s[obs_mask].X
        if hasattr(obs_expr, 'toarray'):
            obs_expr = obs_expr.toarray()
        obs_mean = obs_expr.mean(axis=0)
        obs_delta = np.array(obs_mean - ctrl_mean).flatten()

        # Predicted: mean expression from STATE output for this perturbation
        # STATE output format may vary — try multiple approaches
        pred_mask = adata_pred_s.obs[pert_col] == gene if pert_col in adata_pred_s.obs else None
        if pred_mask is not None and pred_mask.sum() > 0:
            pred_expr = adata_pred_s[pred_mask].X
            if hasattr(pred_expr, 'toarray'):
                pred_expr = pred_expr.toarray()
            pred_mean = pred_expr.mean(axis=0)
            pred_delta = np.array(pred_mean - ctrl_mean).flatten()
        else:
            continue

        # Pearson correlation
        if np.std(obs_delta) > 1e-10 and np.std(pred_delta) > 1e-10:
            r, p = stats.pearsonr(obs_delta, pred_delta)
        else:
            r, p = 0.0, 1.0

        scores.append({
            "gene": gene,
            "pearson_correlation": round(r, 6),
            "pearson_pvalue": round(p, 10),
            "n_perturbed_cells": int(n_obs),
            "method": "STATE_ST-Parse",
        })

    except Exception as e:
        pass  # Skip genes that fail

print(f"\nScored: {len(scores)} genes")
if scores:
    accs = [s['pearson_correlation'] for s in scores]
    print(f"Mean Pearson r: {np.mean(accs):.4f}")
    print(f"Median: {np.median(accs):.4f}")

# ============================================================
# CELL 6: Save results and download
# ============================================================
OUTPUT_TSV = "state_k562_per_gene_scores.tsv"

with open(OUTPUT_TSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "gene", "pearson_correlation", "pearson_pvalue",
        "n_perturbed_cells", "method"
    ], delimiter="\t")
    writer.writeheader()
    writer.writerows(scores)

print(f"Saved {OUTPUT_TSV} ({len(scores)} genes)")

# Load gene classifications (upload gene_circuit_classes.tsv to Colab first)
try:
    classes = {}
    with open("gene_circuit_classes.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            classes[row["gene"]] = row["circuit_class"]

    # Quick per-class breakdown
    from collections import defaultdict
    by_class = defaultdict(list)
    for s in scores:
        cls = classes.get(s["gene"], "unclassified")
        by_class[cls].append(s["pearson_correlation"])

    print("\nPer-class accuracy:")
    for cls in ["I", "II", "III", "IV", "V", "unclassified"]:
        vals = by_class.get(cls, [])
        if vals:
            print(f"  Class {cls}: N={len(vals)}, mean r={np.mean(vals):.4f}")
except FileNotFoundError:
    print("\nUpload gene_circuit_classes.tsv for per-class breakdown,")
    print("or download the TSV and analyze locally.")

# Download from Colab
try:
    from google.colab import files
    files.download(OUTPUT_TSV)
    print(f"\nDownloading {OUTPUT_TSV}...")
except ImportError:
    print(f"\nResults saved to {OUTPUT_TSV}")
    print("Download this file and place it in progframe/results/")
