import json, os, sys

BASE = r"C:\Users\garyw\glmp\docs\open-questions\glmp-f1-workingdata-2026-08-14"
scored = json.load(open(os.path.join(BASE, "f1_scored.json"), encoding="utf-8"))
meta = json.load(open(os.path.join(BASE, "f1_metadata.json"), encoding="utf-8"))["papers"]

rows = [(pmid, v["score"]) for pmid, v in scored.items() if v.get("score") is not None]
rows.sort(key=lambda x: -x[1])
total = len(rows)

start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
end = int(sys.argv[2]) if len(sys.argv) > 2 else 100
step = int(sys.argv[3]) if len(sys.argv) > 3 else 5

print(f"total scored: {total}, score range: max={rows[0][1]:.4f} min={rows[-1][1]:.4f}")
for pct in range(start, end + 1, step):
    idx = int(total * pct / 100)
    idx = min(idx, total - 1)
    print(f"--- p{pct} (rank {idx}, score={rows[idx][1]:.4f}) ---")
    for j in range(idx, min(idx + 5, total)):
        pmid, s = rows[j]
        title = meta[pmid]["title"]
        print(f"  {s:.4f}  {title[:100]}")
