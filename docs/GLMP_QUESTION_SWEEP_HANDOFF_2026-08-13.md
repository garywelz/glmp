# GLMP question-sweep handoff — for Gary, Claude Chat, and Cursor (2026-08-13)

**Purpose of this doc:** a status report on the GLMP corpus-expansion work of the last
several days (2026-08-08 through 2026-08-13), written so all three of us can do a joint
assessment of where the project stands and what to prioritize next. Everything below is
checked directly against live Firestore state or the commit history, not recalled from
memory — full detail lives in `docs/GLMP_MASTER_TODO.md` item 53 if anyone wants the
blow-by-blow.

## The headline

**All 11 numbered GLMP questions (`glmp-q1`–`glmp-q11`) are now attributed end to end.**
That's the finish line for an expansion effort that started 2026-08-08. Corpus total is
**117,316 papers** in `research_papers` (Firestore, `copernicusai` database), up from
roughly 45 papers under the old 2-question declaration a week ago.

## How we got here (chronological)

1. **Item 50–52 (ATAP work, prior days):** built and proved out the acquire → dedupe →
   score → cutoff-by-title-reading → write → embed → spot-check pipeline on ATAP's
   corpus first. This is the pattern everything below reuses.
2. **2026-08-08 — GLMP declaration expanded.** Gary's framing: GLMP should have
   field-spanning coverage on ATAP's scale, not a 2-question sliver. Declaration expanded
   from 2 active questions to 10 (`glmp-q1`–`q10`) + 2 frontier questions (`glmp-f1`,
   `glmp-f2`), derived from the real category/organism counts in `glmp-v2/metadata.json`
   (217 charts), not invented.
