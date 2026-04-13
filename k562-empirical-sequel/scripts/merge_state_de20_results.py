"""
Merge STATE DE20 results into the meta-analysis.
Compare STATE_DE20 vs STATE_HVG vs 14 benchmark methods.
"""
import csv
import numpy as np
from scipy import stats
from collections import defaultdict

def main():
    # Load STATE DE20 scores
    state_de20 = {}
    with open("results/state_k562_de20_scores.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            state_de20[row["gene"]] = float(row["pearson_correlation"])
    print(f"STATE DE20 scores: {len(state_de20)} genes")
    print(f"  Mean r = {np.mean(list(state_de20.values())):.4f}")
    print(f"  Median r = {np.median(list(state_de20.values())):.4f}")

    # Load STATE HVG scores (original)
    state_hvg = {}
    with open("results/state_k562_per_gene_scores.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            state_hvg[row["gene"]] = float(row["pearson_correlation"])
    print(f"\nSTATE HVG scores: {len(state_hvg)} genes")
    print(f"  Mean r = {np.mean(list(state_hvg.values())):.4f}")

    # Load benchmark scores
    blind_scores = defaultdict(dict)
    with open("results/merged_scores.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            blind_scores[row["method"]][row["gene"]] = float(row["pearson_correlation"])
    methods_14 = sorted(blind_scores.keys())
    print(f"\n14 benchmark methods loaded")

    # Load classifications
    classes = {}
    with open("gene_circuit_classes.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            classes[row["gene"]] = row["circuit_class"]

    # Benchmark gene set
    bench_genes = set(blind_scores[methods_14[0]].keys())
    overlap_de20 = bench_genes & set(state_de20.keys())
    print(f"Overlap (benchmark ∩ STATE_DE20): {len(overlap_de20)} genes")

    # Per-class gene lists
    class_genes = defaultdict(list)
    for g in overlap_de20:
        class_genes[classes.get(g, "I")].append(g)

    # ============================================================
    print(f"\n{'='*72}")
    print("COMPARISON: STATE_DE20 vs STATE_HVG vs 14 BENCHMARK METHODS")
    print(f"{'='*72}")

    print(f"\n{'Class':6s} {'N':>4s} {'14-method':>10s} {'STATE_HVG':>10s} {'STATE_DE20':>11s}")
    print("-" * 50)
    for cls in ["I", "II", "III", "IV", "V"]:
        genes = class_genes.get(cls, [])
        if not genes:
            continue
        bench_r = np.mean([np.mean([blind_scores[m][g] for m in methods_14]) for g in genes])
        hvg_r = np.mean([state_hvg.get(g, np.nan) for g in genes if g in state_hvg])
        de20_r = np.mean([state_de20[g] for g in genes])
        print(f"{cls:6s} {len(genes):4d} {bench_r:10.4f} {hvg_r:10.4f} {de20_r:11.4f}")

    # ============================================================
    print(f"\n{'='*72}")
    print("META-ANALYSIS: 14 methods + STATE_DE20 (16 total)")
    print(f"{'='*72}")

    # Add STATE_DE20 to methods
    all_methods_16 = methods_14 + ["STATE_HVG", "STATE_DE20"]
    blind_scores["STATE_HVG"] = state_hvg
    blind_scores["STATE_DE20"] = state_de20

    diffs = []
    print(f"\n{'Method':20s} {'C1 mean':>8s} {'C3 mean':>8s} {'C3-C1':>8s} {'Dir':>10s}")
    print("-" * 60)
    for m in all_methods_16:
        c1_vals = [blind_scores[m].get(g, np.nan) for g in class_genes.get("I", [])]
        c3_vals = [blind_scores[m].get(g, np.nan) for g in class_genes.get("III", [])]
        c1_vals = [v for v in c1_vals if not np.isnan(v)]
        c3_vals = [v for v in c3_vals if not np.isnan(v)]
        if not c1_vals or not c3_vals:
            continue
        c1m = np.mean(c1_vals)
        c3m = np.mean(c3_vals)
        diff = c3m - c1m
        diffs.append((m, diff))
        direction = "C3 harder" if diff < 0 else "~equal" if abs(diff) < 0.01 else "C3 easier"
        marker = " <--" if "STATE" in m else ""
        print(f"{m:20s} {c1m:8.4f} {c3m:8.4f} {diff:+8.4f} {direction:>10s}{marker}")

    # Stats on all 16
    all_diffs = np.array([d for _, d in diffs])
    neg = sum(1 for d in all_diffs if d < 0)
    t, p_t = stats.ttest_1samp(all_diffs, 0, alternative="less")
    binom = stats.binomtest(neg, len(all_diffs), 0.5, alternative="greater")

    print(f"\n  Methods with C3 < C1: {neg}/{len(all_diffs)}")
    print(f"  Sign test: p = {binom.pvalue:.4f}")
    print(f"  One-sample t-test: t = {t:.3f}, p = {p_t:.4f}")
    print(f"  Mean C3-C1 difference: {all_diffs.mean():.4f}")

    # Also show original 15-method result for comparison
    print(f"\n{'='*72}")
    print("COMPARISON: ORIGINAL 15-METHOD vs NEW 16-METHOD")
    print(f"{'='*72}")

    diffs_15 = [d for m, d in diffs if m != "STATE_DE20"]
    diffs_15 = np.array(diffs_15)
    t15, p15 = stats.ttest_1samp(diffs_15, 0, alternative="less")
    neg15 = sum(1 for d in diffs_15 if d < 0)

    print(f"  Original 15 methods: {neg15}/{len(diffs_15)} show C3<C1, t={t15:.3f}, p={p15:.4f}")
    print(f"  New 16 methods:      {neg}/{len(all_diffs)} show C3<C1, t={t:.3f}, p={p_t:.4f}")

    # ============================================================
    print(f"\n{'='*72}")
    print("STATE_DE20: CLASS III GENES DETAIL")
    print(f"{'='*72}")

    c3_genes = class_genes.get("III", [])
    print(f"\n{'Gene':12s} {'Bench14':>8s} {'ST_HVG':>8s} {'ST_DE20':>8s}")
    print("-" * 42)
    for g in sorted(c3_genes):
        bench_r = np.mean([blind_scores[m].get(g, np.nan) for m in methods_14])
        hvg_r = state_hvg.get(g, np.nan)
        de20_r = state_de20.get(g, np.nan)
        print(f"{g:12s} {bench_r:8.4f} {hvg_r:8.4f} {de20_r:8.4f}")

if __name__ == "__main__":
    main()
