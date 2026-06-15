#!/usr/bin/env python3
"""
Sync metadata process entries from authoritative glmp-v2/processes/**/*.json sources.

Updates per-process fields (nodes, conditionals, loops, complexity, logicGates, …)
and recomputes collection statistics in all metadata indexes.

Run after trim_dense_legacy_charts.py or compute_regulatory_cycles.py.
"""

from __future__ import annotations

import glob
import json
from collections import Counter
from pathlib import Path

META_FILES = [
    "glmp-v2/metadata.json",
    "glmp-v2/data/metadata.json",
    "glmp-v2/viewer/metadata.json",
]
SRC_GLOB = "glmp-v2/processes/**/*.json"

DETAIL_MAP = {
    "ground-truth": "low",
    "curated": "low",
    "regulatory_core": "low",
    "topology_schematic": "low",
    "detailed": "detailed",
    "maximum": "maximum",
}


def load_sources() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for f in glob.glob(SRC_GLOB, recursive=True):
        p = json.load(open(f, encoding="utf-8"))
        out[p["id"]] = p
    return out


def complexity_label(proc: dict) -> str:
    detail = proc.get("complexity", {}).get("detailLevel", "")
    return DETAIL_MAP.get(detail, detail or "unknown")


def patch_logic_gates(entry_lg: dict | None, proc_lg: dict) -> dict:
    lg = proc_lg or {}
    out = {"or": lg.get("or", 0), "and": lg.get("and", 0)}
    if entry_lg and "total" in entry_lg:
        out["total"] = out["or"] + out["and"]
    if entry_lg and "not" in entry_lg:
        out["not"] = lg.get("not", 0)
    return out


def sync_file(path: str, sources: dict[str, dict]) -> None:
    data = json.load(open(path, encoding="utf-8"))
    procs = data["processes"]
    missing = []
    totals = Counter()

    for entry in procs:
        pid = entry.get("id")
        if pid not in sources:
            missing.append(pid)
            continue
        p = sources[pid]
        nodes = p.get("totalNodes", p.get("complexity", {}).get("nodes", 0))
        lg = p.get("logicGates", {})

        entry["nodes"] = nodes
        if "totalNodes" in entry:
            entry["totalNodes"] = nodes
        entry["conditionals"] = p.get("conditionals", 0)
        entry["loops"] = p.get("loops", 0)
        entry["feedbackEdges"] = p.get("feedbackEdges", 0)
        entry["complexity"] = complexity_label(p)
        entry["notGates"] = p.get("notGates", lg.get("not", 0))
        entry["lastUpdated"] = p.get("lastUpdated", entry.get("lastUpdated"))
        if entry.get("logicGates") is not None:
            entry["logicGates"] = patch_logic_gates(entry.get("logicGates"), lg)

        totals["nodes"] += nodes
        totals["conditionals"] += entry["conditionals"]
        totals["loops"] += entry["loops"]
        totals["or"] += lg.get("or", 0)
        totals["and"] += lg.get("and", 0)
        totals["not"] += lg.get("not", 0)

    st = data.setdefault("statistics", {})
    st["totalNodes"] = totals["nodes"]
    st["totalConditionals"] = totals["conditionals"]
    st["loops"] = totals["loops"]
    st["totalOR"] = totals["or"]
    st["totalAND"] = totals["and"]
    st["totalNOT"] = totals["not"]
    st["totalGates"] = totals["or"] + totals["and"] + totals["not"]

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print(f"  {path}: synced {len(procs)} entries; nodes={totals['nodes']}, loops={totals['loops']}"
          + (f"; missing {len(missing)}" if missing else ""))


def main() -> None:
    sources = load_sources()
    print(f"Loaded {len(sources)} source processes")
    for path in META_FILES:
        if Path(path).exists():
            sync_file(path, sources)
        else:
            print(f"  SKIP (missing): {path}")


if __name__ == "__main__":
    main()
