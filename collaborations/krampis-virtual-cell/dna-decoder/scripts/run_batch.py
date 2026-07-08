#!/usr/bin/env python3
"""
run_batch.py — GLMP batch decoder pipeline runner

Processes manifests from queue/pending/ sequentially.
Designed to run as a nightly cron job at 2 AM ET on the Jetson.

Usage:
  python3 run_batch.py              # process all pending manifests
  python3 run_batch.py --limit 5   # process at most 5 tonight
  python3 run_batch.py --dry-run   # show what would run without executing
"""

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

try:
    from google.cloud import firestore
except ImportError:
    firestore = None

SCRIPT_DIR = Path(__file__).parent
DECODER_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))
from genbank_fetch import fetch_from_manifest  # noqa: E402

QUEUE = DECODER_DIR / "queue"
SEQUENCES_DIR = Path(os.environ.get("GLMP_SEQUENCES_DIR", DECODER_DIR / "sequences"))
RESULTS_DIR = DECODER_DIR / "results"
PARSER = DECODER_DIR / "glmp_logic_parser.py"

def _fimo_bin() -> str:
    env = os.environ.get("FIMO_BIN")
    if env and Path(env).exists():
        return env
    sibling = Path(sys.executable).parent / "fimo"
    if sibling.exists():
        return str(sibling)
    found = shutil.which("fimo")
    if found:
        return found
    return "fimo"

LOG_DIR = Path(os.environ.get("GLMP_LOG_DIR", "/media/sdcard/logs"))
if sys.platform == "win32" and not LOG_DIR.exists():
    LOG_DIR = DECODER_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / f"batch_decoder_{datetime.now().strftime('%Y%m%d')}.log"

PROJECT = "regal-scholar-453620-r7"
DATABASE = "copernicusai"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


def resolve_path(manifest_key: str) -> Path:
    path = DECODER_DIR / manifest_key
    if manifest_key.startswith("sequences/"):
        alt = SEQUENCES_DIR / Path(manifest_key).name
        if alt.exists():
            return alt
    return path


def fetch_sequence(
    manifest: dict,
    dry_run: bool = False,
    force_refetch: bool = False,
) -> Path:
    """Fetch promoter sequence from NCBI, or validate existing file against manifest."""
    from sequence_guard import load_fasta, sha256_sequence, validate_sequence_against_manifest

    seq_file = resolve_path(manifest["sequence_file"])

    if seq_file.exists() and not force_refetch:
        if dry_run:
            log.info("  DRY RUN — would validate existing sequence: %s", seq_file)
            return seq_file
        validate_sequence_against_manifest(manifest, seq_file)
        log.info("  Sequence validated against manifest: %s", seq_file)
        return seq_file

    if force_refetch and seq_file.exists():
        log.info("  --force-refetch: replacing %s", seq_file)

    region = manifest.get("genomic_region") or {}
    accession = manifest.get("ncbi_accession", "")
    if not accession or accession == "TBD":
        raise ValueError(
            f"ncbi_accession is TBD — cannot auto-fetch sequence for {manifest['circuit_id']}"
        )
    if region.get("start") is None or region.get("end") is None:
        raise ValueError(
            f"genomic_region coordinates missing — cannot fetch {manifest['circuit_id']}"
        )
    coords_source = str(region.get("coordinates_source", ""))
    if "TBD" in coords_source:
        raise ValueError(
            f"Genomic coordinates are TBD — cannot fetch sequence for {manifest['circuit_id']}"
        )

    log.info(
        "  Fetching %s:%s-%s strand=%s -> %s",
        accession,
        region["start"],
        region["end"],
        region.get("strand", "+"),
        seq_file.name,
    )

    if dry_run:
        log.info("  DRY RUN — would fetch to %s", seq_file)
        return seq_file

    fetch_from_manifest(manifest, seq_file)
    _, seq = load_fasta(seq_file)
    manifest["sequence_sha256"] = sha256_sequence(seq)
    log.info(
        "  Wrote sequence %s (%d bp, sha256=%s…)",
        seq_file,
        len(seq),
        manifest["sequence_sha256"][:12],
    )
    return seq_file


