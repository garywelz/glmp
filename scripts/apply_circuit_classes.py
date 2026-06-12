#!/usr/bin/env python3
"""
Apply circuit-class assignments to the process JSONs and sync the metadata indexes.

Source of truth = the per-process JSON `circuitClass*` fields.
  - Microbial processes (108): (re)written here from classify_flowchart_circuits.classify()
    so the extended curated layer takes effect.
  - Ground-truth batches (synthetic_*, human_*): left untouched — their class is authored.

Then every metadata file's per-process class fields + circuitClassDistribution are
re-synced from the JSONs. Idempotent; safe to re-run.
"""

import glob
import json
from collections import Counter
from pathlib import Path

import classify_flowchart_circuits as C  # CURATED / classify() / CLASS_NAME

PROCESS_GLOB = "glmp-v2/processes/**/*.json"
META_FILES = ["glmp-v2/metadata.json", "glmp-v2/data/metadata.json", "glmp-v2/viewer/metadata.json"]


def is_ground_truth(proc):
    return bool(proc.get("groundTruth")) or str(proc.get("id", "")).startswith(("synthetic_", "human_"))


def update_process_jsons():
    files = sorted(glob.glob(PROCESS_GLOB, recursive=True))
    updated = 0
    for f in files:
        proc = json.load(open(f))
        if is_ground_truth(proc):
            continue
        cls, topo, rationale, source, confidence, needs_review = C.classify(proc)
        proc["circuitClass"] = cls
        proc["circuitClassName"] = C.CLASS_NAME[cls]
        proc["topologyType"] = topo
        proc["circuitClassConfidence"] = confidence
        proc["circuitClassNeedsReview"] = needs_review
        proc["circuitClassRationale"] = rationale
        proc["circuitClassEvidence"] = source
        with open(f, "w") as fh:
            json.dump(proc, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        updated += 1
    return updated, len(files)


def build_class_map():
    m = {}
    for f in sorted(glob.glob(PROCESS_GLOB, recursive=True)):
        proc = json.load(open(f))
        pid = proc.get("id")
        if not pid:
            continue
        m[pid] = {
            "circuitClass": proc.get("circuitClass"),
            "topologyType": proc.get("topologyType"),
            "circuitClassConfidence": proc.get("circuitClassConfidence"),
        }
    return m


def sync_metadata(path, class_map):
    data = json.load(open(path))
    procs = data.get("processes", [])
    missing = []
    for entry in procs:
        pid = entry.get("id")
        cm = class_map.get(pid)
        if not cm:
            missing.append(pid)
            continue
        entry["circuitClass"] = cm["circuitClass"]
        entry["topologyType"] = cm["topologyType"]
        entry["circuitClassConfidence"] = cm["circuitClassConfidence"]
    dist = Counter(e.get("circuitClass") for e in procs if e.get("circuitClass"))
    if "statistics" in data:
        data["statistics"]["circuitClassDistribution"] = {
            k: dist[k] for k in ["I", "II", "III", "IV", "V"] if dist.get(k)
        }
    with open(path, "w") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return len(procs), dict(dist), missing


def main():
    upd, total = update_process_jsons()
    print(f"Process JSONs: rewrote class fields on {upd}/{total} (ground-truth skipped)")
    class_map = build_class_map()
    for path in META_FILES:
        if not Path(path).exists():
            print(f"  SKIP (missing): {path}")
            continue
        n, dist, missing = sync_metadata(path, class_map)
        msg = f"  {path}: synced {n} entries; dist {dist}"
        if missing:
            msg += f"; WARNING unmapped ids: {missing[:5]}{'...' if len(missing) > 5 else ''}"
        print(msg)


if __name__ == "__main__":
    main()
