#!/usr/bin/env python3
"""Summarize dna_topology_class from latest logic JSONs."""
import json
import sys
from pathlib import Path

RES = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("results")
DATE = sys.argv[2] if len(sys.argv) > 2 else "20260708"
CIRCUITS = [
    "ecoli_lac_operon", "ecoli_ara_operon", "ecoli_trp_operon",
    "ecoli_sos_lexa", "ecoli_sos_reca", "ecoli_flhdc_flagellar",
    "ecoli_lambda_switch", "ecoli_dna_damage_checkpoint",
]

for cid in CIRCUITS:
    files = sorted(RES.glob(f"{cid}_logic_{DATE}*.json"))
    if not files:
        print(f"{cid}|MISSING")
        continue
    d = json.loads(files[-1].read_text(encoding="utf-8"))
    rels = d.get("relationships", [])
    lac_not = [
        r for r in rels
        if r.get("logic_type") == "NOT"
        and any(x in r.get("site_a", "") + r.get("site_b", "")
                for x in ("LacI", "TrpR"))
    ]
    laci = sum(1 for r in lac_not if "LacI" in r.get("site_a", "") + r.get("site_b", ""))
    trpr = sum(1 for r in lac_not if "TrpR" in r.get("site_a", "") + r.get("site_b", ""))
    print(
        f"{cid}|{d.get('dna_topology_class')}|{d.get('glmp_biological_class')}|"
        f"laci_not={laci}|trpr_not={trpr}|total_not={len([r for r in rels if r.get('logic_type')=='NOT'])}"
    )
