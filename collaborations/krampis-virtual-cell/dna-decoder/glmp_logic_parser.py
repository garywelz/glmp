#!/usr/bin/env python3.8
"""
GLMP DNA Decoder — Stage 3 Logic Parser
========================================
Takes FIMO motif scan output (TSV) and applies GLMP grammar rules
to assign logical types to binding site relationships.

GLMP Grammar Rules (from Papers I & II):
  - AND (cooperative):     inter-site distance 15–50 bp
  - XOR (competitive):     inter-site distance < 15 bp
  - OR (independent):      inter-site distance > 50 bp
  - NOT (repression):      repressor site overlapping or adjacent to RNAP site
  - FEEDBACK:              TF product regulates its own gene

Usage:
  python3.8 glmp_logic_parser.py \
    --hits results/lac_test/fimo.tsv results/lac_test2/fimo.tsv \
    --sequence sequences/lac_operon_region.fa \
    --circuit lac_operon \
    --organism ecoli_k12 \
    --output results/lac_operon_logic.json

Author: Gary Welz, GLMP / CUNY Graduate Center
Date: June 2026
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime


# ── GLMP Grammar Rule Constants ──────────────────────────────────────────────

AND_MIN_BP  = 15    # cooperative binding lower threshold
AND_MAX_BP  = 50    # cooperative binding upper threshold
XOR_MAX_BP  = 15    # steric exclusion threshold
NOT_OVERLAP = 5     # repressor within this many bp of RNAP site = NOT gate

# Known RNAP binding site positions relative to TSS (for E. coli)
# These are approximate; will be refined when real genomic coords are used
RNAP_BINDING_REGION = (-35, -10)   # -35 and -10 elements relative to TSS

# Known repressor TFs — these are candidates for NOT gate assignment
REPRESSOR_TFS = {
    "LacI", "LacI_lacO1", "TrpR", "AraC_repressor",
    "LexA", "MetJ", "PurR", "CytR"
}

# Known activator TFs — these are candidates for AND/OR input assignment
ACTIVATOR_TFS = {
    "CRP", "crp", "MA2303.1", "CAP", "AraC_activator",
    "NtrC", "OmpR", "PhoB"
}


# ── Data Classes ─────────────────────────────────────────────────────────────

class BindingSite:
    """Represents a single TF binding site hit from FIMO."""

    def __init__(self, motif_id, motif_alt, sequence_name,
                 start, stop, strand, score, pvalue, qvalue, matched_seq):
        self.motif_id     = motif_id
        self.motif_alt    = motif_alt
        self.sequence_name = sequence_name
        self.start        = int(start)
        self.stop         = int(stop)
        self.strand       = strand
        self.score        = float(score) if score != '.' else 0.0
        self.pvalue       = float(pvalue)
        self.qvalue       = float(qvalue) if qvalue != '.' else 1.0
        self.matched_seq  = matched_seq
        self.center       = (self.start + self.stop) / 2
        self.length       = self.stop - self.start + 1

    def is_repressor(self):
        return any(r.lower() in self.motif_id.lower() or
                   r.lower() in self.motif_alt.lower()
                   for r in REPRESSOR_TFS)

    def is_activator(self):
        return any(a.lower() in self.motif_id.lower() or
                   a.lower() in self.motif_alt.lower()
                   for a in ACTIVATOR_TFS)

    def to_dict(self):
        return {
            "motif_id":      self.motif_id,
            "motif_alt":     self.motif_alt,
            "start":         self.start,
            "stop":          self.stop,
            "strand":        self.strand,
            "score":         self.score,
            "pvalue":        self.pvalue,
            "qvalue":        self.qvalue,
            "matched_seq":   self.matched_seq,
            "center":        self.center,
            "length":        self.length,
            "is_repressor":  self.is_repressor(),
            "is_activator":  self.is_activator()
        }


class LogicalRelationship:
    """Represents a logical relationship between two binding sites."""

    def __init__(self, site_a, site_b, distance_bp, logic_type,
                 confidence, rule_applied, notes=""):
        self.site_a        = site_a
        self.site_b        = site_b
        self.distance_bp   = distance_bp
        self.logic_type    = logic_type      # AND, OR, XOR, NOT, FEEDBACK
        self.confidence    = confidence      # high, medium, low
        self.rule_applied  = rule_applied    # which GLMP rule fired
        self.notes         = notes

    def to_dict(self):
        return {
            "site_a":        self.site_a.motif_id,
            "site_b":        self.site_b.motif_id,
            "site_a_pos":    f"{self.site_a.start}–{self.site_a.stop}",
            "site_b_pos":    f"{self.site_b.start}–{self.site_b.stop}",
            "distance_bp":   round(self.distance_bp),
            "logic_type":    self.logic_type,
            "confidence":    self.confidence,
            "rule_applied":  self.rule_applied,
            "notes":         self.notes
        }


# ── FIMO Parser ───────────────────────────────────────────────────────────────

def load_fimo_tsv(filepath, min_pvalue=0.05, min_qvalue=0.5):
    """
    Load FIMO TSV output and return list of BindingSite objects.
    Filters out weak hits by default.
    """
    sites = []

    if not os.path.exists(filepath):
        print(f"  WARNING: FIMO file not found: {filepath}", file=sys.stderr)
        return sites

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split('\t')
            if len(parts) < 9:
                continue

            # FIMO TSV columns:
            # motif_id, motif_alt_id, sequence_name, start, stop,
            # strand, score, p-value, q-value, matched_sequence
            try:
                site = BindingSite(
                    motif_id     = parts[0],
                    motif_alt    = parts[1],
                    sequence_name = parts[2],
                    start        = parts[3],
                    stop         = parts[4],
                    strand       = parts[5],
                    score        = parts[6],
                    pvalue       = parts[7],
                    qvalue       = parts[8] if len(parts) > 8 else '.',
                    matched_seq  = parts[9] if len(parts) > 9 else ''
                )

                # Filter weak hits
                if site.pvalue <= min_pvalue:
                    sites.append(site)

            except (ValueError, IndexError) as e:
                print(f"  WARNING: Could not parse line: {line[:80]}... ({e})",
                      file=sys.stderr)
                continue

    print(f"  Loaded {len(sites)} hits from {os.path.basename(filepath)}")
    return sites


# ── GLMP Grammar Rule Engine ──────────────────────────────────────────────────

def calculate_distance(site_a, site_b):
    """Calculate center-to-center distance between two binding sites."""
    return abs(site_a.center - site_b.center)


def apply_grammar_rules(sites):
    """
    Apply GLMP grammar rules to a list of binding sites.
    Returns list of LogicalRelationship objects.
    """
    relationships = []

    if len(sites) < 2:
        print("  Only one site — no pairwise relationships to evaluate.")
        return relationships

    # Evaluate all pairs
    for i in range(len(sites)):
        for j in range(i + 1, len(sites)):
            site_a = sites[i]
            site_b = sites[j]

            distance = calculate_distance(site_a, site_b)

            logic_type   = None
            confidence   = None
            rule_applied = None
            notes        = ""

            # ── Rule 1: NOT gate ─────────────────────────────────────────────
            # Repressor binding site overlapping or adjacent to RNAP binding
            # site blocks transcription initiation
            if site_a.is_repressor() or site_b.is_repressor():
                repressor = site_a if site_a.is_repressor() else site_b
                other     = site_b if site_a.is_repressor() else site_a

                # Check for overlap (distance < half the length of smaller site)
                min_half_len = min(repressor.length, other.length) / 2
                if distance < min_half_len + NOT_OVERLAP:
                    logic_type   = "NOT"
                    confidence   = "high"
                    rule_applied = "repressor_overlaps_target"
                    notes = (f"{repressor.motif_id} binding blocks access "
                             f"at distance {round(distance)} bp")
                else:
                    # Repressor present but not overlapping — still a NOT gate
                    # at the circuit level, just not via steric overlap
                    logic_type   = "NOT"
                    confidence   = "medium"
                    rule_applied = "repressor_site_present"
                    notes = (f"{repressor.motif_id} represses at "
                             f"{round(distance)} bp from {other.motif_id}")

            # ── Rule 2: XOR / competitive exclusion ──────────────────────────
            # Two activators within <15 bp sterically exclude each other
            elif distance < XOR_MAX_BP:
                logic_type   = "XOR"
                confidence   = "medium"
                rule_applied = "steric_exclusion_distance"
                notes = (f"Distance {round(distance)} bp < {XOR_MAX_BP} bp "
                         f"threshold — competitive binding")

            # ── Rule 3: AND / cooperative binding ────────────────────────────
            # Two sites within 15–50 bp cooperate to produce strong output
            elif AND_MIN_BP <= distance <= AND_MAX_BP:
                logic_type   = "AND"
                confidence   = "medium"
                rule_applied = "cooperative_spacing_distance"
                notes = (f"Distance {round(distance)} bp within "
                         f"{AND_MIN_BP}–{AND_MAX_BP} bp cooperative range")

            # ── Rule 4: OR / independent action ──────────────────────────────
            # Two sites > 50 bp apart act independently
            elif distance > AND_MAX_BP:
                logic_type   = "OR_INDEPENDENT"
                confidence   = "low"
                rule_applied = "independent_spacing_distance"
                notes = (f"Distance {round(distance)} bp > {AND_MAX_BP} bp "
                         f"— independent action; AND logic may emerge "
                         f"from promoter architecture, not spacing geometry")

            if logic_type:
                rel = LogicalRelationship(
                    site_a       = site_a,
                    site_b       = site_b,
                    distance_bp  = distance,
                    logic_type   = logic_type,
                    confidence   = confidence,
                    rule_applied = rule_applied,
                    notes        = notes
                )
                relationships.append(rel)

    return relationships


# ── Circuit Summary Builder ────────────────────────────────────────────────────

def build_circuit_summary(sites, relationships, circuit_name, organism):
    """
    Build a structured circuit summary from sites and relationships.
    This is the Stage 3 output — a logical formula for the circuit.
    """

    # Count logical types
    logic_counts = {}
    for rel in relationships:
        logic_counts[rel.logic_type] = logic_counts.get(rel.logic_type, 0) + 1

    # Identify the dominant logic pattern
    has_not  = "NOT" in logic_counts
    has_and  = "AND" in logic_counts
    has_or   = "OR_INDEPENDENT" in logic_counts

    # Build circuit class hint based on topology
    # (Full class assignment requires loop detection — simplified here)
    if has_not and has_and:
        topology_hint = "Class II candidate — negative feedback with AND gate"
    elif has_not and not has_and:
        topology_hint = "Class I/II candidate — repression present"
    elif has_and and not has_not:
        topology_hint = "Class I candidate — combinatorial activation"
    else:
        topology_hint = "Indeterminate — insufficient topology signal"

    summary = {
        "circuit_name":    circuit_name,
        "organism":        organism,
        "decoded_at":      datetime.now().isoformat(),
        "decoder_version": "0.1.0-prototype",
        "glmp_version":    "2026-06",
        "binding_sites": [s.to_dict() for s in sites],
        "relationships": [r.to_dict() for r in relationships],
        "logic_summary": {
            "total_sites":        len(sites),
            "total_relationships": len(relationships),
            "logic_type_counts":  logic_counts,
            "has_not_gate":       has_not,
            "has_and_gate":       has_and,
            "has_or_logic":       has_or,
            "topology_hint":      topology_hint
        },
        "notes": [
            "Stage 3 prototype — rule-based logic assignment from spacing geometry",
            "Inter-site distances measured from FIMO hit centers in test sequence",
            "Full genomic coordinates required for precise distance validation",
            "NOT gate confidence requires overlap with RNAP binding site confirmation",
            "Biological validation by molecular biology expert required before"
            " use as training data"
        ]
    }

    return summary


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="GLMP Stage 3 Logic Parser — assigns logical types to "
                    "FIMO binding site hits using GLMP grammar rules"
    )
    parser.add_argument(
        "--hits", nargs="+", required=True,
        help="One or more FIMO TSV output files"
    )
    parser.add_argument(
        "--circuit", default="unknown_circuit",
        help="Circuit name (e.g. lac_operon)"
    )
    parser.add_argument(
        "--organism", default="unknown_organism",
        help="Organism identifier (e.g. ecoli_k12)"
    )
    parser.add_argument(
        "--output", default=None,
        help="Output JSON file path (default: <circuit>_logic.json)"
    )
    parser.add_argument(
        "--pvalue-threshold", type=float, default=0.05,
        help="Maximum p-value for FIMO hits to include (default: 0.05)"
    )
    parser.add_argument(
        "--qvalue-threshold", type=float, default=0.1,
        help="Maximum q-value for FIMO hits to include (default: 0.1)"
    )
    parser.add_argument(
        "--max-sites", type=int, default=100,
        help="Maximum sites after filtering, sorted by p-value (default: 100)"
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Print detailed output"
    )

    args = parser.parse_args()

    print(f"\nGLMP DNA Decoder — Stage 3 Logic Parser")
    print(f"Circuit:  {args.circuit}")
    print(f"Organism: {args.organism}")
    print(f"─" * 50)

    # Load all FIMO hit files
    all_sites = []
    for hit_file in args.hits:
        print(f"\nLoading: {hit_file}")
        sites = load_fimo_tsv(hit_file, min_pvalue=args.pvalue_threshold)
        all_sites.extend(sites)

    if not all_sites:
        print("\nERROR: No binding sites loaded. Check FIMO output files.",
              file=sys.stderr)
        sys.exit(1)

    print(f"\nTotal sites loaded: {len(all_sites)}")

    # Apply q-value filter
    before = len(all_sites)
    all_sites = [s for s in all_sites if s.qvalue <= args.qvalue_threshold]
    print(f"After q-value filter (q<={args.qvalue_threshold}): {len(all_sites)} sites (removed {before - len(all_sites)})")

    # Apply max-sites cap — keep top hits by p-value
    if len(all_sites) > args.max_sites:
        all_sites.sort(key=lambda s: s.pvalue)
        all_sites = all_sites[:args.max_sites]
        print(f"Capped at top {args.max_sites} sites by p-value")

    # Sort sites by position for relationship evaluation
    all_sites.sort(key=lambda s: s.start)

    if args.verbose:
        print("\nBinding sites (sorted by position):")
        for s in all_sites:
            flag = "[REP]" if s.is_repressor() else "[ACT]" if s.is_activator() else "     "
            print(f"  {flag} {s.motif_id:30s} pos {s.start:4d}–{s.stop:4d} "
                  f"strand {s.strand}  p={s.pvalue:.2e}  seq={s.matched_seq}")

    # Apply grammar rules
    print(f"\nApplying GLMP grammar rules...")
    relationships = apply_grammar_rules(all_sites)

    print(f"Relationships found: {len(relationships)}")

    if args.verbose:
        print("\nLogical relationships:")
        for rel in relationships:
            print(f"  [{rel.logic_type:15s}] "
                  f"{rel.site_a.motif_id:25s} ↔ {rel.site_b.motif_id:25s} "
                  f"dist={round(rel.distance_bp):4d} bp  "
                  f"conf={rel.confidence}  rule={rel.rule_applied}")

    # Build circuit summary
    summary = build_circuit_summary(
        all_sites, relationships, args.circuit, args.organism
    )

    # Print logic summary
    print(f"\n{'─'*50}")
    print(f"CIRCUIT LOGIC SUMMARY: {args.circuit}")
    print(f"{'─'*50}")
    ls = summary["logic_summary"]
    print(f"  Binding sites:    {ls['total_sites']}")
    print(f"  Relationships:    {ls['total_relationships']}")
    print(f"  NOT gates:        {'YES' if ls['has_not_gate'] else 'no'}")
    print(f"  AND gates:        {'YES' if ls['has_and_gate'] else 'no'}")
    print(f"  OR logic:         {'YES' if ls['has_or_logic'] else 'no'}")
    print(f"  Topology hint:    {ls['topology_hint']}")
    print(f"\n  Logic type counts:")
    for ltype, count in ls['logic_type_counts'].items():
        print(f"    {ltype:20s}: {count}")

    # Write output JSON
    output_path = args.output or f"{args.circuit}_logic.json"
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\nOutput written to: {output_path}")
    print(f"Done.\n")


if __name__ == "__main__":
    main()
