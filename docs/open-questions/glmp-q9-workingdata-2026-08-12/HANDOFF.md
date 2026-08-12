# glmp-q9 sweep — session handoff (2026-08-12)

Session ended mid-sweep due to an API-side session block (unrelated to this
work — see `q9-session-error-note.md` in this folder). All PubMed
acquisition and scoring is done and cached in this folder; nothing needs
to be re-fetched or re-embedded. What's left is finishing the falloff
read, then the write/embed/spot-check/write-up steps that q3/q4/q6/q7/q8
all followed.

## Question being swept

`glmp-q9`: "What regulatory logic governs developmental commitment and
cell-fate decisions, and how is the decision made irreversible?"

Terms: `cell fate decision network`, `developmental switch commitment`,
`sporulation initiation regulation`, `competence regulation Bacillus
subtilis`, `lineage commitment transcription factor`, `epigenetic memory
gene expression`.

## Status of each stage

1. **PubMed search** — DONE. `q9_search.py` → `q9_pmids_raw.json`.
   10,198 unique PMIDs across the 6 terms (matches the recorded tightened
   dry-count figure, 10,194, within a few days' index drift).
2. **Metadata fetch** — DONE. `q9_fetch.py` → `q9_metadata.json`.
   10,195/10,198 fetched (3 failed to parse, normal rate, IDs recorded in
   the file's own `failed` list).
3. **Corpus dedup** — DONE. `q9_dedupe.py` → `q9_dedupe.json`.
   611 candidates already in corpus (merge targets), 9,587 genuinely new.
   **Rollback pre-write proof confirmed: 0 docs currently carry `glmp-q9`
   in `question_scope_ids`** — clean baseline, safe to write into.
4. **Scoring** — DONE. `q9_score.py` → `q9_scored.json`.
   All 10,195 scored by cosine similarity against the embedded question
   text. Reused existing Firestore embeddings for the 611 already-corpus
   papers; freshly embedded the other 9,584 via
   `text-embedding-3-small` (title+abstract+keywords, matching
   `create_text_for_paper()`'s production convention). 0 errors.
5. **Falloff read / cutoff — IN PROGRESS, not decided yet.** This is the
   step to resume.

## Falloff read so far — read this before continuing

**Important correction made mid-read, worth preserving:** the top ~60%
of results by score are almost entirely mammalian developmental biology
(T-cell lineage commitment, embryonic stem cell differentiation,
myogenesis, osteoblast/adipocyte switches, hematopoietic lineage
factors). First instinct was to read this as off-topic contamination,
since GLMP is mostly bacteria-focused. **That instinct was wrong — checked
before acting on it.** GLMP's own 217-chart catalog
(`glmp-v2/metadata.json`) already includes a `Hematopoiesis` category
(C/EBPα, GATA1–PU.1, SCL/TAL1 — human and mouse blood-lineage switches)
alongside its bacterial/yeast/fly/worm `Developmental Decision` /
`Developmental Patterning` / `Developmental Program` charts (*B.
subtilis* sporulation/competence/biofilm, *S. cerevisiae* meiosis,
*Drosophila* gap-gene/segment-polarity, *C. elegans* dauer switch). So
the mammalian content in the search results is genuinely on-topic for
this question, not a term-tightening failure like the earlier "Class
II"/"competence regulation" false-positive findings. **Do not re-flag
this as contamination without re-deriving this same check.**

Real bacterial sporulation/competence papers ARE present throughout the
ranking, just diluted by the much larger mammalian-developmental-biology
literature rather than absent — e.g. the #8-ranked paper overall
(0.08th percentile) is "Temporal competition between differentiation
programs determines cell fate choice," and genuine *B. subtilis*
sporulation papers (SirA/DnaA, spoIIM/sigma-E, AbrB, KinB→phosphorelay)
still appear as late as p84–p88.

**Percentile-block sampling done so far** (`q9_percentile_titles.txt` =
p10–p60 single-title samples; `q9_percentile_titles_2.txt` = p60–p90
single-title samples; `q9_percentile_blocks.txt` = 5-title windows every
2 points from p58–p92, the most useful file for the actual cutoff
decision). Reading the blocks file:

- **p58–p70**: still majority genuinely on-topic (bacterial sporulation,
  hematopoietic/lineage-commitment, developmental transcription factors),
  with the first scattered off-topic titles appearing (hippocampal
  memory-formation epigenetics at p58 — a different sense of "memory"
  than the term intends).
- **p72–p80**: mix shifts — real bacterial sporulation content (CodY,
  LiaS/LiaR, MinC-FtsZ, spoIIM) still present, but increasingly
  interleaved with clearly off-topic material: HIV latency, prefrontal-
  cortex fear-extinction epigenetics, diabetic nephropathy epigenetics,
  CAR-T-cell antitumor reprogramming, Alzheimer's treatment papers.
- **p82–p92**: off-topic material becomes frequent (Alzheimer's QTL,
  cold-shock protein biochemistry, nanoneedle drug delivery, epilepsy
  electrophysiology, schizophrenia models) but genuine bacterial
  sporulation/competence papers (SirA/Soj/ParA, srfA locus, AbrB/SinR,
  Bacillus anthracis pXO1 Rap phosphatase) are *still* interleaved even
  this far down — later than any prior sweep's falloff.

**Not yet decided: where exactly to cut.** The mixed-interleaving pattern
(genuine on-topic bacterial content persisting deep into the ranking,
never cleanly separating from off-topic drift) resembles `glmp-q4`'s
"switch" overload more than `glmp-q6`'s clean falloff — a single sharp
cutoff will necessarily include some off-topic material and exclude some
genuine bacterial sporulation content no matter where it's set, the same
tradeoff `glmp-q4` named explicitly rather than hid.

## Recommended next step

Read `q9_percentile_blocks.txt` directly (it's short, ~10KB) rather than
re-deriving it. A defensible cutoff reads like it sits somewhere in the
**p70–p80 range** (score ≈0.30–0.33) — p58–p70 is still clearly
majority on-topic, p82+ is clearly majority off-topic, and p70–p80 is
the genuine transition zone. Pick the specific point by the same
standard every prior sweep used: where does the *majority* in a 5-title
window flip from on-topic to off-topic, not where does the last on-topic
title appear (some on-topic content will always be lost past any single
cutoff — q4 accepted this explicitly for "switch").

Once the cutoff is picked:
1. Compute the resulting count (rows in `q9_scored.json` with
   `score >= cutoff`), split new (9,587 pool) vs. merge (611 pool) using
   `q9_dedupe.json`.
2. File a short prediction (expected rollback count, expected scoped
   spot-check behavior) before writing — matches every prior sweep's
   discipline, and this session's own q8 write-up named skipping this as
   a real gap worth not repeating.
3. Dry-run: confirm all candidate docs above cutoff load cleanly from
   `q9_metadata.json`/reused embeddings, no duplicate IDs.
4. Rollback pre-write proof already done (0, see above) — re-confirm
   fresh at write time in case anything changed since 2026-08-12.
5. Write: new docs need `question_scope_ids: ["glmp-q9"]`,
   `acquisition_matches: [{question: "glmp-q9", kind: "active_question",
   score, terms}]`, `run_id: "glmp-q9-firstpass-<date>"`, plus the
   standard paper schema fields from `q9_metadata.json`. New docs also
   need their embedding written (already computed in `q9_scored.json`
   only as a similarity float, not the raw vector — the raw 1536-dim
   vectors from the scoring run were NOT persisted to disk, only the
   cosine similarity was, to keep the checkpoint file small. **The
   embedding backfill step will need to re-embed new docs from scratch**
   using `create_text_for_paper()`'s exact convention
   (title+abstract+keywords), the same as `backfill_research_paper_
   embeddings.py` does for every prior sweep — this is not extra work,
   it's the same embedding-backfill stage every sweep already runs.)
   Merge docs (611) get `ArrayUnion` onto `acquisition_matches` and a
   recomputed `question_scope_ids`, no new embedding needed (they already
   have one).
6. Rollback post-write proof: exact count match.
7. Embedding backfill: pin → dry-run → pilot-5 → live `find_nearest`
   proof → full run, matching every prior sweep.
8. Scoped-retrieval spot-check: `search_semantic(question="glmp-q9", ...)`
   against `cloud-run-backend/mcp_server/tools/vector_search.py` (see
   this session's q8 spot-check for the exact call pattern), verify
   narrowing to `["papers"]` and genuine on-topic top-5 with matching
   `acquisition_matches` scores.
9. Update `docs/research_focus.json` with `glmp-q9`'s live entry, write
   up `docs/GLMP_MASTER_TODO.md` item 53 with the real falloff narrative
   (this time done live, not reconstructed after the fact like `glmp-q8`
   had to be), commit, push if asked.

## Task list state (may not survive the session boundary)

This session had TaskCreate items #1–7 tracking this exact sequence
(#1 in_progress, #2–7 pending). If the new session doesn't see them,
this file is the source of truth — recreate them from the list above if
useful, but they're not required to resume; everything needed is in this
folder.
