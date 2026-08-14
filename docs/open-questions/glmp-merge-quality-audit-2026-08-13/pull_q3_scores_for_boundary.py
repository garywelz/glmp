import json
from google.cloud import firestore

db = firestore.Client(project="regal-scholar-453620-r7", database="copernicusai")
col = db.collection("research_papers")

d = json.load(open(
    r'C:\Users\garyw\glmp\docs\open-questions\glmp-merge-quality-audit-2026-08-13\q10_q3_boundary_sample.json',
    encoding='utf-8'
))

all_rows = d['near_boundary_15'] + d['near_top_5']
pmids = [r['pmid'] for r in all_rows]

refs = [col.document(f"pubmed_{p}") for p in pmids]
docs_by_id = {}
for snap in db.get_all(refs):
    if snap.exists:
        docs_by_id[snap.id] = snap.to_dict()

out = []
for r in all_rows:
    doc = docs_by_id.get(f"pubmed_{r['pmid']}")
    q3_score = None
    if doc:
        for m in (doc.get("acquisition_matches") or []):
            if m.get("question") == "glmp-q3":
                q3_score = m.get("score")
                break
    out.append({
        "pmid": r["pmid"],
        "q10_score": r["q10_score"],
        "q3_score": q3_score,
        "title": r["title"],
    })

outpath = r'C:\Users\garyw\glmp\docs\open-questions\glmp-merge-quality-audit-2026-08-13\q10_q3_boundary_with_q3_scores.json'
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"wrote {outpath}")

for r in out:
    q3s = f"{r['q3_score']:.4f}" if r['q3_score'] is not None else "MISSING"
    print(f"q10={r['q10_score']:.4f}  q3={q3s}  {r['title'][:80]}")
