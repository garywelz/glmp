import json, os

BASE = r"C:\Users\garyw\glmp\docs\open-questions\glmp-f1-workingdata-2026-08-14"
CUTOFF = 0.3769

scored = json.load(open(os.path.join(BASE, "f1_scored.json"), encoding="utf-8"))
meta = json.load(open(os.path.join(BASE, "f1_metadata.json"), encoding="utf-8"))["papers"]
dedupe = json.load(open(os.path.join(BASE, "f1_dedupe.json"), encoding="utf-8"))["existing"]
raw = json.load(open(os.path.join(BASE, "f1_pmids_raw.json"), encoding="utf-8"))
per_term = raw["per_term"]

candidates = [pmid for pmid, v in scored.items() if v.get("score") is not None and v["score"] >= CUTOFF]
print(f"candidates >= {CUTOFF}: {len(candidates)}")

# integrity checks
missing_meta = [p for p in candidates if p not in meta]
dup_check = len(candidates) == len(set(candidates))
already_f1 = [p for p in candidates if dedupe.get(f"pubmed_{p}", {}).get("already_f1")]

print(f"missing metadata: {len(missing_meta)}")
print(f"no duplicate pmids: {dup_check}")
print(f"already tagged glmp-f1 (should be 0): {len(already_f1)}")

new_docs = [p for p in candidates if f"pubmed_{p}" not in dedupe]
merge_docs = [p for p in candidates if f"pubmed_{p}" in dedupe]
print(f"new: {len(new_docs)}  merge: {len(merge_docs)}")

# term attribution + zero-term check
zero_terms = 0
for p in candidates:
    terms = [t for t, r in per_term.items() if p in r["pmids"]]
    if not terms:
        zero_terms += 1
print(f"candidates with zero matched terms (should be 0): {zero_terms}")

# merge run_id breakdown
from collections import Counter
run_ids = Counter(dedupe[f"pubmed_{p}"].get("run_id") for p in merge_docs)
print("merge docs by prior run_id:")
for rid, n in run_ids.most_common():
    print(f"  {rid}: {n}")

out = {
    "cutoff": CUTOFF,
    "candidates": candidates,
    "new_docs": new_docs,
    "merge_docs": merge_docs,
}
with open(os.path.join(BASE, "f1_dryrun_candidates.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
print("wrote f1_dryrun_candidates.json")
