#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


BRACKET_TOKEN_PATTERN = re.compile(r"\[([0-9A-Za-z+\-.]{1,12})\]")
DOUBLE_CURLY_OPEN = re.compile(r"\{\{")
DOUBLE_CURLY_CLOSE = re.compile(r"\}\}")


def sanitize_mermaid_string(mermaid: str) -> str:
    sanitized = BRACKET_TOKEN_PATTERN.sub(r"(\\1)", mermaid)
    # Mermaid flowcharts use single { } for diamonds; double {{ }} is invalid and triggers parser errors.
    sanitized = DOUBLE_CURLY_OPEN.sub("{", sanitized)
    sanitized = DOUBLE_CURLY_CLOSE.sub("}", sanitized)
    return sanitized


def process_json_file(json_path: Path, write_changes: bool) -> bool:
    try:
        with json_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: Could not read JSON {json_path}: {e}", file=sys.stderr)
        return False

    mermaid = data.get("mermaid", "")
    if not isinstance(mermaid, str):
        return False

    sanitized = sanitize_mermaid_string(mermaid)
    if sanitized == mermaid:
        return False

    if write_changes:
        data["mermaid"] = sanitized
        try:
            with json_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"ERROR: Could not write JSON {json_path}: {e}", file=sys.stderr)
            return False

    return True


def find_json_files(root: Path) -> list[Path]:
    candidates = []
    for pattern in [
        "processes_with_not_gates/**/*.json",
        "processes/**/*.json",
    ]:
        candidates.extend(root.glob(pattern))
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for p in candidates:
        if p not in seen and p.is_file():
            seen.add(p)
            unique.append(p)
    return unique


def main() -> int:
    parser = argparse.ArgumentParser(description="Sanitize Mermaid strings by replacing short bracketed tokens [..] with (..)")
    parser.add_argument("--root", default=".", help="Project root to search (default: current directory)")
    parser.add_argument("--write", action="store_true", help="Write changes to files (otherwise dry run)")
    parser.add_argument("--limit", type=int, default=0, help="Optional limit on number of files to process")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    json_files = find_json_files(root)

    changed = []
    checked_count = 0
    for jf in json_files:
        if args.limit and len(changed) >= args.limit:
            break
        did_change = process_json_file(jf, write_changes=args.write)
        checked_count += 1
        if did_change:
            changed.append(jf)

    if changed:
        print("Sanitized files:")
        for p in changed:
            print(f" - {p}")
    else:
        print("No changes needed.")

    print(f"Checked: {checked_count} files. Changed: {len(changed)} files.")

    # Exit code: 0 if no changes needed, 2 if changes were made in dry-run, 0 if written
    if changed and not args.write:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())



