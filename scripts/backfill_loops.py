#!/usr/bin/env python3
"""
Backfill the `loops` statistic for the whole collection.

Loops = number of distinct nodes that have an edge pointing to an earlier-declared
node in the Mermaid source (feedback / back-edges) — the same definition used by
build_synthetic_batch1.compute_stats and shown in the database-table "Loops" column.

The 108 original microbial charts never stored `loops`, and the metadata entry
template lacks a `loops` key, so it was dropped for every process during integration.
This script (idempotent):
  1. recomputes `loops` from `mermaid` for every source process JSON and writes it,
  2. writes `loops` into every metadata process entry (matched by id),
  3. sets statistics.loops = sum across the collection,
in glmp-v2/metadata.json, glmp-v2/data/metadata.json, glmp-v2/viewer/metadata.json.
"""

import glob
import json
import re
from pathlib import Path

META_FILES = ["glmp-v2/metadata.json", "glmp-v2/data/metadata.json", "glmp-v2/viewer/metadata.json"]
SRC_GLOB = "glmp-v2/processes/**/*.json"

ARROW_RE = re.compile(r"\s*(?:<-->|<==>|x--x|o--o|-\.-+>|-\.-+|--+>|--+|==+>|==+|--[xo]|[ox]--)\s*")


def _strip_labels(line):
    """Remove edge labels |..| and node-shape brackets so only ids + arrows remain."""
    line = re.sub(r"\|[^|]*\|", " ", line)
    prev = None
    while prev != line:
        prev = line
        line = re.sub(r"\[\([^()\[\]]*\)\]", " ", line)   # [(db)]
        line = re.sub(r"\[\[[^\[\]]*\]\]", " ", line)     # [[subroutine]]
        line = re.sub(r"\(\([^()]*\)\)", " ", line)       # ((circle))
        line = re.sub(r"\{\{[^{}]*\}\}", " ", line)       # {{hexagon}}
        line = re.sub(r"\(\[[^()\[\]]*\]\)", " ", line)   # ([stadium])
        line = re.sub(r"\[[^\[\]]*\]", " ", line)         # [rect]
        line = re.sub(r"\([^()]*\)", " ", line)           # (round)
        line = re.sub(r"\{[^{}]*\}", " ", line)           # {diamond}
        line = re.sub(r">[^\]]*\]", " ", line)            # >asymmetric]
    return line


def count_loops(mermaid):
    if not mermaid:
        return 0
    order = {}
    edges = []
    for raw in mermaid.splitlines():
        s = raw.strip()
        if not s or s.startswith("%%"):
            continue
        low = s.split()[0].lower() if s.split() else ""
        if low in ("graph", "flowchart", "subgraph", "end", "style", "classdef",
                   "class", "linkstyle", "direction", "click"):
            continue
        cleaned = _strip_labels(s)
        if not ARROW_RE.search(cleaned):
            # node declaration line only — still register id order
            for tok in re.findall(r"[A-Za-z0-9_]+", cleaned):
                order.setdefault(tok, len(order))
            continue
        parts = ARROW_RE.split(cleaned)
        ids = []
        for part in parts:
            toks = re.findall(r"[A-Za-z0-9_]+", part)
            ids.append(toks[0] if toks else None)
        for nid in ids:
            if nid is not None:
                order.setdefault(nid, len(order))
        for a, b in zip(ids, ids[1:]):
            if a is not None and b is not None:
                edges.append((a, b))
    loop_sources = {a for a, b in edges if a in order and b in order and order[b] < order[a]}
    return len(loop_sources)


def backfill_sources():
    id_to_loops = {}
    changed = 0
    for f in sorted(glob.glob(SRC_GLOB, recursive=True)):
        p = json.load(open(f))
        loops = count_loops(p.get("mermaid", ""))
        id_to_loops[p.get("id")] = loops
        if p.get("loops") != loops:
            p["loops"] = loops
            with open(f, "w") as fh:
                json.dump(p, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
            changed += 1
    print(f"Source files: {len(id_to_loops)} scanned, {changed} updated; total loops {sum(id_to_loops.values())}")
    return id_to_loops


def patch_metadata(path, id_to_loops):
    data = json.load(open(path))
    procs = data["processes"]
    missing = []
    total = 0
    for p in procs:
        pid = p.get("id")
        if pid in id_to_loops:
            p["loops"] = id_to_loops[pid]
        else:
            p.setdefault("loops", count_loops(p.get("mermaid", "")))
            missing.append(pid)
        total += p.get("loops", 0) or 0
    st = data.get("statistics", {})
    if st is not None:
        st["loops"] = total
        data["statistics"] = st
    with open(path, "w") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"  {path}: loops set on {len(procs)} entries; statistics.loops={total}"
          + (f"; {len(missing)} not in source map" if missing else ""))


def main():
    id_to_loops = backfill_sources()
    for path in META_FILES:
        if Path(path).exists():
            patch_metadata(path, id_to_loops)
        else:
            print(f"  SKIP (missing): {path}")


if __name__ == "__main__":
    main()
