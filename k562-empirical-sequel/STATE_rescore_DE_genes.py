"""
STATE Re-scoring on Top-20 DE Genes
====================================
Paste this entire cell into your Colab notebook and run it.

It will:
1. Check if state_predictions.h5ad exists (from previous run)
2. If not, re-download data + model and re-run inference
3. Compute top-20 DE genes per perturbation (matching benchmark metric)
4. Re-score STATE predictions on those DE genes
5. Save and download the results
"""

import os, gc, time
import numpy as np
import scanpy as sc
from scipy import stats, sparse
from google.colab import files

t0 = time.time()

# ============================================================
# STEP 1: Check what files we have
# ============================================================
DATA_PATH = "ReplogleWeissman2022_K562_essential.h5ad"
PRED_PATH = "state_predictions.h5ad"
PROC_PATH = "k562_for_state.h5ad"
MODEL_DIR = "ST-HVG-Parse/zeroshot/split_0"

have_data = os.path.exists(DATA_PATH)
have_pred = os.path.exists(PRED_PATH)
have_proc = os.path.exists(PROC_PATH)

print(f"Data file ({DATA_PATH}): {'FOUND' if have_data else 'MISSING'}")
print(f"Predictions ({PRED_PATH}): {'FOUND' if have_pred else 'MISSING'}")
print(f"Processed data ({PROC_PATH}): {'FOUND' if have_proc else 'MISSING'}")

# ============================================================
# STEP 2: Download data if missing
# ============================================================
if not have_data:
    import urllib.request
    print("\nDownloading K562 data (1.5 GB)...")
    url = "https://zenodo.org/records/7041849/files/ReplogleWeissman2022_K562_essential.h5ad?download=1"
    urllib.request.urlretrieve(url, DATA_PATH)
    print(f"Downloaded: {os.path.getsize(DATA_PATH)/1e9:.1f} GB")

# ============================================================
# STEP 3: Download model and run inference if predictions missing
# ============================================================
if not have_pred:
    print("\n--- Need to re-run STATE inference ---")

    # Download model
    if not os.path.exists(os.path.join(MODEL_DIR, "config.yaml")):
        from huggingface_hub import snapshot_download
        print("Downloading model (zeroshot/split_0 only, ~600 MB)...")
        snapshot_download(
            "arcinstitute/ST-HVG-Parse",
            local_dir="ST-HVG-Parse",
            allow_patterns=[
                "zeroshot/split_0/config.yaml",
                "zeroshot/split_0/checkpoints/best.ckpt",
                "zeroshot/split_0/*.pkl",
                "zeroshot/split_0/*.pt",
                "zeroshot/split_0/*.torch",
                "zeroshot/split_0/*.txt",
            ],
        )
        print("Model downloaded.")

    # Preprocess data
    if not have_proc:
        print("\nPreprocessing data...")
        adata = sc.read_h5ad(DATA_PATH)
        adata.obs["gene"] = adata.obs["gene"].replace({"non-targeting": "PBS"})
        sc.pp.normalize_total(adata, target_sum=1e4)
        sc.pp.log1p(adata)
        sc.pp.highly_variable_genes(adata, n_top_genes=2000)
        hvg_mask = adata.var["highly_variable"]
        adata.obsm["X_hvg"] = adata[:, hvg_mask].X.toarray() if sparse.issparse(adata[:, hvg_mask].X) else adata[:, hvg_mask].X.copy()
        adata.write_h5ad(PROC_PATH)
        print(f"Saved preprocessed data: {PROC_PATH}")
        del adata; gc.collect()

    # Run inference
    print("\nRunning STATE inference...")
    ckpt = os.path.join(MODEL_DIR, "checkpoints", "best.ckpt")
    cmd = f"python -m state tx infer --adata_path {PROC_PATH} --model_path {MODEL_DIR} --checkpoint_path {ckpt} --output_path {PRED_PATH}"
    os.system(cmd)
    assert os.path.exists(PRED_PATH), f"Inference failed — {PRED_PATH} not created"
    print("Inference complete.")

print(f"\nSetup done ({time.time()-t0:.0f}s)")

# ============================================================
# STEP 4: Load data and predictions
# ============================================================
print("\n" + "="*60)
print("LOADING DATA FOR RE-SCORING")
print("="*60)

# Load original (raw) data for DE gene computation
print("Loading original data...")
adata_obs = sc.read_h5ad(DATA_PATH)
print(f"  Original: {adata_obs.shape}")

# Normalize the original data
sc.pp.normalize_total(adata_obs, target_sum=1e4)
sc.pp.log1p(adata_obs)

