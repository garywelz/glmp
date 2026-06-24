#!/usr/bin/env python3.8
"""
Shared utilities for split CopernicusAI scout workers (Phase 2).

Wraps existing acquire_*_batch.py scripts in copernicus-web — does not reimplement APIs.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── Path resolution (repo staging or Jetson /media/sdcard/scheduler/scout/) ──

def scheduler_root() -> Path:
    here = Path(__file__).resolve().parent
    if here.name == "scout":
        return here.parent
    return here


def _ensure_import_paths() -> None:
    root = scheduler_root()
    for p in (root, root / "scout"):
        s = str(p)
        if s not in sys.path:
            sys.path.insert(0, s)


_ensure_import_paths()

from firestore_config import (  # noqa: E402
    DEFAULT_CREDENTIALS_PATH,
    HUGGINGFACE_SPACE_DIR,
    LOGS_ROOT,
    VENV_PYTHON,
)

SOURCE_ALIASES = {
    "pubmed": "pubmed",
    "biorxiv": "biorxiv_medrxiv",
    "biorxiv_medrxiv": "biorxiv_medrxiv",
    "arxiv": "arxiv",
}

DEFAULT_CONFIG = HUGGINGFACE_SPACE_DIR / "scripts/acquire_papers/daily_scout_config.json"
PAPERS_ROOT = HUGGINGFACE_SPACE_DIR / "metadata-database/papers"
LOG_DIR = HUGGINGFACE_SPACE_DIR / "paper_acquisition_logs/daily_scout"


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def resolve_python() -> str:
    venv_py = HUGGINGFACE_SPACE_DIR / "paper_acquisition_venv/bin/python3"
    if venv_py.exists():
        return str(venv_py)
    if VENV_PYTHON.exists():
        return str(VENV_PYTHON)
    return sys.executable or "python3"


def load_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    path = config_path or DEFAULT_CONFIG
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def compute_source_target(source_key: str, config: Dict[str, Any]) -> int:
    """Mirror daily_scout_runner.py budget split for a single enabled source."""
    limits = config.get("limits", {})
    base = int(limits.get("papers_per_source_per_run", limits.get("papers_per_source_per_day", 100)))
    total_cap = limits.get("total_papers_per_run", limits.get("total_papers_per_day"))
    weights = limits.get("source_weights", {})

    sources = config.get("sources", {})
    if source_key not in sources or not sources[source_key].get("enabled", False):
        return base

    enabled = [(k, v) for k, v in sources.items() if v.get("enabled", False)]
    n = len(enabled)
    if total_cap is not None and n > 0 and weights:
        enabled_weights = {
            name: max(0.0, float(weights.get(name, cfg.get("budget_weight", 0))))
            for name, cfg in enabled
        }
        total_weight = sum(enabled_weights.values())
        if total_weight > 0 and source_key in enabled_weights:
            weighted = max(1, round(int(total_cap) * enabled_weights[source_key] / total_weight))
            return min(base, weighted)

    if total_cap is not None and n > 0:
        per = max(1, int(total_cap) // n)
        return min(base, per)

    return base


def count_paper_json_files(root: Path) -> int:
    if not root.exists():
        return 0
    n = 0
    for p in root.rglob("*.json"):
        if p.name.startswith("batch_"):
            continue
        n += 1
    return n


def lock_path(source: str, run_type: str) -> Path:
    return Path(f"/tmp/scout_{source}_{run_type}.lock")


def acquire_lock(source: str, run_type: str) -> bool:
    lp = lock_path(source, run_type)
    if lp.exists():
        return False
    lp.write_text(f"pid={os.getpid()} started={iso_now()}\n", encoding="utf-8")
    return True


def release_lock(source: str, run_type: str) -> None:
    lp = lock_path(source, run_type)
    try:
        lp.unlink(missing_ok=True)
    except TypeError:
        if lp.exists():
            lp.unlink()


def write_status(
    job_id: str,
    status: str,
    doc_count: int = 0,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    error_message: Optional[str] = None,
    dry_run: bool = False,
) -> None:
    from scheduler.status_writer import write_job_status

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and DEFAULT_CREDENTIALS_PATH.exists():
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(DEFAULT_CREDENTIALS_PATH)

    write_job_status(
        job_id=job_id,
        status=status,
        doc_count=doc_count,
        start_time=start_time,
        end_time=end_time,
        error_message=error_message,
        dry_run=dry_run,
    )


def acquire_command(source_key: str, count: int, python: str) -> List[str]:
    ap = HUGGINGFACE_SPACE_DIR / "scripts/acquire_papers"
    if source_key == "pubmed":
        return [
            python,
            str(ap / "acquire_pubmed_batch.py"),
            "--recent",
            str(count),
            "--classic",
            "0",
        ]
    if source_key == "biorxiv_medrxiv":
        return [
            python,
            str(ap / "acquire_biorxiv_medrxiv_batch.py"),
            "--recent",
            str(count),
        ]
    if source_key == "arxiv":
        return [
            python,
            str(ap / "acquire_arxiv_batch.py"),
            "--recent",
            str(count),
            "--classic",
            "0",
        ]
    raise ValueError(f"Unknown source: {source_key}")


def run_subprocess(cmd: List[str], log_file: Path, cwd: Path, timeout: int = 3600) -> int:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"\n{'=' * 80}\n")
        log.write(f"{' '.join(cmd)}\n")
        log.write(f"Started: {iso_now()}\n")
        log.write(f"{'=' * 80}\n")
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            stdout=log,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )
        log.write(f"\nExit code: {result.returncode}\n")
        return result.returncode


def run_glmp_pubmed_supplement(python: str, log_file: Path) -> int:
    supplement = Path(__file__).resolve().parent / "glmp_pubmed_supplement.py"
    if not supplement.exists():
        return 0
    return run_subprocess(
        [python, str(supplement)],
        log_file,
        HUGGINGFACE_SPACE_DIR,
        timeout=1800,
    )


def run_ingest(log_file: Path) -> int:
    script = HUGGINGFACE_SPACE_DIR / "scripts/ingest_metadata_to_firestore.sh"
    if not script.exists():
        return 1
    return run_subprocess(["bash", str(script)], log_file, HUGGINGFACE_SPACE_DIR, timeout=7200)


def run_scout(
    source: str,
    run_type: str,
    *,
    with_glmp_queries: bool = False,
    with_ingest: bool = False,
    dry_run_status: bool = False,
    config_path: Optional[Path] = None,
) -> int:
    """
    Run one split scout worker.

    source: pubmed | biorxiv | arxiv
    run_type: am | pm
    """
    source_key = SOURCE_ALIASES.get(source, source)
    job_id = f"scout_{source}_{run_type}"
    start = iso_now()

    LOGS_ROOT.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"{source}_{run_type}_{datetime.now().strftime('%Y%m%d')}.log"
    split_log = LOGS_ROOT / f"scout_{source}_{run_type}.log"

    if not acquire_lock(source, run_type):
        print(f"SKIP: lock exists for {source}/{run_type} ({lock_path(source, run_type)})")
        return 0

    try:
        write_status(job_id, "running", start_time=start, dry_run=dry_run_status)

        config = load_config(config_path)
        count = compute_source_target(source_key, config)
        python = resolve_python()
        json_before = count_paper_json_files(PAPERS_ROOT)

        print(f"Scout {job_id}: target={count} papers, python={python}")

        if dry_run_status:
            print(f"DRY RUN: would run {acquire_command(source_key, count, python)}")
            if with_glmp_queries and source_key == "pubmed":
                print("DRY RUN: would run glmp_pubmed_supplement.py")
            if with_ingest:
                print("DRY RUN: would run ingest_metadata_to_firestore.sh")
            write_status(job_id, "success", doc_count=0, start_time=start, end_time=iso_now(), dry_run=True)
            return 0

        rc = run_subprocess(acquire_command(source_key, count, python), log_file, HUGGINGFACE_SPACE_DIR)
        if rc != 0:
            write_status(
                job_id,
                "failure",
                start_time=start,
                end_time=iso_now(),
                error_message=f"acquire exited {rc}",
            )
            return rc

        if with_glmp_queries and source_key == "pubmed":
            sup_rc = run_glmp_pubmed_supplement(python, log_file)
            if sup_rc != 0:
                write_status(
                    job_id,
                    "failure",
                    start_time=start,
                    end_time=iso_now(),
                    error_message=f"glmp supplement exited {sup_rc}",
                )
                return sup_rc

        json_after = count_paper_json_files(PAPERS_ROOT)
        doc_delta = max(0, json_after - json_before)

        if with_ingest:
            ingest_rc = run_ingest(log_file)
            if ingest_rc != 0:
                write_status(
                    job_id,
                    "failure",
                    doc_count=doc_delta,
                    start_time=start,
                    end_time=iso_now(),
                    error_message=f"ingest exited {ingest_rc}",
                )
                return ingest_rc

        write_status(job_id, "success", doc_count=doc_delta, start_time=start, end_time=iso_now())

        # Mirror key lines to /media/sdcard/logs for cron tailing
        with open(split_log, "a", encoding="utf-8") as sl:
            sl.write(f"{iso_now()} {job_id} success doc_delta={doc_delta}\n")

        return 0

    except subprocess.TimeoutExpired:
        write_status(
            job_id,
            "failure",
            start_time=start,
            end_time=iso_now(),
            error_message="timeout",
        )
        return 1
    except Exception as exc:
        write_status(
            job_id,
            "failure",
            start_time=start,
            end_time=iso_now(),
            error_message=str(exc),
        )
        raise
    finally:
        release_lock(source, run_type)
