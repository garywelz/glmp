#!/usr/bin/env python3
"""
Recompute paper-aligned `loops` (nodes on directed cycles) for the full collection.

Idempotent:
  1. updates every glmp-v2/processes/**/*.json,
  2. patches glmp-v2/metadata.json, glmp-v2/data/metadata.json, glmp-v2/viewer/metadata.json,
  3. sets statistics.loops = sum across collection.

Run:
  python3 scripts/compute_regulatory_cycles.py
  python3 scripts/compute_regulatory_cycles.py --report   # show legacy vs new for high deltas
"""

from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

from mermaid_graph import compute_regulatory_stats

META_FILES = [
    "glmp-v2/metadata.json",
    "glmp-v2/data/metadata.json",
    "glmp-v2/viewer/metadata.json",
]
SRC_GLOB = "glmp-v2/processes/**/*.json"


def backfill_sources(report: bool = False) -> dict[str, dict]:
    id_to_stats: dict[str, dict] = {}
    changed = 0
    deltas = []

    for f in sorted(glob.glob(SRC_GLOB, recursive=True)):
        p = json.load(open(f, encoding="utf-8"))
        stats = compute_regulatory_stats(p.get("mermaid", ""))
        pid = p.get("id")
        id_to_stats[pid] = stats

        old_loops = p.get("loops")
        new_loops = stats["loops"]
        if report and old_loops is not None and abs(old_loops - new_loops) >= 3:
            deltas.append((pid, old_loops, new_loops, stats["legacyLoops"]))

        updated = False
        for key in ("loops", "feedbackEdges", "totalNodes", "edges", "conditionals"):
            val = stats.get(key if key != "totalNodes" else "nodes")
            if p.get(key) != val:
                p[key] = val
                updated = True
        if updated:
            with open(f, "w", encoding="utf-8") as fh:
                json.dump(p, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
            changed += 1

    total_loops = sum(s["loops"] for s in id_to_stats.values())
    print(f"Source files: {len(id_to_stats)} scanned, {changed} updated; total loops={total_loops}")

    if report and deltas:
        deltas.sort(key=lambda x: -(x[1] - x[2]))
        print("\nLargest legacy→cycle reductions (pid, old, new, legacy_back_edge):")
        for row in deltas[:25]:
            print(f"  {row[0]}: {row[1]} → {row[2]}  (legacy back-edge={row[3]})")

    return id_to_stats


def patch_metadata(path: str, id_to_stats: dict[str, dict]) -> None:
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    for p in data["processes"]:
        pid = p.get("id")
        if pid in id_to_stats:
            st = id_to_stats[pid]
            p["loops"] = st["loops"]
            p["feedbackEdges"] = st["feedbackEdges"]
        total += p.get("loops", 0) or 0
    if data.get("statistics") is not None:
        data["statistics"]["loops"] = total
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"  {path}: loops={total}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", action="store_true", help="Print largest metric deltas")
    args = parser.parse_args()

    id_to_stats = backfill_sources(report=args.report)
    for path in META_FILES:
        if Path(path).exists():
            patch_metadata(path, id_to_stats)
        else:
            print(f"  SKIP (missing): {path}")


if __name__ == "__main__":
    main()