# Load predictions
print("Loading predictions...")
adata_pred = sc.read_h5ad(PRED_PATH)
print(f"  Predictions: {adata_pred.shape}")

# Load processed data (has HVG info)
print("Loading processed data...")
adata_proc = sc.read_h5ad(PROC_PATH)
hvg_names = list(adata_proc.var_names[adata_proc.var["highly_variable"]]) if "highly_variable" in adata_proc.var.columns else list(adata_proc.var_names)
print(f"  HVG count: {len(hvg_names)}")

# ============================================================
# STEP 5: Compute control means and identify perturbations
# ============================================================
gene_col = "gene"
all_genes = list(adata_obs.var_names)

# Control label — may be 'non-targeting' or 'PBS' depending on preprocessing
ctrl_labels = []
for label in ["non-targeting", "PBS", "control"]:
    if label in adata_obs.obs[gene_col].values:
        ctrl_labels.append(label)
print(f"Control labels in original data: {ctrl_labels}")

ctrl_mask_obs = adata_obs.obs[gene_col].isin(ctrl_labels)
print(f"Control cells (observed): {ctrl_mask_obs.sum()}")

# Control mean in full gene space (for DE gene identification)
X_ctrl_obs = adata_obs[ctrl_mask_obs].X
if sparse.issparse(X_ctrl_obs):
    X_ctrl_obs = X_ctrl_obs.toarray()
ctrl_mean_full = X_ctrl_obs.mean(axis=0).flatten()

# Control labels in predictions
ctrl_labels_pred = []
for label in ["non-targeting", "PBS", "control"]:
    if label in adata_pred.obs[gene_col].values:
        ctrl_labels_pred.append(label)
print(f"Control labels in predictions: {ctrl_labels_pred}")

ctrl_mask_pred = adata_pred.obs[gene_col].isin(ctrl_labels_pred)

# Get HVG expression from predictions
if "X_hvg" in adata_pred.obsm:
    X_pred_hvg = np.array(adata_pred.obsm["X_hvg"])
    print(f"Predictions HVG matrix shape: {X_pred_hvg.shape}")
else:
    X_pred_full = adata_pred.X
    if sparse.issparse(X_pred_full):
        X_pred_full = X_pred_full.toarray()
    hvg_indices = [all_genes.index(g) for g in hvg_names if g in all_genes]
    X_pred_hvg = X_pred_full[:, hvg_indices]
    print(f"Extracted HVG predictions: {X_pred_hvg.shape}")

# Control mean in HVG space (from processed/observed data)
if "X_hvg" in adata_proc.obsm:
    ctrl_mask_proc = adata_proc.obs[gene_col].isin(["PBS", "non-targeting", "control"])
    X_ctrl_hvg = np.array(adata_proc[ctrl_mask_proc].obsm["X_hvg"])
else:
    X_ctrl_hvg_obs = adata_obs[ctrl_mask_obs][:, hvg_names].X
    if sparse.issparse(X_ctrl_hvg_obs):
        X_ctrl_hvg_obs = X_ctrl_hvg_obs.toarray()
    X_ctrl_hvg = X_ctrl_hvg_obs

ctrl_mean_hvg = X_ctrl_hvg.mean(axis=0).flatten()
pred_ctrl_mean_hvg = X_pred_hvg[ctrl_mask_pred.values].mean(axis=0).flatten()

# Get perturbation list
perturbations = [p for p in adata_obs.obs[gene_col].unique()
                 if p not in ctrl_labels and p not in ctrl_labels_pred]
print(f"\nPerturbations to score: {len(perturbations)}")

# ============================================================
# STEP 6: Score on top-20 DE genes
# ============================================================
print("\n" + "="*60)
print("SCORING ON TOP-20 DE GENES PER PERTURBATION")
print("="*60)

# Map HVG names to indices in the full gene list
hvg_set = set(hvg_names)
hvg_to_full_idx = {g: all_genes.index(g) for g in hvg_names if g in all_genes}
hvg_to_hvg_idx = {g: i for i, g in enumerate(hvg_names)}

results_de20 = []
results_hvg = []

