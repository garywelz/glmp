# GLMP + CopernicusAI — Master To-Do

Hand-maintained priorities with live AUTO-STATUS appended below.
Read alongside: `docs/GLMP_GOALS.md`.

<!-- CURATED:START -->
## Where things stand — 2026-07-23

**Findability pattern (through-line).** Suite checks often ask whether things
*exist*, not whether they are *retrievable*. Three instances this week: junk
vectors polluting retrieval; 405 papers present-but-unembedded; 90 episodes
embedded only on `podcast_jobs` while live `find_nearest` targets `episodes`.
A periodic check for this pattern is now tracked as item 21.

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
closed (`cfb155f81`); research_focus keystone at glmp `9bb8bd9`. Decoder
honesty / CRP / biologist notes unchanged below in parked.

**FINDING: flowchart-source-papers.tsv provenance is ~54% reliable per-row.**
Diagnostic (2026-07-26, pattern C): of 481 rows, correct-PMID rate ~54%;
DOIs not uniformly safe (mismatches + unresolved); bad rows independently
mis-IDed, no mechanical offset. IMPLICATION: any GLMP text citing chart
sources from this TSV may cite wrong papers — verify before publication.
**QUEUED THREAD:** full re-harvest from `raw_citation` free-text against a
resolver, ~220 rows to correct, own runway (not a quick fix). Seeded
`research_focus.flagged` with 5 verified in-corpus IDs (Jacob/Monod,
cAMP-Crp, attenuation, two QS/activation circuits) — retrieval seed only,
not a bibliography.

**FINDING: `copernicus-api` auth enforcement has no locatable source
(2026-07-26).** Diagnostic: `/api/*` rejects with token-style errors ("No
token provided" / "Authentication failed", reproduced live against the
service), but the enforcing code is not in `cloud-run-backend` source, git
history (`copernicus-web` + `glmp`, full-history search), or Secret Manager
(verified: no `jwt`/`JWT` strings anywhere in the FastAPI app code, no
subscriber- or jwt-named secret exists in the project). The only
`/api/subscribers/login` route returns `{subscriber_id, email, name,
subscription_tier, message}` — no token. So: something in front of or around
the FastAPI app enforces token auth, but its source is not locatable in the
suite's repos or GCP secrets. That unlocatable enforcement is itself the
finding — auth logic with no version-controlled source we can find.
**OPEN QUESTIONS (do not start):** what actually performs the token check
(not found in-repo — could be a proxy, an API Gateway, a separate service, or
config not in these repos); how a valid token is obtained, given login mints
none; whether `/api/vector-search` is reachable by any means today or
effectively locked.

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
now returns "Could not resolve to a Repository" for all four). Items 14-16
(footer prose relabel, stale allowlist entries, ATAP corpus git-history
depth check) since closed.

**Thread fully closed out (2026-07-30).** Live-verified rather than
re-executed: `sciencevideodb` (`7b58d67f9`), `copernicusai` (`904712fdd`),
and `metadata_database` (`b3dbd91`) all confirmed `RUNNING` on HF with
deployed `sha` matching local `HEAD` — no stale `mathematics-database`
Space links remain in any of the three. Also corrected a prior
mischaracterization: the "duplicate local checkout" above wasn't actually
one repo cloned twice — `C:\Users\garyw\atap` (GitHub source repo: docs +
`research_focus.json` only, no README.md) and
`C:\Users\garyw\hf-spaces\atap` (the HF Space checkout) are two distinct
repos serving different purposes, both correctly renamed on disk with
correct remotes. The Space checkout's README (the only one that exists)
was already fully rewritten (`6464185`, 2026-07-23) with zero stale
references. Nothing left open on this thread.

