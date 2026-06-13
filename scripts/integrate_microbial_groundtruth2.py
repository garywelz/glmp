#!/usr/bin/env python3
"""
Index the Batch-2 ground-truth microbial circuits (build_microbial_groundtruth2.py) into the
metadata files. Same approach as integrate_microbial_groundtruth.py: these live in the
bacillus/ecoli dirs and share prefixes with the existing charts, so we key on an explicit id
set, then recompute totals / organisms / categories / circuitClassDistribution from the full
process list. Idempotent.

Patches: glmp-v2/metadata.json, glmp-v2/data/metadata.json, glmp-v2/viewer/metadata.json
"""

import json
from pathlib import Path

from integrate_microbial_groundtruth import patch_file as _patch_file
import integrate_microbial_groundtruth as base
import build_microbial_groundtruth2 as B

TARGET_IDS = [s["id"] for s in B.SPECS]
META_FILES = ["glmp-v2/metadata.json", "glmp-v2/data/metadata.json", "glmp-v2/viewer/metadata.json"]


def load_targets():
    procs = []
    for spec in B.SPECS:
        path = B.out_dir_for(spec["id"]) / f"{spec['id']}.json"
        procs.append(json.load(open(path)))
    return procs


def main():
    base.TARGET_IDS = TARGET_IDS
    targets = load_targets()
    print(f"Indexing {len(targets)} Batch-2 ground-truth microbial circuits: {TARGET_IDS}")
    for path in META_FILES:
        if not Path(path).exists():
            print(f"  SKIP (missing): {path}")
            continue
        removed, added, total, dist = _patch_file(path, targets)
        print(f"  {path}: -{removed} stale, +{added} -> {total} total; class dist {dist}")


if __name__ == "__main__":
    main()
