#!/usr/bin/env python3
"""
GLMP Validation — Computation Track: RegulonDB cross-reference analysis.

Follows validation/task-brief-computation.md's four-step protocol exactly
(steps 1-3 implemented here; step 4's report is written up separately in
crp_lac_ara_trp_regulondb_validation_report.md, not generated text -- the
findings need to be read and stated, not templated).

Run against local copies of the decoder output (dna-decoder/results/) and
the RegulonDB v14.5.0 flat file already staged locally (.tmp/regulondb-v14/
TF-RISet.tsv) -- both already present, no download needed.
"""

import csv
import json
import sys
from pathlib import Path

GLMP_ROOT = Path(r"C:\Users\garyw\glmp")
RESULTS_DIR = GLMP_ROOT / "collaborations/krampis-virtual-cell/dna-decoder/results"
REGULONDB_TSV = GLMP_ROOT / ".tmp/regulondb-v14/TF-RISet.tsv"

CIRCUITS = {
    "lac": RESULTS_DIR / "ecoli_lac_operon_logic_20260708.json",
    "ara": RESULTS_DIR / "ecoli_ara_operon_logic_20260708.json",
    "trp": RESULTS_DIR / "ecoli_trp_operon_logic_20260708.json",
}

# Decoder motif_id -> RegulonDB tfName. Checked directly against both files
# before writing this map, not assumed: RegulonDB uses "CRP" (there is also
# a distinct "CRP-Sxy" complex, not the same regulator, excluded on purpose).
MOTIF_TO_REGULONDB_TF = {
    "LacI_lacO": "LacI",
    "CRP_CAP": "CRP",
    "TrpR_trpO": "TrpR",
    "AraC_araI": "AraC",  # not present in any decode output -- listed for completeness
}

# Belt-and-suspenders alongside the numeric window below: found (see
# COORD_FRAME note) that the trp decode file's own scanned window
# (1319737-1320275) misses RegulonDB's real trpLp TrpR sites entirely
# (1323103-1323136, ~3.4kb outside the window) -- a second, independent
# coordinate-frame mismatch from the lac one, so restricting the
# false-negative search to a numeric window derived from the decode file's
# own (possibly wrong) coordinates would silently under-report trp's FNs
# the same way pure position-matching under-reported lac's TPs. Anchoring
# by the circuit's real regulated promoter name(s) -- ground truth, not
# derived from the file being validated -- avoids that failure mode.
PROMOTER_ALLOWLIST = {
    "lac": {"lacZp1", "lacZp2", "lacZp3"},
    "ara": {"araBp", "araCp"},
    "trp": {"trpLp"},
}

TOLERANCE_BP = 20

# Added after discovering the lac circuit's decode-file coordinates do not
# share RegulonDB's reference frame (see COORD_FRAME note below): position
# matching alone silently mis-scores real hits as false positives whenever a
# circuit's file has this problem. Sequence identity is ground truth --
# verified by hand against RegulonDB's own tfrsSeq column before trusting it
# as a match criterion -- and is used here as a second, independent check
# whenever position matching fails, not as a replacement for it (ara and trp
# both work correctly under position alone, so both checks are kept and each
# TP is labeled with which one fired).
COMPLEMENT = str.maketrans("ACGTacgt", "TGCAtgca")


def reverse_complement(seq):
    return seq.translate(COMPLEMENT)[::-1]


# "Experimentally validated" per the task brief -- RegulonDB's own column
# doc (line 20 of the header) documents confidenceLevel as spelled-out
# Confirmed/Strong/Weak, but the actual data column uses single-letter
# codes (C/S/W/?) -- confirmed by inspecting real rows before trusting the
# doc string. C/S matches the same "Confirmed or Strong only" convention
# already used in this codebase's own findability_probe.py training filter.
CONFIDENT_LEVELS = {"C", "S"}


