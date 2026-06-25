#!/usr/bin/env python3
"""Print scheduler_status docs for split scouts. Run on Jetson with copernicus env."""
import os
from google.cloud import firestore

os.environ.setdefault(
    "GOOGLE_APPLICATION_CREDENTIALS",
    os.path.expanduser("~/.config/copernicus/gcp-sa.json"),
)

db = firestore.Client(project="regal-scholar-453620-r7", database="copernicusai")
ids = [
    "scout_pubmed_am",
    "scout_pubmed_pm",
    "scout_biorxiv_am",
    "scout_biorxiv_pm",
    "scout_arxiv_am",
    "scout_arxiv_pm",
    "scout_ingest_am",
    "scout_ingest_pm",
]
for doc_id in ids:
    snap = db.collection("scheduler_status").document(doc_id).get()
    if not snap.exists:
        print(f"{doc_id}: (no doc)")
        continue
    x = snap.to_dict()
    ts = x.get("last_run_at") or x.get("updated_at") or "?"
    if hasattr(ts, "isoformat"):
        ts = ts.isoformat()[:19]
    elif isinstance(ts, str):
        ts = ts[:19]
    print(
        f"{doc_id}: status={x.get('last_status')} "
        f"docs={x.get('last_doc_count')} runs={x.get('total_runs')} "
        f"failures={x.get('consecutive_failures', 0)} at={ts}"
    )
