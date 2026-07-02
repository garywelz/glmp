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

__version__ = "0.2.2"

# Q-value threshold for confident gate evidence (matches production FIMO filter)
CONFIDENCE_Q_THRESHOLD = 0.05

# Custom PWM motifs from motifs/laci_motif.meme (not in JASPAR CORE).
# FIMO q-values are unreliable for small custom motif sets (pi0 ~ 1);
# use p-value <= CONFIDENCE_Q_THRESHOLD for confidence on these instead.
CUSTOM_PWM_MOTIF_IDS = {
    "LacI_lacO1",
    "TrpR_trpO",
    "LexA_SOS_box",
}


# ── GLMP Grammar Rule Constants ──────────────────────────────────────────────

AND_MIN_BP  = 15    # cooperative binding lower threshold
AND_MAX_BP  = 50    # cooperative binding upper threshold
XOR_MAX_BP  = 15    # steric exclusion threshold
NOT_OVERLAP = 5     # repressor within this many bp of RNAP site = NOT gate

# Known RNAP binding site positions relative to TSS (for E. coli)
# These are approximate; will be refined when real genomic coords are used
RNAP_BINDING_REGION = (-35, -10)   # -35 and -10 elements relative to TSS

# Known repressor TFs — prokaryotic defaults for NOT gate assignment
REPRESSOR_TFS = {
    "LacI", "LacI_lacO1", "TrpR", "AraC_repressor",
    "LexA", "MetJ", "PurR", "CytR",
}

# Known activator TFs — prokaryotic defaults for AND/OR input assignment
ACTIVATOR_TFS = {
    "CRP", "crp", "MA2303.1", "CAP", "AraC_activator",
    "NtrC", "OmpR", "PhoB",
}

ORGANISM_TF_EXTENSIONS = {
    "s_cerevisiae": {
        "repressors": {"MIG1", "MA0337.2"},
        "activators": {"GAL4", "MA0299.1"},
    },
}

# Supported --organism values (RNAP geometry intentionally shared for raw decode)
SUPPORTED_ORGANISMS = {
    "ecoli_k12": {
        "display_name": "Escherichia coli K-12",
        "domain": "prokaryote",
    },
    "s_cerevisiae": {
        "display_name": "Saccharomyces cerevisiae S288C",
        "domain": "eukaryote",
        "decode_warning": (
            "RNAP_BINDING_REGION still uses prokaryotic -35/-10 geometry; "
            "yeast TATA/Inr not modeled (intentional raw decode)"
        ),
    },
    "phage_lambda": {
        "display_name": "Bacteriophage lambda",
        "domain": "bacteriophage",
        "decode_warning": (
            "RNAP_BINDING_REGION uses generic prokaryotic -35/-10 geometry; "
            "lambda PR/PRM and operator-centric windows may not match E. coli sigma70 spacing"
        ),
    },
}


def repressor_tfs_for_organism(organism):
    tfs = set(REPRESSOR_TFS)
    tfs.update(ORGANISM_TF_EXTENSIONS.get(organism, {}).get("repressors", set()))
    return tfs


def activator_tfs_for_organism(organism):
    tfs = set(ACTIVATOR_TFS)
    tfs.update(ORGANISM_TF_EXTENSIONS.get(organism, {}).get("activators", set()))
    return tfs


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
        self.organism     = "unknown_organism"

    def is_repressor(self, organism=None):
        tfs = repressor_tfs_for_organism(organism or self.organism)
        return any(r.lower() in self.motif_id.lower() or
                   r.lower() in self.motif_alt.lower()
                   for r in tfs)

    def is_activator(self, organism=None):
        tfs = activator_tfs_for_organism(organism or self.organism)
        return any(a.lower() in self.motif_id.lower() or
                   a.lower() in self.motif_alt.lower()
                   for a in tfs)

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
            "is_activator":  self.is_activator(),
            "is_custom_pwm": is_custom_pwm_site(self),
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