for i, pert in enumerate(perturbations):
    # Observed: get perturbed cells in full gene space
    obs_mask = (adata_obs.obs[gene_col] == pert).values
    pred_mask = (adata_pred.obs[gene_col] == pert).values

    n_obs = obs_mask.sum()
    n_pred = pred_mask.sum()
    if n_obs < 5 or n_pred < 5:
        continue

    # Observed delta in full gene space
    X_obs_pert = adata_obs[obs_mask].X
    if sparse.issparse(X_obs_pert):
        X_obs_pert = X_obs_pert.toarray()
    obs_mean_full = X_obs_pert.mean(axis=0).flatten()
    obs_delta_full = obs_mean_full - ctrl_mean_full

    # Find top-20 DE genes (by absolute delta) that are also HVGs
    abs_delta_full = np.abs(obs_delta_full)
    # Sort all genes by absolute delta, pick top ones that are in HVG set
    sorted_gene_idx = np.argsort(abs_delta_full)[::-1]
    de20_hvg_indices = []
    de20_full_indices = []
    for idx in sorted_gene_idx:
        gene_name = all_genes[idx]
        if gene_name in hvg_set:
            de20_hvg_indices.append(hvg_to_hvg_idx[gene_name])
            de20_full_indices.append(idx)
        if len(de20_hvg_indices) >= 20:
            break

    if len(de20_hvg_indices) < 5:
        continue

    # Observed delta for DE20 genes (in HVG space for alignment)
    obs_delta_de20 = np.array([obs_delta_full[fi] for fi in de20_full_indices])

    # Predicted delta for DE20 genes
    pred_pert_hvg = X_pred_hvg[pred_mask].mean(axis=0).flatten()
    pred_delta_hvg = pred_pert_hvg - pred_ctrl_mean_hvg
    pred_delta_de20 = pred_delta_hvg[de20_hvg_indices]

    # Pearson on DE20
    if np.std(obs_delta_de20) > 0 and np.std(pred_delta_de20) > 0:
        r_de20, p_de20 = stats.pearsonr(obs_delta_de20, pred_delta_de20)
    else:
        r_de20, p_de20 = 0.0, 1.0

    results_de20.append({
        "gene": pert,
        "pearson_correlation": r_de20,
        "pearson_pvalue": p_de20,
        "n_perturbed_cells": int(n_obs),
        "n_de_genes_used": len(de20_hvg_indices),
        "method": "STATE_DE20",
    })

    # Also re-score on all HVGs for comparison
    obs_hvg_pert = adata_obs[obs_mask][:, hvg_names].X
    if sparse.issparse(obs_hvg_pert):
        obs_hvg_pert = obs_hvg_pert.toarray()
    obs_mean_hvg = obs_hvg_pert.mean(axis=0).flatten()
    obs_delta_hvg = obs_mean_hvg - ctrl_mean_hvg

    if np.std(obs_delta_hvg) > 0 and np.std(pred_delta_hvg) > 0:
        r_hvg, p_hvg = stats.pearsonr(obs_delta_hvg, pred_delta_hvg)
    else:
        r_hvg, p_hvg = 0.0, 1.0

    results_hvg.append({
        "gene": pert,
        "pearson_correlation": r_hvg,
        "pearson_pvalue": p_hvg,
        "n_perturbed_cells": int(n_obs),
        "method": "STATE_HVG2000",
    })

    if (i + 1) % 100 == 0:
        print(f"  ... {i+1}/{len(perturbations)} ({time.time()-t0:.0f}s)")

print(f"\nScored {len(results_de20)} perturbations on DE20")
print(f"Scored {len(results_hvg)} perturbations on HVG2000")

# ============================================================
# STEP 7: Summary and save
# ============================================================
import pandas as pd

df_de20 = pd.DataFrame(results_de20)
df_hvg = pd.DataFrame(results_hvg)

print("\n" + "="*60)
print("RESULTS COMPARISON")
print("="*60)
print(f"\nSTATE on 2000 HVGs:  mean r = {df_hvg['pearson_correlation'].mean():.4f}, "
      f"median = {df_hvg['pearson_correlation'].median():.4f}")
print(f"STATE on top-20 DE:  mean r = {df_de20['pearson_correlation'].mean():.4f}, "
      f"median = {df_de20['pearson_correlation'].median():.4f}")

# Top 10 by DE20
print("\nTop 10 genes (DE20 scoring):")
top10 = df_de20.nlargest(10, "pearson_correlation")
for _, row in top10.iterrows():
    print(f"  {row['gene']:15s}  r = {row['pearson_correlation']:.4f}")

# Save
OUT_DE20 = "state_k562_de20_scores.tsv"
OUT_HVG = "state_k562_hvg_rescored.tsv"
df_de20.to_csv(OUT_DE20, sep="\t", index=False)
df_hvg.to_csv(OUT_HVG, sep="\t", index=False)
print(f"\nSaved: {OUT_DE20} ({len(df_de20)} genes)")
print(f"Saved: {OUT_HVG} ({len(df_hvg)} genes)")

# Download
print("\nDownloading files...")
files.download(OUT_DE20)
print(f"\nTotal runtime: {time.time()-t0:.0f}s")
print("DONE. Place the downloaded TSV in progframe/results/")
