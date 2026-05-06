#!/usr/bin/env python3
"""
Effect-size-controlled analysis: tests whether circuit class predicts
prediction accuracy AFTER controlling for perturbation effect size.

Three approaches:
  1. OLS regression: accuracy ~ effect_size + circuit_class
  2. Effect-size-matched subsampling (propensity-style)
  3. Partial correlation: accuracy vs class, controlling for effect size
"""

import csv
import os
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


def load_all_data():
    """Load classifications, PCC scores, and E-distance effect sizes."""
    # Classifications
    classes = {}
    with open("gene_circuit_classes.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            classes[row["gene"]] = row

    # E-distance effect sizes from baseControl
    effect_sizes = {}
    with open("scPerturBench_Results/Genetic_perturbation/genetic_single_performance_top100.csv") as f:
        for row in csv.DictReader(f):
            if "K562" not in row["DataSet"] or row["method"] != "baseControl":
                continue
            gene = row["op"].rsplit("_", 1)[0]
            try:
                effect_sizes[gene] = float(row["edistance_score"])
            except ValueError:
                pass

    # PCC scores (pearson_distance → correlation)
    pcc_scores = defaultdict(dict)
    with open("scPerturBench_Results/Genetic_perturbation/all_dataset_genetic.csv") as f:
        for row in csv.DictReader(f):
            if "K562" not in row["DataSet"] or row["metric"] != "pearson_distance":
                continue
            try:
                pcc_scores[row["method"]][row["perturb"]] = 1.0 - float(row["performance"])
            except ValueError:
                pass

    return classes, effect_sizes, pcc_scores


def build_gene_table(classes, effect_sizes, pcc_scores, method):
    """Build a per-gene table for one method with all needed fields."""
    rows = []
    for gene in classes:
        if gene not in pcc_scores.get(method, {}) or gene not in effect_sizes:
            continue
        cls = classes[gene]["circuit_class"]
        rows.append({
            "gene": gene,
            "class": cls,
            "feedback": 0 if cls == "I" else 1,
            "class_numeric": {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5}[cls],
            "accuracy": pcc_scores[method][gene],
            "effect_size": effect_sizes[gene],
        })
    return rows


def ols_regression(rows, label):
    """OLS: accuracy = β0 + β1*effect_size + β2*feedback + ε"""
    n = len(rows)
    y = np.array([r["accuracy"] for r in rows])
    x_es = np.array([r["effect_size"] for r in rows])
    x_fb = np.array([r["feedback"] for r in rows])

    X = np.column_stack([np.ones(n), x_es, x_fb])
    beta, residuals, rank, sv = np.linalg.lstsq(X, y, rcond=None)

    y_hat = X @ beta
    resid = y - y_hat
    dof = n - 3
    mse = np.sum(resid**2) / dof
    var_beta = mse * np.linalg.inv(X.T @ X)
    se_beta = np.sqrt(np.diag(var_beta))
    t_stats = beta / se_beta
    p_values = 2 * stats.t.sf(np.abs(t_stats), dof)

    r_squared = 1 - np.sum(resid**2) / np.sum((y - np.mean(y))**2)

    lines = []
    lines.append(f"\n  OLS Regression: accuracy ~ effect_size + feedback_class")
    lines.append(f"  N = {n},  R² = {r_squared:.4f}")
    lines.append(f"  {'Variable':20s}  {'β':>8s}  {'SE':>8s}  {'t':>8s}  {'p':>10s}")
    lines.append(f"  {'-'*60}")
    names = ["intercept", "effect_size", "feedback (II-V)"]
    for i, name in enumerate(names):
        sig = "***" if p_values[i] < 0.001 else "**" if p_values[i] < 0.01 else "*" if p_values[i] < 0.05 else "n.s."
        lines.append(f"  {name:20s}  {beta[i]:8.4f}  {se_beta[i]:8.4f}  {t_stats[i]:8.3f}  {p_values[i]:10.6f}  {sig}")

    return "\n".join(lines), beta, p_values


def matched_subsampling(rows, n_iterations=1000):
    """For each feedback gene, match to Class I genes with similar effect size."""
    fb_genes = [r for r in rows if r["feedback"] == 1]
    c1_genes = [r for r in rows if r["feedback"] == 0]
    c1_es = np.array([r["effect_size"] for r in c1_genes])

    np.random.seed(42)
    diffs = []

    for _ in range(n_iterations):
        matched_c1_accs = []
        fb_accs = []
        for fb in fb_genes:
            distances = np.abs(c1_es - fb["effect_size"])
            candidates = np.where(distances < 0.05)[0]
            if len(candidates) == 0:
                candidates = np.argsort(distances)[:5]
            chosen = np.random.choice(candidates)
            matched_c1_accs.append(c1_genes[chosen]["accuracy"])
            fb_accs.append(fb["accuracy"])
        diffs.append(np.mean(matched_c1_accs) - np.mean(fb_accs))

    ci_lo, ci_hi = np.percentile(diffs, [2.5, 97.5])
    mean_diff = np.mean(diffs)

    lines = []
    lines.append(f"\n  Effect-Size Matched Subsampling ({n_iterations} iterations)")
    lines.append(f"  Matching window: ±0.05 E-distance (nearest 5 if none)")
    lines.append(f"  Feedback genes: {len(fb_genes)}")
    lines.append(f"  Mean difference (matched Class I − feedback): {mean_diff:+.4f}")
    lines.append(f"  Bootstrap 95% CI: [{ci_lo:+.4f}, {ci_hi:+.4f}]")
    if ci_lo > 0:
        lines.append(f"  → Class I higher after matching (supports H1)")
    elif ci_hi < 0:
        lines.append(f"  → Feedback higher after matching (opposes H1)")
    else:
        lines.append(f"  → CI includes zero (no significant difference after matching)")

    return "\n".join(lines), mean_diff, ci_lo, ci_hi


def partial_correlation(rows):
    """Partial correlation between accuracy and feedback, controlling for effect size."""
    y = np.array([r["accuracy"] for r in rows])
    x_fb = np.array([r["feedback"] for r in rows])
    x_es = np.array([r["effect_size"] for r in rows])

    # Residualize accuracy on effect_size
    slope_y, intercept_y, _, _, _ = stats.linregress(x_es, y)
    resid_y = y - (slope_y * x_es + intercept_y)

    # Residualize feedback on effect_size
    slope_f, intercept_f, _, _, _ = stats.linregress(x_es, x_fb)
    resid_f = x_fb - (slope_f * x_es + intercept_f)

    r_partial, p_partial = stats.pearsonr(resid_y, resid_f)

    lines = []
    lines.append(f"\n  Partial Correlation: accuracy ~ feedback | effect_size")
    lines.append(f"  r_partial = {r_partial:.4f},  p = {p_partial:.6f}  "
                 f"{'***' if p_partial < 0.001 else '**' if p_partial < 0.01 else '*' if p_partial < 0.05 else 'n.s.'}")
    if r_partial < 0:
        lines.append(f"  Direction: negative (feedback → lower accuracy, as H1 predicts)")
    else:
        lines.append(f"  Direction: positive (feedback → higher accuracy, opposite to H1)")

    return "\n".join(lines), r_partial, p_partial


def effect_size_scatter(rows, method, classes):
    """Figure 4: scatter of effect size vs accuracy, colored by class."""
    fig, ax = plt.subplots(figsize=(10, 7))

    c1 = [r for r in rows if r["class"] == "I"]
    fb = [r for r in rows if r["class"] != "I"]

    ax.scatter(
        [r["effect_size"] for r in c1],
        [r["accuracy"] for r in c1],
        alpha=0.15, s=12, color="#2980b9", label="Class I (N=758)", zorder=1,
    )

    for r in fb:
        color = CLASS_COLORS[r["class"]]
        ax.scatter(
            r["effect_size"], r["accuracy"],
            s=80, color=color, zorder=3, edgecolors="white", linewidth=0.8,
        )
        ax.annotate(
            f"{r['gene']} ({r['class']})",
            (r["effect_size"], r["accuracy"]),
            fontsize=6.5, ha="left", va="bottom",
            xytext=(5, 3), textcoords="offset points",
            color=color, fontweight="bold",
        )

    # Regression line for Class I
    es_c1 = np.array([r["effect_size"] for r in c1])
    acc_c1 = np.array([r["accuracy"] for r in c1])
    slope, intercept, r_val, p_val, _ = stats.linregress(es_c1, acc_c1)
    x_line = np.linspace(es_c1.min(), es_c1.max(), 100)
    ax.plot(x_line, slope * x_line + intercept, "--", color="#2980b9", alpha=0.6,
            label=f"Class I trend (r={r_val:.2f}, p={p_val:.2e})")

    ax.set_xlabel("Perturbation Effect Size (E-distance score)", fontsize=11)
    ax.set_ylabel("Prediction Accuracy (Pearson correlation)", fontsize=11)
    ax.set_title(f"Effect Size vs. Accuracy — {method}\nFeedback genes labeled; Class I trend line shown",
                 fontsize=12, fontweight="bold")

    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="#2980b9", alpha=0.4, label="Class I (feed-forward)"),
    ] + [Patch(facecolor=CLASS_COLORS[c], label=f"Class {c}") for c in ["II", "III", "IV", "V"]]
    ax.legend(handles=legend_elements, fontsize=8, loc="lower right")
    ax.grid(alpha=0.15)

    path = RESULTS_DIR / f"fig4_effect_size_vs_accuracy_{method}.png"
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return str(path)


