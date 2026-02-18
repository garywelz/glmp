#!/usr/bin/env python3
"""
Normalize over-quoted Mermaid node labels like ["\"text\""] -> ["text"]

This occurs when a prior quoting pass re-quoted already-quoted labels.
Safe to run multiple times (idempotent).
"""

import json
import re
import sys
from pathlib import Path


def normalize_overquoted(mermaid: str) -> str:
    # Replace patterns ["\"...\""] -> ["..."]
    pattern = re.compile(r"(\w+)\[\"\\\"([^\]]*?)\\\"\"\]")

    def repl(match: re.Match) -> str:
        node_id = match.group(1)
        label = match.group(2)
        return f'{node_id}["{label}"]'

    # Apply repeatedly until stable to handle rare nested cases
    previous = None
    current = mermaid
    while previous != current:
        previous = current
        current = pattern.sub(repl, current)
    return current


def fix_file(path: Path) -> bool:
    try:
        with path.open('r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return False

    mermaid = data.get('mermaid')
    if not isinstance(mermaid, str):
        return False

    fixed = normalize_overquoted(mermaid)
    if fixed == mermaid:
        return False

    data['mermaid'] = fixed
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return True


def main() -> int:
    root = Path('processes_with_not_gates')
    if not root.exists():
        print('❌ processes_with_not_gates not found')
        return 1

    total = 0
    changed = 0
    for p in sorted(root.rglob('*.json')):
        total += 1
        if fix_file(p):
            changed += 1
            print(f'✅ Normalized: {p}')

    print(f"\n📊 Dedupe summary: {changed}/{total} files normalized")
    return 0


if __name__ == '__main__':
    sys.exit(main())



