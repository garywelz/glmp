#!/usr/bin/env python3
"""
Run CellOracle on K562 Perturb-seq benchmark.
Follows the protocol from Li et al. (bioRxiv 2024) CellPB benchmark:
uses load_human_promoter_base_GRN (no scATAC-seq required).

Prerequisites:
  conda activate celloracle_env
  pip install celloracle scanpy scipy

Input:
  benchmark_data/k562_perturb_seq.h5ad
  OR download ReplogleWeissman2022_K562_gwps.h5ad from scPerturb

Output:
  results/celloracle_k562_per_gene_scores.tsv
  results/celloracle_grn_topology.tsv  (for Hypothesis 7: GRN concordance)

Estimated runtime: 8–24 hours (CPU, 16+ GB RAM)
"""

import os
import sys
import csv
import time
import logging
from pathlib import Path

import numpy as np
import scanpy as sc
from scipy import stats

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

DATA_PATHS = [
    Path("benchmark_data/ReplogleWeissman2022_K562_essential.h5ad"),
    Path("benchmark_data/k562_perturb_seq.h5ad"),
    Path("ReplogleWeissman2022_K562_essential.h5ad"),
]

# Genes we classified in Phase 1
CLASSIFIED_GENES = Path("k562_benchmark_genes.txt")


def find_data():
    for p in DATA_PATHS:
        if p.exists():
            return p
    print("ERROR: K562 Perturb-seq data not found.")
    print("Please download from:")
    print("  https://virtualcellmodels.cziscience.com/dataset/k562-essential-perturb-seq")
    print("  OR https://zenodo.org/records/10044268")
    print(f"Place the .h5ad file in one of: {[str(p) for p in DATA_PATHS]}")
    sys.exit(1)


def load_and_preprocess(adata_path):
    """Load and preprocess K562 data for CellOracle."""
    log.info(f"Loading {adata_path}...")
    adata = sc.read_h5ad(adata_path)
    log.info(f"  Shape: {adata.shape}")

    # Standard preprocessing
    sc.pp.filter_genes(adata, min_cells=10)
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, n_top_genes=3000)

    # PCA + neighbors for CellOracle
    sc.tl.pca(adata, n_comps=50)
    sc.pp.neighbors(adata, n_pcs=50)
    sc.tl.umap(adata)

    log.info(f"  After preprocessing: {adata.shape}")
    return adata


def build_grn(adata):
    """Build GRN using CellOracle's built-in human promoter base GRN."""
    import celloracle as co

    log.info("Loading human promoter base GRN...")
    base_grn = co.data.load_human_promoter_base_GRN(
        version="hg19_gimmemotifsv5_fpr2"
    )
    log.info(f"  Base GRN: {base_grn.shape}")

    # Initialize Oracle object
    oracle = co.Oracle()
    oracle.import_anndata_as_raw_count(
        adata=adata,
        cluster_column_name="cell_type" if "cell_type" in adata.obs.columns else None,
        embedding_name="X_umap",
    )

    # If no cluster column, add a dummy one (all K562)
    if "cell_type" not in oracle.adata.obs.columns:
        oracle.adata.obs["cell_type"] = "K562"

    oracle.import_TF_data(TF_info_matrix=base_grn)

    log.info("Fitting GRN models (this takes a while)...")
    t0 = time.time()
    oracle.fit_GRN_for_simulation(
        alpha=10,
        use_cluster_specific_TFinfo=False,
    )
    log.info(f"  GRN fitting complete in {(time.time()-t0)/60:.1f} minutes")

    return oracle


def extract_grn_topology(oracle, output_path):
    """Extract the inferred GRN edges for Hypothesis 7 concordance analysis."""
    log.info("Extracting GRN topology...")
    try:
        links = oracle.fitted_GRN
        if hasattr(links, "filtered_links"):
            edges = []
            for cluster, df in links.filtered_links.items():
                for _, row in df.iterrows():
                    edges.append({
                        "source": row.get("source", ""),
                        "target": row.get("target", ""),
                        "coef": row.get("coef_mean", 0),
                        "cluster": cluster,
                    })
            with open(output_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["source", "target", "coef", "cluster"],
                                        delimiter="\t")
                writer.writeheader()
                writer.writerows(edges)
            log.info(f"  Wrote {len(edges)} GRN edges to {output_path}")
    except Exception as e:
        log.warning(f"  Could not extract GRN topology: {e}")


