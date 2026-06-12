#!/usr/bin/env python3
"""
Integrate the Batch 1 synthetic-biology processes into the GLMP metadata indexes.

Idempotent: strips any existing `synthetic_*` entries first, then re-adds from the
current process JSONs and re-derives the affected aggregate counters incrementally
(existing per-organism numbers are preserved exactly; only the synthetic deltas are
added). Run after scripts/build_synthetic_batch1.py.

Patches: glmp-v2/metadata.json, glmp-v2/data/metadata.json, glmp-v2/viewer/metadata.json
"""

import glob
import json
from collections import Counter
from pathlib import Path

EXTRA_GLOBS = ["glmp-v2/processes/synthetic/*.json", "glmp-v2/processes/human/*.json"]
EXTRA_PREFIXES = ("synthetic_", "human_")
META_FILES = ["glmp-v2/metadata.json", "glmp-v2/data/metadata.json", "glmp-v2/viewer/metadata.json"]


def load_synthetic():
    """Load all extra-batch process JSONs (synthetic ground-truth + human curated)."""
    procs = []
    for pattern in EXTRA_GLOBS:
        for f in sorted(glob.glob(pattern)):
            procs.append(json.load(open(f)))
    return procs


def build_entry(template_keys, proc):
    """Build a metadata process entry whose keys match an existing entry (template_keys)."""
    nodes = proc["totalNodes"]
    lg = proc["logicGates"]
    resolvers = {
        "id": proc["id"],
        "name": proc["name"],
        "organism": proc["organism"],
        "category": proc["category"],
        "description": proc["description"],
        "verified": proc["verified"],
        "created": proc["created"],
        "lastUpdated": proc["lastUpdated"],
        "generated": proc.get("created", ""),
        "citations": len(proc.get("sources", [])),
        "complexity": "low",
        "nodes": nodes,
        "totalNodes": nodes,
        "conditionals": proc["conditionals"],
        "notGates": proc["notGates"],
        "loops": proc["loops"],
        "circuitClass": proc["circuitClass"],
        "circuitClassName": proc["circuitClassName"],
        "topologyType": proc["topologyType"],
        "circuitClassConfidence": proc["circuitClassConfidence"],
    }
    entry = {}
    for k in template_keys:
        if k == "logicGates":
            entry[k] = None  # set by patch_file via logicgates_for() to match file shape
        elif k in resolvers:
            entry[k] = resolvers[k]
        else:
            entry[k] = None
    return entry


def logicgates_for(sample_lg, lg):
    out = {"or": lg["or"], "and": lg["and"]}
    if "total" in sample_lg:
        out["total"] = lg["or"] + lg["and"]
    if "not" in sample_lg:
        out["not"] = lg["not"]
    return out


def upsert_named_count(lst, name, delta):
    for item in lst:
        if item.get("name") == name:
            item["processCount"] = item.get("processCount", 0) + delta
            return
    lst.append({"name": name, "processCount": delta})


def patch_file(path, synth):
    data = json.load(open(path))
    procs = data["processes"]

    # 1. Remove any prior extra-batch entries (idempotency).
    before = len(procs)
    procs = [p for p in procs if not str(p.get("id", "")).startswith(EXTRA_PREFIXES)]
    removed = before - len(procs)

    # 2. Build entries matching this file's entry schema.
    template_keys = list(data["processes"][0].keys())
    sample_lg = data["processes"][0].get("logicGates", {"or": 0, "and": 0})
    new_entries = []
    for proc in synth:
        e = build_entry(template_keys, proc)
        if "logicGates" in template_keys:
            e["logicGates"] = logicgates_for(sample_lg, proc["logicGates"])
        new_entries.append(e)
    procs.extend(new_entries)
    data["processes"] = procs

    # 3. Counters: re-derive synthetic delta and re-baseline (remove old synth, add new).
    n = len(synth)
    sums = Counter()
    cls_dist = Counter()
    verified = 0
    for proc in synth:
        sums["totalNodes"] += proc["totalNodes"]
        sums["totalConditionals"] += proc["conditionals"]
        sums["orGates"] += proc["logicGates"]["or"]
        sums["andGates"] += proc["logicGates"]["and"]
        sums["notGates"] += proc["logicGates"]["not"]
        cls_dist[proc["circuitClass"]] += 1
        verified += 1 if proc["verified"] else 0

    # totalProcesses
    data["totalProcesses"] = len(procs)

    st = data.get("statistics", {})
    # Subtract any stale synthetic contribution is impossible to know precisely, so we
    # rebuild from the canonical 108 baseline by recomputing across non-synthetic + new.
    # Simpler & exact: recompute the whole-collection stats from the process entries.
    def g(p, *keys, default=0):
        for k in keys:
            if k in p and p[k] is not None:
                return p[k]
        return default
    tot_nodes = sum(g(p, "nodes", "totalNodes") for p in procs)
    tot_cond = sum(g(p, "conditionals") for p in procs)
    or_g = sum((p.get("logicGates") or {}).get("or", 0) for p in procs)
    and_g = sum((p.get("logicGates") or {}).get("and", 0) for p in procs)
    not_g = sum(g(p, "notGates") for p in procs)
    verified_total = sum(1 for p in procs if p.get("verified"))
    dist = Counter(p.get("circuitClass") for p in procs if p.get("circuitClass"))

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

    # organisms / categories (recompute counts from the full process list)
    if "organisms" in data:
        org_counts = Counter(p.get("organism", "Unknown") for p in procs)
        for item in data["organisms"]:
            if item.get("name") in org_counts:
                item["processCount"] = org_counts[item["name"]]
        existing_names = {item.get("name") for item in data["organisms"]}
        for name, c in org_counts.items():
            if name not in existing_names:
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
    return removed, n, data["totalProcesses"], st.get("circuitClassDistribution")


def main():
    synth = load_synthetic()
    print(f"Loaded {len(synth)} synthetic processes")
    for path in META_FILES:
        if not Path(path).exists():
            print(f"  SKIP (missing): {path}")
            continue
        removed, added, total, dist = patch_file(path, synth)
        print(f"  {path}: -{removed} stale, +{added} synthetic -> {total} total; class dist {dist}")


if __name__ == "__main__":
    main()
