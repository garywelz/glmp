#!/usr/bin/env python3
"""
Backfill the `loops` statistic for the whole collection.

Loops = distinct nodes on at least one directed cycle in the Mermaid graph
(Paper I / III definition). See scripts/mermaid_graph.py.

Idempotent:
  1. recomputes `loops` and `feedbackEdges` from `mermaid` for every process JSON,
  2. writes into metadata process entries,
  3. sets statistics.loops = sum across the collection.

Prefer scripts/compute_regulatory_cycles.py (same logic, includes --report).
"""

import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mermaid_graph import compute_regulatory_stats

META_FILES = ["glmp-v2/metadata.json", "glmp-v2/data/metadata.json", "glmp-v2/viewer/metadata.json"]
SRC_GLOB = "glmp-v2/processes/**/*.json"


def backfill_sources():
    id_to_stats = {}
    changed = 0
    for f in sorted(glob.glob(SRC_GLOB, recursive=True)):
        p = json.load(open(f, encoding="utf-8"))
        stats = compute_regulatory_stats(p.get("mermaid", ""))
        id_to_stats[p.get("id")] = stats
        updated = False
        for key, val in (
            ("loops", stats["loops"]),
            ("feedbackEdges", stats["feedbackEdges"]),
            ("totalNodes", stats["nodes"]),
            ("edges", stats["edges"]),
            ("conditionals", stats["conditionals"]),
        ):
            if p.get(key) != val:
                p[key] = val
                updated = True
        if updated:
            with open(f, "w", encoding="utf-8") as fh:
                json.dump(p, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
            changed += 1
    total = sum(s["loops"] for s in id_to_stats.values())
    print(f"Source files: {len(id_to_stats)} scanned, {changed} updated; total loops {total}")
    return id_to_stats


def patch_metadata(path, id_to_stats):
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
    print(f"  {path}: loops set on {len(data['processes'])} entries; statistics.loops={total}")


def main():
    id_to_stats = backfill_sources()
    for path in META_FILES:
        if Path(path).exists():
            patch_metadata(path, id_to_stats)
        else:
            print(f"  SKIP (missing): {path}")


if __name__ == "__main__":
    main()
