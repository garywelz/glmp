#!/usr/bin/env python3
"""
Convert GLMP process JSON files to the standardized 5-color legend.

This is a *mechanical* transformation:
- Updates each process `colorScheme` to the 5-color standard
- Rewrites Mermaid `style ... fill:...,color:...` lines to match the 5-color standard
- Collapses gate-specific colors (OR/AND/NOT) into the standard "blue" (intermediates & states)

Supported input schemes:
1) 7-color GLMP v2 (adds orange+lavender for OR/AND)
2) 8-color GLMP (green/amber/blue/cyan + yellow/purple/red gates + black outputs)

Usage:
  python3 scripts/convert_processes_to_5_color.py \
    --in-dir /home/gdubs/glmp/processes_with_not_gates \
    --out-dir /home/gdubs/glmp/glmp-v2/processes
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple


FIVE_COLOR_SCHEME = {
    "red": {
        "hex": "#ff6b6b",
        "category": "Triggers & Inputs",
        "description": "Environmental signals, nutrient availability, stress conditions",
    },
    "yellow": {
        "hex": "#ffd43b",
        "category": "Structures & Objects",
        "description": "Enzymes, receptor proteins, regulatory complexes",
    },
    "green": {
        "hex": "#51cf66",
        "category": "Processing & Operations",
        "description": "Metabolic reactions, signal transduction, gene expression",
    },
    "blue": {
        "hex": "#74c0fc",
        "category": "Intermediates & States",
        "description": "Metabolites, signaling molecules, regulatory states",
    },
    "violet": {
        "hex": "#b197fc",
        "category": "Products & Outputs",
        "description": "Biomolecules, cellular responses, system behaviors",
    },
}


def text_color_for_fill(fill_hex: str) -> str:
    """Choose a high-contrast text color for our standard palette."""
    fill = fill_hex.lower()
    if fill == FIVE_COLOR_SCHEME["yellow"]["hex"]:
        return "#000"
    return "#fff"


@dataclass(frozen=True)
class MapRule:
    new_fill: str
    new_text: Optional[str] = None


# Hex -> (new_fill, new_text)
# NOTE: This mapping is intentionally conservative and only rewrites known palette values.
HEX_MAP: Dict[str, MapRule] = {
    # --- Standard 5-color (keep) ---
    "#ff6b6b": MapRule(new_fill="#ff6b6b", new_text="#fff"),
    "#ffd43b": MapRule(new_fill="#ffd43b", new_text="#000"),
    "#51cf66": MapRule(new_fill="#51cf66", new_text="#fff"),
    "#74c0fc": MapRule(new_fill="#74c0fc", new_text="#fff"),
    "#b197fc": MapRule(new_fill="#b197fc", new_text="#fff"),

    # --- 7-color GLMP v2 extras (collapse to blue) ---
    "#ff9f43": MapRule(new_fill="#74c0fc", new_text="#fff"),  # OR gates -> blue
    "#b4b4dc": MapRule(new_fill="#74c0fc", new_text="#fff"),  # AND gates -> blue
    "#c3a6ff": MapRule(new_fill="#74c0fc", new_text="#fff"),  # AND gates alt -> blue

    # --- 8-color scheme used in processes_with_not_gates ---
    "#ffa726": MapRule(new_fill="#ffd43b", new_text="#000"),  # enzymes/proteins -> yellow
    "#42a5f5": MapRule(new_fill="#51cf66", new_text="#fff"),  # operations -> green
    "#b3e5fc": MapRule(new_fill="#74c0fc", new_text="#fff"),  # intermediates -> blue
    "#ffd600": MapRule(new_fill="#74c0fc", new_text="#fff"),  # OR -> blue
    "#7950f2": MapRule(new_fill="#74c0fc", new_text="#fff"),  # AND -> blue
    "#e74c3c": MapRule(new_fill="#74c0fc", new_text="#fff"),  # NOT -> blue
    "#000000": MapRule(new_fill="#b197fc", new_text="#fff"),  # final outcomes -> violet

    # NOTE: In the 8-color scheme, #51cf66 meant "Environmental Triggers"
    # We map it to standard red to regain the standard semantics.
    # But #51cf66 is also the standard "Processing" green in 5-color diagrams.
    #
    # We only apply this remap if we detect the 8-color scheme in the JSON's colorScheme keys.
}


STYLE_RE = re.compile(
    r"^(?P<prefix>\s*style\s+)(?P<id>[^\s]+)(?P<rest>\s+fill:(?P<fill>#[0-9a-fA-F]{6})\s*,\s*color:(?P<color>#[0-9a-fA-F]{3,6})\s*)$"
)


def detect_scheme(process: dict) -> str:
    scheme = process.get("colorScheme") or {}
    keys = set(scheme.keys())
    if {"green", "amber", "darkSkyBlue", "lightCyan", "yellow", "purple", "red", "black"} <= keys:
        return "eight_color"
    if {"red", "yellow", "green", "blue", "violet"} <= keys and ({"orange", "lavender"} & keys):
        return "seven_color"
    if {"red", "yellow", "green", "blue", "violet"} <= keys:
        return "five_color"
    return "unknown"


def rewrite_mermaid_styles(mermaid: str, scheme_type: str) -> Tuple[str, int]:
    changed = 0
    out_lines = []
    for line in mermaid.splitlines():
        m = STYLE_RE.match(line)
        if not m:
            out_lines.append(line)
            continue

        fill = m.group("fill").lower()
        txt = m.group("color").lower()

        # Special case: 8-color scheme uses #51cf66 as *triggers*; map it to standard red.
        if scheme_type == "eight_color" and fill == "#51cf66":
            new_fill = FIVE_COLOR_SCHEME["red"]["hex"]
            new_txt = text_color_for_fill(new_fill)
            out_lines.append(f"{m.group('prefix')}{m.group('id')} fill:{new_fill},color:{new_txt}")
            changed += 1
            continue

        rule = HEX_MAP.get(fill)
        if not rule:
            out_lines.append(line)
            continue

        new_fill = rule.new_fill
        new_txt = rule.new_text or text_color_for_fill(new_fill)

        if new_fill != fill or new_txt.lower() != txt:
            out_lines.append(f"{m.group('prefix')}{m.group('id')} fill:{new_fill},color:{new_txt}")
            changed += 1
        else:
            out_lines.append(line)

    return "\n".join(out_lines), changed


def convert_one(in_path: Path, out_path: Path) -> Tuple[bool, int]:
    raw = in_path.read_text(encoding="utf-8")
    process = json.loads(raw)

    scheme_type = detect_scheme(process)

    # Always set the standardized 5-color scheme
    process["colorScheme"] = FIVE_COLOR_SCHEME

    mermaid = process.get("mermaid")
    changed_styles = 0
    if isinstance(mermaid, str) and mermaid.strip():
        new_mermaid, changed_styles = rewrite_mermaid_styles(mermaid, scheme_type)
        process["mermaid"] = new_mermaid

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(process, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return True, changed_styles


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    in_dir = Path(args.in_dir).resolve()
    out_dir = Path(args.out_dir).resolve()

    if not in_dir.exists():
        raise SystemExit(f"Input dir not found: {in_dir}")

    json_paths = sorted([p for p in in_dir.rglob("*.json") if p.is_file()])
    if not json_paths:
        raise SystemExit(f"No .json files found under {in_dir}")

    total = 0
    total_style_changes = 0

    for p in json_paths:
        rel = p.relative_to(in_dir)
        out_path = out_dir / rel

        if args.dry_run:
            total += 1
            continue

        _, changed_styles = convert_one(p, out_path)
        total += 1
        total_style_changes += changed_styles

    print(f"Converted {total} process files")
    if not args.dry_run:
        print(f"Total Mermaid style lines rewritten: {total_style_changes}")
        print(f"Output directory: {out_dir}")


if __name__ == "__main__":
    main()

