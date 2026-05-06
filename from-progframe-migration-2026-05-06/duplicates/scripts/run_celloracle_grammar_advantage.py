#!/usr/bin/env python3
"""
Path 3A: CellOracle vs grammar-blind mean (14 methods) on the TF subset.

For each gene scored by CellOracle, compute grammar_advantage =
  CellOracle_r - mean(pearson_r over 14 benchmark methods for that gene).

Outputs:
  - results/celloracle_grammar_advantage.tsv
  - results/celloracle_grammar_advantage_summary.txt
"""
import csv
from collections import defaultdict
from pathlib import Path

import numpy as np

RESULTS = Path("results")
MERGED = RESULTS / "merged_scores.tsv"
CELLO = RESULTS / "celloracle_k562_per_gene_scores.tsv"
CLASSES = Path("gene_circuit_classes.tsv")
OUT_TSV = RESULTS / "celloracle_grammar_advantage.tsv"
OUT_TXT = RESULTS / "celloracle_grammar_advantage_summary.txt"


def main():
    blind = defaultdict(dict)
    with open(MERGED) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            blind[row["method"]][row["gene"]] = float(row["pearson_correlation"])
    methods = sorted(blind.keys())
    if len(methods) != 14:
        print(f"Warning: expected 14 benchmark methods, found {len(methods)}")

    celloracle = {}
    with open(CELLO) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            celloracle[row["gene"]] = float(row["pearson_correlation"])

    classes = {}
    with open(CLASSES) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            classes[row["gene"]] = row["circuit_class"]

    bench_genes = set.intersection(*(set(blind[m].keys()) for m in methods))

    rows_out = []
    for gene, co_r in sorted(celloracle.items()):
        if gene not in classes:
            continue
        vals = [blind[m][gene] for m in methods if gene in blind[m]]
        in_bench = gene in bench_genes and len(vals) == len(methods)
        if not in_bench:
            blind_mean = float(np.mean(vals)) if vals else float("nan")
            adv = (co_r - blind_mean) if vals else float("nan")
        else:
            blind_mean = float(np.mean(vals))
            adv = co_r - blind_mean
        rows_out.append({
            "gene": gene,
            "circuit_class": classes[gene],
            "in_benchmark_780": "yes" if in_bench else "no",
            "celloracle_r": round(co_r, 6),
            "grammar_blind_mean_r": round(blind_mean, 6) if vals else "",
            "grammar_advantage": round(adv, 6) if vals else "",
            "n_blind_methods": len(vals),
        })

    OUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_TSV, "w", newline="") as f:
        w = csv.DictWriter(
            f,
            delimiter="\t",
            fieldnames=[
                "gene", "circuit_class", "in_benchmark_780", "celloracle_r",
                "grammar_blind_mean_r", "grammar_advantage", "n_blind_methods",
            ],
        )
        w.writeheader()
        w.writerows(rows_out)

    lines = []
    lines.append("CellOracle vs 14-method grammar-blind mean (K562 essential screen)")
    lines.append(f"N CellOracle TFs (all): {len(rows_out)}")
    bench_rows = [r for r in rows_out if r["in_benchmark_780"] == "yes"]
    lines.append(f"N in benchmark 780 ∩ all 14 methods: {len(bench_rows)}")
    lines.append("")
    by_class = defaultdict(list)
    for r in bench_rows:
        by_class[r["circuit_class"]].append(float(r["grammar_advantage"]))
    lines.append("Mean grammar advantage (CellOracle - blind mean) by class:")
    for cls in ["I", "II", "III", "IV", "V"]:
        if cls not in by_class:
            continue
        v = by_class[cls]
        lines.append(f"  Class {cls}: N={len(v):2d}, mean adv={np.mean(v):+.4f}, median={np.median(v):+.4f}")
    myc = next((r for r in rows_out if r["gene"] == "MYC"), None)
    if myc:
        lines.append("")
        lines.append(
            f"MYC (Class {myc['circuit_class']}): CellOracle r={myc['celloracle_r']}, "
            f"blind mean={myc['grammar_blind_mean_r']}, advantage={myc['grammar_advantage']}"
        )
    txt = "\n".join(lines) + "\n"
    OUT_TXT.write_text(txt)
    print(txt)
    print(f"Wrote {OUT_TSV} and {OUT_TXT}")


if __name__ == "__main__":
    main()