**`math_processes` → `atap_graphs` migration complete (2026-07-27).** Full
gated migration, verified at every phase, in `copernicus-web`:
- **Writer #1** fixed and fail-loud (`f8a85bcbc`): `sync_math_processes.py`
  previously wrote metadata only — `create_text_for_math_process()` was
  defined but never called, and the embedding step it referenced
  (`backfill_embeddings.py`) doesn't exist in the repo. Added the missing
  embedding step (`get_embedding_service()` + `resolve_embedding_model_name`,
  same pattern as `sync_glmp_processes.py`), and made it fail-loud on
  purpose: an unavailable service aborts the run, a failed/empty embed or
  unresolvable label aborts that doc's write. An `atap_graphs` doc is never
  written without a vector — silent unembedded docs were the defect being
  fixed, so the writer must not be able to recreate them. Migration script
  itself committed separately (`2f76224a9`).
- **Data migration**: 237/237 docs copied `math_processes` → `atap_graphs`,
  same IDs, full `.set()` (idempotent, safe to re-run). Verified byte-for-byte
  on a spot-checked doc (all 1536 vector values equal, not just length), text
  fields intact. The `math-set-theory-001` "orphan" named in the original
  migration spec was checked directly and never existed in the live
  collection (confirmed via `.get()` and a full GCS-manifest-vs-Firestore ID
  diff, zero mismatches either direction) — migration count was 237 → 237,
  not 237 → 236.
- **Relabel check**: all 237 already measured 1536d / `text-embedding-3-small`
  post-copy — relabel was a confirmed no-op, nothing to fix.
- **Index**: 1536-dim vector index on `atap_graphs.embedding` built and
  `READY`, mirroring `research_papers`'s config exactly.
- **Reader + Writer #2** (`5038b467a`): `mcp_server/config.py`'s
  `COLLECTION_MATH_PROCESSES` constant value moved to `"atap_graphs"` (name
  kept — renaming it would touch `vector_search.py` x4 and
  `index_existing_content.py` for no functional gain); `endpoints/content
  /routes.py`'s separately-hardcoded `PROCESS_FAMILY_COLLECTIONS` dict
  updated too. `sync_all_process_families.py`'s `FAMILIES` list — a second,
  independent metadata-only writer — no longer contains `math_processes` (or
  `atap_graphs`); `atap_graphs` is synced exclusively through the dedicated
  fail-loud `sync_math_processes()` function, not the generic
  `process_sync_common` path used by chemistry/physics/computer_science/
  biology. One writer discipline for `atap_graphs`, not two.
- **Deployed**: Cloud Build `8269b3f6` → revision
  `copernicus-podcast-api-00245-zh8`, 100% traffic, `/health` 200.
- **Live proof, both directions**: a throwaway marker doc written to
  `atap_graphs` only (confirmed absent from `math_processes`) came back
  through the live `/api/vector-search/semantic` endpoint before the delete —
  proof the reader had actually moved, not just that both collections still
  held identical data. Anchor query ("field extension degree theorem")
  surfaced `abstract_algebra-field-theory-extensions` at #1. After deleting
  `math_processes`, a follow-up live query still returned correct
  `atap_graphs` results, confirming the delete didn't break the live path.
- **`math_processes` deleted**: all 237 docs removed, collection confirmed
  empty (0 docs, `math-set-theory-001` confirmed still absent).
- **Standards recorded**: chart/graph embedding text-builders must include
  Mermaid source — `atap_graphs` already does (confirmed on both of its
  text-builders). `glmp_processes` re-embed + rename to `_graphs`-family
  naming is **deferred**, blocked on the RegulonDB redraw decision (Nathan
  Lents, ~2-4 weeks) — do not touch `glmp_processes` until that resolves; its
  current text-builder already includes Mermaid too, so the deferred re-embed
  doesn't need to add that, just keep it. Naming taxonomy going forward:
  mathematical-object collections → `_graphs`, empirical
  literature-derived-process collections stay `_processes`. Applied to
  `atap_graphs` now; not retroactively applied to any other collection unless
  independently touched.
