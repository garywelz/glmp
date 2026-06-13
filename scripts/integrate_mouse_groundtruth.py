#!/usr/bin/env python3
"""
Index the mouse ground-truth circuits (build_mouse_groundtruth.py) into the metadata files.
Same explicit-id approach as plant/developmental integrators. Idempotent.
Patches glmp-v2/metadata.json, glmp-v2/data/metadata.json, glmp-v2/viewer/metadata.json.
"""

import json
from pathlib import Path

from integrate_microbial_groundtruth import patch_file as _patch_file
import integrate_microbial_groundtruth as base
import build_mouse_groundtruth as B

TARGET_IDS = [s["id"] for s in B.SPECS]
META_FILES = ["glmp-v2/metadata.json", "glmp-v2/data/metadata.json", "glmp-v2/viewer/metadata.json"]


def load_targets():
    return [json.load(open(B.OUT_DIR / f"{s['id']}.json")) for s in B.SPECS]


def main():
    base.TARGET_IDS = TARGET_IDS
    targets = load_targets()
    print(f"Indexing {len(targets)} mouse ground-truth circuits: {TARGET_IDS}")
    for path in META_FILES:
        if not Path(path).exists():
            print(f"  SKIP (missing): {path}")
            continue
        removed, added, total, dist = _patch_file(path, targets)
        print(f"  {path}: -{removed} stale, +{added} -> {total} total; class dist {dist}")


if __name__ == "__main__":
    main()
