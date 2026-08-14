import json
from google.cloud import firestore

db = firestore.Client(project="regal-scholar-453620-r7", database="copernicusai")
col = db.collection("research_papers")

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
    if n % 2000 == 0:
        print(f"  streamed {n}...")

print(f"total: {n}, with score: {len(rows)}")
rows.sort(key=lambda x: x[1])
total = len(rows)
print(f"score range: min={rows[0][1]:.4f} max={rows[-1][1]:.4f}")

mid_idx = total // 2
near_boundary = rows[:15]
near_mid = rows[mid_idx - 7 : mid_idx + 8]
near_top = rows[-10:]

def fmt(band):
    return [{"pmid": doc_id.replace("pubmed_", ""), "q8_score": s, "title": t} for doc_id, s, t in band]

out = {
    "total_q8_docs": total,
    "score_min": rows[0][1],
    "score_max": rows[-1][1],
    "near_boundary_15": fmt(near_boundary),
    "near_median_15": fmt(near_mid),
    "near_top_10": fmt(near_top),
}
outpath = r'C:\Users\garyw\glmp\docs\open-questions\glmp-merge-quality-audit-2026-08-13\q8_full_bands.json'
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"wrote {outpath}")
