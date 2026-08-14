# Merge-quality audit + glmp-q8 prune — session handoff (2026-08-13/14)

Written proactively given several recurring session-terminating API errors
this session (`req_011Ce14nKEsDUu4qqHipFuvg`, `req_011Ce16689V8jVpmUVAzXjc7`,
`req_011Ce16H8baRfw1qtjFwq6vB`, `req_011Ce16fNW7FnaZHVH33tHj5` — filed as
feedback, ID `7b88b432-3e33-42ba-9655-b5a2be1ee6f0`). All substantive work
below is complete and committed to Firestore/docs already — this file exists
so a new session has full context, not because anything is mid-write.

## What this thread was

After the `glmp-q10`/`glmp-q2` close-out (all 11 numbered questions swept —
see `docs/GLMP_QUESTION_SWEEP_HANDOFF_2026-08-13.md`), Gary looped in Claude
Chat and Cursor for a joint assessment of what's next. Both raised open
items; this session verified the checkable ones directly rather than debate
them, then acted on what the verification found.

## Status: all done, not in progress

1. **`glmp-f1` terms fixed** in `research_focus.json` — synced to the
   2026-08-08 tightening decision (`Class II`/`transcription activation`
   removed) that had been decided and documented in item 53 but never
   applied to the live file. Confirmed the risk was real but dormant (live
   daily-scout cron reads `daily_scout_config.json`, not
   `research_focus.json`, directly — so nothing was actively firing on the
   bad terms). Done.

2. **Merge-quality audit, two pairs sampled at score boundaries (not
   top-ranked docs):**
   - `glmp-q2`–`glmp-q8` (1,692 overlap docs): **clean.** No
     volume-artifact signature — every sampled doc's `glmp-q8` score sat
     well above `glmp-q8`'s own cutoff regardless of its `glmp-q2` score.
   - `glmp-q10`–`glmp-q3` (486 overlap docs): **real distortion found.**
     Near `glmp-q10`'s boundary, `glmp-q3` scores exceeded `glmp-q10`
     scores by ~0.10 on average (reversed near the top, by ~0.16) —
     boundary docs read as genuine `glmp-q3` papers only weakly crossing
     `glmp-q10`'s noisier, lower cutoff. Consistent with `glmp-q10`'s
     already-known "network" term-overload, not a new defect. **Not
     acted on** — named as a finding, no prune run against this pair (see
     "not yet decided" below).

3. **`glmp-q8`'s own cutoff, independently verified for the first time —
   the significant finding.** `glmp-q8`'s original write-up was a
   reconstruction (the session that ran it ended before documenting
   itself); its recorded 0.36 cutoff was never verified by title-reading,
   only reverse-engineered as the minimum score among already-written
   docs. A full percentile-block read (5-point steps across all 10,153
   live-attributed docs) found on-topic majority holding only through
   ~p10 (score ≥0.5004) — real cutoff should have been dramatically
   higher than 0.36.

4. **Gary's decision: prune, don't just re-document.** Weighed leaving the
   extra ~9,000 papers (no direct cost either way) against two concrete
   downsides — degraded precision for `question=glmp-q8`-scoped queries,
   and a documentation claim that would be known-inflated, bearing
   directly on Goals Priority 2's "100,000+ high-relevance" target. Chose
   to fix it for real.

5. **Prune executed — first subtractive operation in this project.**
   Dry-run → 6-doc live pilot (verified directly: both
   `question_scope_ids` and `acquisition_matches` cleanly emptied, docs
   themselves untouched, embeddings intact) → full run: 9,131 processed,
   6,523 left with no other question (now unscoped, same normal state as
   any daily-scout paper — not removed from the corpus), 2,608 retained
   under other legitimate attribution, 0 failures. **Rollback proof
   exact: 10,153 → 1,016.** Corpus total essentially unchanged
   (117,316 → 117,334) since nothing was deleted, only the `glmp-q8`
   scope tag.

6. **Docs updated:** `research_focus.json`'s `glmp-q8` entry and
   `GLMP_MASTER_TODO.md` item 53 both carry the full finding — the audit
   methodology, both merge-pair results, the percentile data, the
   decision, and the exact execution numbers. **Not yet committed or
   pushed to GitHub** — that's the one remaining step.

## Resolved since this handoff was written

- **`glmp-q10` re-verification (2026-08-14, follow-up session):** ran the
  same independent re-verification sequence used on `glmp-q8` — full
  percentile read of all 6,971 live-attributed docs (5-point steps, then
  2-point steps through the p40–60 transition zone). **Different outcome
  than `glmp-q8`: the cutoff holds up.** Unlike `glmp-q8`'s reconstructed
  number, `glmp-q10`'s cutoff was genuinely title-verified at sweep time,
  and the fresh read reproduced the documented oscillation almost exactly
  (clean on-topic blocks recur as late as p44/p48, dip p46/50/52, recover
  p54/56, then settle off-topic from p58 on, never recovering). The
  `glmp-q10`–`glmp-q3` boundary distortion still holds but reads as a
  normal thresholding edge effect on the bottom ~10% band, not a
  miscalibration. **Decision: no prune.** Working files added to this
  folder: `pull_q10_full_scores.py`, `_percentile_sample_q10.py`,
  `q10_all_scored_live.json`. Full note appended to `glmp-q10`'s entry in
  `research_focus.json`.
- **`glmp-f1`/`glmp-f2` scope question** (tighten-and-sweep `f1` vs. leave
  frontier out of the pipeline entirely) — Gary's call this session was
  "leave out of scope for now," not a permanent decision. Still open per
  the original three-way handoff.
- **Front-end/status-page count honesty** (Cursor's finding — AUTO-STATUS
  still says 62,312, status pages advertise "Target: 100,000") — not
  touched this session.

## Immediate next step if resuming

1. Commit and push (`docs/research_focus.json`, `docs/GLMP_MASTER_TODO.md`,
   `docs/open-questions/glmp-merge-quality-audit-2026-08-13/` working
   folder) — ask Gary first per this project's standing rule, don't just
   do it.
2. Ask Gary whether to run the same re-verification-and-decide sequence
   against `glmp-q10`'s own cutoff, and/or the `glmp-q10`–`glmp-q3`
   distortion specifically, now that `glmp-q8` has been through it.
3. Loop the outcome back to Claude Chat/Cursor if Gary wants — this
   session's finding (a ~9,000-paper prune) is significant enough to be
   worth their independent read too, not just a fait accompli.

## Working files in this folder

Every pull/audit/prune script used this session is saved here (not
scratchpad) — `pull_q2_q8_boundary.py`, `pull_q10_q3_boundary.py`,
`pull_q8_boundary.py`, `pull_q8_full_bands.py`, `pull_q8_full_scores.py`,
`prune_q8_below_p10.py`, plus their JSON outputs
(`q8_all_scored_live.json` is the full 10,153-row cache, reusable for any
follow-up read without re-querying Firestore) and verification scripts.
