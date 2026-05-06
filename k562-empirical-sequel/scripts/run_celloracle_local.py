#!/usr/bin/env python3
"""
CellOracle K562 Perturb-seq Benchmark — Local Runner
=====================================================

Run with the celloracle conda environment:
  /home/gdubs/miniconda3/envs/celloracle/bin/python run_celloracle_local.py

This script:
1. Loads preprocessed control cells from benchmark_data/k562_control_cells.h5ad
2. Builds a GRN using CellOracle's built-in human promoter base GRN
3. Simulates knockdown for each classified gene
4. Scores predictions against observed perturbation means
5. Outputs results/celloracle_k562_per_gene_scores.tsv

Memory: ~4-6 GB (control cells only, not the full 310K-cell matrix)
Runtime: ~4-12 hours on 8-core laptop
"""

import os
import sys
import csv
import time
import logging
from pathlib import Path

import numpy as np
from scipy import stats
import scanpy as sc
import celloracle as co

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(message)s")
log = logging.getLogger(__name__)

RESULTS = Path("results")
RESULTS.mkdir(exist_ok=True)

CTRL_PATH = Path("benchmark_data/k562_control_cells.h5ad")
MEANS_PATH = Path("benchmark_data/k562_perturbation_means.npz")
CLASS_PATH = Path("gene_circuit_classes.tsv")
FULL_DATA_PATH = Path("benchmark_data/ReplogleWeissman2022_K562_essential.h5ad")


def load_control_cells():
    """Load the pre-extracted control cells."""
    if not CTRL_PATH.exists():
        log.error(f"{CTRL_PATH} not found. Run prepare_celloracle_data.py first.")
        sys.exit(1)
    log.info(f"Loading control cells from {CTRL_PATH}...")
    adata = sc.read_h5ad(str(CTRL_PATH))
    log.info(f"  Shape: {adata.shape}")
    return adata


def load_perturbation_means():
    """Load pre-computed perturbation means for scoring."""
    if not MEANS_PATH.exists():
        log.error(f"{MEANS_PATH} not found. Run prepare_celloracle_data.py first.")
        sys.exit(1)
    data = np.load(str(MEANS_PATH), allow_pickle=True)
    ctrl_mean = data["ctrl_mean"]
    gene_names = data["gene_names"]
    pert_means = data["pert_means"]
    pert_counts = data["pert_counts"]
    var_names = data["var_names"]

    means_dict = {}
    counts_dict = {}
    for i, gene in enumerate(gene_names):
        means_dict[str(gene)] = pert_means[i]
        counts_dict[str(gene)] = int(pert_counts[i])

    log.info(f"  Loaded means for {len(means_dict)} perturbation targets")
    return ctrl_mean, means_dict, counts_dict, list(var_names)


def load_classifications():
    classes = {}
    with open(CLASS_PATH) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            classes[row["gene"]] = row["circuit_class"]
    log.info(f"  {len(classes)} gene classifications loaded")
    return classes


def preprocess(adata):
    """
    Preprocess control cells for CellOracle.
    CellOracle expects RAW COUNTS (it does its own normalization internally).
    We only do HVG selection on a temporary normalized copy, then subset
    the raw counts to those HVGs.
    """
    log.info("Preprocessing control cells...")
    adata = adata.copy()

    sc.pp.filter_genes(adata, min_cells=3)

    # Identify HVGs on a normalized copy (don't modify raw counts)
    adata_norm = adata.copy()
    sc.pp.normalize_total(adata_norm, target_sum=1e4)
    sc.pp.log1p(adata_norm)
    sc.pp.highly_variable_genes(adata_norm, n_top_genes=2500)
    hvg_mask = adata_norm.var.highly_variable
    del adata_norm

    # Subset raw counts to HVGs
    adata = adata[:, hvg_mask].copy()
    log.info(f"  After HVG filter: {adata.shape} (raw counts preserved)")

    # CellOracle needs embedding coordinates for visualization
    # Do a quick PCA/UMAP on normalized data for embedding only
    adata_for_embed = adata.copy()
    sc.pp.normalize_total(adata_for_embed, target_sum=1e4)
    sc.pp.log1p(adata_for_embed)
    sc.tl.pca(adata_for_embed, n_comps=50)
    sc.pp.neighbors(adata_for_embed, n_pcs=50)
    sc.tl.umap(adata_for_embed)

    # Transfer embedding to raw-count adata
    adata.obsm["X_umap"] = adata_for_embed.obsm["X_umap"]
    del adata_for_embed

    if "cell_type" not in adata.obs.columns:
        adata.obs["cell_type"] = "K562"

    log.info(f"  Preprocessed: {adata.shape}")
    return adata


