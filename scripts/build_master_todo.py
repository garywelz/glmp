#!/usr/bin/env python3
"""
Assemble docs/GLMP_MASTER_TODO.md from live sources and publish to GCS.

Designed for Jetson cron. Never modifies the local glmp working tree — reads
canonical CURATED block via ``git fetch`` + ``git show origin/main:...`` only.
"""
from __future__ import annotations

import argparse
import html as html_module
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

try:
    from google.cloud import storage
except ImportError:
    storage = None  # type: ignore

# ── Jetson paths (override via env for local testing) ─────────────────────────

GLMP_REPO = Path("/media/sdcard/glmp")
GIT_PATH = "docs/GLMP_MASTER_TODO.md"
SA_KEY = Path("/home/gary/.config/copernicus/gcp-sa.json")
# Option B two-bucket split (2026-07-06): private TODO md, public status HTML + corpus JSON.
GCS_PUBLIC_BUCKET = "regal-scholar-453620-r7-podcast-storage"
GCS_PRIVATE_BUCKET = "regal-scholar-453620-r7-internal"
GCS_TODO_OBJECT = "GLMP_MASTER_TODO.md"
GCS_HTML_OBJECT = "GLMP_STATUS.html"
PUBLIC_STATUS_URL = (
    f"https://storage.googleapis.com/{GCS_PUBLIC_BUCKET}/{GCS_HTML_OBJECT}"
)
LOCAL_DEBUG = Path("/media/sdcard/status/GLMP_MASTER_TODO.md")
LOCAL_DEBUG_HTML = Path("/media/sdcard/status/GLMP_STATUS.html")
CRON_LOG = Path("/media/sdcard/logs/master_todo_cron.log")

DECODER_RESULTS = (
    GLMP_REPO / "collaborations/krampis-virtual-cell/dna-decoder/results"
)
DECODER_QUEUE = GLMP_REPO / "collaborations/krampis-virtual-cell/dna-decoder/queue"
SCOUT_PUBMED_LOG = Path("/media/sdcard/logs/scout_pubmed_am.log")
SCOUT_INGEST_LOGS = (
    Path("/media/sdcard/logs/scout_ingest.log"),
    Path(
        "/home/gdubs/copernicus-web-public/huggingface-space/"
        "paper_acquisition_logs/daily_scout/ingest.log"
    ),
)
BATCH_DECODER_LOG_DIR = Path("/media/sdcard/logs")

STATUS_JSON_BLOB = "knowledge-engine-status.json"
ET = ZoneInfo("America/New_York")

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

CURATED_START = "<!-- CURATED:START -->"
CURATED_END = "<!-- CURATED:END -->"
AUTO_STATUS_HEADING = "## AUTO-STATUS"

# Must never appear on the public HTML status page.
HTML_FORBIDDEN_STRINGS = (
    "CURATED:START",
    "CURATED:END",
    "<!-- CURATED",
    "Nathan Lents",
    "copernicusai-tts",
    "ElevenLabs",
    "YouTube",
    "Zenodo",
    "NASA-ADS",
    "Descript API",
    "IAM too broad",
    "deferred free-key",
    "Krampis's students",
    "Security + consolidation",
    "GitHub-PAT",
    "Top priorities (next)",
    "Parked / backlog",
    "Reminder to self",
)

HEADER = """# GLMP + CopernicusAI — Master To-Do

Hand-maintained priorities with live AUTO-STATUS appended below.
Read alongside: `docs/GLMP_GOALS.md`.
"""


@dataclass
class SourceResult:
    ok: bool
    value: Any = None
    source_time: Optional[str] = None
    error: Optional[str] = None


@dataclass
class RunState:
    stale_sources: List[str] = field(default_factory=list)
    last_good: Dict[str, Any] = field(default_factory=dict)


def log_line(status: str, stale: List[str], html: str = "n/a") -> str:
    ts = datetime.now(ET).strftime("%Y-%m-%d %H:%M:%S %Z")
    stale_part = ",".join(stale) if stale else "none"
    return f"{ts} status={status} stale={stale_part} html={html}"


