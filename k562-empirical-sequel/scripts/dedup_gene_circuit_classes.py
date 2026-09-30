#!/usr/bin/env python3
"""
Deduplicate gene_circuit_classes.tsv when the same HGNC symbol appears under multiple
circuit_class rows (e.g. TRRUST_topology Class I + literature Class III).

Scientific intent (GLMP / rBio cohorts):
  Prefer the annotation that reflects curated feedback / bistability (high-tier classes
  supported by literature) over TRRUST-derived feed-forward topology rows for the same gene.

Ranking:
  1) circuit_class tier: III > II > IV > V > I
  2) confidence: high > medium > low
  3) evidence_source contains 'literature' (case-insensitive) over other sources

Usage (from repo root):
  python3 k562-empirical-sequel/scripts/dedup_gene_circuit_classes.py
  python3 k562-empirical-sequel/scripts/dedup_gene_circuit_classes.py --dry-run
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import pandas as pd

TIER = {"III": 5, "II": 4, "IV": 3, "V": 2, "I": 1}
CONF = {"high": 3, "medium": 2, "low": 1}


def deduplicate(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    c = df.copy()
    c["_tier"] = c["circuit_class"].map(TIER).fillna(0).astype(int)
    c["_conf"] = c["confidence"].astype(str).str.lower().map(CONF).fillna(0).astype(int)
    c["_lit"] = (
        c["evidence_source"].fillna("").str.contains("literature", case=False).astype(int)
    )
    c = c.sort_values(
        ["gene", "_tier", "_conf", "_lit"],
        ascending=[True, False, False, False],
    )
    out = c.groupby("gene", as_index=False).first().drop(columns=["_tier", "_conf", "_lit"])
    n_dup = len(df) - len(out)
    return out, n_dup


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--input",
        type=Path,
        default=Path("gene_circuit_classes.tsv"),
        help="Input TSV (repo root)",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=Path("gene_circuit_classes.tsv"),
        help="Output TSV (default: overwrite input)",
    )
    p.add_argument(
        "--backup",
        type=Path,
        default=Path("gene_circuit_classes.before_dedup.tsv"),
        help="Copy of input before overwrite",
    )
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    df = pd.read_csv(args.input, sep="\t")
    before = len(df)
    out, n_collapsed = deduplicate(df)
    after = len(out)
    print(f"Rows: {before} -> {after} (collapsed {n_collapsed} duplicate rows)")
    print("Class counts:", out["circuit_class"].value_counts().to_dict())

    if args.dry_run:
        dups = df[df.duplicated(subset=["gene"], keep=False)].sort_values("gene")
        print(f"Genes with >1 row before dedup: {dups['gene'].nunique()}")
        print(dups.to_string(index=False))
        return

    if args.output.resolve() == args.input.resolve():
        shutil.copy2(args.input, args.backup)
        print(f"Backup written: {args.backup}")

    out.to_csv(args.output, sep="\t", index=False)
    print(f"Wrote: {args.output}")


if __name__ == "__main__":
    main()