- **Not in this thread**: frontend chart-link/Mermaid-preview rendering for
  process-family search results (`SearchInterface.tsx` already renders
  `atap_graphs` hits as plain text cards — a chart-specific "View Chart" link
  or inline Mermaid render is a small, separate follow-on, scoped but not
  built); any other process-collection rename.

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
4. ~~**Remaining `embedding_model` hardcodes**~~ — done. Five files
   (`sync_{glmp,physics,chemistry,cs}_processes.py`, `sync_videos.py`) fixed
   `81bd1bc3c`; the sixth (`index_existing_content.py`, 3 sites) fixed
   `deff18da4`. All six now resolve the label via `resolve_embedding_model_name`
   (fail-loud, no substituted default). Verified: no remaining instance of the
   actual bug (a script hardcoding `"text-embedding-004"` as an
   `embedding_model` fallback regardless of which provider ran). The two
   `"text-embedding-004"` strings still in the codebase are unrelated to this
   bug — `services/embedding_service.py`'s own Vertex-provider default (the
   correct model name for that provider) and a comment in `auto_embedding.py`
   describing the fix.
5. ~~**8-podcast relabel** — `podcast_jobs` docs labeled 004 with measured dim
   **1536** (by dim, never by label alone).~~ — done, verified directly via
   Firestore query: 0 docs currently labeled `text-embedding-004` with an
   actual 1536d vector. (46 docs still say `text-embedding-004`, but all 46
   measure genuinely 768d — the separate, already-known legacy Vertex
   vectors, not the mislabeled ones this item was about.)
6. ~~**Math focus file**~~ — done. Draft v2 became `atap/docs/research_focus.json`
   (`a62ac33`), verified live: raw URL 200
   (`raw.githubusercontent.com/garywelz/atap/main/docs/research_focus.json`),
   commit confirmed on `origin/main`, content holds `active_questions` and
   `frontier` including the n=3 algorithm-capsule question. Wired into the
   ATAP Claude project's fetch-live instructions.
7. ~~**TSV provenance audit**~~ — diagnostic 2026-07-26: pattern C (~54%
   correct-PMID). Seeded `research_focus.flagged` with 5 verified in-corpus
   IDs. Full re-harvest queued (see FINDING above).
8. ~~**Disable old OpenAI key (`…MYQA`)**~~ — done, verified via
   `gcloud secrets versions list openai-api-key`: v6 `enabled`, v1-5
   `disabled`.
9. ~~**Delete defunct `copernicus` Cloud Run service**~~ — done 2026-07-23,
   verified: `gcloud run services describe copernicus` now errors "Cannot
   find service."
10. **Narrow `copernicus-service` IAM** — project-level `editor` + `run.admin` +
    `storage.admin` + `cloudsql.admin` (plus secretAccessor).
11. ~~**Document Express auth on `copernicus-api`**~~ — done. Documented as
    the `fe9b337` finding (auth enforcement not locatable in-repo or Secret
    Manager) and flagged at governance level as a known limitation of the
    record-of-truth principle (`CONSTITUTION.md` §4, commit `676aa5918`).
    The underlying open questions (what performs the check, how a token is
    obtained, whether `/api/vector-search` is reachable) are **not closed** —
    they stay deferred, "do not start," in the `fe9b337` finding. This item
    was "document it"; that's done. Resolving it is a separate, unscheduled
    thread.
12. *(Split into items 26-28 below — CRP PWM, sciencevideodb quality,
    GitHub housekeeping — per 2026-07-30 request to divide this bundled
    item into its three slash-separated parts.)*
13. ~~**DISCIPLINE_DATABASES_PLAN.md rewrite**~~ — done, commit `c7a614529`:
    reframed as engine (ATAP) vs. Methods & Tools demonstration corpus
    (biology/chemistry/CS/physics), against the engine-vs-discipline
    distinction, not find-and-replace.
14. ~~**metadata_database footer prose relabel**~~ — done (2026-07-30),
    commit `b3dbd91` in the `metadata_database` HF Space repo: "serving GLMP,
    the Mathematics Database, and CopernicusAI" → "serving GLMP, ATAP, and
    CopernicusAI." Verified live at
    `garywelz-metadata-database.static.hf.space/index.html` post-deploy.