def run_fimo(manifest: dict, seq_file: Path, dry_run: bool = False):
    """Run FIMO motif scanner on the sequence."""
    circuit_id = manifest["circuit_id"]
    results_dir = RESULTS_DIR / f"{circuit_id}_jaspar"

    jaspar_db = resolve_path(manifest.get("jaspar_db", "motifs/JASPAR2024_CORE_non-redundant_pfms_meme.txt"))
    qval = manifest.get("qvalue_threshold", 0.05)

    fimo = _fimo_bin()
    cmd = [
        fimo,
        "--thresh",
        str(qval),
        "--oc",
        str(results_dir),
        str(jaspar_db),
        str(seq_file),
    ]

    log.info("  Running FIMO: %s", " ".join(cmd))

    if dry_run:
        log.info("  DRY RUN — would write to %s", results_dir)
        return results_dir / "fimo.tsv", []

    if not jaspar_db.exists():
        raise FileNotFoundError(f"JASPAR database not found: {jaspar_db}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FIMO failed: {result.stderr}")

    prok_hits = []
    for pwm_file in manifest.get("custom_pwm_files", []):
        pwm_path = resolve_path(pwm_file)
        if not pwm_path.exists():
            log.warning("  Custom PWM missing (skipped): %s", pwm_path)
            continue
        prok_dir = RESULTS_DIR / f"{circuit_id}_prok_{pwm_path.stem}"
        prok_cmd = [
            fimo,
            "--thresh",
            "0.01",
            "--oc",
            str(prok_dir),
            str(pwm_path),
            str(seq_file),
        ]
        log.info("  Running FIMO (custom PWM): %s", pwm_file)
        prok = subprocess.run(prok_cmd, capture_output=True, text=True)
        if prok.returncode != 0:
            log.warning("  Custom FIMO failed for %s: %s", pwm_file, prok.stderr[:200])
        else:
            prok_hits.append(str(prok_dir / "fimo.tsv"))

    pending = manifest.get("pending_custom_pwms") or []
    if pending:
        names = ", ".join(p.get("name", "?") for p in pending)
        log.warning(
            "  Pending custom PWMs (may yield INSUFFICIENT_EVIDENCE): %s", names
        )

    return results_dir / "fimo.tsv", prok_hits


def run_parser(manifest: dict, fimo_hits: Path, prok_hits: list, dry_run: bool = False) -> dict:
    """Run glmp_logic_parser.py and return the result JSON."""
    circuit_id = manifest["circuit_id"]
    manifest_path = QUEUE / "running" / f"{circuit_id}.yaml"
    output_path = RESULTS_DIR / f"{circuit_id}_logic_{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"

    hits_args = [str(fimo_hits)] + prok_hits
    cmd = [
        sys.executable,
        str(PARSER),
        "--hits",
        *hits_args,
        "--circuit",
        circuit_id,
        "--organism",
        manifest.get("organism", "ecoli_k12"),
        "--manifest",
        str(manifest_path),
        "--output",
        str(output_path),
        "--qvalue-threshold",
        str(manifest.get("qvalue_threshold", 0.05)),
        "--repressor-qvalue-threshold",
        str(manifest.get("repressor_qvalue_threshold", 1.0)),
        "--max-sites",
        str(manifest.get("max_sites", 50)),
    ]

    log.info("  Running parser: %s", " ".join(cmd))

    if dry_run:
        log.info("  DRY RUN — would write to %s", output_path)
        return {"dna_topology_class": "DRY_RUN", "status": "dry_run"}

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Parser failed: {result.stderr}\n{result.stdout}")

    with open(output_path, encoding="utf-8") as f:
        return json.load(f)