# The decoder's own locked operative thresholds are per-motif, not global --
# confirmed directly against motifs/custom_pwm_registry.yaml (not assumed
# from CRP_PWM_BIOLOGIST_REVIEW.md alone, which only documents CRP's own
# lock). An earlier pass of this script applied CRP's 1e-4 lock to every
# motif, which was silently wrong for TrpR (real lock 0.05, an order of
# magnitude looser) and scored trp as having zero threshold-passing
# predictions when several of its raw hits actually clear TrpR's own lock.
# Caught by Cursor reading the registry directly (2026-08-20) and confirmed
# here against the same source before correcting.
MOTIF_PVALUE_THRESHOLD = {
    "LacI_lacO": 1.0e-5,
    "CRP_CAP": 1.0e-4,
    "TrpR_trpO": 0.05,
}


def load_predicted_sites(circuit_key):
    with open(CIRCUITS[circuit_key], encoding="utf-8") as f:
        data = json.load(f)
    all_sites = []
    passing_sites = []
    for s in data.get("binding_sites", []):
        rec = {
            "motif_id": s["motif_id"],
            "start": s["start"],
            "stop": s["stop"],
            "center": s["center"],
            "strand": s["strand"],
            "pvalue": s["pvalue"],
            "qvalue": s["qvalue"],
            "matched_seq": s["matched_seq"],
        }
        all_sites.append(rec)
        threshold = MOTIF_PVALUE_THRESHOLD.get(s["motif_id"])
        if threshold is not None and s["pvalue"] <= threshold:
            passing_sites.append(rec)
    return data, all_sites, passing_sites


