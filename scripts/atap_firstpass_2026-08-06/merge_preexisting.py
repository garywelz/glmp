"""
A2 requirement 5: a hit against the existing corpus must still record the
new attribution -- not a no-op. These 7 papers were already in
research_papers (predating this run, no run_id) so skip_existing correctly
left them untouched rather than overwriting; this additively merges just
the acquisition_matches + run_id fields, same shape as item 45's
merge_citation_onto_firestore_doc, so they carry ATAP provenance too
without touching title/abstract/sources/anything else.
"""
import json
from google.cloud import firestore

RUN_ID = "atap-firstpass-20260806"
PRE_EXISTING_AIDS = [
    "2006.04757v3", "1903.00936v2", "2605.02787v1", "2606.24415v1",
    "2008.03496v1", "2601.05691v2", "1902.00355v3",
]

db = firestore.Client(project="regal-scholar-453620-r7", database="copernicusai")
col = db.collection("research_papers")

candidates_dir = r"C:\Users\garyw\AppData\Local\Temp\atap_firstpass\papers"

for aid in PRE_EXISTING_AIDS:
    safe_id = aid.replace("/", "_")
    with open(f"{candidates_dir}\\{safe_id}.json", encoding="utf-8") as f:
        candidate = json.load(f)
    doc_id = f"arxiv_{safe_id}"
    doc_ref = col.document(doc_id)
    snap = doc_ref.get()
    if not snap.exists:
        print(f"  {aid}: MISSING at write time, skipping merge (unexpected)")
        continue
    existing = snap.to_dict() or {}
    existing_matches = existing.get("acquisition_matches") or []
    new_matches = candidate.get("acquisition_matches") or []
    # Additive: keep whatever was there (nothing, in this case), append new.
    merged_matches = existing_matches + [m for m in new_matches if m not in existing_matches]
    doc_ref.update({
        "acquisition_matches": merged_matches,
        "run_id": existing.get("run_id") or RUN_ID,
        "acquisition_channel": existing.get("acquisition_channel") or RUN_ID,
    })
    print(f"  {aid}: merged {len(new_matches)} match(es), doc otherwise untouched")

print("Done.")
