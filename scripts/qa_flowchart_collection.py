#!/usr/bin/env python3
"""
QA report for the GLMP flowchart collection.

This script is intentionally conservative: it reports contradictions and likely review
targets, but it does not modify files. Use it before expanding the collection or before
promoting sequence annotations to training data.
"""

import glob
import json
from collections import Counter

META_FILES = [
    "glmp-v2/metadata.json",
    "glmp-v2/data/metadata.json",
    "glmp-v2/viewer/metadata.json",
]


def load_sources():
    rows = []
    for path in sorted(glob.glob("glmp-v2/processes/**/*.json", recursive=True)):
        proc = json.load(open(path))
        rows.append((path, proc))
    return rows


def complexity_value(proc):
    complexity = proc.get("complexity", "unknown")
    if isinstance(complexity, dict):
        return complexity.get("detailLevel") or "unknown"
    return complexity or "unknown"


def main():
    rows = load_sources()
    print(f"Source process JSONs: {len(rows)}")
    classes = Counter()
    organisms = Counter()
    missing_required = []
    class_loop_zero = []
    missing_sequence = []
    needs_review = []
    complexity = Counter()

    required = [
        "id",
        "name",
        "organism",
        "mermaid",
        "circuitClass",
        "topologyType",
        "totalNodes",
        "conditionals",
        "logicGates",
        "notGates",
        "loops",
    ]

    for path, proc in rows:
        pid = proc.get("id", path)
        classes[proc.get("circuitClass")] += 1
        organisms[proc.get("organism")] += 1
        complexity[complexity_value(proc)] += 1
        for key in required:
            if key not in proc:
                missing_required.append((pid, key))
        loops = proc.get("loops", 0) or 0
        circuit_class = proc.get("circuitClass")
        if circuit_class in ("II", "III", "IV") and loops == 0:
            class_loop_zero.append(
                (
                    pid,
                    circuit_class,
                    proc.get("topologyType"),
                    bool(proc.get("groundTruth")),
                    proc.get("circuitClassNeedsReview", False),
                )
            )
        if not proc.get("sequenceAnnotation"):
            missing_sequence.append(pid)
        if proc.get("circuitClassNeedsReview"):
            needs_review.append(pid)

    print("Class distribution:", dict(classes))
    print("Organisms:", dict(organisms))
    print("Source complexity levels:", dict(complexity))
    print(f"Missing required fields: {len(missing_required)}")
    for pid, key in missing_required[:50]:
        print(f"  MISSING {pid}: {key}")
    print(f"Missing sequenceAnnotation: {len(missing_sequence)}")
    print(f"Explicit circuitClassNeedsReview: {len(needs_review)}")
    for pid in needs_review[:50]:
        print(f"  NEEDS_REVIEW {pid}")

    print(f"Class II/III/IV with loops == 0: {len(class_loop_zero)}")
    for pid, circuit_class, topology, ground_truth, review in class_loop_zero:
        status = "needs_review" if review else "unreviewed"
        gt = "ground_truth" if ground_truth else "heuristic"
        print(f"  CLASS_LOOP_ZERO {pid}: class={circuit_class} topology={topology} {gt} {status}")

    source_by_id = {proc["id"]: proc for _, proc in rows}
    for path in META_FILES:
        data = json.load(open(path))
        procs = data["processes"]
        ids = [p.get("id") for p in procs]
        duplicate_ids = sorted({pid for pid in ids if ids.count(pid) > 1})
        missing_source = [pid for pid in ids if pid not in source_by_id]
        missing_loops = [pid for pid, p in zip(ids, procs) if "loops" not in p]
        bad_complexity = [
            pid
            for pid, p in zip(ids, procs)
            if pid in source_by_id and p.get("complexity") != complexity_value(source_by_id[pid])
        ]
        print(f"\nMetadata: {path}")
        print(f"  totalProcesses={data.get('totalProcesses')} entries={len(procs)}")
        print(f"  stats.classDist={data.get('statistics', {}).get('circuitClassDistribution')}")
        print(f"  stats.loops={data.get('statistics', {}).get('loops')}")
        print(f"  duplicate ids={len(duplicate_ids)}")
        print(f"  entries missing source JSON={len(missing_source)}")
        print(f"  entries missing loops field={len(missing_loops)}")
        print(f"  complexity drift vs source={len(bad_complexity)}")
        for pid in bad_complexity[:30]:
            print(
                f"    COMPLEXITY_DRIFT {pid}: "
                f"metadata={next(p for p in procs if p.get('id') == pid).get('complexity')} "
                f"source={complexity_value(source_by_id[pid])}"
            )


if __name__ == "__main__":
    main()
