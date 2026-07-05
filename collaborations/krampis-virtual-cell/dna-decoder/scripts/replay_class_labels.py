#!/usr/bin/env python3
"""Replay classification on existing decode JSON (no re-decode)."""
import json
import sys

sys.path.insert(0, "/media/sdcard/glmp/collaborations/krampis-virtual-cell/dna-decoder")
from glmp_logic_parser import (
    BindingSite,
    LogicalRelationship,
    assess_classification_confidence,
    _topology_gate_flags,
    _eligible_relationships,
    CONFIDENCE_Q_THRESHOLD,
)

RESULTS = "/media/sdcard/glmp/collaborations/krampis-virtual-cell/dna-decoder/results"

FILES = [
    ("lac", f"{RESULTS}/lac_operon_logic_v2.json"),
    ("ara", f"{RESULTS}/ara_operon_logic_v3.json"),
    ("trp", f"{RESULTS}/trp_operon_logic_v4.json"),
    ("sos_lexa", f"{RESULTS}/ecoli_sos_lexa_logic_20260702.json"),
    ("sos_reca", f"{RESULTS}/ecoli_sos_reca_logic_20260702.json"),
    ("flhdc", f"{RESULTS}/ecoli_flhdc_flagellar_logic_20260701.json"),
    ("lambda", f"{RESULTS}/ecoli_lambda_switch_logic_20260703.json"),
    ("dna_damage", f"{RESULTS}/ecoli_dna_damage_checkpoint_logic_20260705.json"),
]


def load_json(path):
    with open(path) as f:
        return json.load(f)


def rebuild(data):
    site_index = {}
    sites = []
    for s in data["binding_sites"]:
        bs = BindingSite(
            motif_id=s["motif_id"],
            motif_alt=s.get("motif_alt", s["motif_id"]),
            sequence_name="replay",
            start=s["start"],
            stop=s["stop"],
            strand=s.get("strand", "+"),
            score=s.get("score", 0),
            pvalue=s.get("pvalue", 1),
            qvalue=s.get("qvalue", 1),
            matched_seq=s.get("matched_seq", ""),
        )
        bs.organism = data.get("organism", "ecoli_k12")
        key = (s["motif_id"], s["start"], s["stop"])
        site_index[key] = bs
        sites.append(bs)

    rels = []
    for r in data["relationships"]:
        pos_a = r["site_a_pos"].replace("\u2013", "-").split("-")
        pos_b = r["site_b_pos"].replace("\u2013", "-").split("-")
        sa = site_index[(r["site_a"], int(pos_a[0]), int(pos_a[1]))]
        sb = site_index[(r["site_b"], int(pos_b[0]), int(pos_b[1]))]
        rels.append(
            LogicalRelationship(
                site_a=sa,
                site_b=sb,
                distance_bp=r["distance_bp"],
                logic_type=r["logic_type"],
                confidence=r.get("confidence", "medium"),
                rule_applied=r.get("rule_applied", ""),
                notes=r.get("notes", ""),
            )
        )
    return rels


def reason_text(has_not, has_and, eligible, predicted, note):
    e_not = sum(1 for r in eligible if r.logic_type == "NOT")
    e_and = sum(1 for r in eligible if r.logic_type == "AND")
    if predicted == "II":
        return f"eligible NOT={e_not}, eligible AND={e_and} -> Class II"
    if predicted == "I/II":
        return f"eligible NOT={e_not}, eligible AND=0 (no activator AND) -> repression-only I/II"
    if predicted == "I":
        return f"eligible AND={e_and}, no eligible NOT -> activation-only I"
    if predicted == "INSUFFICIENT_EVIDENCE":
        if note:
            return note
        return f"eligible NOT={e_not}, eligible AND={e_and}; zero confident TF gates"
    if predicted == "INDETERMINATE":
        return note or "confident OR/XOR with known TF; no NOT/AND resolution"
    return note or ""


print("circuit|old_class|predicted_class|eligible_not|eligible_and|reason")
for label, path in FILES:
    data = load_json(path)
    rels = rebuild(data)
    has_not, has_and = _topology_gate_flags(rels)
    eligible = _eligible_relationships(rels)
    new_cls, note, conf, stats = assess_classification_confidence(
        rels, has_not, has_and, data.get("organism", "ecoli_k12")
    )
    old = data.get("dna_topology_class")
    reason = reason_text(has_not, has_and, eligible, new_cls, note)
    print(
        f"{label}|{old}|{new_cls}|"
        f"{sum(1 for r in eligible if r.logic_type=='NOT')}|"
        f"{sum(1 for r in eligible if r.logic_type=='AND')}|"
        f"{reason}"
    )

print("\nClass II count:", end=" ")
count_ii = 0
for label, path in FILES:
    data = load_json(path)
    rels = rebuild(data)
    hn, ha = _topology_gate_flags(rels)
    nc, *_ = assess_classification_confidence(rels, hn, ha, data.get("organism", "ecoli_k12"))
    if nc == "II":
        count_ii += 1
        print(label, end=" ")
print(count_ii)
