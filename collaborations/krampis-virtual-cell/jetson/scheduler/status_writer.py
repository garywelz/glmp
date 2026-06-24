#!/usr/bin/env python3.8
"""
Write job heartbeats to Firestore scheduler_status collection.

Standalone — importable by scout and decoder cron jobs on the Jetson.

Example:
  python3.8 status_writer.py \\
    --job-id scout_pubmed_am \\
    --status success \\
    --doc-count 47 \\
    --start 2026-06-24T10:15:00+00:00 \\
    --end 2026-06-24T10:18:43+00:00
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

# Allow running from repo staging path or deployed /media/sdcard/scheduler/
_JETSON_ROOT = Path(__file__).resolve().parents[1]
if str(_JETSON_ROOT) not in sys.path:
    sys.path.insert(0, str(_JETSON_ROOT))

from firestore_config import (  # noqa: E402
    DEFAULT_CREDENTIALS_PATH,
    FIRESTORE_DATABASE,
    GCP_PROJECT_ID,
    SCHEDULER_STATUS_COLLECTION,
)


def _parse_iso(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get_firestore_client():
    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds and DEFAULT_CREDENTIALS_PATH.exists():
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(DEFAULT_CREDENTIALS_PATH)
    from google.cloud import firestore

    return firestore.Client(project=GCP_PROJECT_ID, database=FIRESTORE_DATABASE)


def write_job_status(
    job_id: str,
    status: str,
    doc_count: int = 0,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    next_scheduled: Optional[str] = None,
    error_message: Optional[str] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """
    Upsert scheduler_status/{job_id}. Increments total_runs; updates consecutive_failures.
    """
    if status not in ("success", "failure", "running"):
        raise ValueError(f"status must be success|failure|running, got {status!r}")

    end_iso = end_time or _iso_now()
    start_iso = start_time or end_iso

    payload: Dict[str, Any] = {
        "job_id": job_id,
        "last_run_start": start_iso,
        "last_run_end": end_iso if status != "running" else None,
        "last_status": status,
        "last_doc_count": int(doc_count),
        "updated_at": _iso_now(),
    }
    if next_scheduled:
        payload["next_scheduled"] = next_scheduled
    if error_message:
        payload["last_error"] = error_message

    if dry_run:
        payload["_dry_run"] = True
        payload["_note"] = (
            f"Would upsert {SCHEDULER_STATUS_COLLECTION}/{job_id} "
            f"in project={GCP_PROJECT_ID} database={FIRESTORE_DATABASE}"
        )
        return payload

    db = get_firestore_client()
    ref = db.collection(SCHEDULER_STATUS_COLLECTION).document(job_id)
    snap = ref.get()

    total_runs = 0
    consecutive_failures = 0
    if snap.exists:
        existing = snap.to_dict() or {}
        total_runs = int(existing.get("total_runs") or 0)
        consecutive_failures = int(existing.get("consecutive_failures") or 0)

    if status == "running":
        payload["total_runs"] = total_runs
        payload["consecutive_failures"] = consecutive_failures
    else:
        total_runs += 1
        payload["total_runs"] = total_runs
        if status == "success":
            payload["consecutive_failures"] = 0
        else:
            payload["consecutive_failures"] = consecutive_failures + 1

    ref.set(payload, merge=True)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Upsert scheduler_status heartbeat in Firestore.")
    parser.add_argument("--job-id", required=True, help="Stable job identifier, e.g. scout_pubmed_am")
    parser.add_argument(
        "--status",
        required=True,
        choices=["success", "failure", "running"],
        help="Run outcome",
    )
    parser.add_argument("--doc-count", type=int, default=0, help="Documents processed this run")
    parser.add_argument("--start", help="ISO8601 run start (default: now)")
    parser.add_argument("--end", help="ISO8601 run end (default: now)")
    parser.add_argument("--next-scheduled", help="Optional ISO8601 next scheduled run")
    parser.add_argument("--error", help="Error message when status=failure")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print payload only; do not write to Firestore",
    )
    args = parser.parse_args()

    if args.start:
        _parse_iso(args.start)
    if args.end:
        _parse_iso(args.end)

    try:
        result = write_job_status(
            job_id=args.job_id,
            status=args.status,
            doc_count=args.doc_count,
            start_time=args.start,
            end_time=args.end,
            next_scheduled=args.next_scheduled,
            error_message=args.error,
            dry_run=args.dry_run,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    import json

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
