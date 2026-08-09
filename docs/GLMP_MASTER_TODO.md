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
Seeded `research_focus.flagged` with 5 verified in-corpus IDs (Jacob/Monod,
cAMP-Crp, attenuation, two QS/activation circuits) — retrieval seed only,
not a bibliography. **Superseded (2026-08-05): the queued re-harvest thread
turned out to be unrunnable as scoped — see item 25 below for the full
trace (original PMIDs were AI-assigned at flowchart-authoring time in
October 2025, `raw_citation` is generated from them so re-resolving it is
circular, and the 54%/"~220 rows" figures themselves have no reproducible
methodology committed anywhere in this repo).**

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
    pulled, cron copy synced). **Automated render witnessed** (2026-07-30):
    overnight cycle `01:21Z` wrote `### Findability` into published
    `GLMP_MASTER_TODO.md` / `GLMP_STATUS.html` (Overall WARNING, physics
    anchor PASS, 2 coverage/index warnings; hook OK). Same-day AM cycle
    `15:36Z` also rendered the section (Overall ALERT, 13/14 — physics
    anchor NOT FOUND after item-22 ID migration; fail-soft, master_todo
    still OK). Pending-first-cycle caveat dropped. Probe surfaced two
    real findings on first run: physics ID corruption (item 22) and a
    chemistry near-duplicate (item 24 below).
    **Ground-truth diagnosis of the 15:36Z ALERT, requested by Gary/Claude
    Chat (2026-07-30) — do not file as assumed-benign migration noise.**
    Ran all three requested checks directly, not inferred:
    1. **Old anchor ID** (`electromagnetism-wave-function`) — confirmed
       `exists: False` in `physics_processes` (direct Firestore `.get()`).
       It was renamed away by item 22's fix, not just relabeled.
    2. **New ID's embedding** (`electromagnetism-electromagnetic-induction`)
       — confirmed present and intact: 1536-dim vector, title "Electromagnetic
       Induction (Faraday's Law)" (exactly the anchor query's intended
       target). The copy-then-delete re-ID did **not** strand the vector.
    3. **Live retrieval right now** — ran the exact anchor query ("why does
       a changing magnetic field create an electric current") against the
       production `/api/vector-search/semantic` endpoint. Result:
       `electromagnetism-electromagnetic-induction` at **rank 1** — the
       best possible outcome, not just "findable."
    **Verdict: Case 1 (benign), not a regression.** Physics retrieval is
    fully healthy; the doc was always findable, just under its corrected
    ID. Root cause of the 11:36 ET ALERT: the anchor-fix commit
    (`b67dfb692`, 11:05 ET — same commit that did the ID fix) landed only
    31 minutes before that cron cycle ran, and Jetson pulls are manual, not
    automatic mid-cycle — so Jetson was almost certainly still running the
    pre-fix probe script with the stale anchor at 11:36 ET. Confirmed
    `b67dfb692` is a direct git ancestor of `8640e7983` (the item-23 fix,
    12:49 ET, which Jetson has already pulled per Cursor's report) — so
    Jetson's checkout now has the correct anchor too, no separate pull
    needed. No code change required; the anchor was already correct in the
    repo before this diagnosis was even requested. Next automated cycle
    (tonight's PM run) should show a clean 14/14 — that's the remaining
    witness, not a fix.
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
    **Jetson file-level + pull confirmed** (`8640e7983` on HFS/worker).
    **Automated cycle on the new path: not yet witnessed** — commit landed
    12:49 ET; today's AM chain was 11:36 ET (still pre-fix). Next PM/AM
    cycle is the witness.

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

25. ~~**TSV re-harvest**~~ — **CANNOT BE RESOLVED AS SCOPED (2026-08-05,
    Claude Chat catch, traced and confirmed).** The item as written asks to
    "re-harvest from `raw_citation` free-text against a resolver" — but
    `raw_citation` is generated *from* each row's own `pmid`/`doi`/`title`
    columns (confirmed: it's a formatted citation string built from those
    fields, live-checked against the actual TSV), not an independent
    original. Re-resolving it returns the same wrong paper every time — the
    method is circular, not a quick-fix engineering task as originally
    scoped.
    **Traced fully, both open provenance questions Claude Chat raised:**
    1. **Where did the original PMIDs come from?** Git-blamed the flagellar
       row (PMID 38926585, an unrelated TnpB transposon paper Claude Chat
       flagged) back to its earliest commit, `1ee3076` (2025-10-15,
       `gcs-processes/ecoli/ecoli_e._coli_flagellar_assembly.json`). The
       process JSON's own fields answer it directly:
       `verifiedBy: "AI-assisted generation with PubMed literature review"`,
       `notes: "Auto-generated using PubMed and Gemini APIs. Based on 5
       peer-reviewed sources."` The wrong PMID was assigned by a model
       during original flowchart authoring in October 2025, not inherited
       from any upstream human-curated artifact. Made worse by the
       manifest-builder script itself
       (`scripts/build_flowchart_source_papers_manifest.py`,
       `pick_canonical_source()`): it takes `sources[0]` with a DOI,
       position-based, no relevance check — and this process's own
       `sources` array has the *correct* flagellar-assembly paper sitting
       right there at position 1, never picked because position 0 already
       had a DOI too. The `bb9b8a4` commit Claude Chat asked about
       (2026-07-15, "ingest provenance") is unrelated to this — it's 9
       months downstream, adding harvest sidecar files
       (`interpretive_layer.tsv`, Mermaid diagrams), not the original PMID
       assignment.
    2. **Where does "~220 of 481" come from?** Traced the file's own
       history: 481 is real — the live `flowchart-source-papers.tsv` has
       482 lines (1 header + 481 data rows), confirmed by direct count.
       Commit `09f4dc9` (2026-07-11) explains why: it replaced a June
       217/199-canonical-row manifest (archived as
       `flowchart-source-papers.pre-harvest-2026-06.tsv`, the "pre-harvest"
       file with `canonical_doi`/`canonical_pmid`/`canonical_title` columns
       and no `raw_citation` anywhere) with "the cleaned 481-row harvest" —
       a one-row-per-source-paper schema, not one-row-per-process. But **the
       harvest tool that produced those 481 rows, and whatever check
       produced "~54% correct," were never committed** — no script, no
       per-row verification output, nothing beyond the master todo's own
       summary sentence (commit `ce1cd5d`, 2026-07-26). "~220" is not a
       second, independently-verified data point — it's `481 × (1 − 0.54)
       ≈ 220`, arithmetic restating the 54% figure, not a separate count of
       specific wrong rows. **The 54% figure itself cannot be reproduced or
       audited from anything in this repository.**
    **Conclusion, matching Claude Chat's:** #25 as scoped is not
    re-runnable. What it actually needs is **re-sourcing** — finding papers
    that genuinely support each chart, from scratch — not re-resolving
    already-circular text. That's a different, larger task needing biology
    judgment, the same bottleneck already holding #26 and #33. Recommend
    folding it into that queue rather than treating it as an engineering
    task. **First actual task, not yet started:** identify which of the 481
    rows are wrong at all — unknown until then, "which rows are wrong" *is*
    the blocking first step, not a preamble to one.
    `research_focus.flagged` remains seeded with 5 separately-verified
    in-corpus IDs (retrieval seed only, not a bibliography) — unaffected by
    this finding, since those were checked individually rather than trusted
    from the TSV.
    **Splits into three tiers with very different costs (Claude Chat,
    2026-08-05), independently verified against the actual process
    files, not taken on trust:** reading all 217 current `glmp-v2/processes`
    JSON files' own `sources` array lengths (excluding
    `_previous_versions/`, which held 3 stale duplicates) gives exactly
    **121 with 2+ sources, 87 with exactly 1, 9 with 0** — matching Claude
    Chat's figures exactly. The insight that splits them: `pick_canonical_source()`
    (the manifest builder) takes `sources[0]` with a DOI and never checks
    relevance — so the 121-chart tier isn't a sourcing problem, it's a
    **selection** problem, and the right paper may already be sitting
    unused in the same row (as it literally is for the flagellar case).
    Only the 87 single-source charts are genuine re-sourcing, the same
    biologist bottleneck as #26/#33; the 9 zero-source charts are already
    flagged `needs_krampis_review`.
    **Tier-one sized with real data, not an inherited estimate (2026-08-05).**
    Built the measurement Claude Chat suggested — embedding similarity
    between each process's own subject text (`name`+`description`) and
    each of its sources' titles, using the engine's actual production
    model (`text-embedding-3-small`, fetched live via the same
    `openai-api-key` secret the ingest pipeline uses) — not a second
    generative pass, a discriminative similarity measurement instead, per
    Claude Chat's own caution that validating a reselection can't be
    another model pass. **Validated against the one already-known case
    before trusting it on the rest**: for the flagellar row, the method
    correctly ranks `sources[1]` (the real flagellar paper, sim=0.766) far
    above `sources[0]` (the picked TnpB paper, sim=0.292) — gap 0.474, the
    largest in the whole set.
    **Result across all 121 multi-source charts:** the picked source is
    *not* the top-ranked one, by a meaningful margin, in **54** of them —
    the real, measured size of the reselection-candidate tier, not the
    inherited "~220" figure (which was arithmetic on an unreproducible
    54%, per the correction above, and was never tier-specific anyway).
    Confidence isn't uniform across those 54 — gap-size breakdown: **10
    with gap >0.20** (near-certain mismatches, flagellar's 0.474 among
    them), **17 with gap >0.15**, **20 in 0.10–0.20**, and **17 below
    0.10** (short/generic titles like "Glycolysis" produce weaker signal,
    lower confidence). Notably, **`ecoli_lac_operon` is in the flagged set**
    (gap 0.253) — the same circuit at the center of the active cAMP-CRP
    work with Lents; worth surfacing to him directly rather than waiting
    for a full pass. Full 54-row list (both titles, both similarity scores,
    sorted by gap size) filed at
    `docs/open-questions/source-reselection-candidates-2026-08-05.tsv`,
    same convention as `loop-audit-candidates-2026-08-04.md` — a
    pre-registered record, not a private working file.
    **Not done, per Claude Chat's explicit design:** no row has been
    reselected or changed. The originally-planned next step (mechanical
    reselection of the 17 near-certain+solid rows, then a biologist
    spot-check to accept/reject the method wholesale) **did not survive
    the spot-check** — see the correction immediately below, done before
    any file was touched.
    **Corrected before any write, once the spot-check was actually run
    (2026-08-05):** manually checked all 10 near-certain (gap ≥0.20) rows
    against their full source metadata — including each source's own
    `note` field, not just its title, which the embedding check never saw.
    Result: only **4 of 10 look like real errors**
    (`ecoli_e._coli_flagellar_assembly`, `ecoli_protein_folding_chaperones`,
    `yeast_yeast_vacuolar_protein_sorting`, `synthetic_recombinase_counter`
    — picked source is genuinely tangential, alternative squarely on-topic).
    **4 of 10 look like likely false positives**: `ecoli_lac_operon`
    (picked = Jacob & Monod 1961, the Nobel-winning original operon paper,
    explicitly noted as such — the "better-ranked" alternative is a 1996
    review whose title just contains "lactose operon" verbatim),
    `yeast_mating_type_switching` (picked = Nasmyth 1983, noted as the
    discovery of the actual mother-daughter HO-expression asymmetry
    mechanism — the alternative is "a comprehensive modern review"),
    `bacillus_competence_development` (picked = the ComK bistable-switch
    paper, arguably *more* mechanistically specific than the alternative's
    "comprehensive review"), and `ecoli_anaerobic_respiration` (FNR vs
    ArcA — E. coli's two co-equal master anaerobic regulators, not a
    right-vs-wrong pair at all). **2 of 10 genuinely ambiguous**
    (`yeast_oxidative_stress_response`, `yeast_heat_shock_response`).
    **Pattern in the false positives:** the picked source is a foundational
    or mechanistically-specific paper, and the embedding prefers the
    alternative because its title lexically contains the process's own
    query terms — a different signal than "is this the right citation,"
    correlated with it only sometimes. This shows up **within the highest-
    confidence gap tier**, not just among the weak/short-title rows
    excluded earlier — a ~40% false-positive rate on the tier that was
    about to be auto-reselected.
    **Conclusion: no mechanical reselection, for any tier, without
    per-row review.** The embedding measurement is a good *triage* signal
    — it found every genuine error checked so far, including flagellar —
    but gap size alone doesn't separate real errors from lexical
    coincidences, even at gap ≥0.20. The 54-row list stays valuable as a
    **prioritized human-review queue**, not an auto-apply list; treating
    "near-certain" as safe-to-auto-fix was the mistake, caught before any
    of the 217 process JSONs were touched. Also confirmed, checked rather
    than assumed, why this matters beyond the TSV: the flagellar process is
    live in Firestore `glmp_processes` with a real embedding
    (`text-embedding-3-small`, computed 2026-06-07) built partly from its
    `sources` array text — so a wrong reselection wouldn't just be a
    documentation error, it would reach live semantic search. A correct
    reselection would need the same downstream propagation (re-sync via
    `sync_glmp_processes.py`, re-embed) to actually land — and separately,
    `flowchart-source-papers.tsv`'s current 481-row harvested schema was
    produced by a tool not present in this repo (see the finding above), so
    that specific derived artifact **cannot be correctly regenerated** with
    anything currently committed here, independent of the reselection
    question.
    **Standalone email drafted, then superseded by Gary's better channel
    (2026-08-05).** Drafted per Claude Chat's request — the lac_operon case,
    specifically *because* it's a good concrete illustration of the
    false-positive risk, not despite it — asking whether Jacob & Monod or
    the alternative is the better citation, stating plainly this is a
    machine-measured signal that may be a lexical coincidence. Draft kept
    for the record, not sent:
    `docs/open-questions/lac-operon-source-finding-for-lents-2026-08-05.md`.
    **Gary caught a better path**: Lents already has the canonical
    `ecoli_lac_operon` record open via
    `collaborations/krampis-virtual-cell/shared-diagrams-for-lents.md`
    (Layer 2's viewer links), which already invites feedback through its own
    built-in "Improve this process" form — a standalone email would be a
    redundant channel on top of one already working, not a needed one.
    **Folded into that document instead** (`glmp@28e5c44`): one line noting
    an automated citation cross-check is running corpus-wide, that lac's own
    citation held up fine on it, and that the same form/PMID-note path
    covers anything he notices on any chart. States the true, low-key
    result (no error found here) rather than raising a concern that the
    analysis itself didn't support.
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
28. ~~**GitHub housekeeping**~~ (split from former item 12) — DONE, closed
    2026-08-04. Scope decided (Gary, via Claude Chat): **`copernicus-web`-only**
    — the other five suite repos go on a separate future list, not folded into this
    item.
    - ~~`copernicus-web` README~~ — DONE (`0277e89b2`). Rewrote it as the monorepo
      it actually is; the old one had described it as a standalone Spotify podcast
      site since a June 2025 initial commit, unchanged by a later, misleadingly-
      titled "Complete update" commit. Verified via a full unshallow (repo was a
      shallow 69-commit clone locally, real history is 268 commits) that nothing
      else was pending against the file before overwriting it.
    - **Issue triage:** DONE, trivially — zero open issues on `copernicus-web`.
    - **GitHub Actions:** DONE, trivially — no `.github/workflows/` configured at
      all; the only run in the repo's history is GitHub's own automatic
      Dependency Graph bot (pip, `/papers`, 2026-06-10), not a custom workflow.
    - **Full-history credential scan (2026-08-04), requested by Claude Chat**
      after noticing `bfg-1.14.0.jar` committed twice in this repo — BFG's only
      purpose is stripping secrets from history, so something was apparently
      scrubbed at some point, but that alone doesn't confirm completeness.
      Unshallowed and checked 9 secret-shape pattern classes (OpenAI, Google API
      key, GitHub PAT, AWS key, Slack token, Google OAuth token, PEM private-key
      blocks, GCP service-account `"private_key":` JSON field, Twilio-style SID)
      across full history using commit-listing-only greps (`git log -G`, never
      `-p` on a match — no secret content was ever printed, per the standing
      credential-handling rule). **Result: every hit traced to a false positive**
      — vendored third-party library source (`google-auth`, `python-rsa`,
      `googleapiclient`, inside three different committed venvs, since untracked)
      whose own code legitimately contains strings like `"private_key":` and PEM
      headers as parsing constants, plus a browser-saved webpage snapshot
      (`podcastwothumbnails.html` + `_files/`) whose Google CDN URL parameters
      coincidentally match the Google-API-key shape. No real secret found in
      current reachable history. **Marked limit, not a clean bill of health**
      (`governance/CONSTITUTION.md` §5: "treat a clearly marked limit as a
      finding, not a failure to paper over") — a scan of post-purge history
      can't see whatever a genuine BFG run already removed, by construction.
      This confirms nothing *currently reachable* is exposed; it does not confirm
      the BFG jar's presence is benign. The jar's own commits carry no message
      referencing a purge; more likely an accidental byproduct of a bulk sweep
      than evidence of a deliberate, completed rewrite — but that's a guess, not
      a finding. Standing limit, not resolved.
    - **The 4 open draft PRs — read in full, not judged by name** (per Claude
      Chat's caution that two might be live findings, not cruft):
      - ~~`cursor/mathematics-database-flowchart-errors-d178`~~ — CLOSED
        (2026-08-04), with rationale comment on the PR. Fixed real Mermaid syntax
        bugs (concatenated `style` directives, invalid `{[...]}` decision-node
        syntax, raw HTML in labels) but against root-level scratch/temp files
        (`math.html`, `tmp-binomial.html`, `sanitized_processes*/`), not the real
        corpus path (`huggingface-space/mathematics-processes-database/`, still
        current) — not a mergeable diff as it stood. **Not closed-and-forgotten:**
        the underlying Mermaid-syntax bug class is real and worth checking against
        the actual live corpus files independently of this branch — separate,
        still-open follow-up, not tracked as its own item yet.
      - ~~`cursor/verify-and-correct-computational-pattern-counts-977c`~~ —
        MERGED (2026-08-04), `copernicus-web@1cf51477e`, squash, docs-only, zero
        code changes. Real finding, not cruft: GLMP's chart counts *pattern
        instances*, so a process with both an AND gate and an OR gate is counted
        twice — estimated 25-40% overcount. Distinct from item 33's
        loops/feedbackEdges false-negative issue (different defect: overcounting
        vs. hidden cycles), not overlapping despite both being
        presence-vs-correctness findings. Landed as `detailed_overlap_analysis.md`
        and `glmp_pattern_analysis.md` at the `copernicus-web` repo root — this had
        sat unactioned for 11 months and was worth keeping.
      - ~~`cursor/sync-rss-status-with-firestore-d6f6`~~ — CLOSED (2026-08-04),
        with rationale comment on the PR. Touched live `cloud-run-backend/main.py`
        (116KB, confirmed still the live FastAPI entrypoint, drifted since Jun 29
        independent of this PR's Nov 2025 base). The script it recreates,
        `sync_rss_status.py`, already exists today — but only under
        `archive/one_off_scripts/root/`, meaning someone already independently
        judged this exact tool a spent one-off. Closed as superseded rather than
        force-merged given the drift risk; the underlying discrepancy (Firestore
        `submitted_to_rss` lagging the real RSS feed) is a separate, current
        question left open for a fresh check, not resurrected via this branch.
      - ~~`cursor/fix-podcast-generation-system-issues-a5f1`~~ — CLOSED
        (2026-08-04), with rationale comment on the PR. Confirmed stale: its core
        changes targeted `cloud-run-backend/main_google.py`, which no longer
        exists on main at all — the file it patches is gone, and the podcast
        pipeline has been substantially rebuilt since this branch's Aug 2025 base.
    - Whether GitHub housekeeping extends to the other five repos: resolved by
      moving that scope to **item 41**, which now holds it with ownership per
      finding. Superseded here, not duplicated — item 28 is closed.
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
    **Addendum (2026-07-30, surfaced during the `copernicus-web` cleanout's
    Tier 3 review):** this item's fix was applied directly to Firestore/GCS
    but never reconciled back to the local git-tracked mirror in
    `copernicus-web`, `huggingface-space/physics-processes-database/` — it
    still held all 12 old corrupted slugs. That mirror is the exact source
    `huggingface-space/scripts/upload_all_processes_to_gcs.sh` uploads to
    GCS; running it unreconciled would have silently overwritten the fixed
    production data with the stale corrupted version. Fixed in
    `copernicus-web` commit `1c0c6de30` (committed, **not yet pushed** —
    pending Gary's go, per the repo's gated status): downloaded the actual
    corrected content from GCS for all 12 processes, renamed the 24
    files, removed the 12 stale `.json.backup` files, and applied the same
    slug substitution to `process-index.json`, `collections.json`,
    `whole-of-physics-graph-data.json`, plus **two files the original fix
    missed** — `metadata.json` (12 refs) and `physical-universe-map.html`
    (18 refs). Verified byte-identical (modulo line endings) against the
    live GCS copy.
    **Follow-up fix (2026-07-30), same day:** the internal `"id"` field
    finding above is now resolved. `copernicus-web` commit `36c34eaa8`
    fixed the internal `"id"` field and the `flowchartStandard.basis`
    `"source_extraction:<id>"` reference in all 12 GCS files (and the local
    mirror identically) — each had exactly 2 old-slug occurrences, both
    corrected. Confirmed via `sync_physics_processes.py` that Firestore's
    `process_id`/doc-id are derived from the GCS file path, not this
    internal field, so the fix has no Firestore blast radius. HTML viewer
    files checked and were already clean (0 old-slug references). Dry-run
    confirmed the expected 2→0 count per file before the real run;
    post-fix verification confirms zero remaining old-slug references and
    valid JSON in all 12 files. `findability_probe.py` re-run shows no
    regression. Both `1c0c6de30` and `36c34eaa8` are pushed to
    `origin/main`. Item 30 and its follow-ups are now fully closed.

31. **FINDING — exposed YouTube API key, rotation never completed** —
    PARTIALLY RESOLVED (2026-07-30); **not closed** — see the Jetson gap at
    the end. Key deletion itself is done: enabled `apikeys.googleapis.com` (was disabled)
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
    **Additional pre-deletion thoroughness check, requested by Claude Chat
    (2026-07-30, done retroactively — key was already deleted by the time
    asked, but this is a value-based grep, not repo/git-history-dependent,
    so it's still a valid check against the deleted key string):** grepped
    the literal key value across all 5 locally-cloned repos
    (`copernicus-web`, `glmp`, `sciencevideodb`, `atap`, `hf-spaces`, all
    working-tree files, not just tracked ones). Every match confined to
    the dormant `sciencevideodb` repo's own documentation describing the
    exposure itself (`PENDING_KEY_ROTATION.md`, `FIND_EXPOSED_KEY.md`,
    etc.) — zero hits in any actively-used repo's source or config.
    **One gap remains, cannot close without SSH**: Jetson-side env/config
    files were not checked (no SSH access this session). Given this
    codebase's established pattern is Secret Manager for all live
    credentials (not hardcoded/local `.env` values — the 2026-07-23
    credential-shaped-file sweep found none tracked in git, though that
    doesn't rule out an untracked local file), the risk is judged low but
    not zero. **Ask for Cursor, still standing (2026-08-04, Gary confirmed
    keep open rather than accept the residual risk)**: a quick `grep -r` for
    the literal old key value across Jetson's env/config paths would close
    this definitively. Item stays open until that runs.

32. **FINDING — `programming_framework` index.html has diverged from the
    deployed Space, unclear which is current (2026-07-30, surfaced during
    the repo/Space cleanout's `progframe` pass).** `progframe/`'s local
    copy (`programming_framework/index.html`, bulk-committed `72bf07b`
    2026-06-28) and the actual deployed Space
    (`hf-spaces/programming_framework`, content last touched `0b60f3c`
    2026-04-29, only a credential-hygiene commit since) differ by 1189
    diff lines — not a small edit. Content comparison (not just commit
    date) says the **deployed Space's version is the more developed one**:
    fully-styled Tailwind sections (Prior Work & Research Contributions,
    How It Works, Technical Architecture, Validation & Accuracy) vs.
    `progframe`'s simpler plain-tag/inline-style version ("Project
    Overview," "Technical Foundation: Mermaid Markdown"). Commit-date
    alone is misleading here: `progframe`'s later timestamp is a bulk
    re-import (same pattern as other repos' wholesale-snapshot commits
    this session), not necessarily forward development. **Not touched —
    flagged for Cursor/manual review**, not resolved as part of the
    cleanout (this is a content-currency question, not a stale-file
    question). 34 files total exist in `progframe/programming_framework/`
    that aren't in the deployed Space (mostly `chemistry-processes-database/`,
    which uploads directly to GCS rather than through the Space, so may be
    expected — not all 34 are alarming, `index.html` is the one that
    actually matters since it's what's served).
    **Addendum**: the Space's own `style.css` (real, substantial, 4 real
    commits including "Add comprehensive Programming Framework content" —
    not HF-default boilerplate) is currently unreferenced by `index.html`,
    but its class names (`.tab-btn`, `.batch-status`,
    `.status-card.complete/in-progress/external`) don't match either
    `index.html` version compared above — suggesting a **third**, even
    earlier tabbed-UI redesign this stylesheet belonged to, now itself
    superseded. Same underlying story (multiple historical redesigns,
    unclear which is canonical), not a separate issue — not proposed for
    archival given its entanglement with this open question.

33. **AUDIT — `loops`/`feedbackEdges` blind to a duplicate-node pattern
    corpus-wide — RUN, candidates identified (2026-08-04, Gary's go).**
    Surfaced 2026-08-02 while fact-checking a Zenodo-cited lac operon record.
    `loops`/`feedbackEdges` are computed mechanically from Mermaid-graph cycle
    detection (`scripts/mermaid_graph.py` / `backfill_loops.py`), not curated.
    If one biological entity is given two node IDs (e.g. permease modeled as
    both `G[Lactose Permease LacY]` and `PP[Lactose Permease]`), a real
    feedback cycle renders as a straight-line path and the detector correctly
    reports `loops: 0` for a graph that should show a loop — a false
    negative, not a bug in the detector. `ecoli_lac_operon` was caught only
    because a human curator separately noticed the inconsistency and left a
    `circuitClassNeedsReview: true` rationale note; nothing forces that catch
    to happen.

    **Corpus scan** (`glmp-v2/processes/**/*.json`, current versions only —
    217 total): **85 processes show `loops: 0`** (identical count for
    `feedbackEdges: 0` — the two are perfectly correlated in this corpus).
    Of those, **77 carry no `circuitClassNeedsReview` flag** — the exact
    uncaught-defect population this item exists to find.

    **Heuristic pass to prioritize those 77**, not just count them: extracted
    node-ID → label pairs from each Mermaid source (reusing the same
    `parse_mermaid`-adjacent bracket syntax, separately since the existing
    parser strips labels before cycle detection) and checked for duplicate or
    near-duplicate labels on different node IDs — the actual signature of the
    `ecoli_lac_operon` defect. Verified the method first against the known
    case before trusting it on the rest: correctly found `G`/`PP` ("Lactose
    Permease LacY" / "Lactose Permease", a substring relationship, not exact)
    in the already-flagged file.

    Result, tiered by confidence:
    - **11 processes with an exact-label duplicate** (highest priority —
      identical text on two different node IDs): `bacillus_sporulation_initiation`,
      `ecoli_e._coli_acid_resistance`, `ecoli_e._coli_flagellar_assembly`,
      `ecoli_e._coli_two_component_signaling`, `ecoli_heat_shock_response`,
      `ecoli_pentose_phosphate_pathway`, `ecoli_trp_operon`,
      `yeast_gcn4_starvation`, `yeast_glycolysis`, `yeast_pka_pathway`,
      `yeast_yeast_peroxisome_biogenesis`.
    - **24 processes with a substring-only duplicate** (lower confidence —
      spot-checked and much of this tier looks like ordinary biosynthesis
      pathway naming, e.g. `ecoli_arginine_biosynthesis`'s 15 pairs are
      mostly enzyme-name-contains-substrate-name, like "N-Acetylglutamate"
      vs. "N-Acetylglutamate Synthase" — different, real, correctly distinct
      entities, not the same node twice).
    - **42 processes with no duplicate-label signal at all** — likely
      genuinely acyclic, not misdetected.

    **One false positive caught and recorded, not silently fixed:**
    `ecoli_trp_operon`'s "exact" hit is `AZ='Tryptophan Synthase β'` ==
    `BA='Tryptophan Synthase α'` — these are **not** duplicates, they're the
    two real subunits of a genuine two-subunit enzyme complex. My
    normalization strips non-ASCII characters before comparing, so it
    collapsed `β` and `α` away and produced a false match. Flagging this
    explicitly rather than trusting the label — the heuristic has this
    specific, now-known blind spot (any pair distinguished only by a
    non-ASCII character, e.g. Greek-letter subunit names) and should be
    re-checked with unicode-aware normalization before anyone treats the
    11-item list as final.

    **Not done — explicitly needs a biologist, not Claude Code**, per this
    doc's own standing reminder: whether each exact-duplicate candidate is a
    real `ecoli_lac_operon`-style defect (same entity, two IDs, a hidden real
    loop) or legitimate biology (the same intermediate/step genuinely
    recurring at two distinct points in a process, e.g. yeast_gcn4_starvation's
    repeated "40S Scans from Cap" could be two real ribosome-scanning events
    in a reinitiation cycle, not one entity duplicated) is a judgment call
    this session can scope but not make. Presence-without-correctness, same
    family as the findability probe (item 21) but for structural/topological
    correctness rather than retrievability.

    **Follow-up audit (2026-08-04, Claude Chat): is the false positive itself
    a bigger finding than the candidate list?** The `ecoli_trp_operon` false
    positive (Tryptophan Synthase β/α collapsed by non-ASCII stripping) raised
    a real question — does that same stripping run anywhere in the actual
    production pipeline, where it could be silently merging distinct
    corpus-wide (α/β/γ subunits, σ factors, Δ mutants — Greek/special
    characters carrying real meaning is a recurring feature of this domain,
    not an edge case; `σ32` is already separately out-of-scope in the decoder
    backlog for a related reason). **Checked, clean result:** the stripping
    was confined to this session's one-off audit script, never run against
    real data. `create_text_for_glmp` (`copernicus-web`
    `mcp_server/tools/vector_search.py:1116`, the actual embedding-text
    builder) concatenates raw fields with no character filtering at all.
    Both dedup scripts in the pipeline
    (`copernicus-web/cloud-run-backend/scripts/dedup_chemistry_processes_stubs.py`,
    `glmp/k562-empirical-sequel/scripts/dedup_gene_circuit_classes.py`) have
    no ASCII-stripping normalization — the latter only lowercases a
    confidence label. The Mermaid parser's node-ID extraction
    (`mermaid_graph.py`'s `_first_id`) only ever reads the short arbitrary ID
    codes (`AZ`, `BA`), never derives them from label text, so cycle
    detection itself can't be affected either. **Also addressed:** the
    heuristic's `normalize()` step does lowercase and collapse whitespace
    before comparing, so case/whitespace variants would already be caught —
    the real remaining gap is same-entity-different-wording with no shared
    substring, plus the non-ASCII collapse already found. The 11 candidates
    are still a floor, not a ceiling, just via a narrower gap than
    case/whitespace.

    **Pre-sorted before sending to Lents (2026-08-04, Claude Chat), not
    left as ten undifferentiated rows.** A second candidate is checkable
    without biology, same class as the trp false positive:
    `yeast_yeast_peroxisome_biogenesis`'s duplicate labels are the node's
    own full text — `Pex3 (PMP Receptor)` vs. `Pex16 (PMP Receptor)`,
    `Dnm1 (Fission Dynamin)` vs. `Vps1 (Fission Dynamin)` — two named
    proteins sharing a role description, not one protein under two IDs.
    Confirmed against the raw Mermaid source before accepting it. The
    remaining nine, prior-probability sorted (Claude Chat's read, explicitly
    not adjudication — neither of us is a biologist): four likely-fine
    (`yeast_glycolysis`, `bacillus_sporulation_initiation`,
    `ecoli_heat_shock_response`, `ecoli_e._coli_flagellar_assembly`) where
    recurrence is textbook-expected; four genuinely-plausible
    (`ecoli_pentose_phosphate_pathway`, `yeast_pka_pathway`,
    `ecoli_e._coli_acid_resistance`, `yeast_gcn4_starvation`) where a missed
    feedback edge fits the biology. **One catch, recorded rather than
    silently applied:** Claude Chat's sort omitted
    `ecoli_e._coli_two_component_signaling` from all three tiers. Checked
    the raw Mermaid source directly before placing it anywhere: genuinely
    mixed evidence within the one process — the duplicated "OR: ompF or
    ompC?" decision recurring under both the high- and low-osmolarity
    branches reads like real EnvZ/OmpR biology (not a defect), but
    `J --> AD[High Osmolarity]` (a direct edge into a second
    identically-labeled node) looks more like the artifact pattern. Left
    unsorted rather than forced into a tier — flagged as its own row with
    the reasoning shown, not a confident guess dressed up as a sort.

    **Moved from a named draft to an open pre-registration (2026-08-04,
    Claude Chat, `6aa8cd4`).** The candidate list now lives at
    `docs/open-questions/loop-audit-candidates-2026-08-04.md` — addressed
    to nobody, not gated on Lents specifically, predictions recorded
    *before* any ruling so the pre-sort's own precision becomes measurable
    once rulings arrive (an "Outcome" column per row). The two false
    positives are named as a characterized error mode of the heuristic
    there, not just worked examples. Old location
    (`collaborations/krampis-virtual-cell/lents-questions-....md`, named
    for a reviewer who'd never seen or agreed to it) removed from the
    working tree — **still reachable in `glmp`'s public history at commit
    `954e6f0`**, since `git rm` does not erase history. Whether that
    warrants a history rewrite is explicitly Gary's call, not decided or
    executed here. The CRP PWM question (item 26) was deliberately not
    carried into the new file — it stays a Lents-specific scheduling fact,
    not an open question anyone can adjudicate.

    **Two related naming decisions, resolved 2026-08-04 (Gary + Claude
    Chat), recorded here so neither stays an open flag:**
    - **`collaborations/krampis-virtual-cell/` is not being renamed.**
      Considered because the directory names a collaborator the same way
      the removed draft did, but the cases differ: Prof. Krampis has seen
      the name in correspondence and hasn't objected — an active, ongoing,
      opted-in collaboration, not a name attached without agreement. The
      rename would also cost real breakage for no benefit: GitHub blob URLs
      embedded in paper-II, paper-III, and `synthesis-biorxiv.md`, ~12
      external path references, and a possible Jetson cron path. If ever
      revisited: check the deposit question first, then external
      references, then intra-folder scripts/cron paths, then `git mv` last
      — in that order, not reversed.
    - **Standing rule going forward:** don't put a person's name in a new
      path or filename until they've opted in. Krampis has (implicitly);
      Prof. Lents has not yet — no new files should carry his name until he
      has. **Existing exception, checked directly, not guessed:**
      `collaborations/krampis-virtual-cell/shared-diagrams-for-lents.md` is
      fine as-is — unlike the removed draft, its content is written in
      first-person direct address ("my distilled models... treat them as
      'my model, please correct,'" "a proposed edit I'd value your call
      on") and its 3-commit history (`f06d5bf` → `6623f6a` → `4753fbc`)
      shows it was built as active collaboration material from the start,
      not an internal document retroactively addressed to him. The filename
      matches what the file actually is. Not verifiable from the repo:
      whether he's actually seen it yet.

34. ~~**FINDING — Knowledge Engine "Node Explanation (OpenAI RAG)" does not ground
    on the clicked node**~~ (2026-08-03) — **FIXED AND DEPLOYED** (2026-08-04,
    `copernicus-web@9b90e9ef1`, Cloud Build `cf52f050`, revision
    `copernicus-podcast-api-00246-q6z`, confirmed `100%` traffic). Traced the frontend feature
    (`knowledge-engine` → Knowledge Map → click a node → "🧠 Node Explanation") to
    `/api/rag/answer` on `copernicus-podcast-api-phzp4ie2sq-uc.a.run.app`. Reproduced
    directly against the live endpoint, not inferred from the UI:
    - **Test 1** — real paper node `biorxiv_10.64898_2026.07.02.736007` ("HERC4 limits
      oxidative stress-induced DNA damage..."), `focus_id` set to that id,
      `mode=paper_explanation`, question = the frontend's own template text ("Explain
      this paper and its findings"). Result: the answer explained an unrelated paper —
      "bioRxiv: the preprint server for biology" — never mentioning HERC4. None of the
      50 returned sources was the clicked paper.
    - **Test 2 (control)** — `mode=general`, no `focus_id`, a real specific question
      ("What is the CRISPR-Cas9 mechanism?"): retrieval was genuinely on-topic (real
      PubMed/DOI-backed papers, real podcasts, real GLMP processes), answer accurate.
      The RAG mechanism itself works when a user types a real question.

    **Root cause found (2026-08-04):** `services/rag_service.py`'s
    `answer_question()` appended `focus_id` as a literal string onto the question
    (`f"{question} {focus_id}"`) before running semantic search. An opaque ID like
    `biorxiv_10.64898_2026.07.02.736007` carries almost no signal to an embedding
    model next to natural-language question text — retrieval was effectively still
    just matching the boilerplate question alone, exactly reproducing Test 1's
    symptom. Citations were never fabricated (real titles/DOIs from the corpus),
    just irrelevant to the node clicked — misdirected retrieval, not hallucination,
    confirmed.

    **Fix:** added `_fetch_focus_document()` — when `focus_id` is present, fetch
    that exact document directly by ID (tries `research_papers`, `glmp_processes`,
    `atap_graphs`, chemistry/physics/computer_science/biology `_processes`, in
    order) and guarantee it as citation `[1]`, instead of hoping a mangled query
    string wins a semantic ranking against its own question text. Semantic search
    still runs on the plain question for neighbor context. Falls back to
    semantic-only retrieval (logged warning, no crash) if `focus_id` doesn't match
    any collection.

    **Verified against live Firestore + OpenAI before committing, not just
    compiled or code-reviewed:**
    - `_fetch_focus_document('biorxiv_10.64898_2026.07.02.736007')` correctly
      returns the HERC4 paper's real title/abstract/DOI.
    - Full `answer_question()` re-run of the exact Test 1 scenario: the generated
      answer now explains the actual clicked paper (HERC4 DNA damage) instead of
      the unrelated preprint-server paper, focus document as citation `[1]`.
    - `concept_explanation` path (the open question from the original finding)
      verified separately against a real GLMP process ID
      (`glmp_processes/ecoli_iron_homeostasis`) — correct title/description
      fetched, confirming it had the same bug and now has the same fix.
    - Nonexistent `focus_id` degrades gracefully: warning logged, falls back to
      semantic-only, no crash, no fabricated grounding.

    **Also observed, separate minor bug, not fixed here:** `similarity_score` is
    `0.0` on every semantically-retrieved source in both original tests, on-topic
    or not — the field is never populated, not just low. Out of scope for this
    fix (the injected focus document correctly shows `1.0`; the pre-existing
    semantic-search scoring bug is untouched).

    **Deployed and verified live (2026-08-04), per Gary's explicit go.**
    `gcloud builds submit --config cloudbuild.yaml .` — build `cf52f050`
    (`SUCCESS`, 4m52s) — deployed revision `copernicus-podcast-api-00246-q6z`,
    confirmed `latestRevision: true` / `percent: 100`. Not just trusted the
    build status: called the live `/api/rag/answer` endpoint reproducing the
    exact Test 1 scenario against production. Citation `[1]` is the HERC4
    paper with `similarity_score: 1.0`, and the generated answer correctly
    explains HERC4/oxidative-stress-induced DNA damage — the same bug, on the
    same live service, now produces correct output. Item fully closed.

    **Two follow-up checks Claude Chat raised, both closed clean:**
    - **Cache risk** — none. Confirmed by calling the live endpoint twice with
      the identical question + `focus_id`: `generated_at` differed by seconds
      both times, proving no response is ever cached or replayed. No
      `cache-control`/`age`/`x-cache` headers, no caching code in
      `rag_service.py`/`routes.py`, no stored-answers Firestore collection
      found anywhere in `cloud-run-backend`. The fix reaches every future
      query immediately; nothing needed invalidating.
    - **Was the concatenation bug a pattern, not one call site?** No —
      checked every `embed_text()`/`search_semantic()` call site in
      `cloud-run-backend`. Every other one builds its embedding text from a
      proper `create_text_for_X(data)` content builder (title/abstract/
      description); the dev/test CLI scripts take plain user queries with no
      ID involved. `f"{question} {focus_id}"` was genuinely isolated to the
      one call site already fixed.

35. **PROPOSE — rebuild automated science-video ingestion (2026-08-03, from papers/
    videos growth-plan discussion).** Confirmed via `sciencevideodb`'s own README:
    there is currently **no automated ingestion running at all** — the 582-video
    catalog is a static JSON snapshot on GCS, last touched by a "now-inactive process."
    A real, tested YouTube API client (10/10 tests passing) exists but sits in a
    separate, dormant `github.com/garywelz/sciencevideodb` monorepo (last active
    December 2025), disconnected from any working database, search, or frontend.
    "Increase the video rate" is therefore a rebuild-first problem, not a tuning
    problem — there is no live cadence to speed up.
    **Needs scoping, not yet built:**
    - Decide: resurrect the dormant repo's ingestion client, or write a smaller one
      against the current static-catalog architecture (channel list → oEmbed/YouTube
      Data API → append to `videos-metadata.json` on GCS, same shape as today's file).
    - Decide where new videos land — today there's no database, just a GCS JSON file;
      channel-attribution bugs already found once this way (item 27) argue for some
      verification step on ingest, not raw appends.
    - Cron/schedule equivalent to the paper scout pattern (Jetson cron, or a Cloud Run
      scheduled job — video ingestion doesn't obviously need Jetson's edge placement
      the way the paper scout does). Cron/schedule design is Cursor's domain per
      `AGENT_ROLES.md`.
    Queue entry only — design and execution ownership still to be decided.

36. **PROPOSE — domain-tuned scouts for GLMP and ATAP frontiers (promoted from
    backlog, rescoped 2026-08-03).** Original note: current scouts aren't tuned to
    either engine's actual research frontier, only to a coarse `discipline` field
    (biology: 29,184, mathematics: 17,153 papers). Rescoped after reading the live
    scout config directly:
    - **GLMP side is partially already true.** `daily_scout_config.json` (v2.0) is
      already 100% biology/GLMP-tuned — 10 PubMed query clusters on gene regulation,
      operons, regulatory circuits, synthetic biology, key GLMP-relevant authors/labs
      (Voigt, Weissman, Regev, Yanofsky, Schleif, Stormo), plus arXiv q-bio categories
      and bioRxiv subject filters. What it is **not** tuned to: `research_focus.json`'s
      actual active frontier questions — it's discipline-relevant, not
      frontier-relevant. Gap is narrower than the original note assumed.
    - **ATAP side has no active scout at all.** No math/logic/algorithms query set
      exists anywhere in `daily_scout_config.json` — `sources.nasa_ads` is even
      disabled. ATAP's 17,153-paper corpus is not growing via any automated
      acquisition today; unclear by what process it grew historically (likely manual/
      `progframe`-side work, per `AGENT_ROLES.md`'s migration note).
    **Needs scoping, not yet built:**
    - A parallel `atap_scout_config.json`-equivalent: query clusters against ATAP's
      `research_focus.json` frontier (axiomatic theories, algorithm-capsule
      regularity, the n=3 pattern), not just "mathematics" broadly — same
      discipline-vs-frontier gap as GLMP's, but starting from zero instead of partial.
    - Whether ATAP papers should route through PubMed/bioRxiv/arXiv (arXiv `math.*`
      categories, most likely) or need a different source entirely (MathSciNet/
      zbMATH-style, if accessible) — not evaluated yet.
    - Re-tune GLMP's existing config against `research_focus.json` specifically, not
      just add ATAP from scratch — same frontier-vs-discipline fix applies to both.
    Supersedes the backlog note below — tracked here, not there.

37. **PROPOSE — growth plan: paper/video acquisition + podcast-to-video pipeline
    (2026-08-03, design-only, queue entry).** Full draft grounded in direct
    inspection of the live scout config, `sciencevideodb`'s README,
    `podcast_generation_service.py`, and three prior December-2025 planning docs in
    `copernicus-web/docs/` (`DESCRIPT_INTEGRATION_THOUGHTS.md`,
    `docs/video/VIDEO_GRAPHICS_INTEGRATION_ANALYSIS.md`,
    `docs/video/VIDEO_FEATURE_ROADMAP.md` — architecture-only, never implemented
    beyond dead scaffolding). Covers, at a summary level (full plan not yet filed
    in a repo — currently a local draft pending Gary/Claude Chat review):
    - **Papers:** tune before scaling — item 36 (frontier-tuned scouts) should land
      before raising `daily_scout_config.json`'s volume caps; enable the
      already-wired-but-disabled NASA ADS source as a free win.
    - **Videos:** item 35 covers this — no dependency either direction.
    - **Podcast-to-video, gradual:** four phases — (A) inline graphics shown in the
      web player, no video file; (B) short animations (Matplotlib/Plotly); (C)
      timed still-frame sequences (A+B's assets, timestamped); (D) full MP4
      composition via FFmpeg/MoviePy, reusing the real-but-unfinished
      `VideoGenerationService` scaffolding and the marked-but-commented-out
      extension point at `podcast_generation_service.py:2618-2630`. Descript stays
      optional manual-polish only, per the Dec-2025 analysis's conclusion (its API
      doesn't cover graphics/overlay/timeline composition) — never load-bearing for
      the automated pipeline.
    - **FINDING, confirmed via full-repo grep:** podcast generation today sources
      content from **live external PubMed/arXiv search**
      (`research_pipeline.py`), not from the internal 63k-paper corpus or any
      process/flowchart collection (`glmp_processes`, `atap_graphs`, etc.) — the
      podcast pipeline and the knowledge base are fully disconnected systems today.
      Fixing this is a prerequisite for KB-sourced podcasts, not a side effect of
      anything already built.
    - **Dependency flag:** a KB-sourced content path should NOT route through the
      `/api/rag/answer` endpoint — item 34 already found it doesn't reliably anchor
      on a specific requested document. Recommend a direct Firestore read by
      process/paper ID instead, which also sidesteps the dependency entirely since
      the pilot always knows exactly which process it wants.
    - **Pilot scope:** GLMP + ATAP first (richest structured source material,
      already-curated citations — e.g. `research_focus.flagged`'s existing lac
      operon seed), Phase A only (inline graphics, no animation/video yet). The one
      genuinely net-new technical piece: **no Mermaid→image renderer exists
      anywhere in the repo** (confirmed via grep; `mermaid_images/` samples are a
      manual one-off, not a script's output) — building this is the pilot's real
      dependency, everything else in Phase A is assembly of existing pieces.
    **Ownership:** backend/pipeline work (Cloud Run service code, Jetson/cron
    scheduling) — Cursor's domain to execute per `AGENT_ROLES.md`. Design-only for
    now; not built, not scheduled, not assigned.

38. ~~**Ask for Cursor — check whether the AUTO-STATUS cron is still running**~~ —
    RESOLVED (2026-08-03/04). **Not stalled — wrong artifact was being read.**
    Cursor confirmed `build_master_todo.py` fires every AM/PM cycle (through at
    least Sun PM, `2026-08-04T01:18:29Z`, `status=fresh`) from the git checkout
    path (`/media/sdcard/glmp/scripts/build_master_todo.py`, per item 23's fix),
    but it **does not overwrite this git-tracked file's AUTO-STATUS block** — it
    writes to `/media/sdcard/status/GLMP_MASTER_TODO.md` and GCS instead, by
    design. Independently verified against the live GCS copy, not just taken on
    report: `GLMP_STATUS.html` on `regal-scholar-453620-r7-podcast-storage` shows
    `AUTO-GENERATED 2026-08-03T21:18:27-04:00` and `63,186` papers (`gsutil stat`
    confirms `Update time: 2026-08-04T01:18:29 GMT`, the same second) — matches
    Cursor's report exactly. The `2026-07-05` stamp this item originally flagged
    is a committed snapshot of this doc from that date, frozen in git, not
    evidence of a stopped cron — this file's own AUTO-STATUS block will always
    look stale unless someone deliberately commits a regenerated snapshot, which
    the design intentionally avoids. Live self-reporting lives at
    `/media/sdcard/status/` + GCS, not in this git file.

39. ~~**Check the real ATAP/mathematics corpus for the Mermaid syntax bugs
    found in PR #5**~~ — RESOLVED (2026-08-04), clean result. **Scope note:
    this corpus is `huggingface-space/mathematics-processes-database/` in
    `copernicus-web` — a different repo, different files, and a different
    kind of check entirely from item 33's GLMP corpus (217 biology
    processes, `glmp-v2/processes/**/*.json`). This item never touched
    classification or content correctness — only whether the Mermaid syntax
    parses without rendering errors. A clean syntax scan is not a clean
    correctness scan; it says nothing about whether any chart's content is
    final. **Correction (2026-08-04):** an earlier version of this note
    also invoked GLMP's 5-class-system caveat as applying to this corpus
    too — checked `atap/docs/research_focus.json` directly and that's
    wrong. ATAP has its own, entirely separate frontier questions
    (algorithm-capsule regularity, proof-role vocabulary adequacy, whether
    Mermaid is even the right representation) with no mention of a 5-class
    system or Lents-classification review — that caveat is specific to
    GLMP's biology corpus (see item 33) and doesn't transfer here just
    because both are "process charts." The correct, narrower claim for this
    corpus: syntax-clean, content/correctness unverified — not "provisional
    pending the same GLMP decision."**

    **The note also lives where a reader would actually see it, not just
    here.** This to-do isn't what someone browsing the charts consults —
    added the same syntax-vs-correctness caveat directly to the live
    catalog page a real reader lands on (`mathematics-database-table.html`
    header, `copernicus-web@f14209ab7`), and verified it live on the
    deployed GCS page after publishing, not just committed to git.

    Closed PR `cursor/mathematics-database-flowchart-errors-d178` (item 28)
    fixed real Mermaid rendering bugs — `style` directives concatenated onto
    node/edge statements, invalid `{[...]}` decision-node syntax, raw HTML
    embedded in labels, all causing intermittent parse failures — but only
    against root-level scratch/temp copies, never the real corpus.

    **Scanned all 280 files** in the actual corpus
    (`huggingface-space/mathematics-processes-database/processes/**/*.html`
    — confirmed the correct directory first: the sibling `collections/`
    dir's 96 files have zero Mermaid content, a different page type
    entirely, out of scope). Built targeted checks for each of the three
    named patterns:
    - Concatenated `style` directives (more than one `style X ...` on a
      single logical line, or a `style` clause following other node/edge
      content on the same line): **0 files.**
    - Invalid `\w+\{\[` decision-node syntax: **0 files.**
    - Raw HTML in labels (any `<letter` not part of a `<br/>` tag): **2
      files flagged, both confirmed false positives** on inspection —
      `information_theory-channel.html` and `information_theory-coding.html`
      both contain `R<C ⇒ reliable`-style lines, which is literal
      information-theory notation (Rate < Capacity), not malformed markup.

    **Zero real instances of any of the three patterns exist in the live
    corpus.** Nothing to fix — the "decide whether a fresh, correctly-scoped
    fix is warranted" step this item originally called for is moot; there's
    no rendering defect to scope a fix against. (Whether the charts'
    *content* needs revision is a separate, open question — see scope note
    above.)

40. ~~**FINDING (Core-scoped) — trace propagation of the pre-correction
    computational pattern counts**~~ — RESOLVED (2026-08-04). Traced the exact
    figures the analysis corrects (243 "pattern instances" / 545 visualizations
    / 45.1% prevalence, broken down OR 110, NOT 45, Feedback 31, AND 17, State
    Machines ~25, Decision Trees ~15 — from `detailed_overlap_analysis.md` and
    `glmp_pattern_analysis.md`, both merged into `copernicus-web` this session)
    across every surface item 40 named:
    - **Live GLMP Space** (`hf-spaces/glmp`, both `index.html` and `README.md`):
      not present. Git history shows `545` *was* present as of an Aug/Oct 2025
      snapshot, but a large October 15, 2025 rewrite (`905df3e`, -869/+423
      lines) removed it — incidentally, not as a deliberate correction, but
      the wrong figure has been off the live page for over a year regardless.
      No current pattern-prevalence stat under any other numbers exists on the
      page at all — nothing to correct because nothing quantitative is
      claimed there now.
    - **Programming Framework Space, CopernicusAI Core Space, the GCS database
      table** (`glmp-database-table.html`): no match, any of the three figures.
    - **The deposited Zenodo methods paper** — the highest-stakes surface,
      checked directly: `collaborations/krampis-virtual-cell/mermaid-perturbation-design-zenodo.md`
      (source for DOI `10.5281/zenodo.20831780`) — no match. No erratum
      needed; the deposited record never carried this figure.
    - **Paper drafts and proposals** (`nsf-proposal/`, `doe-proposal/`,
      `papers/` in `copernicus-web`): every apparent hit traced individually
      and confirmed noise — all matches on "545" were the unrelated retrieval
      metric `nDCG@10 = 0.545` (a different evaluation entirely), one "243"
      hit was a journal page-range citation. No genuine occurrence anywhere.
    **Conclusion: nothing to correct.** The inflated figure was live on the
    GLMP Space roughly a year ago, was already gone before this month's audit
    ever started, and never reached the deposited paper, the other Spaces, or
    any draft document. PR #977c's merge (`copernicus-web@1cf51477e`) can be
    treated as fully handled — the concern that prompted this item (a merge
    reading as "done" while a public record still carried the error) does not
    apply here; verified, not assumed.

41. **File cross-suite GitHub housekeeping findings, not executed (2026-08-04).**
    Full survey in `docs/GITHUB_HOUSEKEEPING_TODO.md` (this repo) — item 28 was
    scoped `copernicus-web`-only, so everything below was found during that
    survey but belongs to another project or needs Gary's decision first.
    Filed, not actioned:
    - **A2 — `atap` has no README.** Public repo, 4 commits; GitHub renders the
      CC0 legal text as the landing body instead of a description. Highest
      external-visibility defect in the suite. Unblocks the reorg plan's Part 1
      "retitle ATAP" item. Owner: ATAP project.
    - **B — per-repo defects table**, one row each for `atap` (also missing
      `research_focus.json`, confirms reorg plan Part 4's open item),
      `sciencevideodb` (README has duplicated YAML front-matter *and*
      declares `sdk: gradio` against the actually-live `sdk: static`),
      `metadata-database` (README is one future-tense sentence for a live
      Resource backing ~62,900 papers), `glmp` (README cites ~62,700 papers
      against the live ~62,900 — consider a dated/generated figure, not a
      hardcode), `progframe` (README still says "Mathematics database",
      predates the ATAP rename — **unverified whether the prose should change
      even where GCS paths legitimately keep the old name**).
    - **C1 — license posture is inconsistent, looks accidental**: `copernicus-web`
      MIT, `atap` CC0, `progframe`/`metadata-database` have unchecked LICENSE
      files, **`glmp` and `sciencevideodb` have none** (defaults to
      all-rights-reserved) — `glmp` being unlicensed is the sharpest gap given
      it's the suite's most public-facing research surface. Gary's call.
    - **C2 — no `CONTRIBUTING.md` in any suite repo**, relevant to the reorg
      plan's Part 4 collaborator-onboarding work.
    - **C3 — PR disposition** — superseded, already done: item 28 records all
      four `copernicus-web` PRs as merged/closed with rationale.
    - **C4 — no CI anywhere** in `copernicus-web` beyond GitHub's own
      dependency-graph bot. Given the PI-control collaboration model
      (`governance/SUITE_REORG_PLAN.md` §4), this may be deliberate rather than
      an oversight. Flagged, not prescribed.
    Owner per finding is noted above; nothing in this item is Claude Code's to
    execute unilaterally — visible actions on other repos need their own go.

42. **PROPOSE — surface item 34's fallback path as a self-reporting counter,
    not a Cloud Run log line (2026-08-04, Claude Chat).** The RAG grounding
    fix (item 34) falls back to semantic-only retrieval when `focus_id`
    doesn't resolve to any known document, logging a `structured_logger.warning`
    and nothing else. If that path starts firing regularly in production — a
    frontend bug sending malformed IDs, a renamed process ID no longer
    matching, a new content collection not yet added to `_FOCUS_ID_COLLECTIONS`
    — the symptom is exactly item 34's original bug, silently returning,
    invisible unless someone goes looking in Cloud Run logs by hand. Not
    scoped or built: needs a persistence mechanism (a Firestore counter
    written on each fallback, or a Cloud Monitoring log-based metric) plus a
    read path into `glmp`'s AUTO-STATUS, matching the `findability_probe.py` →
    `read_findability_status()` pattern already established for item 21.
    Cross-repo (counter lives in `copernicus-web`, surfaced in `glmp`) —
    same shape as item 34 itself.

43. **Researcher-cited intake — DONE end-to-end (2026-08-05): built, tested,
    ingested, and its own ingestion bug found and fixed live.** Plan:
    `copernicus-web/huggingface-space/scripts/acquire_papers/`
    `43-researcher-cited-intake.md` (placement note: put next to the code it
    documents, not in a governance/docs folder — flagging per the standing
    governance-doc-scatter open question rather than assuming this was the
    obviously right call). A front door, not a pipeline: when a researcher
    cites a paper (email, Zoom, review comment), it enters the corpus carrying
    who/when/why. Currently the only inbound literature route for ATAP (no
    scout exists there — see item 36) and ungated unlike A1/A2 (items 25/36).
    Built as `researcher_cited_intake.py`, same directory — manual invocation
    only, no cron, no interface, per the plan's own recommendation. Accepts
    DOI/PMID/arXiv ID/bibcode/publisher URL (incl. Cell Press PII)/free text
    plus `--cited-by`/`--cited-date`/`--cited-context`/`--cited-project`;
    reuses the existing Crossref/PubMed/arXiv/bioRxiv-medRxiv/NASA-ADS
    resolvers and `validate_metadata.py`/`deduplicate_papers.py` rather than
    reimplementing any of them. On ambiguous or failed resolution, queues the
    original text verbatim and exits non-zero — never a best-effort guess
    (item 25's lesson, applied here before it bit here too).
    **One correction made before building:** the plan's draft proposed
    `source: "researcher_citation"`, which fails `metadata_schema.json`'s
    closed six-value `source` enum. Fixed to a separate `acquisition_channel`
    field (schema has `additionalProperties: true`, so no schema edit
    needed) — `source` stays whichever resolver actually ran.
    **Test case resolved (2026-08-05), the awkward path proven, not just
    described:** Prof. Lents' Biophysical Journal citation
    (`https://www.cell.com/biophysj/fulltext/S0006-3495(22)00045-5`, a
    publisher URL in PII form, no DOI) → Crossref indexes Elsevier/Cell Press
    PIIs (punctuation stripped) as each work's `alternative-id` and supports
    `filter=alternative-id:<value>` as an exact-match lookup — not a scrape of
    cell.com, which is Cloudflare-gated and returned 403 when tried directly.
    PII → `alternative-id` `S0006349522000455` → exactly one match: DOI
    `10.1016/j.bpj.2022.01.016`, "Inducer exclusion, by itself, cannot
    account for the glucose-mediated lac repression of *Escherichia coli*"
    (Aggarwal & Narang, *Biophysical Journal* 121(5):820-829, 2022) — directly
    on-topic for the cAMP-CRP question Lents was working, confirming this is
    the right paper. Dry run only (no `--write`): validates at 91.7% quality
    (`validate_metadata.validate_paper`; the only gap is a missing `abstract`,
    which Crossref doesn't carry for this Elsevier record and which isn't
    required), confirmed **not** already in `research_papers` by a live
    Firestore query, confirmed absent from the local `crossref/` mirror
    (12,235 files) via `deduplicate_papers.are_duplicates`. **Nothing written
    to the corpus — holding for Gary's go per the plan's explicit gate**
    before any `--write` run.
    **Two related findings surfaced, not fixed (out of scope for this task):**
    `validate_metadata.py`'s hardcoded `valid_sources` list is missing
    `biorxiv`/`medrxiv` (both valid per the schema's six-value enum) — would
    wrongly fail any bioRxiv/medRxiv-sourced record, including one resolved by
    this same script's `10.1101/`-prefix preprint-first path. And: an
    already-in-corpus re-citation (a researcher citing a paper this script's
    dedup check finds already present) currently just reports the duplicate
    and writes nothing — the provenance signal (who/when/why re-cited it) is
    dropped rather than merged onto the existing doc, since that would be a
    separate production write not scoped here. Both recorded as open questions
    in the plan doc, not actioned.
    **Not done:** the intake-mechanism question (manual vs. repo-file-plus-cron
    vs. form vs. email) is still open by design — plan recommends starting
    manual for a month before committing to an interface; PMID resolution is
    implemented but untested in this environment (no `biopython` installed
    here — it's expected to already be present wherever the batch acquirers
    actually run); bibcode resolution likewise implemented but untested (no
    `NASA_ADS_API_TOKEN` exercised this session).
    **Gary's go given; `--write` and the real ingest both run (2026-08-05).**
    `researcher_cited_intake.py --write` produced the metadata JSON (same
    record shown above). `cloud-run-backend/scripts/ingest_papers_from_metadata_json.py`
    was run scoped to that one file only (an isolated single-file `--root`,
    not the full local mirror, specifically to avoid accidentally mass-ingesting
    whatever else happens to sit in the local `metadata-database/papers/`
    checkout) — dry-run first (would-write: 1, 0 gate hits), then for real.
    Live-verified: `research_papers/crossref_10.1016_j.bpj.2022.01.016` exists
    with correct title/DOI/authors/journal.
    **FINDING, caught only by checking the live doc rather than trusting the
    ingest script's own success output:** none of the five provenance fields
    (`acquisition_channel`, `cited_by`, `cited_date`, `cited_context`,
    `cited_project`) made it into Firestore. Root cause:
    `_to_firestore_paper()` in the ingest script hardcodes an explicit
    allowlist of fields it copies from source JSON to the Firestore doc —
    provenance was never on that list, since no prior caller had ever
    supplied it. The paper became findable; *why it was worth adding* — the
    entire stated point of item #43 — was silently dropped at the very last
    step. Same presence-without-correctness shape as items 21/28/33 in this
    doc, just in a new location.
    **Fixed same-day**, `copernicus-web@9a7f524cb`: added a small additive
    block to `_to_firestore_paper()` passing through the five fields when
    present, verified against both a provenance-bearing sample (all five
    fields correctly appear) and an ordinary scout-acquired sample (no
    provenance keys added — existing behavior unchanged for every other
    record type). **Backfilled the already-ingested doc** via a Firestore
    merge update sourced from its own JSON file (not re-run through the
    ingest script, since `skip_existing` would have just skipped it) —
    live-verified post-merge: all five fields present with correct values.
    Item #43 is a complete, working, live-proven path from a researcher's
    citation to a retrievable, provenance-bearing corpus entry — **DONE
    status caveated, not unqualified: see item 45**, a real gap in this same
    feature (already-in-corpus re-citations) that's flagged, not built. The
    ingest-script bug this item's catch led to is generalized in item 44,
    which outranks everything else on this list.

44. **FINDING (Core-scoped) — the ingest allowlist was dropping 15 of
    `metadata_schema.json`'s 31 fields, corpus-wide, for every source, since
    before item #43 existed. FIXED same-day (2026-08-05).** Claude Chat's
    follow-up question on item 43's provenance-drop catch: "is the allowlist
    dropping more than provenance?" — checked directly rather than assumed
    either way. Diffed `_to_firestore_paper()`'s explicit field list against
    the schema's 31 properties: `year`, `citation_count`, `bibcode`, `issn`,
    `issue`, `journal_full`, `language`, `page`, `published_date`,
    `publisher`, `updated_date`, `volume`, `author_string`,
    `deduplication_method`, `deduplication_confidence` had no path into
    Firestore at all, for any source. **Confirmed live, not left as a
    synthetic worst case:** spot-checked 3 real documents each across
    crossref/pubmed/arxiv/biorxiv (`research_papers`, **63,198 docs total**)
    — every sampled doc had zero of the 15 fields — and a corpus-wide count
    on a non-empty `year` filter returned **1** document out of 63,198. This
    predates item 43 entirely; item 43 only surfaced it because its five new
    fields happened to be the ones someone finally checked for.
    **Fixed** (`copernicus-web@a92b14c2f`), same additive pattern as the
    provenance fix: never overwrites a key already set, skips fields absent
    from the source JSON, changes nothing for a record that never carried
    them. Verified against a synthetic all-31-fields-populated record (all
    15 previously-dropped fields now appear) and an ordinary minimal record
    (no new keys added — regression-checked). Backfilled item 43's own test
    doc with its now-recovered fields (`year`, `citation_count`, `volume`,
    `issue`, `page`, `publisher`, `issn`, `language`, `author_string`) as a
    single-doc proof; the doc now carries all 31 schema fields it has values
    for.
    **NOT done — the actual scale question, deliberately not answered
    unilaterally:** whether/how to backfill the ~63,197 other already-ingested
    docs. That needs each doc's original source JSON, and it's genuinely
    unknown how many of those still exist (Jetson-side acquisition output,
    partially mirrored locally, not necessarily complete or 1:1 with what's
    live in Firestore) — a much larger and riskier undertaking than a single
    doc's merge update, and a scale-of-effort decision for Gary, not
    something to start speculatively.
    **Retrieval/ranking dependency check, done (2026-08-05).** Grepped every
    non-script backend file touching `research_papers`
    (`vector_search.py`, `rag.py`, `rag_service.py`, `knowledge_map_service.py`
    + its routes, `papers/routes.py`, `content/routes.py`,
    `cross_component.py`) for all 15 fields. Semantic search/RAG (the actual
    embedding-based retrieval path) reference none of them — ranking there
    runs purely on the vector, unaffected either way. Two real dependencies
    found, both confirmed live against production, not just read in the
    code:
    - **`/api/papers/query`'s `min_citation_count` filter has been
      effectively dead code for the corpus's entire existence.** It runs a
      Firestore inequality `where('citation_count', '>=', N)`, which
      excludes any doc lacking the field entirely (standard Firestore
      semantics, confirmed empirically: `citation_count >= 0` matched
      exactly **1** doc out of 63,198 — our own backfilled item-43 test
      doc). Today's fix makes this correct going forward for newly-ingested
      papers; the ~63,197-doc backlog stays invisible to this filter until
      backfilled.
    - **Knowledge Map date-range filtering (`_paper_passes_date_filters`)
      falls back `published_at` → `published_date` → `year`, and silently
      *passes* (does not exclude) any doc with none of the three** — so
      date-range browsing has been unable to actually narrow the bulk of
      the corpus by date; results have been over-inclusive, not wrongly
      empty. `published_at` turns out to come from a **different, third
      writer** (see below), not from this ingest script at all.
    **Bigger finding, surfaced by chasing `published_at`'s origin:**
    `research_papers` has **at least three independent writers with three
    different document shapes** — this ingest script (source-prefixed doc
    IDs), `cloud-run-backend/scripts/sync_research_papers.py` (a `Paper`
    object sync, contributes `published_at`), and the
    `/api/papers/upload` FastAPI endpoint (UUID `paper_id` docs, minimal
    fields, explains the UUID-style doc IDs seen while spot-checking).
    Same "no single writer discipline" shape as item 24's `atap_graphs`
    fix, now found here too — today's allowlist fix only closes the gap
    for one of the three writers.
    **Third writer identified (2026-08-05), by request:**
    `cloud-run-backend/scripts/sync_research_papers.py`. It reads a `Paper`
    row from a *separate* PostgreSQL "research metadata" database (a sibling
    service/repo, `copernicusai-research-metadata`, not present in this
    checkout — the script's own import path assumes it's cloned next to
    `copernicus-web` and exits with an explicit error if it isn't found) and
    writes it to `research_papers` using the Postgres row's own `paper_id`
    (a UUID) directly as the Firestore document ID — the source of the
    UUID-style doc IDs. Confirmed field-for-field, not by name alone:
    `convert_paper_to_firestore_format()` writes exactly `paper_id`,
    `arxiv_id`, `doi`, `title`, `authors`, `abstract`, `published_at`,
    `categories`, `sources` (defaults to `["arxiv"]` if the Postgres row
    doesn't set it), `ingested_at`, `updated_at`, `created_at`, `discipline`
    — 13 fields, matching the live sampled UUID doc's 16 keys once the
    other 3 (`embedding`, `embedding_model`, `embedding_updated_at`) are
    accounted for: this script's own embedding attempt writes
    `embedding_updated` (no `_at`) inline, but the live docs show
    `embedding_updated_at`, meaning the embeddings on these docs were added
    afterward by a *separate* pass (matching `_at`-suffix naming
    convention used elsewhere, e.g. `backfill_research_paper_embeddings.py`)
    rather than by this script's own inline attempt — a fourth touch-point
    on the same collection, though only for embeddings, not the rest of the
    document. Verified live: sampled 15 UUID-style docs, all 15 have
    `sources: ["arxiv"]` exactly matching this script's default. Not a rogue
    or abandoned script — actively documented
    (`docs/planning/SYNC_SCRIPTS_READY.md`) as a manual, Jetson-run batch job
    (`python3 scripts/sync_research_papers.py [--dry-run] [--limit N]
    [--no-skip-existing]`), last touched 2026-07-23 in the same commit
    (`c066ed185`) that fixed the hardcoded-embedding-model bug (item 4) —
    so it's a live, maintained part of the pipeline for arXiv papers sourced
    from that separate Postgres database, running in parallel to (not
    instead of) the JSON-file-based `acquire_papers/` →
    `ingest_papers_from_metadata_json.py` path this whole item-44 thread has
    been about. **Not evaluated further, out of scope for this ask:**
    whether `sync_research_papers.py`'s own field set has the same
    schema-completeness gaps as `ingest_papers_from_metadata_json.py` did
    (it doesn't write `year`, `citation_count`, or most of the same 15
    fields either) — a legitimate follow-on question, not answered here.
    **Checked (2026-08-05), by request — different shape of gap, not the
    same bug.** Grepped every `paper.<attr>` access in the file: exactly 11
    distinct attributes (`paper_id`, `arxiv_id`, `doi`, `title`, `authors`,
    `abstract`, `published_at`, `categories`, `sources`, `ingested_at`,
    `updated_at`), and **all 11 are forwarded to Firestore** —
    `convert_paper_to_firestore_format()` doesn't read a field and then
    discard it the way the other script's allowlist did. So this isn't a
    code-level drop; if there's a gap, it's upstream, in whether the
    Postgres `Paper` row/table even *has* columns for `year`,
    `citation_count`, `volume`, `issue`, `page`, `journal`, `keywords`,
    `language`, `publisher`, `issn`. **Genuinely can't verify that from
    here** — `copernicusai-research-metadata` (the sibling repo defining
    the `Paper` model) isn't cloned in this checkout, and no planning doc in
    `copernicus-web` documents that table's schema; marked as a real limit,
    not guessed past.
    **One gap findable without the sibling repo, because it needs no new
    source data at all:** no `url` or `pdf_url` field is ever set, despite
    `arxiv_id` being present on every doc this script touches. Every other
    arXiv acquirer in this codebase (`acquire_arxiv_batch.py`'s
    `parse_arxiv_entry`) already derives
    `f"https://arxiv.org/abs/{arxiv_id}"` — the same derivation would work
    here with zero dependency on the Postgres schema.
    **Fixed same-day** (`copernicus-web@1f12b3f4b`), once asked: sets `url`
    and `pdf_url` from `arxiv_id` when present, guarded so it adds nothing
    when absent — verified against both cases with a mock `Paper` object
    (couldn't import the real one; its module chain requires the sibling
    repo). Additive only, same pattern as every other fix in this item.
    Applies going forward to new syncs; the already-synced ~12,040 UUID docs
    aren't backfilled by this (same re-run-the-script mechanics as any other
    field here — `sync_research_papers.py --no-skip-existing` would refresh
    them, not attempted here since it wasn't asked for and touches the live
    collection at that scale).
    **Superseded, resolved a different way (2026-08-05).** Handed to
    Cursor as a `sync_research_papers.py --no-skip-existing` re-run;
    Cursor caught a real problem before running it and stopped: Jetson's
    checkout was 3 commits behind (still on `8640e7983`, pre-dating the
    `url`/`pdf_url` fix); the `copernicusai-research-metadata` GitHub URL
    resolves to an empty stub, not the real Postgres app; a Cloud SQL
    instance (`research-metadata-db`) exists but has no matching Secret
    Manager URL or proxy set up anywhere found. More fundamentally,
    `--no-skip-existing` calls `.set()`, which **rewrites the whole
    document and re-triggers embedding generation** — not the two-field
    patch this was supposed to be. Cursor proposed the actually-correct
    fix instead: a Firestore-only pass, no Postgres involved at all —
    stream `research_papers` for `arxiv_id`-bearing docs missing
    `url`/`pdf_url`, `update()` (merge, not `set()`) just those two derived
    fields. Dry-run first: paginated the full 63,198-doc collection
    (a single unbounded `.stream()` timed out past ~25k docs; cursor-based
    `order_by("__name__")` batches of 1000 fixed it) — **23,025 docs would
    update**, not the ~12,040 originally scoped. The other 10,985 are
    `arxiv_`-prefixed docs from the *other* writer
    (`ingest_papers_from_metadata_json.py`), which always set `url`
    correctly but never set `pdf_url` at all — a second, previously-unflagged
    gap (`pdf_url` isn't in `metadata_schema.json`'s strict property list,
    so the earlier 15-field schema audit never caught it). Ran the real
    backfill after showing the expanded scope and getting explicit go:
    batched Firestore `update()`s (400/commit), touching only missing
    fields, matching the dry-run count exactly — **23,025 updated, 40,173
    skipped (no `arxiv_id`), 0 errors**. Live-verified: a UUID-style doc and
    a `crossref_`-prefixed doc (no `arxiv_id`, correctly left untouched)
    checked directly, plus a 500-doc spot re-check confirmed **zero**
    remaining `arxiv_id`-bearing docs missing either field. No Postgres, no
    Jetson, no Cursor round-trip needed in the end — this session already
    had live Firestore credentials and the fix required nothing else.
    **Correction to this item's own framing above:** the Knowledge Map
    date-filter gap does not actually affect these UUID docs — they carry
    `published_at`, which `_paper_passes_date_filters` checks *first*,
    before falling back to `published_date`/`year`. That gap is specific to
    docs from `ingest_papers_from_metadata_json.py`, which have none of the
    three.
    **Also noted, not chased further:** a 2026-early planning doc
    (`docs/planning/TEST_SYNC_COMPLETE.md`) references a *different* script
    path, `copernicusai-research-metadata/scripts/sync_to_firestore.py`
    (inside the sibling repo itself), described as "the working sync
    script" — possibly a second, duplicate, or superseding sync path beyond
    `cloud-run-backend/scripts/sync_research_papers.py`. Unverifiable
    without that repo; flagged, not resolved.
    **Separate, more serious problem, found by reading the citation_count
    call sites rather than just grepping the name:** `citation_count` is
    semantically overloaded. `/api/papers/{id}/link-podcast/{podcast_id}`
    unconditionally **overwrites** `citation_count` with
    `len(used_in_podcasts)` — a "how many podcasts used this paper" count,
    not the external bibliometric citation count the acquirers compute.
    Today's fix means a freshly-ingested paper now carries its real
    citation count — until the moment it's linked to any podcast, at which
    point that real value is silently clobbered with a small unrelated
    integer. This is a live landmine independent of the backfill question:
    even fully backfilling `citation_count` corpus-wide would leave it
    unstable for every paper that ever gets used in a podcast.
    **DECIDED AND FIXED same-day (2026-08-05), per Gary's explicit request to
    resolve this before any backfill.** `citation_count` keeps its
    schema-defined meaning — external bibliometric citation count — full
    stop. Evidence was unanimous, not a coin flip: all four acquirers
    (Crossref/PubMed/NASA ADS/bioRxiv), `semantic_scholar_service.py`, and
    `research_pipeline.py`'s NASA ADS sort/scoring all treat it as external;
    an archived relevance-scoring script even used it as a ranking-boost
    signal; `metadata_schema.json`'s own field description says "Number of
    citations (when available)." The `link-podcast` call site was the one
    outlier. Checked before touching it, not assumed safe: zero frontend
    references to `citation_count` anywhere, the endpoint's own response
    body never returned the field, and a live Firestore scan confirmed
    **zero documents have ever actually had `used_in_podcasts` set** — the
    collision was live but had never fired, so there was no corrupted data
    to reconcile. Fixed in `copernicus-web@b14998dc4`:
    `/api/papers/{id}/link-podcast/{podcast_id}` now writes
    `podcast_usage_count` instead of `citation_count`; `used_in_podcasts`
    itself (the source list) is untouched and the count remains trivially
    derivable from it either way. **This unblocks a future `citation_count`
    backfill** — it would otherwise have been unstable for any paper ever
    linked to a podcast; that risk is now closed regardless of when/whether
    the backfill itself happens.
    **DECIDED (2026-08-05), per Gary's explicit request: no corpus-wide
    `citation_count` backfill for now.** Checked both potential consumers for
    actual live use before deciding, the same way `link-podcast` was checked
    before being fixed — **correction to this item's own earlier framing**:
    neither turns out to be live. `/api/papers/query`'s `min_citation_count`
    filter has no caller anywhere in the codebase or frontend (grepped for
    `/api/papers/query` and `min_citation_count` — hits only in the route's
    own definition and API-reference docs, same dead-endpoint shape as
    `link-podcast` before it was found unused). The only other consumer,
    a ranking-boost formula, lives in `archive/one_off_scripts/root/`
    (already dead code, not deployed). So there is currently no live feature
    a backfill would fix — the earlier "two live features depend on this
    data" was wrong; both are unused.
    **Feasibility was the other half of the decision, checked rather than
    assumed:** a full corpus scan by doc-ID prefix gives the actual
    composition — `pubmed_` 25,318, `crossref_` 12,274, UUID-style (a third
    writer, `sync_research_papers.py` or `/api/papers/upload`, entirely
    outside this ingest script's reach) 12,040, `arxiv_` 10,985, `biorxiv_`
    1,531, `medrxiv_` 1,035. Matched against the local acquisition-JSON
    mirror's per-source counts: crossref ~100% covered (12,235/12,274),
    arxiv ~94% (10,279/10,985), pubmed only ~92% (23,324-ish/25,318),
    biorxiv ~52% (803/1,531), medrxiv ~63% (652/1,035) — and the 12,040
    UUID-style docs (19% of the corpus) aren't reachable via this mirror at
    all, needing their own separate investigation of whichever writer
    produced them first. A real backfill would be partial by construction,
    not a clean pass over the whole corpus.
    **Conclusion:** speculative completeness with no live consumer and
    genuinely incomplete source data is exactly the kind of premature
    investment this doc's own standing practice argues against. Revisit
    if/when a real feature (the query filter or a ranking signal) actually
    gets built and needs it — scope the backfill to what that feature
    requires at that time, not to "all 63,197 docs" as a goal in itself. If
    it's ever needed: crossref and arxiv are the cheap, high-coverage wins;
    pubmed/biorxiv/medrxiv would need either accepting partial local
    coverage or a live re-query pass (DOI/PMID/bibcode are already present
    on every doc, so re-querying Crossref/PubMed/NASA-ADS/Semantic Scholar
    per doc is possible without the original JSON, just slow — 63k
    rate-limited API calls is a multi-hour-to-multi-day job); the
    UUID-style docs need their source identified before anything else.
    **Note on schema completeness (Claude Chat, 2026-08-05):**
    `pdf_url` is not among `metadata_schema.json`'s tracked properties,
    which is why the earlier 15-field audit missed the 10,985 `arxiv_`
    -prefixed documents lacking it entirely — that gap was only found
    afterward, while scoping the backfill's actual row count. **The schema
    is therefore not a reliable inventory of fields present in production.**
    Any future audit that diffs live documents against the schema inherits
    this blind spot and should enumerate fields from actual documents as
    well, not from the schema alone.

45. ~~**GAP in item 43 — re-citation of an already-in-corpus paper drops the
    provenance signal.**~~ **RESOLVED (2026-08-05) — no longer speculative
    once item 47's batch hit it 8 times for real.** Raised by Claude Chat:
    this isn't an edge case, it's the steady state — as the corpus grows,
    "a researcher cites something already present" becomes the *ordinary*
    outcome. It stopped being a hypothetical the moment 8 of the 73
    foundational-paper references (item 47) turned out to already be in
    `research_papers`.
    **Decision:** merge, using the exact `citations` schema built the same
    day for item 47's local-mirror collision (a paper cited twice within
    one batch) — the same shape, reused rather than inventing a second one,
    per the reuse note left when that schema was first built. Answers the
    design questions this item originally left open: append to a list (not
    overwrite), a doc can carry multiple citers, and — since this script is
    manual/sequential by design (no cron, no concurrency) — concurrent
    re-citation races were out of scope to solve here.
    **Built and shipped** (`copernicus-web@f9203b0ac`): the Firestore-
    duplicate branch of `researcher_cited_intake.py` now reads the existing
    doc, merges the new citation event via the same `merge_citation()`
    logic already proven at the local-mirror and fresh-ingest layers, and
    writes back *only* the provenance fields via a scoped Firestore
    `update()` — the paper's real metadata (title/authors/abstract/etc)
    is never touched. Local-mirror-only duplicates (not yet in Firestore)
    are left as report-only; extending merge there wasn't needed for the
    case in front of us and would be a different acquisition-pipeline
    concern.
    **Verified on the real 8, not a synthetic case:** dry-ran all 8 first
    (each correctly showed what would merge, wrote nothing), then ran for
    real. **Live-verified directly in Firestore, not just the exit code:**
    the two multiply-cited papers (Gardner's toggle switch, Elowitz's
    oscillator — each cited 3× across the three foundational papers)
    correctly accumulated to 3 citations each; Jacob & Monod and scGPT
    (each cited once) show 1. All four papers' original title/authors/
    `sources` fields confirmed byte-identical to before — the merge
    touched provenance only.
    Item 43's full loop is now proven for every case it needs to handle:
    new paper (the Lents record), same paper cited twice before ingest
    (item 47's local collision), and now a re-citation of a paper already
    live in the corpus.

46. **PROPOSE — A2, the standing acquisition contract (item #37 Part A;
    proposal only, nothing implemented, 2026-08-05).** Both plan docs
    committed to `copernicus-web/huggingface-space/scripts/acquire_papers/`
    — same directory as item #43's plan, since A2 is the same acquisition
    subsystem: `A2-standing-acquisition-contract.md` (the contract itself)
    and `governance-resource-collection-scope.md` (the original proposal,
    kept for the record; its content is placed into
    `governance/RESOURCE_MANIFEST.md`, see below, not left only here).
    **Fresh-fetched both repos and verified all four claims before
    filing, per the handoff's own instructions:**
    1. `docs/research_focus.json` schema — **confirmed exactly**: both
       `glmp` and `atap` have it, same `active_questions[].{q,since,terms}`
       shape, GLMP 2 questions, ATAP 4 (ATAP also has a `categories` field
       the schema note anticipated).
    2. `daily_scout_config.json` — **confirmed exactly**: 10 PubMed + 4
       arXiv queries, every one `discipline: biology`,
       `total_papers_per_run: 1000`, source weights (PubMed 0.5,
       bioRxiv/medRxiv 0.35, arXiv 0.15) match precisely.
    3. **Load-bearing claim, confirmed**: grepped both repos for
       `research_focus` — one hit, `copernicus-web/governance/`
       `check_citations.py`, which only checks that the *filename* exists
       as a citation target (a governance-doc integrity linter), never
       reads the file's content. Nothing in the acquisition pipeline
       consumes it. A2's central premise holds.
    4. **Reference count — corrected, not confirmed.** Independently
       recounted the three foundational papers' actual reference sections
       (not a naive numbered-list regex, which over-counts by picking up
       unrelated numbered lists elsewhere in each document — paper-I: 36
       raw matches vs. 33 real references; paper-III: 28 vs. 21). Real
       counts: paper-I 33, paper-II 19 new (explicitly builds on paper-I's
       33), paper-III 21 new — **73 total, not 83**. DOI count, verified
       two independent ways (a `doi.org/` substring match and a bare
       `10\.\d{4,}/` pattern, identical results both times): paper-I 7/33,
       paper-II 14/19, paper-III 20/21 — **41 with a resolvable DOI, not
       33**. Both the placed governance text and this item use the
       corrected figures.
    **Placement asked, not assumed, per the handoff's explicit
    instruction:** Claude Chat's draft pointed at `CONSTITUTION.md` §7,
    which doesn't match — that section is "Naming & Terms," not Resources,
    and no existing section fits topically (closest is §4, "Records of
    truth"). Asked Gary directly; chose `RESOURCE_MANIFEST.md` under
    "Shared resource collections" instead — a direct fit, since that
    section already lists the metadata database as a shared collection.
    Placed (`copernicus-web@75cb84e56`) with the corrected 73-reference
    figure, and with a header note rather than a flipped date: the
    document's "last verified against reality: 2026-08-04" claim covers
    what it covered then; the new subsection added 2026-08-05 carries no
    verification claim of its own, called out explicitly rather than
    silently riding on the existing date — exactly the false-claim pattern
    this field exists to prevent.
    **A1 found and filed (2026-08-05, later the same day).** It existed —
    drafted alongside A2 and the governance text, but never handed over in
    that batch; downloaded separately once Gary noticed the gap. Filed next
    to A2, same directory:
    `copernicus-web/huggingface-space/scripts/acquire_papers/`
    `A1-glmp-source-backfill-plan.md`.
    **Two corrections applied before filing, both flagged by Claude Chat as
    stale by the time A1 surfaced:**
    1. Its "Open question 1" (does ingestion route through the stub gate?)
       was already answered hours after drafting — the gate is conjunctive
       (rejects only when there's no usable title *and* no identifier),
       defaults to `observe`, and all 216 papers have at least a title plus
       a DOI or PMID. Struck with the answer recorded, not left open.
    2. Its `**Hard dependency:** item #25` header line was stale — #25 was
       reworked hours after A1 was drafted, from "TSV re-harvest" to the
       three-tier re-sourcing split (item 25 above). Replaced with A1's
       actual status: **blocked, deliberately, until ~2026-09-01**, pending
       Prof. Lents' and Me-Me's biology review — not blocked on a resolver
       run anyone could pick up and unblock sooner. The plan's own "Gate:
       item #25" section body was also rewritten to describe the current
       #25 (121 multi-source/54 flagged/~40% false-positive rate even at
       high confidence, 87 single-source, 9 source-less) rather than the
       superseded "~220 of 481 need re-resolving" framing.
    Everything else in the plan holds as originally drafted, per Claude
    Chat's own read: the 216/217 finding, the identifier readiness table,
    the 217−208=9 reconciliation, the two recorded triage failures
    (including the `SOS` tokenizer false-negative — the same
    token-discarding failure mode as item #33's trp-operon β/α case, a
    third instance in the suite), and the behavioural success criterion.
    **Part A of #37 now reads coherently**: A1 blocked until September
    pending Lents/Me-Me, A2 pending `research_focus.json`'s field
    semantics, #43 done and live.
    **Blocker cleared same day (2026-08-05) — Claude Chat's point that
    "A2's blocker is one message from you" turned out right.** Asked Gary
    directly, concretely, with each field's actual current contents shown
    rather than asked abstractly: **`flagged`** = curated priority-seed
    papers, always-include (matches how item 25 already used
    `research_focus.flagged` as a verified retrieval seed). **`mute`** = a
    negative filter, exclude these topics outright. **`frontier`** = drives
    acquisition the same way `active_questions` does — its own `terms`
    field exists for exactly this, not informational-only despite reading
    like framing prose at a glance. **`horizons`** = adjacent-field
    awareness, included at lower priority, matching the governance
    companion doc's "bridges over silos" framing. Recorded in the contract
    itself (`copernicus-web@b572455e4`), not just here.
    **Still not implemented** — confirming semantics isn't building the
    scout — but sequencing step 2 (ATAP first, since it has zero
    acquisition today) is now the next actionable step, not a design
    question waiting on anyone.
    **Two consequences of those answers changed the contract's text, not
    just its glossary — caught same day, before drift set in
    (`copernicus-web@bb7e2bd36`):**
    - **`flagged` moved out of A2's scope, into #43's.** Always-include
      seed papers a researcher curated and justified are researcher-cited
      by another name — same provenance shape, same `citations` merge
      semantics already shipped and verified on 8 real cases (item 45).
      Routing them through the scout would put a resolved ingest problem
      back through an unbuilt one. `mute` stays in A2's scope — a genuine
      scout filtering decision, not a citation.
    - **`horizons` cross-referenced with the governance text, both
      directions.** It's the concrete mechanism for
      `RESOURCE_MANIFEST.md`'s adjacency principle ("admits work from
      adjacent disciplines... when semantic relationship earns it"), not a
      separate idea that happens to resemble it — the principle says why,
      `horizons` is where a project says which fields it means. Neither
      doc pointed at the other before; both do now.
    **Checked, not assumed, before editing:** requirement 1's own top
    sentence already correctly named both `active_questions[].terms` and
    `frontier[].terms` as acquisition targets — the specific staleness
    risked (right in the glossary, stale in the requirement, the pattern
    corrected three times earlier today) didn't actually happen this time.
    **Worth noting for what it says about the drafting, not just the
    result (Claude Chat):** that sentence was written before the
    semantics were confirmed, inferring `frontier` drives acquisition from
    the fact that it has its own `terms` array. The inference happened to
    be right — but checking rather than assuming was the correct move
    regardless of the outcome, and recording "the staleness didn't happen
    this time" is worth more than silence would have been: it's a verified
    negative, distinguishable from a staleness risk nobody actually looked
    at.
    **A design generalization, captured before it's lost to the day
    ending:** moving `flagged` to #43 makes #43 the general path for
    *anything a human deliberately chose* — an email citation, a paper's
    bibliography, a curated seed list, all the same shape. Cleaner boundary
    than originally drawn; A2 gets smaller for it.
    **Two more things written into the contract itself before stopping for
    the day** (`copernicus-web@c54d018f9`), so they don't live only in
    conversation: the ~40% false-positive calibration figure was already in
    the doc but parked under "what this leaves to #36," disconnected from
    requirement 2 (attribute every candidate) where a similarity-based
    mechanism would actually need it — cross-referenced in place. And
    ATAP's four `active_questions` have `terms` but have never been run
    against a live source; whether they return anything usable is itself a
    finding about the declaration, not a null result to route past — noted
    at sequencing step 2, paired with item #48 as the same gap from two
    sides.
    **End of day, 2026-08-05.** Built and proven on three distinct cases:
    a new paper (Lents), the same paper cited twice before ingest, and a
    re-citation of a paper already live in the corpus. #44 backfilled
    23,025 documents. #45's merge semantics shipped and verified live.
    #48 filed. A1 and A2 both filed, corrected, and — for A2 — actually
    unblocked. The governance text written, placed, and now
    cross-referenced with the field that implements it. #25 went from an
    unreproducible "~220 rows" estimate to a measured, tiered, 54-row
    candidate list with its own false-positive rate known. Nothing left
    mid-air that isn't explicitly logged as deliberately parked.

47. **PROPOSE — researcher-cited backfill of the foundational papers'
    73 references via #43, separately actionable from A2 (2026-08-05).**
    The 73 references in paper-I/II/III (corrected count, see item 46)
    qualify as researcher-cited under #43's own terms — cited by a
    participant (Gary, as the papers' author), in a stated context (each
    paper's argument). 41 have a resolvable DOI already in the text and
    would resolve immediately through `researcher_cited_intake.py`'s DOI
    path; the other 32 (mostly pre-DOI-era books, dissertations, and
    non-journal sources — Euclid, Hilbert, Peano, Brouwer's dissertation,
    several Stanford Encyclopedia-linked classics) would exercise the
    free-text path, which per #43's own design is never auto-accepted and
    would queue to the review file instead — a real test of that path at
    volume it has never had (the Lents test case was one record). Seeds
    the shared corpus with exactly the cross-domain material ATAP
    currently lacks, without waiting on A2's semantics questions to
    resolve. **Dry-run complete (2026-08-05), nothing written.** Ran all
    73 through the real `researcher_cited_intake.py` (each reference's own
    DOI when present, free text otherwise), no `--write` at any point.
    **Final result: 32 resolved cleanly, 33 unresolved, 8 already in the
    corpus.**
    **#45's gap is no longer hypothetical.** 8 of 73 (~11%) hit the exact
    gap #45 describes — a real hit rate, not an edge case. Four distinct
    already-in-corpus papers, cited 8 times across the three papers
    (Gardner's toggle switch and Elowitz's oscillator each cited in all
    three; Jacob & Monod once; scGPT once) — each citation's specific
    `cited_context` (why *that* paper, in *that* argument) is reported by
    the script and then discarded, not merged, exactly as #45 describes.
    This one batch alone would be 8 concrete instances of the gap, not a
    theoretical one.
    **Three real bugs found in `researcher_cited_intake.py` /
    `validate_metadata.py` by testing at volume, fixed same-day
    (`copernicus-web@f9889a304`)** — this is the point of running 73
    real references instead of one:
    1. `DOI_RE` truncated any DOI containing a literal `)` — exactly the
       old Elsevier PII-derived DOI format (`10.1016/S0022-2836(61)`
       `80072-7`, Jacob & Monod 1961) that the script already parsed
       correctly *as a PII string* but broke on when given as the DOI
       itself. Fixed with a paren-balance-aware trim.
    2. `resolve_doi()`'s bioRxiv-first path treated more than one API
       response entry as "ambiguous" — but a DOI-scoped bioRxiv query only
       ever returns multiple entries for multiple *revisions* of that same
       DOI, never a different paper. Confirmed against two real preprints
       in this batch (2 and 4 revisions, identical titles throughout). Now
       picks the latest version.
    3. `validate_metadata.py`'s `valid_sources` list was already flagged
       missing `biorxiv`/`medrxiv` when #43 was first built (open question
       5 in the plan doc) — no longer theoretical: fix (2) surfaced two
       real, correctly-resolved bioRxiv preprints that then failed
       validation on exactly this gap. Fixed.
    **One real content error found, in the paper itself, not the
    pipeline:** paper-II reference #3 (Thanos & Maniatis 1995, *Cell*)
    cites DOI `10.1016/0092-8674(95)90417-0`, which does not exist —
    confirmed directly against Crossref, not inferred. Found the real
    paper by title search: `10.1016/0092-8674(95)90136-1`, exact title
    match ("Virus induction of human IFNβ gene expression requires the
    assembly of an enhanceosome"). **Not corrected in the paper** — that's
    Gary's document to edit, flagging rather than touching it.
    **32 clean records written (2026-08-05), local JSON only — Firestore
    ingest not yet run.** Reclassified all 73 fresh (no corpus/state
    changes since the dry run; confirmed identical 32/33/8 split), then
    ran `--write` on just the 32 — not the 8 duplicates, not the 33
    unresolved, matching this item's own scoping exactly.
    **Found a fourth issue, this time in how the batch was run, not in
    the script: only 28 unique files exist on disk from those 32
    writes.** Three papers are cited more than once across the three
    foundational papers — Shen-Orr's network-motifs paper (paper-I#11 +
    paper-III#7), Rice's theorem (paper-I#30 + paper-II#11 +
    paper-III#13), and the ENCODE Project paper (paper-II#17 +
    paper-III#10) — and `researcher_cited_intake.py --write` has no
    protection against two different citations of the same paper landing
    on the same output path: each later write silently overwrote the
    earlier one's `cited_context`/`cited_by`/etc, no warning, no merge.
    **Same failure shape as item 45 (a re-citation's provenance dropped,
    not merged) — just one layer earlier**, at the local-JSON-mirror
    step, before Firestore ingest even runs, so #45's existing dedup
    checks (against `research_papers` and the local `crossref/` mirror)
    never had a chance to catch it: those check different directories
    than where `researcher_cited_*.json` files land, and Firestore
    doesn't have these papers yet either. Concretely, not hypothetically:
    **4 of the 32 citations' specific context (paper-I#11, paper-I#30,
    paper-II#11, paper-II#17) is gone from disk** — only the
    chronologically-last citation of each of the 3 repeated papers
    survives (paper-III#7, paper-III#13, paper-III#10 respectively).
    **Fixed and recovered same-day (2026-08-05), per Gary's request to
    design the multi-citer schema before ingesting anything.**
    Designed and built the schema item 45 itself was already gesturing
    at: a `citations` list of per-event objects
    (`cited_by`/`cited_date`/`cited_context`/`cited_project`), with the
    existing singular fields kept in sync with the latest event for any
    reader that doesn't know about the list yet. A record with no
    `citations` array yet (the legacy shape, i.e. every one of these 28
    files) has its own singular fields recovered as citation #1 the
    first time it's touched again — nothing about the old shape is
    discarded. Appending is idempotent: re-running the identical citation
    doesn't duplicate the list entry. Unit-tested before trusting it on
    real files (legacy-record recovery, append, and re-run idempotency,
    all confirmed) — same discipline as every other fix this session,
    verify before you rely on it. Shipped in
    `copernicus-web@86a8149fe`.
    **Then used it for real**, not just built and left: re-ran the exact
    4 lost citations (paper-I#11, paper-I#30, paper-II#11, paper-II#17)
    through the fixed script with `--write`. All 4 merged cleanly.
    Live-verified by reading all 3 affected files directly: Shen-Orr's
    paper now correctly shows both citations
    (`researcher_cited_crossref_10.1038_ng881.json`), Rice's theorem
    shows all 3 (interesting resolution detail — Crossref canonicalizes
    the JSTOR-prefixed DOI `10.2307/1990888` both papers cite to its own
    `10.1090/S0002-9947-1953-0053041-6`, so both correctly landed on the
    same record despite citing the DOI differently), and ENCODE shows
    both. **All 32 citations are now correctly represented across the 28
    files — zero lost.**
    Reuse note for whenever item 45 itself gets built: this is the same
    `citations` shape, deliberately — an already-Firestore-ingested paper
    getting re-cited should append to this same list via a Firestore
    update, not invent a second schema.
    **Ingested to Firestore (2026-08-05), Gary's go given.** Caught one
    more instance of the exact same allowlist gap before running it,
    not after: `ingest_papers_from_metadata_json.py`'s field allowlist
    knew about the four singular `cited_*` fields but not the new
    `citations` list added the same day — ingesting as-is would have
    dropped the just-recovered multi-citer history straight back down to
    a single citation, undoing the merge fix above. Fixed
    (`copernicus-web@f9e052900`), unit-tested (a record with a
    `citations` list passes through intact; an ordinary record without
    one is unaffected) before running anything real.
    Scoped to exactly these 28 files (an isolated `--root`, same
    precedent as item 43's original ingest) — dry-run first (would-write
    28, 0 gate hits), then for real: **wrote 28, skipped 0, failed 0.**
    Live-verified, not just trusted the exit code: read all 3
    multi-citer docs directly from `research_papers` —
    Shen-Orr shows 2/2 citations, Rice's theorem 3/3, ENCODE 2/2, all
    with correct `cited_context` text. Corpus count 63,198 → 63,226,
    exactly +28. Item 43's full loop (researcher sends a citation → it's
    findable, with who/when/why intact, even when the same paper is
    cited more than once) is now proven end to end, not just for the
    single-citation case.
    **The 8 corpus-duplicates (item 45 proper) — resolved same day, see
    item 45.** Merged onto their existing docs rather than left
    unwritten; not still open.

48. **FINDING — ATAP process files: 218 of 237 have an empty `sources`
    array (2026-08-05).** Surfaced while verifying an earlier claim for
    item 46 (A2), never filed on its own — recorded now rather than left
    living only in conversation. Verified directly, not re-quoted:
    `copernicus-web/huggingface-space/mathematics-processes-database/`
    `processes/**/*.json`, 237 files, `sources` field empty on 218,
    populated on 19. Same shape as item 46's own framing of A2's
    motivation (ATAP has no acquisition at all, not just an untuned
    one) — this is the citation-layer half of that gap: even where ATAP
    *does* have process files, most carry no source citations to backfill
    from, the mathematics-side analogue of GLMP's 216/217 gap A1 exists to
    fix. No plan filed yet — not scoped, not sequenced, not assigned. Given
    A1's own shape (identify what's missing, ingest what's ready, resolve
    the source-less remainder with human judgment), this likely wants an
    "A1 for ATAP," but that's a decision, not something to assume by
    building it.

49. **FINDING, then FIXED (2026-08-06) — `acquire_arxiv_batch.py` discarded
    its own computed discipline.** Confirmed against current `main`: line 181 computes
    `category = determine_discipline(...)` correctly (physics/math/
    computer_science/biology by arXiv category prefix), then lines
    204-205 hardcode `"category": "biology"` and `"discipline": "biology"`
    regardless — the computed value is thrown away. A two-line fix,
    sized before touching it per Claude Chat's explicit request.
    **Measured directly against live Firestore, not estimated:** of 550
    arxiv-sourced `research_papers` documents with `discipline: "biology"`,
    **237 (43%) have a `math.` or `cs.` primary category** — 199 `cs.`,
    38 `math.` **One methodology note**: `primary_category` itself never
    reached Firestore either (a related, smaller allowlist gap, same
    family as item 44's finding but never previously caught since it's an
    arxiv-acquirer-specific field, not in `metadata_schema.json`'s tracked
    properties) — used `categories[0]` as the proxy instead, reliable
    since arXiv lists the primary category first, spot-checked against
    samples before trusting it.
    **Fuller picture than the strict math/cs question asked for, since the
    data was already in hand:** only **240 of 550 (44%) are correctly
    labeled** (genuine `q-bio.*`). The remaining 313 split: 237 math/cs
    (above), 53 more that should be physics (`physics.*`/`cond-mat`/
    `math-ph`), 12 `eess`, 5 `stat`, 3 `nlin`. **This is a #44-scale
    problem, not a two-line-fix-and-move-on** — the fix stops new damage;
    whether/how to backfill the 313 already-mislabeled documents is a
    scale-of-effort decision, explicitly not made here.
    **Both fixes applied, 2026-08-06, on Claude Chat's explicit go-ahead
    after this sizing landed** (`copernicus-web@12da1c1e3`): the two
    hardcoded `"biology"` literals now use the already-computed `category`
    value, and a latent operator-precedence bug in that same line
    (`primary_category or categories[0] if categories else ""`, which
    Python parses as `(primary_category or categories[0]) if categories
    else ""` — silently dropping `primary_category` whenever `categories`
    was empty) was fixed at the same time, since the value it feeds was
    about to start mattering for the first time. `primary_category` is
    now also carried through to Firestore on ingest, closing the
    allowlist gap this item's own methodology note had to work around
    with a proxy. Both changes are additive — new records only, no
    existing document touched; the 313-document backfill decision above
    is unaffected and still open.

50. **ATAP declaration dry-run against live arXiv — feasibility report,
    no writes, no ingest (2026-08-06).** Ran all 25 `active_questions`
    terms (corrected from the handoff's claimed 26 — 7+7+6+5, verified by
    counting, not assumed) and all 18 `frontier` terms against the real
    arXiv API: in-category vs. no-category, and — for `active_questions`,
    which carry a `since` date — windowed vs. unwindowed. Raw responses
    cached (43 terms × up to 4 queries), full structured results
    filed alongside this item for reproducibility without re-querying.
    **Finding 1 — WRONG as first reported, corrected same day (Claude Chat
    catch, twice).** Originally reported as "question 4 is close to
    non-functional as phrased," based on 4 of its 5 terms returning zero
    hits in every mode. **The zero was the instrument, not the
    declaration.** All four queries used a single quoted 4-word phrase
    (`all:"formal methods systems biology"`) — arXiv's exact-phrase match on
    a long compound descriptive phrase essentially never fires, since real
    papers say "formal methods *for* systems biology" or similar, breaking
    the literal 4-gram. A first hand-tested re-check confirmed the
    hypothesis on all four terms — but Claude Chat's second catch was
    broader and more important: **every multi-word term in the whole sweep
    used this same construction, so every count in the filed JSON is a
    floor, not a measurement — not only the ones that happened to land on
    zero.** A plausible-looking undercount doesn't announce itself the way
    a zero does.
    **Response: re-ran the full sweep systematically** (in-category,
    unwindowed only — see scope note below) with three constructions per
    multi-word term — floor (original quoted full phrase), corrected
    (non-overlapping quoted word-pair chunks, ANDed), ceiling (every word
    ANDed, unquoted, no adjacency) — rather than hand-checking a few terms
    again. Filed as `atap-arxiv-feasibility-corrected-2026-08-06.json`; the
    original file now carries a header flagging it as instrument-affected
    and pointing here. Results, floor → corrected → ceiling:
    - Recovered (instrument artifact, real literature exists): "Boolean
      network model" 7→62→106; "model checking biological" 0→18→20;
      "formal verification biology" 0→11→15; "formal methods application"
      (frontier-4) 0→125→480.
    - **Third null in effect, cause not fully established (Claude Chat
      correction, 2026-08-06):** "formal methods systems biology" stays
      0→0 under corrected word-pair chunking. First filed here as a
      diagnosed artifact — "the natural break is elsewhere, not a clean
      2+2 split" — but that's a hypothesis, not a confirmed diagnosis: it
      hasn't been tested against an actual re-chunked query the way the
      other artifacts were confirmed by re-running with a fix that
      recovered real hits. ceiling=38 shows related literature exists
      somewhere in the broader unquoted-word match, but nothing confirms
      it's about *this* term rather than the ceiling's own looseness.
      Treated the same as the two confirmed nulls below for the Task 3
      acquisition run — returns nothing, run and expect nothing — but
      listed separately because "returns nothing, cause not fully
      established" and "confirmed genuine null" are different claims.
    - **Confirmed genuine null, not an artifact:** "qualitative modeling
      gene regulation" — 0 under all three constructions including the
      loosest, no-adjacency-required one. This is now the one term in
      question 4 that may actually need rephrasing.
    - **Confirmed genuine near-null, not an artifact:** "proof role
      vocabulary" (frontier-2) — 0→0→2. Stays a real finding about that
      frontier question, not lost among the corrections.
    - Note on `interdisciplinary formalization` (frontier-4): the earlier
      hand-check found 151 hits with a looser query; the systematic
      in-category re-run shows 0→0→10. Not a contradiction — the 151 was
      unrestricted across all of arXiv, not limited to ATAP's five declared
      categories (math.LO, cs.LO, cs.PL, math.CT, cs.DM); the in-category
      ceiling of 10 is the number that actually bears on ATAP's feasibility.
    **This is the fifth instance today of the day's recurring shape** (trp
    Greek letters, peroxisome names, the `SOS` tokenizer, a regex reporting
    zero DOIs, now a phrase-match query) — a measurement came back empty
    and the instrument was at fault, not the thing being measured. Added to
    `AGENT_ROLES.md` v1.6 as a standing working preference: an empty or
    surprising result is a claim about the instrument until the instrument
    is checked. Do not treat question 4 as needing a rewrite on the
    strength of the original zero-hit report — only "qualitative modeling
    gene regulation" holds up as a real gap.
    **Finding 2 — answers the windowed-vs-unwindowed framing question
    directly, direction solid, magnitudes are floors.** Windowed counts run
    10-60× smaller than unwindowed across nearly every term
    ("diagonalization": 382 in-category all-time vs. **7** since
    2026-07-01; "incompleteness": 629 vs. **12**). **ATAP's first pass
    should be a historical/frontier sweep, not a windowed scout run** —
    there is a large, real, already-published body of work predating the
    declared `since` dates; a windowed-only scout from day one would look
    broken when it's actually just caught up on backlog that was never
    ingested. **Caveat inherited from Finding 1's fix:** the windowed
    figures above were not re-run with corrected query construction — both
    sides of each ratio move together under the same phrase-query defect,
    so the *direction* (windowed ≪ unwindowed) holds, but the exact
    multiples (10-60×) are a floor-over-floor ratio, not a measured one.
    **Finding 3 — zero corpus overlap.** Sampled each term's top-5 hits
    (not exhaustive — a true unique-paper count isn't cheap for terms
    with hundreds/thousands of hits) and checked every sampled ID against
    `research_papers` by `arxiv_id`: **zero matches, across all four
    questions.** ATAP's declared frontier isn't redundant with what's
    already in the corpus.
    **Frontier terms**, checked separately (in-category/no-category only,
    no `since` date to window by): frontier-3 (representation/notation:
    "knowledge representation," "string diagram," "commutative diagram")
    is the one area with substantial hits (up to 305 in-category); the
    other four frontier groups return single digits to zero even
    unfiltered — consistent with genuinely open, thinly-studied questions
    rather than a phrasing problem, unlike question 4's pattern above.
    **Not built:** the declaration-reading runner (Task 3) stays held, per
    the handoff's own sequencing — writing it before this report landed
    would have meant guessing at the query construction it should produce.

51. **ATAP first-pass acquisition runner — built, dry-run reports zero
    corpus overlap, no Firestore write yet (2026-08-06).** Task 3, on
    Gary's explicit decisions relayed via Claude Chat: full unwindowed
    sweep, automated relevance scoring only (no manual review gate),
    review happens *after* ingest rather than as a gate.
    **Dry-count first, per the handoff's own gate** ("if it's 80,000,
    Gary should see it before the write"): 3,463 unique arXiv IDs across
    all 43 terms (in-category, corrected query construction, every
    term's fetch matched its declared total — exact, not another
    floor). ~5.5% of the 62,900-doc corpus — large enough to give ATAP
    real representation, small enough to review, per Claude Chat.
    **Build:** fetched full entries (not just IDs) for the 40 non-null
    terms, reusing item 50's cached responses (same query params,
    almost entirely cache hits — no new arXiv load). Applied ATAP's
    `mute` filter (`research_focus.json`): 3 papers dropped, all on
    "cryptocurrency" (a Proofgold blockchain explorer, a ledger-
    structures paper, a smart-contract verification paper) — the filter
    caught exactly what it was built for. **3,460 unique candidates**
    survive (3,463 − 3 muted).
    **Third null, listed separately from the two confirmed ones (Claude
    Chat correction):** "formal methods systems biology" treated the
    same as the confirmed nulls for this run — skipped, contributes 0 —
    but recorded as "returns nothing, cause not fully established," not
    filed under the same diagnosis as the other artifacts item 50 fixed.
    **Scoring:** relevance score = cosine similarity between a paper's
    title+abstract embedding and its matched question's embedding
    (`text-embedding-3-small`), computed per (paper, question) match —
    a paper matched under multiple questions carries one score per
    match, none of them gating the write. **No single global threshold
    was set, and this is a finding, not just a design choice deferred:**
    per-question score distributions are not comparable to each other —
    frontier-2's entire range (0.13–0.26, 10 papers) sits below
    active-question-2's 10th percentile (0.26), and frontier-3's range
    (0.09–0.45, 552 papers) is centered well below it too. A global
    cutoff tuned to look reasonable against Q2's 1,940 papers (54% of
    the sweep) would silently erase most of the frontier questions'
    already-thin candidate sets — confirming Claude Chat's specific
    concern about Q2 dominating a pooled threshold. If/when review
    prunes, it should prune **per question**, not against one shared
    number. Full distributions (min/p10/median/p90/max) and 10 sampled
    titles at top/mid/bottom per question filed in
    `atap-firstpass-score-report-2026-08-06.json`.
    **Resolved exact numbers, replacing item 50's "~700 with stated
    overlap" frontier estimate:** frontier-1: 36, frontier-2: 10,
    frontier-3: 552, frontier-4: 129, frontier-5: 2 (frontier-5's 2
    papers make its distribution not meaningfully a "distribution").
    Active questions: Q1 733, Q2 1,940, Q3 197, Q4 91. (Sums exceed
    3,460 because some papers match more than one question — e.g.
    "proof structure" spans Q1 and frontier-1 — each contributes to
    both questions' own unique counts by design.)
    **Provenance, per A2 requirement 2:** every candidate tagged with
    `run_id` (`atap-firstpass-20260806`), `acquisition_channel`, and
    `acquisition_matches` (list of `{kind, question, term, score}`) —
    attributed to the specific question, not just to ATAP. Allowlist
    gap for both fields caught and closed in
    `ingest_papers_from_metadata_json.py` *before* the dry-run, not
    after (same recurring bug class as items 43/44/49).
    **Dry-run reported `Skipped: 0` — WRONG, and wrong for a reason worth
    recording on its own.** `--dry-run` stages each doc via `batch.create()`
    but never calls `batch.commit()`, so the `AlreadyExists` check that
    produces a real skip count never runs — dry-run mode is structurally
    blind to pre-existing docs, not evidence of their absence. Caught
    because the real write's skip count (7) didn't match the dry-run's (0)
    and the discrepancy was chased down rather than let stand — this
    script's `--dry-run` cannot be used to verify zero-duplicate-writes
    before a real run; only the write itself (or a direct `get()` check)
    can. Worth carrying forward anywhere else this script's dry-run is
    trusted for that purpose.
    **Rollback proven before it was needed, per Claude Chat's request:**
    confirmed all 3,460 local candidate files carried `run_id` before
    writing anything, wrote a rollback/audit script
    (`rollback_query.py`, filed in `scripts/atap_firstpass_2026-08-06/`)
    querying `research_papers.where("run_id", "==", "atap-firstpass-
    20260806")`, and ran it pre-write (0 matches, as expected) to prove
    the query mechanics before trusting it post-write.
    **Process check, then write:** `Get-CimInstance` showed only this
    session's own `claude.exe` plus the Chrome native-host helper
    (previously diagnosed as benign) — no second live session, safe to
    write. Ingest result: `Wrote: 3453, Skipped: 7, Gate hits: 0,
    Failed: 0`.
    **Finding 3 corrected: not zero overlap, 7 of 3,460 (0.2%).**
    The 7 skips were real, not an artifact — checked each by direct
    `get()`: all 7 already existed in `research_papers` with `created_at`
    dates from 2026-01-19 through 2026-06-24 (pre-dating this run by
    months) and no `run_id`, i.e. acquired earlier by the generic arXiv
    scout. Finding 3's original sampled top-5-per-term check missed
    these (small sample against terms with hundreds of hits); the
    dry-run's blind `Skipped: 0` then independently failed to catch it
    for the structural reason above. Two different failures landing on
    the same wrong number is itself worth noticing.
    **Fixed per A2 requirement 5, not left as a silent skip:** "a hit
    against the existing corpus must still record the new attribution."
    `skip_existing`'s `create()`-based collision handling correctly left
    all 7 existing docs untouched (no title/abstract/sources clobbered —
    requirement 4 held), but a bare skip would have discarded the new
    question/term/score attribution these papers also earned. Additively
    merged `acquisition_matches` + `run_id` onto the 7 existing docs
    (same shape as item 45's `merge_citation_onto_firestore_doc`, same
    file filed as `rollback_query.py`'s sibling `merge_preexisting.py`).
    Re-ran the rollback query after: **3,460 matches, exact** — every
    candidate this run touched, whether freshly written or merged onto
    an existing doc, is now findable and reversible by `run_id`.
    **GLMP spot-check, pre/post pair, per Claude Chat's request:** ran
    three GLMP Node-Explanation-style RAG queries (lac operon/CRP,
    GRN-as-dependency-graph mathematical structure, operon evolutionary
    complexity) before and after the write, saved full citation lists
    both times (`atap-firstpass-glmp-spotcheck-pre/post-2026-08-06.json`).
    **Zero citation-set change on all three** — same papers cited,
    same counts (36/40/39), before and after. Answer text differs
    slightly between runs (LLM sampling variance at the same citation
    set, not a retrieval effect). **Reading this honestly: no evidence
    of dilution, but also no evidence of uptake** — on these three
    queries, none of the 3,460 new papers ranked into the top context
    window. Doesn't clear the dilution question generally, only on the
    three queries actually run; a query that leans harder on the formal/
    mathematical side of GLMP (rather than the biology side, which all
    three of these did) might behave differently and hasn't been tested
    — **it has now.** Ran two more queries specifically bridging GLMP
    and ATAP's material (network-motif formal structure vs. graph
    similarity; category-theoretic/proof-graph framing applied to the
    lac operon's regulatory logic) and checked their citation lists
    directly against `run_id` rather than eyeballing titles. **Still
    zero** — 0 of ~40 citations on either query trace back to this
    run's 3,460 papers, even when the question was written to invite
    exactly that connection. Filed as
    `atap-firstpass-glmp-spotcheck-formal-lean-2026-08-06.json`. Reading
    this straight, same as before: no dilution, but also no uptake, now
    on five queries instead of three, including the two built to give
    it the best chance. Doesn't prove uptake will never happen — an
    embedding-similarity RAG search may simply not be the right lens for
    a connection this abstract — but the "shared corpus helps GLMP see
    category theory" hypothesis has no supporting evidence yet, only
    the absence of harm.
    **Retroactive caveat on `--dry-run`'s `Skipped: 0`, for the record:**
    items 43 and 47 both quote a dry-run "0 skips" result before their
    real writes. Neither conclusion is actually in doubt — item 43's
    "not already in `research_papers`" claim came from a direct live
    Firestore query run separately, and item 47's write was verified by
    corpus-count delta (+28, exact) and direct reads of the multi-citer
    docs — but if either record is read as "the dry-run's 0 skips proved
    non-duplication," that reading is wrong. The dry-run number was
    never the evidence; the separate live check next to it was, in both
    cases. Worth being explicit about which sentence in a past record is
    doing the evidentiary work when the same tool's output text hasn't
    changed but what it means has.
    **5.5% of the corpus, one project, one domain, in one run — flagged
    by Claude Chat for later:** if GLMP retrieval quality shifts going
    forward, this run is the first place to look, and `run_id` is what
    makes that testable rather than a guess.
    A2 gained a new requirement from this run's per-question-threshold
    finding: "thresholds are per-question or they are not thresholds"
    (`copernicus-web`, A2 §2).

    **Correction, 2026-08-07: the zero-uptake result above was measuring
    the pipeline, not the premise (Claude Chat's diagnosis, confirmed).**
    Checked the Firestore schema directly: the 7 merged pre-existing
    docs carry `embedding`/`embedding_model`; none of the 3,453 freshly
    written docs did. GLMP's retrieval is Firestore native vector search
    (`find_nearest` on the `embedding` field) — a doc without that field
    is structurally unrankable, not merely low-relevance. All five
    "zero uptake" spot-checks were answered honestly against an index
    that never contained the thing being tested.
    **Fixed via the proper tool, not improvised:** `backfill_research_paper_embeddings.py`'s
    own `--pin`/`--dry-run`/`--pilot`/`--run` workflow. `--pin` census
    matched exactly 3,453 — independent confirmation the 7-doc merge
    worked (the merged docs correctly did *not* need re-embedding), a
    case of two measurements agreeing where they could have disagreed,
    same standard as the rollback-count check above. `--pilot 5` wrote
    5 real embeddings; proved the write path with a live `find_nearest`
    query on one pilot doc's own title before trusting the rest — it
    ranked first, `run_id` intact. Full `--run` completed clean:
    **3,453 embedded, 0 skipped, 0 failed.**
    **Corpus-wide census, per Claude Chat's request — the invisible-
    papers question generalizes past this run, and the answer is
    reassuring: 0 of 66,697 documents corpus-wide now lack an
    embedding.** Not a longstanding #44-shaped gap. Checked items 43
    and 47's specific researcher-cited papers directly (33 docs via
    `acquisition_channel == "researcher_citation"`, including Lents'
    cAMP-CRP paper): **all 33 already embedded**, most since shortly
    after their 2026-08-05 ingest — evidence of a working periodic
    auto-embed process (`--auto` cron, per the script's own docstring)
    that had two days to reach the item 43/47 batch but not yet the
    hours-old ATAP batch when the original spot-checks ran. #43/#47's
    "in the corpus, retrievable, and its record shows who cited it"
    criterion holds; the gap was time-lag on new records, not a
    standing hole.
    **Re-ran all five spot-check queries against the now-complete
    index — real, graded uptake, matching Claude Chat's stated
    prediction almost exactly:** the two pure-biology queries (lac
    operon/CRP; evolutionary complexity) still show **0** ATAP-run
    citations. The GRN-as-dependency-graph query (a partial bridge)
    shows **1**. The two queries built specifically to bridge GLMP and
    ATAP show real pickup: network-motif formal structure **2** ATAP
    papers, and the category-theory/proof-graph query **5** — with an
    ATAP paper (**"Graphical Regular Logic"**) ranking **first**.
    Filed as `atap-firstpass-glmp-spotcheck-post-embed-2026-08-07.json`.
    **The shared-corpus hypothesis now has actual supporting evidence,
    not just absence of harm** — graded exactly along the semantic
    distance predicted in advance, not read post-hoc into a pooled
    result. Raw build/score/spot-check reports, the embedding backfill
    log, and the rollback/merge scripts filed alongside this item for
    reproducibility.

52. **GLMP retroactive attribution — report only, no writes (2026-08-08).**
    Design note filed: `project-oriented-research-design-note.md` —
    thinking, not a build spec, prompted by Gary's 2026-08-06 framing
    ("I want to drive it in a very specific direction to ask specific
    questions"). Core claim: for GLMP the job is attribution before
    acquisition — GLMP's ~63,000 papers carry nothing connecting them to
    GLMP's own declared questions, while ATAP's 3,453 (item 51) carry
    full `acquisition_matches` provenance. The newest, smallest project
    is the best-instrumented one.
    **Two claims fresh-fetch-verified before acting on them, both
    correct:** `research_focus.json` — 2 active questions (9 terms
    each), 2 frontier entries (4 terms each), 5 flagged PMIDs, 2 mute
    terms, exactly as claimed. `KNOWLEDGE_MAP_FILTERING_NOTE.md` is
    stale — the endpoint (`endpoints/knowledge_map/routes.py`) declares
    all six filter params and `build_graph()`
    (`services/knowledge_map_service.py:758`) genuinely uses them
    (in-memory filtering, vector-seeded path on `keyword`), not just
    accepts and drops them. Dated rather than deleted
    (`copernicus-web`, same convention as governance docs) — the real
    remaining gap is narrower than the note describes: filtering exists
    on library dimensions, not on "which declared question does this
    serve."
    **Task A — scored the existing corpus against GLMP's 2 active
    questions + 2 frontier entries, reusing item 51's now-universal
    embeddings (no re-embedding, no new papers, `since` ignored per the
    handoff).** 66,738 papers scanned, all embedded (matches the
    2026-08-06 census), 0 muted (the 2 mute terms are narrow enough
    that nothing in the corpus matches verbatim — expected, not a gate
    failure).
    **Finding: the "CRP" ambiguity contaminates active-question-1's top
    end.** Its highest-scoring hits are "Evolution of C-Reactive
    Protein" (0.5588) and "Phylogenetic aspects of C-reactive protein"
    (0.5087) — the wrong CRP entirely. GLMP's "CRP" is the cAMP
    receptor protein; the biomedical literature's overwhelmingly more
    common "CRP" is an inflammation biomarker, and the embedding model
    doesn't fully disambiguate even with "binding-site sets" and
    "position weight matrices" in the same question text. Active-
    question-2 (no bare "CRP", built around "E. coli," "activator,"
    "PWM") shows no equivalent contamination — its top-10 are
    plausible on-target hits (toggle switches, network motifs in *E.
    coli*, flagella regulators, promoter engineering). This is a
    declaration-wording problem, not a scoring-method problem, and it's
    specific to one of the four dimensions, not general — exactly why
    per-question review beats a pooled score.
    Frontier-1's top hit is the actual paper Lents cited
    (`crossref_10.1016_j.bpj.2022.01.016`, item 43's original test
    case) — genuine signal at the top, with some drift a few ranks down
    (CRISPR/Cas13a diagnostics, quantum decoders — likely "CRP"/
    "decoder"-adjacent term collisions of the same shape). Frontier-2's
    top-10 are diffuse but plausible (gene-regulation modeling papers).
    Mid and bottom samples across all four dimensions are unambiguous
    noise (obituaries, award announcements, unrelated physics/astronomy)
    — the floor behaves correctly.
    **Unclaimed remainder:** of 66,738 papers, only **45 score above
    0.5** on any of the 4 dimensions, **1,189 above 0.4**, **15,856
    above 0.3**, **57,577 above 0.2** (median max-score: 0.257). No
    global threshold is set — per-question-thresholds-or-none, per the
    ATAP-run finding this design note explicitly carries forward — these
    are reference points for Gary/Claude Chat to judge, not a verdict.
    Reading it plainly: GLMP's declaration claims a small, sharp sliver
    of the corpus; the great majority of the ~63,000 generic biology
    papers serve neither GLMP's stated questions nor, per item 51, most
    of ATAP's. Confirms the design note's own prediction (a narrow
    declaration of the *current investigation*, not of GLMP's subject
    matter, produces a small claimed set) rather than indicating
    something broken.
    Full distributions, all four dimensions' top/mid/bottom-10 samples
    filed as `glmp-retroactive-attribution-report-2026-08-08.json`.
    **Task B — GLMP's 5 flagged PMIDs, dry-run only.** All 5 already
    exist in the corpus (all embedded); per the 2026-08-05 A2 decision,
    flagged papers route through #43's citation-shaped path, not
    scoring. Dry-run shows what a `citations`-list merge would add for
    each — `cited_by: "Gary Welz"`, `cited_date: "2026-07-26"` (the
    declaration's own `updated` date), `cited_context`: the flagged
    `note` text, `cited_project: "glmp"`. `pubmed_13718526` (Jacob &
    Monod 1961) already carries one citation from item 47's
    foundational-papers batch — this would be a second, distinct
    event, exactly what the multi-citer schema exists for. Filed as
    `glmp-flagged-papers-citation-merge-dryrun-2026-08-08.json`.
    **Not done, per the handoff's explicit scope:** no UI work, no
    question dimension added to the graph endpoint, no attribution
    written, no threshold set. All of it holds for Gary's review of the
    distributions above.

    **Follow-up, same day (Claude Chat's read of this item):**
    **(a) A distinct failure-mode direction, worth naming explicitly.**
    Every prior instrument-catch this week was normalization discarding
    a discriminating token (trp's Greek letters, peroxisome names, the
    `SOS` tokenizer, the quoted 4-gram). The CRP finding is the
    reverse — an embedding *retaining* a token whose dominant corpus
    meaning is wrong. The fix is different in kind: not a code bug, a
    declaration-wording problem.
    **(b) Tried the fix, measured it, it did not work — reporting that
    plainly rather than assuming the obvious fix would land.** Reworded
    active-question-1's `q` to "cAMP receptor protein (CRP) /
    catabolite activator protein (CAP)" in place of bare "CRP"
    (`research_focus.json`, `updated` bumped to 2026-08-08) and
    re-scored the full corpus against the new text alone. **The
    contamination did not clear.** "Evolution of C-Reactive Protein"
    dropped only from 0.5588 to 0.5168 and stayed in the top 2; the new
    #1 (0.5408) is an unrelated CXCR4/ACKR3 signaling paper, and most of
    the new top-15 is generic receptor/proteomics material — spelling
    out "receptor protein" and "activator protein" pulled in a second,
    broader kind of noise (any paper about protein receptors generally)
    on top of the first. One genuine hit did surface at rank 12 ("The
    dual role of cAMP receptor protein (CRP) in regulating type 3
    fimbriae expression") that plausibly wasn't reachable before.
    **Open, not solved:** short-question-embedding similarity appears to
    key on generic high-frequency biomedical vocabulary ("protein,"
    "receptor," "binding") as much as on the specific named entity that
    actually discriminates relevance. Reworded question text is kept
    (marginal improvement, one genuine hit surfaced) but active-
    question-1's scores should not be trusted at the top without a
    human read until this is actually fixed — a real fix likely needs
    either a longer/more specific anchor text weighted toward *E. coli*/
    bacterial vocabulary, or a scoring method that isn't pure embedding
    similarity over one question string. Filed as `q1_rescore.json`.
    **(c) Frontier-1's Lents hit is an independent validation, worth
    stating as such.** A researcher-cited paper (item 43's original test
    case) surfaced at the top of the one frontier question it was cited
    for, with nothing done to promote it — the method works when the
    terms aren't ambiguous, which is the useful contrast to (b).
    **(d) The design note's own recommendation was wrong, and the note
    should not be read as still arguing the opposite:** 45 papers above
    0.5 out of 66,738 is a direct answer to the note's central open
    question — GLMP's coverage gap is a *missing-papers* problem, not
    an attribution problem the retroactive pass could substitute for.
    Targeted GLMP acquisition (A2) is warranted, informed by this
    attribution pass's numbers rather than guessed at, reversing the
    note's "attribution before acquisition might be enough" framing.
    Attribution was still the right first step — cheap, no new data,
    and it's what makes this correction possible with numbers instead
    of a guess — but it is not a substitute for A2.
    **(e) Task B executed for real, on explicit go-ahead, live-
    verified.** All 5 flagged-paper citation merges written — additive,
    nothing else on any doc touched. Jacob & Monod's doc now carries 2
    distinct citation events (item 47's foundational-papers reference,
    2026-06-14, and this flagging, 2026-07-26) — read directly from
    Firestore after the write, not trusted from the write call's return
    value. Minor, non-blocking note found in the same read: the two
    events use different casing for `cited_project` (`"GLMP"` vs.
    `"glmp"`) — pre-existing inconsistency from before this session,
    left as-is rather than silently normalized without being asked.

    **Second follow-up, same day — tested two candidate fixes before
    concluding the dimension needs indefinite human review, per Claude
    Chat's push not to stop at "open, not solved."**
    **(f) Mute filtering (`c-reactive protein`, `inflammation marker`)
    against the original bare-CRP text: partial, diagnostic result.**
    The C-reactive protein cluster is gone from the top 15 — muting
    worked for the specific cluster it targeted. But the new top 15 is
    still off-target: generic protein-benchmark and biomarker papers
    (`ProtDBench`, antibody validation, proteomics biomarker panels),
    nothing about *E. coli*, CRP, or binding sites specifically. This
    confirms the diagnosis rather than fixing the dimension: the
    question text keys on generic "protein/binding/biomarker" register,
    and muting one wrong cluster only exposes the next one — it treats
    a symptom, not the cause.
    **(g) Paper-to-paper anchoring: works, decisively.** Scored the
    corpus against a single seed paper's own embedding —
    `pubmed_35648826`, the flagged note's own "direct Crp literature
    seed" — instead of against question text. **Every one of the top 15
    hits is genuinely on-topic:** *E. coli* stress-response systems
    (PhoP/PhoQ, envelope-stress Rcs/Cpx signaling), bacterial death/
    lysis pathways, acid-resistance and oxidative-stress systems — zero
    C-reactive-protein contamination, zero generic-proteomics noise.
    Confirms Claude Chat's hypothesis directly: Jacob & Monod's abstract
    (and this seed's) carries no C-reactive-protein register to latch
    onto, so the ambiguity is sidestepped structurally rather than
    filtered after the fact.
    **Caveat, so this isn't oversold as fully solved:** the top hits
    lean toward the seed paper's own dominant framing (this one is
    titled around a "stress-mediated bacterial death pathway," so its
    neighbors skew toward stress/death-pathway biology specifically,
    not narrowly "CRP binding-site/PWM evidence") — a single seed
    inherits that seed's thematic center, not the declared question's
    exact scope. The likely refinement is multiple seeds per question
    (the flagged papers plus Lents' cited paper) scored and combined,
    not a single anchor. Not tested here; flagged for whoever builds
    the real attribution pass.
    **Implication for the eventual write:** for active-question-1
    specifically (and plausibly frontier-1, same "CRP" term), paper-
    anchor scoring using the flagged seeds should replace or supplement
    question-text scoring. Active-question-2 and frontier-2 showed no
    equivalent contamination in the original pass and don't need this.
    Filed as `glmp-q1-two-fixes-test-2026-08-08.json`.
    **(h) `cited_project` casing normalized corpus-wide, root cause
    fixed.** Surveyed before touching anything: top-level field was 33
    `"GLMP"` vs. 4 `"glmp"` (ATAP's own field was 1000/1000 `"atap"` —
    ATAP's invocations happened to stay consistent, GLMP's didn't).
    Traced to the actual cause: `researcher_cited_intake.py` stores
    whatever casing an operator typed on the CLI verbatim, no
    normalization (`copernicus-web`) — fixed to lowercase at write time
    so this can't drift again. Backfilled existing data: 33 top-level
    docs plus 15 citation events inside `citations[]` arrays across 7
    docs, all normalized to `"glmp"`. Live-verified after: 0 remaining
    uppercase, Jacob & Monod's two citation events both read back
    consistent.

    **Third follow-up, same day — multi-seed combination test,
    predicted before measuring.** A2 amended: `flagged` gains a second
    role as scoring anchors (paper-to-paper, not text-to-paper), and
    `mute`'s limit is now recorded (excludes a known topic, doesn't fix
    a query matching on the wrong dimension) — both in
    `copernicus-web`'s A2 doc, §1.
    **Prediction, stated before running:** mean-of-seeds cleanest/most
    representative; union broader and noisier (each seed's own
    idiosyncratic neighbors leaking in); intersection degenerate (six
    thematically diverse seeds unlikely to share a tight neighborhood,
    so min-across-seeds mostly measures the worst-matching seed).
    **Result: partially right, and the more useful finding is a
    different one.** Combined all 6 available seeds (the 5 flagged
    papers + Lents' citation). Intersection *was* markedly weaker as
    predicted — scores 0.42–0.45 versus 0.65–0.77 for mean/union — but
    still surfaced plausible gene-regulatory-circuit material, not
    garbage. Union was **not** noticeably noisier than mean — the two
    overlap heavily in their top ranks (several identical papers in
    both top-15s), because the 6 seeds themselves aren't embedding-wise
    far apart.
    **The finding that actually matters: none of the three combination
    methods stayed on active-question-1's specific target.** All three
    converge on a broader "synthetic gene-circuit engineering" theme —
    coherent, real research, clearly GLMP-adjacent, but not narrowly
    "CRP binding-site evidence / PWM." The single-seed test two rounds
    earlier (`pubmed_35648826` alone, the one note explicitly marked
    "direct Crp literature seed") stayed tighter to the actual question
    than any multi-seed combination did. Reason, once looked for: only
    1 of the 6 seeds is actually about CRP/PWM specifically — the other
    5 are flagged for GLMP's research programme generally (pattern
    formation, quorum sensing, attenuation, Jacob & Monod's founding
    paper), not for *this* question. Averaging or unioning across a
    seed set that's mostly off-topic *for this question* dilutes the
    one seed that was on-topic, rather than sharpening it.
    **Correction to the amendment above, recorded rather than left
    implicit:** seed selection for anchoring should be **per-question**,
    using only seeds actually relevant to that question — which may be
    a single paper, and that's a feature of a well-scoped question, not
    a shortfall to fix by adding more seeds. `flagged` papers are
    project-level judgments, not pre-tagged to a specific
    `active_questions`/`frontier` entry; using the whole list
    indiscriminately as one combined anchor set is the mistake this
    test surfaced, not a property of mean/union/intersection as
    combination methods. Filed as
    `glmp-q1-multiseed-test-2026-08-08.json`.

    **Fourth follow-up, same day — schema gap closed
    (`research_focus.json`, both projects share the format).** Neither
    `flagged` nor `active_questions`/`frontier` had a field for *which
    question a seed anchors* — the exact thing the multi-seed test
    showed was missing. Two candidate fixes; Claude Chat asked for the
    call before either was implemented. **Chose a `seeds` list on each
    `active_questions`/`frontier` entry over a `questions` back-
    reference on `flagged`.** The back-reference option needs something
    stable to point at, and `active_questions` entries have no ID, only
    free-text `q` — a reference would have to match that text verbatim
    and would have silently broken this very session, when
    active-question-1's text was reworded for the CRP fix. `seeds`
    living inside the question object needs no cross-reference and
    matches how the file is already consumed — one object per question,
    carrying its text, terms, and now its anchors together.
    Added `active_questions[0].seeds` (`pubmed_35648826`, `crossref_
    10.1016_j.bpj.2022.01.016`) and `frontier[0].seeds` (the same Lents
    citation). **Populated only with the two papers this session's own
    testing actually justified** — not bulk-copied from the rest of
    `flagged`, which is precisely the mistake the multi-seed test
    surfaced. A paper can be a project-level `flagged` entry, a
    question-level `seeds` entry, both, or `seeds`-only (Lents'
    citation isn't in `flagged` at all) — the two fields are
    independent.
    **Named, not silently left implicit: this doesn't yet make the
    combination-method question testable.** Active-question-1 has 2
    seeds now, still short of enough for mean/union/intersection to
    meaningfully diverge. Not a blocker — the growth path already
    exists via #43: every paper a researcher cites while working a
    specific question is a candidate seed, with `cited_context` already
    capturing why. Wiring #43 to record *which question* a citation
    was for, so it can feed a question's `seeds` automatically, is real
    future work — named here, not built, and not guessed at. Full
    reasoning filed in `copernicus-web`'s A2 doc, §1.

    **Fifth follow-up, same day — #43 wired, on Claude Chat's three
    corrections to my own proposal.** I'd suggested auto-appending a
    cited paper to `seeds`; Claude Chat's read was sharper: a citation
    event and a seed are different claims, and conflating them would
    rebuild the exact dilution the multi-seed test just caught. Built
    to her spec, not mine.
    **(1) Stable question IDs, added to both projects' declarations
    before any citation record could point at prose.** `glmp-q1`,
    `glmp-q2`, `glmp-f1`, `glmp-f2`; `atap-q1`–`atap-q4`,
    `atap-f1`–`atap-f5`. Done first, specifically because the seeds-
    inside-question design only solved the reference problem for the
    declaration file — a Firestore citation record can't nest inside
    `research_focus.json` and needs something stable to point at.
    **(2) `researcher_cited_intake.py` gained `--cited-for-question`**
    (`copernicus-web`) — optional, defaults to empty, filtered out by
    the script's existing truthy-only field logic when unset, so an
    unspecified association writes nothing rather than a guess.
    Records the association only; **does not** write to `seeds` —
    that stays the separate, deliberate step Claude Chat specified.
    Added to `CITATION_EVENT_FIELDS` (the tuple both the `citations[]`
    entries and the top-level-field sync read from) *before* any real
    caller exists, closing the allowlist-gap shape pre-emptively for
    once rather than catching it after a write. Mirrored into
    `ingest_papers_from_metadata_json.py`'s allowlist for the same
    reason.
    **(3) Retroactive backfill — read all 33, mapped 1.** Pulled every
    researcher-cited record's actual `cited_context` text rather than
    guessing from titles. Exactly one is an obvious, current-question
    match: Lents' citation, `crossref_10.1016_j.bpj.2022.01.016`
    (`cited_context`: "while looking into the cAMP-CRP issue") →
    `glmp-q1`. The other 32 — item 47's foundational-papers batch — are
    GLMP paper-I/II/III reference-list citations (bistability theory,
    bibliographic classics, perturbation-prediction methods, Rice's
    theorem, etc.): real citations, correctly provenanced, but
    recording what was already in the papers' argument, not what
    Gary was actively working against `research_focus.json`'s
    currently-declared questions. One candidate looked temptingly
    close — Stormo's "DNA binding sites: representation and discovery,"
    cited in GLMP paper-II as "the JASPAR/motif database approach,"
    shares vocabulary with `glmp-q2`'s terms — but it's a backward-
    looking methodology reference from when the paper was written, not
    a citation made while working the question, so it's left null
    rather than inferred from keyword overlap. Left null is the
    honest answer for 32 of 33, per Claude Chat's own standard: a
    wrong guess reads as signal and is worse than a gap.

53. **Expanded GLMP declaration proposal — dry-count run, overshoots
    the target before the outliers are even counted (2026-08-08).**
    Gary's framing: GLMP should have field-spanning coverage on ATAP's
    scale (~3,000+ relevant papers), not the ~45-paper sliver item 52
    found. Claude Chat's diagnosis, checked and correct: the two
    numbers aren't comparable — ATAP's 3,453 came from *acquisition*
    (fetched and written in against its declaration), GLMP's 45 came
    from *attribution* (scoring what's already in the corpus against a
    2-question declaration covering one narrow investigation, not a
    field). Proposed fix: expand GLMP's declaration to span the field
    the charts actually cover, then run its own acquisition sweep —
    same path as ATAP, not a threshold change.
    **Proposal verified against live chart data before running
    anything.** `glmp-research-focus-expanded-PROPOSAL.json` (filed)
    expands from 2 to 10 active questions, derived from
    `glmp-v2/metadata.json`'s real category/organism counts, not
    invented: every cited number checked exactly — 217 total charts,
    E. coli 68, *Synthetic Biology* category 39 (previously
    unrepresented in the declaration), Stress Response 20, Signal
    Transduction 11, and the three metabolic categories (Metabolic
    Pathway 13 + Metabolic Regulation 7 + Metabolic Signaling 4)
    summing to exactly 24 as claimed.
    **Dry-counted before anything else, same discipline as ATAP's item
    50/51 — and needed a different instrument, not the same one.**
    GLMP's corpus is majority-PubMed, not arXiv (`daily_scout_config.json`
    weights: PubMed 0.5, bioRxiv/medRxiv 0.35, arXiv 0.15) — reused
    ATAP's arXiv-specific query construction here would have measured
    the wrong 15% of the field. Queried NCBI E-utilities directly
    (`esearch`) instead, existing `acquire_pubmed_batch.py`/
    `daily_scout_config.json` convention confirmed first: unquoted
    multi-word phrases, no `[tiab]` restriction — PubMed's automatic
    term mapping doesn't share arXiv's quoted-phrase pitfall, checked
    with a 4-term pilot before trusting the full 71-term sweep across
    the 10 questions + 2 frontier entries.
    **Pass 1 (raw counts, all 71 terms): confirms Claude Chat's own
    named risk, decisively.** 16 term-rows exceed 15,000 raw hits,
    three of them catastrophic — `metabolic regulation transcription`
    612,358; `competence regulation` 558,108; `transcription
    activation` 242,672 (twice, in `glmp-q2` and `glmp-f1`). **`Class
    II` (139,975) is the same failure shape as the CRP finding, more
    severe:** MHC Class II, drug classes, dental restorations, FDA
    device classes — "Class II" in the lac-operon-activator sense
    `glmp-f1` intends is a minor sense of a heavily overloaded string.
    `competence regulation` likely the same (clinical/educational
    "competency," not cellular DNA-uptake competence). One genuine
    zero: `operon re-anchoring` (`glmp-f2`) — GLMP's own internal
    decoder terminology, not literature vocabulary; a real null, not
    an instrument artifact, and not worth chasing.
    **Pass 2 (deduplicated union, non-outlier terms only, capped at
    300 PMIDs/term relevance-sorted): 13,153 unique papers — already
    roughly 3× Claude Chat's stated 3,000–5,000 target, before a single
    one of the 16 excluded outlier terms is added back in.** The cap
    itself means 13,153 is a floor, not a ceiling — most terms hit the
    300-per-term cap, so the true clean-term union is larger still.
    Per-question unique counts ranged 182 (`glmp-f2`) to 1,831
    (`glmp-q2`), all filed in
    `glmp-expanded-dry-count-pass2-2026-08-08.json`.
    **Reading it straight: this declaration, as worded, overshoots.**
    Not a reason to abandon the field-spanning approach — Gary's
    reasoning for wanting ATAP-scale coverage stands, and the category
    counts underneath the 10 questions are real — but several terms
    need tightening (bacterial/*E. coli*-scoping qualifiers, dropping
    or replacing the ambiguous ones) before this is sized right, per
    Claude Chat's own stated fix: "the fix is tightening terms, not
    lowering a threshold, since thresholds must be per-question and
    none is set." **Not yet done:** no declaration committed, no
    seeds added, no acquisition sweep run. Raw pass1/pass2 data and
    the proposal itself filed for reproducibility; next step is
    revising the ~16 flagged terms before re-dry-counting, not
    proceeding to acquisition on the current wording.

    **Follow-up, same day — tightened per Claude Chat's three
    suggestions, then a bigger surprise than the tightening itself.**
    `Class II` removed from `glmp-f1` entirely (not reworded) — per
    Claude Chat's diagnosis, its intended sense exists only inside
    GLMP's own typology, so no rewording rescues it; `glmp-f1` already
    has a seed (Lents' citation) and is now scored via that anchor for
    this concept instead. `signal transduction transcription bacteria`
    dropped from `glmp-q7` as redundant with its remaining four terms.
    `operon re-anchoring`'s zero was kept, not chased — the third
    genuine null this week, and per Claude Chat the most informative:
    it means `glmp-f2` is asking a question in language the field
    doesn't use, independent of any acquisition question.
    **The other 14 outlier terms were bacterial/*E. coli*-scoped, each
    tested live before being locked in** (`glmp-tightening-pilot-2026-08-08`,
    folded into the tightened declaration file) — e.g.
    `metabolic regulation transcription` (612,358) →
    `metabolic operon regulation Escherichia coli` (6,957);
    `competence regulation` (558,108) →
    `competence regulation Bacillus subtilis` (1,391, since natural
    competence is overwhelmingly studied in that organism specifically).
    **Watched for the opposite failure, per Claude Chat's explicit
    caution:** every reworded term's new count compared against its
    sibling terms in the same question before accepting it — the
    lowest, `cAMP receptor protein binding site prediction` at 263, is
    in the same range as existing siblings (`DNase footprinting` 4,377,
    `position weight matrix` 1,516) and `RegulonDB` was already 96
    pre-tightening, so 263 reads as a real, narrow phrase, not an
    over-tightened artifact. None of the 14 reworded terms landed
    anywhere near the near-zero range this week's genuine artifacts
    have occupied.
    **Re-ran uncapped, per Claude Chat's explicit instruction that the
    300/term cap made the first number a floor — and the result
    reframes the question rather than answering it.** Full enumeration
    hit a real PubMed API limit along the way: `esearch` refuses
    `retstart` above 9,998, so `ChIP-seq` (14,028 hits) and
    `two-component system` (11,257) could only be fetched to 9,999 each
    — a genuine instrument ceiling, not a bug, disclosed rather than
    silently capped. **Grand union across all 66 tightened terms:
    121,327 unique papers** — not smaller than the capped estimate,
    *ten times larger* than the previous 13,153, and roughly 30–40×
    Claude Chat's own stated 3,000–5,000 target. Per-question range:
    2,233 (`glmp-f2`) to 29,011 (`glmp-q1`).
    **Why tightening succeeded per-term and still produced a bigger
    union, worth stating plainly rather than treated as a tightening
    failure:** every individual term is now well-behaved (no more
    100K+ single-term catastrophes) — the size comes from the
    declaration's breadth, not from bad wording. Ten genuinely
    different biological subfields (CRP/PWM evidence, network motifs,
    bistability, synthetic circuits, stress regulons, two-component
    signaling, metabolic regulation, developmental commitment, network
    inference methods) share very little vocabulary with each other, so
    their term sets barely overlap and the union sums close to the
    per-question totals rather than collapsing the way redundant terms
    within one narrow topic would. **This is the structural difference
    from ATAP that Claude Chat named at the outset, showing up as a
    number rather than a description:** ATAP's 3,453 came from a
    windowed sweep of a genuinely small corner of arXiv (`math.LO`,
    `math.CT`, four related categories); GLMP's declaration, once it
    actually spans "the field" the way Gary asked for, is spanning a
    literature that is simply much larger. 3,000–5,000 was reasoned by
    analogy to ATAP's raw number, not derived from GLMP's field's own
    size — this dry-count is the first real measurement of that size,
    and it says the analogy doesn't transfer.
    **Not a tightening problem to keep chasing — a scope decision for
    Gary, named rather than resolved unilaterally.** Two honest paths,
    not decided here: (a) accept that comprehensive field coverage for
    GLMP is genuinely a 100K+-paper undertaking and treat that as the
    real number — matching the governance principle already on record
    ("bounded by relevance, comprehensive within the field, size a
    consequence rather than a target") — which changes what
    "acquisition" even means at this scale (relevance-ranked triage
    into the corpus, not "fetch everything"); or (b) narrow the
    declaration's breadth itself (fewer of the 10 questions, or a
    tighter cut within each) to trade field-spanning-ness for a
    tractable sweep size closer to the original target. Both are
    legitimate; picking between them is not a wording fix. Full
    per-term and per-question numbers filed in
    `glmp-expanded-dry-count-tightened-2026-08-08.json`. Nothing
    written, no declaration committed, no sweep run.

    **Follow-up, same day — Claude Chat rejected the size question
    outright and redirected to a per-question relevance cutoff, tested
    on one question end to end.** Her argument: top-k retrieval doesn't
    degrade with corpus size the way a library does, embedding cost at
    121K scale is trivial (~$1), and the real cost — an unviewable
    knowledge graph — is fixed by per-question scoping, not by
    shrinking the corpus. The actual risk is that 121,327 is a
    *union* (matches any term), not a relevance ranking; nobody had
    scored those papers against the questions yet. Her instruction:
    acquire per question, rank by relevance, cut where each question's
    own score distribution falls off — a measurement, not a guess —
    starting with one question (`glmp-q5`, synthetic circuits, 39
    charts, previously unrepresented) before committing the other nine.
    **Ran `glmp-q5` end to end.** 7,561 unique PMIDs (already known,
    uncapped, from the tightened dry-count). Fetched full metadata via
    NCBI `efetch` for 7,557 (4 failed to parse). Deduped against the
    corpus: only 250 already present, 7,307 genuinely new — consistent
    with the design note's "previously unrepresented" read on this
    category. Embedded all 7,557 (reusing existing embeddings for the
    250 already-corpus papers) and scored every one against `glmp-q5`'s
    question text.
    **Found the falloff by reading titles, not by reading the curve.**
    The decile breakdown was smooth, no visible cliff (0.73 → 0.05
    across deciles, roughly even steps) — a numeric-only read would
    have had to guess. Sampled actual titles at 2-point percentile
    steps instead: unambiguously on-topic through ~48th percentile
    (score ≈0.36 — "Microbial Dynamic Regulatory Tools," "dual-layer
    signal amplifier... cellular sensors"), then a hard qualitative
    turn by the mid-50s (melanoma classifiers, implantable neural
    stimulators, oxytocin receptor comparisons in primates — clearly
    off-topic despite continuous-looking scores). **Cutoff set at 0.35
    — the boundary where the actual mix changes, not a round number
    picked in advance.** Yields 3,876 papers: 3,642 new, 234 already in
    the corpus (needing the attribution-merge treatment, same as item
    51's 7 pre-existing ATAP docs — not yet executed).
    **0.35 is `glmp-q5`'s cutoff, explicitly not GLMP's, per Claude
    Chat's correction — recorded here so it isn't quietly inherited.**
    The ATAP run already established that score ranges aren't
    comparable across questions (frontier-2's whole range sat below
    active-question-2's 10th percentile). The next question scored gets
    its own percentile sampling and its own title-read falloff; if it
    also lands near 0.35, that's a coincidence worth noting, not
    confirmation of a reusable default.
    **Dry-run clean:** 3,642 candidates, 0 failed to load, 0 gate hits,
    0 skipped (skip-check is meaningless in dry-run per item 51's own
    finding, but these were already corpus-deduped upstream during
    scoring, so this dry-run only needed to catch load/gate problems,
    not duplicates — and found none). Tagged with
    `run_id: glmp-q5-firstpass-20260809`, `acquisition_channel`, and
    `acquisition_matches` (originating PubMed term(s) + relevance score
    per paper) — same provenance shape as item 51.
    **Not yet written.** Holding for explicit go-ahead before the real
    Firestore write, same as every production write this week — this
    one would add 3,642 new documents (5.5% of the current ~66,738-doc
    corpus, comparable in scale to ATAP's own first-pass run) plus 234
    merges. Once written: re-run the spot-check method from item 51 —
    predict which GLMP queries should sharpen given synthetic-circuit
    coverage, measure, grade against the prediction — the same
    discipline that validated ATAP's run.
    **Separately flagged by Claude Chat, not yet started: the 216
    missing flowchart-source papers.** A named list
    (`collaborations/krampis-virtual-cell/flowchart-source-papers.tsv`,
    482 rows with PMIDs/DOIs already identified) — "should be acquired
    directly, not hoped for," independent of any breadth sweep since no
    term-based search guarantees hitting a specific named paper. Likely
    routes through #43 (known IDs, not a term sweep) rather than this
    scoring pipeline. Not started this session.
    Full scored dataset (7,557 rows) and the cutoff rationale filed as
    `glmp-q5-full-scored-2026-08-09.json` /
    `glmp-q5-scoring-summary-2026-08-09.json`.

    **Written, embedded, spot-checked — two predictions confirmed
    decisively, two genuinely wrong, reported as such (2026-08-09).**
    Per Claude Chat's explicit prerequisites before the write: rollback
    proven at 0 pre-write, gradient predicted and filed
    (`glmp-q5-spotcheck-prediction-2026-08-09.md`) before any post-write
    query ran, process check clean (only this session's own `claude.exe`
    plus the known-benign Chrome helper). Wrote 3,642 new docs (0
    skipped, 0 failed, 0 gate hits) and additively merged
    `acquisition_matches` onto the 234 already-in-corpus docs. Rollback
    query confirmed exactly 3,876 post-write. Embedding backfill run in
    full (pin → pilot-5 → live `find_nearest` proof on its own title,
    ranked first → full run): **3,642/3,642 embedded, 0 failed** —
    checked explicitly before reading anything into the spot-check, per
    Claude Chat's reminder that ATAP's first spot-check measured an
    empty index, not a relevance failure.
    **Graded against the written prediction, not read post-hoc:**
    - Q1 (synthetic circuits, predicted *sharpens*) — **confirmed
      decisively.** All 5 sampled citations are `glmp-q5`-run papers.
    - Q2 (synthetic vs. natural circuit logic, predicted *sharpens*) —
      **confirmed decisively.** Same result, all 5 sampled citations
      from the new run.
    - Q3 (CRP/PWM, predicted *should not move much*) — **wrong, and my
      first explanation for why was also wrong (Claude Chat's catch,
      checked directly rather than accepted).** 4 of 5 sampled
      citations are `glmp-q5`-run papers. First read: "genuine
      cross-relevance the category split undersold." That reading is
      unfalsifiable on its own — every surprise can be explained that
      way after the fact — and the actual pre/post diff doesn't
      support it. **What got displaced from the top-5 paper slots:**
      "Transcription Factor Binding Site Mapping Using ChIP-Seq"
      (ChIP-seq is literally one of `glmp-q1`'s own declared terms),
      "Massively parallel characterization of transcriptional
      regulatory elements" (direct MPRA-style site-validation
      methodology), and a computational regulation-design-optimization
      framework — all more specifically on-point for "validated
      binding-site sets... by what methods were they derived and
      validated" than what replaced them. **What replaced them** is
      about *engineering* synthetic regulatory parts ("Engineering
      Synthetic cis-Regulatory Elements for... Three Transcriptional
      Factors," "Tuning promoter strength through RNA polymerase
      binding site design") — design papers, not characterization-of-
      natural-evidence papers, each scoring 0.36–0.48 against `glmp-q5`
      (comfortably above its own 0.35 cutoff) but not obviously closer
      to `glmp-q1`'s actual question than what they pushed out.
      **Verdict: dilution wearing uptake's clothes, exactly as Claude
      Chat's alternative hypothesis predicted.** Item 52 measured only
      45 papers above 0.5 across the whole prior corpus for GLMP's
      declared questions — `glmp-q1` was thin. 3,642 semantically-
      adjacent papers arriving at once won top-k by sheer numerical
      presence against a starved baseline, not by being better answers.
      A researcher asking specifically how CRP binding sites were
      derived and validated now gets four-fifths circuit-engineering
      papers instead of the ChIP-seq/MPRA methodology papers that used
      to rank there.
    - Q4 (heat shock/sigma factors, predicted *should not move at
      all*) — **wrong, more modestly, and this one needs no such
      caveat.** 1 of the sampled citations is a new q5-run paper
      ("Anti-Sigma Factors in *E. coli*... Controlling Sigma Factors
      Availability") — sigma factors genuinely are synthetic-circuit
      control parts. Small, real, well-explained miss, no displacement
      question needed at this scale (one addition, not four).
    **Corrected read: this is a real regression risk from the write,
    not a demonstration that the questions overlap.** Pure similarity
    ranking let a numerically-abundant adjacent topic (synthetic
    circuit engineering) outrank a numerically-scarce on-topic one
    (CRP site characterization) for a query about the latter. This is
    the concrete, empirical case *for* the project-oriented-attribution
    design note's own proposal (item 52) — retrieval scoped to a
    declared question, rather than corpus-wide similarity alone, is
    what would have kept `glmp-q1`'s query from being won by
    `glmp-q5`'s papers regardless of relative volume. Not yet acted on;
    named as the reason the design note's navigation idea matters in
    practice, not just in principle. Nothing rolled back — the papers
    are correctly attributed to `glmp-q5` and the write itself is
    sound; the finding is about retrieval-time ranking, not the
    acquisition decision.
    Filed: `glmp-q5-spotcheck-pre-2026-08-09.json`,
    `glmp-q5-spotcheck-post-2026-08-09.json`,
    `glmp-q5-spotcheck-prediction-2026-08-09.md`.

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
- ~~Build domain-specific GLMP and ATAP scouts~~ — promoted to item 36 above
  (2026-08-03), rescoped against the live scout config rather than left as a
  one-line note.

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
