#!/usr/bin/env python3
"""
select_batch.py — GLMP batch decoder circuit selection algorithm

Reads glmp_processes, ranks circuits by decode confidence,
writes YAML manifests to queue/pending/ for run_batch.py to execute.

Usage:
  python3 select_batch.py --top 10        # queue top 10 by priority
  python3 select_batch.py --organism ecoli_k12  # queue all E. coli
  python3 select_batch.py --all           # queue everything unprocessed
  python3 select_batch.py --dry-run       # show ranking without writing
  python3 select_batch.py --top 10 --yes  # non-interactive (cron-safe)
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

try:
    from google.cloud import firestore
except ImportError:
    firestore = None

SCRIPT_DIR = Path(__file__).parent
DECODER_DIR = SCRIPT_DIR.parent
GLMP_ROOT = DECODER_DIR.parent.parent.parent
CATALOG_DIR = GLMP_ROOT / "glmp-v2" / "processes"
QUEUE_PENDING = DECODER_DIR / "queue" / "pending"
SEQUENCES_DIR = Path(
    __import__("os").environ.get("GLMP_SEQUENCES_DIR", DECODER_DIR / "sequences")
)

ORGANISM_SCORES = {
    "ecoli": 100,
    "ecoli_k12": 100,
    "e._coli": 100,
    "synthetic": 80,
    "bacillus": 60,
    "bacillus_subtilis": 60,
    "yeast": 30,
    "s_cerevisiae": 30,
    "arabidopsis": 15,
    "celegans": 15,
    "drosophila": 15,
    "mouse": 10,
    "human": 10,
    "phage_lambda": 90,
    "bacteriophage_lambda": 90,
}

DEPRIORITIZE = {"human", "mouse", "arabidopsis", "celegans", "drosophila"}

_catalog_cache = None


def load_catalog():
    global _catalog_cache
    if _catalog_cache is not None:
        return _catalog_cache
    catalog = {}
    if not CATALOG_DIR.exists():
        _catalog_cache = catalog
        return catalog
    for path in CATALOG_DIR.rglob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        cid = data.get("id") or path.stem
        catalog[cid] = data
    _catalog_cache = catalog
    return catalog


def catalog_class_fields(circuit_id: str) -> dict:
    """Biological class from glmp-v2 catalog JSON, not Firestore."""
    cat = load_catalog().get(circuit_id, {})
    return {
        "glmp_biological_class": cat.get("circuitClass"),
        "glmp_biological_subclass": cat.get("circuitSubclass"),
        "glmp_biological_class_note": cat.get("circuitClassRationale", "")[:500],
    }


def normalize_organism(raw: str, doc_id: str) -> str:
    organism = (raw or "").lower().replace(" ", "_").replace(".", "")
    if organism:
        return organism
    for prefix in ORGANISM_SCORES:
        if doc_id.startswith(prefix.replace(".", "")):
            return prefix
    if doc_id.startswith("ecoli"):
        return "ecoli_k12"
    if doc_id.startswith("yeast"):
        return "s_cerevisiae"
    return "unknown"


def score_circuit(doc_id: str, data: dict) -> int:
    organism = normalize_organism(data.get("organism"), doc_id)
    score = ORGANISM_SCORES.get(organism, 5)
    if any(d in organism for d in DEPRIORITIZE):
        score -= 20
    seq_file = SEQUENCES_DIR / f"{doc_id}.fa"
    if seq_file.exists():
        score += 10
    cat_fields = catalog_class_fields(doc_id)
    if cat_fields.get("glmp_biological_class"):
        score += 5
    return score


def already_queued(circuit_id: str) -> bool:
    for state in ("pending", "running", "completed", "failed"):
        if (DECODER_DIR / "queue" / state / f"{circuit_id}.yaml").exists():
            return True
    return False


def already_decoded(data: dict) -> bool:
    return bool(data.get("dna_topology_class"))


def manifest_status(manifest: dict) -> str:
    accession = manifest.get("ncbi_accession", "")
    region = manifest.get("genomic_region") or {}
    coords_src = str(region.get("coordinates_source", ""))
    promoter_src = str((manifest.get("promoter_region") or {}).get("coordinates_source", ""))
    if accession in ("", "TBD", None):
        return "coordinates_needed"
    if region.get("start") is None or region.get("end") is None:
        return "coordinates_needed"
    if "TBD" in coords_src or "TBD" in promoter_src:
        return "coordinates_needed"
    return "ready"


def write_manifest(circuit_id: str, data: dict, score: int) -> Path:
    organism = normalize_organism(data.get("organism"), circuit_id)
    cat = catalog_class_fields(circuit_id)
    ncbi = "NC_000913.3" if "ecoli" in circuit_id or organism.startswith("ecoli") else "TBD"

    manifest = {
        "process_id": data.get("process_id")
        or f"biology:process:{circuit_id.replace('_', '-')}",
        "circuit_id": circuit_id,
        "organism": organism,
        "ncbi_accession": ncbi,
        "genomic_region": {
            "start": None,
            "end": None,
            "strand": "+",
            "tss": None,
            "coordinates_source": "TBD — look up in RegulonDB or EcoCyc before running",
        },
        "promoter_region": {
            "gene": data.get("name", circuit_id),
            "tss_offset_upstream": 1000,
            "tss_offset_downstream": 200,
            "strand": "+",
        },
        "sequence_file": f"sequences/{circuit_id}.fa",
        "jaspar_db": "motifs/JASPAR2024_CORE_non-redundant_pfms_meme.txt",
        "custom_pwm_files": [],
        "pending_custom_pwms": [],
        "qvalue_threshold": 0.05,
        "repressor_qvalue_threshold": 1.0,
        "max_sites": 50,
        "glmp_biological_class": cat.get("glmp_biological_class"),
        "glmp_biological_subclass": cat.get("glmp_biological_subclass"),
        "glmp_biological_class_note": cat.get("glmp_biological_class_note", ""),
        "glmp_biological_class_source": "curated_catalog",
        "source_paper_ids": [],
        "_selection_score": score,
        "_status": "coordinates_needed",
    }
    manifest["_status"] = manifest_status(manifest)

    out_path = QUEUE_PENDING / f"{circuit_id}.yaml"
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Select circuits for batch decode")
    parser.add_argument("--top", type=int, help="Queue top N circuits by priority score")
    parser.add_argument("--organism", help="Queue all circuits for this organism")
    parser.add_argument("--all", action="store_true", help="Queue all unprocessed circuits")
    parser.add_argument("--dry-run", action="store_true", help="Show ranking without writing")
    parser.add_argument(
        "--yes", action="store_true", help="Skip confirmation prompt (for cron/scripts)"
    )
    args = parser.parse_args()

    if not any([args.top, args.organism, args.all, args.dry_run]):
        parser.print_help()
        sys.exit(1)

    if firestore is None:
        print("ERROR: google-cloud-firestore required", file=sys.stderr)
        sys.exit(1)

    print("Connecting to Firestore...")
    db = firestore.Client(project="regal-scholar-453620-r7", database="copernicusai")
    docs = list(db.collection("glmp_processes").stream())
    print(f"Found {len(docs)} processes in glmp_processes")
    print(f"Catalog entries loaded: {len(load_catalog())} from {CATALOG_DIR}")

    candidates = []
    skipped_decoded = 0
    skipped_queued = 0

    for doc in docs:
        data = doc.to_dict() or {}
        if already_decoded(data):
            skipped_decoded += 1
            continue
        if already_queued(doc.id):
            skipped_queued += 1
            continue
        organism = normalize_organism(data.get("organism"), doc.id)
        if args.organism and args.organism not in (doc.id + organism):
            continue
        score = score_circuit(doc.id, data)
        candidates.append((score, doc.id, data))

    candidates.sort(key=lambda x: -x[0])

    print(f"\nSkipped: {skipped_decoded} already decoded, {skipped_queued} already queued")
    print(f"Candidates to queue: {len(candidates)}")

    if args.top:
        candidates = candidates[: args.top]

    print(f"\nTop {len(candidates)} circuits by priority score:")
    for score, circuit_id, _data in candidates:
        cat = catalog_class_fields(circuit_id)
        cls = cat.get("glmp_biological_class") or "?"
        print(f"  [{score:3d}] {circuit_id}  (catalog class {cls})")

    if args.dry_run:
        print("\nDry run — no manifests written.")
        return

    if not args.yes:
        confirm = input(f"\nWrite {len(candidates)} manifests to queue/pending/? (yes/no): ")
        if confirm.lower() != "yes":
            print("Aborted.")
            return

    QUEUE_PENDING.mkdir(parents=True, exist_ok=True)
    written = 0
    for score, circuit_id, data in candidates:
        out_path = write_manifest(circuit_id, data, score)
        print(f"  Written: {out_path.name} (_status={manifest_status(yaml.safe_load(out_path.read_text()))})")
        written += 1

    print(f"\n✅ {written} manifests written to queue/pending/")
    print("Review manifests and fill in genomic_region before running run_batch.py")


if __name__ == "__main__":
    main()