def build_grn(adata):
    """Build GRN using CellOracle's human promoter base GRN."""
    log.info("Initializing CellOracle Oracle object...")

    oracle = co.Oracle()

    # Pass the HVG-filtered adata directly (not adata.raw which has all genes)
    oracle.import_anndata_as_raw_count(
        adata=adata,
        cluster_column_name="cell_type",
        embedding_name="X_umap",
    )

    log.info("Loading human promoter base GRN...")
    base_grn = co.data.load_human_promoter_base_GRN()
    oracle.import_TF_data(TF_info_matrix=base_grn)

    log.info("Performing PCA...")
    oracle.perform_PCA()

    log.info("Performing KNN imputation (creates imputed_count layer)...")
    t0 = time.time()
    oracle.knn_imputation(n_pca_dims=100, balanced=True, b_sight=500,
                          b_maxl=200, n_jobs=-1)
    log.info(f"  KNN imputation done in {(time.time()-t0)/60:.1f} min")

    log.info("Fitting GRN for simulation (this may take 30-120 minutes)...")
    t0 = time.time()
    oracle.fit_GRN_for_simulation(
        alpha=10,
        use_cluster_specific_TFdict=False,
    )
    elapsed = (time.time() - t0) / 60
    log.info(f"  GRN fitted in {elapsed:.1f} minutes")

    return oracle


def get_simulable_tfs(oracle):
    """Identify which genes CellOracle can simulate (TFs in the base GRN)."""
    base_grn = co.data.load_human_promoter_base_GRN()
    tf_names = set(base_grn.columns[2:])
    oracle_genes = set(oracle.adata.var_names)
    return tf_names & oracle_genes


def simulate_and_score(oracle, target_genes, ctrl_mean, pert_means, pert_counts, var_names):
    """
    For each target gene that is a TF in the base GRN:
    1. Simulate knockdown through the GRN
    2. Extract predicted expression change (delta_X in gene space)
    3. Compare against observed change using Pearson correlation
    """
    simulable = get_simulable_tfs(oracle)
    simulable_targets = [g for g in target_genes if g in simulable and g in pert_means]
    skipped = [g for g in target_genes if g not in simulable]

    log.info(f"Target genes: {len(target_genes)}")
    log.info(f"  Simulable (TFs in base GRN): {len(simulable_targets)}")
    log.info(f"  Skipped (not TFs): {len(skipped)}")

    # Map oracle gene names to indices for scoring
    oracle_gene_list = list(oracle.adata.var_names)
    oracle_gene_set = set(oracle_gene_list)

    # Build a mapping from full-genome gene indices to oracle gene indices
    # for comparing predicted vs observed shifts in the oracle gene space
    var_to_oracle_idx = {}
    for i, vname in enumerate(var_names):
        if vname in oracle_gene_set:
            var_to_oracle_idx[vname] = (i, oracle_gene_list.index(vname))

    log.info(f"  Shared genes for scoring: {len(var_to_oracle_idx)}")

    scores = []
    t0 = time.time()

    for i, gene in enumerate(simulable_targets):
        log.info(f"  [{i+1}/{len(simulable_targets)}] Simulating {gene}...")

        try:
            oracle.simulate_shift(
                perturb_condition={gene: 0.0},
                n_propagation=3,
            )

            # CellOracle stores simulated expression in oracle.adata.layers["simulation"]
            # and the delta (shift) in oracle.adata.layers["delta_X"]
            # OR in oracle.delta_embedding / oracle.adata.obsm["delta_embedding"]
            pred_delta = None

            # Method 1: delta_X layer (per-gene expression changes)
            if "delta_X" in oracle.adata.layers:
                delta_x = oracle.adata.layers["delta_X"]
                pred_delta = np.array(delta_x.mean(axis=0)).flatten()
                log.info(f"    Got delta_X: shape={delta_x.shape}")

            # Method 2: simulate_shift stores delta in adata.obsm
            elif "delta_embedding" in oracle.adata.obsm:
                de = oracle.adata.obsm["delta_embedding"]
                pred_delta = np.array(de.mean(axis=0)).flatten()
                log.info(f"    Got delta_embedding: shape={de.shape}")

            # Method 3: Compute from simulation layer
            elif "simulation" in oracle.adata.layers:
                sim = np.array(oracle.adata.layers["simulation"].mean(axis=0)).flatten()
                imp = np.array(oracle.adata.layers["imputed_count"].mean(axis=0)).flatten()
                pred_delta = sim - imp
                log.info(f"    Computed from simulation-imputed")

            if pred_delta is None:
                log.warning(f"    No prediction output found")
                log.info(f"    Available layers: {list(oracle.adata.layers.keys())}")
                log.info(f"    Available obsm: {list(oracle.adata.obsm.keys())}")
                continue

            # Observed shift (in full genome space) — extract only shared genes
            obs_vals = []
            pred_vals = []
            for vname, (full_idx, oracle_idx) in var_to_oracle_idx.items():
                obs_vals.append(pert_means[gene][full_idx] - ctrl_mean[full_idx])
                pred_vals.append(pred_delta[oracle_idx])

            obs_arr = np.array(obs_vals)
            pred_arr = np.array(pred_vals)

            if np.std(obs_arr) > 1e-10 and np.std(pred_arr) > 1e-10:
                r, p = stats.pearsonr(obs_arr, pred_arr)
            else:
                r, p = 0.0, 1.0

            scores.append({
                "gene": gene,
                "pearson_correlation": round(r, 6),
                "pearson_pvalue": round(p, 10),
                "n_perturbed_cells": pert_counts.get(gene, 0),
                "method": "CellOracle",
            })
            log.info(f"    Pearson r = {r:.4f}")

        except Exception as e:
            log.warning(f"    FAILED: {type(e).__name__}: {e}")

    elapsed = (time.time() - t0) / 60
    log.info(f"  Done: {len(scores)} scored in {elapsed:.1f} min")
    return scores


