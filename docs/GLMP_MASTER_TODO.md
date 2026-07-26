# GLMP + CopernicusAI — Master To-Do

Hand-maintained priorities with live AUTO-STATUS appended below.
Read alongside: `docs/GLMP_GOALS.md`.

<!-- CURATED:START -->
## Where things stand — 2026-07-23

**Findability pattern (through-line).** Suite checks often ask whether things
*exist*, not whether they are *retrievable*. Three instances this week: junk
vectors polluting retrieval; 405 papers present-but-unembedded; 90 episodes
embedded only on `podcast_jobs` while live `find_nearest` targets `episodes`.

**Post-ingest ordering fix shipped and validated (2026-07-23).** Status publish
+ MASTER_TODO chain from `scout_ingest.sh` on success (`cee1928ef`, CRLF-safe
sync `444d192dd`, asymmetry note `fd585ec75`). PM (20:15) and AM (10:30) cycles
both validated post-install; standalone 10:40/10:45 cron removed, the chain is
now the sole trigger. *(Jetson-log-based; Gary/Cursor-reported — I have no SSH
access to independently verify crontab/log state this session.)*

**Label fix + episodes gap closed.** Hardcoded `text-embedding-004` fixed on
four handoff sites (`c066ed185`). Episodes: 1536d index READY; parameterized
backfill (`621831bb0`) embedded **90/90** @ 1536; live `find_nearest` returns
sensible topical hits. Dual-field `description`/`description_markdown`
prevents title-only degradation. **Embed-at-promote fix designed, committed,
and deployed** (`ed618599f`, revision `copernicus-podcast-api-00244-lj6`,
2026-07-24) — carries the embedding already computed at promote forward onto
`episodes` instead of stranding it; verify-pending on the next real promote
(item 18).

**OpenAI key rotation complete (2026-07-23).** Env rewritten from SM
`openai-api-key:latest` (v6); last-8 changed; embed smoke 1536 /
`text-embedding-3-small`. **Old key disabled** — verified directly via
`gcloud secrets versions list openai-api-key`: v6 `enabled`, v1-5 `disabled`.
Cloud Run `copernicus-api` uses secretKeyRef `latest`; the defunct
`copernicus` service (which also carried this secretKeyRef) was deleted
2026-07-23 (verified: `gcloud run services describe copernicus` now errors
"Cannot find service"). Express gateway on `copernicus-api` blocks
unauthenticated vector-search (Bearer required; form undocumented in-repo) —
still open, item 11.

**Earlier this week (still true).** Untitled husk sweep 1,543 deleted;
manifest glob-exclusion certified (`d256a0adf`); 405-paper embed backfill
closed (`cfb155f81`); research_focus keystone at glmp `9bb8bd9` (`flagged`
empty pending TSV audit). Decoder honesty / CRP / biologist notes unchanged
below in parked.

**Credential-shaped file sweep complete (2026-07-23, run by Cursor).** No
credential-shaped files tracked in git across copernicus-web, glmp, or the HF
Space checkouts — history clean too. Yoga 9i + Jetson path scans completed,
paths-only per the standing rule (`AGENT_ROLES.md` credential-handling
section). `/home/gary/.config/copernicus/env.bak.20260723` (held the revoked
key) deleted. `.gitignore` prevention added across all six Space repos +
`mathematics-database`. **Deferred, still open:** untracking ~14k venv paths
in copernicus-web (item 19).