def main():
    print("Effect-Size Controlled Analysis\n")
    print("Loading data...")
    classes, effect_sizes, pcc_scores = load_all_data()

    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("EFFECT-SIZE CONTROLLED ANALYSIS")
    report_lines.append("=" * 70)
    report_lines.append("")
    report_lines.append("Question: Does circuit class predict accuracy AFTER")
    report_lines.append("controlling for perturbation effect size (E-distance)?")

    for method in ["scGPT", "GEARS", "linearModel", "trainMean"]:
        rows = build_gene_table(classes, effect_sizes, pcc_scores, method)
        if not rows:
            continue

        header = f"\n{'═' * 70}\nMETHOD: {method}  (N = {len(rows)})\n{'═' * 70}"
        report_lines.append(header)
        print(header)

        # Check effect size confound first
        fb = [r for r in rows if r["feedback"] == 1]
        c1 = [r for r in rows if r["feedback"] == 0]
        es_fb = [r["effect_size"] for r in fb]
        es_c1 = [r["effect_size"] for r in c1]
        u, p = stats.mannwhitneyu(es_c1, es_fb, alternative="two-sided")
        confound = (f"\n  Effect-size confound check:"
                    f"\n    Class I effect size:  mean={np.mean(es_c1):.4f}  median={np.median(es_c1):.4f}"
                    f"\n    Feedback effect size: mean={np.mean(es_fb):.4f}  median={np.median(es_fb):.4f}"
                    f"\n    Mann-Whitney p = {p:.6f}  "
                    f"{'→ SIGNIFICANT confound' if p < 0.05 else '→ no significant confound'}")
        report_lines.append(confound)
        print(confound)

        # 1. OLS regression
        ols_text, beta, p_vals = ols_regression(rows, method)
        report_lines.append(ols_text)
        print(ols_text)

        # 2. Matched subsampling
        match_text, mean_diff, ci_lo, ci_hi = matched_subsampling(rows)
        report_lines.append(match_text)
        print(match_text)

        # 3. Partial correlation
        partial_text, r_partial, p_partial = partial_correlation(rows)
        report_lines.append(partial_text)
        print(partial_text)

        # Figure
        fig_path = effect_size_scatter(rows, method, classes)
        report_lines.append(f"\n  Figure: {fig_path}")
        print(f"\n  Figure: {fig_path}")

    # Write report
    report_path = RESULTS_DIR / "effect_size_controlled_tests.txt"
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines) + "\n")
    print(f"\nWrote {report_path}")


if __name__ == "__main__":
    main()
