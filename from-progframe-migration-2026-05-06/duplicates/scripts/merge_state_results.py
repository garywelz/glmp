#!/usr/bin/env python3
"""
Merge STATE results into the existing analysis.
Run after downloading state_k562_per_gene_scores.tsv from Colab.

Usage:
  python merge_state_results.py results/state_k562_per_gene_scores.tsv
"""
import csv
import sys
import numpy as np
from scipy import stats
from collections import defaultdict

def main():
    if len(sys.argv) < 2:
        state_path = "results/state_k562_per_gene_scores.tsv"
    else:
        state_path = sys.argv[1]

    # Load STATE scores
    state_scores = {}
    with open(state_path) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            state_scores[row["gene"]] = float(row["pearson_correlation"])
    print(f"STATE scores loaded: {len(state_scores)} genes")

    # Load existing grammar-blind scores
    blind_scores = defaultdict(dict)
    with open("results/merged_scores.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            blind_scores[row["method"]][row["gene"]] = float(row["pearson_correlation"])
    methods = sorted(blind_scores.keys())

    # Load classifications
    classes = {}
    with open("gene_circuit_classes.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            classes[row["gene"]] = row["circuit_class"]

    bench = set(blind_scores[methods[0]].keys())
    overlap = bench & set(state_scores.keys())
    print(f"Overlap with benchmark genes: {len(overlap)}")

    # Add STATE to methods
    all_methods = methods + ["STATE"]
    for gene, r in state_scores.items():
        blind_scores["STATE"][gene] = r

    # Per-class analysis
    print(f"\n{'='*72}")
    print(f"STATE vs OTHER METHODS — Per-Class Analysis")
    print(f"{'='*72}")

    class_genes = defaultdict(list)
    for g in overlap:
        class_genes[classes.get(g, "I")].append(g)

    print(f"\n{'Class':6s} {'N':>4s} {'STATE':>8s} {'Others':>8s} {'Diff':>8s}")
    print("-" * 40)
    for cls in ["I", "II", "III", "IV", "V"]:
        genes = class_genes.get(cls, [])
        if not genes:
            continue
        st = [state_scores[g] for g in genes if g in state_scores]
        ot = [np.mean([blind_scores[m][g] for m in methods]) for g in genes]
        print(f"{cls:6s} {len(genes):4d} {np.mean(st):8.4f} {np.mean(ot):8.4f} "
              f"{np.mean(st)-np.mean(ot):+8.4f}")

    # Class I vs Class III for STATE specifically
    c1 = [state_scores[g] for g in class_genes.get("I", []) if g in state_scores]
    c3 = [state_scores[g] for g in class_genes.get("III", []) if g in state_scores]

    if c1 and c3:
        print(f"\n{'='*72}")
        print(f"STATE: CLASS I vs CLASS III")
        print(f"{'='*72}")
        print(f"Class I:   N={len(c1)}, mean r={np.mean(c1):.4f}")
        print(f"Class III: N={len(c3)}, mean r={np.mean(c3):.4f}")
        print(f"Diff: {np.mean(c3)-np.mean(c1):+.4f}")
        if len(c3) >= 2:
            u, p = stats.mannwhitneyu(c3, c1, alternative="less")
            print(f"Mann-Whitney (H1: C3 < C1): p={p:.4f}")

    # Meta-analysis: add STATE to the 14-method comparison
    print(f"\n{'='*72}")
    print(f"UPDATED META-ANALYSIS (15 methods including STATE)")
    print(f"{'='*72}")

    diffs_c3_c1 = []
    for m in all_methods:
        c1_vals = [blind_scores[m].get(g, np.nan) for g in class_genes.get("I", [])]
        c3_vals = [blind_scores[m].get(g, np.nan) for g in class_genes.get("III", [])]
        c1_vals = [v for v in c1_vals if not np.isnan(v)]
        c3_vals = [v for v in c3_vals if not np.isnan(v)]
        if c1_vals and c3_vals:
            diff = np.mean(c3_vals) - np.mean(c1_vals)
            diffs_c3_c1.append(diff)
            marker = " <-- STATE" if m == "STATE" else ""
            print(f"  {m:16s}: C3-C1 = {diff:+.4f}{marker}")

    md = np.array(diffs_c3_c1)
    neg = sum(1 for d in md if d < 0)
    t, p_t = stats.ttest_1samp(md, 0, alternative="less")
    result = stats.binomtest(neg, len(md), 0.5, alternative="greater")
    print(f"\n  C3 < C1 in: {neg}/{len(md)} methods")
    print(f"  Sign test: p={result.pvalue:.4f}")
    print(f"  One-sample t: t={t:.3f}, p={p_t:.4f}")

if __name__ == "__main__":
    main()
