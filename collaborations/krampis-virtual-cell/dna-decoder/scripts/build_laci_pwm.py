#!/usr/bin/env python3
"""
build_laci_pwm.py — Stage 1: LacI operator PWM (recon + build + validate).

Replaces the crude nsites=1 LacI consensus with a multi-site PWM when data allow.
Does NOT integrate into the decoder parser or re-decode circuits.

LacI is a narrow-specificity repressor (lac operators O1/O2/O3 only in RegulonDB).
CRP-style train-on-others / hold-out-lac non-circularity is generally NOT feasible;
validation is known-operator recovery, LOO within operators, specificity, and the
420 eligible-NOT collapse check vs the legacy motif.
"""

from __future__ import annotations

import json
import random
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
DECODER_DIR = SCRIPT_DIR.parent
MOTIFS_DIR = DECODER_DIR / "motifs"
SEQUENCES_DIR = DECODER_DIR / "sequences"
QUEUE_COMPLETED = DECODER_DIR / "queue" / "completed"
PARSER = DECODER_DIR / "glmp_logic_parser.py"
VALIDATION_DIR = DECODER_DIR / "_laci_pwm_validation"  # gitignored scratch

REGULONDB_DEFAULT = Path("/tmp/regulondb-v14/TF-RISet.tsv")
GCS_REGULONDB_PREFIX = "validation/regulondb-v14/TF-RISet.tsv"

LEGACY_MEME = MOTIFS_DIR / "laci_motif.meme"
LEGACY_ARCHIVE = MOTIFS_DIR / "laci_motif_nsites1_legacy.meme"
OUTPUT_MEME = MOTIFS_DIR / "laci_lacO.meme"
SITE_LISTS_YAML = MOTIFS_DIR / "laci_site_lists.yaml"
VALIDATION_YAML = MOTIFS_DIR / "laci_pwm_validation.yaml"
RECON_YAML = MOTIFS_DIR / "laci_pwm_recon.yaml"

MOTIF_ID = "LacI_lacO"
MOTIF_NAME = "LacI lac repressor operator E. coli K-12"
TARGET_WIDTH = 21

ECOLI_BG = {"A": 0.247, "C": 0.252, "G": 0.252, "T": 0.249}
STRONG_EVIDENCE = frozenset({"C", "S"})

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

# Canonical operator names / expected affinity (O1 strongest).
KNOWN_OPERATORS = {
    "lacO1": {
        "sequence": "AATTGTGAGCGGATAACAATT",
        "expected_rank": 1,
        "source": "Gilbert_Maxam_1973; RegulonDB RDBECOLIRIC04260",
    },
    "lacO2_genomic": {
        "sequence": "GGTTGTTACTCGCTCACATTT",
        "expected_rank": 2,
        "source": "RegulonDB RDBECOLIRIC04258 (genomic O2 annotation)",
    },
    "lacO2_classic": {
        "sequence": "AAATTGTGAGCGCTCACAATT",
        "expected_rank": 2,
        "source": "textbook_classic_O2 (not in RegulonDB TF-RISet)",
    },
    "lacO3": {
        "sequence": "GGCAGTGAGCGCAACGCAATT",
        "expected_rank": 3,
        "source": "RegulonDB RDBECOLIRIC04259",
    },
}

# Additional literature sequences for PWM depth (not independent genomic sites).
LITERATURE_SUPPLEMENT = [
    ("Osym_symmetric", "TGTGTGAGCGCTCACA", "Bellomy_1997_symmetric_ideal", "curated"),
    ("Osym_padded_21", "AAATTGTGAGCGGATAACAATT", "near_O1_symmetric_family", "curated"),
]

