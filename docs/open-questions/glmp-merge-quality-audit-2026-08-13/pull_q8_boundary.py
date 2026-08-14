import json
from google.cloud import firestore

db = firestore.Client(project="regal-scholar-453620-r7", database="copernicusai")
col = db.collection("research_papers")

CUTOFF = 0.36

print("streaming all glmp-q8-attributed docs (projected fields only)...")
q = col.where("question_scope_ids", "array_contains", "glmp-q8").select(
    ["title", "acquisition_matches"]
)
rows = []
n = 0
for snap in q.stream():
    n += 1
    data = snap.to_dict() or {}
    q8_score = None
    for m in (data.get("acquisition_matches") or []):
        if m.get("question") == "glmp-q8":
            q8_score = m.get("score")
            break
    if q8_score is not None:
        rows.append((snap.id, q8_score, data.get("title", "")))
    if n % 1000 == 0:
        print(f"  streamed {n}...")

print(f"total glmp-q8 docs streamed: {n}, with q8 score: {len(rows)}")
rows.sort(key=lambda x: x[1])

print(f"score range: min={rows[0][1]:.4f} max={rows[-1][1]:.4f}")

# nearest to cutoff from below (should be none, since cutoff was enforced) and above
near_boundary = rows[:20]

out = {
    "q8_cutoff_recorded": CUTOFF,
    "total_q8_docs_with_score": len(rows),
    "actual_min_score": rows[0][1],
    "near_boundary_20": [
        {"pmid": doc_id.replace("pubmed_", ""), "q8_score": s, "title": t}
        for doc_id, s, t in near_boundary
    ],
}
outpath = r'C:\Users\garyw\glmp\docs\open-questions\glmp-merge-quality-audit-2026-08-13\q8_boundary_sample.json'
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"wrote {outpath}")
