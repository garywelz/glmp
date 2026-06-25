# Jetson Phase 2 Split Scouts — Handoff Report (Evening)

**Date:** 2026-06-24 (evening)  
**Jetson:** `gary@192.168.1.222`  
**Yoga 9i:** `C:\Users\garyw\glmp`  
**Prepared for:** Cursor and Claude Code

**Prior docs:** [`JETSON_DECODER_HANDOFF_2026-06-24.md`](JETSON_DECODER_HANDOFF_2026-06-24.md) (decoder + morning scout), [`jetson/scout/README.md`](jetson/scout/README.md)

---

## Executive summary

Phase 2 split scouts are **deployed, manually tested (AM + PM), cron-installed, and live**. The old 10:15 AM monolith (`run_daily_scout_with_ingest.sh`) has been **replaced** by staggered split scouts + `scout_ingest.sh`.

**First automated cron run:** tomorrow **10:15 AM ET** (`scout_pubmed_am`).

---

## Critical terminology: `am` / `pm`

| Argument | Meaning | NOT |
|----------|---------|-----|
| `am` | Morning cron slot | A PubMed topic or subject area |
| `pm` | Evening cron slot | A biology domain shorthand |

Search content comes from `daily_scout_config.json` (existing acquire scripts). Optional GLMP extra PubMed queries use `query_terms.py` + `glmp_pubmed_supplement.py` — unrelated to `am`/`pm`.

---

## What was built

### Phase 1 — Scheduler (`/media/sdcard/scheduler/`)

| File | Purpose |
|------|---------|
| `firestore_config.py` | Project `regal-scholar-453620-r7`, db `copernicusai` |
| `setup_firestore_collections.py` | Seeds `glmp_circuits/_schema`, `scheduler_status/_schema` |
| `scheduler/status_writer.py` | Heartbeats → `scheduler_status/{job_id}` |
| `check_scout_status.py` | CLI to print all scout status docs |

### Phase 2 — Split scouts (`/media/sdcard/scheduler/scout/`)

| File | Purpose |
|------|---------|
| `scout_pubmed.py` | PubMed (~600/run) + optional GLMP supplement |
| `scout_biorxiv.py` | BioRxiv/MedRxiv (~250/run) |
| `scout_arxiv.py` | arXiv (~150/run) |
| `scout_common.py` | Locks, subprocess wrappers, Firestore status |
| `scout_ingest.sh` | Push local JSON → Firestore **`research_papers`** |
| `query_terms.py` | GLMP PubMed query clusters 1–3 |
| `glmp_pubmed_supplement.py` | Extra PubMed searches for GLMP terms |

---

## Cron schedule (installed, active)

```cron
CRON_TZ=America/New_York

10 10 * * *  remind_paper_scout_coffee.sh

# AM round
15 10 * * *  scout_pubmed.py am   → /media/sdcard/logs/scout_pubmed_am.log
20 10 * * *  scout_biorxiv.py am  → /media/sdcard/logs/scout_biorxiv_am.log
25 10 * * *  scout_arxiv.py am    → /media/sdcard/logs/scout_arxiv_am.log
30 10 * * *  scout_ingest.sh      → /media/sdcard/logs/scout_ingest.log

# PM round
0  20 * * *  scout_pubmed.py pm   → /media/sdcard/logs/scout_pubmed_pm.log
5  20 * * *  scout_biorxiv.py pm  → /media/sdcard/logs/scout_biorxiv_pm.log
10 20 * * *  scout_arxiv.py pm    → /media/sdcard/logs/scout_arxiv_pm.log
15 20 * * *  scout_ingest.sh      → /media/sdcard/logs/scout_ingest.log
```

**9 jobs total.** Monolith removed.

---

## Manual test results (2026-06-24)

### Scouts — acquire logs (ground truth)

| Scout | Exit | Papers processed (acquire log) | Firestore `last_doc_count` |
|-------|------|------------------------------|----------------------------|
| `scout_pubmed_am` | ✅ | 75 | 75 |
| `scout_biorxiv_am` | ✅ | 60 | 0 |
| `scout_arxiv_am` | ✅ | 150 | 0 |
| `scout_pubmed_pm` | ✅ | 0 (same-day repeat) | 0 |
| `scout_biorxiv_pm` | ✅ | 0 | 0 |
| `scout_arxiv_pm` | ✅ | 0 | 0 |

**Why bioRxiv/arXiv show `last_doc_count=0`:** heartbeat counts **new JSON files on disk** (before − after). Morning monolith had already written those files; PM/same-day re-runs update in place without new files.

**Do not confuse** `last_doc_count` with Firestore ingest writes or acquire “target” budget.

### Ingest — two separate runs today

| Run | Log file | Wrote | Skipped | Failed |
|-----|----------|-------|---------|--------|
| **10:15 AM monolith** | `paper_acquisition_logs/daily_scout/ingest.log` | **143** | 48,222 | 0 |
| **Split-scout manual ingest** | `/media/sdcard/logs/scout_ingest.log` | **79** | 48,362 | 0 |