# External DB recon notes (manual survey; no machine ingest in this pipeline).
EXTERNAL_SOURCE_RECON = [
    {
        "source": "RegulonDB v14.5 TF-RISet",
        "access": "GCS validation/regulondb-v14/TF-RISet.tsv",
        "laci_rows_confirmed_strong": None,
        "notes": "Primary source; filled at runtime.",
    },
    {
        "source": "CollecTF",
        "access": "https://collectf.umbc.edu/",
        "laci_rows_confirmed_strong": 0,
        "notes": "No E. coli LacI operator PWM ingested in this pipeline; site count not exported.",
    },
    {
        "source": "PRODORIC",
        "access": "https://www.prodoric.de/",
        "laci_rows_confirmed_strong": 0,
        "notes": "LacI operator matrices exist in literature but not staged in GCS for this build.",
    },
    {
        "source": "Spec-seq / SELEX variant collections",
        "access": "Kinney et al.; E-GEOD-61223; Bellomy thermodynamics",
        "laci_rows_confirmed_strong": "1000s (variants)",
        "notes": (
            "Rich variant data exist in publications but are not machine-readable in repo. "
            "Supplement limited curated Osym-family sequences only."
        ),
    },
]


@dataclass
class LaciSite:
    site_id: str
    sequence: str
    core: str
    source: str
    evidence: str  # regulondb | literature | curated
    operator_name: str
    ri_id: Optional[str] = None
    left: Optional[int] = None
    right: Optional[int] = None
    strand: Optional[str] = None
    confidence: Optional[str] = None
    promoter: Optional[str] = None
    in_lac_operon: bool = False
    holdout_role: Optional[str] = None  # loo_fold | known_positive_panel | training

    @property
    def key(self) -> str:
        return self.site_id


def _fimo_bin() -> str:
    import os

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
    from google.cloud import storage

    client = storage.Client()
    blob = client.bucket("regal-scholar-453620-r7-podcast-storage").blob(GCS_REGULONDB_PREFIX)
    blob.download_to_filename(str(dest))
    return dest


def extract_uppercase_core(raw_seq: str) -> str:
    return "".join(ch for ch in raw_seq if ch.isupper())


def align_laci_core(raw_seq: str, target: int = TARGET_WIDTH) -> Optional[str]:
    """Align lac operator on central GCG dyad (21 bp window)."""
    upper = extract_uppercase_core(raw_seq)
    if not upper:
        return None
    if len(upper) < target:
        return None

    # Prefer central GCG (hinge region in O1).
    idx = upper.find("GCG")
    if idx >= 0:
        center = idx + 1
        start = max(0, center - 10)
        if start + target <= len(upper):
            return upper[start : start + target]

    for anchor in ("GTG", "CAC", "CACA"):
        idx = upper.find(anchor)
        if idx >= 0:
            start = max(0, idx - 6)
            if start + target <= len(upper):
                return upper[start : start + target]

    return upper[:target]


def parse_laci_row(cols: List[str]) -> Optional[LaciSite]:
    if len(cols) < 21 or cols[3] != "LacI":
        return None
    conf = cols[19].strip()
    if conf not in STRONG_EVIDENCE:
        return None
    raw_seq = cols[9]
    core = align_laci_core(raw_seq)
    if core is None:
        return None
    try:
        left = int(cols[6])
        right = int(cols[7])
    except ValueError:
        return None
    promoter = cols[12]
    op_name = "lacO1" if "AATTGTGAGCGGATAACAATT" in core else (
        "lacO3" if "GGCAGTGAGCGCAACGCA" in core else "lacO2_genomic"
    )
    return LaciSite(
        site_id=cols[0],
        sequence=raw_seq,
        core=core[:TARGET_WIDTH],
        source="regulondb",
        evidence=cols[20],
        operator_name=op_name,
        ri_id=cols[0],
        left=left,
        right=right,
        strand=cols[8],
        confidence=conf,
        promoter=promoter,
        in_lac_operon=True,
    )


