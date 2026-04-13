#!/usr/bin/env python3
"""
GRN Signal Propagation Model — a grammar-aware perturbation predictor.

Uses the TRRUST Gene Regulatory Network to predict perturbation responses
via signed personalized PageRank. Each gene knockout is modeled as removing
a node from the GRN and propagating effects through the network.

This is explicitly grammar-aware: predictions are entirely determined by
GRN topology and edge signs (activation/repression).
"""

import numpy as np
import pandas as pd
import anndata as ad
import scanpy as sc
from scipy import sparse, stats
import time
import sys

TRRUST_PATH = "regulatory_data/trrust_rawdata.human.tsv"
DATA_PATH = "benchmark_data/ReplogleWeissman2022_K562_essential.h5ad"
CLASSES_PATH = "gene_circuit_classes.tsv"
OUTPUT_PATH = "results/grn_propagation_scores.tsv"

ALPHA = 0.7       # damping factor for PageRank propagation
MAX_ITER = 50     # convergence iterations
TOL = 1e-6        # convergence tolerance
TOP_DE = 20       # score on top-20 DE genes (matching benchmark metric)


def load_trrust(path):
    """Parse TRRUST into edge list with signed weights."""
    edges = []
    with open(path) as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 3:
                continue
            regulator, target, effect = parts[0], parts[1], parts[2]
            if effect == "Activation":
                w = +1.0
            elif effect == "Repression":
                w = -1.0
            else:
                w = +0.5  # Unknown edges get weak positive weight
            edges.append((regulator, target, w))
    return edges


def build_adjacency(edges, gene_list):
    """Build signed adjacency matrix aligned to gene_list.
    A[i,j] = weight means gene j regulates gene i (column j -> row i).
    """
    gene_to_idx = {g: i for i, g in enumerate(gene_list)}
    n = len(gene_list)
    row, col, data = [], [], []

    for regulator, target, w in edges:
        if regulator in gene_to_idx and target in gene_to_idx:
            ri = gene_to_idx[target]      # target is the row (affected)
            ci = gene_to_idx[regulator]   # regulator is the column (cause)
            row.append(ri)
            col.append(ci)
            data.append(w)

    A = sparse.csr_matrix((data, (row, col)), shape=(n, n))

    col_sums = np.abs(A).sum(axis=0).A1
    col_sums[col_sums == 0] = 1.0
    D_inv = sparse.diags(1.0 / col_sums)
    A_norm = A @ D_inv

    return A_norm


def propagate(A_norm, seed_idx, alpha=ALPHA, max_iter=MAX_ITER, tol=TOL):
    """Signed personalized PageRank from seed node.

    Propagates a knockout signal (-1 at seed) through the GRN.
    Returns predicted delta vector for all genes.
    """
    n = A_norm.shape[0]
    seed = np.zeros(n)
    seed[seed_idx] = -1.0  # knockout

    delta = seed.copy()
    for _ in range(max_iter):
        delta_new = alpha * (A_norm @ delta) + (1 - alpha) * seed
        if np.max(np.abs(delta_new - delta)) < tol:
            break
        delta = delta_new

    return delta


