"""
Live Firestore / Jetson paths — verified 2026-06-24 via crontab -l and SSH.

Update this module after infrastructure changes; do not assume briefing paths.
"""

from __future__ import annotations

import os
from pathlib import Path

# GCP / Firestore (matches ingest_metadata_to_firestore.sh + Jetson env)
GCP_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "regal-scholar-453620-r7")
FIRESTORE_DATABASE = os.environ.get("FIRESTORE_DATABASE", "copernicusai")

# Existing production collection (scout ingest target — NOT "papers")
RESEARCH_PAPERS_COLLECTION = "research_papers"

# New collections (Phase 1+)
GLMP_CIRCUITS_COLLECTION = "glmp_circuits"
SCHEDULER_STATUS_COLLECTION = "scheduler_status"

DEFAULT_CREDENTIALS_PATH = Path(
    os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS",
        "/home/gary/.config/copernicus/gcp-sa.json",
    )
)

# Jetson layout (readlink -f /home/gdubs/copernicus-web-public → SD card, 2026-06-24)
LEGACY_REPO_SYMLINK = Path("/home/gdubs/copernicus-web-public")
COPERNICUS_REPO_ROOT = Path("/media/sdcard/copernicus-worker/copernicus-web")
HUGGINGFACE_SPACE_DIR = LEGACY_REPO_SYMLINK / "huggingface-space"
VENV_PYTHON = Path("/media/sdcard/copernicus-worker/venv/bin/python3.8")
DECODER_ROOT = Path("/media/sdcard/decoder")
SCHEDULER_DEPLOY_ROOT = Path("/media/sdcard/scheduler")
SCOUT_DEPLOY_ROOT = SCHEDULER_DEPLOY_ROOT / "scout"
LOGS_ROOT = Path("/media/sdcard/logs")

# Live cron (crontab -l, America/New_York)
CRON_SCOUT_INGEST = (
    "15 10 * * * . /home/gary/.config/copernicus/env && "
    "GOOGLE_APPLICATION_CREDENTIALS=/home/gary/.config/copernicus/gcp-sa.json "
    f"{HUGGINGFACE_SPACE_DIR}/scripts/acquire_papers/run_daily_scout_with_ingest.sh"
)

EXAMPLE_GLMP_CIRCUIT_DOC = {
    "circuit_id": "yeast_gal_system",
    "organism": "Saccharomyces cerevisiae",
    "taxon_id": 4932,
    "glmp_class": "III",
    "decoded_at": "2026-06-24T02:15:00Z",
    "mermaid_flowchart": "graph TD\n  GAL4 -->|activates| GAL1\n...",
    "binding_sites": [
        {
            "tf": "GAL4",
            "gene": "GAL1",
            "start": 423,
            "end": 441,
            "qvalue": 0.001,
        }
    ],
    "source_papers": [
        {
            "doi": "10.1093/nar/example",
            "title": "Example paper",
            "firestore_id": "pubmed_example",
        }
    ],
    "source_sequences": [
        {
            "gene": "GAL1",
            "accession": "SGD:S000000224",
            "fasta_path": "/media/sdcard/decoder/sequences/GAL1.fa",
        }
    ],
    "parser_version": "0.2.0",
    "fimo_version": "5.5.9",
    "jaspar_version": "2024_CORE",
    "notes": "",
}

EXAMPLE_SCHEDULER_STATUS_DOC = {
    "job_id": "scout_pubmed_am",
    "last_run_start": "2026-06-24T10:15:00Z",
    "last_run_end": "2026-06-24T10:18:43Z",
    "last_status": "success",
    "last_doc_count": 47,
    "consecutive_failures": 0,
    "total_runs": 312,
    "next_scheduled": "2026-06-25T10:15:00Z",
}
