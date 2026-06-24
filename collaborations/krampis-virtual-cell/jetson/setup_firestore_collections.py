#!/usr/bin/env python3.8
"""
Bootstrap / verify Firestore collections for GLMP decoder automation.

Firestore creates collections on first document write. This script:
  - Verifies connectivity and that research_papers exists (scout target)
  - Prints schemas for glmp_circuits and scheduler_status
  - With --apply: writes _schema seed documents (safe to re-run)

Default is --dry-run (no writes).

Example:
  python3.8 setup_firestore_collections.py
  python3.8 setup_firestore_collections.py --apply
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

_JETSON_ROOT = Path(__file__).resolve().parent
if str(_JETSON_ROOT) not in sys.path:
    sys.path.insert(0, str(_JETSON_ROOT))

from firestore_config import (  # noqa: E402
    DEFAULT_CREDENTIALS_PATH,
    EXAMPLE_GLMP_CIRCUIT_DOC,
    EXAMPLE_SCHEDULER_STATUS_DOC,
    FIRESTORE_DATABASE,
    GCP_PROJECT_ID,
    GLMP_CIRCUITS_COLLECTION,
    RESEARCH_PAPERS_COLLECTION,
    SCHEDULER_STATUS_COLLECTION,
)


def get_client():
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and DEFAULT_CREDENTIALS_PATH.exists():
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(DEFAULT_CREDENTIALS_PATH)
    from google.cloud import firestore

    return firestore.Client(project=GCP_PROJECT_ID, database=FIRESTORE_DATABASE)


def _schema_seed(collection: str, purpose: str, example: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "_kind": "schema_seed",
        "collection": collection,
        "purpose": purpose,
        "example_document": example,
        "managed_by": "setup_firestore_collections.py",
    }


def dry_run_report() -> Dict[str, Any]:
    return {
        "project_id": GCP_PROJECT_ID,
        "database": FIRESTORE_DATABASE,
        "credentials_path": str(DEFAULT_CREDENTIALS_PATH),
        "credentials_exists": DEFAULT_CREDENTIALS_PATH.exists(),
        "existing_collection_verified": RESEARCH_PAPERS_COLLECTION,
        "collections_to_initialize": [
            {
                "name": GLMP_CIRCUITS_COLLECTION,
                "document_id_pattern": "{circuit_id}",
                "seed_doc_id": "_schema",
                "example": EXAMPLE_GLMP_CIRCUIT_DOC,
            },
            {
                "name": SCHEDULER_STATUS_COLLECTION,
                "document_id_pattern": "{job_id}",
                "seed_doc_id": "_schema",
                "example": EXAMPLE_SCHEDULER_STATUS_DOC,
            },
        ],
        "note": (
            "Dry run only. Re-run with --apply to write _schema seed documents. "
            "Scout ingest continues to use research_papers unchanged."
        ),
    }


def verify_research_papers(db) -> Dict[str, Any]:
    col = db.collection(RESEARCH_PAPERS_COLLECTION)
    sample = list(col.limit(1).stream())
    return {
        "collection": RESEARCH_PAPERS_COLLECTION,
        "reachable": True,
        "sample_doc_exists": bool(sample),
        "sample_doc_id": sample[0].id if sample else None,
    }


def apply_seeds(db) -> List[Dict[str, Any]]:
    writes = []

    glmp_ref = db.collection(GLMP_CIRCUITS_COLLECTION).document("_schema")
    glmp_payload = _schema_seed(
        GLMP_CIRCUITS_COLLECTION,
        "Decoded GLMP circuits from DNA decoder batch runner",
        EXAMPLE_GLMP_CIRCUIT_DOC,
    )
    glmp_ref.set(glmp_payload, merge=True)
    writes.append({"collection": GLMP_CIRCUITS_COLLECTION, "doc_id": "_schema", "action": "upserted"})

    sched_ref = db.collection(SCHEDULER_STATUS_COLLECTION).document("_schema")
    sched_payload = _schema_seed(
        SCHEDULER_STATUS_COLLECTION,
        "Cron / batch job heartbeats",
        EXAMPLE_SCHEDULER_STATUS_DOC,
    )
    sched_ref.set(sched_payload, merge=True)
    writes.append({"collection": SCHEDULER_STATUS_COLLECTION, "doc_id": "_schema", "action": "upserted"})

    return writes


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify and optionally seed Firestore collections.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write _schema seed documents (default: dry-run only)",
    )
    args = parser.parse_args()

    if args.apply:
        try:
            db = get_client()
            rp = verify_research_papers(db)
            seeds = apply_seeds(db)
            report = {
                "mode": "apply",
                "research_papers_check": rp,
                "seeds_written": seeds,
            }
        except Exception as exc:
            print(json.dumps({"mode": "apply", "error": str(exc)}, indent=2))
            return 1
    else:
        report = dry_run_report()
        report["mode"] = "dry-run"
        # Best-effort live check without requiring apply
        try:
            db = get_client()
            report["research_papers_check"] = verify_research_papers(db)
        except Exception as exc:
            report["research_papers_check"] = {"reachable": False, "error": str(exc)}

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
