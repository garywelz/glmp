# Knowledge Engine — Browse linking & papers corpus handoff

**Date:** 2026-07-17  
**Authors / agents:** Cursor (Yoga) with Gary Welz  
**Audience:** Gary, Claude Chat, Claude Code  
**Status:** Frontend live; ops snapshot uploaded; May eval freeze unchanged  

---

## Purpose

Summarize what changed on the Knowledge Engine Browse surface this session, what we measured about the papers corpus, and what is still open for discussion.

---

## 1. Product changes (live on `copernicus-frontend`)

Browse Content cards on `/knowledge-engine` now open real destinations where a safe public URL exists. Pattern: title is an external link (`target="_blank"`); no inventing viewers that do not exist.

| Content | Destination | Rule |
|---|---|---|
| **GLMP processes** | GCS Mermaid viewer `…/glmp-v2/viewer/index.html?process=<chart_id>` | Only `process_family === 'glmp'` + safe id. Other families stay unlinked (table DBs only). |
| **Podcasts (90)** | `https://copernicusai.fyi/episodes/<episode_id>` | Safe slug ids; matches podcast table / `episode_link`. |
| **Papers (~64k)** | DOI → PubMed → arXiv → raw `url` | Same resolver as `papers-database-table.html`. Link only when a field resolves. |

**Papers UX extras**
- Untitled stubs (`title` empty or `"Untitled"`) are **hidden** from Browse cards, with a per-page note.
- Papers pages over-fetch (`limit=50`) so stub-heavy `updated_at` pages still show titled cards.
- “Open full database table” link added for papers (GCS `papers-database-table.html`).

**Code**
- `components/knowledge-engine/ContentBrowser.tsx`
- `components/knowledge-engine/constants.ts` (`PAPERS_DATABASE_TABLE_HREF`)

**Deploys (Cloud Build → Cloud Run `copernicus-frontend`)**

| Commit | Change | Revision |
|---|---|---|
| `cf96e69f8` | Link GLMP Browse cards to viewer | `00037-rkg` (prior) |
| `0793be80f` | Link podcast Browse cards to episode pages | `00038-drx` |
| `9e357b497` | Link papers + hide untitled stubs | **`00039-j9j` (current)** |

**Live URL:** https://copernicus-frontend-phzp4ie2sq-uc.a.run.app/knowledge-engine  

**Not in scope this session**
- next-auth / `useSession` console noise (pre-existing; local `NEXT_PUBLIC_NEXTAUTH_URL` unset).
- Linking math/chemistry/physics/CS/biology process cards to a viewer (no shared interactive viewer).
- Backend browse API changes (papers already returned `doi` / `pmid` / `arxiv_id` / `url`).

---

## 2. Papers corpus measurement (Task 3 — ops snapshot)

### Why
Before linking 64k papers we measured whether identifiers exist. Early Browse pages looked stub-heavy because sort is `updated_at DESC` — not representative of the corpus.

### Artefact (ops only — not a new eval freeze)

| | |
|---|---|
| Local | `C:\Users\garyw\exports\research_papers_20260717.jsonl.gz` |
| GCS snapshot | `gs://regal-scholar-453620-r7-podcast-storage/research_data/snapshots/research_papers_20260717.jsonl.gz` |
| GCS manifest | `gs://regal-scholar-453620-r7-podcast-storage/research_data/manifests/research_papers_20260717.jsonl.gz.sha256` |
| SHA256 | `c241f6371f4613a61e1ac44aea399c8af5858d6ccc8ddbe575eaaadf51d13b23` |
| Exporter | `huggingface-space/scripts/export_research_papers_jsonl.py` |
| Brief | `papers/_task3_snapshot_brief.md` |
| Method notes | `docs/EVAL_FREEZE.md` |

**Do not treat this as replacing** the citable May freeze  
`research_papers_20260526.jsonl.gz` (Zenodo / dense-retrieval paper). That artefact remains the evaluation corpus.