The **79** is the correct count for the Phase 2 AM round ingest (mostly PubMed net-new after morning). Claude Code briefly misread the monolith log as the split-scout result.

`scout_ingest.sh` does **not** write `scheduler_status/scout_ingest_*` docs.

---

## Firestore status schema

Each scout writes `scheduler_status/{job_id}`:

```json
{
  "job_id": "scout_pubmed_am",
  "last_status": "success",
  "last_doc_count": 75,
  "total_runs": 1,
  "consecutive_failures": 0
}
```

**Check all scouts:**

```bash
ssh gary@192.168.1.222 "
  source ~/.config/copernicus/env
  export GOOGLE_APPLICATION_CREDENTIALS=~/.config/copernicus/gcp-sa.json
  /media/sdcard/copernicus-worker/venv/bin/python3.8 \
    /media/sdcard/scheduler/check_scout_status.py
"
```

Repo path: `collaborations/krampis-virtual-cell/jetson/check_scout_status.py`  
Jetson path: `/media/sdcard/scheduler/check_scout_status.py` (deploy with `deploy_phase2.sh`)

---

## Repo state (`garywelz/glmp`, `main`)

| Commit | Message |
|--------|---------|
| `163afe8` | Add `check_scout_status.py` |
| `40cab79` | Force LF for `.sh` and `.py` (`.gitattributes`) |
| `829943a` | Consolidated decoder + scout handoff |
| `3745ba4` | Phase 2 split scout workers |
| `d4df03c` | Phase 1 scheduler + Firestore bootstrap |

---

## Infrastructure snapshot

| Item | Location | Status |
|------|----------|--------|
| SD card (ext4, ~117 GB) | `/media/sdcard` | ~3.6 GB used, ~108 GB free |
| eMMC | `/` | ~8.4 GB used, ~4.6 GB free |
| Copernicus repo | `/media/sdcard/copernicus-worker/copernicus-web` | ✅ |
| Scout venv | `.../paper_acquisition_venv` (Python 3.8) | ✅ |
| Scheduler | `/media/sdcard/scheduler/` | ✅ |
| Logs | `/media/sdcard/logs/` | ✅ |
| GCP key | `~/.config/copernicus/gcp-sa.json` | ✅ |
| DNA decoder | `/media/sdcard/decoder/` | ✅ (see morning handoff) |
| MEME/FIMO | `/media/sdcard/miniforge3/envs/meme-env` | ✅ v5.5.9 |

---

## Known issues / TODOs

1. **CRLF on deploy** — fixed in git via `.gitattributes`; if an old copy exists on Jetson: `sed -i 's/\r//' /media/sdcard/scheduler/scout/scout_ingest.sh`
2. **Python 3.8 EOL** — Google libs warn every run; plan venv upgrade to 3.10+
3. **BioRxiv `last_doc_count=0`** — expected on same-day re-run; verify acquire logs if concerned, not `query_terms.py` for `am`/`pm`
4. **GLMP PubMed supplement** — not tested on cron yet (runs add `--no-glmp-queries` or default without supplement in manual tests)
5. **Miniforge installer** — safe to delete: `/media/sdcard/Miniforge3-Linux-aarch64.sh`
6. **Monitor first cron day** — tomorrow 10:15–10:30 ET; `tail -f` must be run locally (non-interactive SSH blocks on `-f`)

---

## What’s next

### Scout (monitoring)

1. **Tomorrow AM** — confirm first cron cycle in `/media/sdcard/logs/scout_*_am.log`
2. **Tomorrow PM** — confirm 20:00–20:15 cycle
3. **Optional** — enable GLMP PubMed supplement on one manual run before adding to cron

### Decoder Phase 3 (Cursor / Yoga)

1. YAML manifests (lac, ara, trp) → `run_batch.py` + `firestore_writer.py`
2. Wire decoder → `glmp_circuits` collection
3. See [`dna-decoder/CURSOR_BRIEFING_DECODER_AUTOMATION.md`](dna-decoder/CURSOR_BRIEFING_DECODER_AUTOMATION.md)

### Other

- RegulonDB manual download → `/media/sdcard/decoder/motifs/regulondb/`
- TrpR PWM refinement (PDB 1QP0)
- Lac operon expert review — [`lac-operon-annotation-review.md`](lac-operon-annotation-review.md)

---

## Division of labor

| Task | Cursor (Yoga 9i) | Claude Code (Jetson SSH) |
|------|------------------|---------------------------|
| Write scripts / docs | ✅ | — |
| Deploy | `deploy_phase1.sh`, `deploy_phase2.sh` | Verify paths |
| Run scouts / FIMO | — | ✅ |
| Cron changes | Document | ✅ (done) |
| Monitor logs | — | ✅ tomorrow |

---

## Resume in a new chat

```
@JETSON_PHASE2_HANDOFF_2026-06-24.md

Jetson Phase 2 scouts are cron-live. Monolith replaced.
First auto run tomorrow 10:15 AM ET.
Next: monitor cron, then Decoder Phase 3 on Yoga.
```

---

*Gary Welz · GLMP / CopernicusAI · 2026-06-24 evening*
