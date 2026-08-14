import json
from google.cloud import firestore

rows = json.load(open(
    r'C:\Users\garyw\glmp\docs\open-questions\glmp-merge-quality-audit-2026-08-13\q8_all_scored_live.json',
    encoding='utf-8'
))
CUTOFF = 0.5004
below = [r for r in rows if r["q8_score"] < CUTOFF]
pilot_pmids = [r["pmid"] for r in below[:6]]

db = firestore.Client(project="regal-scholar-453620-r7", database="copernicusai")
col = db.collection("research_papers")

for pmid in pilot_pmids:
    doc = col.document(f"pubmed_{pmid}").get()
    d = doc.to_dict()
    print(pmid, "title=", (d.get("title") or "")[:55])
    print("   question_scope_ids=", d.get("question_scope_ids"))
    print("   acquisition_matches=", d.get("acquisition_matches"))
    print("   has_embedding=", d.get("embedding") is not None)
