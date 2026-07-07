#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "results" / "lac_operon_logic_guardrail.json"
d = json.loads(path.read_text(encoding="utf-8"))
rels = d["relationships"]
not_rels = [r for r in rels if r["logic_type"] == "NOT"]
print("NOT total", len(not_rels))
print("NOT rules", Counter(r["rule_applied"] for r in not_rels))
lac_not = [r for r in not_rels if "LacI" in r["site_a"] or "LacI" in r["site_b"]]
print("LacI NOT", len(lac_not))
print("LacI overlap", sum(1 for r in lac_not if r["rule_applied"] == "repressor_overlaps_target"))

sites = {s["motif_id"]: s for s in d["binding_sites"]}
for mid in ("LacI_lacO1", "MA2303.1"):
    if mid in sites:
        print(mid, "q=", sites[mid]["qvalue"])
