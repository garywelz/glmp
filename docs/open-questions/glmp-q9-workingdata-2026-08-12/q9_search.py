import json, time, sys
import requests

TERMS = [
    "cell fate decision network",
    "developmental switch commitment",
    "sporulation initiation regulation",
    "competence regulation Bacillus subtilis",
    "lineage commitment transcription factor",
    "epigenetic memory gene expression",
]

EMAIL = "gary@copernicusai.fyi"
ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
OUT = r"C:\Users\garyw\AppData\Local\Temp\claude\C--Users-garyw-glmp\917cae92-4c16-4f2f-9e46-409f794b52a0\scratchpad\q9_pmids_raw.json"

def esearch(term, retmax=9999):
    params = {
        "db": "pubmed",
        "term": term,
        "retmax": retmax,
        "sort": "relevance",
        "retmode": "json",
        "email": EMAIL,
    }
    r = requests.get(ESEARCH, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    res = data["esearchresult"]
    count = int(res["count"])
    ids = res.get("idlist", [])
    return count, ids

results = {}
for term in TERMS:
    count, ids = esearch(term)
    truncated = count > len(ids)
    print(f"{term!r}: raw_count={count} fetched={len(ids)} truncated={truncated}")
    results[term] = {"raw_count": count, "fetched": len(ids), "truncated": truncated, "pmids": ids}
    time.sleep(0.34)

union = set()
for term, r in results.items():
    union.update(r["pmids"])

print(f"\nUnique PMID union across {len(TERMS)} terms: {len(union)}")

with open(OUT, "w", encoding="utf-8") as f:
    json.dump({"per_term": results, "union_pmids": sorted(union)}, f, indent=2)
print(f"wrote {OUT}")
