# GLMP + CopernicusAI — Master To-Do

Hand-maintained priorities with live AUTO-STATUS appended below.
Read alongside: `docs/GLMP_GOALS.md`.

<!-- CURATED:START -->
## Where things stand — 2026-07-23

**Findability pattern (through-line).** Suite checks often ask whether things
*exist*, not whether they are *retrievable*. Three instances this week: junk
vectors polluting retrieval; 405 papers present-but-unembedded; 90 episodes
embedded only on `podcast_jobs` while live `find_nearest` targets `episodes`.

**Post-ingest ordering fix shipped (2026-07-23).** Status publish + MASTER_TODO
now chain from `scout_ingest.sh` on success (`cee1928ef`, CRLF-safe sync
`444d192dd`, asymmetry note `fd585ec75`). Standalone 10:40/10:45 cron **kept**
until AM validates (safer cutover). First evidence = tonight’s PM 20:15
(~21:20); AM double-publish is the cutover gate. PM has no fallback cron
(durable asymmetry — ship risky chain changes in the morning).

**Label fix + episodes gap closed (partial).** Hardcoded `text-embedding-004`
fixed on four handoff sites (`c066ed185`). Episodes: 1536d index READY;
parameterized backfill (`621831bb0`) embedded **90/90** @ 1536;
live `find_nearest` returns sensible topical hits. Dual-field
`description`/`description_markdown` prevents title-only degradation.
**Still open:** embed-at-promote (else 90/90 decays on next promote).

**OpenAI key rotation (Jetson env, 2026-07-23).** Env rewritten from SM
`openai-api-key:latest` (v6); last-8 changed; embed smoke 1536 /
`text-embedding-3-small`. Backup `env.bak.20260723` still holds old key —
**disable old OpenAI key (`…MYQA`) to finish rotation** (re-enable is one click
if PM/AM misbehaves; AM still has publish cron backup). Cloud Run
`copernicus`/`copernicus-api` already use secretKeyRef `latest`. Express
gateway on `copernicus-api` blocks unauthenticated vector-search (Bearer
required; form undocumented in-repo).

**Earlier this week (still true).** Untitled husk sweep 1,543 deleted;
manifest glob-exclusion certified (`d256a0adf`); 405-paper embed backfill
closed (`cfb155f81`); research_focus keystone at glmp `9bb8bd9` (`flagged`
empty pending TSV audit). Decoder honesty / CRP / biologist notes unchanged
below in parked.

## Top priorities (next)
1. **PM chain logs (tonight)** — after ~21:30 ET: ingest OK, hook START/OK near
   completion, wrapper exit 0. First evidence the post-ingest chain fires.
2. **AM double-publish then remove 10:40/10:45 cron** — stale 10:40 then ~11:35
   overwrite; if clean, remove standalone lines (verbatim restore in
   `SCOUT_ARCHITECTURE.md`).
3. **Embed-at-promote** — write 1536d embedding onto `episodes` at promote so
   new episodes don’t strand; pairs with (optional) stop embedding only on
   `podcast_jobs`.
4. **Remaining `embedding_model` hardcodes** — `sync_{glmp,physics,chemistry,cs}_processes.py`,
   `sync_videos.py`, `index_existing_content.py` soft defaults.
5. **8-podcast relabel** — `podcast_jobs` docs labeled 004 with measured dim
   **1536** (by dim, never by label alone). Cosmetic on a collection search
   doesn’t query; demoted.
6. **Math focus file** — after GLMP `research_focus.json`; draft v2 ready.
7. **TSV provenance audit** — flowchart TSV PMIDs mismatched Firestore
   (3-for-3 wrong); produces verified IDs for `research_focus.flagged`.
8. **Disable old OpenAI key (`…MYQA`)** — finishes rotation; inert-izes
   `env.bak.20260723` copy. Decide tonight vs watch-first.
9. **Delete defunct `copernicus` Cloud Run service** — dead since ~Apr 2025;
   still carries `OPENAI_API_KEY` secretKeyRef.
10. **Narrow `copernicus-service` IAM** — project-level `editor` + `run.admin` +
    `storage.admin` + `cloudsql.admin` (plus secretAccessor).
11. **Document Express auth on `copernicus-api`** — Bearer required;
    in-repo subscriber login issues no JWT; can’t self-test API without the
    gateway token.
12. **CRP PWM / sciencevideodb quality / GitHub housekeeping** — prior science
    + Space eval priorities (unchanged leverage).

## Parked / backlog
- Decoder follow-ups: operon re-anchoring; trp LacI motif contamination; σ32
  out of scope; RegulonDB 3-bucket decodability PROVISIONAL/CONFOUNDED.
- Build AraC PWM (recover an evidence-backed ara decode).
- Scout inline-embed on ingest critical path (coverage still reopens each cycle
  until then; scheduled `--auto` slot reserved in post-ingest hooks).
- ~~Backfill docstring + StructuralError~~ — done in `621831bb0`.
- Parked: `text-embedding-3-large` evaluation.
- Deferred free-key rotations: YouTube, Zenodo, NASA-ADS.
- copernicusai-tts IAM too broad — tighten.
- Descript API parallel experiment (never replace ElevenLabs).
- Rename papers-database-table.html → metadata-database.html.
- Biologist engagement: Lents after Krampis; widen pool.

## Reminder to self
Gary is a logician, not a biologist. Biological claims (bucket assignments, mechanism, PWM
site quality) require a qualified biologist. The evolutionary-complexity hypothesis stays a
downstream test OUTPUT, never a decoder-design INPUT.
<!-- CURATED:END -->

---

## AUTO-STATUS

AUTO-GENERATED 2026-07-05T22:30:00-04:00 — rebuilt each run.

### CopernicusAI corpus

| Signal | Value |
|--------|-------|
| Paper count | **62,312** |
| Status source | `knowledge-engine-status.json` on GCS (`count_source: api`) |
| Status JSON `last_updated` | 2026-07-03T13:04:47Z |
| Embedding coverage | 59,499 / 62,312 (97.26%) |
| GLMP v2 processes (metadata) | 217 |
| Last scout run (status JSON) | ⚠️ not published in `knowledge-engine-status.json` |
| Last scout run (Jetson logs) | pubmed_am log mtime **2026-07-05 10:15 ET**; ingest log **2026-07-05 11:27 ET** |

### GLMP decoder (8 known circuits — 2026-07-05 re-decode)

Source: Jetson `results/*_logic_20260705.json` (parser fix a9eb66d).

| circuit_id | `dna_topology_class` |
|------------|----------------------|
| `ecoli_lac_operon` | I/II |
| `ecoli_ara_operon` | INSUFFICIENT_EVIDENCE |
| `ecoli_trp_operon` | I/II |
| `ecoli_sos_lexa` | I/II |
| `ecoli_sos_reca` | I/II |
| `ecoli_flhdc_flagellar` | INSUFFICIENT_EVIDENCE |
| `ecoli_lambda_switch` | INSUFFICIENT_EVIDENCE |
| `ecoli_dna_damage_checkpoint` | I/II |

**Class II reachable on any circuit:** no (zero activator PWMs at confidence threshold).

| Batch / queue | Value |
|---------------|-------|
| Last regression summary | `regression_redecode_20260705.json` — **8/8** circuits |
| Queue pending | 0 |
| Queue completed | 17 |
| Queue failed | 0 |
| Last batch decoder log | `batch_decoder_20260705.log` (manual 8-circuit regression run) |
