"""
Compute top-20 differentially expressed genes per perturbation from K562 data.
These are used to re-score STATE on the same metric as the 14 benchmark methods.

Output: results/top20_de_genes_per_perturbation.tsv
"""

import numpy as np
import pandas as pd
import anndata as ad
from scipy import sparse
import time
import json

DATA_PATH = "benchmark_data/ReplogleWeissman2022_K562_essential.h5ad"
OUTPUT_TSV = "results/top20_de_genes_per_perturbation.tsv"
OUTPUT_JSON = "results/top20_de_genes_per_perturbation.json"

t0 = time.time()
print("Loading K562 data...")
adata = ad.read_h5ad(DATA_PATH)
print(f"  {adata.shape[0]} cells × {adata.shape[1]} genes ({time.time()-t0:.0f}s)")

gene_col = "gene"
gene_names = list(adata.var_names)

# Identify control cells
ctrl_labels = ["non-targeting"]
ctrl_mask = adata.obs[gene_col].isin(ctrl_labels).values
print(f"  Control cells: {ctrl_mask.sum()}")

# Extract and normalize control expression
print("Computing control mean expression...")
X_ctrl = adata[ctrl_mask].X
if sparse.issparse(X_ctrl):
    X_ctrl = X_ctrl.toarray()
X_ctrl = X_ctrl.astype(np.float64)
lib_ctrl = X_ctrl.sum(axis=1, keepdims=True)
lib_ctrl[lib_ctrl == 0] = 1
median_lib = np.median(lib_ctrl)
X_ctrl_norm = np.log1p(X_ctrl / lib_ctrl * median_lib)
ctrl_mean = X_ctrl_norm.mean(axis=0)
print(f"  Control mean computed ({time.time()-t0:.0f}s)")

# Get all perturbations
perturbations = [p for p in adata.obs[gene_col].unique() if p not in ctrl_labels]
print(f"\nComputing top-20 DE genes for {len(perturbations)} perturbations...")

results = []
de_dict = {}

for i, pert in enumerate(perturbations):
    mask = (adata.obs[gene_col] == pert).values
    n_cells = mask.sum()
    if n_cells < 5:
        continue

    X_pert = adata[mask].X
    if sparse.issparse(X_pert):
        X_pert = X_pert.toarray()
    X_pert = X_pert.astype(np.float64)
    lib_pert = X_pert.sum(axis=1, keepdims=True)
    lib_pert[lib_pert == 0] = 1
    X_pert_norm = np.log1p(X_pert / lib_pert * median_lib)
    pert_mean = X_pert_norm.mean(axis=0)

    delta = pert_mean - ctrl_mean
    abs_delta = np.abs(delta)
    top20_idx = np.argsort(abs_delta)[-20:][::-1]
    top20_genes = [gene_names[j] for j in top20_idx]

    de_dict[pert] = top20_genes

    for rank, j in enumerate(top20_idx):
        results.append({
            "perturbation": pert,
            "rank": rank + 1,
            "de_gene": gene_names[j],
            "delta": delta[j],
            "abs_delta": abs_delta[j],
        })

    if (i + 1) % 100 == 0:
        print(f"  ... {i+1}/{len(perturbations)} ({time.time()-t0:.0f}s)")

print(f"  Done ({time.time()-t0:.0f}s)")

df = pd.DataFrame(results)
df.to_csv(OUTPUT_TSV, sep="\t", index=False)
print(f"\nSaved {len(df)} rows to {OUTPUT_TSV}")

with open(OUTPUT_JSON, "w") as f:
    json.dump(de_dict, f)
print(f"Saved {len(de_dict)} perturbation DE gene lists to {OUTPUT_JSON}")
print(f"\nTotal: {time.time()-t0:.0f}s")
