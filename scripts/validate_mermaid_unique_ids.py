#!/usr/bin/env python3
"""
Validate Mermaid node ID uniqueness within each process.

Why: If the same node ID is reused with different labels/shapes, Mermaid merges the node,
which can produce confusing visuals and seemingly "wrong" colors/styles.

This script flags:
- Same node ID declared with multiple different label texts
- Same node ID declared with multiple different shape types ([], (), {}, (()), etc.)

Usage:
  python3 scripts/validate_mermaid_unique_ids.py --dir /home/gdubs/glmp/glmp-v2/processes
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple


@dataclass(frozen=True)
class NodeDecl:
    shape: str
    label: str
    line: str


# Capture node declarations like:
#   A[Label]
#   B(Label)
#   C{Question?}
#   D((Circle))
#   E([Stadium])
#
# We intentionally ignore edges without explicit labels.
NODE_DECL_RE = re.compile(
    r"(?P<id>[A-Za-z0-9_.-]+)\s*(?P<open>\(\(|\(\[|\[|\(|\{)\s*(?P<label>.*?)\s*(?P<close>\]\)|\)\)|\]|\)|\})"
)


def normalize_shape(open_tok: str, close_tok: str) -> str:
    return f"{open_tok}{close_tok}"


def extract_declarations(mermaid: str) -> Dict[str, List[NodeDecl]]:
    decls: Dict[str, List[NodeDecl]] = {}
    for raw_line in mermaid.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("%%"):
            continue
        if line.startswith("style "):
            continue
        for m in NODE_DECL_RE.finditer(line):
            nid = m.group("id")
            shape = normalize_shape(m.group("open"), m.group("close"))
            label = m.group("label").strip()
            decls.setdefault(nid, []).append(NodeDecl(shape=shape, label=label, line=raw_line))
    return decls


def find_conflicts(decls: Dict[str, List[NodeDecl]]) -> Dict[str, Dict[str, Set[str]]]:
    conflicts: Dict[str, Dict[str, Set[str]]] = {}
    for nid, lst in decls.items():
        shapes = {d.shape for d in lst}
        labels = {d.label for d in lst if d.label}
        # Only flag if there are multiple distinct labels or shapes
        if len(labels) > 1 or len(shapes) > 1:
            conflicts[nid] = {
                "shapes": shapes,
                "labels": labels,
            }
    return conflicts


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--limit", type=int, default=50, help="Max conflicts to print.")
    args = ap.parse_args()

    base = Path(args.dir).resolve()
    if not base.exists():
        raise SystemExit(f"Not found: {base}")

    total_files = 0
    files_with_conflicts = 0
    printed = 0

    for jf in sorted(base.rglob("*.json")):
        obj = json.loads(jf.read_text(encoding="utf-8"))
        mermaid = obj.get("mermaid")
        if not isinstance(mermaid, str) or not mermaid.strip():
            continue
        total_files += 1

        decls = extract_declarations(mermaid)
        conflicts = find_conflicts(decls)
        if not conflicts:
            continue

        files_with_conflicts += 1
        if printed < args.limit:
            print(f"\n=== {jf} ===")
            # Print up to a few node IDs per file
            for nid, info in list(conflicts.items())[:10]:
                print(f"- {nid}: shapes={sorted(info['shapes'])} labels={sorted(info['labels'])[:4]}")
            printed += 1

    print(f"\nScanned process files: {total_files}")
    print(f"Files with ID conflicts: {files_with_conflicts}")


if __name__ == "__main__":
    main()

