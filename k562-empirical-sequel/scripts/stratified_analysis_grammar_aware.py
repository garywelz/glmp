#!/usr/bin/env python3
"""
Phase 3b: Grammar-Aware Stratified Analysis
Compares grammar-blind (scGPT, GEARS) vs grammar-aware (CellOracle)
predictions stratified by circuit class.

Tests Hypothesis 2: grammar-aware models outperform grammar-blind models
specifically on feedback circuit genes (Classes II-V), with the largest
advantage on Class III (bistable).

Inputs:
  - gene_circuit_classes.tsv                         (Phase 1)
  - results/merged_scores.tsv                        (grammar-blind, from Phase 3)
  - results/celloracle_k562_per_gene_scores.tsv      (CellOracle)
  - results/state_k562_per_gene_scores.tsv           (STATE, optional)

Outputs:
  - results/grammar_comparison_stats.txt
  - results/fig5_grammar_blind_vs_aware.png
  - results/fig6_class_x_model_interaction.png
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS_DIR = Path("results")
CLASS_COLORS = {
    "I": "#2980b9", "II": "#27ae60", "III": "#f39c12",
    "IV": "#e67e22", "V": "#c0392b",
}


def load_classifications():
    classes = {}
    with open("gene_circuit_classes.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            classes[row["gene"]] = row["circuit_class"]
    return classes


def load_grammar_blind():
    """Load scGPT and GEARS per-gene scores from Phase 3."""
    scores = defaultdict(dict)
    with open(RESULTS_DIR / "merged_scores.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["method"] in ("scGPT", "GEARS"):
                scores[row["method"]][row["gene"]] = float(row["pearson_correlation"])
    return scores


def load_model_scores(path, model_name):
    """Load per-gene scores from CellOracle or STATE."""
    scores = {}
    if not path.exists():
        print(f"  WARNING: {path} not found — skipping {model_name}")
        return scores
    with open(path) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            try:
                scores[row["gene"]] = float(row["pearson_correlation"])
            except (ValueError, KeyError):
                continue
    print(f"  Loaded {len(scores)} {model_name} scores from {path}")
    return scores


def compare_models(classes, blind_scores, aware_scores, blind_name, aware_name):
    """Compare grammar-blind vs grammar-aware, stratified by class."""
    lines = []
    lines.append(f"\n{'═' * 70}")
    lines.append(f"COMPARISON: {blind_name} (grammar-blind) vs {aware_name} (grammar-aware)")
    lines.append(f"{'═' * 70}")

    # Find common genes
    common = set(blind_scores.keys()) & set(aware_scores.keys()) & set(classes.keys())
    lines.append(f"\n  Common genes: {len(common)}")

    if len(common) < 10:
        lines.append("  Too few common genes for analysis")
        return "\n".join(lines)

    # Per-class comparison
    by_class = defaultdict(lambda: {"blind": [], "aware": [], "diff": []})
    for gene in common:
        cls = classes[gene]
        b = blind_scores[gene]
        a = aware_scores[gene]
        by_class[cls]["blind"].append(b)
        by_class[cls]["aware"].append(a)
        by_class[cls]["diff"].append(a - b)  # positive = aware better

    lines.append(f"\n  Per-class results (positive diff = {aware_name} better):")
    lines.append(f"  {'Class':6s} {'N':>4s} {'Blind mean':>11s} {'Aware mean':>11s} {'Δ(A−B)':>8s} {'p':>10s}")
    lines.append(f"  {'-' * 60}")

    for cls in ["I", "II", "III", "IV", "V"]:
        data = by_class.get(cls)
        if not data or not data["blind"]:
            continue
        n = len(data["blind"])
        b_mean = np.mean(data["blind"])
        a_mean = np.mean(data["aware"])
        d_mean = np.mean(data["diff"])

        if n >= 2:
            _, p = stats.wilcoxon(data["blind"], data["aware"])
        else:
            p = float("nan")

        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "n.s." if not np.isnan(p) else "—"
        lines.append(f"  {cls:6s} {n:4d} {b_mean:11.4f} {a_mean:11.4f} {d_mean:+8.4f} {p:10.6f}  {sig}")

    # Binary: Class I vs feedback
    c1_diff = by_class["I"]["diff"]
    fb_diff = []
    for cls in ["II", "III", "IV", "V"]:
        fb_diff.extend(by_class[cls]["diff"])

    lines.append(f"\n  Binary advantage (aware − blind):")
    lines.append(f"    Class I:     mean Δ = {np.mean(c1_diff):+.4f}  (N={len(c1_diff)})")
    if fb_diff:
        lines.append(f"    Feedback:    mean Δ = {np.mean(fb_diff):+.4f}  (N={len(fb_diff)})")
        lines.append(f"    Interaction: feedback Δ − Class I Δ = {np.mean(fb_diff) - np.mean(c1_diff):+.4f}")

        # Test interaction: is the grammar-aware advantage larger for feedback genes?
        if len(fb_diff) >= 2:
            u, p = stats.mannwhitneyu(fb_diff, c1_diff, alternative="greater")
            lines.append(f"    Mann-Whitney (H2: feedback advantage > Class I advantage): p = {p:.6f}  "
                         f"{'***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'n.s.'}")

    # Hypothesis 2 specific: Class III advantage
    c3_diff = by_class.get("III", {}).get("diff", [])
    if c3_diff:
        lines.append(f"\n  Class III (bistable) specific:")
        lines.append(f"    N = {len(c3_diff)}, mean Δ = {np.mean(c3_diff):+.4f}")
        lines.append(f"    Genes: {[g for g in common if classes[g] == 'III']}")
        if len(c3_diff) >= 2 and len(c1_diff) >= 2:
            u, p = stats.mannwhitneyu(c3_diff, c1_diff, alternative="greater")
            lines.append(f"    H2 test (Class III Δ > Class I Δ): p = {p:.6f}")

    return "\n".join(lines)


def main():
    print("Grammar-Aware Stratified Analysis\n")

    classes = load_classifications()
    print(f"  {len(classes)} genes classified")

    # Load grammar-blind scores
    blind = load_grammar_blind()
    for m in blind:
        print(f"  {m}: {len(blind[m])} genes (grammar-blind)")

    # Load grammar-aware scores
    celloracle = load_model_scores(RESULTS_DIR / "celloracle_k562_per_gene_scores.tsv", "CellOracle")
    state = load_model_scores(RESULTS_DIR / "state_k562_per_gene_scores.tsv", "STATE")

    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("GRAMMAR-BLIND vs GRAMMAR-AWARE STRATIFIED ANALYSIS")
    report_lines.append("=" * 70)

    if celloracle:
        for blind_name in ["scGPT", "GEARS"]:
            if blind_name in blind:
                result = compare_models(classes, blind[blind_name], celloracle,
                                        blind_name, "CellOracle")
                report_lines.append(result)
                print(result)

    if state:
        for blind_name in ["scGPT", "GEARS"]:
            if blind_name in blind:
                result = compare_models(classes, blind[blind_name], state,
                                        blind_name, "STATE")
                report_lines.append(result)
                print(result)

    if not celloracle and not state:
        print("\n  No grammar-aware model scores found yet.")
        print("  Run run_celloracle_k562.py and/or run_state_k562.py first.")
        print("  Then re-run this script.")
        sys.exit(0)

    # Write report
    report_path = RESULTS_DIR / "grammar_comparison_stats.txt"
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines) + "\n")
    print(f"\nWrote {report_path}")


if __name__ == "__main__":
    main()
