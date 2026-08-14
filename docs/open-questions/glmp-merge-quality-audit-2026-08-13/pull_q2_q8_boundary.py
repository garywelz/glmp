import json

base = r'C:\Users\garyw\glmp\docs\open-questions\glmp-q2-workingdata-2026-08-12'
scored = json.load(open(base + r'\q2_scored.json', encoding='utf-8'))
dedupe = json.load(open(base + r'\q2_dedupe.json', encoding='utf-8'))
meta = json.load(open(base + r'\q2_metadata.json', encoding='utf-8'))['papers']

existing = dedupe['existing']
CUTOFF = 0.4025  # q2's cutoff

# q2-merge docs whose prior run_id was glmp-q8-firstpass-20260811
q8_merge_pmids = [
    k.replace('pubmed_', '') for k, v in existing.items()
    if v['run_id'] == 'glmp-q8-firstpass-20260811'
]
print(f"q2-merge docs from q8's run: {len(q8_merge_pmids)}")

# their q2 scores -- ONLY docs that actually passed q2's cutoff and were written to q2's scope
scored_pairs = [
    (p, scored[p]['score']) for p in q8_merge_pmids
    if p in scored and scored[p].get('score') is not None and scored[p]['score'] >= CUTOFF
]
scored_pairs.sort(key=lambda x: x[1])  # ascending: boundary (near cutoff) first

print(f"scored: {len(scored_pairs)}, q2-score range: min={scored_pairs[0][1]:.4f} max={scored_pairs[-1][1]:.4f}")

# sample: 15 nearest to cutoff (both sides, but all are >=cutoff since these ARE in the merge set which required score>=cutoff)
# take lowest-scoring 15 (closest to the q2 cutoff boundary) plus 5 near the top for contrast
near_boundary = scored_pairs[:15]
near_top = scored_pairs[-5:]

out = {
    "q2_cutoff": CUTOFF,
    "total_q8_merge_docs_in_q2": len(q8_merge_pmids),
    "near_boundary_15": [
        {"pmid": p, "q2_score": s, "title": meta[p]["title"]}
        for p, s in near_boundary
    ],
    "near_top_5": [
        {"pmid": p, "q2_score": s, "title": meta[p]["title"]}
        for p, s in near_top
    ],
}
outpath = r'C:\Users\garyw\glmp\docs\open-questions\glmp-merge-quality-audit-2026-08-13\q2_q8_boundary_sample.json'
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"wrote {outpath}")