15. ~~**Prune stale settings.local.json allowlist entries**~~ — done
    (2026-07-30). Removed the four `mathematics-database`-path entries from
    `copernicus-web/.claude/settings.local.json`, confirmed both old local
    checkout paths no longer exist first. File is gitignored (local-only by
    design, no commit/push applicable). The one entry covering
    `hf-spaces/mathematics-database/**` specifically was already redundant
    with the broader `Read(//c/Users/garyw/hf-spaces/**)` entry that
    remains — no functional loss.
16. ~~**Git-history depth check on ATAP corpus**~~ — done (2026-07-30).
    Zero substantive history: exactly **one commit** (`093587d38`,
    2026-06-12) ever touches
    `copernicus-web/huggingface-space/mathematics-processes-database/`, and
    that commit is literally the repo's root commit — a wholesale initial
    import of 75,192 files (11.5M insertions) covering the entire repo at
    once (venv, config, everything), not a dedicated add-this-corpus commit.
    Scoped to just this directory: 664 files, 74,557 insertions, all in that
    same single commit — no prior or subsequent history at all. The whole
    repo has only 57 commits total; only this one ever touched the
    directory. DECISION: **fresh-commit, not subtree-split** — a
    subtree-split exists to preserve incremental history, and there is none
    to preserve here; splitting would just carry over one opaque bulk
    snapshot with extra ceremony. Same opacity-of-provenance concern as the
    `flowchart-source-papers.tsv` finding, different dimension (chronological
    history vs. citation accuracy) — recorded for the same reason.
17. ~~**Pin `copernicus-podcast-api` Dockerfile base image to a digest**~~ —
    done, commit `12ea2bc09` in `copernicus-web`: pinned to
    `sha256:db3ff2e1800a8581e2c48a27c3995339d47bdf046da21c7627accd3d51053a93`
    (verified via that deploy's Cloud Build log to be the exact digest
    already pulled, a true no-op pin). The 07-24 deploy had pulled a fresh
    base layer ("Downloaded newer image for python:3.11-slim") alongside an
    unrelated code change; pinning stops that recurring unnoticed.