**Governance files staged for Project KB re-sync (2026-07-23).**
`CONSTITUTION.md`, `METHODS_CATALOG.md`, `RESOURCE_MANIFEST.md` copied from
copernicus-web `governance/` (commit `d4a673d5f`; manifest last edited
`fedfae034`) to `C:\Users\garyw\Desktop\kb-sync\` for upload — confirmed the
copies carry the corrected concept DOIs and the new ATAP rows.

**ATAP rename propagation complete (2026-07-24).** `mathematics-database`
renamed to `atap` on HF Hub + GitHub; propagated through copernicus-web and
glmp docs, all three sibling-Space footer links, the atap Space's own
README/cardData/GitHub-About, and `DISCIPLINE_DATABASES_PLAN.md`'s
engine-vs-demonstration-corpus reframing (item 13). Duplicate local checkout
consolidated to `hf-spaces/atap`. **Four discipline stub repos deleted**
(`biology-database`, `chemistry-database`, `computer-science-database`,
`physics-database` — verified 0 forks/stars before deletion, `gh repo view`
now returns "Could not resolve to a Repository" for all four). Still open:
items 14-16 (footer prose relabel, stale allowlist entries, ATAP corpus
git-history depth check).

## Top priorities (next)
1. ~~**PM chain logs (tonight)** — after ~21:30 ET: ingest OK, hook START/OK near
   completion, wrapper exit 0. First evidence the post-ingest chain fires.~~ —
   done, PM cycle validated 2026-07-23 (Gary/Cursor-reported; Jetson logs, not
   independently verified this session).
2. ~~**AM double-publish then remove 10:40/10:45 cron** — stale 10:40 then ~11:35
   overwrite; if clean, remove standalone lines (verbatim restore in
   `SCOUT_ARCHITECTURE.md`).~~ — done, AM validated and standalone cron removed
   (Gary/Cursor-reported; Jetson crontab, not independently verified this
   session).
3. ~~**Deploy embed-at-promote fix (`ed618599f`)** — carries the embedding
   already computed at promote (both auto-promote and manual RSS-submit
   paths) forward onto `episodes` instead of stranding it on `podcast_jobs`;
   gated on 1536d + non-empty `embedding_model`.~~ — deployed 2026-07-24,
   revision `copernicus-podcast-api-00244-lj6` (verified `Ready: True`, 100%
   traffic; `/health` 200; `find_nearest` smoke test against `episodes`
   returned relevant hits). Correctness of the fix itself is still
   VERIFY PENDING on the next real promote (item 18) — deploying it isn't
   the same as proving it.
4. **Remaining `embedding_model` hardcodes** — `sync_{glmp,physics,chemistry,cs}_processes.py`,
   `sync_videos.py`, `index_existing_content.py` soft defaults.
5. ~~**8-podcast relabel** — `podcast_jobs` docs labeled 004 with measured dim
   **1536** (by dim, never by label alone).~~ — done, verified directly via
   Firestore query: 0 docs currently labeled `text-embedding-004` with an
   actual 1536d vector. (46 docs still say `text-embedding-004`, but all 46
   measure genuinely 768d — the separate, already-known legacy Vertex
   vectors, not the mislabeled ones this item was about.)
6. **Math focus file** — after GLMP `research_focus.json`; draft v2 ready.
7. **TSV provenance audit** — flowchart TSV PMIDs mismatched Firestore
   (3-for-3 wrong); produces verified IDs for `research_focus.flagged`.
8. ~~**Disable old OpenAI key (`…MYQA`)**~~ — done, verified via
   `gcloud secrets versions list openai-api-key`: v6 `enabled`, v1-5
   `disabled`.
9. ~~**Delete defunct `copernicus` Cloud Run service**~~ — done 2026-07-23,
   verified: `gcloud run services describe copernicus` now errors "Cannot
   find service."
10. **Narrow `copernicus-service` IAM** — project-level `editor` + `run.admin` +
    `storage.admin` + `cloudsql.admin` (plus secretAccessor).
11. **Document Express auth on `copernicus-api`** — Bearer required;
    in-repo subscriber login issues no JWT; can’t self-test API without the
    gateway token.
12. **CRP PWM / sciencevideodb quality / GitHub housekeeping** — prior science
    + Space eval priorities (unchanged leverage).
13. ~~**DISCIPLINE_DATABASES_PLAN.md rewrite**~~ — done, commit `c7a614529`:
    reframed as engine (ATAP) vs. Methods & Tools demonstration corpus
    (biology/chemistry/CS/physics), against the engine-vs-discipline
    distinction, not find-and-replace.
14. **metadata_database footer prose relabel** —
    `hf-spaces/metadata_database/index.html:34` still reads "serving GLMP, the
    Mathematics Database, and CopernicusAI"; relabel to ATAP.
15. **Prune stale settings.local.json allowlist entries** —
    `copernicus-web/.claude/settings.local.json` has four tool-permission
    entries referencing the deleted `mathematics-database` local paths.
    Harmless, unused, cosmetic.
16. **Git-history depth check on ATAP corpus** —
    `copernicus-web/huggingface-space/mathematics-processes-database/`
    (664 files): commit count, date range, substantive history vs. bulk
    import. Decides subtree-split vs. fresh-commit before migration; a
    provenance defect was already found in `flowchart-source-papers.tsv`
    this week, so recording where content came from has real value.
17. **Pin `copernicus-podcast-api` Dockerfile base image to a digest** —
    currently floating `python:3.11-slim`. The 07-24 deploy pulled a fresh
    base layer ("Downloaded newer image for python:3.11-slim" in the Cloud
    Build log), so a code-only redeploy silently carried a Python patch
    bump too. All smoke tests passed that time, but future rebuilds should
    change only what was intended — pin to a specific digest.
18. **VERIFY PENDING — embed-at-promote** (`ed618599f`, deployed as revision
    `copernicus-podcast-api-00244-lj6`, 2026-07-24). Unproven until the next
    real podcast generation/promote. Check then: the new `episodes` doc has
    `embedding_model` set and a 1536d vector, and surfaces in a
    `find_nearest` query against `episodes`. Do not synthesize a test
    podcast to force this.
19. **Untrack ~14k venv paths in copernicus-web** — deferred from the
    2026-07-23 credential-shaped-file sweep (Cursor); stays open.
20. **PROPOSE — GLMP Daily Brief / Collaborator Window** (design task, not
    built yet). A fetchable status page serving two audiences from one
    artifact: the GLMP project's opening context (collaborator sees current
    project state) and the welcome-package landing surface for
    Krampis/Lents/Me-Me.
    - **Content** (collaborator-facing, *not* the engineering queue): live
      collection counts — research-paper corpus, sciencevideodb, podcasts,
      flowchart/process count; what's available (papers, process flowcharts,
      papers-in-progress); current research state + what changed recently
      (the frontier, in plain terms — reads `research_focus.json`); how to
      contribute (a path for partners to suggest edits to charts, podcasts,
      papers, videos).
    - **Host/mechanism**: GitHub Pages (`garywelz.github.io/glmp`), not GCS —
      renders from the repo, can't drift, updates on push; fetchable at a
      stable URL the GLMP project instructions can pull daily. Counts come
      from live status sources that already exist
      (`knowledge-engine-status.json`, `/api/content/stats`), never
      hand-maintained — a stale brief is worse than none. Generation can ride
      the existing post-ingest chain (`build_master_todo.py` already runs as
      a hook; a collaborator-brief output is a small addition, not new
      machinery).
    - **Not the MASTER_TODO** — engineering items (venv untracking, IAM,
      hardcodes) are noise to a biologist; different audience, different
      document.
    - Queue entry only — design is next session.

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
