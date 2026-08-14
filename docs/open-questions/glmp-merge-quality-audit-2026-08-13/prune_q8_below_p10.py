#!/usr/bin/env python3
"""
Remove glmp-q8 attribution from docs below the independently-verified real
cutoff (p10, score >= 0.5004). Approved by Gary 2026-08-13/14.

For each below-cutoff doc: read full acquisition_matches, filter out the
glmp-q8 entry, recompute question_scope_ids as the flat mirror of the
remaining acquisition_matches[].question + cited_for_question if present
(same formula as ingest_papers_from_metadata_json.py's _to_firestore_paper).
Does NOT delete the document -- it remains a valid corpus member under any
other question it legitimately carries, or unscoped if q8 was its only tag.

Modes: --dry-run (default) | --write
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

from google.cloud import firestore

CUTOFF = 0.5004  # p10
PROJECT = "regal-scholar-453620-r7"
DATABASE = "copernicusai"


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def recompute_scope(data: dict) -> tuple[list, list]:
    """Returns (new_acquisition_matches, new_question_scope_ids) with glmp-q8 removed."""
    matches = [m for m in (data.get("acquisition_matches") or []) if m.get("question") != "glmp-q8"]
    scope = set()
    for m in matches:
        if isinstance(m, dict) and m.get("question"):
            scope.add(str(m["question"]))
    if data.get("cited_for_question"):
        scope.add(str(data["cited_for_question"]))
    return matches, sorted(scope)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    write = bool(args.write)

    rows = json.load(open(
        r'C:\Users\garyw\glmp\docs\open-questions\glmp-merge-quality-audit-2026-08-13\q8_all_scored_live.json',
        encoding='utf-8'
    ))
    below = [r for r in rows if r["q8_score"] < CUTOFF]
    print(f"Mode: {'WRITE' if write else 'DRY-RUN'}")
    print(f"total glmp-q8 docs: {len(rows)}  below cutoff ({CUTOFF}): {len(below)}")

    if args.limit:
        below = below[: args.limit]
        print(f"limited to {len(below)} for this run")

    db = firestore.Client(project=PROJECT, database=DATABASE)
    col = db.collection("research_papers")

    CHUNK = 300
    processed = 0
    orphaned = 0  # docs where q8 was the only attribution
    still_multi = 0
    failed = 0

    for i in range(0, len(below), CHUNK):
        chunk = below[i : i + CHUNK]
        refs = [col.document(f"pubmed_{r['pmid']}") for r in chunk]
        snaps = {s.id: s for s in db.get_all(refs)}

        batch = db.batch() if write else None
        staged = 0
        for r in chunk:
            doc_id = f"pubmed_{r['pmid']}"
            snap = snaps.get(doc_id)
            if not snap or not snap.exists:
                failed += 1
                print(f"  MISSING {doc_id}")
                continue
            data = snap.to_dict() or {}
            if "glmp-q8" not in (data.get("question_scope_ids") or []):
                # already processed / never had it -- skip silently, idempotent
                continue
            new_matches, new_scope = recompute_scope(data)
            if not new_scope:
                orphaned += 1
            else:
                still_multi += 1
            if write:
                batch.update(
                    col.document(doc_id),
                    {
                        "acquisition_matches": new_matches,
                        "question_scope_ids": new_scope,
                        "updated_at": _now_iso(),
                    },
                )
                staged += 1
            processed += 1

        if write and staged:
            batch.commit()
        print(f"  progress: {min(i + CHUNK, len(below))}/{len(below)}")

    print("=" * 60)
    print(f"processed={processed} orphaned(no other question)={orphaned} still_multi_scoped={still_multi} missing={failed}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
