#!/usr/bin/env python3
"""
Index the ground-truth microbial/phage circuits (build_microbial_groundtruth.py) into the
metadata files. Unlike the synthetic/human integrator, these live in the yeast/ecoli dirs
and share prefixes with the existing 108 charts, so we key on an explicit id set rather
than a prefix. Idempotent: removes any existing entries for these ids, re-adds from the
JSONs, and recomputes totals / organisms / categories / circuitClassDistribution from the
full process list.

Patches: glmp-v2/metadata.json, glmp-v2/data/metadata.json, glmp-v2/viewer/metadata.json
"""

import json
from collections import Counter
from pathlib import Path

from integrate_synthetic_batch1 import build_entry, logicgates_for

import build_microbial_groundtruth as B

TARGET_IDS = [s["id"] for s in B.SPECS]
META_FILES = ["glmp-v2/metadata.json", "glmp-v2/data/metadata.json", "glmp-v2/viewer/metadata.json"]


def load_targets():
    procs = []
    for spec in B.SPECS:
        path = B.out_dir_for(spec["id"]) / f"{spec['id']}.json"
        procs.append(json.load(open(path)))
    return procs


def g(p, *keys, default=0):
    for k in keys:
        if k in p and p[k] is not None:
            return p[k]
    return default


def patch_file(path, targets):
    data = json.load(open(path))
    procs = data["processes"]

    before = len(procs)
    procs = [p for p in procs if p.get("id") not in set(TARGET_IDS)]
    removed = before - len(procs)

    template_keys = list(data["processes"][0].keys())
    sample_lg = data["processes"][0].get("logicGates", {"or": 0, "and": 0})
    for proc in targets:
        e = build_entry(template_keys, proc)
        if "logicGates" in template_keys:
            e["logicGates"] = logicgates_for(sample_lg, proc["logicGates"])
        procs.append(e)
    data["processes"] = procs
    data["totalProcesses"] = len(procs)

    tot_nodes = sum(g(p, "nodes", "totalNodes") for p in procs)
    tot_cond = sum(g(p, "conditionals") for p in procs)
    or_g = sum((p.get("logicGates") or {}).get("or", 0) for p in procs)
    and_g = sum((p.get("logicGates") or {}).get("and", 0) for p in procs)
    not_g = sum(g(p, "notGates") for p in procs)
    verified_total = sum(1 for p in procs if p.get("verified"))
    dist = Counter(p.get("circuitClass") for p in procs if p.get("circuitClass"))

    st = data.get("statistics", {})
    if st:
        st["totalNodes"] = tot_nodes
        st["totalConditionals"] = tot_cond
        st["orGates"] = or_g
        st["andGates"] = and_g
        st["notGates"] = not_g
        st["totalLogicGates"] = or_g + and_g + not_g
        st["verifiedProcesses"] = verified_total
        st["circuitClassDistribution"] = {k: dist[k] for k in ["I", "II", "III", "IV", "V"] if dist.get(k)}
        data["statistics"] = st

    if "organisms" in data:
        org_counts = Counter(p.get("organism", "Unknown") for p in procs)
        for item in data["organisms"]:
            if item.get("name") in org_counts:
                item["processCount"] = org_counts[item["name"]]
        existing = {item.get("name") for item in data["organisms"]}
        for name, c in org_counts.items():
            if name not in existing:
                data["organisms"].append({"name": name, "processCount": c})
    if "categories" in data:
        cat_counts = Counter(p.get("category", "Unknown") for p in procs)
        for item in data["categories"]:
            if item.get("name") in cat_counts:
                item["processCount"] = cat_counts[item["name"]]
        existing = {item.get("name") for item in data["categories"]}
        for name, c in cat_counts.items():
            if name not in existing:
                data["categories"].append({"name": name, "processCount": c})

    with open(path, "w") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return removed, len(targets), data["totalProcesses"], st.get("circuitClassDistribution")


def main():
    targets = load_targets()
    print(f"Indexing {len(targets)} ground-truth microbial/phage circuits: {TARGET_IDS}")
    for path in META_FILES:
        if not Path(path).exists():
            print(f"  SKIP (missing): {path}")
            continue
        removed, added, total, dist = patch_file(path, targets)
        print(f"  {path}: -{removed} stale, +{added} -> {total} total; class dist {dist}")


if __name__ == "__main__":
    main()
