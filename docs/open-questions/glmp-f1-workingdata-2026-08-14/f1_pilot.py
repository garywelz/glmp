import json, os
from datetime import datetime, timezone
from google.cloud import firestore

BASE = r"C:\Users\garyw\glmp\docs\open-questions\glmp-f1-workingdata-2026-08-14"
RUN_ID = "glmp-f1-firstpass-20260814"

scored = json.load(open(os.path.join(BASE, "f1_scored.json"), encoding="utf-8"))
meta = json.load(open(os.path.join(BASE, "f1_metadata.json"), encoding="utf-8"))["papers"]
raw = json.load(open(os.path.join(BASE, "f1_pmids_raw.json"), encoding="utf-8"))
per_term = raw["per_term"]
dryrun = json.load(open(os.path.join(BASE, "f1_dryrun_candidates.json"), encoding="utf-8"))

db = firestore.Client(project="regal-scholar-453620-r7", database="copernicusai")
col = db.collection("research_papers")

def terms_for(pmid):
    return [t for t, r in per_term.items() if pmid in r["pmids"]]

def now_iso():
    return datetime.now(timezone.utc).isoformat()

pilot_new = dryrun["new_docs"][:3]
pilot_merge = dryrun["merge_docs"][:3]
print("pilot new:", pilot_new)
print("pilot merge:", pilot_merge)

for pmid in pilot_new:
    p = meta[pmid]
    doc = {
        "url": None,
        "pmid": pmid,
        "raw_source_id": f"pubmed_{pmid}",
        "title": p["title"],
        "abstract": p["abstract"],
        "authors": p["authors"],
        "author_string": p["author_string"],
        "journal": p["journal"],
        "journal_full": p["journal_full"],
        "year": p["year"],
        "doi": p["doi"],
        "keywords": p["keywords"],
        "sources": ["pubmed"],
        "categories": [],
        "discipline": "biology",
        "arxiv_id": None,
        "question_scope_ids": ["glmp-f1"],
        "acquisition_matches": [{
            "question": "glmp-f1",
            "kind": "frontier",
            "score": scored[pmid]["score"],
            "terms": terms_for(pmid),
        }],
        "run_id": RUN_ID,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    col.document(f"pubmed_{pmid}").set(doc)
    print(f"  wrote new: pubmed_{pmid}")

for pmid in pilot_merge:
    ref = col.document(f"pubmed_{pmid}")
    ref.update({
        "question_scope_ids": firestore.ArrayUnion(["glmp-f1"]),
        "acquisition_matches": firestore.ArrayUnion([{
            "question": "glmp-f1",
            "kind": "frontier",
            "score": scored[pmid]["score"],
            "terms": terms_for(pmid),
        }]),
        "updated_at": now_iso(),
    })
    print(f"  updated merge: pubmed_{pmid}")

print("\nverifying directly from Firestore...")
for pmid in pilot_new + pilot_merge:
    snap = col.document(f"pubmed_{pmid}").get()
    d = snap.to_dict()
    f1_matches = [m for m in (d.get("acquisition_matches") or []) if m.get("question") == "glmp-f1"]
    print(f"  pubmed_{pmid}: question_scope_ids={d.get('question_scope_ids')} f1_matches={f1_matches} has_embedding={d.get('embedding') is not None}")
