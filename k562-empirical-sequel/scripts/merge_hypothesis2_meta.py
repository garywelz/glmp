#!/usr/bin/env python3
"""
Meta-analysis including GRN propagation (Hypothesis 2 extension).

Adds GRN_Propagation to the same framework as merge_state_de20_results.py:
14 benchmark methods + STATE_HVG + STATE_DE20 (+ optional GRN_Propagation).

Requires:
  results/merged_scores.tsv
  results/state_k562_per_gene_scores.tsv
  results/state_k562_de20_scores.tsv
  results/grn_propagation_scores.tsv   (from run_grn_propagation.py)
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

RESULTS = Path("results")


def load_classes():
    classes = {}
    with open("gene_circuit_classes.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            classes[row["gene"]] = row["circuit_class"]
    return classes


def main():
    state_de20 = {}
    with open(RESULTS / "state_k562_de20_scores.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            state_de20[row["gene"]] = float(row["pearson_correlation"])

    state_hvg = {}
    with open(RESULTS / "state_k562_per_gene_scores.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            state_hvg[row["gene"]] = float(row["pearson_correlation"])

    blind_scores = defaultdict(dict)
    with open(RESULTS / "merged_scores.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            blind_scores[row["method"]][row["gene"]] = float(row["pearson_correlation"])
    methods_14 = sorted(blind_scores.keys())

    grn_path = RESULTS / "grn_propagation_scores.tsv"
    grn_scores = {}
    if grn_path.exists():
        with open(grn_path) as f:
            for row in csv.DictReader(f, delimiter="\t"):
                grn_scores[row["gene"]] = float(row["pearson_correlation"])
        print(f"GRN propagation: {len(grn_scores)} genes")
    else:
        print(f"WARNING: {grn_path} not found — run run_grn_propagation.py first", file=sys.stderr)

    classes = load_classes()
    bench_genes = set(blind_scores[methods_14[0]].keys())
    overlap = bench_genes & set(state_de20.keys())
    class_genes = defaultdict(list)
    for g in overlap:
        class_genes[classes.get(g, "I")].append(g)

    blind_scores["STATE_HVG"] = state_hvg
    blind_scores["STATE_DE20"] = state_de20
    if grn_scores:
        blind_scores["GRN_Propagation"] = grn_scores

    method_list = methods_14 + ["STATE_HVG", "STATE_DE20"]
    if grn_scores:
        method_list.append("GRN_Propagation")

    print(f"\n{'='*72}")
    print(f"META-ANALYSIS: {len(method_list)} methods (14 benchmark + STATE + GRN)")
    print(f"{'='*72}")
    print(f"\n{'Method':22s} {'C1 mean':>8s} {'C3 mean':>8s} {'C3-C1':>8s}")
    print("-" * 52)

    diffs = []
    for m in method_list:
        c1 = [blind_scores[m].get(g, np.nan) for g in class_genes.get("I", [])]
        c3 = [blind_scores[m].get(g, np.nan) for g in class_genes.get("III", [])]
        c1 = [v for v in c1 if not np.isnan(v)]
        c3 = [v for v in c3 if not np.isnan(v)]
        if not c1 or not c3:
            print(f"{m:22s}  (insufficient overlap for C1 or C3)")
            continue
        c1m, c3m = np.mean(c1), np.mean(c3)
        diff = c3m - c1m
        diffs.append(diff)
        mark = ""
        if m in ("STATE_DE20", "GRN_Propagation"):
            mark = " <--"
        print(f"{m:22s} {c1m:8.4f} {c3m:8.4f} {diff:+8.4f}{mark}")

    if diffs:
        arr = np.array(diffs)
        neg = sum(1 for d in arr if d < 0)
        t, p_t = stats.ttest_1samp(arr, 0, alternative="less")
        b = stats.binomtest(neg, len(arr), 0.5, alternative="greater")
        print(f"\n  C3 < C1: {neg}/{len(arr)} methods")
        print(f"  Sign test: p = {b.pvalue:.4f}")
        print(f"  One-sample t vs 0 (less): t = {t:.3f}, p = {p_t:.4f}")

    if grn_scores:
        print(f"\n{'='*72}")
        print("GRN_Propagation: class-stratified mean r (benchmark gene set)")
        print(f"{'='*72}")
        for cls in ["I", "II", "III", "IV", "V"]:
            genes = class_genes.get(cls, [])
            vals = [grn_scores[g] for g in genes if g in grn_scores]
            if vals:
                print(f"  Class {cls}: N={len(vals):3d}, mean r={np.mean(vals):.4f}")


if __name__ == "__main__":
    main()
