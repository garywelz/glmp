#!/usr/bin/env python3
"""
Phase B1 — lac re-anchor, ara/trp manifest coord-sync, sequence guard validation.

Run on Jetson after git pull. Does NOT touch B2 circuits or cron.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
DECODER_DIR = SCRIPT_DIR.parent
SEQUENCES_DIR = DECODER_DIR / "sequences"
ARCHIVE_DIR = DECODER_DIR / "archive"
QUEUE_COMPLETED = DECODER_DIR / "queue" / "completed"
REGULONDB_PROMOTER = Path("/tmp/regulondb-v14/PromoterSet.tsv")

sys.path.insert(0, str(SCRIPT_DIR))
from genbank_fetch import fetch_from_manifest, fetch_genomic_slice  # noqa: E402
from sequence_guard import sha256_sequence, validate_sequence_against_manifest  # noqa: E402

# RegulonDB TF / CRP sites (NC_000913.3, + strand coordinates)
LAC_ELEMENTS = {
    "lacO1": (366323, 366343),
    "CRP_lacZp1": (366394, 366415),
    "lacO3": (366415, 366435),
    "lacO2_excluded": (365922, 365942),
}

UPSTREAM_BP = 200
DOWNSTREAM_BP = 1000


def load_laczp1_tss(promoter_tsv: Path) -> dict:
    if not promoter_tsv.exists():
        raise FileNotFoundError(
            f"RegulonDB PromoterSet.tsv not found at {promoter_tsv}"
        )
    with promoter_tsv.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split("\t")
            if len(parts) < 5:
                continue
            name = parts[1]
            if name == "lacZp1":
                return {
                    "promoter": name,
                    "strand": parts[2],
                    "tss": int(parts[3]),
                    "first_gene": parts[6] if len(parts) > 6 else "lacZ",
                    "row_id": parts[0],
                    "evidence": parts[12] if len(parts) > 12 else "",
                }
    raise ValueError("lacZp1 not found in PromoterSet.tsv")


def compute_window(tss: int) -> tuple[int, int]:
    return tss - UPSTREAM_BP, tss + DOWNSTREAM_BP


def element_inside(name: str, left: int, right: int, win_start: int, win_end: int) -> bool:
    mid = (left + right) // 2
    return win_start <= mid <= win_end


def checkpoint_operators(win_start: int, win_end: int) -> dict:
    report = {}
    for name, (left, right) in LAC_ELEMENTS.items():
        report[name] = {
            "coords": f"{left}-{right}",
            "inside": element_inside(name, left, right, win_start, win_end),
        }
    required = ["lacO1", "CRP_lacZp1", "lacO3"]
    missing = [n for n in required if not report[n]["inside"]]
    if missing:
        raise RuntimeError(
            f"CHECKPOINT FAILED: {missing} outside window {win_start}-{win_end}. "
            f"Report: {json.dumps(report, indent=2)}"
        )
    if report["lacO2_excluded"]["inside"]:
        print("WARNING: lacO2 falls inside window (expected excluded for standard 1201 bp)")
    return report


def write_manifest(path: Path, manifest: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")


def update_manifest_sha(manifest: dict, seq_path: Path) -> str:
    from sequence_guard import load_fasta

    _, seq = load_fasta(seq_path)
    digest = sha256_sequence(seq)
    manifest["sequence_sha256"] = digest
    return digest


def patch_lac_manifest(existing: dict, tss: int, win_start: int, win_end: int, strand: str) -> dict:
    m = dict(existing)
    m["ncbi_accession"] = "NC_000913.3"
    m["genomic_region"] = {
        "start": win_start,
        "end": win_end,
        "strand": strand,
        "tss": tss,
        "coordinates_source": (
            "RegulonDB v14.5 PromoterSet lacZp1 (RDBECOLIPMC03370); "
            f"TSS={tss} strand={strand}; window TSS-{UPSTREAM_BP}/+{DOWNSTREAM_BP} "
            f"(1201 bp). Re-anchored Phase B1 2026-07-08. "
            "Synthetic prototype archived as archive/lac_operon_region_synthetic_prototype.fa"
        ),
    }
    m["sequence_file"] = "sequences/lac_operon_region.fa"
    m["sequence_archive_note"] = (
        "Jun 24 pUC-style synthetic replaced by reference slice in Phase B1"
    )
    return m


def patch_ara_manifest(existing: dict) -> dict:
    m = dict(existing)
    m["ncbi_accession"] = "NC_000913.3"
    m["genomic_region"] = {
        "start": 69800,
        "end": 70400,
        "strand": "+",
        "tss": 70075,
        "coordinates_source": (
            "601 bp ara control region; FASTA header U00096.3:69800-70400 "
            "(≡ NC_000913.3). Manifest coords synced to on-disk sequence Phase B1 "
            "2026-07-08. TSS from RegulonDB araBp (RDBECOLIPMC03333)."
        ),
    }
    return m


def patch_trp_manifest(existing: dict) -> dict:
    m = dict(existing)
    m["ncbi_accession"] = "NC_000913.3"
    m["genomic_region"] = {
        "start": 1319700,
        "end": 1320400,
        "strand": "+",
        "tss": 1323108,
        "coordinates_source": (
            "700 bp trp control region v3; FASTA NC_000913.3:1319700-1320400. "
            "Manifest coords synced to on-disk sequence Phase B1 2026-07-08. "
            "TSS from RegulonDB trpLp (RDBECOLIPMC03403)."
        ),
    }
    return m


def step_pin_lac_window(promoter_tsv: Path) -> dict:
    lac = load_laczp1_tss(promoter_tsv)
    tss = lac["tss"]
    strand = "-" if lac["strand"].lower().startswith("rev") else lac["strand"]
    win_start, win_end = compute_window(tss)
    length = win_end - win_start + 1
    containment = checkpoint_operators(win_start, win_end)
    info = {
        "promoter": lac["promoter"],
        "tss": tss,
        "strand": strand,
        "win_start": win_start,
        "win_end": win_end,
        "length": length,
        "containment": containment,
        "regulondb_row": lac["row_id"],
    }
    print("=== STEP 1 CHECKPOINT PASS ===")
    print(json.dumps(info, indent=2))
    return info


def step_reanchor_lac(manifest: dict, win_info: dict, dry_run: bool = False) -> Path:
    lac_fa = SEQUENCES_DIR / "lac_operon_region.fa"
    archive_fa = ARCHIVE_DIR / "lac_operon_region_synthetic_prototype.fa"

    if lac_fa.exists():
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        if not archive_fa.exists():
            shutil.copy2(lac_fa, archive_fa)
            print(f"Archived synthetic -> {archive_fa}")
        else:
            print(f"Archive already exists: {archive_fa}")

    manifest = patch_lac_manifest(
        manifest,
        win_info["tss"],
        win_info["win_start"],
        win_info["win_end"],
        win_info["strand"],
    )

    if dry_run:
        print(f"DRY RUN: would fetch lac -> {lac_fa}")
        return lac_fa

    fetch_from_manifest(manifest, lac_fa)
    digest = update_manifest_sha(manifest, lac_fa)
    print(f"Wrote reference-true lac FASTA ({lac_fa}, sha256={digest[:16]}…)")

    mf_path = QUEUE_COMPLETED / "ecoli_lac_operon.yaml"
    write_manifest(mf_path, manifest)
    print(f"Updated manifest {mf_path}")
    return lac_fa


def step_sync_ara_trp(dry_run: bool = False) -> None:
    for cid, patcher in (
        ("ecoli_ara_operon", patch_ara_manifest),
        ("ecoli_trp_operon", patch_trp_manifest),
    ):
        mf_path = QUEUE_COMPLETED / f"{cid}.yaml"
        manifest = yaml.safe_load(mf_path.read_text(encoding="utf-8"))
        updated = patcher(manifest)
        seq_path = SEQUENCES_DIR / Path(updated["sequence_file"]).name
        if not dry_run:
            digest = update_manifest_sha(updated, seq_path)
            write_manifest(mf_path, updated)
            print(f"Synced {cid} manifest coords (sha256={digest[:16]}…, sequence unchanged)")
        else:
            print(f"DRY RUN: would sync {cid} manifest")


def backfill_all_manifest_sha256(dry_run: bool = False) -> None:
    """Write sequence_sha256 to every completed manifest from on-disk FASTA."""
    from run_batch import resolve_path

    for mf_path in sorted(QUEUE_COMPLETED.glob("*.yaml")):
        manifest = yaml.safe_load(mf_path.read_text(encoding="utf-8"))
        seq_path = resolve_path(manifest["sequence_file"])
        if dry_run:
            continue
        digest = update_manifest_sha(manifest, seq_path)
        write_manifest(mf_path, manifest)
        print(f"  sha256 {manifest['circuit_id']}: {digest[:16]}…")


def step_validate_all() -> int:
    cmd = [sys.executable, str(SCRIPT_DIR / "validate_all_sequences.py")]
    print("Running validate_all_sequences.py …")
    result = subprocess.run(cmd, cwd=str(DECODER_DIR))
    return result.returncode


def step_redecode(circuits: list[str]) -> int:
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "redecode_regression.py"),
        "--circuits",
        *circuits,
    ]
    print(f"Re-decoding: {circuits}")
    return subprocess.run(cmd, cwd=str(DECODER_DIR)).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase B1 re-anchoring")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-redecode", action="store_true")
    parser.add_argument(
        "--promoter-tsv",
        type=Path,
        default=REGULONDB_PROMOTER,
    )
    args = parser.parse_args()

    lac_mf = QUEUE_COMPLETED / "ecoli_lac_operon.yaml"
    if not lac_mf.exists():
        print(f"Missing {lac_mf}", file=sys.stderr)
        return 1

    lac_manifest = yaml.safe_load(lac_mf.read_text(encoding="utf-8"))
    win_info = step_pin_lac_window(args.promoter_tsv)
    step_reanchor_lac(lac_manifest, win_info, dry_run=args.dry_run)
    step_sync_ara_trp(dry_run=args.dry_run)

    if args.dry_run:
        print("DRY RUN complete — no validation/re-decode")
        return 0

    rc = step_validate_all()
    if rc != 0:
        print("STOP: guard validation failed", file=sys.stderr)
        return rc

    backfill_all_manifest_sha256(dry_run=args.dry_run)

    if not args.skip_redecode:
        rc = step_redecode(["ecoli_lac_operon", "ecoli_ara_operon", "ecoli_trp_operon"])
        if rc != 0:
            return rc

    report = {
        "phase": "B1",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "lac_window": win_info,
    }
    out = DECODER_DIR / "results" / "phase_b1_reanchor_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