3. **Same day — dry-count overshoots, catastrophic term overload found.** Several terms
   were pulling 100K+ raw PubMed hits from unrelated senses of the same string:
   `competence regulation` (educational/clinical competency, not DNA uptake), `Class II`
   (MHC/drug classes/FDA device classes, not lac-operon activator classes), `transcription
   activation` (`glmp-q2`/`glmp-f1`, 242,672 hits). Terms were tightened
   (`glmp-tightening-pilot-2026-08-08.json`) — narrowed to bacterial/*E. coli*-scoped
   phrasing per term, not a threshold change.
4. **2026-08-09 — `glmp-q5` piloted first** (synthetic gene circuits, previously
   unrepresented category). Established the per-question methodology used for every sweep
   since: acquire everything, score against the question, **find the cutoff by reading
   actual titles at percentile steps, not by reading the score curve** (decile bands are
   smooth and uninformative; the real signal is in the titles). 3,876 papers.
5. **2026-08-09 — `glmp-q1` attribution + a real infra bug found and fixed.** Scoping
   `glmp-q1`'s query returned `glmp-q5`'s papers instead of its own — corpus-wide
   similarity search let a high-volume question's sweep crowd out a thin one's retrieval.
   Diagnosed, and **question-scoped retrieval was built and verified** (a `question` param
   on the retrieval endpoints, now load-bearing infrastructure every subsequent sweep
   depends on). Along the way, `glmp-q1` itself split into `glmp-q1` (evidence) +
   `glmp-q11` (methods) — its original seed pair covered one facet of a two-clause
   question, not both.
6. **2026-08-09 through 2026-08-11 — resumed sweeps: `glmp-q3`, `q4`, `q6`, `q7`, `q8`.**
   Each surfaced its own falloff shape and, in a few cases, its own infra finding.
   `glmp-q4` and again `glmp-q7` each found a batch of docs already embedded mid-run by
   something other than the sweep itself — same signature both times, consistent with an
   independent external actor (the daily-scout cron) running on its own schedule, not
   corruption or a local bug. `glmp-q8`'s session ended before it could write up its own
   process; that entry was reconstructed from live Firestore state instead — a real gap,
   named as one rather than backfilled with invention.
7. **2026-08-12 — `glmp-q9` swept, recovering cleanly across a session boundary.** The
   session doing this sweep hit an unrelated API-side block mid-analysis; the working
   state had already been copied to a durable repo folder rather than left in the
   session-only scratchpad, so the next session resumed without losing anything. Worth
   noting as a pattern that worked, not just a close call.
8. **2026-08-12/13 — `glmp-q10` swept** (computational network-inference methods) — the
   noisiest falloff of the whole series, since "network" is the single most overloaded
   term in the entire expanded term set (draws false positives from neuroscience, ML,
   epidemiology).
9. **2026-08-13 — full-suite audit, prompted by Gary asking directly** whether every
   declared question had actually been swept. Checked live against Firestore for all 13
   IDs (`q1`–`q11`, `f1`, `f2`) rather than trusted from docs. Found two real things:
   - **`glmp-q5` was swept back on 2026-08-09 but never added to
     `research_focus.json`'s `active_questions` array** — a bookkeeping gap, not a
     missing sweep. Backfilled.
   - **`glmp-q2` was tightened on 2026-08-08 alongside `glmp-q1` but never actually
     swept** — a real gap, fell through when the "remaining sweeps" list jumped from
     `glmp-q1` straight to `glmp-q3`.
10. **2026-08-13 — `glmp-q2` swept, closing the gap.** Largest single-question search
    pool of the whole series (29,008 unique PMIDs). Falloff was a third distinct shape —
    gradual dilution rather than `q9`'s noisy oscillation or `q10`'s extreme overload.
    Named finding: `PWM` (one of `glmp-q2`'s own declared terms) collides with "pokeweed
    mitogen," an unrelated immunology reagent — same failure class as the `Class
    II`/`competence regulation` contamination, just below the raw-count threshold that
    screen was checking.

## Current state — every question, checked live

| ID | Papers attributed | Swept | Notes |
|---|---:|---|---|
| `glmp-q1` | 1,495 | 2026-08-09 | Seed-pair anchor scoring, not text-similarity (evidence facet) |
| `glmp-q2` | 8,702 | 2026-08-13 | Closed a real gap this week |
| `glmp-q3` | 2,468 | 2026-08-09 | |
| `glmp-q4` | 1,241 | 2026-08-09 | |
| `glmp-q5` | 3,876 | 2026-08-09 | Pilot question; just backfilled into `research_focus.json` |
| `glmp-q6` | 3,583 | 2026-08-10 | Cleanest falloff of any sweep |
| `glmp-q7` | 12,400 | 2026-08-10/11 | Largest candidate pool before `q2` |
| `glmp-q8` | 10,153 | 2026-08-11 | Write-up reconstructed after a session ended early |
| `glmp-q9` | 7,342 | 2026-08-12 | Recovered across a session boundary |
| `glmp-q10` | 6,971 | 2026-08-12/13 | Noisiest falloff (term "network" heavily overloaded) |
| `glmp-q11` | 471 | 2026-08-09 | Methods facet, split from `glmp-q1` |
| `glmp-f1` | 0 | — | Frontier question, out of scope (see below) |
| `glmp-f2` | 0 | — | Frontier question, structurally not a sweep candidate |

Every entry above has a live `_acquisition_note` (or `_split_note` for `q1`/`q11`) in
`research_focus.json`, checked to match Firestore counts exactly, not just recorded once
and trusted.

## Explicitly out of scope right now

`glmp-f1` and `glmp-f2` are a different category from the numbered questions — open
engineering/judgment calls about the Programming Framework decoder itself
("is Class II activation reachable in practice," "does the RegulonDB 3-bucket
decodability categorization survive review"), not literature-corpus questions in the same
sense. `glmp-f2`'s defining term (`operon re-anchoring`) is GLMP's own internal decoder
terminology, not literature vocabulary — not a sweep candidate at all, ever. `glmp-f1`
still carries its original un-tightened terms (`Class II`, `transcription activation`)
and would need the same tightening treatment `q1`/`q2` got before a sweep would mean
anything. Left out of scope per Gary's explicit call this session — a candidate for the
group assessment below, not decided as permanently parked.

## Infra findings from this run worth carrying forward

- **Question-scoped retrieval** (the `question` param on `search_semantic`/
  `build_graph`/`answer_question`) is now load-bearing — every sweep since `q1` depends
  on it to avoid cross-question competition in retrieval.
- **Per-question cutoffs are real and non-transferable.** Every sweep found its own
  cutoff by reading titles; nothing has been near identical to another question's cutoff
  by coincidence, and the discipline explicitly warns against inheriting one.
- **Falloff shapes vary structurally, not just numerically** — clean single cliff
  (`q6`), noisy oscillation with late bounce-backs (`q9`, `q10`), gradual dilution
  (`q3`, `q5`, `q2`). Worth knowing if anyone builds tooling that assumes one shape.
- **Term-overload homonym traps are a recurring failure class**, not a one-off: CRP
  (C-reactive protein), Class II (MHC/drug/device classes), competence (clinical/
  educational), and now PWM (pokeweed mitogen). Worth a standing check on any new term
  before it's trusted, not just at declaration time.
- **An external actor (daily-scout cron) embeds docs mid-sweep, independent of the sweep
  process** — observed twice (`q4`, `q7`), same signature both times. Not a bug, but
  worth knowing if anyone builds tooling that assumes exclusive access to the corpus
  during a sweep.
- **One session-recovery pattern worked well** (`glmp-q9`): copying working state out of
  the session scratchpad into a durable repo folder *before* a session-ending error hit,
  rather than after. Cheap insurance, worth being routine practice.

## One operational note (informational, not urgent)

`glmp-q2`'s working-data folder includes a 58MB raw-metadata JSON (the largest search
pool of the series triggered it) — GitHub warned on push (still succeeded, recommended
Git LFS). Gary's call: this was an unusual circumstance, not expected to recur, no action
needed now. Flagged here for visibility since Cursor/Claude Chat may also touch this repo.

## Open items for the group assessment

Not proposing answers here — these are the live threads worth deciding on together:

1. **`glmp-f1`/`glmp-f2`** — worth tightening and sweeping like `q1`/`q2` were, or
   genuinely a different kind of work (Gary + Claude Chat judgment calls, not literature
   acquisition) that shouldn't go through this pipeline at all?
2. **Corpus scale vs. ATAP** — 117,316 papers now vs. ATAP's ~3,453-paper acquisition
   scale from earlier. Is GLMP's field-spanning goal met, over-shot, or is scale not
   actually the right comparison given the two projects cover different fields?
3. **Merge-doc quality** — several sweeps (`q2` especially, 2,411 of 8,702 via merge)
   pulled heavily from papers already attributed to other questions. Worth a pass
   checking whether the *multi*-question attribution is generally sound, or whether some
   of it reflects the same "corpus-wide volume wins" dynamic that `q1`'s original bug was
   an instance of (now scoped-retrieval-protected, but the underlying attribution
   overlap itself hasn't been separately audited).
4. **The `q8` reconstruction gap** — named rather than fixed in the moment (the session
   ended before writing itself up). Worth a deliberate look at whether that's a pattern
   to guard against going forward, or a one-off not worth process changes over?
5. **What's next for GLMP** now that the declared-question backlog is empty — new
   questions, deeper work on existing ones (e.g., the parked AraC PWM decode item), or a
   different kind of work entirely?

Parked/backlog items from `GLMP_MASTER_TODO.md` unrelated to this sweep thread but still
open: decoder follow-ups (operon re-anchoring, trp LacI motif contamination, σ32 out of
scope, RegulonDB 3-bucket decodability still PROVISIONAL/CONFOUNDED), AraC PWM decode,
scout inline-embed on the ingest critical path, `text-embedding-3-large` evaluation
(parked), several free-key rotations, `copernicusai-tts` IAM scope, biologist engagement
(Lents, then widen the pool).