18. ~~**VERIFY PENDING — embed-at-promote**~~ — VERIFIED (2026-07-30). Gary
    generated a real podcast by hand ("CRISPR's Unfolding Revolution:
    Precision Engineering Life's Code," Biology). Job `157a577d-4432-40ac-`
    `8507-8fdf55a7f73c` promoted to `episodes/ever-bio-250044` at
    `2026-07-30T15:58:17`. All three conditions met: `embedding_model` set
    (`text-embedding-3-small`, not stranded/blank), vector is 1536d, and it
    surfaces correctly in a live `/api/vector-search/semantic` query
    ("recent CRISPR gene editing applications") — ranked **#2**, topically
    relevant among the results. The `ed618599f` fix (deployed
    `copernicus-podcast-api-00244-lj6`, 2026-07-24) is confirmed working on
    a real promote, not just deployed.
19. ~~**Untrack ~14k venv paths in copernicus-web**~~ — done 2026-07-26,
    commit `c1234dc99`: `git rm -r --cached` on `venv`, `rss_venv`,
    `cloud-run-backend/backend_venv`, `cloud-run-backend/test_env` (14,871
    files, index-only, zero disk deletions; all four already covered by
    `.gitignore`). Deferred from the 2026-07-23 credential-shaped-file sweep
    (Cursor).
20. *(Split into items 29-30 below — GLMP Daily Brief, Collaborator Window —
    per 2026-07-30 request to divide this bundled item into its
    slash-separated parts. They remain one coupled design — see 29's note.)*
21. ~~**Build a findability check**~~ — DONE (2026-07-29). Probe built
    (`findability_probe.py`, `403e0b4c`), Gate-3 acceptance test passed
    against production (14 anchors, `podcast_jobs` + `math_processes`
    WARNINGs, no false alarms), integrated fail-soft into the nightly chain
    (hook `8eff8947d`, reader `073be02`), Jetson-activated (both repos
    pulled, cron copy synced). PENDING: first automated cron cycle to
    confirm the Findability section renders in the morning report
    (WARNING / 14-14 / 2) — witnessed on the next scheduled run. Probe
    surfaced two real findings on first run: physics ID corruption (item 22)
    and a chemistry near-duplicate (item 24 below).
22. ~~**FINDING — `physics_processes` ID/title mismatch.**~~ FIXED
    (2026-07-30), commit `b67dfb692`: full scan found **12 of 28 docs**
    mismatched (not the 4 originally sampled), a per-subcategory rotation —
    astrophysics, electromagnetism, quantum_mechanics, solid_state, 3 of 3
    wrong in each. All 12 content-verified (title correct, ID corrupt, no
    exceptions) before any write. Firestore-only fix, as decided: each doc
    copied to a new ID derived from its verified title (embedding carried
    across unmodified, doc's own `id`/`process_id` fields updated to match),
    old-ID doc deleted. Verified post-fix: 28/28 docs intact, all 12 old IDs
    gone, vector index unaffected (1536, READY), live `find_nearest` still
    returns the doc correctly under its new ID.
    **NOT fixed — flagged separately**: `metadata.file_path`/`gcs_url` on
    all 12 still point at the old-wrong-slug GCS filenames (the corruption
    exists at the GCS source too, not just in Firestore); the GCS rename is
    a separate, still-open thread. Also: `findability_probe.py`'s physics
    anchor updated to the new ID in the same commit — the Jetson checkout
    needs to pull this commit before its next automated run, same manual
    pull step as before. Full check across the other process collections
    (they sampled clean earlier) still not done.

23. ~~**FINDING — `build_master_todo.py` cron path is a manual copy**~~ FIXED
    (2026-07-30). Chose option (a): point the executed path at the git
    checkout. Live caller is `run_post_ingest_hooks.sh` (post-ingest chain;
    standalone 10:45 cron was already removed). Default
    `MASTER_TODO_SCRIPT` is now `/media/sdcard/glmp/scripts/build_master_todo.py`
    — not `/media/sdcard/glmp-cron/` (one-file manual copy; only that script
    was in the dir). Also updated `jetson_master_todo_cron.sh` + rollback
    lines in `SCOUT_ARCHITECTURE.md` so a restored 10:45 cron cannot reintroduce
    the stale path. `glmp-cron/` can be retired later; no longer on the hot path.

24. ~~**FINDING — possible near-duplicate in `chemistry_processes`**~~ FIXED
    (2026-07-30), commit `bdc0bde1b`. Content-read of the original pair found
    them **not duplicates** — a content-free 2025-12-29 placeholder stub
    ("Chemistry process: {title}", generic auto-generated mermaid) vs. a
    substantive 2026-01-08 doc on the same broad topic. Checking for a
    broader batch found this was **one of 49** identical placeholder stubs
    (28% of the collection), all dated 2025-12-29, spread across essentially
    every subcategory. All had been superseded by later real content — same
    subcategory name in 6 cases, a renamed subcategory in 5
    (`surface_chemistry_catalysis`→`surface_chemistry`,
    `kinetic_processes`→`kinetics`, `thermodynamic_processes`→`thermodynamics`,
    `spectroscopy_analysis`→`spectroscopy_advanced`,
    `electrochemical_processes`→`electrochemistry`) — but never removed, so
    they competed in retrieval against the content that replaced them.
    Confirmed out of scope for Knowledge Engine concerns first
    (`chemistry_processes` is a Methods & Tools demonstration collection, not
    part of a running project like GLMP/ATAP); all 49 then deleted as a
    batch. Verified: 124/124 remaining (173 − 49), zero placeholder-pattern
    docs left, index unaffected, full probe re-run confirms both chemistry
    anchors still rank 1.

25. **TSV re-harvest** — promoted from the curated FINDING above (2026-07-26
    diagnostic: `flowchart-source-papers.tsv`, 481 rows, ~54% correct-PMID
    rate, pattern C — bad rows independently mis-IDed, no mechanical offset
    to correct for). Full re-harvest from `raw_citation` free-text against a
    resolver, ~220 rows to correct. Own runway, not a quick fix.
    `research_focus.flagged` already seeded with 5 verified in-corpus IDs as
    a retrieval seed only — this item is the full correction, not that seed.
26. **BACK BURNER — CRP PWM** (split from former item 12). Build a
    position-weight-matrix for CRP binding sites from RegulonDB data — the
    highest-leverage remaining science move on the decoder, would let the
    lac operon reach an evidence-backed Class II call from sequence rather
    than curated biology alone. Real molecular-biology work: per the
    Reminder to Self below, needs a qualified biologist's judgment, not
    something to execute unilaterally. **On hold pending Prof. Lents'
    feedback** (2026-07-30) — do not proceed until he's weighed in.
27. ~~**sciencevideodb quality**~~ — DONE (2026-07-30, split from former item
    12). Scoped as 4 quick fixes; the discipline-naming check led straight
    into a much larger finding: **43% of the 753-video catalog (322 videos)
    had wrong YouTube channel attribution** — a batch ingestion bug had
    mapped several claimed channels to entirely the wrong real channel.
    Verified every one of the 753 videos individually against YouTube's
    oEmbed endpoint (not a sample — a full census) before touching
    anything:
    - **5 channels 100% misattributed**: "Khan Academy" (116) was actually
      66 SSSniperWolf (pop-culture/reaction junk, zero science) + 50 Google
      for Developers (real dev/cloud content); "Caltech" (54) was actually
      Chandoo (Excel/Power BI tutorials, junk); "SciShow" (50, incl. 1
      unreachable/401) was actually OpenAI product/business content;
      "UC Berkeley" (53) was actually ElectroBOOM (real electrical-
      engineering demo channel). "FuseSchool" (50) was actually Domain of
      Science (real science channel, per-video categories already matched
      actual content, so left as-is beyond the channel-name fix).
    - **Numberphile** (54, channel attribution correct): 53/54 miscategorized
      (mostly `chemistry` instead of `mathematics`) — fixed.
    - **Remediation** (`videos-metadata.json` on GCS): deleted 171 videos
      (120 junk + 50 OpenAI business content + 1 dead link), re-attributed
      and recategorized 202 legitimate videos to their real channel, fixed
      Numberphile's 53 miscategorized entries, fixed the `cs`/
      `computer_science` naming split (418 records). Catalog now: **582
      videos, 11 channels** (down from 753/13). Verified post-fix: counts
      reconcile, zero bad-channel labels remain, no duplicate IDs, JSON
      valid, live GCS copy matches.
    - **Page/README honest rewrite** (`copernicus-web` HF Space repo
      `hf-spaces/sciencevideodb`, commit `dca17c3`): replaced aspirational
      claims (transcript-based search, vector-DB semantic search,
      "Integration Framework... designed for CopernicusAI Knowledge Engine
      integration") with what's actually true — keyword search over
      title/description/channel only, no transcript text stored, no vector
      search; corrected milestone numbers to 582/11; added a clear "Live
      Today" vs. "Built But Disconnected" (a separate, dormant
      `github.com/garywelz/sciencevideodb` monorepo, last active December
      2025, with a real tested YouTube API client but no working database/
      search/frontend) vs. "Planned, Never Built" (Postgres, vector DB,
      Meilisearch/OpenSearch, Vercel) breakdown. One claim was checked and
      confirmed **true**, left alone: the Research Tools Dashboard at
      `copernicus-frontend-.../knowledge-engine` is real and live.
    - **Transcript-coverage check**: inconclusive — YouTube's unauthenticated
      caption-list endpoint no longer returns useful data without proper
      API access; documented in the page itself that the ~72% caption flag
      is a stored ingestion-time value, not independently re-verified.
    - **Dead-link check**: fully covered as a side effect of the full
      oEmbed census (not just a sample) — exactly 2 broken links found
      (1 confirmed 404, 1 confirmed 401 traced by title to the same OpenAI
      junk batch), both already removed above.
    - **`app.py` cleanup** (commit `6d452b4`): deleted, along with
      `requirements.txt` (existed solely for its Gradio dependency) — the
      file was never served (Space `sdk` is `static`) and its own text
      described the same fictional architecture just corrected elsewhere.
    Space confirmed `RUNNING` at `6d452b4` post-deploy (HF Spaces API).
28. **GitHub housekeeping** (split from former item 12). Unspecified —
    needs scoping (stale branches? README updates? issue triage?) before
    it's actionable.
29. **PROPOSE — GLMP Daily Brief / Collaborator Window** (recombined
    2026-07-30 — briefly split into former items 29-30, merged back since
    they're one artifact, not two independent builds; design task, not
    built yet). A fetchable, auto-updating status page serving two
    audiences from one artifact: the GLMP project's opening context, and
    the welcome-package landing surface for Krampis/Lents/Me-Me and future
    collaborators — current project state, what's available (papers,
    process flowcharts, papers-in-progress, sciencevideodb, podcasts),
    current research state + what changed recently (the frontier, in plain
    terms — reads `research_focus.json`), how to contribute. Host/mechanism:
    GitHub Pages (`garywelz.github.io/glmp`), not GCS — renders from the
    repo, can't drift, updates on push, fetchable at a stable URL. Counts
    come from live status sources that already exist
    (`knowledge-engine-status.json`, `/api/content/stats`), never
    hand-maintained — a stale brief is worse than none. Generation can ride
    the existing post-ingest chain (`build_master_todo.py` already runs as a
    hook; this is a small addition, not new machinery). Not the MASTER_TODO
    — engineering items (venv untracking, IAM, hardcodes) are noise to this
    audience; different document. Queue entry only — design is next
    session.
30. ~~**FINDING — `physics_processes` GCS filenames still wrong**~~ — DONE
    `2d11b6f1a` (`copernicus-web`). Scope grew mid-fix: beyond the 12
    GCS file pairs (24 files renamed) and 12 `metadata.file_path`/`gcs_url`
    Firestore updates originally scoped, three catalog files
    (`process-index.json`, `collections.json`,
    `whole-of-physics-graph-data.json`) also referenced the old slugs and
    needed the same substitution — one of them (`whole-of-physics-graph-data.json`,
    84KB, 3 graph layout variants) had 157 references across node ids,
    `processId`, `url`, and link source/target fields. Fixed via whole-file
    string substitution (old slug → new slug), safe because no old slug is
    a substring of another or of any new slug (checked programmatically
    before any write). Dry-run confirmed exact counts before the real run.
    Post-fix verification: all 24 old GCS files gone, all 24 new files
    present with intact content, all 12 Firestore metadata fields correct,
    zero remaining old-slug references in any of the 3 catalog files, all
    still valid JSON. Final live regression check —
    `findability_probe.py` re-run — confirms no regression: physics anchor
    ("why does a changing magnetic field create an electric current") ranks
    1, `physics_processes` fully embedded (28/28) with a READY index.

31. ~~**FINDING — exposed YouTube API key, rotation never completed**~~ —
    RESOLVED (2026-07-30). Enabled `apikeys.googleapis.com` (was disabled)
    and matched the old key's literal value against every API key in the
    project by content, not by label — found it under display name
    **"API key 1"** (UID `b40e3f27...`, created 2025-04-06), **not** under
    any YouTube-labeled key. Its restriction had been silently changed away
    from YouTube at some point (`updateTime: 2026-06-19`) to **only
    `generativelanguage.googleapis.com` (Gemini)** — so the original
    "still live for YouTube" concern was already stale; the risk had moved
    to a different API without the rotation doc ever being updated to
    reflect it. Confirmed it matched none of the three live Gemini secrets
    (`GEMINI_API_KEY`, `gemini-api-key`, `google-ai-api-key`) that
    deployed services actually pull from — nothing currently depends on it
    via the standard Secret Manager pattern. Deleted outright
    (`gcloud services api-keys delete`), confirmed gone from the active
    list (4 keys remain, down from 5). The `youtube-api-key` Secret
    Manager secret itself (holding the legitimate replacement key) was
    untouched.

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