def main():
    print("=" * 60)
    print("CellOracle K562 Perturbation Benchmark")
    print("Grammar-Aware Model — Local Runner")
    print("=" * 60)
    print(f"RAM: {os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / 1e9:.1f} GB")
    print()

    # Load data
    ctrl_adata = load_control_cells()
    ctrl_mean, pert_means, pert_counts, var_names = load_perturbation_means()
    classes = load_classifications()

    # Target genes: classified AND have perturbation data
    target_genes = sorted(set(classes.keys()) & set(pert_means.keys()))
    log.info(f"Target genes (classified + have pert data): {len(target_genes)}")

    # Preprocess
    adata = preprocess(ctrl_adata)

    # Build GRN
    oracle = build_grn(adata)

    # Simulate and score
    scores = simulate_and_score(oracle, target_genes, ctrl_mean, pert_means, pert_counts, var_names)

    # Write scores
    out_path = RESULTS / "celloracle_k562_per_gene_scores.tsv"
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f,
                           fieldnames=["gene", "pearson_correlation", "pearson_pvalue",
                                       "n_perturbed_cells", "method"],
                           delimiter="\t")
        w.writeheader()
        w.writerows(scores)
    log.info(f"Wrote {out_path}")

    # Summary
    if scores:
        accs = [s["pearson_correlation"] for s in scores]
        print(f"\n{'='*60}")
        print(f"RESULTS SUMMARY")
        print(f"{'='*60}")
        print(f"  Genes scored: {len(scores)}")
        print(f"  Mean Pearson r: {np.mean(accs):.4f}")
        print(f"  Median Pearson r: {np.median(accs):.4f}")
        print(f"  Std: {np.std(accs):.4f}")

        # Quick stratification
        from collections import defaultdict
        by_class = defaultdict(list)
        for s in scores:
            if s["gene"] in classes:
                by_class[classes[s["gene"]]].append(s["pearson_correlation"])

        print(f"\n  Per-class breakdown:")
        for cls in ["I", "II", "III", "IV", "V"]:
            vals = by_class.get(cls, [])
            if vals:
                print(f"    Class {cls}: N={len(vals)}, mean r={np.mean(vals):.4f}")

        print(f"\n  Next: run stratified_analysis_grammar_aware.py")
    else:
        print("\n  No scores produced — check logs for errors")


if __name__ == "__main__":
    main()