def write_to_firestore(manifest: dict, parse_result: dict, status: str, error_log: str = None):
    """Write decode result to glmp_circuits and update glmp_processes."""
    if firestore is None:
        raise RuntimeError("google-cloud-firestore not installed")

    db = firestore.Client(project=PROJECT, database=DATABASE)
    circuit_id = manifest["circuit_id"]
    now = datetime.now(timezone.utc).isoformat()

    # SOS regulon: two promoter-level glmp_circuits docs (ecoli_sos_reca,
    # ecoli_sos_lexa) share one glmp_processes entry (ecoli_sos_lexa).
    # Both manifests use process_id biology:process:ecoli-sos-lexa.
    process_doc_id = circuit_id
    if circuit_id == "ecoli_sos_reca":
        process_doc_id = "ecoli_sos_lexa"

    circuit_doc = {
        "circuit_id": circuit_id,
        "process_id": manifest.get("process_id"),
        "organism": manifest.get("organism"),
        "decode_date": now[:10],
        "decoder_version": "v0.2.2",
        "sequence_file": manifest.get("sequence_file"),
        "genomic_region": manifest.get("genomic_region"),
        "sequence_source": f"NCBI {manifest.get('ncbi_accession', 'unknown')}",
        "pending_custom_pwms": manifest.get("pending_custom_pwms", []),
        "fimo_params": {
            "qvalue_threshold": manifest.get("qvalue_threshold", 0.05),
            "repressor_qvalue_threshold": manifest.get("repressor_qvalue_threshold", 1.0),
            "max_sites": manifest.get("max_sites", 50),
            "jaspar_db": manifest.get("jaspar_db"),
            "custom_pwm_files": manifest.get("custom_pwm_files", []),
        },
        "binding_sites": parse_result.get("binding_sites", []),
        "dna_topology_class": parse_result.get("dna_topology_class"),
        "dna_topology_note": parse_result.get("dna_topology_note"),
        "dna_topology_confidence": parse_result.get("dna_topology_confidence"),
        "glmp_biological_class": parse_result.get("glmp_biological_class"),
        "glmp_biological_subclass": parse_result.get("glmp_biological_subclass"),
        "glmp_biological_class_source": parse_result.get("glmp_biological_class_source"),
        "glmp_biological_class_note": parse_result.get("glmp_biological_class_note"),
        "circuit_class": parse_result.get("circuit_class"),
        "status": status,
        "error_log": error_log,
        "source_paper_ids": manifest.get("source_paper_ids", []),
        "updated_at": firestore.SERVER_TIMESTAMP,
    }

    db.collection("glmp_circuits").document(circuit_id).set(circuit_doc)
    log.info("  Written to glmp_circuits: %s (status=%s)", circuit_id, status)

    if status == "complete" and parse_result.get("dna_topology_class"):
        process_update = {
            "dna_topology_class": parse_result.get("dna_topology_class"),
            "dna_topology_note": parse_result.get("dna_topology_note"),
            "dna_topology_confidence": parse_result.get("dna_topology_confidence"),
            "glmp_biological_class": parse_result.get("glmp_biological_class"),
            "glmp_biological_subclass": parse_result.get("glmp_biological_subclass"),
            "glmp_biological_class_source": parse_result.get("glmp_biological_class_source"),
            "glmp_biological_class_note": parse_result.get("glmp_biological_class_note"),
            "circuit_class": parse_result.get("circuit_class"),
            "decoder_version": "v0.2.2",
            "decode_date": now[:10],
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
        db.collection("glmp_processes").document(process_doc_id).set(process_update, merge=True)
        log.info("  Updated glmp_processes: %s", process_doc_id)


def process_manifest(manifest_path: Path, dry_run: bool = False) -> bool:
    """Process one manifest through the full pipeline. Returns True on success."""
    with open(manifest_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    circuit_id = manifest["circuit_id"]
    log.info("\n%s", "=" * 60)
    log.info("Processing: %s", circuit_id)
    log.info("%s", "=" * 60)

    running_path = QUEUE / "running" / manifest_path.name
    parse_result = {}

    if not dry_run:
        shutil.move(str(manifest_path), str(running_path))

    try:
        seq_file = fetch_sequence(manifest, dry_run)
        fimo_hits, prok_hits = run_fimo(manifest, seq_file, dry_run)
        parse_result = run_parser(manifest, fimo_hits, prok_hits, dry_run)

        if not dry_run:
            write_to_firestore(manifest, parse_result, status="complete")

        completed_path = QUEUE / "completed" / manifest_path.name
        if not dry_run:
            shutil.move(str(running_path), str(completed_path))

        log.info("✅ %s — COMPLETE", circuit_id)
        log.info("   dna_topology_class: %s", parse_result.get("dna_topology_class"))
        log.info("   glmp_biological_class: %s", parse_result.get("glmp_biological_class"))
        return True

    except Exception as exc:
        error_msg = str(exc)
        log.error("❌ %s — FAILED: %s", circuit_id, error_msg)

        if not dry_run:
            write_to_firestore(manifest, parse_result, status="failed", error_log=error_msg)
            failed_path = QUEUE / "failed" / manifest_path.name
            src = running_path if running_path.exists() else manifest_path
            if src.exists():
                shutil.move(str(src), str(failed_path))

        return False


def main():
    parser = argparse.ArgumentParser(description="GLMP batch decoder runner")
    parser.add_argument("--limit", type=int, help="Process at most N circuits")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would run without executing"
    )
    args = parser.parse_args()

    pending = sorted((QUEUE / "pending").glob("*.yaml"))
    pending = [p for p in pending if p.name != ".gitkeep"]

    if not pending:
        log.info("No pending manifests — nothing to do.")
        return

    def manifest_score(p):
        with open(p, encoding="utf-8") as f:
            m = yaml.safe_load(f)
        return -(m.get("_selection_score", 0))

    pending.sort(key=manifest_score)

    if args.limit:
        pending = pending[: args.limit]

    log.info("%sProcessing %d manifests", "DRY RUN — " if args.dry_run else "", len(pending))

    success = 0
    failed = 0

    for manifest_path in pending:
        if process_manifest(manifest_path, args.dry_run):
            success += 1
        else:
            failed += 1
        if not args.dry_run:
            time.sleep(30)

    log.info("\n%s", "=" * 60)
    log.info("BATCH COMPLETE: %d success, %d failed", success, failed)
    log.info("%s", "=" * 60)


if __name__ == "__main__":
    main()