### Headline numbers

| Metric | May 2026-05-26 | July 2026-07-17 |
|---|---:|---:|
| Documents (n) | 59,499 | **64,164** |
| Δ n | — | +4,665 |
| Any link (DOI ∨ PMID ∨ arXiv) | 99.69% | **97.73%** |
| Untitled stubs | 182 (0.31%) | **1,441 (2.25%)** |
| Titled but unlinkable | 0 | 15 (`glmp_flowchart_experiment`) |

**July resolver priority (first hit wins):** DOI 40,495 → arXiv 21,200 → PMID 1,013 → none 1,456.

**Sources still 100% linkable when known:** pubmed, arxiv, crossref, biorxiv, medrxiv, glmp_flowchart.  
**Unlinkable mass:** almost entirely `source=unknown` Untitled stubs (1,441) plus 15 experiment rows.

**Implication for Browse linking:** Frontend opportunistic links are justified — ~98% of the live corpus has a resolvable identifier. Remaining gap is data hygiene (stubs), not missing UI destinations.

---

## 3. Operational notes (for Claude Code / Cursor)

- Yoga now has Application Default Credentials for Firestore (`copernicusai` DB). Export completed in ~40s for 64k docs with `--projection minimal`.
- Background Claude Code (`dontAsk`) could **not** run shell for this job; interactive Claude Code or Cursor with ADC is the workable path.
- Claude Code lane (per `AGENT_ROLES.md`): publishing / HF / polish. Cursor owns Jetson/SSH and multi-file pipeline work. Task 3 (Firestore export + GCS mirror) was done by Cursor on Yoga after ADC login.
- Optional follow-ups Claude Code could own later: HF Space copy polish for Browse behavior; documenting the July ops snapshot in a Space README; **not** silently replacing the May eval freeze.

---

## 4. Open questions for Claude Chat / Gary

1. **Stub cleanup:** Should we delete, quarantine, or stop ingesting `Untitled` / `source=unknown` papers (grew 182 → 1,441)? Browse only hides them.
2. **Browse sort:** Keep `updated_at DESC`, or prefer titled-only / title sort so page 1 is not stub-skewed even before client filter?
3. **Non-GLMP processes:** Leave unlinked, or invent per-family viewers later?
4. **July snapshot role:** Ops/audit only (recommended), or promote to a second evaluation freeze with new SHA in META/Zenodo?
5. **Papers table vs Browse:** Is Browse the discovery surface, or should we push users harder toward `papers-database-table.html`?

---

## 5. Suggested paste for Claude Chat

> We shipped Knowledge Engine Browse links for GLMP charts, all 90 podcasts, and papers (DOI→PubMed→arXiv→url), and hide Untitled paper stubs. Live revision `copernicus-frontend-00039-j9j`. We also took an ops-only Firestore snapshot `research_papers_20260717.jsonl.gz` (n=64,164, 97.73% linkable; stubs up to 1,441). May eval freeze untouched. Full write-up: `copernicus-web/papers/KNOWLEDGE_ENGINE_BROWSE_LINKS_HANDOFF_2026-07-17.md`. Please discuss stub cleanup, browse sort, and whether July should stay ops-only.

---

## 6. File index

| Path | Role |
|---|---|
| `components/knowledge-engine/ContentBrowser.tsx` | Browse UI links + stub hide |
| `components/knowledge-engine/constants.ts` | Papers table href |
| `papers/_task3_snapshot_brief.md` | Task 3 runbook |
| `papers/KNOWLEDGE_ENGINE_BROWSE_LINKS_HANDOFF_2026-07-17.md` | This report |
| `docs/EVAL_FREEZE.md` | Freeze / export / GCS layout |
| `huggingface-space/scripts/export_research_papers_jsonl.py` | Exporter |

---

*End of handoff. No further action required until Gary returns from Claude Chat discussion.*