def append_cron_log(line: str) -> None:
    CRON_LOG.parent.mkdir(parents=True, exist_ok=True)
    with CRON_LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def gcs_client():
    if storage is None:
        raise RuntimeError("google-cloud-storage is not installed")
    return storage.Client.from_service_account_json(str(SA_KEY))


def download_gcs_todo() -> Optional[str]:
    try:
        client = gcs_client()
        blob = client.bucket(GCS_PRIVATE_BUCKET).blob(GCS_TODO_OBJECT)
        if not blob.exists():
            return None
        return blob.download_as_text(encoding="utf-8")
    except Exception:
        return None


def extract_curated_block(text: str) -> Optional[str]:
    if CURATED_START not in text or CURATED_END not in text:
        return None
    start = text.index(CURATED_START)
    end = text.index(CURATED_END) + len(CURATED_END)
    return text[start:end].strip()


def parse_last_good(existing: Optional[str]) -> Dict[str, Any]:
    """Parse fallback values from the current GCS TODO markdown."""
    if not existing:
        return {}
    lg: Dict[str, Any] = {}
    curated = extract_curated_block(existing)
    if curated:
        lg["curated_block"] = curated

    def table_cell(label: str) -> Optional[str]:
        m = re.search(
            rf"\|\s*{re.escape(label)}\s*\|\s*(.+?)\s*\|",
            existing,
        )
        return m.group(1).strip() if m else None

    for key, label in [
        ("paper_count", "Paper count"),
        ("status_source", "Status source"),
        ("status_last_updated", "Status JSON `last_updated`"),
        ("embedding_coverage", "Embedding coverage"),
        ("glmp_v2_processes", "GLMP v2 processes (metadata)"),
        ("scout_last_run", "Last scout run"),
        ("class_ii_reachable", "Class II reachable on any circuit"),
        ("regression_summary", "Last regression summary"),
        ("queue_pending", "Queue pending"),
        ("queue_completed", "Queue completed"),
        ("queue_failed", "Queue failed"),
        ("batch_decoder_log", "Last batch decoder log"),
        ("decoder_source_note", "decoder_source_note"),
    ]:
        val = table_cell(label)
        if val:
            lg[key] = val

    circuits = {}
    for cid in REGRESSION_CIRCUITS:
        m = re.search(
            rf"\|\s*`{re.escape(cid)}`\s*\|\s*(.+?)\s*\|",
            existing,
        )
        if m:
            circuits[cid] = m.group(1).strip()
    if circuits:
        lg["circuits"] = circuits

    m = re.search(r"Source: Jetson `(.+?)`", existing)
    if m:
        lg["decoder_source_note"] = m.group(1)

    m = re.search(
        r"### GLMP decoder \(8 known circuits — (.+?)\)",
        existing,
    )
    if m:
        lg["decoder_decode_date"] = m.group(1)

    return lg


