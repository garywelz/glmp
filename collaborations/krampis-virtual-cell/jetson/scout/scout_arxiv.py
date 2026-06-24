#!/usr/bin/env python3.8
"""Split scout worker: arXiv only."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scout_common import run_scout  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="CopernicusAI arXiv scout (split worker)")
    parser.add_argument("run_type", choices=["am", "pm"], help="Run slot label")
    parser.add_argument("--ingest", action="store_true", help="Run Firestore ingest after acquisition")
    parser.add_argument("--dry-run-status", action="store_true", help="Log only; no acquire")
    args = parser.parse_args()

    return run_scout(
        "arxiv",
        args.run_type,
        with_glmp_queries=False,
        with_ingest=args.ingest,
        dry_run_status=args.dry_run_status,
    )


if __name__ == "__main__":
    raise SystemExit(main())