def load_fimo_tsv(filepath, min_pvalue=0.05):
    """
    Load FIMO TSV output and return list of BindingSite objects.
    Filters by p-value only; q-value filtering happens downstream
    with separate thresholds for repressors vs activators.
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

            # Skip TSV header row
            if parts[0] == 'motif_id':
                continue

            # FIMO TSV columns:
            # motif_id, motif_alt_id, sequence_name, start, stop,
            # strand, score, p-value, q-value, matched_sequence
            try:
                site = BindingSite(
                    motif_id      = parts[0],
                    motif_alt     = parts[1],
                    sequence_name = parts[2],
                    start         = parts[3],
                    stop          = parts[4],
                    strand        = parts[5],
                    score         = parts[6],
                    pvalue        = parts[7],
                    qvalue        = parts[8] if len(parts) > 8 else '.',
                    matched_seq   = parts[9] if len(parts) > 9 else ''
                )

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


def is_custom_pwm_site(site):
    return site.motif_id in CUSTOM_PWM_MOTIF_IDS


def _site_passes_confidence_threshold(site, threshold=CONFIDENCE_Q_THRESHOLD):
    """JASPAR hits use q-value; custom PWM hits use p-value at same cutoff."""
    if is_custom_pwm_site(site):
        return site.pvalue <= threshold
    return site.qvalue <= threshold


def _repressor_site(rel):
    if rel.site_a.is_repressor():
        return rel.site_a
    if rel.site_b.is_repressor():
        return rel.site_b
    return None


def _relationship_involves_known_tf(rel):
    return (
        rel.site_a.is_repressor() or rel.site_a.is_activator()
        or rel.site_b.is_repressor() or rel.site_b.is_activator()
    )


def _relationship_eligible_for_classification(rel, q_threshold=CONFIDENCE_Q_THRESHOLD):
    """Exclude weak repressor-distance NOT hits from classification support."""
    if rel.logic_type == "NOT":
        repressor = _repressor_site(rel)
        if repressor and not _site_passes_confidence_threshold(repressor, q_threshold):
            return False
    return _relationship_involves_known_tf(rel)


def _relationship_is_confident(rel, q_threshold=CONFIDENCE_Q_THRESHOLD):
    if rel.logic_type == "NOT":
        repressor = _repressor_site(rel)
        if repressor:
            return _site_passes_confidence_threshold(repressor, q_threshold)
        return (
            _site_passes_confidence_threshold(rel.site_a, q_threshold)
            and _site_passes_confidence_threshold(rel.site_b, q_threshold)
        )
    if rel.logic_type == "AND":
        known = [
            s for s in (rel.site_a, rel.site_b)
            if s.is_repressor() or s.is_activator()
        ]
        if known:
            return all(_site_passes_confidence_threshold(s, q_threshold) for s in known)
    return (
        _site_passes_confidence_threshold(rel.site_a, q_threshold)
        and _site_passes_confidence_threshold(rel.site_b, q_threshold)
    )


def _proposed_topology_class(has_not, has_and):
    """Map detected gate types to a proposed GLMP circuit class label."""
    if has_not and has_and:
        return "II", ["NOT", "AND"]
    if has_not:
        return "I/II", ["NOT"]
    if has_and:
        return "I", ["AND"]
    return None, []


def _derive_dna_topology_confidence(dna_topology_class, stats, geometry_warning):
    """Map gate evidence to high/medium/partial/insufficient confidence."""
    if dna_topology_class in ("INSUFFICIENT_EVIDENCE", "INDETERMINATE", None):
        return "insufficient"
    if geometry_warning:
        return "partial"
    confident = stats.get("supporting_gates_confident", 0)
    if confident >= 2:
        return "high"
    if confident >= 1:
        return "medium"
    return "partial"


def assess_classification_confidence(relationships, has_not, has_and, organism,
                                     q_threshold=CONFIDENCE_Q_THRESHOLD):
    """
    Check whether gate evidence supports a non-trivial circuit class claim.
    Returns (dna_topology_class, dna_topology_note, dna_topology_confidence, stats).
    """
    proposed_class, supporting_types = _proposed_topology_class(has_not, has_and)
    stats = {
        "proposed_class": proposed_class,
        "supporting_gate_types": supporting_types,
        "supporting_gates_total": 0,
        "supporting_gates_confident": 0,
        "supporting_gates_weak": 0,
        "q_threshold": q_threshold,
    }

    if not proposed_class:
        return None, None, "insufficient", stats

    supporting = [
        r for r in relationships
        if r.logic_type in supporting_types
        and _relationship_eligible_for_classification(r, q_threshold)
    ]
    stats["supporting_gates_total"] = len(supporting)
    if not supporting:
        note = (
            "No supporting gates with confident evidence for known "
            f"transcription factors (JASPAR q<={q_threshold}; custom PWM "
            f"p<={q_threshold})."
        )
        return "INSUFFICIENT_EVIDENCE", note, "insufficient", stats

    confident = [r for r in supporting if _relationship_is_confident(r, q_threshold)]
    weak = len(supporting) - len(confident)
    stats["supporting_gates_confident"] = len(confident)
    stats["supporting_gates_weak"] = weak

    geometry_warning = geometry_warning_for_organism(organism)
    if geometry_warning and proposed_class in ("II", "III", "IV", "V"):
        confident_not = [r for r in confident if r.logic_type == "NOT"]
        if not confident_not:
            note = (
                f"{weak} of {len(supporting)} supporting gates have q-value > "
                f"{q_threshold}. DNA-level evidence insufficient for confident "
                "classification. Manual review recommended."
            )
            return "INSUFFICIENT_EVIDENCE", note, "insufficient", stats

    if weak > len(confident):
        note = (
            f"{weak} of {len(supporting)} supporting gates have q-value > "
            f"{q_threshold}. DNA-level evidence insufficient for confident "
            "classification. Manual review recommended."
        )
        return "INSUFFICIENT_EVIDENCE", note, "insufficient", stats

    topology_confidence = _derive_dna_topology_confidence(
        proposed_class, stats, geometry_warning
    )
    return proposed_class, None, topology_confidence, stats


def geometry_warning_for_organism(organism):
    """Return a warning when promoter geometry assumptions mismatch organism."""
    if organism == "s_cerevisiae":
        return (
            "RNAP binding region geometry is prokaryotic (-35/-10) but organism is "
            "s_cerevisiae. NOT-gate promoter-overlap logic may not apply. "
            "Treat circuit_class with caution."
        )
    if organism == "phage_lambda":
        return (
            "RNAP binding region geometry uses prokaryotic (-35/-10) assumptions but "
            "organism is phage_lambda. Lambda PR/PRM promoter spacing and CI/Cro "
            "operator geometry may not match E. coli sigma70 models. "
            "Treat circuit_class with caution."
        )
    return None


# ── Manifest loader ───────────────────────────────────────────────────────────

def load_manifest(manifest_path):
    """Load YAML manifest with curated biological class metadata."""
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML is required for --manifest. Install with: pip install pyyaml",
              file=sys.stderr)
        sys.exit(1)
    with open(manifest_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _biological_class_fields(manifest_data):
    """Extract glmp_biological_class* fields from manifest (never from FIMO)."""
    if not manifest_data or not manifest_data.get("glmp_biological_class"):
        return {
            "glmp_biological_class": None,
            "glmp_biological_subclass": None,
            "glmp_biological_class_source": None,
            "glmp_biological_class_note": None,
        }
    return {
        "glmp_biological_class": manifest_data.get("glmp_biological_class"),
        "glmp_biological_subclass": manifest_data.get("glmp_biological_subclass"),
        "glmp_biological_class_source": "curated_catalog",
        "glmp_biological_class_note": manifest_data.get("glmp_biological_class_note"),
    }


# ── Circuit Summary Builder ────────────────────────────────────────────────────

def build_circuit_summary(sites, relationships, circuit_name, organism,
                          manifest_data=None):
    """
    Build a structured circuit summary from sites and relationships.
    This is the Stage 3 output — a logical formula for the circuit.
    """

    org_profile = SUPPORTED_ORGANISMS.get(organism, {})

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

    dna_topology_class, dna_topology_note, dna_topology_confidence, confidence_stats = (
        assess_classification_confidence(relationships, has_not, has_and, organism)
    )
    if dna_topology_class is None:
        dna_topology_class = "INDETERMINATE"
    geometry_warning = geometry_warning_for_organism(organism)
    bio_fields = _biological_class_fields(manifest_data)

    summary = {
        "circuit_name":    circuit_name,
        "organism":        organism,
        "decoded_at":      datetime.now().isoformat(),
        "decoder_version": __version__,
        "glmp_version":    "2026-06",
        "dna_topology_class": dna_topology_class,
        "dna_topology_note": dna_topology_note,
        "dna_topology_confidence": dna_topology_confidence,
        **bio_fields,
        "circuit_class":   dna_topology_class,
        "binding_sites": [s.to_dict() for s in sites],
        "relationships": [r.to_dict() for r in relationships],
        "logic_summary": {
            "total_sites":        len(sites),
            "total_relationships": len(relationships),
            "logic_type_counts":  logic_counts,
            "has_not_gate":       has_not,
            "has_and_gate":       has_and,
            "has_or_logic":       has_or,
            "topology_hint":      topology_hint,
            "dna_topology_class": dna_topology_class,
            "dna_topology_note": dna_topology_note,
            "dna_topology_confidence": dna_topology_confidence,
            "classification_confidence": confidence_stats,
        },
    }
    if geometry_warning:
        summary["geometry_warning"] = geometry_warning

    summary["notes"] = [
        "Stage 3 prototype — rule-based logic assignment from spacing geometry",
        "Inter-site distances measured from FIMO hit centers in test sequence",
        "Full genomic coordinates required for precise distance validation",
        "NOT gate confidence requires overlap with RNAP binding site confirmation",
        "Biological validation by molecular biology expert required before"
        " use as training data",
    ] + ([org_profile["decode_warning"]] if org_profile.get("decode_warning") else [])

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
        choices=list(SUPPORTED_ORGANISMS.keys()) + ["unknown_organism"],
        help="Organism identifier: ecoli_k12, s_cerevisiae, or phage_lambda"
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
        help="Maximum q-value for non-repressor FIMO hits (default: 0.1)"
    )
    parser.add_argument(
        "--repressor-qvalue-threshold", type=float, default=None,
        help="Maximum q-value for repressor FIMO hits, applied separately "
             "before the max-sites cap so repressors are always included. "
             "Defaults to --qvalue-threshold if not set. Use 0.9 or 1.0 "
             "for prokaryotic repressors underrepresented in JASPAR."
    )
    parser.add_argument(
        "--max-sites", type=int, default=100,
        help="Maximum non-repressor sites after filtering, sorted by p-value "
             "(default: 100). Repressor sites passing --repressor-qvalue-threshold "
             "are always included on top of this cap."
    )
    parser.add_argument(
        "--manifest", default=None,
        help="YAML manifest with curated glmp_biological_class metadata"
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Print detailed output"
    )

    args = parser.parse_args()

    manifest_data = None
    if args.manifest:
        print(f"Manifest: {args.manifest}")
        manifest_data = load_manifest(args.manifest)

    # Resolve repressor q-value threshold (defaults to general threshold)
    rep_q_thresh = (args.repressor_qvalue_threshold
                    if args.repressor_qvalue_threshold is not None
                    else args.qvalue_threshold)

    print(f"\nGLMP DNA Decoder — Stage 3 Logic Parser v{__version__}")
    print(f"Circuit:  {args.circuit}")
    print(f"Organism: {args.organism}")
    org_profile = SUPPORTED_ORGANISMS.get(args.organism)
    if org_profile:
        print(f"  Domain: {org_profile['domain']}")
        warning = org_profile.get("decode_warning")
        if warning:
            print(f"  WARNING: {warning}")
    print(f"  q-threshold (non-repressors): {args.qvalue_threshold}")
    print(f"  q-threshold (repressors):     {rep_q_thresh}")
    print(f"─" * 50)

    # Load all FIMO hit files
    all_sites = []
    for hit_file in args.hits:
        print(f"\nLoading: {hit_file}")
        sites = load_fimo_tsv(hit_file, min_pvalue=args.pvalue_threshold)
        for site in sites:
            site.organism = args.organism
        all_sites.extend(sites)

    if not all_sites:
        print("\nERROR: No binding sites loaded. Check FIMO output files.",
              file=sys.stderr)
        sys.exit(1)

    print(f"\nTotal sites loaded: {len(all_sites)}")

    # ── Split into repressors and non-repressors, apply separate q-thresholds
    repressor_sites    = [s for s in all_sites if s.is_repressor()]
    nonrepressor_sites = [s for s in all_sites if not s.is_repressor()]

    # Filter repressors by their (looser) threshold
    rep_before = len(repressor_sites)
    repressor_sites = [s for s in repressor_sites if s.qvalue <= rep_q_thresh]
    print(f"Repressor sites (q<={rep_q_thresh}): {len(repressor_sites)} "
          f"(removed {rep_before - len(repressor_sites)})")

    # Filter non-repressors by the standard threshold
    nonrep_before = len(nonrepressor_sites)
    nonrepressor_sites = [s for s in nonrepressor_sites
                          if s.qvalue <= args.qvalue_threshold]
    print(f"Non-repressor sites (q<={args.qvalue_threshold}): "
          f"{len(nonrepressor_sites)} "
          f"(removed {nonrep_before - len(nonrepressor_sites)})")

    # ── Apply max-sites cap to non-repressors only; repressors always included
    if len(nonrepressor_sites) > args.max_sites:
        nonrepressor_sites.sort(key=lambda s: s.pvalue)
        nonrepressor_sites = nonrepressor_sites[:args.max_sites]
        print(f"Non-repressor sites capped at top {args.max_sites} by p-value")

    # Combine: repressors first (guaranteed), then non-repressors
    all_sites = repressor_sites + nonrepressor_sites
    print(f"Total sites for grammar evaluation: {len(all_sites)} "
          f"({len(repressor_sites)} repressors + "
          f"{len(nonrepressor_sites)} non-repressors)")

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
        all_sites, relationships, args.circuit, args.organism, manifest_data
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
    print(f"  DNA topology:     {summary.get('dna_topology_class', ls.get('dna_topology_class'))}")
    print(f"  Topology conf.:   {summary.get('dna_topology_confidence', ls.get('dna_topology_confidence'))}")
    if summary.get("glmp_biological_class"):
        sub = summary.get("glmp_biological_subclass")
        bio = summary["glmp_biological_class"]
        print(f"  Biological class: {bio}{(' / ' + sub) if sub else ''} (curated_catalog)")
    if summary.get("dna_topology_note"):
        print(f"  Topology note:    {summary['dna_topology_note']}")
    if summary.get("geometry_warning"):
        print(f"  Geometry warning: {summary['geometry_warning']}")
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