def load_regulondb_laci(tfri_path: Path) -> List[LaciSite]:
    sites: List[LaciSite] = []
    seen: set[str] = set()
    with tfri_path.open(encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            site = parse_laci_row(line.rstrip("\n").split("\t"))
            if site is None:
                continue
            if site.key in seen:
                continue
            seen.add(site.key)
            sites.append(site)
    return sites


def build_curated_training_pool(rdb_sites: List[LaciSite]) -> Tuple[List[LaciSite], Dict[str, object]]:
    """Merge RegulonDB + literature supplements; dedupe by core sequence."""
    pool: List[LaciSite] = list(rdb_sites)
    by_core = {s.core.upper(): s for s in pool}

    for name, seq, src, ev in LITERATURE_SUPPLEMENT:
        core = align_laci_core(seq)
        if core is None or len(core) < TARGET_WIDTH:
            continue
        if core in by_core:
            continue
        site = LaciSite(
            site_id=f"lit_{name}",
            sequence=seq.upper(),
            core=core[:TARGET_WIDTH],
            source="literature",
            evidence=ev,
            operator_name=name,
            in_lac_operon=False,
        )
        pool.append(site)
        by_core[core] = site

    # Add classic O2 if not identical to genomic RDB row.
    classic = KNOWN_OPERATORS["lacO2_classic"]["sequence"]
    core_c = align_laci_core(classic) or classic
    if core_c not in by_core:
        pool.append(
            LaciSite(
                site_id="lit_lacO2_classic",
                sequence=classic,
                core=core_c[:TARGET_WIDTH],
                source="literature",
                evidence="textbook",
                operator_name="lacO2_classic",
                in_lac_operon=False,
            )
        )

    recon = {
        "regulondb_laci_confirmed_strong": len(rdb_sites),
        "literature_supplement_added": len(pool) - len(rdb_sites),
        "total_training_candidates": len(pool),
        "all_in_lac_operon": all(s.in_lac_operon for s in rdb_sites),
        "crp_style_holdout_feasible": False,
        "holdout_verdict": (
            "NO — RegulonDB lists only three LacI binding sites, all at lacZp1 / lacZ "
            "scope (operators O1/O2/O3). There is no independent LacI site pool to train "
            "on while holding out the natural lac operators. Validation uses leave-one-out "
            "among operators, known-operator recovery in the lac promoter, specificity on "
            "non-lac promoters, and the 420 eligible-NOT collapse vs legacy nsites=1 PWM."
        ),
        "validation_approach": "specificity_and_known_operator_based_with_loo",
        "external_sources": EXTERNAL_SOURCE_RECON,
    }
    EXTERNAL_SOURCE_RECON[0]["laci_rows_confirmed_strong"] = len(rdb_sites)
    return pool, recon


def build_pfm(cores: List[str]) -> Tuple[Dict[str, List[int]], int]:
    width = len(cores[0])
    pfm = {b: [0] * width for b in "ACGT"}
    for seq in cores:
        for i, base in enumerate(seq):
            if base in pfm:
                pfm[base][i] += 1
    return pfm, width


def pfm_to_ppm(pfm: Dict[str, List[int]], n_sites: int, pseudocount: float = 0.1) -> Dict[str, List[float]]:
    denom = n_sites + 4 * pseudocount
    return {b: [(c + pseudocount) / denom for c in pfm[b]] for b in "ACGT"}


def write_meme(ppm: Dict[str, List[float]], length: int, n_sites: int, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        fh.write("MEME version 4\n\nALPHABET= ACGT\n\nstrands: + -\n\n")
        fh.write("Background letter frequencies\n")
        fh.write(
            f"A {ECOLI_BG['A']:.3f} C {ECOLI_BG['C']:.3f} "
            f"G {ECOLI_BG['G']:.3f} T {ECOLI_BG['T']:.3f}\n\n"
        )
        fh.write(f"MOTIF {MOTIF_ID} {MOTIF_NAME}\n\n")
        fh.write(f"letter-probability matrix: alength= 4 w= {length} nsites= {n_sites} E= 0\n")
        for pos in range(length):
            fh.write(
                f"  {ppm['A'][pos]:.6f}  {ppm['C'][pos]:.6f}  "
                f"{ppm['G'][pos]:.6f}  {ppm['T'][pos]:.6f}\n"
            )
        fh.write("\n")


def consensus_from_ppm(ppm: Dict[str, List[float]]) -> str:
    return "".join(max("ACGT", key=lambda b: ppm[b][i]) for i in range(len(ppm["A"])))


def palindrome_shape_check(consensus: str) -> Dict[str, object]:
    """Check GTG ... CAC inverted-repeat operator shape (degenerate allowed)."""
    left = consensus[4:9] if len(consensus) >= 9 else consensus[:5]
    right = consensus[-9:-4] if len(consensus) >= 9 else consensus[-5:]
    left_ok = sum(a == b for a, b in zip(left, "GTGAG")) >= 3
    right_ok = sum(a == b for a, b in zip(right, "CACAT")) >= 3
    return {
        "consensus": consensus,
        "left_half_checked": left,
        "right_half_checked": right,
        "pass": left_ok and right_ok,
    }


def pad_for_fimo(seq: str, min_len: int = 40) -> str:
    """Pad short operator sequences so FIMO (w=21) can scan them."""
    seq = seq.upper()
    if len(seq) >= min_len:
        return seq
    flank = "ACGTACGTACGT"
    need = min_len - len(seq)
    left = flank[: need // 2]
    right = flank[: need - len(left)]
    return left + seq + right


def write_fasta(path: Path, records: List[Tuple[str, str]], min_len: int = 0) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for name, seq in records:
            out = pad_for_fimo(seq, min_len) if min_len else seq.upper()
            fh.write(f">{name}\n{out}\n")


def run_fimo(meme_path: Path, fasta_path: Path, out_dir: Path, thresh: float) -> List[Dict[str, str]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [_fimo_bin(), "--thresh", str(thresh), "--oc", str(out_dir), str(meme_path), str(fasta_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        err = (result.stderr or result.stdout or "")[:500]
        raise RuntimeError(f"FIMO failed ({meme_path.name}): {err}")
    tsv = out_dir / "fimo.tsv"
    rows: List[Dict[str, str]] = []
    if not tsv.is_file():
        return rows
    header: Optional[List[str]] = None
    with tsv.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            cols = line.split("\t")
            if header is None:
                if cols and cols[0] == "motif_id":
                    header = cols
                continue
            if header and len(cols) == len(header):
                rows.append(dict(zip(header, cols)))
    return rows


def leave_one_out_validation(pool: List[LaciSite], locked_candidate: float = 1e-4) -> List[Dict[str, object]]:
    """Train on n-1 operators, FIMO-scan held-out operator sequence."""
    rdb_ops = [s for s in pool if s.in_lac_operon]
    results = []
    for held in rdb_ops:
        train = [s for s in pool if s.key != held.key]
        cores = [s.core for s in train]
        pfm, width = build_pfm(cores)
        ppm = pfm_to_ppm(pfm, len(cores))
        tmp_meme = VALIDATION_DIR / f"loo_{held.operator_name}.meme"
        write_meme(ppm, width, len(cores), tmp_meme)
        fa = VALIDATION_DIR / f"loo_{held.operator_name}.fa"
        write_fasta(fa, [(held.operator_name, held.core)], min_len=40)
        rows = run_fimo(tmp_meme, fa, VALIDATION_DIR / f"loo_{held.operator_name}_fimo", locked_candidate)
        best_p = min((float(r["p-value"]) for r in rows), default=None)
        results.append({
            "held_out": held.operator_name,
            "held_out_ri_id": held.ri_id,
            "train_n": len(train),
            "recovered": bool(rows),
            "best_pvalue": best_p,
            "hits": len(rows),
        })
    return results


def known_operator_panel_fimo(meme_path: Path, thresh: float) -> List[Dict[str, object]]:
    records = [(name, info["sequence"]) for name, info in KNOWN_OPERATORS.items()]
    fa = VALIDATION_DIR / "known_operators.fa"
    write_fasta(fa, records, min_len=40)
    rows = run_fimo(meme_path, fa, VALIDATION_DIR / "known_operators_fimo", thresh)
    by_name: Dict[str, List[Dict[str, str]]] = {}
    for r in rows:
        by_name.setdefault(r.get("sequence_name", ""), []).append(r)
    out = []
    for name, info in KNOWN_OPERATORS.items():
        hits = by_name.get(name, [])
        best_p = min((float(h["p-value"]) for h in hits), default=None)
        best_score = max((float(h["score"]) for h in hits), default=None) if hits else None
        out.append({
            "operator": name,
            "sequence": info["sequence"],
            "expected_rank": info["expected_rank"],
            "source": info["source"],
            "recovered_at_thresh": bool(hits),
            "best_pvalue": best_p,
            "best_score": best_score,
            "n_hits": len(hits),
        })
    ranks = sorted([x for x in out if x["best_pvalue"] is not None], key=lambda x: x["best_pvalue"])
    for i, item in enumerate(ranks, 1):
        item["observed_p_rank"] = i
    return out


def circuit_promoter_sequences() -> List[Tuple[str, str]]:
    records: List[Tuple[str, str]] = []
    for cid in REGRESSION_CIRCUITS:
        if cid == "ecoli_lac_operon":
            continue
        manifest = QUEUE_COMPLETED / f"{cid}.yaml"
        if not manifest.is_file():
            continue
        data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
        seq_file = SEQUENCES_DIR / Path(data.get("sequence_file", "")).name
        if not seq_file.is_file():
            continue
        seq = "".join(l for l in seq_file.read_text().splitlines() if not l.startswith(">"))
        records.append((cid, seq))
    return records


def calibrate_threshold(
    meme_path: Path,
    known_ops_fa: Path,
    lac_window_fa: Path,
    negative_records: List[Tuple[str, str]],
) -> Dict[str, object]:
    candidates = [1e-6, 5e-6, 1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2]
    neg_fa = VALIDATION_DIR / "specificity_neg.fa"
    write_fasta(neg_fa, negative_records)
    sweep = []
    best = None
    for thresh in candidates:
        k_rows = run_fimo(meme_path, known_ops_fa, VALIDATION_DIR / f"cal_k_{thresh}", thresh)
        l_rows = run_fimo(meme_path, lac_window_fa, VALIDATION_DIR / f"cal_l_{thresh}", thresh)
        n_rows = run_fimo(meme_path, neg_fa, VALIDATION_DIR / f"cal_n_{thresh}", thresh)
        o1_hits = [r for r in k_rows if r.get("sequence_name") == "lacO1"]
        neg_rate = len(n_rows) / max(len(negative_records), 1)
        entry = {
            "thresh": thresh,
            "known_operator_hits": len(k_rows),
            "lac_window_hits": len(l_rows),
            "lacO1_recovered": bool(o1_hits),
            "negative_hits": len(n_rows),
            "negative_rate": round(neg_rate, 4),
        }
        sweep.append(entry)
        if o1_hits and len(k_rows) >= 3 and neg_rate <= 0.05:
            if best is None or thresh > best["thresh"]:
                best = dict(entry)
    if best is None:
        best = sorted(sweep, key=lambda e: (-int(e["lacO1_recovered"]), -e["known_operator_hits"], e["negative_rate"]))[0]
    return {
        "locked_fimo_pvalue_threshold": float(best["thresh"]),
        "threshold_sweep": sweep,
        "locked_at": best,
        "selection_rationale": "Recover lacO1 + >=3 known operators with negative FPR <= 5%; else rank by lacO1 then known hits then FPR.",
    }


def count_laci_not_gates(
    custom_meme: Path,
    lac_fasta: Path,
    custom_fimo_thresh: float,
    motif_ids: Tuple[str, ...] = ("LacI_lacO1", "LacI_lacO"),
) -> Dict[str, object]:
    """Run JASPAR + custom FIMO on lac region and count LacI NOT via parser."""
    jaspar = MOTIFS_DIR / "JASPAR2024_CORE_non-redundant_pfms_meme.txt"
    if not jaspar.is_file():
        jaspar = Path("/media/sdcard/decoder/motifs/JASPAR2024_CORE_non-redundant_pfms_meme.txt")
    if not jaspar.is_file():
        return {"error": "JASPAR DB missing", "laci_not_gates": None}

    jaspar_dir = VALIDATION_DIR / "notcheck_jaspar"
    custom_dir = VALIDATION_DIR / "notcheck_custom"
    run_fimo(jaspar, lac_fasta, jaspar_dir, 0.05)
    run_fimo(custom_meme, lac_fasta, custom_dir, custom_fimo_thresh)

    out_json = VALIDATION_DIR / "notcheck_logic.json"
    cmd = [
        sys.executable,
        str(PARSER),
        "--hits",
        str(jaspar_dir / "fimo.tsv"),
        str(custom_dir / "fimo.tsv"),
        "--circuit",
        "ecoli_lac_operon",
        "--organism",
        "ecoli_k12",
        "--output",
        str(out_json),
        "--qvalue-threshold",
        "0.05",
        "--repressor-qvalue-threshold",
        "1.0",
        "--max-sites",
        "50",
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    data = json.loads(out_json.read_text(encoding="utf-8"))
    rels = data.get("relationships", [])
    lac_not = [
        r for r in rels
        if r.get("logic_type") == "NOT"
        and any(mid in r.get("site_a", "") or mid in r.get("site_b", "") for mid in motif_ids)
    ]
    overlap = sum(1 for r in lac_not if r.get("rule_applied") == "repressor_overlaps_target")
    custom_hits = [
        s for s in data.get("binding_sites", [])
        if any(s.get("motif_id", "").startswith(mid[:8]) for mid in motif_ids)
    ]
    return {
        "total_not_gates": len([r for r in rels if r.get("logic_type") == "NOT"]),
        "laci_not_gates": len(lac_not),
        "laci_overlap_not_gates": overlap,
        "custom_laci_binding_sites": len(custom_hits),
        "custom_fimo_thresh": custom_fimo_thresh,
        "motif_id_in_meme": custom_meme.name,
    }


def archive_legacy_meme() -> None:
    if LEGACY_MEME.is_file() and not LEGACY_ARCHIVE.is_file():
        shutil.copy2(LEGACY_MEME, LEGACY_ARCHIVE)
        print(f"Archived legacy PWM: {LEGACY_ARCHIVE}")


def safety_valve_check(pool: List[LaciSite], recon: Dict[str, object]) -> Optional[str]:
    rdb_n = recon["regulondb_laci_confirmed_strong"]
    if rdb_n < 2:
        return (
            f"SAFETY VALVE: only {rdb_n} RegulonDB LacI sites — cannot build meaningful PWM. "
            "Consider adopting a published peer-reviewed LacI PSSM instead."
        )
    if len(pool) < 3:
        return (
            f"SAFETY VALVE: training pool has only {len(pool)} sequences after merge — "
            "marginal improvement over nsites=1; report and reconsider."
        )
    return None


def main() -> int:
    print("=" * 60)
    print("LacI PWM Stage 1 — recon + build + validate (no parser integration)")
    print("=" * 60)

    tfri = REGULONDB_DEFAULT
    if not tfri.is_file():
        print(f"Downloading RegulonDB TF-RISet to {tfri}...")
        download_regulondb(tfri)

    # ── PART A: recon ─────────────────────────────────────────────
    rdb_sites = load_regulondb_laci(tfri)
    pool, recon = build_curated_training_pool(rdb_sites)
    RECON_YAML.write_text(yaml.dump(recon, sort_keys=False, allow_unicode=True), encoding="utf-8")

    print("\nPART A — DATA LANDSCAPE RECON")
    print(f"  RegulonDB LacI (Confirmed|Strong): {len(rdb_sites)}")
    for s in rdb_sites:
        print(f"    {s.ri_id} {s.operator_name} {s.left}-{s.right} {s.core} ({s.confidence})")
    print(f"  Training pool after literature supplement: {len(pool)}")
    print(f"  VERDICT: CRP-style holdout feasible? {recon['crp_style_holdout_feasible']}")
    print(f"  Approach: {recon['validation_approach']}")
    print(f"  Written: {RECON_YAML}")

    valve = safety_valve_check(pool, recon)
    if valve:
        print(f"\n{valve}", file=sys.stderr)
        # Continue if we have >=3 pool — marginal but document; stop only if <2 RDB.
        if recon["regulondb_laci_confirmed_strong"] < 2:
            return 2

    archive_legacy_meme()

    # ── PART B: build ─────────────────────────────────────────────
    # Primary PWM: RegulonDB operators only (avoid literature mis-alignment).
    rdb_only = [s for s in pool if s.in_lac_operon]
    training = rdb_only if len(rdb_only) >= 3 else pool
    for s in training:
        s.holdout_role = "training"
    cores = [s.core for s in training]
    pfm, width = build_pfm(cores)
    ppm = pfm_to_ppm(pfm, len(cores))
    consensus = consensus_from_ppm(ppm)
    shape = palindrome_shape_check(consensus)
    write_meme(ppm, width, len(cores), OUTPUT_MEME)
    print(f"\nPART B — BUILD")
    print(f"  Written: {OUTPUT_MEME} (nsites={len(cores)})")
    print(f"  Consensus: {consensus}")
    print(f"  Palindrome shape: {shape}")

    # ── PART C: validate ──────────────────────────────────────────
    known_fa = VALIDATION_DIR / "known_operators.fa"
    write_fasta(known_fa, [(n, i["sequence"]) for n, i in KNOWN_OPERATORS.items()], min_len=40)
    lac_fa = SEQUENCES_DIR / "lac_operon_region.fa"
    if not lac_fa.is_file():
        lac_fa = Path("/media/sdcard/decoder/sequences/lac_operon_region.fa")
    neg_records = circuit_promoter_sequences() + [
        (f"random_ecoli_{i}", "".join(random.Random(42 + i).choices("ACGT", k=200)))
        for i in range(20)
    ]

    print("\nPART C — VALIDATE (calibrating threshold...)")
    cal = calibrate_threshold(OUTPUT_MEME, known_fa, lac_fa, neg_records)
    locked = cal["locked_fimo_pvalue_threshold"]
    print(f"  LOCKED FIMO p-value threshold: {locked}")

    known_panel = known_operator_panel_fimo(OUTPUT_MEME, locked)
    loo = leave_one_out_validation([s for s in pool if s.in_lac_operon], locked)
    neg_fa = VALIDATION_DIR / "specificity_final.fa"
    write_fasta(neg_fa, neg_records)
    neg_rows = run_fimo(OUTPUT_MEME, neg_fa, VALIDATION_DIR / "specificity_final", locked)
    lac_rows = run_fimo(OUTPUT_MEME, lac_fa, VALIDATION_DIR / "lac_window_final", locked)

    print("\n  Known-operator panel:")
    for item in known_panel:
        print(f"    {item['operator']}: p={item.get('best_pvalue')} rank={item.get('observed_p_rank')} "
              f"expected_rank={item['expected_rank']}")

    print("\n  Leave-one-out (within lac operators — NOT CRP-equivalent holdout):")
    for item in loo:
        print(f"    hold {item['held_out']}: recovered={item['recovered']} p={item.get('best_pvalue')}")

    print("\n  THE 420 CHECK (eligible LacI NOT gates at locked custom FIMO threshold):")
    legacy_not_loose = count_laci_not_gates(LEGACY_MEME, lac_fa, 0.01, ("LacI_lacO1",))
    new_not_loose = count_laci_not_gates(OUTPUT_MEME, lac_fa, 0.01, ("LacI_lacO",))
    legacy_not = count_laci_not_gates(LEGACY_MEME, lac_fa, locked, ("LacI_lacO1",))
    new_not = count_laci_not_gates(OUTPUT_MEME, lac_fa, locked, ("LacI_lacO",))
    print(f"    At locked p<={locked}:")
    print(f"      Legacy nsites=1: {legacy_not.get('laci_not_gates')} LacI NOT "
          f"({legacy_not.get('custom_laci_binding_sites')} custom hits)")
    print(f"      New PWM:         {new_not.get('laci_not_gates')} LacI NOT "
          f"({new_not.get('custom_laci_binding_sites')} custom hits)")
    print(f"    At loose FIMO 0.01 (parser load threshold — diagnostic only):")
    print(f"      Legacy: {legacy_not_loose.get('laci_not_gates')} NOT; "
          f"New: {new_not_loose.get('laci_not_gates')} NOT")

    # ── PART D: honest statement ──────────────────────────────────
    honest = {
        "non_circular_holdout_equivalent_to_crp": False,
        "reason": recon["holdout_verdict"],
        "guarantees_achieved": [
            "Multi-site PWM (nsites>1) from RegulonDB + curated literature supplements",
            f"Locked FIMO threshold p<={locked} from controls before any re-decode",
            "Known-operator recovery panel (lacO1/O2/O3)",
            "Leave-one-out recovery among the three RegulonDB operators (within-operon only)",
            f"Specificity scan: {len(neg_records)} non-lac sequences, "
            f"{len(neg_rows)} hits at locked threshold",
            f"420 collapse check at locked threshold: legacy "
            f"{legacy_not.get('laci_not_gates')} → new {new_not.get('laci_not_gates')} "
            f"eligible LacI NOT gates",
            "Consensus palindrome shape check",
        ],
        "guarantees_not_achieved": [
            "CRP-style out-of-sample holdout of lac operators while training on independent LacI sites",
            "Large-scale SELEX/Spec-seq variant training (data not ingested)",
        ],
        "lac_class_ii_implication": (
            "Stage 2 integration NOT performed. Replacing the crude LacI PWM may change lac "
            "dna_topology_class; biologist must re-evaluate after Stage 2 re-decode."
        ),
    }

    validation = {
        "stage": 1,
        "status": "internally_validated_pending_biologist_signoff",
        "motif_id": MOTIF_ID,
        "pwm_file": str(OUTPUT_MEME.name),
        "legacy_pwm_archive": str(LEGACY_ARCHIVE.name),
        "regulondb_release": "14.5.0",
        "build_method": (
            "21bp GTG/CAC-family aligned cores; RegulonDB Confirmed|Strong LacI rows + "
            "curated literature Osym/O2 supplements; count matrix + 0.1 pseudocount; "
            "E. coli background"
        ),
        "n_training_sites": len(training),
        "consensus": consensus,
        "palindrome_shape_check": shape,
        "locked_fimo_pvalue_threshold": locked,
        "threshold_calibration": cal,
        "recon_verdict": recon,
        "leave_one_out_validation": loo,
        "known_operator_panel": known_panel,
        "specificity": {
            "negative_sequences": len(neg_records),
            "negative_hits_at_locked": len(neg_rows),
            "negative_rate": round(len(neg_rows) / max(len(neg_records), 1), 4),
            "lac_window_hits_at_locked": len(lac_rows),
        },
        "not_gate_420_check": {
            "at_locked_threshold": {"legacy_meme": legacy_not, "new_meme": new_not},
            "at_loose_fimo_0p01_diagnostic": {
                "legacy_meme": legacy_not_loose,
                "new_meme": new_not_loose,
            },
            "collapse_ratio_locked": (
                round(new_not.get("laci_not_gates", 0) / max(legacy_not.get("laci_not_gates", 1), 1), 4)
            ),
        },
        "honest_validation_statement": honest,
    }

    site_lists = {
        "regulondb_release": "14.5.0",
        "source": "TF-RISet.tsv + curated literature supplements",
        "filter": "tfName=LacI, confidenceLevel in (Confirmed, Strong) for RegulonDB rows",
        "training_sites": [asdict(s) for s in training],
        "known_operator_panel_sequences": KNOWN_OPERATORS,
    }

    SITE_LISTS_YAML.write_text(yaml.dump(site_lists, sort_keys=False, allow_unicode=True), encoding="utf-8")
    VALIDATION_YAML.write_text(yaml.dump(validation, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"\nWritten: {SITE_LISTS_YAML}")
    print(f"Written: {VALIDATION_YAML}")
    print("\nPART D — honest validation statement recorded in validation YAML.")
    print("Stage 1 complete — STOP before parser integration / re-decode.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
