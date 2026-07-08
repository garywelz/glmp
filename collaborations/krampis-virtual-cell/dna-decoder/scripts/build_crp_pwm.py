#!/usr/bin/env python3
"""
build_crp_pwm.py — Stage 1: CRP/CAP PWM from RegulonDB v14.5 TF-RISet.

Builds a non-circular custom PWM (training sites only), validates with FIMO,
locks a significance threshold from controls — does NOT touch the decoder parser.
"""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
DECODER_DIR = SCRIPT_DIR.parent
MOTIFS_DIR = DECODER_DIR / "motifs"
QUEUE_COMPLETED = DECODER_DIR / "queue" / "completed"
SEQUENCES_DIR = DECODER_DIR / "sequences"
VALIDATION_DIR = DECODER_DIR / "_crp_pwm_validation"  # gitignored scratch

REGULONDB_DEFAULT = Path("/tmp/regulondb-v14/TF-RISet.tsv")
GCS_REGULONDB_PREFIX = "validation/regulondb-v14/TF-RISet.tsv"

REGRESSION_CIRCUITS = [
    "ecoli_lac_operon",
    "ecoli_ara_operon",
    "ecoli_trp_operon",
    "ecoli_sos_lexa",
    "ecoli_sos_reca",
    "ecoli_flhdc_flagellar",
    "ecoli_lambda_switch",
    "ecoli_dna_damage_checkpoint",
]

# Promoter / gene scope for holdout beyond strict coordinate overlap.
CIRCUIT_SCOPE: Dict[str, Dict[str, List[str]]] = {
    "ecoli_lac_operon": {
        "genes": ["lacZ", "lacY", "lacA", "lacI"],
        "promoters": ["lacZp1", "lacZp2", "lacZp"],
    },
    "ecoli_ara_operon": {
        "genes": ["araA", "araB", "araD", "araC"],
        "promoters": ["araBp", "araCp", "araAp"],
    },
    "ecoli_trp_operon": {
        "genes": ["trpE", "trpD", "trpC", "trpB", "trpA", "trpR"],
        "promoters": ["trpLp", "trpRp"],
    },
    "ecoli_sos_lexa": {
        "genes": ["lexA"],
        "promoters": ["lexAp"],
    },
    "ecoli_sos_reca": {
        "genes": ["recA"],
        "promoters": ["recAp"],
    },
    "ecoli_flhdc_flagellar": {
        "genes": ["flhD", "flhC"],
        "promoters": ["flhDp"],
    },
    "ecoli_lambda_switch": {
        "genes": ["cI", "cro", "N", "cII"],
        "promoters": ["cIp", "croP", "pL", "pR"],
    },
    "ecoli_dna_damage_checkpoint": {
        "genes": ["lexA", "recA", "sulA", "umuD"],
        "promoters": ["lexAp", "recAp", "sulAp"],
    },
}

# Known-positive promoters (not in training) for validation panel (c).
POSITIVE_CONTROLS = [
    ("galPp", "galP", "RDBECOLIRIC05619"),  # Weak in RegulonDB; included as literature CRP promoter
    ("fadLp", "fadL", "RDBECOLIRIC04022"),
    ("ptsHp", "ptsH", "RDBECOLIRIC02795"),
    ("exuTp2", "exuT", "RDBECOLIRIC00047"),
]

# E. coli K-12 MG1655 background (NC_000913.3 composition).
ECOLI_BG = {"A": 0.247, "C": 0.252, "G": 0.252, "T": 0.249}

MOTIF_ID = "CRP_CAP"
MOTIF_NAME = "CRP/CAP cyclic-AMP activator E. coli K-12"
OUTPUT_MEME = MOTIFS_DIR / "crp_cap.meme"
SITE_LISTS_YAML = MOTIFS_DIR / "crp_site_lists.yaml"
VALIDATION_YAML = MOTIFS_DIR / "crp_pwm_validation.yaml"

STRONG_EVIDENCE = frozenset({"C", "S"})  # Confirmed, Strong


@dataclass
class CrpSite:
    ri_id: str
    tfrs_id: str
    left: int
    right: int
    strand: str
    sequence: str
    core: str
    confidence: str
    tfrs_evidence: str
    ri_evidence: str
    promoter: str
    first_gene: str
    ri_function: str
    holdout_circuit: Optional[str] = None
    holdout_reason: Optional[str] = None

    @property
    def key(self) -> str:
        return f"{self.tfrs_id}:{self.left}-{self.right}"


