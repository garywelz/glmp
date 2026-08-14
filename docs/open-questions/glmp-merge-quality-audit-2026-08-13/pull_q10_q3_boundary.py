import json

base = r'C:\Users\garyw\glmp\docs\open-questions\glmp-q10-workingdata-2026-08-12'
scored = json.load(open(base + r'\q10_scored.json', encoding='utf-8'))
dedupe = json.load(open(base + r'\q10_dedupe.json', encoding='utf-8'))
meta = json.load(open(base + r'\q10_metadata.json', encoding='utf-8'))['papers']

existing = dedupe['existing']
CUTOFF = 0.3442  # q10's cutoff

q3_merge_pmids = [
    k.replace('pubmed_', '') for k, v in existing.items()
    if v['run_id'] == 'glmp-q3-firstpass-20260809'
]
print(f"q10-merge docs from q3's run (all, pre-cutoff-filter): {len(q3_merge_pmids)}")

scored_pairs = [
    (p, scored[p]['score']) for p in q3_merge_pmids
    if p in scored and scored[p].get('score') is not None and scored[p]['score'] >= CUTOFF
]
scored_pairs.sort(key=lambda x: x[1])

print(f"scored & above cutoff: {len(scored_pairs)}, q10-score range: min={scored_pairs[0][1]:.4f} max={scored_pairs[-1][1]:.4f}")

near_boundary = scored_pairs[:15]
near_top = scored_pairs[-5:]

out = {
    "q10_cutoff": CUTOFF,
    "total_q3_merge_docs_in_q10": len(scored_pairs),
    "near_boundary_15": [
        {"pmid": p, "q10_score": s, "title": meta[p]["title"]}
        for p, s in near_boundary
    ],
    "near_top_5": [
        {"pmid": p, "q10_score": s, "title": meta[p]["title"]}
        for p, s in near_top
    ],
}
outpath = r'C:\Users\garyw\glmp\docs\open-questions\glmp-merge-quality-audit-2026-08-13\q10_q3_boundary_sample.json'
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"wrote {outpath}")
