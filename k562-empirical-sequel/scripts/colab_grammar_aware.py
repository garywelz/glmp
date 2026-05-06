#!/usr/bin/env python3
"""
Grammar-Aware vs Grammar-Blind Perturbation Benchmark
=====================================================

Run this on Google Colab Pro+ (A100 GPU, 25+ GB RAM).

Setup cell for Colab:
  !pip install celloracle scanpy cell-eval arc-state

Downloads K562 essential Perturb-seq data from scPerturb,
runs CellOracle (grammar-aware) and optionally STATE (grammar-blind),
then performs stratified analysis by circuit class.

Upload gene_circuit_classes.tsv to Colab before running.
"""

import os
import sys
import csv
import time
import logging
from pathlib import Path
from collections import defaultdict

import numpy as np
from scipy import stats

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(message)s")
log = logging.getLogger(__name__)

RESULTS = Path("results")
RESULTS.mkdir(exist_ok=True)

# ─────────────────────────────────────────────────────────
#  STEP 0: Download K562 essential Perturb-seq
# ─────────────────────────────────────────────────────────

DATA_PATH = Path("ReplogleWeissman2022_K562_essential.h5ad")


def download_data():
    if DATA_PATH.exists():
        log.info(f"Data already exists: {DATA_PATH}")
        return
    import urllib.request
    url = "https://zenodo.org/api/records/10044268/files/ReplogleWeissman2022_K562_essential.h5ad/content"
    log.info(f"Downloading K562 essential data (1.5 GB)...")
    urllib.request.urlretrieve(url, str(DATA_PATH))
    log.info(f"Downloaded: {DATA_PATH}")


# ─────────────────────────────────────────────────────────
#  STEP 1: Load and preprocess
# ─────────────────────────────────────────────────────────

def load_data():
    import scanpy as sc
    log.info("Loading K562 data...")
    adata = sc.read_h5ad(str(DATA_PATH))
    log.info(f"  Shape: {adata.shape}")
    log.info(f"  Perturbation column: 'gene'")

    unique_perts = adata.obs["gene"].unique()
    log.info(f"  Unique perturbations: {len(unique_perts)} (including non-targeting)")

    return adata


def preprocess_for_celloracle(adata):
    """Standard preprocessing pipeline for CellOracle."""
    import scanpy as sc
    adata = adata.copy()

    sc.pp.filter_genes(adata, min_cells=10)
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, n_top_genes=3000)

    sc.tl.pca(adata, n_comps=50)
    sc.pp.neighbors(adata, n_pcs=50)
    sc.tl.umap(adata)

    if "cell_type" not in adata.obs.columns:
        adata.obs["cell_type"] = "K562"

    log.info(f"  Preprocessed: {adata.shape}")
    return adata


# ─────────────────────────────────────────────────────────
#  STEP 2: CellOracle (grammar-aware)
# ─────────────────────────────────────────────────────────

def run_celloracle(adata_processed, target_genes):
    """
    Build GRN from control cells, simulate knockdown for each target gene.
    Returns per-gene prediction scores.
    """
    import celloracle as co

    log.info("=" * 60)
    log.info("CellOracle: Grammar-Aware Perturbation Prediction")
    log.info("=" * 60)

    # Load built-in human promoter base GRN (no scATAC-seq needed)
    log.info("Loading human promoter base GRN...")
    base_grn = co.data.load_human_promoter_base_GRN()
    log.info(f"  Base GRN: {base_grn.shape}")

    # Initialize Oracle
    oracle = co.Oracle()
    oracle.import_anndata_as_raw_count(
        adata=adata_processed,
        cluster_column_name="cell_type",
        embedding_name="X_umap",
    )
    oracle.import_TF_data(TF_info_matrix=base_grn)

    # Fit GRN
    log.info("Fitting GRN (this takes 30-120 minutes)...")
    t0 = time.time()
    oracle.fit_GRN_for_simulation(alpha=10, use_cluster_specific_TFinfo=False)
    log.info(f"  GRN fitted in {(time.time()-t0)/60:.1f} min")

    # Extract inferred GRN edges for topology analysis
    grn_edges = extract_grn_edges(oracle)

    # Simulate each perturbation
    log.info(f"Simulating {len(target_genes)} knockdowns...")
    results = {}
    t0 = time.time()

    for i, gene in enumerate(target_genes):
        if (i + 1) % 100 == 0:
            elapsed = (time.time() - t0) / 60
            rate = (i + 1) / elapsed
            eta = (len(target_genes) - i - 1) / rate
            log.info(f"  [{i+1}/{len(target_genes)}]  {elapsed:.1f} min elapsed, ~{eta:.0f} min remaining")

        try:
            oracle.simulate_shift(
                perturb_condition={gene: 0.0},
                n_propagation=3,
            )
            # CellOracle stores simulation results in oracle.adata
            if hasattr(oracle, "simulation_result") and oracle.simulation_result is not None:
                results[gene] = oracle.simulation_result.copy()
            elif "delta_embedding" in oracle.adata.obsm:
                results[gene] = oracle.adata.obsm["delta_embedding"].copy()
        except Exception as e:
            log.debug(f"  {gene}: failed ({e})")

    log.info(f"  Completed {len(results)}/{len(target_genes)} simulations "
             f"in {(time.time()-t0)/60:.1f} min")

    return oracle, results, grn_edges


