#!/usr/bin/env python3
"""
Run STATE (Arc Institute) on K562 Perturb-seq benchmark.
Uses ST-Parse pre-trained model from HuggingFace.

Prerequisites:
  pip install arc-state cell-eval
  # GPU required (A100 recommended, RTX 4090 may work)

Input:
  benchmark_data/k562_perturb_seq.h5ad

Output:
  results/state_k562_per_gene_scores.tsv

Estimated runtime: 4–8 hours on A100
Run on: Google Colab Pro+ / Lambda Labs / local GPU

IMPORTANT: ST-Parse was trained on broad perturbation data.
The model st-x-replogle-full was trained ON Replogle data and
should NOT be used (data leakage). Use ST-Parse for fair evaluation.
"""

import os
import sys
import csv
import time
import logging
import subprocess
from pathlib import Path

import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

DATA_PATHS = [
    Path("benchmark_data/k562_perturb_seq.h5ad"),
    Path("benchmark_data/ReplogleWeissman2022_K562_gwps.h5ad"),
]


def find_data():
    for p in DATA_PATHS:
        if p.exists():
            return p
    print("ERROR: K562 Perturb-seq data not found.")
    print("Please download from:")
    print("  https://virtualcellmodels.cziscience.com/dataset/k562-essential-perturb-seq")
    print(f"Place the .h5ad file in one of: {[str(p) for p in DATA_PATHS]}")
    sys.exit(1)


def download_model():
    """Download ST-Parse from HuggingFace if not present."""
    model_dir = Path("benchmark_data/ST-Parse")
    if model_dir.exists():
        log.info(f"Model found at {model_dir}")
        return model_dir

    log.info("Downloading ST-Parse model from HuggingFace...")
    try:
        subprocess.run([
            "huggingface-cli", "download", "arcinstitute/ST-Parse",
            "--local-dir", str(model_dir),
        ], check=True)
        log.info(f"  Downloaded to {model_dir}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        log.info("Trying alternative download method...")
        subprocess.run([
            sys.executable, "-m", "huggingface_hub", "download",
            "arcinstitute/ST-Parse", "--local-dir", str(model_dir),
        ], check=True)

    return model_dir


def run_inference(data_path, model_dir):
    """Run STATE inference using the CLI tool."""
    output_dir = RESULTS_DIR / "state_raw_output"
    output_dir.mkdir(exist_ok=True)

    log.info("Running STATE inference...")
    log.info(f"  Model: {model_dir}")
    log.info(f"  Data: {data_path}")
    log.info(f"  Output: {output_dir}")

    # Detect perturbation column name
    import scanpy as sc
    adata = sc.read_h5ad(data_path)
    pert_col = None
    for col in ["gene", "perturbation", "guide_id", "condition"]:
        if col in adata.obs.columns:
            pert_col = col
            break

    if pert_col is None:
        log.error("Cannot identify perturbation column")
        sys.exit(1)

    log.info(f"  Perturbation column: {pert_col}")
    del adata  # free memory before inference

    t0 = time.time()
    cmd = [
        "state", "tx", "infer",
        "--model_dir", str(model_dir),
        "--pert_col", pert_col,
        "--adata", str(data_path),
        "--output", str(output_dir),
    ]
    log.info(f"  Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = (time.time() - t0) / 60

    if result.returncode != 0:
        log.error(f"STATE inference failed:\n{result.stderr}")
        sys.exit(1)

    log.info(f"  Inference complete in {elapsed:.1f} minutes")
    return output_dir


def score_predictions(data_path, output_dir):
    """
    Score STATE predictions using cell-eval metrics.
    Alternatively, compute Pearson correlation manually.
    """
    log.info("Scoring STATE predictions...")

    # Try cell-eval first
    try:
        cmd = [
            "cell-eval", "score",
            "--predicted", str(output_dir),
            "--observed", str(data_path),
            "--output", str(RESULTS_DIR / "state_celleval_scores.tsv"),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            log.info("  Scored with cell-eval")
            return parse_celleval_scores(RESULTS_DIR / "state_celleval_scores.tsv")
    except FileNotFoundError:
        pass

    # Manual scoring fallback
    log.info("  Falling back to manual scoring...")
    return manual_scoring(data_path, output_dir)


def manual_scoring(data_path, output_dir):
    """Compute per-gene Pearson correlation between predicted and observed."""
    import scanpy as sc
    from scipy import stats as sp_stats

    adata_obs = sc.read_h5ad(data_path)
    # Load predictions
    pred_files = list(output_dir.glob("*.h5ad"))
    if not pred_files:
        log.error("No prediction files found")
        return []

    adata_pred = sc.read_h5ad(pred_files[0])

    scores = []
    # Implementation depends on STATE output format
    # This is a skeleton — adapt based on actual output structure
    log.warning("Manual scoring requires adaptation to STATE output format.")
    log.warning("Please use cell-eval for accurate scoring.")

    return scores


def parse_celleval_scores(path):
    """Parse cell-eval output into our standard format."""
    scores = []
    with open(path) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            scores.append({
                "gene": row.get("gene", row.get("perturbation", "")),
                "pearson_correlation": float(row.get("pearson", row.get("pcc", 0))),
                "pearson_pvalue": 0.0,
                "n_perturbed_cells": 0,
            })
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
    print("STATE K562 Perturb-seq Benchmark Runner")
    print("=" * 60)

    # Check GPU
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_mem = torch.cuda.get_device_properties(0).total_mem / 1e9
            log.info(f"GPU: {gpu_name} ({gpu_mem:.1f} GB)")
        else:
            log.warning("No GPU detected! STATE requires GPU for reasonable runtime.")
            response = input("Continue anyway? [y/N] ")
            if response.lower() != "y":
                sys.exit(0)
    except ImportError:
        log.warning("PyTorch not installed — cannot check GPU")

    data_path = find_data()
    model_dir = download_model()

    output_dir = run_inference(data_path, model_dir)
    scores = score_predictions(data_path, output_dir)

    if scores:
        write_scores(scores, RESULTS_DIR / "state_k562_per_gene_scores.tsv")
        accs = [s["pearson_correlation"] for s in scores]
        print(f"\n  Genes scored: {len(scores)}")
        print(f"  Mean Pearson r: {np.mean(accs):.4f}")
    else:
        print("\n  No scores produced. Check cell-eval output format.")

    print(f"\nNext: run stratified_analysis_grammar_aware.py")


if __name__ == "__main__":
    main()
