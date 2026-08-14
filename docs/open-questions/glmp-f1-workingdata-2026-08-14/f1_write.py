import json, os, time
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

already_piloted = set(dryrun["new_docs"][:3]) | set(dryrun["merge_docs"][:3])
new_docs = [p for p in dryrun["new_docs"] if p not in already_piloted]
merge_docs = [p for p in dryrun["merge_docs"] if p not in already_piloted]
print(f"remaining new: {len(new_docs)}  remaining merge: {len(merge_docs)}")

new_ok, new_fail = 0, 0
for pmid in new_docs:
    try:
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
        new_ok += 1
    except Exception as e:
        print(f"  FAIL new pubmed_{pmid}: {e}")
        new_fail += 1
    if new_ok % 50 == 0 and new_ok > 0:
        print(f"  new progress: {new_ok}/{len(new_docs)}")

merge_ok, merge_fail = 0, 0
for pmid in merge_docs:
    try:
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
        merge_ok += 1
    except Exception as e:
        print(f"  FAIL merge pubmed_{pmid}: {e}")
        merge_fail += 1
    if merge_ok % 50 == 0 and merge_ok > 0:
        print(f"  merge progress: {merge_ok}/{len(merge_docs)}")

print(f"\nDONE. new: {new_ok} ok, {new_fail} failed. merge: {merge_ok} ok, {merge_fail} failed.")
