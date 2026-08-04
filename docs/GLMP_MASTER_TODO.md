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

33. **AUDIT (scoped, not run) — `loops`/`feedbackEdges` may be blind to a
    duplicate-node pattern corpus-wide.** Surfaced 2026-08-02 while
    fact-checking a Zenodo-cited lac operon record. `loops`/`feedbackEdges`
    are computed mechanically from Mermaid-graph cycle detection
    (`scripts/mermaid_graph.py` / `backfill_loops.py`), not curated. If one
    biological entity is given two node IDs (e.g. permease modeled as both
    `G[Lactose Permease LacY]` and `PP[Lactose Permease]`), a real feedback
    cycle renders as a straight-line path and the detector correctly reports
    `loops: 0` for a graph that should show a loop — a false negative, not a
    bug in the detector. `ecoli_lac_operon` was caught only because a human
    curator separately noticed the inconsistency and left a
    `circuitClassNeedsReview: true` rationale note; nothing forces that catch
    to happen. **Scope, don't run yet:** how many other corpus records show
    `loops: 0` (or `feedbackEdges: 0`) with no such review flag — same defect,
    uncaught. Presence-without-correctness, same family as the findability
    probe (item 21) but for structural/topological correctness rather than
    retrievability. Gary scopes execution later.

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

39. **Check the real ATAP/mathematics corpus for the Mermaid syntax bugs found in
    PR #5 (promoted 2026-08-04, not yet scoped or run).** Closed PR
    `cursor/mathematics-database-flowchart-errors-d178` (item 28) fixed real
    Mermaid rendering bugs — `style` directives concatenated onto node/edge
    statements, invalid `{[...]}` decision-node syntax, raw HTML embedded in
    labels, all causing intermittent parse failures — but only against
    root-level scratch/temp copies (`math.html`, `tmp-binomial.html`,
    `sanitized_processes*/`), never against the real corpus path
    (`huggingface-space/mathematics-processes-database/`). **Whether these same
    defect patterns exist in the actual live files was never checked** — the PR
    never touched them, so its existence proves nothing either way about the
    real corpus's health. Needs: a scan of the live `mathematics-processes-database/`
    HTML/Mermaid files for the three specific patterns above, then a decision on
    whether any found instances warrant a fresh, correctly-scoped fix (reusing
    PR #5's diagnosis, not its diff, since that diff targets files that no
    longer matter).

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