def load_regulondb_sites():
    """Parse TF-RISet.tsv, skip the license/comment preamble, return every
    row keyed by tfName with its site window and confidence level."""
    rows = []
    with open(REGULONDB_TSV, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            if line.startswith("1)id"):
                continue  # the pipe-delimited column-index header line
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 27:
                continue
            rows.append(
                {
                    "ri_id": parts[0],
                    "tf_name": parts[3],
                    "tfrs_left": parts[6],
                    "tfrs_right": parts[7],
                    "strand": parts[8],
                    "tfrs_seq": parts[9],
                    "ri_function": parts[10],
                    "promoter_name": parts[12],
                    "target": parts[18],
                    "confidence": parts[19],
                }
            )
    return rows


def to_int_or_none(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def main():
    regulondb_rows = load_regulondb_sites()
    print(f"Loaded {len(regulondb_rows)} total RegulonDB TF-RISet rows.")
    confident_rows = [r for r in regulondb_rows if r["confidence"] in CONFIDENT_LEVELS]
    print(f"Of those, {len(confident_rows)} are Confirmed or Strong (experimentally validated).")

    report = {}

    for circuit_key in CIRCUITS:
        decode_data, all_sites, predicted = load_predicted_sites(circuit_key)
        print(f"\n=== {circuit_key} ({decode_data['circuit_name']}) ===")
        thresholds_used = sorted({MOTIF_PVALUE_THRESHOLD[m] for m in set(s["motif_id"] for s in all_sites) if m in MOTIF_PVALUE_THRESHOLD})
        print(f"Raw FIMO hits: {len(all_sites)}  |  Passing per-motif locked threshold ({thresholds_used}): {len(predicted)}")

        # Window is based on the full raw scan (all_sites), not just the
        # threshold-passing subset -- this is what the decoder actually
        # looked at, and trp has zero passing sites but was still scanned.
        if all_sites:
            window_start = min(s["start"] for s in all_sites) - 20
            window_stop = max(s["stop"] for s in all_sites) + 20
        else:
            window_start = window_stop = None
        print(f"Decoder-scanned genomic window: {window_start}-{window_stop}")

        # RegulonDB rows for TFs actually relevant to this circuit's motifs,
        # restricted to the genomic window the decoder actually scanned --
        # a genome-wide CRP or LacI comparison would pull in >100 unrelated
        # promoters and produce a meaningless recall number.
        relevant_tf_names = {
            MOTIF_TO_REGULONDB_TF[m]
            for m in set(s["motif_id"] for s in all_sites) | {"AraC_araI"}
            if m in MOTIF_TO_REGULONDB_TF
        }
        if circuit_key == "ara":
            relevant_tf_names.add("AraC")  # always check for AraC here even if 0 predicted

        allowed_promoters = PROMOTER_ALLOWLIST.get(circuit_key, set())
        validated_in_window = []
        promoter_rescued_ids = set()
        for r in confident_rows:
            if r["tf_name"] not in relevant_tf_names:
                continue
            left = to_int_or_none(r["tfrs_left"])
            right = to_int_or_none(r["tfrs_right"])
            in_window = (
                left is not None and right is not None and window_start is not None
                and (window_start <= left <= window_stop or window_start <= right <= window_stop)
            )
            in_promoter = r["promoter_name"] in allowed_promoters
            if not (in_window or in_promoter):
                continue
            validated_in_window.append(r)
            if in_promoter and not in_window:
                promoter_rescued_ids.add(r["ri_id"])

        print(f"RegulonDB Confirmed/Strong sites for {sorted(relevant_tf_names)} in this window: {len(validated_in_window)}")
        if promoter_rescued_ids:
            print(f"  (of which {len(promoter_rescued_ids)} fall outside the decode file's own scanned window but are "
                  f"included by promoter name -- see COORD_FRAME note; the window itself may be shifted for this circuit)")

        # --- overlap analysis ---
        # Two independent match tests, tried in order. Position is tried
        # first (it's what the task brief specifies); sequence identity is
        # the fallback for a circuit whose decode file turns out not to
        # share RegulonDB's coordinate frame (found: true for lac, not for
        # ara/trp -- see coord_frame_flags below).
        true_positives = []
        false_positives = []
        matched_regulondb_ids = set()
        coord_frame_flags = []  # sequence-only matches: decode coords disagree with RegulonDB's

        for p in predicted:
            tf = MOTIF_TO_REGULONDB_TF.get(p["motif_id"])
            pos_match = None
            seq_match = None
            p_seq = p["matched_seq"].upper()
            p_seq_rc = reverse_complement(p_seq)
            for r in validated_in_window:
                if r["tf_name"] != tf:
                    continue
                left, right = to_int_or_none(r["tfrs_left"]), to_int_or_none(r["tfrs_right"])
                if left is not None and right is not None:
                    r_center = (left + right) / 2.0
                    if abs(p["center"] - r_center) <= TOLERANCE_BP:
                        pos_match = r
                        break
                r_seq = r["tfrs_seq"].upper()
                if r_seq and (p_seq in r_seq or p_seq_rc in r_seq):
                    seq_match = r

            if pos_match:
                true_positives.append((p, pos_match, "position"))
                matched_regulondb_ids.add(pos_match["ri_id"])
            elif seq_match:
                true_positives.append((p, seq_match, "sequence-only"))
                matched_regulondb_ids.add(seq_match["ri_id"])
                coord_frame_flags.append((p, seq_match))
            else:
                false_positives.append(p)

        false_negatives = [r for r in validated_in_window if r["ri_id"] not in matched_regulondb_ids]

        print(f"True positives:  {len(true_positives)}")
        print(f"False positives: {len(false_positives)}")
        print(f"False negatives: {len(false_negatives)}")

        for p, r, how in true_positives:
            print(f"  TP ({how}): {p['motif_id']} @ {p['start']}-{p['stop']} <-> RegulonDB {r['ri_id']} "
                  f"({r['promoter_name']}, {r['tfrs_left']}-{r['tfrs_right']}, conf={r['confidence']}, "
                  f"fn={r['ri_function']})  |  q={p['qvalue']:.3g}")
        for p in false_positives:
            print(f"  FP: {p['motif_id']} @ {p['start']}-{p['stop']}  matched_seq={p['matched_seq']}  q={p['qvalue']:.3g}")
        for r in false_negatives:
            print(f"  FN: RegulonDB {r['ri_id']} {r['tf_name']} @ {r['tfrs_left']}-{r['tfrs_right']} "
                  f"({r['promoter_name']}, conf={r['confidence']}, fn={r['ri_function']}, target={r['target']})")

        if coord_frame_flags:
            print(f"  COORD-FRAME FLAG: {len(coord_frame_flags)} true positive(s) in this circuit matched by "
                  f"sequence identity only -- decode-file genomic coordinates disagree with RegulonDB's for "
                  f"this circuit specifically (see notebook entry, not a real false-positive/negative issue).")
            for p, r in coord_frame_flags:
                left = to_int_or_none(r["tfrs_left"])
                offset = p["start"] - left if left is not None else None
                print(f"    decode {p['start']}-{p['stop']} vs RegulonDB {r['ri_id']} {r['tfrs_left']}-{r['tfrs_right']}  "
                      f"(offset={offset})")

        report[circuit_key] = {
            "predicted_count": len(predicted),
            "regulondb_validated_count": len(validated_in_window),
            "true_positives": len(true_positives),
            "false_positives": len(false_positives),
            "false_negatives": len(false_negatives),
            "tp_detail": [
                {
                    "motif_id": p["motif_id"], "start": p["start"], "stop": p["stop"],
                    "regulondb_id": r["ri_id"], "promoter": r["promoter_name"],
                    "regulondb_range": f"{r['tfrs_left']}-{r['tfrs_right']}",
                    "confidence": r["confidence"], "function": r["ri_function"],
                    "matched_by": how,
                }
                for p, r, how in true_positives
            ],
            "coord_frame_flags": [
                {
                    "motif_id": p["motif_id"], "decode_range": f"{p['start']}-{p['stop']}",
                    "regulondb_id": r["ri_id"], "regulondb_range": f"{r['tfrs_left']}-{r['tfrs_right']}",
                    "offset": (p["start"] - to_int_or_none(r["tfrs_left"])) if to_int_or_none(r["tfrs_left"]) is not None else None,
                }
                for p, r in coord_frame_flags
            ],
            "fp_detail": [
                {"motif_id": p["motif_id"], "start": p["start"], "stop": p["stop"], "qvalue": p["qvalue"]}
                for p in false_positives
            ],
            "fn_detail": [
                {
                    "regulondb_id": r["ri_id"], "tf_name": r["tf_name"],
                    "range": f"{r['tfrs_left']}-{r['tfrs_right']}", "promoter": r["promoter_name"],
                    "confidence": r["confidence"], "function": r["ri_function"], "target": r["target"],
                }
                for r in false_negatives
            ],
        }

    total_tp = sum(c["true_positives"] for c in report.values())
    total_fp = sum(c["false_positives"] for c in report.values())
    total_fn = sum(c["false_negatives"] for c in report.values())
    total_predicted = sum(c["predicted_count"] for c in report.values())
    total_validated = sum(c["regulondb_validated_count"] for c in report.values())

    print("\n=== TOTALS ===")
    print(f"Predicted sites: {total_predicted}  RegulonDB validated (in-window): {total_validated}")
    print(f"TP={total_tp} FP={total_fp} FN={total_fn}")
    precision = (total_tp / total_predicted * 100) if total_predicted else 0.0
    recall = (total_tp / total_validated * 100) if total_validated else 0.0
    print(f"Precision: {precision:.1f}%   Recall: {recall:.1f}%")

    out_path = Path(__file__).parent / "regulondb_crossref_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "report": report,
                "totals": {
                    "predicted": total_predicted, "regulondb_validated": total_validated,
                    "true_positives": total_tp, "false_positives": total_fp, "false_negatives": total_fn,
                    "precision_pct": round(precision, 1), "recall_pct": round(recall, 1),
                },
            },
            f, indent=2,
        )
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    sys.exit(main())
