import json
from google.cloud import firestore

db = firestore.Client(project="regal-scholar-453620-r7", database="copernicusai")
col = db.collection("research_papers")

print("streaming all glmp-q10-attributed docs (projected fields only)...")
q = col.where("question_scope_ids", "array_contains", "glmp-q10").select(
    ["title", "acquisition_matches"]
)
rows = []
n = 0
for snap in q.stream():
    n += 1
    data = snap.to_dict() or {}
    q10_score = None
    for m in (data.get("acquisition_matches") or []):
        if m.get("question") == "glmp-q10":
            q10_score = m.get("score")
            break
    if q10_score is not None:
        rows.append({"pmid": snap.id.replace("pubmed_", ""), "q10_score": q10_score, "title": data.get("title", "")})
    if n % 2000 == 0:
        print(f"  streamed {n}...")

print(f"total: {n}, with score: {len(rows)}")
rows.sort(key=lambda x: -x["q10_score"])

outpath = r'C:\Users\garyw\glmp\docs\open-questions\glmp-merge-quality-audit-2026-08-13\q10_all_scored_live.json'
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(rows, f, indent=2, ensure_ascii=False)
print(f"wrote {outpath} ({len(rows)} rows)")
