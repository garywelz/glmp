#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FASTA = ROOT / "sequences" / "gal1_promoter_1kb.fa"
JSON = ROOT / "results" / "gal1_promoter_logic.json"
GENOMIC_START = 278021

seq = "".join(FASTA.read_text().splitlines()[1:])
pat = re.compile(r"CGG[ATGC]{11}CCG", re.I)
print("UASg consensus sites (CGGN11CCG):")
for m in pat.finditer(seq):
    g = GENOMIC_START + m.start()
    print(f"  genomic {g + 1}-{g + 15}: {m.group()}")

data = json.loads(JSON.read_text())
print("\nGAL4 hits in parser output (q <= 0.05):")
for s in data["binding_sites"]:
    if s["motif_id"] == "MA0299.1":
        print(
            f"  {s['start']}-{s['stop']} {s['strand']} "
            f"p={s['pvalue']:.2e} q={s['qvalue']:.4f} {s['matched_seq']}"
        )

gal_rels = [
    r for r in data["relationships"]
    if r["site_a"]["motif_id"] == "MA0299.1" and r["site_b"]["motif_id"] == "MA0299.1"
]
print(f"\nGAL4-GAL4 relationships: {len(gal_rels)}")
for r in gal_rels:
    print(f"  {r['logic_type']} dist={r['distance_bp']}bp rule={r['rule_applied']}")

mig_gal = [
    r for r in data["relationships"]
    if {"MA0299.1", "MA0337.2"} == {r["site_a"]["motif_id"], r["site_b"]["motif_id"]}
]
print(f"\nGAL4-MIG1 relationships: {len(mig_gal)}")
for r in mig_gal[:5]:
    print(f"  {r['logic_type']} dist={r['distance_bp']}bp rule={r['rule_applied']}")

print("\nLogic summary:", json.dumps(data["logic_summary"], indent=2))
