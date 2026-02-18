#!/usr/bin/env python3
"""
Remove explicit Mermaid styling for *gate/decision* nodes so they render with defaults.

Important: We intentionally do NOT infer gate nodes from graph topology (in/out degree),
because merges/splits can appear in non-gate “process step” nodes. Instead, we unstyle
only nodes that are explicitly encoded as decision/gate nodes in Mermaid:

- Any node declared with diamond syntax: `ID{ ... }`
- Any node whose ID matches a gate naming convention like ANDGATE/ORGATE/NOTGATE

Result: gate nodes render with Mermaid defaults (typically white fill + black text/border),
while ordinary nodes keep their 5-color semantic styling.

This script edits the process JSON files in-place (updates `mermaid` only).

Usage:
  python3 scripts/unstyle_gate_nodes.py --dir /home/gdubs/glmp/glmp-v2/processes
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple


STYLE_LINE_RE = re.compile(
    r"^(?P<indent>\s*)style\s+(?P<id>[A-Za-z0-9_.-]+)\s+fill:(?P<fill>#[0-9a-fA-F]{6})\s*,\s*color:(?P<color>#[0-9a-fA-F]{3,6})\s*$"
)

ID_PREFIX_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+)")
DIAMOND_NODE_RE = re.compile(r"(^|[^A-Za-z0-9_.-])(?P<id>[A-Za-z0-9_.-]+)\{")
GATE_ID_RE = re.compile(r"^(ANDGATE|ORGATE|NOTGATE)\d*$", re.IGNORECASE)

def find_gate_nodes(mermaid: str) -> Set[str]:
    gates: Set[str] = set()
    for line in mermaid.splitlines():
        if "style " in line:
            continue
        for m in DIAMOND_NODE_RE.finditer(line):
            gates.add(m.group("id"))

    # Gate naming conventions (explicit gate nodes)
    for line in mermaid.splitlines():
        if "style " not in line:
            continue
        m = STYLE_LINE_RE.match(line)
        if m and GATE_ID_RE.match(m.group("id")):
            gates.add(m.group("id"))

    return gates


def remove_style_lines_for_nodes(mermaid: str, ids: Set[str]) -> Tuple[str, int]:
    out: List[str] = []
    removed = 0
    for line in mermaid.splitlines():
        m = STYLE_LINE_RE.match(line)
        if m and m.group("id") in ids:
            removed += 1
            continue
        out.append(line)
    return "\n".join(out), removed


def iter_json_files(base_dir: Path) -> Iterable[Path]:
    for p in sorted(base_dir.rglob("*.json")):
        if p.is_file():
            yield p


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="Directory containing process JSON files (recursive).")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    base = Path(args.dir).resolve()
    if not base.exists():
        raise SystemExit(f"Not found: {base}")

    total_files = 0
    total_removed = 0

    for jf in iter_json_files(base):
        raw = jf.read_text(encoding="utf-8")
        obj = json.loads(raw)
        mermaid = obj.get("mermaid")
        if not isinstance(mermaid, str) or not mermaid.strip():
            continue

        gate_ids = find_gate_nodes(mermaid)
        if not gate_ids:
            continue

        new_mermaid, removed = remove_style_lines_for_nodes(mermaid, gate_ids)
        if removed == 0:
            continue

        total_files += 1
        total_removed += removed

        if not args.dry_run:
            obj["mermaid"] = new_mermaid
            jf.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if args.dry_run:
        print(f"[dry-run] Would edit {total_files} files, removing {total_removed} style lines")
    else:
        print(f"Edited {total_files} files, removed {total_removed} style lines for gate nodes")


if __name__ == "__main__":
    main()

