#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "results"
PAIRS = [
    ("lac_operon_logic_v2.json", "lac_operon_logic_guardrail.json"),
    ("ara_operon_logic.json", "ara_operon_logic_guardrail.json"),
    ("trp_operon_logic_v3.json", "trp_operon_logic_guardrail.json"),
]


def summarize(path):
    if not path.exists():
        return {"missing": str(path)}
    d = json.loads(path.read_text(encoding="utf-8"))
    ls = d.get("logic_summary", {})
    return {
        "topology_hint": ls.get("topology_hint"),
        "circuit_class": d.get("circuit_class", ls.get("circuit_class")),
        "circuit_class_note": d.get("circuit_class_note"),
        "geometry_warning": d.get("geometry_warning"),
    }


for baseline_name, guardrail_name in PAIRS:
    print(f"=== {baseline_name} vs {guardrail_name} ===")
    b = summarize(ROOT / baseline_name)
    g = summarize(ROOT / guardrail_name)
    print("baseline:", b)
    print("guardrail:", g)
    if b.get("topology_hint") != g.get("topology_hint"):
        print("REGRESSION: topology_hint changed")
    print()

print("=== gal1_promoter_logic_v2.json ===")
print(summarize(ROOT / "gal1_promoter_logic_v2.json"))
