import json, sys

rows = json.load(open(
    r'C:\Users\garyw\glmp\docs\open-questions\glmp-merge-quality-audit-2026-08-13\q10_all_scored_live.json',
    encoding='utf-8'
))
total = len(rows)

start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
end = int(sys.argv[2]) if len(sys.argv) > 2 else 100
step = int(sys.argv[3]) if len(sys.argv) > 3 else 5

for pct in range(start, end + 1, step):
    idx = int(total * pct / 100)
    idx = min(idx, total - 1)
    print(f"--- p{pct} (rank {idx}, score={rows[idx]['q10_score']:.4f}) ---")
    for j in range(idx, min(idx + 5, total)):
        r = rows[j]
        print(f"  {r['q10_score']:.4f}  {r['title'][:100]}")
