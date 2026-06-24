#!/usr/bin/env python3.8
"""Split scout worker: PubMed only (+ optional GLMP query supplement)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scout_common import run_scout  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="CopernicusAI PubMed scout (split worker)")
    parser.add_argument("run_type", choices=["am", "pm"], help="Run slot label for logging and job_id")
    parser.add_argument(
        "--glmp-queries",
        action="store_true",
        default=True,
        help="Run GLMP cluster 1–3 PubMed supplement after main acquire (default: on)",
    )
    parser.add_argument("--no-glmp-queries", action="store_true", help="Skip GLMP query supplement")
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Run ingest_metadata_to_firestore.sh after acquisition (off by default)",
    )
    parser.add_argument("--dry-run-status", action="store_true", help="Log only; no acquire or Firestore writes")
    args = parser.parse_args()

    return run_scout(
        "pubmed",
        args.run_type,
        with_glmp_queries=not args.no_glmp_queries,
        with_ingest=args.ingest,
        dry_run_status=args.dry_run_status,
    )


if __name__ == "__main__":
    raise SystemExit(main())