def fetch_curated_from_git() -> SourceResult:
    try:
        subprocess.run(
            ["git", "-C", str(GLMP_REPO), "fetch", "origin", "main"],
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
        proc = subprocess.run(
            ["git", "-C", str(GLMP_REPO), "show", f"origin/main:{GIT_PATH}"],
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        block = extract_curated_block(proc.stdout)
        if not block:
            return SourceResult(False, error="CURATED markers missing in git show output")
        return SourceResult(True, block, datetime.now(ET).isoformat())
    except Exception as exc:
        return SourceResult(False, error=str(exc))


def read_corpus_status() -> SourceResult:
    try:
        client = gcs_client()
        text = (
            client.bucket(GCS_PUBLIC_BUCKET)
            .blob(STATUS_JSON_BLOB)
            .download_as_text(encoding="utf-8")
        )
        data = json.loads(text)
        return SourceResult(
            True,
            {
                "papers": data.get("papers"),
                "last_updated": data.get("last_updated"),
                "count_source": data.get("count_source", "api"),
                "papers_with_embedding": data.get("papers_with_embedding"),
                "papers_embedding_coverage_percent": data.get(
                    "papers_embedding_coverage_percent"
                ),
                "glmp_v2_processes": (data.get("process_databases") or {}).get(
                    "glmp_v2"
                ),
            },
            data.get("last_updated"),
        )
    except Exception as exc:
        return SourceResult(False, error=str(exc))


def _log_mtime(path: Path) -> Optional[str]:
    if path.is_file():
        ts = datetime.fromtimestamp(path.stat().st_mtime, tz=ET)
        return ts.strftime("%Y-%m-%d %H:%M ET")
    return None


def read_scout_freshness() -> SourceResult:
    try:
        pubmed_success = None
        if SCOUT_PUBMED_LOG.is_file():
            for line in reversed(SCOUT_PUBMED_LOG.read_text(encoding="utf-8", errors="replace").splitlines()):
                if "scout_pubmed_am success" in line.lower():
                    pubmed_success = line.strip()
                    break
        ingest_mtime = None
        for p in SCOUT_INGEST_LOGS:
            mt = _log_mtime(p)
            if mt:
                ingest_mtime = mt
                break
        if not pubmed_success and not ingest_mtime:
            return SourceResult(False, error="no scout log data")
        return SourceResult(
            True,
            {"pubmed_success": pubmed_success, "ingest_mtime": ingest_mtime},
            _log_mtime(SCOUT_PUBMED_LOG),
        )
    except Exception as exc:
        return SourceResult(False, error=str(exc))


def _newest_logic_json(circuit_id: str) -> Optional[Path]:
    matches = sorted(
        DECODER_RESULTS.glob(f"{circuit_id}_logic_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return matches[0] if matches else None


def read_decoder_circuits() -> SourceResult:
    try:
        circuits: Dict[str, str] = {}
        newest_name = None
        newest_mtime = 0.0
        for cid in REGRESSION_CIRCUITS:
            path = _newest_logic_json(cid)
            if not path:
                return SourceResult(False, error=f"missing logic json for {cid}")
            with path.open(encoding="utf-8") as fh:
                data = json.load(fh)
            circuits[cid] = data.get("dna_topology_class", "?")
            mt = path.stat().st_mtime
            if mt > newest_mtime:
                newest_mtime = mt
                newest_name = path.name
        decode_date = datetime.fromtimestamp(newest_mtime, tz=ET).strftime("%Y-%m-%d")
        return SourceResult(
            True,
            {"circuits": circuits, "newest_file": newest_name, "decode_date": decode_date},
            datetime.fromtimestamp(newest_mtime, tz=ET).isoformat(),
        )
    except Exception as exc:
        return SourceResult(False, error=str(exc))


def read_queue_counts() -> SourceResult:
    try:
        counts = {}
        for name in ("pending", "completed", "failed"):
            d = DECODER_QUEUE / name
            counts[name] = len(list(d.glob("*.yaml"))) if d.is_dir() else 0
        return SourceResult(True, counts, datetime.now(ET).isoformat())
    except Exception as exc:
        return SourceResult(False, error=str(exc))


def read_regression_summary() -> SourceResult:
    try:
        matches = sorted(
            DECODER_RESULTS.glob("regression_redecode_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not matches:
            return SourceResult(False, error="no regression summary json")
        path = matches[0]
        with path.open(encoding="utf-8") as fh:
            rows = json.load(fh).get("rows", [])
        return SourceResult(
            True,
            {"filename": path.name, "count": len(rows)},
            datetime.fromtimestamp(path.stat().st_mtime, tz=ET).isoformat(),
        )
    except Exception as exc:
        return SourceResult(False, error=str(exc))


def read_batch_decoder_log() -> SourceResult:
    try:
        matches = sorted(
            BATCH_DECODER_LOG_DIR.glob("batch_decoder_*.log"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not matches:
            return SourceResult(False, error="no batch_decoder log")
        path = matches[0]
        note = f"{path.name} (Jetson batch decoder log)"
        return SourceResult(
            True,
            {"filename": path.name, "note": note},
            datetime.fromtimestamp(path.stat().st_mtime, tz=ET).isoformat(),
        )
    except Exception as exc:
        return SourceResult(False, error=str(exc))


def _stale_cell(live: Optional[str], lg_key: str, state: RunState, source: str) -> str:
    if live is not None:
        return live
    state.stale_sources.append(source)
    prev = state.last_good.get(lg_key, "⚠️ unavailable")
    if prev and not str(prev).startswith("⚠️"):
        return f"⚠️ stale — last good: {prev}"
    return str(prev)


def build_auto_status(
    corpus: SourceResult,
    scout: SourceResult,
    decoder: SourceResult,
    queue: SourceResult,
    regression: SourceResult,
    batch_log: SourceResult,
    state: RunState,
) -> str:
    now_display = datetime.now(ET).isoformat(timespec="seconds")

    lg = state.last_good
    cdata = corpus.value if corpus.ok and isinstance(corpus.value, dict) else {}
    sdata = scout.value if scout.ok and isinstance(scout.value, dict) else {}
    ddata = decoder.value if decoder.ok and isinstance(decoder.value, dict) else {}
    qdata = queue.value if queue.ok and isinstance(queue.value, dict) else {}
    rdata = regression.value if regression.ok and isinstance(regression.value, dict) else {}
    bdata = batch_log.value if batch_log.ok and isinstance(batch_log.value, dict) else {}

    papers = cdata.get("papers")
    if isinstance(papers, int):
        paper_cell = f"**{papers:,}**"
    elif lg.get("paper_count"):
        state.stale_sources.append("corpus.papers")
        paper_cell = f"⚠️ stale — last good: {lg['paper_count']}"
    else:
        state.stale_sources.append("corpus.papers")
        paper_cell = "⚠️ unavailable"

    last_upd = cdata.get("last_updated")
    if last_upd:
        last_upd_cell = last_upd
    else:
        state.stale_sources.append("corpus.last_updated")
        last_upd_cell = _stale_cell(None, "status_last_updated", state, "corpus.last_updated")

    emb = cdata.get("papers_with_embedding")
    papers_total = cdata.get("papers")
    if emb is not None and papers_total:
        pct = cdata.get("papers_embedding_coverage_percent")
        if pct is None and papers_total:
            pct = round(100.0 * emb / papers_total, 2)
        emb_cell = f"{emb:,} / {papers_total:,} ({pct}%)"
    elif lg.get("embedding_coverage"):
        state.stale_sources.append("corpus.embedding")
        emb_cell = f"⚠️ stale — last good: {lg['embedding_coverage']}"
    else:
        state.stale_sources.append("corpus.embedding")
        emb_cell = "⚠️ unavailable"

    glmp_v2 = cdata.get("glmp_v2_processes")
    if glmp_v2 is not None:
        glmp_v2_cell = str(glmp_v2)
    elif lg.get("glmp_v2_processes"):
        state.stale_sources.append("corpus.glmp_v2")
        glmp_v2_cell = f"⚠️ stale — last good: {lg['glmp_v2_processes']}"
    else:
        state.stale_sources.append("corpus.glmp_v2")
        glmp_v2_cell = "⚠️ unavailable"

    pubmed_line = sdata.get("pubmed_success")
    ingest_mt = sdata.get("ingest_mtime")
    if pubmed_line or ingest_mt:
        parts = []
        if pubmed_line:
            parts.append(f"pubmed_am success **{pubmed_line}**")
        if ingest_mt:
            parts.append(f"ingest log **{ingest_mt}**")
        scout_cell = "; ".join(parts)
    else:
        prev = lg.get("scout_last_run") or lg.get("scout_jetson_logs")
        if prev:
            state.stale_sources.append("scout")
            scout_cell = f"⚠️ stale — last good: {prev}"
        else:
            state.stale_sources.append("scout")
            scout_cell = "⚠️ unavailable"

    circuits = ddata.get("circuits") if ddata else None
    decoder_stale = not decoder.ok
    if decoder_stale:
        state.stale_sources.append("decoder.circuits")
        circuits = lg.get("circuits", {})
    decode_date = (
        ddata.get("decode_date") if ddata else lg.get("decoder_decode_date", "unknown")
    )
    newest_file = (
        ddata.get("newest_file") if ddata else lg.get("decoder_source_note", "*_logic_*.json")
    )

    circuit_rows = []
    for cid in REGRESSION_CIRCUITS:
        cls = (circuits or {}).get(cid)
        if cls and not decoder_stale:
            circuit_rows.append(f"| `{cid}` | {cls} |")
        elif cls:
            circuit_rows.append(f"| `{cid}` | ⚠️ stale — last good: {cls} |")
        else:
            state.stale_sources.append(f"decoder.{cid}")
            prev = (lg.get("circuits") or {}).get(cid, "⚠️ unavailable")
            circuit_rows.append(f"| `{cid}` | ⚠️ stale — last good: {prev} |")

    any_ii = any(v == "II" for v in (circuits or {}).values())
    if circuits and not decoder_stale:
        class_ii_line = (
            "**Class II reachable on any circuit:** yes"
            if any_ii
            else "**Class II reachable on any circuit:** no (zero activator PWMs at confidence threshold)."
        )
    elif lg.get("class_ii_reachable"):
        state.stale_sources.append("decoder.class_ii")
        class_ii_line = f"⚠️ stale — last good: {lg['class_ii_reachable']}"
    else:
        state.stale_sources.append("decoder.class_ii")
        class_ii_line = "⚠️ Class II reachability unavailable"

    def queue_cell(key: str, qkey: str) -> str:
        val = qdata.get(qkey)
        if val is not None:
            return str(val)
        lgk = f"queue_{qkey}"
        if lg.get(lgk):
            state.stale_sources.append(f"queue.{qkey}")
            return f"⚠️ stale — last good: {lg[lgk]}"
        state.stale_sources.append(f"queue.{qkey}")
        return "⚠️ unavailable"

    if rdata.get("filename"):
        reg_cell = f"`{rdata['filename']}` — **{rdata.get('count', '?')}/{len(REGRESSION_CIRCUITS)}** circuits"
    elif lg.get("regression_summary"):
        state.stale_sources.append("regression")
        reg_cell = f"⚠️ stale — last good: {lg['regression_summary']}"
    else:
        state.stale_sources.append("regression")
        reg_cell = "⚠️ unavailable"

    if bdata.get("note"):
        batch_cell = bdata["note"]
    elif lg.get("batch_decoder_log"):
        state.stale_sources.append("batch_log")
        batch_cell = f"⚠️ stale — last good: {lg['batch_decoder_log']}"
    else:
        state.stale_sources.append("batch_log")
        batch_cell = "⚠️ unavailable"

    count_source = cdata.get("count_source", "api")
    status_source = f"`knowledge-engine-status.json` on GCS (`count_source: {count_source}`)"

    lines = [
        "---",
        "",
        "## AUTO-STATUS",
        "",
        f"AUTO-GENERATED {now_display} — rebuilt each run.",
        "",
        "### CopernicusAI corpus",
        "",
        "| Signal | Value |",
        "|--------|-------|",
        f"| Paper count | {paper_cell} |",
        f"| Status source | {status_source} |",
        f"| Status JSON `last_updated` | {last_upd_cell} |",
        f"| Embedding coverage | {emb_cell} |",
        f"| GLMP v2 processes (metadata) | {glmp_v2_cell} |",
        f"| Last scout run | {scout_cell} |",
        "",
        f"### GLMP decoder (8 known circuits — {decode_date} re-decode)",
        "",
        f"Source: Jetson `results/{newest_file}` (newest per circuit).",
        "",
        "| circuit_id | `dna_topology_class` |",
        "|------------|----------------------|",
        *circuit_rows,
        "",
        class_ii_line,
        "",
        "| Batch / queue | Value |",
        "|---------------|-------|",
        f"| Last regression summary | {reg_cell} |",
        f"| Queue pending | {queue_cell('pending', 'pending')} |",
        f"| Queue completed | {queue_cell('completed', 'completed')} |",
        f"| Queue failed | {queue_cell('failed', 'failed')} |",
        f"| Last batch decoder log | {batch_cell} |",
        "",
    ]
    return "\n".join(lines)


def assemble_document(curated_block: str, auto_status: str) -> str:
    return HEADER + "\n" + curated_block + "\n\n" + auto_status


def validate_document(text: str) -> Tuple[bool, str]:
    if not text or len(text.strip()) < 200:
        return False, "document too short or empty"
    if CURATED_START not in text or CURATED_END not in text:
        return False, "CURATED markers missing"
    if AUTO_STATUS_HEADING not in text:
        return False, "AUTO-STATUS section missing"
    if "AUTO-GENERATED" not in text:
        return False, "AUTO-GENERATED header missing"
    return True, "ok"


def extract_auto_status_section(document: str) -> Optional[str]:
    if AUTO_STATUS_HEADING not in document:
        return None
    start = document.index(AUTO_STATUS_HEADING)
    return document[start:].strip()


def _inline_md(text: str) -> str:
    """Minimal inline markdown: **bold**, `code`, plain escape."""
    text = html_module.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def render_auto_status_html(auto_status_md: str) -> str:
    """Render AUTO-STATUS markdown subset to self-contained HTML."""
    body_parts: List[str] = []
    table_rows: List[List[str]] = []
    in_table = False

    def flush_table() -> None:
        nonlocal in_table, table_rows
        if not table_rows:
            in_table = False
            return
        html_rows = []
        for i, row in enumerate(table_rows):
            tag = "th" if i == 0 else "td"
            cells = "".join(f"<{tag}>{_inline_md(c)}</{tag}>" for c in row)
            html_rows.append(f"<tr>{cells}</tr>")
        body_parts.append("<table>" + "".join(html_rows) + "</table>")
        table_rows = []
        in_table = False

    for raw in auto_status_md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush_table()
            continue
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(set(c) <= {"-", ":", " "} for c in cells):
                continue
            table_rows.append(cells)
            in_table = True
            continue
        flush_table()
        if line.startswith("### "):
            body_parts.append(f"<h3>{_inline_md(line[4:])}</h3>")
        elif line.startswith("## "):
            body_parts.append(f"<h2>{_inline_md(line[3:])}</h2>")
        elif line.startswith("---"):
            continue
        else:
            body_parts.append(f"<p>{_inline_md(line)}</p>")

    flush_table()

    generated = ""
    for part in body_parts:
        if part.startswith("<p>AUTO-GENERATED"):
            generated = part
            break

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GLMP / CopernicusAI — Live Status</title>
<style>
body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 2rem; line-height: 1.5; color: #1a1a1a; max-width: 960px; }}
h1 {{ font-size: 1.5rem; margin-bottom: 0.25rem; }}
.subtitle {{ color: #555; margin-bottom: 1.5rem; }}
h2 {{ font-size: 1.15rem; margin-top: 1.75rem; border-bottom: 1px solid #ddd; padding-bottom: 0.25rem; }}
h3 {{ font-size: 1rem; margin-top: 1.25rem; }}
table {{ border-collapse: collapse; width: 100%; margin: 0.75rem 0 1rem; font-size: 0.92rem; }}
th, td {{ border: 1px solid #ccc; padding: 0.45rem 0.6rem; text-align: left; vertical-align: top; }}
th {{ background: #f4f4f4; }}
code {{ background: #f6f6f6; padding: 0.1em 0.35em; border-radius: 3px; font-size: 0.9em; }}
strong {{ font-weight: 600; }}
</style>
</head>
<body>
<h1>GLMP / CopernicusAI — Live Status</h1>
<p class="subtitle">Non-sensitive operational snapshot (AUTO-STATUS only). Updated by Jetson cron.</p>
{generated}
{"".join(p for p in body_parts if p != generated)}
</body>
</html>
"""


def validate_html_safe(html: str) -> Tuple[bool, str]:
    if not html or len(html.strip()) < 300:
        return False, "html too short or empty"
    if "AUTO-GENERATED" not in html or "CopernicusAI corpus" not in html:
        return False, "AUTO-STATUS content missing from html"
    lower = html.lower()
    for forbidden in HTML_FORBIDDEN_STRINGS:
        if forbidden.lower() in lower:
            return False, f"forbidden string present: {forbidden!r}"
    return True, "ok"


def publish_private_todo(content: str) -> None:
    client = gcs_client()
    blob = client.bucket(GCS_PRIVATE_BUCKET).blob(GCS_TODO_OBJECT)
    blob.upload_from_string(content, content_type="text/markdown")


def publish_public_html(html: str) -> None:
    client = gcs_client()
    blob = client.bucket(GCS_PUBLIC_BUCKET).blob(GCS_HTML_OBJECT)
    blob.upload_from_string(html, content_type="text/html; charset=utf-8")
    blob.acl.all().grant_read()
    blob.acl.save()


def write_local_debug(content: str) -> None:
    LOCAL_DEBUG.parent.mkdir(parents=True, exist_ok=True)
    LOCAL_DEBUG.write_text(content, encoding="utf-8")


def write_local_debug_html(content: str) -> None:
    LOCAL_DEBUG_HTML.parent.mkdir(parents=True, exist_ok=True)
    LOCAL_DEBUG_HTML.write_text(content, encoding="utf-8")


def run(dry_run: bool = False) -> int:
    state = RunState()
    existing = download_gcs_todo()
    state.last_good = parse_last_good(existing)

    curated_src = fetch_curated_from_git()
    if curated_src.ok:
        curated_block = curated_src.value
    elif state.last_good.get("curated_block"):
        curated_block = state.last_good["curated_block"]
        state.stale_sources.append("curated.git")
    else:
        append_cron_log(log_line("failed", ["curated"], "aborted"))
        print("ERROR: CURATED fetch failed and no GCS fallback", file=sys.stderr)
        return 1

    corpus = read_corpus_status()
    scout = read_scout_freshness()
    decoder = read_decoder_circuits()
    queue = read_queue_counts()
    regression = read_regression_summary()
    batch_log = read_batch_decoder_log()

    auto_status = build_auto_status(
        corpus, scout, decoder, queue, regression, batch_log, state
    )
    document = assemble_document(curated_block, auto_status)
    ok, reason = validate_document(document)
    if not ok:
        append_cron_log(
            log_line("validation_failed", state.stale_sources + [reason], "aborted")
        )
        print(f"ERROR: validation failed: {reason}", file=sys.stderr)
        return 1

    auto_section = extract_auto_status_section(document)
    html_status = "skipped"
    html_content = None
    if auto_section:
        try:
            html_content = render_auto_status_html(auto_section)
            html_ok, html_reason = validate_html_safe(html_content)
            if not html_ok:
                print(f"ERROR: HTML guard failed: {html_reason}", file=sys.stderr)
                html_status = "aborted"
                html_content = None
        except Exception as exc:
            print(f"ERROR: HTML render failed: {exc}", file=sys.stderr)
            html_status = "aborted"
            html_content = None
    else:
        html_status = "aborted"

    write_local_debug(document)
    if html_content:
        write_local_debug_html(html_content)

    overall = "fresh" if not state.stale_sources else "degraded"

    if dry_run:
        line = log_line(overall, sorted(set(state.stale_sources)), "skipped")
        print(
            f"dry-run: wrote {LOCAL_DEBUG} ({len(document)} bytes), "
            f"html debug {LOCAL_DEBUG_HTML if html_content else 'n/a'}, skipped GCS upload"
        )
        if html_content:
            hits = [s for s in HTML_FORBIDDEN_STRINGS if s.lower() in html_content.lower()]
            print(f"html guard grep: {len(hits)} forbidden hits ({'PASS' if not hits else 'FAIL'})")
        append_cron_log(line + " mode=dry-run")
        return 0

    try:
        publish_private_todo(document)
    except Exception as exc:
        append_cron_log(
            log_line("upload_failed", state.stale_sources + [str(exc)], html_status)
        )
        print(f"ERROR: private TODO upload failed: {exc}", file=sys.stderr)
        return 1

    if html_content:
        try:
            publish_public_html(html_content)
            html_status = "published"
        except Exception as exc:
            print(f"ERROR: HTML upload failed (TODO ok): {exc}", file=sys.stderr)
            html_status = "aborted"

    line = log_line(overall, sorted(set(state.stale_sources)), html_status)
    append_cron_log(line)
    print(
        f"published gs://{GCS_PRIVATE_BUCKET}/{GCS_TODO_OBJECT} ({len(document)} bytes)"
    )
    if html_status == "published":
        print(f"published {PUBLIC_STATUS_URL} ({len(html_content)} bytes)")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Build and publish GLMP_MASTER_TODO.md")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Assemble local debug copy only; no GCS upload",
    )
    args = parser.parse_args()
    sys.exit(run(dry_run=args.dry_run))


if __name__ == "__main__":
    main()
