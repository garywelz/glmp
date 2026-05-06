#!/usr/bin/env python3
"""
Phase 3: Stratified Analysis
Merges gene circuit classifications with scPerturBench K562 benchmark scores,
runs statistical tests for Hypothesis 1 (accuracy gradient by circuit class),
and generates figures.

Inputs:
  - gene_circuit_classes.tsv          (Phase 1 output)
  - scPerturBench_Results/Genetic_perturbation/all_dataset_genetic.csv

Outputs:
  - results/merged_scores.tsv
  - results/statistical_tests.txt
  - results/fig1_accuracy_by_class.png
  - results/fig2_method_comparison.png
  - results/fig3_class1_vs_feedback.png
"""

import csv
import os
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

CLASS_FILE = Path("gene_circuit_classes.tsv")
BENCH_FILE = Path("scPerturBench_Results/Genetic_perturbation/all_dataset_genetic.csv")

FOCUS_METHODS = ["scGPT", "GEARS", "GeneCompass", "linearModel", "trainMean"]
CLASS_COLORS = {
    "I": "#2980b9", "II": "#27ae60", "III": "#f39c12",
    "IV": "#e67e22", "V": "#c0392b",
}
FEEDBACK_COLORS = {"I (feed-forward)": "#2980b9", "II+ (feedback)": "#c0392b"}


def load_classifications():
    classes = {}
    with open(CLASS_FILE) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            classes[row["gene"]] = row
    return classes


