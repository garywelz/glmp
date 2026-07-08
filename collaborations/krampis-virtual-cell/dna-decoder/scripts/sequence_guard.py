#!/usr/bin/env python3
"""Validate on-disk decode FASTA against manifest genomic_region (hard-fail guard)."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Optional, Tuple

from genbank_fetch import fetch_genomic_slice

# MG1655 complete genome — same assembly, either accession.
ACCESSION_EQUIV = {
    "NC_000913.3": frozenset({"NC_000913.3", "U00096.3"}),
    "U00096.3": frozenset({"NC_000913.3", "U00096.3"}),
}


def accessions_equivalent(a: str, b: str) -> bool:
    a = (a or "").strip()
    b = (b or "").strip()
    if a == b:
        return True
    equiv = ACCESSION_EQUIV.get(a, frozenset({a}))
    return b in equiv


def load_fasta(path: Path) -> Tuple[str, str]:
    """Return (header_without_gt, sequence)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or not lines[0].startswith(">"):
        raise ValueError(f"Not a FASTA file: {path}")
    header = lines[0][1:].strip()
    seq = "".join(line.strip() for line in lines[1:] if line.strip()).upper()
    if not seq:
        raise ValueError(f"Empty sequence in {path}")
    return header, seq


def sha256_sequence(seq: str) -> str:
    return hashlib.sha256(seq.upper().encode("ascii")).hexdigest()


def parse_header_coords(header: str) -> Tuple[Optional[str], Optional[int], Optional[int]]:
    """
    Parse accession:start-end from genbank_fetch or NCBI-style FASTA headers.
    Returns (accession, start, end) or (None, None, None).
    """
    m = re.search(r"(NC_\d+\.\d+|U\d+\.\d+|J\d+\.\d+):(\d+)-(\d+)", header)
    if not m:
        return None, None, None
    return m.group(1), int(m.group(2)), int(m.group(3))


def expected_sequence(manifest: dict) -> str:
    region = manifest.get("genomic_region") or {}
    accession = manifest.get("ncbi_accession", "")
    start, end = region.get("start"), region.get("end")
    strand = region.get("strand", "+")
    if not accession or start is None or end is None:
        raise ValueError(
            f"Manifest {manifest.get('circuit_id')} missing accession or genomic_region"
        )
    return fetch_genomic_slice(accession, int(start), int(end), strand)


def validate_sequence_against_manifest(
    manifest: dict,
    seq_path: Path,
    *,
    skip_ncbi: bool = False,
) -> dict:
    """
    Validate on-disk FASTA. Returns metadata dict on success.
    Raises RuntimeError with diagnostic detail on failure.
    """
    circuit_id = manifest.get("circuit_id", seq_path.stem)
    if not seq_path.exists():
        raise RuntimeError(
            f"[{circuit_id}] sequence file missing: {seq_path}"
        )

    region = manifest.get("genomic_region") or {}
    manifest_acc = manifest.get("ncbi_accession", "")
    manifest_start = int(region["start"])
    manifest_end = int(region["end"])
    manifest_strand = region.get("strand", "+")

    header, disk_seq = load_fasta(seq_path)
    disk_hash = sha256_sequence(disk_seq)

    header_acc, header_start, header_end = parse_header_coords(header)
    header_mismatch = []
    if header_acc and not accessions_equivalent(header_acc, manifest_acc):
        header_mismatch.append(
            f"accession header={header_acc!r} manifest={manifest_acc!r}"
        )
    if header_start is not None and header_start != manifest_start:
        header_mismatch.append(
            f"start header={header_start} manifest={manifest_start}"
        )
    if header_end is not None and header_end != manifest_end:
        header_mismatch.append(f"end header={header_end} manifest={manifest_end}")

    stored_hash = manifest.get("sequence_sha256")
    if stored_hash and stored_hash != disk_hash:
        raise RuntimeError(
            f"[{circuit_id}] sequence_sha256 mismatch: "
            f"manifest={stored_hash} disk={disk_hash} ({seq_path})"
        )

    if skip_ncbi:
        if header_mismatch:
            raise RuntimeError(
                f"[{circuit_id}] FASTA header does not match manifest: "
                + "; ".join(header_mismatch)
                + f"\n  header: {header[:100]}"
            )
        return {
            "circuit_id": circuit_id,
            "path": str(seq_path),
            "length": len(disk_seq),
            "sha256": disk_hash,
            "header_ok": not header_mismatch,
        }

    try:
        ref_seq = expected_sequence(manifest)
    except Exception as exc:
        raise RuntimeError(
            f"[{circuit_id}] NCBI fetch failed during validation: {exc}"
        ) from exc

    ref_hash = sha256_sequence(ref_seq)
    if disk_seq != ref_seq:
        delta = len(disk_seq) - len(ref_seq)
        # First differing position for diagnostics
        diff_at = next(
            (i for i, (a, b) in enumerate(zip(disk_seq, ref_seq)) if a != b),
            min(len(disk_seq), len(ref_seq)),
        )
        raise RuntimeError(
            f"[{circuit_id}] sequence mismatch vs manifest NCBI window\n"
            f"  manifest: {manifest_acc}:{manifest_start}-{manifest_end} "
            f"strand={manifest_strand}\n"
            f"  file: {seq_path}\n"
            f"  header: {header[:120]}\n"
            f"  length delta: disk={len(disk_seq)} expected={len(ref_seq)} ({delta:+d})\n"
            f"  disk first30: {disk_seq[:30]}\n"
            f"  expected first30: {ref_seq[:30]}\n"
            f"  disk sha256: {disk_hash}\n"
            f"  expected sha256: {ref_hash}\n"
            + (
                f"  header issues: {'; '.join(header_mismatch)}\n"
                if header_mismatch
                else ""
            )
            + (f"  first diff at 0-based index {diff_at}" if diff_at else "")
        )

    return {
        "circuit_id": circuit_id,
        "path": str(seq_path),
        "length": len(disk_seq),
        "sha256": disk_hash,
        "header_ok": not header_mismatch,
        "ncbi_verified": True,
    }