def run_perturbation_simulations(oracle, gene_list):
    """Simulate knockdown for each gene and collect predicted expression changes."""
    log.info(f"Running perturbation simulations for {len(gene_list)} genes...")
    predictions = {}
    total = len(gene_list)

    for i, gene in enumerate(gene_list):
        if (i + 1) % 50 == 0:
            log.info(f"  Progress: {i+1}/{total}")

        try:
            oracle.simulate_shift(
                perturb_condition={gene: 0.0},  # knockdown to 0
                n_propagation=3,
            )
            # Get the predicted shift (delta expression)
            shift = oracle.adata.obsm.get("delta_embedding", None)
            if shift is not None:
                predictions[gene] = {
                    "shift_mean": shift.mean(axis=0),
                    "shift_raw": shift,
                }
            else:
                # Try alternative attribute names
                for attr in ["simulation_result", "perturb_result"]:
                    if hasattr(oracle, attr):
                        result = getattr(oracle, attr)
                        predictions[gene] = {"result": result}
                        break
        except Exception as e:
            log.debug(f"  {gene}: simulation failed ({e})")
            continue

    log.info(f"  Completed {len(predictions)}/{total} simulations")
    return predictions


def score_predictions(adata, predictions, gene_list):
    """
    Score CellOracle predictions against observed expression changes.
    For each perturbed gene, compute Pearson correlation between
    predicted and observed mean expression change vectors.
    """
    log.info("Scoring predictions against observed data...")

    # The scPerturb K562 essential dataset uses:
    #   obs["gene"] for perturbation target (categories include "non-targeting")
    #   obs["perturbation"] also works (categories include "control")
    pert_col = "gene"
    control_label = "non-targeting"
    if pert_col not in adata.obs.columns:
        pert_col = "perturbation"
        control_label = "control"

    control_mask = adata.obs[pert_col] == control_label
    if control_mask.sum() == 0:
        log.error("Cannot identify control cells")
        return []

    ctrl_expr = np.array(adata[control_mask].X.mean(axis=0)).flatten()
    log.info(f"  Control cells: {control_mask.sum()}")

    scores = []
    for gene in gene_list:
        if gene not in predictions:
            continue

        # Observed: mean expression of perturbed cells - control
        pert_mask = adata.obs[pert_col] == gene
        if pert_mask.sum() < 5:
            continue

        obs_expr = np.array(adata[pert_mask].X.mean(axis=0)).flatten()
        obs_delta = obs_expr - ctrl_expr

        # Predicted: CellOracle's simulated shift
        pred = predictions[gene]
        if "shift_mean" in pred:
            pred_delta = pred["shift_mean"]
        else:
            continue

        # Ensure same dimensionality
        min_len = min(len(obs_delta), len(pred_delta))
        obs_delta = obs_delta[:min_len]
        pred_delta = pred_delta[:min_len]

        # Pearson correlation
        if np.std(obs_delta) > 0 and np.std(pred_delta) > 0:
            r, p = stats.pearsonr(obs_delta, pred_delta)
        else:
            r, p = 0.0, 1.0

        scores.append({
            "gene": gene,
            "pearson_correlation": r,
            "pearson_pvalue": p,
            "n_perturbed_cells": int(pert_mask.sum()),
        })

    log.info(f"  Scored {len(scores)} genes")
    return scores


def write_scores(scores, output_path):
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["gene", "pearson_correlation", "pearson_pvalue", "n_perturbed_cells"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(scores)
    log.info(f"Wrote {output_path}")


def main():
    print("=" * 60)
    print("CellOracle K562 Perturb-seq Benchmark Runner")
    print("=" * 60)

    # Load gene list
    with open(CLASSIFIED_GENES) as f:
        gene_list = [line.strip() for line in f if line.strip()]
    log.info(f"Target genes: {len(gene_list)}")

    # Find and load data
    data_path = find_data()
    adata = load_and_preprocess(data_path)

    # Build GRN
    oracle = build_grn(adata)

    # Extract GRN topology for Hypothesis 7
    extract_grn_topology(oracle, RESULTS_DIR / "celloracle_grn_topology.tsv")

    # Run simulations
    predictions = run_perturbation_simulations(oracle, gene_list)

    # Score
    scores = score_predictions(adata, predictions, gene_list)

    # Write
    write_scores(scores, RESULTS_DIR / "celloracle_k562_per_gene_scores.tsv")

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)
    if scores:
        accs = [s["pearson_correlation"] for s in scores]
        print(f"  Genes scored: {len(scores)}")
        print(f"  Mean Pearson r: {np.mean(accs):.4f}")
        print(f"  Median Pearson r: {np.median(accs):.4f}")
    print(f"\nNext: run stratified_analysis_grammar_aware.py")


if __name__ == "__main__":
    main()