def load_benchmark_scores():
    """Load K562 Pearson distance scores from scPerturBench."""
    scores = defaultdict(dict)
    with open(BENCH_FILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "K562" not in row["DataSet"]:
                continue
            if row["metric"] != "pearson_distance":
                continue
            method = row["method"]
            gene = row["perturb"]
            try:
                val = float(row["performance"])
            except (ValueError, KeyError):
                continue
            scores[method][gene] = val
    return scores


def merge_data(classes, scores):
    """Merge classifications with benchmark scores. Return list of dicts."""
    merged = []
    for method in sorted(scores.keys()):
        for gene, score in scores[method].items():
            if gene not in classes:
                continue
            cls_info = classes[gene]
            pearson_corr = 1.0 - score
            merged.append({
                "gene": gene,
                "method": method,
                "pearson_distance": score,
                "pearson_correlation": pearson_corr,
                "circuit_class": cls_info["circuit_class"],
                "topology_type": cls_info["topology_type"],
                "evidence_source": cls_info["evidence_source"],
                "confidence": cls_info["confidence"],
                "feedback_group": "I (feed-forward)" if cls_info["circuit_class"] == "I" else "II+ (feedback)",
            })
    return merged


def write_merged(merged):
    path = RESULTS_DIR / "merged_scores.tsv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["gene", "method", "pearson_correlation", "pearson_distance",
                         "circuit_class", "feedback_group", "topology_type",
                         "evidence_source", "confidence"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(merged)
    print(f"  Wrote {path} ({len(merged)} rows)")


def run_statistics(merged, out):
    """Run all statistical tests and write report."""
    lines = []
    def p(text=""):
        lines.append(text)
        print(text)

    p("=" * 70)
    p("STRATIFIED ANALYSIS: STATISTICAL TESTS")
    p("=" * 70)

    for method in FOCUS_METHODS:
        rows = [r for r in merged if r["method"] == method]
        if not rows:
            continue

        p(f"\n{'─' * 70}")
        p(f"METHOD: {method}  (N = {len(rows)} genes)")
        p(f"{'─' * 70}")

        # Group by class
        by_class = defaultdict(list)
        for r in rows:
            by_class[r["circuit_class"]].append(r["pearson_correlation"])

        p(f"\n  Per-class summary:")
        for cls in ["I", "II", "III", "IV", "V"]:
            vals = by_class.get(cls, [])
            if vals:
                p(f"    Class {cls}: N={len(vals):4d}  "
                  f"mean={np.mean(vals):.4f}  median={np.median(vals):.4f}  "
                  f"std={np.std(vals):.4f}  "
                  f"[{np.percentile(vals,25):.4f}, {np.percentile(vals,75):.4f}]")
            else:
                p(f"    Class {cls}: N=   0")

        # Binary: Class I vs II+
        class1 = [r["pearson_correlation"] for r in rows if r["circuit_class"] == "I"]
        feedback = [r["pearson_correlation"] for r in rows if r["circuit_class"] != "I"]

        p(f"\n  Binary comparison (Class I vs. Classes II-V combined):")
        p(f"    Class I      : N={len(class1):4d}  mean={np.mean(class1):.4f}  median={np.median(class1):.4f}")
        if feedback:
            p(f"    Classes II-V : N={len(feedback):4d}  mean={np.mean(feedback):.4f}  median={np.median(feedback):.4f}")
            p(f"    Difference   : {np.mean(class1) - np.mean(feedback):+.4f} (Class I − feedback)")
        else:
            p(f"    Classes II-V : N=   0  (no feedback genes matched)")
            continue

        # Mann-Whitney U test (two-sided)
        if len(feedback) >= 2:
            u_stat, u_p = stats.mannwhitneyu(class1, feedback, alternative="two-sided")
            p(f"\n  Mann-Whitney U test (Class I vs II+):")
            p(f"    U = {u_stat:.1f},  p = {u_p:.6f}  {'***' if u_p<0.001 else '**' if u_p<0.01 else '*' if u_p<0.05 else 'n.s.'}")

            # One-sided: Class I > feedback (our hypothesis)
            _, u_p_one = stats.mannwhitneyu(class1, feedback, alternative="greater")
            p(f"    One-sided (H1: Class I > feedback): p = {u_p_one:.6f}  {'***' if u_p_one<0.001 else '**' if u_p_one<0.01 else '*' if u_p_one<0.05 else 'n.s.'}")

        # Welch's t-test
        if len(feedback) >= 2:
            t_stat, t_p = stats.ttest_ind(class1, feedback, equal_var=False)
            p(f"\n  Welch's t-test (Class I vs II+):")
            p(f"    t = {t_stat:.3f},  p = {t_p:.6f}  {'***' if t_p<0.001 else '**' if t_p<0.01 else '*' if t_p<0.05 else 'n.s.'}")

        # Effect size (Cohen's d)
        if len(feedback) >= 2:
            pooled_std = np.sqrt(
                ((len(class1)-1)*np.var(class1, ddof=1) + (len(feedback)-1)*np.var(feedback, ddof=1))
                / (len(class1) + len(feedback) - 2)
            )
            if pooled_std > 0:
                cohens_d = (np.mean(class1) - np.mean(feedback)) / pooled_std
                p(f"    Cohen's d = {cohens_d:.3f}  "
                  f"({'large' if abs(cohens_d) > 0.8 else 'medium' if abs(cohens_d) > 0.5 else 'small' if abs(cohens_d) > 0.2 else 'negligible'})")

        # Kruskal-Wallis across all classes with N >= 2
        valid_groups = [(cls, vals) for cls, vals in sorted(by_class.items()) if len(vals) >= 2]
        if len(valid_groups) >= 2:
            kw_stat, kw_p = stats.kruskal(*[v for _, v in valid_groups])
            group_labels = ", ".join(f"{c}(N={len(v)})" for c, v in valid_groups)
            p(f"\n  Kruskal-Wallis (classes with N≥2: {group_labels}):")
            p(f"    H = {kw_stat:.3f},  p = {kw_p:.6f}  {'***' if kw_p<0.001 else '**' if kw_p<0.01 else '*' if kw_p<0.05 else 'n.s.'}")

        # Bootstrap CI for the mean difference
        if len(feedback) >= 2:
            np.random.seed(42)
            n_boot = 10000
            diffs = []
            for _ in range(n_boot):
                boot_c1 = np.random.choice(class1, size=len(class1), replace=True)
                boot_fb = np.random.choice(feedback, size=len(feedback), replace=True)
                diffs.append(np.mean(boot_c1) - np.mean(boot_fb))
            ci_lo, ci_hi = np.percentile(diffs, [2.5, 97.5])
            p(f"\n  Bootstrap 95% CI for mean difference (Class I − feedback):")
            p(f"    [{ci_lo:+.4f}, {ci_hi:+.4f}]")
            if ci_lo > 0:
                p(f"    CI excludes zero → Class I significantly higher")
            elif ci_hi < 0:
                p(f"    CI excludes zero → Feedback genes significantly higher")
            else:
                p(f"    CI includes zero → no significant difference")

        # List the feedback genes with their scores
        feedback_rows = sorted(
            [r for r in rows if r["circuit_class"] != "I"],
            key=lambda r: r["circuit_class"]
        )
        p(f"\n  Feedback gene details:")
        for r in feedback_rows:
            p(f"    {r['gene']:10s}  Class {r['circuit_class']}  "
              f"r={r['pearson_correlation']:.4f}  ({r['topology_type']})")

    report = "\n".join(lines)
    with open(out, "w") as f:
        f.write(report + "\n")
    print(f"\n  Wrote {out}")
    return report


def make_figures(merged):
    """Generate publication figures."""
    # ── Figure 1: Box plots of accuracy by class (scGPT + scFoundation) ──
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    for ax, method in zip(axes, ["scGPT", "GEARS"]):
        rows = [r for r in merged if r["method"] == method]
        by_class = defaultdict(list)
        for r in rows:
            by_class[r["circuit_class"]].append(r["pearson_correlation"])

        classes_present = [c for c in ["I", "II", "III", "IV", "V"] if c in by_class]
        data = [by_class[c] for c in classes_present]
        positions = list(range(len(classes_present)))
        colors = [CLASS_COLORS[c] for c in classes_present]

        bp = ax.boxplot(data, positions=positions, widths=0.6, patch_artist=True,
                        showfliers=True, flierprops=dict(marker=".", markersize=3, alpha=0.3))
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        for median in bp["medians"]:
            median.set_color("black")
            median.set_linewidth(1.5)

        ax.set_xticks(positions)
        ax.set_xticklabels([f"Class {c}\n(N={len(by_class[c])})" for c in classes_present],
                           fontsize=9)
        ax.set_title(method, fontsize=13, fontweight="bold")
        ax.set_ylabel("Pearson correlation (1 − distance)" if ax == axes[0] else "")
        ax.axhline(y=0, color="gray", linestyle="--", alpha=0.3)
        ax.grid(axis="y", alpha=0.2)

    fig.suptitle("Prediction Accuracy by Circuit Complexity Class — K562 Perturb-seq",
                 fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    path = RESULTS_DIR / "fig1_accuracy_by_class.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Wrote {path}")

    # ── Figure 2: Binary comparison across all methods ──────────────────
    fig, ax = plt.subplots(figsize=(12, 6))
    method_names = []
    class1_means = []
    feedback_means = []
    class1_sems = []
    feedback_sems = []

    for method in sorted(set(r["method"] for r in merged)):
        rows = [r for r in merged if r["method"] == method]
        c1 = [r["pearson_correlation"] for r in rows if r["circuit_class"] == "I"]
        fb = [r["pearson_correlation"] for r in rows if r["circuit_class"] != "I"]
        if not fb:
            continue
        method_names.append(method)
        class1_means.append(np.mean(c1))
        feedback_means.append(np.mean(fb))
        class1_sems.append(np.std(c1) / np.sqrt(len(c1)))
        feedback_sems.append(np.std(fb) / np.sqrt(len(fb)))

    x = np.arange(len(method_names))
    width = 0.35
    bars1 = ax.bar(x - width/2, class1_means, width, yerr=class1_sems,
                   label="Class I (feed-forward)", color="#2980b9", alpha=0.8,
                   capsize=3, error_kw=dict(lw=0.8))
    bars2 = ax.bar(x + width/2, feedback_means, width, yerr=feedback_sems,
                   label="Classes II–V (feedback)", color="#c0392b", alpha=0.8,
                   capsize=3, error_kw=dict(lw=0.8))

    ax.set_ylabel("Mean Pearson correlation", fontsize=11)
    ax.set_title("Class I vs. Feedback Genes: Prediction Accuracy Across 14 Methods",
                 fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(method_names, rotation=45, ha="right", fontsize=8)
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.2)
    ax.axhline(y=0, color="gray", linestyle="--", alpha=0.3)
    fig.tight_layout()
    path = RESULTS_DIR / "fig2_method_comparison.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Wrote {path}")

    # ── Figure 3: Strip plot with individual feedback gene labels ────────
    fig, ax = plt.subplots(figsize=(10, 7))
    for method in ["scGPT", "GEARS"]:
        rows = [r for r in merged if r["method"] == method]
        c1 = [r["pearson_correlation"] for r in rows if r["circuit_class"] == "I"]
        fb_rows = [r for r in rows if r["circuit_class"] != "I"]

        offset = -0.15 if method == "scGPT" else 0.15
        ax.scatter(
            [0 + offset] * len(c1), c1,
            alpha=0.03, s=8, color="#2980b9", zorder=1,
        )
        for r in fb_rows:
            color = CLASS_COLORS[r["circuit_class"]]
            ax.scatter(
                1 + offset, r["pearson_correlation"],
                s=50, color=color, zorder=3, edgecolors="white", linewidth=0.5,
            )
            ax.annotate(
                f"{r['gene']} ({r['circuit_class']})",
                (1 + offset, r["pearson_correlation"]),
                fontsize=5.5, ha="left", va="center",
                xytext=(8, 0), textcoords="offset points",
                color=color, fontweight="bold",
            )

        c1_mean = np.mean(c1)
        fb_mean = np.mean([r["pearson_correlation"] for r in fb_rows]) if fb_rows else 0
        ax.plot([offset - 0.08, offset + 0.08], [c1_mean, c1_mean],
                color="black", linewidth=2, zorder=4)
        if fb_rows:
            ax.plot([1 + offset - 0.08, 1 + offset + 0.08], [fb_mean, fb_mean],
                    color="black", linewidth=2, zorder=4)

    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Class I\n(feed-forward, N=758)", "Classes II–V\n(feedback, N=22)"],
                       fontsize=11)
    ax.set_ylabel("Pearson correlation", fontsize=11)
    ax.set_title("Individual Gene Scores: Feed-Forward vs. Feedback Circuits\n(scGPT left, GEARS right within each group)",
                 fontsize=12, fontweight="bold")
    legend_elements = [Patch(facecolor=c, label=f"Class {k}") for k, c in CLASS_COLORS.items()]
    ax.legend(handles=legend_elements, fontsize=9, loc="lower left")
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    path = RESULTS_DIR / "fig3_class1_vs_feedback.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Wrote {path}")


