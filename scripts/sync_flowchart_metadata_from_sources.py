#!/usr/bin/env python3
"""
Synchronize GLMP metadata indexes from canonical process JSON files.

This repairs metadata drift caused by earlier integration scripts that projected only
legacy template keys (notably hardcoding `complexity: "low"` for added charts).

Canonical source: glmp-v2/processes/**/*.json
Patched indexes:
  - glmp-v2/metadata.json
  - glmp-v2/data/metadata.json
  - glmp-v2/viewer/metadata.json
"""

import glob
import json
from collections import Counter
from pathlib import Path

META_FILES = [
    "glmp-v2/metadata.json",
    "glmp-v2/data/metadata.json",
    "glmp-v2/viewer/metadata.json",
]


def load_sources():
    sources = {}
    for path in sorted(glob.glob("glmp-v2/processes/**/*.json", recursive=True)):
        proc = json.load(open(path))
        sources[proc["id"]] = proc
    return sources


def complexity_value(proc):
    complexity = proc.get("complexity", "unknown")
    if isinstance(complexity, dict):
        return complexity.get("detailLevel") or "unknown"
    return complexity or "unknown"


def logic_gates_for(existing, source):
    lg = source.get("logicGates") or {}
    out = {"or": lg.get("or", 0), "and": lg.get("and", 0)}
    if isinstance(existing, dict) and "total" in existing:
        out["total"] = out["or"] + out["and"]
    if not isinstance(existing, dict) or "not" in existing:
        out["not"] = lg.get("not", 0)
    return out


def sync_entry(entry, source):
    entry["name"] = source.get("name", entry.get("name"))
    entry["organism"] = source.get("organism", entry.get("organism"))
    entry["category"] = source.get("category", entry.get("category"))
    entry["description"] = source.get("description", entry.get("description"))
    entry["verified"] = source.get("verified", entry.get("verified"))
    entry["created"] = source.get("created", entry.get("created"))
    entry["lastUpdated"] = source.get("lastUpdated", entry.get("lastUpdated"))
    entry["citations"] = len(source.get("sources", []))
    entry["complexity"] = complexity_value(source)
    entry["nodes"] = source.get("totalNodes", source.get("nodes", entry.get("nodes", 0)))
    if "totalNodes" in entry:
        entry["totalNodes"] = entry["nodes"]
    entry["conditionals"] = source.get("conditionals", entry.get("conditionals", 0))
    entry["logicGates"] = logic_gates_for(entry.get("logicGates"), source)
    entry["notGates"] = source.get("notGates", entry.get("notGates", 0))
    entry["loops"] = source.get("loops", entry.get("loops", 0))
    entry["circuitClass"] = source.get("circuitClass", entry.get("circuitClass"))
    if "circuitClassName" in source:
        entry["circuitClassName"] = source["circuitClassName"]
    entry["topologyType"] = source.get("topologyType", entry.get("topologyType"))
    entry["circuitClassConfidence"] = source.get(
        "circuitClassConfidence", entry.get("circuitClassConfidence")
    )
    if "circuitClassNeedsReview" in source:
        entry["circuitClassNeedsReview"] = source["circuitClassNeedsReview"]
    return entry


def g(entry, *keys):
    for key in keys:
        if key in entry and entry[key] is not None:
            return entry[key]
    return 0


def recompute(data):
    procs = data["processes"]
    stats = data.get("statistics", {})
    if stats is not None:
        or_g = sum((p.get("logicGates") or {}).get("or", 0) for p in procs)
        and_g = sum((p.get("logicGates") or {}).get("and", 0) for p in procs)
        not_g = sum(g(p, "notGates") for p in procs)
        dist = Counter(p.get("circuitClass") for p in procs if p.get("circuitClass"))
        stats["totalNodes"] = sum(g(p, "nodes", "totalNodes") for p in procs)
        stats["totalConditionals"] = sum(g(p, "conditionals") for p in procs)
        stats["orGates"] = or_g
        stats["andGates"] = and_g
        stats["notGates"] = not_g
        stats["totalLogicGates"] = or_g + and_g + not_g
        stats["loops"] = sum(g(p, "loops") for p in procs)
        stats["verifiedProcesses"] = sum(1 for p in procs if p.get("verified"))
        stats["circuitClassDistribution"] = {
            key: dist[key] for key in ["I", "II", "III", "IV", "V"] if dist.get(key)
        }
        data["statistics"] = stats
    data["totalProcesses"] = len(procs)

    if "organisms" in data:
        counts = Counter(p.get("organism", "Unknown") for p in procs)
        data["organisms"] = [{"name": name, "processCount": count} for name, count in sorted(counts.items())]
    if "categories" in data:
        counts = Counter(p.get("category", "Unknown") for p in procs)
        data["categories"] = [{"name": name, "processCount": count} for name, count in sorted(counts.items())]
    return data


def patch_metadata(path, sources):
    data = json.load(open(path))
    missing_sources = []
    for entry in data["processes"]:
        source = sources.get(entry.get("id"))
        if source is None:
            missing_sources.append(entry.get("id"))
            continue
        sync_entry(entry, source)
    recompute(data)
    with open(path, "w") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return missing_sources, data["totalProcesses"], data.get("statistics", {}).get("circuitClassDistribution")


def main():
    sources = load_sources()
    print(f"Loaded {len(sources)} canonical process JSONs")
    for path in META_FILES:
        if not Path(path).exists():
            print(f"  SKIP missing {path}")
            continue
        missing, total, dist = patch_metadata(path, sources)
        msg = f"  {path}: synced {total} entries; class dist {dist}"
        if missing:
            msg += f"; {len(missing)} entries missing source JSON"
        print(msg)


if __name__ == "__main__":
    main()