def extract_grn_edges(oracle):
    """Extract GRN topology for concordance analysis."""
    edges = []
    try:
        if hasattr(oracle, "coef_matrix_per_cluster"):
            for cluster, coef_df in oracle.coef_matrix_per_cluster.items():
                for target_gene in coef_df.columns:
                    for tf in coef_df.index:
                        coef = coef_df.loc[tf, target_gene]
                        if abs(coef) > 0:
                            edges.append({"source": tf, "target": target_gene, "coef": coef})
        log.info(f"  Extracted {len(edges)} GRN edges")
    except Exception as e:
        log.warning(f"  Could not extract GRN edges: {e}")
    return edges


def score_celloracle(adata_raw, oracle_results, target_genes):
    """
    Compare CellOracle's predicted expression changes against observed.
    For each gene, compute Pearson correlation of predicted vs observed
    mean expression change vector (all genes).
    """
    import scanpy as sc

    log.info("Scoring CellOracle predictions...")

    # Get control and perturbed mean expression
    control_mask = adata_raw.obs["gene"] == "non-targeting"
    ctrl_mean = np.array(adata_raw[control_mask].X.mean(axis=0)).flatten()

    scores = []
    for gene in target_genes:
        if gene not in oracle_results:
            continue

        # Observed change
        pert_mask = adata_raw.obs["gene"] == gene
        if pert_mask.sum() < 5:
            continue
        pert_mean = np.array(adata_raw[pert_mask].X.mean(axis=0)).flatten()
        obs_delta = pert_mean - ctrl_mean

        # Predicted change from CellOracle
        pred = oracle_results[gene]
        if isinstance(pred, np.ndarray):
            pred_delta = pred.mean(axis=0) if pred.ndim == 2 else pred
        else:
            continue

        # Align dimensions
        min_len = min(len(obs_delta), len(pred_delta))
        if min_len < 10:
            continue

        obs_d = obs_delta[:min_len]
        pred_d = pred_delta[:min_len]

        if np.std(obs_d) > 0 and np.std(pred_d) > 0:
            r, p = stats.pearsonr(obs_d, pred_d)
        else:
            r, p = 0.0, 1.0

        scores.append({
            "gene": gene,
            "pearson_correlation": round(r, 6),
            "pearson_pvalue": round(p, 8),
            "n_perturbed_cells": int(pert_mask.sum()),
            "method": "CellOracle",
        })

    log.info(f"  Scored {len(scores)} / {len(target_genes)} genes")
    return scores


# ─────────────────────────────────────────────────────────
#  STEP 3: Stratified Analysis
# ─────────────────────────────────────────────────────────

def load_classifications(path="gene_circuit_classes.tsv"):
    classes = {}
    with open(path) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            classes[row["gene"]] = row["circuit_class"]
    log.info(f"  Loaded {len(classes)} gene classifications")
    return classes