def main():
    print("Phase 3: Stratified Analysis\n")

    print("1. Loading classifications...")
    classes = load_classifications()
    print(f"   {len(classes)} genes classified")

    print("2. Loading benchmark scores...")
    scores = load_benchmark_scores()
    print(f"   {len(scores)} methods loaded")
    for m in sorted(scores.keys()):
        print(f"     {m}: {len(scores[m])} genes")

    print("3. Merging...")
    merged = merge_data(classes, scores)
    write_merged(merged)

    # Quick match stats
    methods_genes = set()
    class_genes = set(classes.keys())
    for m in scores:
        methods_genes |= set(scores[m].keys())
    matched = methods_genes & class_genes
    print(f"   Genes in benchmark: {len(methods_genes)}")
    print(f"   Genes classified:   {len(class_genes)}")
    print(f"   Matched:            {len(matched)}")
    unmatched = methods_genes - class_genes
    if unmatched:
        print(f"   Unmatched benchmark genes: {len(unmatched)} (first 10: {sorted(list(unmatched))[:10]})")

    print("\n4. Statistical tests...")
    report = run_statistics(merged, RESULTS_DIR / "statistical_tests.txt")

    print("\n5. Generating figures...")
    make_figures(merged)

    print("\n" + "=" * 70)
    print("PHASE 3 COMPLETE")
    print("=" * 70)
    print(f"  results/merged_scores.tsv")
    print(f"  results/statistical_tests.txt")
    print(f"  results/fig1_accuracy_by_class.png")
    print(f"  results/fig2_method_comparison.png")
    print(f"  results/fig3_class1_vs_feedback.png")


if __name__ == "__main__":
    main()
