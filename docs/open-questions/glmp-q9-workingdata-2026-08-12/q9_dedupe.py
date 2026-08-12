import json, os
from google.cloud import firestore

BASE = r"C:\Users\garyw\AppData\Local\Temp\claude\C--Users-garyw-glmp\917cae92-4c16-4f2f-9e46-409f794b52a0\scratchpad"
IN = os.path.join(BASE, "q9_pmids_raw.json")
OUT = os.path.join(BASE, "q9_dedupe.json")

db = firestore.Client(project="regal-scholar-453620-r7", database="copernicusai")

with open(IN, encoding="utf-8") as f:
    raw = json.load(f)
pmids = raw["union_pmids"]
ids = [f"pubmed_{p}" for p in pmids]

col = db.collection("research_papers")
existing = {}
CHUNK = 300
for i in range(0, len(ids), CHUNK):
    chunk = ids[i:i+CHUNK]
    refs = [col.document(x) for x in chunk]
    for snap in db.get_all(refs):
        if snap.exists:
            data = snap.to_dict()
            existing[snap.id] = {
                "has_embedding": data.get("embedding") is not None,
                "already_q9": "glmp-q9" in (data.get("question_scope_ids") or []),
                "run_id": data.get("run_id"),
            }
    print(f"checked {min(i+CHUNK, len(ids))}/{len(ids)}, found so far: {len(existing)}")

already_q9 = sum(1 for v in existing.values() if v["already_q9"])
print(f"\nTotal candidates: {len(ids)}")
print(f"Already in corpus: {len(existing)}")
print(f"Already tagged glmp-q9 (should be 0, pre-write): {already_q9}")
print(f"Genuinely new (not in corpus): {len(ids) - len(existing)}")

with open(OUT, "w", encoding="utf-8") as f:
    json.dump({"existing": existing, "total_candidates": len(ids)}, f, indent=2)
print(f"wrote {OUT}")