def stratified_analysis(scores, classes, model_name):
    """Stratify prediction accuracy by circuit class."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"STRATIFIED ANALYSIS: {model_name}")
    lines.append(f"{'='*60}")

    by_class = defaultdict(list)
    for s in scores:
        gene = s["gene"]
        if gene in classes:
            by_class[classes[gene]].append(s["pearson_correlation"])

    lines.append(f"\n  {'Class':6s} {'N':>5s} {'Mean r':>8s} {'Median r':>8s} {'Std':>8s}")
    lines.append(f"  {'-'*45}")

    for cls in ["I", "II", "III", "IV", "V"]:
        vals = by_class.get(cls, [])
        if vals:
            lines.append(f"  {cls:6s} {len(vals):5d} {np.mean(vals):8.4f} {np.median(vals):8.4f} {np.std(vals):8.4f}")

    # Binary: Class I vs feedback
    c1 = by_class.get("I", [])
    fb = []
    for cls in ["II", "III", "IV", "V"]:
        fb.extend(by_class.get(cls, []))

    if c1 and fb:
        lines.append(f"\n  Binary comparison:")
        lines.append(f"    Class I (feed-forward):  N={len(c1)}, mean={np.mean(c1):.4f}")
        lines.append(f"    Class II-V (feedback):   N={len(fb)}, mean={np.mean(fb):.4f}")
        lines.append(f"    Difference (fb - c1):    {np.mean(fb) - np.mean(c1):+.4f}")

        if len(fb) >= 2:
            u, p = stats.mannwhitneyu(c1, fb, alternative="two-sided")
            lines.append(f"    Mann-Whitney U (two-sided): p = {p:.6f}")

            # One-sided: feedback WORSE (our hypothesis for grammar-blind)
            _, p_less = stats.mannwhitneyu(fb, c1, alternative="less")
            lines.append(f"    Mann-Whitney (feedback worse): p = {p_less:.6f}")

            # Effect size (Cohen's d)
            pooled_std = np.sqrt((np.std(c1)**2 + np.std(fb)**2) / 2)
            if pooled_std > 0:
                d = (np.mean(c1) - np.mean(fb)) / pooled_std
                lines.append(f"    Cohen's d: {d:.4f}")

    result = "\n".join(lines)
    print(result)
    return result


def cross_model_interaction(co_scores, blind_scores, classes, blind_name="scGPT"):
    """
    The key test: CLASS x MODEL interaction.
    Is the grammar-aware advantage larger for feedback genes?
    """
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"CLASS x MODEL INTERACTION: CellOracle vs {blind_name}")
    lines.append(f"{'='*60}")

    co_by_gene = {s["gene"]: s["pearson_correlation"] for s in co_scores}
    blind_by_gene = blind_scores

    common = set(co_by_gene.keys()) & set(blind_by_gene.keys()) & set(classes.keys())
    lines.append(f"\n  Common genes: {len(common)}")

    # For each gene, compute advantage = CellOracle - blind
    c1_adv = []
    fb_adv = []
    for gene in common:
        adv = co_by_gene[gene] - blind_by_gene[gene]
        if classes[gene] == "I":
            c1_adv.append(adv)
        else:
            fb_adv.append(adv)

    lines.append(f"\n  Grammar-aware advantage (CellOracle − {blind_name}):")
    lines.append(f"    Class I:    N={len(c1_adv)}, mean Δ = {np.mean(c1_adv):+.4f}")
    if fb_adv:
        lines.append(f"    Feedback:   N={len(fb_adv)}, mean Δ = {np.mean(fb_adv):+.4f}")
        interaction = np.mean(fb_adv) - np.mean(c1_adv)
        lines.append(f"    INTERACTION (fb_Δ − c1_Δ): {interaction:+.4f}")

        if len(fb_adv) >= 2:
            u, p = stats.mannwhitneyu(fb_adv, c1_adv, alternative="greater")
            lines.append(f"    H2 test (feedback advantage > Class I advantage): p = {p:.6f}")
            sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "n.s."
            lines.append(f"    Significance: {sig}")

            lines.append(f"\n  Interpretation:")
            if p < 0.05 and interaction > 0:
                lines.append(f"    HYPOTHESIS SUPPORTED: CellOracle's grammar-aware approach")
                lines.append(f"    shows a larger advantage on feedback genes than Class I genes.")
                lines.append(f"    This is consistent with the conjecture that circuit topology")
                lines.append(f"    (feedback vs feed-forward) determines predictability.")
            else:
                lines.append(f"    Hypothesis not supported at p<0.05.")
                lines.append(f"    Grammar-aware advantage does not differ significantly")
                lines.append(f"    between circuit classes.")

    result = "\n".join(lines)
    print(result)
    return result


# ─────────────────────────────────────────────────────────
#  STEP 4: GRN Concordance Analysis (Hypothesis 7)
# ─────────────────────────────────────────────────────────

def grn_concordance(grn_edges, classes):
    """
    Does CellOracle's inferred GRN agree with our GLMP classification?
    Specifically: do Class II-V genes have more feedback edges in the inferred GRN?
    """
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"GRN CONCORDANCE ANALYSIS (Hypothesis 7)")
    lines.append(f"{'='*60}")

    if not grn_edges:
        lines.append("  No GRN edges extracted — skipping")
        return "\n".join(lines)

    # Build edge set
    import networkx as nx
    G = nx.DiGraph()
    for e in grn_edges:
        G.add_edge(e["source"], e["target"], weight=e["coef"])

    lines.append(f"  Inferred GRN: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    # For each classified gene, check if it participates in feedback loops
    c1_feedback = 0
    c1_total = 0
    fb_feedback = 0
    fb_total = 0

    for gene, cls in classes.items():
        if gene not in G:
            continue

        has_feedback = False
        for nbr in G.successors(gene):
            if nbr == gene:
                has_feedback = True
                break
            for nbr2 in G.successors(nbr):
                if nbr2 == gene:
                    has_feedback = True
                    break
            if has_feedback:
                break

        if cls == "I":
            c1_total += 1
            c1_feedback += int(has_feedback)
        else:
            fb_total += 1
            fb_feedback += int(has_feedback)

    lines.append(f"\n  Class I genes in GRN: {c1_total}, with feedback: {c1_feedback} ({100*c1_feedback/max(c1_total,1):.1f}%)")
    lines.append(f"  Class II-V genes in GRN: {fb_total}, with feedback: {fb_feedback} ({100*fb_feedback/max(fb_total,1):.1f}%)")

    if c1_total > 0 and fb_total > 0:
        # Fisher's exact test
        from scipy.stats import fisher_exact
        table = [[fb_feedback, fb_total - fb_feedback],
                 [c1_feedback, c1_total - c1_feedback]]
        odds, p = fisher_exact(table, alternative="greater")
        lines.append(f"  Fisher's exact (feedback genes more likely in GRN loops): p = {p:.6f}, OR = {odds:.2f}")

    result = "\n".join(lines)
    print(result)
    return result


# ─────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Grammar-Aware vs Grammar-Blind Benchmark")
    print("K562 Essential Gene Perturb-seq")
    print("=" * 60)

    # Download data
    download_data()

    # Load data
    adata = load_data()

    # Load classifications
    classes = load_classifications()

    # Get target genes (intersection of data and classifications)
    data_genes = set(adata.obs["gene"].unique()) - {"non-targeting"}
    target_genes = sorted(set(classes.keys()) & data_genes)
    log.info(f"Target genes (classified & in data): {len(target_genes)}")

    # Preprocess for CellOracle
    adata_processed = preprocess_for_celloracle(adata)

    # Run CellOracle
    oracle, co_results, grn_edges = run_celloracle(adata_processed, target_genes)

    # Score CellOracle predictions
    co_scores = score_celloracle(adata, co_results, target_genes)

    # Save CellOracle scores
    co_path = RESULTS / "celloracle_k562_per_gene_scores.tsv"
    with open(co_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["gene", "pearson_correlation", "pearson_pvalue",
                                          "n_perturbed_cells", "method"], delimiter="\t")
        w.writeheader()
        w.writerows(co_scores)
    log.info(f"Saved CellOracle scores: {co_path}")

    # Save GRN edges
    grn_path = RESULTS / "celloracle_grn_edges.tsv"
    if grn_edges:
        with open(grn_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["source", "target", "coef"], delimiter="\t")
            w.writeheader()
            w.writerows(grn_edges)
        log.info(f"Saved GRN edges: {grn_path}")

    # Stratified analysis
    report_parts = []
    report_parts.append(stratified_analysis(co_scores, classes, "CellOracle"))

    # GRN concordance
    report_parts.append(grn_concordance(grn_edges, classes))

    # Load grammar-blind scores if available (from previous Phase 3)
    blind_path = RESULTS / "merged_scores.tsv"
    if blind_path.exists():
        blind_scores = defaultdict(dict)
        with open(blind_path) as f:
            for row in csv.DictReader(f, delimiter="\t"):
                blind_scores[row["method"]][row["gene"]] = float(row["pearson_correlation"])

        for method_name in ["scGPT", "GEARS"]:
            if method_name in blind_scores:
                report_parts.append(
                    cross_model_interaction(co_scores, blind_scores[method_name],
                                           classes, method_name)
                )

    # Write full report
    report_path = RESULTS / "grammar_comparison_stats.txt"
    with open(report_path, "w") as f:
        f.write("\n".join(report_parts) + "\n")
    log.info(f"Full report: {report_path}")

    # Summary
    if co_scores:
        accs = [s["pearson_correlation"] for s in co_scores]
        print(f"\n{'='*60}")
        print(f"SUMMARY")
        print(f"{'='*60}")
        print(f"  CellOracle genes scored: {len(co_scores)}")
        print(f"  Mean Pearson r: {np.mean(accs):.4f}")
        print(f"  Median Pearson r: {np.median(accs):.4f}")
        print(f"\nAll results saved to {RESULTS}/")


if __name__ == "__main__":
    main()