def _fimo_bin() -> str:
    import os
    import shutil

    env = os.environ.get("FIMO_BIN")
    if env and Path(env).exists():
        return env
    for candidate in (
        Path("/media/sdcard/miniforge3/envs/meme-env/bin/fimo"),
        Path(sys.executable).parent / "fimo",
    ):
        if candidate.exists():
            return str(candidate)
    found = shutil.which("fimo")
    if found:
        return found
    raise RuntimeError("fimo not found on PATH")


def download_regulondb(dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_file():
        return dest
    try:
        from google.cloud import storage
    except ImportError as exc:
        raise RuntimeError(
            f"RegulonDB file missing at {dest} and google-cloud-storage unavailable"
        ) from exc
    client = storage.Client()
    blob = client.bucket("regal-scholar-453620-r7-podcast-storage").blob(GCS_REGULONDB_PREFIX)
    blob.download_to_filename(str(dest))
    return dest


def parse_tf_ri_row(cols: List[str]) -> Optional[CrpSite]:
    if len(cols) < 21 or cols[3] != "CRP":
        return None
    conf = cols[19].strip()
    if conf not in STRONG_EVIDENCE:
        return None
    raw_seq = cols[9]
    core = extract_uppercase_core(raw_seq)
    if len(core) < 16:
        return None
    try:
        left = int(cols[6])
        right = int(cols[7])
    except ValueError:
        return None
    return CrpSite(
        ri_id=cols[0],
        tfrs_id=cols[5],
        left=left,
        right=right,
        strand=cols[8],
        sequence=raw_seq,
        core=core,
        confidence=conf,
        tfrs_evidence=cols[20],
        ri_evidence=cols[21] if len(cols) > 21 else "",
        promoter=cols[12],
        first_gene=cols[16],
        ri_function=cols[10],
    )


def load_crp_sites(tfri_path: Path) -> List[CrpSite]:
    sites: List[CrpSite] = []
    seen: set[str] = set()
    with tfri_path.open(encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            site = parse_tf_ri_row(line.rstrip("\n").split("\t"))
            if site is None:
                continue
            if site.key in seen:
                continue
            seen.add(site.key)
            sites.append(site)
    return sites


def load_circuit_windows() -> Dict[str, Tuple[int, int]]:
    windows: Dict[str, Tuple[int, int]] = {}
    for cid in REGRESSION_CIRCUITS:
        manifest = QUEUE_COMPLETED / f"{cid}.yaml"
        if not manifest.is_file():
            print(f"WARNING: missing manifest {manifest}", file=sys.stderr)
            continue
        data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
        region = data.get("genomic_region") or {}
        start, end = region.get("start"), region.get("end")
        if start is not None and end is not None:
            windows[cid] = (int(start), int(end))
    return windows


def overlaps(a0: int, a1: int, b0: int, b1: int) -> bool:
    return a0 <= b1 and b0 <= a1


def assign_holdouts(
    sites: List[CrpSite], windows: Dict[str, Tuple[int, int]]
) -> Tuple[List[CrpSite], List[CrpSite]]:
    training: List[CrpSite] = []
    held_out: List[CrpSite] = []

    for site in sites:
        matched: Optional[str] = None
        reasons: List[str] = []

        for cid, (start, end) in windows.items():
            scope = CIRCUIT_SCOPE.get(cid, {})
            gene_set = {g.lower() for g in scope.get("genes", [])}
            prom_set = {p.lower() for p in scope.get("promoters", [])}

            if overlaps(site.left, site.right, start, end):
                matched = cid
                reasons.append(f"genomic_overlap:{start}-{end}")
            elif site.first_gene.lower() in gene_set:
                matched = cid
                reasons.append(f"first_gene:{site.first_gene}")
            elif site.promoter.lower() in prom_set:
                matched = cid
                reasons.append(f"promoter:{site.promoter}")

        if matched:
            site.holdout_circuit = matched
            site.holdout_reason = ";".join(reasons)
            held_out.append(site)
        else:
            training.append(site)

    return training, held_out


TARGET_WIDTH = 22
LACO_OVERLAP_PATTERN = re.compile(r"AATTGTGAGCGGATAACAATT?", re.I)


def extract_uppercase_core(raw_seq: str) -> str:
    return "".join(ch for ch in raw_seq if ch.isupper())


def align_crp_core(raw_seq: str, target: int = TARGET_WIDTH) -> Optional[str]:
    """
    Align CRP sites on TGTGA/TGTG half-site family (TGTGA-N6-TCACA).
    RegulonDB cores are often annotated without literal TGTGA (e.g. ara CRP).
    """
    upper = extract_uppercase_core(raw_seq)
    if not upper:
        return None

    for pattern in ("TGTGA", "TTGTG", "TGTG", "TGTTG"):
        idx = upper.find(pattern)
        if idx >= 0:
            start = max(0, idx - 2)
            if start + target <= len(upper):
                return upper[start : start + target]
            if idx + target <= len(upper):
                return upper[idx : idx + target]

    for pattern in ("TCACA", "TCACT", "TCACAC", "TCAC"):
        idx = upper.rfind(pattern)
        if idx >= 0:
            end = idx + len(pattern)
            start = max(0, end - target)
            if len(upper) >= start + target:
                return upper[start : start + target]

    if len(upper) >= target:
        return upper[:target]
    return None


def normalize_training_sites(sites: List[CrpSite]) -> List[CrpSite]:
    out: List[CrpSite] = []
    for site in sites:
        aligned = align_crp_core(site.sequence)
        if aligned is None:
            print(f"WARNING: no CRP alignment at {site.ri_id} — skipping from PWM", file=sys.stderr)
            continue
        site.core = aligned
        out.append(site)
    return out


def annotate_holdout_cores(sites: List[CrpSite]) -> List[CrpSite]:
    """Keep all held-out sites for FIMO; annotate core when alignable."""
    for site in sites:
        aligned = align_crp_core(site.sequence)
        if aligned:
            site.core = aligned
        else:
            site.core = extract_uppercase_core(site.sequence)
    return sites


def is_high_quality_training_site(site: CrpSite) -> bool:
    """Experimental RegulonDB evidence + canonical half-site in aligned core."""
    if "EXP-" not in site.tfrs_evidence:
        return False
    if "TGTGA" not in site.core:
        return False
    if LACO_OVERLAP_PATTERN.search(site.core):
        return False
    return True


def filter_training_quality(sites: List[CrpSite]) -> List[CrpSite]:
    kept: List[CrpSite] = []
    for site in sites:
        if is_high_quality_training_site(site):
            kept.append(site)
        else:
            print(
                f"WARNING: excluding low-quality training site {site.ri_id} "
                f"({site.promoter}, evidence={site.tfrs_evidence[:40]}...)",
                file=sys.stderr,
            )
    return kept


def build_holdout_fasta_records(held_out: List[CrpSite]) -> List[Tuple[str, str]]:
    """Use full TFRS sequence context; add circuit FASTA when available."""
    records: List[Tuple[str, str]] = []
    circuit_fasta = {
        "ecoli_lac_operon": SEQUENCES_DIR / "lac_operon_region.fa",
        "ecoli_ara_operon": SEQUENCES_DIR / "ara_operon_region.fa",
        "ecoli_flhdc_flagellar": SEQUENCES_DIR / "ecoli_flhdc_flagellar.fa",
    }
    for site in held_out:
        cid = site.holdout_circuit or "unknown"
        fasta = circuit_fasta.get(cid or "")
        if fasta and fasta.is_file():
            seq = fasta.read_text(encoding="utf-8").splitlines()
            seq = "".join(line.strip() for line in seq if not line.startswith(">"))
            records.append((f"{cid}_circuit_window", seq))
        records.append(
            (f"{cid}_{site.promoter}_{site.ri_id}", site.sequence.upper())
        )
    return records


def build_pfm(cores: List[str]) -> Tuple[Dict[str, List[int]], int]:
    length = len(cores[0])
    pfm = {b: [0] * length for b in "ACGT"}
    for seq in cores:
        for i, base in enumerate(seq):
            if base in pfm:
                pfm[base][i] += 1
    return pfm, length


def pfm_to_ppm(
    pfm: Dict[str, List[int]], n_sites: int, pseudocount: float = 0.1
) -> Dict[str, List[float]]:
    denom = n_sites + 4 * pseudocount
    return {b: [(count + pseudocount) / denom for count in pfm[b]] for b in "ACGT"}


def write_meme(ppm: Dict[str, List[float]], length: int, n_sites: int, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        fh.write("MEME version 4\n\n")
        fh.write("ALPHABET= ACGT\n\n")
        fh.write("strands: + -\n\n")
        fh.write("Background letter frequencies\n")
        fh.write(
            f"A {ECOLI_BG['A']:.3f} C {ECOLI_BG['C']:.3f} "
            f"G {ECOLI_BG['G']:.3f} T {ECOLI_BG['T']:.3f}\n\n"
        )
        fh.write(f"MOTIF {MOTIF_ID} {MOTIF_NAME}\n\n")
        fh.write(
            f"letter-probability matrix: alength= 4 w= {length} "
            f"nsites= {n_sites} E= 0\n"
        )
        for pos in range(length):
            fh.write(
                f"  {ppm['A'][pos]:.6f}  {ppm['C'][pos]:.6f}  "
                f"{ppm['G'][pos]:.6f}  {ppm['T'][pos]:.6f}\n"
            )
        fh.write("\n")


def consensus_from_ppm(ppm: Dict[str, List[float]]) -> str:
    bases = "ACGT"
    return "".join(max(bases, key=lambda b: ppm[b][i]) for i in range(len(ppm["A"])))


def consensus_shape_check(consensus: str) -> Dict[str, object]:
    """Check TGTGA ... TCACA pseudopalindrome shape (CRP family; allow degeneracy)."""
    left_half = consensus[2:7] if len(consensus) >= 7 else consensus[:5]
    right_half = consensus[-7:-2] if len(consensus) >= 7 else consensus[-5:]
    spacer = consensus[7:-7] if len(consensus) > 14 else consensus[5:-5]
    left_ok = sum(a == b for a, b in zip(left_half, "TGTGA")) >= 4
    right_ok = sum(a == b for a, b in zip(right_half, "TCACA")) >= 3
    return {
        "consensus": consensus,
        "left_half_checked": left_half,
        "right_half_checked": right_half,
        "spacer_len": len(spacer),
        "left_tgtga_match": left_ok,
        "right_tcaca_match": right_ok,
        "pass": left_ok and right_ok,
    }


def write_fasta(path: Path, records: List[Tuple[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for name, seq in records:
            fh.write(f">{name}\n{seq}\n")


def run_fimo(
    meme_path: Path, fasta_path: Path, out_dir: Path, thresh: float
) -> List[Dict[str, str]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        _fimo_bin(),
        "--thresh",
        str(thresh),
        "--oc",
        str(out_dir),
        str(meme_path),
        str(fasta_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    tsv = out_dir / "fimo.tsv"
    if not tsv.is_file():
        return []
    rows: List[Dict[str, str]] = []
    header: Optional[List[str]] = None
    with tsv.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            cols = line.split("\t")
            if header is None:
                if cols and cols[0] == "motif_id":
                    header = cols
                continue
            if header and len(cols) == len(header):
                rows.append(dict(zip(header, cols)))
    return rows


def load_site_by_ri_id(tfri_path: Path, ri_id: str) -> Optional[CrpSite]:
    with tfri_path.open(encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            cols = line.rstrip("\n").split("\t")
            if len(cols) < 21 or cols[0] != ri_id or cols[3] != "CRP":
                continue
            raw_seq = cols[9]
            return CrpSite(
                ri_id=cols[0],
                tfrs_id=cols[5],
                left=int(cols[6]),
                right=int(cols[7]),
                strand=cols[8],
                sequence=raw_seq,
                core=extract_uppercase_core(raw_seq),
                confidence=cols[19].strip(),
                tfrs_evidence=cols[20],
                ri_evidence=cols[21] if len(cols) > 21 else "",
                promoter=cols[12],
                first_gene=cols[16],
                ri_function=cols[10],
            )
    return None


def fetch_positive_control_sequences(
    tfri_path: Path,
    all_sites: List[CrpSite],
    excluded_keys: set[str],
) -> List[Tuple[str, str, str]]:
    """Return (name, sequence, source) for positive controls not in training."""
    records: List[Tuple[str, str, str]] = []
    by_promoter = {s.promoter.lower(): s for s in all_sites}
    by_gene = {s.first_gene.lower(): s for s in all_sites}
    by_ri = {s.ri_id: s for s in all_sites}

    for prom, gene, src in POSITIVE_CONTROLS:
        site = None
        if src.startswith("RDB"):
            site = by_ri.get(src) or load_site_by_ri_id(tfri_path, src)
        else:
            site = by_promoter.get(prom.lower()) or by_gene.get(gene.lower())
        if site is None:
            print(f"WARNING: positive control not found: {prom}/{gene}", file=sys.stderr)
            continue
        if site.key in excluded_keys:
            continue
        records.append((f"{site.promoter}_{site.first_gene}", site.sequence.upper(), site.ri_id))
    return records


def random_ecoli_negative_sequences(n: int = 20, length: int = 200) -> List[Tuple[str, str]]:
    rng = random.Random(42)
    bases = "ACGT"
    weights = [ECOLI_BG[b] for b in bases]
    out: List[Tuple[str, str]] = []
    for i in range(n):
        seq = "".join(rng.choices(bases, weights=weights, k=length))
        out.append((f"random_ecoli_{i+1}", seq))
    return out


def calibrate_threshold(
    meme_path: Path,
    held_out: List[CrpSite],
    positive_records: List[Tuple[str, str, str]],
    negative_records: List[Tuple[str, str]],
) -> Dict[str, object]:
    """Sweep FIMO p-value thresholds; lock before any decoder class inspection."""
    candidates = [1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 5e-2]
    best = None
    sweep = []

    holdout_fasta = VALIDATION_DIR / "holdout.fa"
    pos_fasta = VALIDATION_DIR / "positive.fa"
    neg_fasta = VALIDATION_DIR / "negative.fa"

    write_fasta(
        holdout_fasta,
        build_holdout_fasta_records(held_out),
    )
    write_fasta(pos_fasta, [(n, seq) for n, seq, _ in positive_records])
    write_fasta(neg_fasta, negative_records)

    for thresh in candidates:
        h_rows = run_fimo(meme_path, holdout_fasta, VALIDATION_DIR / f"holdout_{thresh}", thresh)
        p_rows = run_fimo(meme_path, pos_fasta, VALIDATION_DIR / f"positive_{thresh}", thresh)
        n_rows = run_fimo(meme_path, neg_fasta, VALIDATION_DIR / f"negative_{thresh}", thresh)

        holdout_hits = len(h_rows)
        pos_hits = len(p_rows)
        neg_hits = len(n_rows)
        neg_rate = neg_hits / max(len(negative_records), 1)

        entry = {
            "thresh": thresh,
            "holdout_hits": holdout_hits,
            "holdout_total": len(held_out),
            "positive_hits": pos_hits,
            "positive_total": len(positive_records),
            "negative_hits": neg_hits,
            "negative_total": len(negative_records),
            "negative_rate": round(neg_rate, 4),
        }
        sweep.append(entry)

        # Prefer: recover all holdout + most positives, minimize negative FPR.
        if holdout_hits >= len(held_out) and pos_hits >= max(1, len(positive_records) // 2):
            if neg_rate <= 0.05:
                if best is None or thresh > best["thresh"]:
                    best = dict(entry)

    if best is None:
        # Relax: maximize holdout recovery then minimize neg rate.
        ranked = sorted(
            sweep,
            key=lambda e: (
                -e["holdout_hits"],
                -e["positive_hits"],
                e["negative_rate"],
            ),
        )
        best = ranked[0]

    locked = float(best["thresh"])
    return {
        "locked_fimo_pvalue_threshold": locked,
        "selection_rationale": (
            "Maximize holdout + positive recovery with negative FPR <= 5%; "
            "if none, rank by holdout hits then positive hits then FPR."
        ),
        "threshold_sweep": sweep,
        "locked_at": best,
    }


def summarize_fimo_at_threshold(
    meme_path: Path, fasta_path: Path, out_name: str, thresh: float
) -> List[Dict[str, str]]:
    rows = run_fimo(meme_path, fasta_path, VALIDATION_DIR / out_name, thresh)
    return [
        {
            "motif_id": r.get("motif_id", ""),
            "sequence_name": r.get("sequence_name", ""),
            "start": r.get("start", ""),
            "stop": r.get("stop", ""),
            "strand": r.get("strand", ""),
            "score": r.get("score", ""),
            "p-value": r.get("p-value", ""),
            "q-value": r.get("q-value", ""),
            "matched_sequence": r.get("matched_sequence", ""),
        }
        for r in rows
    ]


def site_to_dict(site: CrpSite) -> Dict[str, object]:
    d = asdict(site)
    return d


def main() -> int:
    tfri = REGULONDB_DEFAULT
    if not tfri.is_file():
        print(f"Downloading RegulonDB TF-RISet to {tfri}...")
        download_regulondb(tfri)

    print("Loading CRP sites from RegulonDB TF-RISet (Confirmed + Strong)...")
    all_sites = load_crp_sites(tfri)
    print(f"  Curated strong CRP sites (deduped by TFRS): {len(all_sites)}")

    windows = load_circuit_windows()
    print(f"  Regression circuit windows loaded: {len(windows)}")

    training_raw, held_out_raw = assign_holdouts(all_sites, windows)
    training = normalize_training_sites(training_raw)
    held_out = annotate_holdout_cores(held_out_raw)

    # Safety: no holdout key in training; drop lacO-confounded training rows.
    holdout_keys = {s.key for s in held_out}
    training = [s for s in training if s.key not in holdout_keys]
    training = filter_training_quality(training)

    print(f"  TRAINING sites: {len(training)}")
    print(f"  HELD-OUT sites: {len(held_out)}")
    for s in held_out:
        print(f"    HOLD {s.holdout_circuit}: {s.promoter} {s.left}-{s.right} {s.core}")

    if not training:
        print("ERROR: empty training set", file=sys.stderr)
        return 1

    cores = [s.core for s in training]
    pfm, width = build_pfm(cores)
    ppm = pfm_to_ppm(pfm, len(cores))
    consensus = consensus_from_ppm(ppm)
    shape = consensus_shape_check(consensus)

    write_meme(ppm, width, len(cores), OUTPUT_MEME)
    print(f"\nWritten PWM: {OUTPUT_MEME}")
    print(f"Consensus: {consensus}")
    print(f"Shape check: {shape}")

    training_keys = {s.key for s in training}
    excluded_keys = training_keys | holdout_keys
    positive_records = fetch_positive_control_sequences(tfri, all_sites, excluded_keys)
    negative_records = random_ecoli_negative_sequences()

    print("\nCalibrating FIMO threshold from controls (no decoder class inspection)...")
    threshold_info = calibrate_threshold(OUTPUT_MEME, held_out, positive_records, negative_records)
    locked = threshold_info["locked_fimo_pvalue_threshold"]
    print(f"  LOCKED threshold: p-value <= {locked}")

    holdout_fasta = VALIDATION_DIR / "holdout.fa"
    pos_fasta = VALIDATION_DIR / "positive.fa"
    neg_fasta = VALIDATION_DIR / "negative.fa"

    validation = {
        "stage": 1,
        "status": "internally_validated_pending_biologist_signoff",
        "regulondb_release": "14.5.0",
        "regulondb_source": "TF-RISet.tsv (CRP, confidence Confirmed|Strong)",
        "build_method": (
            "TGTGA-aligned 22bp cores from TF-RISet; count matrix + 0.1 pseudocount; "
            "E. coli background; lacO-confounded RegulonDB rows excluded from training"
        ),
        "n_training_sites": len(training),
        "n_held_out_sites": len(held_out),
        "consensus_shape_check": shape,
        "locked_fimo_pvalue_threshold": locked,
        "threshold_calibration": threshold_info,
        "validation_a_consensus": shape,
        "validation_b_holdout_fimo": summarize_fimo_at_threshold(
            OUTPUT_MEME, holdout_fasta, "final_holdout", locked
        ),
        "validation_c_positive_fimo": summarize_fimo_at_threshold(
            OUTPUT_MEME, pos_fasta, "final_positive", locked
        ),
        "validation_d_negative_fimo": summarize_fimo_at_threshold(
            OUTPUT_MEME, neg_fasta, "final_negative", locked
        ),
    }

    site_lists = {
        "regulondb_release": "14.5.0",
        "source": "TF-RISet.tsv",
        "filter": "tfName=CRP, confidenceLevel in (Confirmed, Strong)",
        "holdout_rules": [
            "genomic_overlap with regression circuit decode window",
            "first_gene in circuit scope",
            "promoter in circuit scope",
        ],
        "training_sites": [site_to_dict(s) for s in training],
        "held_out_sites": [site_to_dict(s) for s in held_out],
    }

    SITE_LISTS_YAML.write_text(yaml.dump(site_lists, sort_keys=False, allow_unicode=True), encoding="utf-8")
    VALIDATION_YAML.write_text(
        yaml.dump(validation, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    print(f"\nWritten site lists: {SITE_LISTS_YAML}")
    print(f"Written validation summary: {VALIDATION_YAML}")
    print("\nStage 1 complete — STOP before parser integration / re-decode.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