def main():
    t0 = time.time()

    print("Loading TRRUST GRN...")
    edges = load_trrust(TRRUST_PATH)
    regulators = set(e[0] for e in edges)
    targets = set(e[1] for e in edges)
    all_grn_genes = regulators | targets
    print(f"  {len(edges)} edges, {len(regulators)} regulators, {len(targets)} targets")
    print(f"  {len(all_grn_genes)} unique genes in GRN")

    print("Loading K562 benchmark data...")
    adata = ad.read_h5ad(DATA_PATH)
    print(f"  {adata.shape[0]} cells x {adata.shape[1]} genes")

    all_genes = list(adata.var_names)
    gene_to_idx = {g: i for i, g in enumerate(all_genes)}
    n_genes = len(all_genes)

    grn_in_data = all_grn_genes & set(all_genes)
    print(f"  GRN genes in benchmark: {len(grn_in_data)}")

    print("Building adjacency matrix...")
    A_norm = build_adjacency(edges, all_genes)
    nnz = A_norm.nnz
    print(f"  Adjacency: {n_genes}x{n_genes}, {nnz} nonzero entries")

    print("Normalizing expression data...")
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)

    gene_col = "gene"
    ctrl_mask = adata.obs[gene_col].isin(["non-targeting"])
    X_ctrl = adata[ctrl_mask].X
    if sparse.issparse(X_ctrl):
        X_ctrl = X_ctrl.toarray()
    ctrl_mean = X_ctrl.mean(axis=0).flatten()
    n_ctrl = ctrl_mask.sum()
    print(f"  Control cells: {n_ctrl}")

    perturbations = [p for p in adata.obs[gene_col].unique()
                     if p not in ["non-targeting", "PBS", "control"]]
    print(f"  Perturbations to score: {len(perturbations)}")

    print("\nRunning GRN propagation for each perturbation...")
    results = []
    scored = 0
    skipped_not_in_data = 0
    skipped_no_grn = 0
    skipped_few_cells = 0
    skipped_no_de = 0

    for i, pert in enumerate(perturbations):
        if pert not in gene_to_idx:
            skipped_not_in_data += 1
            continue

        pert_idx = gene_to_idx[pert]

        col_slice = A_norm[:, pert_idx]
        if isinstance(col_slice, sparse.spmatrix):
            n_downstream = col_slice.nnz
        else:
            n_downstream = np.count_nonzero(col_slice)

        row_slice = A_norm[pert_idx, :]
        if isinstance(row_slice, sparse.spmatrix):
            n_upstream = row_slice.nnz
        else:
            n_upstream = np.count_nonzero(row_slice)

        if n_downstream == 0 and n_upstream == 0:
            skipped_no_grn += 1
            continue

        pert_mask = (adata.obs[gene_col] == pert).values
        n_cells = pert_mask.sum()
        if n_cells < 5:
            skipped_few_cells += 1
            continue

        X_pert = adata[pert_mask].X
        if sparse.issparse(X_pert):
            X_pert = X_pert.toarray()
        obs_mean = X_pert.mean(axis=0).flatten()
        obs_delta = obs_mean - ctrl_mean

        abs_delta = np.abs(obs_delta)
        top_de_idx = np.argsort(abs_delta)[::-1][:TOP_DE]

        if np.std(obs_delta[top_de_idx]) == 0:
            skipped_no_de += 1
            continue

        pred_delta = propagate(A_norm, pert_idx)

        pred_de = pred_delta[top_de_idx]
        obs_de = obs_delta[top_de_idx]

        if np.std(pred_de) == 0:
            r, p = 0.0, 1.0
        else:
            r, p = stats.pearsonr(obs_de, pred_de)

        results.append({
            "gene": pert,
            "pearson_correlation": round(r, 6),
            "pearson_pvalue": round(p, 10),
            "n_perturbed_cells": int(n_cells),
            "n_downstream": n_downstream,
            "n_upstream": n_upstream,
            "method": "GRN_Propagation",
        })
        scored += 1

        if (i + 1) % 100 == 0:
            elapsed = time.time() - t0
            print(f"  {i+1}/{len(perturbations)} ({elapsed:.0f}s) — scored {scored}")

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_PATH, sep='\t', index=False)

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.0f}s")
    print(f"  Scored: {scored}")
    print(f"  Skipped (not in data): {skipped_not_in_data}")
    print(f"  Skipped (no GRN edges): {skipped_no_grn}")
    print(f"  Skipped (< 5 cells): {skipped_few_cells}")
    print(f"  Skipped (no DE variance): {skipped_no_de}")
    print(f"\nSaved to {OUTPUT_PATH}")

    if len(df) > 0:
        print(f"\nMean Pearson r:   {df['pearson_correlation'].mean():.4f}")
        print(f"Median Pearson r: {df['pearson_correlation'].median():.4f}")
        print(f"\nTop 10:")
        for _, row in df.nlargest(10, 'pearson_correlation').iterrows():
            print(f"  {row['gene']:15s}  r = {row['pearson_correlation']:.4f}  "
                  f"(downstream={row['n_downstream']}, upstream={row['n_upstream']})")
        print(f"\nBottom 10:")
        for _, row in df.nsmallest(10, 'pearson_correlation').iterrows():
            print(f"  {row['gene']:15s}  r = {row['pearson_correlation']:.4f}")

    classes = {}
    with open(CLASSES_PATH) as f:
        import csv
        for row_c in csv.DictReader(f, delimiter='\t'):
            classes[row_c['gene']] = row_c['circuit_class']

    if len(df) > 0:
        print("\n" + "=" * 60)
        print("CLASS-STRATIFIED RESULTS")
        print("=" * 60)
        df['class'] = df['gene'].map(classes).fillna('I')
        for cls in ['I', 'II', 'III', 'IV', 'V']:
            sub = df[df['class'] == cls]
            if len(sub) > 0:
                print(f"  Class {cls}: N={len(sub):3d}, "
                      f"mean r={sub['pearson_correlation'].mean():+.4f}, "
                      f"median r={sub['pearson_correlation'].median():+.4f}")


if __name__ == "__main__":
    main()
