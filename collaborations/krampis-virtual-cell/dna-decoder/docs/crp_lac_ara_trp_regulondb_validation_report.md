# GLMP Validation Report — Computation Track
## Genome Logic Modeling Project
---

**Reviewer name:** Claude Code (Anthropic), running the computation track directly at Gary Welz's
request in place of the assigned student reviewer (no response received; see note below)
**Date:** 2026-08-20, revised same day after cross-check with Cursor
**Track:** Computation — RegulonDB cross-reference
**Supervised by:** Prof. Konstantinos Krampis, Hunter College CUNY (task originally assigned to a
student assistant working under his supervision; not otherwise involved in producing this report)
**GLMP decode results version:** `ecoli_{lac,ara,trp}_operon_logic_20260708.json`
**RegulonDB version:** v14.5.0 (`TF-RISet.tsv`, local copy at `glmp/.tmp/regulondb-v14/`)

**Note on provenance:** the validation package
(`.../validation/index.html`) assigned this track to Prof. Krampis's student assistant. After an
extended period with no response, Gary asked whether this was something he could do himself —
confirmed yes, since it is purely computational and every input file (decoder JSON, RegulonDB flat
file) was already staged locally, with no biological judgment calls required (those live in the
parallel biology track). Gary then asked for it to be run. This report is the result. It is not a
replacement for the biology track, which still needs a qualified reviewer.

**Revision note:** the first version of this report used a single p ≤ 0.0001 threshold for all
three motifs, taken only from `CRP_PWM_BIOLOGIST_REVIEW.md`. Cursor, reading
`motifs/custom_pwm_registry.yaml` directly, caught that the decoder's locked thresholds are
per-motif, not global (LacI 1e-5, CRP 1e-4, **TrpR 0.05**) — confirmed against that file before
correcting. This revision uses the correct per-motif thresholds throughout, which changes the trp
section substantially (§3c, §5). Cursor's independent read of the 2026-07-08 B1 re-anchoring
notebook (`lab-notebook-2026-07-08-phase-b1-reanchor.md`) also showed that two things the first
version presented as new findings were already known and documented on that date: the lac
coordinate-frame issue (the notebook's own Step 6 already flags it as a deferred "follow-up hygiene
item," with the correct coordinate transform already written down) and the trp window gap (Step 3
documents the trp manifest window as a deliberate "metadata only" sync, already aware the true
`trpLp` TSS sits outside it). The lacO2 "omission" the first version flagged as a possible gap is
also not one — Step 1 shows it was deliberately excluded from the window. All of this is corrected
below rather than left standing.

---

## 1. Summary

Ran the full computation-track protocol (task-brief-computation.md steps 1–4) against all three
circuits, using each motif's own locked FIMO threshold (LacI p ≤ 1e-5, CRP p ≤ 1e-4, TrpR p ≤ 0.05,
per `custom_pwm_registry.yaml`). **Lac and ara: clean.** 5 predictions total, all 5 correspond to
real, experimentally Confirmed or Strong RegulonDB binding sites by sequence identity, 0 false
positives. **Trp: not clean, but not a decoder-accuracy failure either.** All 10 raw TrpR hits clear
TrpR's own (comparatively loose) 0.05 lock, but their FIMO q-values (0.68–1.0) show they are
statistically indistinguishable from chance, and none land near RegulonDB's real `trpLp` TrpR sites
— because the decode file's scanned DNA window doesn't reach that region at all, a pre-existing,
already-tracked anchoring gap (same failure class as `glmp-f2`), not something newly broken by this
analysis. Overall: precision 33.3% (5/15), recall 19.2% (5/26 RegulonDB RI-rows; see §5 for why this
understates true site recovery). Full detail in §3–§6.

---

## 2. Methods

**Files used:**
- Decoder output: `dna-decoder/results/ecoli_{lac,ara,trp}_operon_logic_20260708.json`
- RegulonDB: `.tmp/regulondb-v14/TF-RISet.tsv` (5,785 data rows; 3,973 Confirmed/Strong)
- Threshold reference: `motifs/custom_pwm_registry.yaml` (`locked_fimo_pvalue_threshold` per motif —
  the authoritative source; `CRP_PWM_BIOLOGIST_REVIEW.md` documents CRP's own lock but not the
  other two motifs')

**Script:** `dna-decoder/scripts/regulondb_crossref_analysis.py` (attached; full source in the repo
at that path). Run with a stock Python 3 interpreter, no external dependencies.

**Criteria used:**

1. **Per-motif threshold filter.** Each decode JSON's `binding_sites` array is FIMO's *full* scan
   output, not pre-filtered. The registry defines a separate locked threshold per motif — LacI_lacO
   1e-5, CRP_CAP 1e-4, TrpR_trpO 0.05 — not one global number. Comparing all raw hits with no filter
   (an early, discarded pass) gives a misleading precision figure by counting sub-threshold noise as
   a real prediction; comparing all three motifs against CRP's threshold alone (an intermediate,
   also-corrected pass) silently under-scored trp by excluding hits that legitimately clear TrpR's
   own, looser lock. Only per-motif threshold-passing sites are scored below.

2. **TF name mapping.** `LacI_lacO → LacI`, `CRP_CAP → CRP`, `TrpR_trpO → TrpR`, `AraC_araI → AraC`
   (present in the map for completeness; no decode file emits it — AraC is absent from JASPAR, as
   the task brief itself anticipates and as `CRP_PWM_BIOLOGIST_REVIEW.md` documents). No CRP/CAP
   synonym collisions found in RegulonDB's `tf_name` column for these circuits.

3. **Confidence filter.** RegulonDB's `confidenceLevel` column uses single-letter codes (`C` /
   `S` / `W` / `?`), not the spelled-out `Confirmed`/`Strong`/`Weak` the column-index header
   documents — confirmed by inspecting real rows before trusting the doc string. `{C, S}` used as
   "experimentally validated," matching the convention already used elsewhere in this codebase
   (`findability_probe.py`'s training filter).

4. **Overlap test — two independent checks, in order:**
   - **Position:** same TF, predicted center within ±20 bp of RegulonDB's `(tfrsLeft+tfrsRight)/2`,
     same chromosome (`NC_000913.3` throughout for both sources). This is exactly what the task
     brief specifies, and it is sufficient on its own for the ara circuit.
   - **Sequence (fallback only):** if position matching fails, compare the decoder's
     `matched_seq` against RegulonDB's `tfrsSeq` column (forward and reverse-complement substring
     match). This check exists because of finding (a) in §4 — position matching alone silently
     scored 4 real lac predictions as false positives. Every sequence-only match is labeled and
     listed separately (§4) rather than folded silently into the position-matched count.

5. **False-negative search window.** RegulonDB rows for the circuit's relevant TF(s), restricted to
   either (a) the decode file's own scanned genomic window (±20 bp padding around its raw hits), or
   (b) the circuit's real regulated promoter name(s) — `lacZp1/2/3` for lac, `araBp`/`araCp` for
   ara, `trpLp` for trp. (b) was added after finding that window (a) alone, for trp, entirely missed
   three real Confirmed `trpLp` TrpR sites sitting ~3.4 kb outside the decoder's own scanned range —
   restricting the FN search to a window derived from the file being validated would have silently
   under-counted false negatives the same way pure position-matching under-counted true positives
   for lac.

---

## 3. Results by circuit

*Per the task brief, the computation track's own scope is the overlap analysis (§5), not the
biology-track annotation checklist. Where a checklist item below is objectively decidable from this
cross-reference (sequence, coordinates), it is answered. Items requiring literature/biological
judgment (gate-type appropriateness, quantitative fold-change values, Class II classification) are
marked **not assessed — biology track** rather than guessed at.*

### 3a. Lac operon

| Item | Assessment | Notes |
|------|------------|-------|
| Binding site sequence (CRP + LacI, all 4 threshold-passing sites) | ✅ Correct | All 4 sequences match RegulonDB `tfrsSeq` exactly (forward or reverse-complement) for real Confirmed/Strong lacZp1/2/3 sites. |
| Genomic coordinates | ❌ Incorrect for this file — but a known, already-tracked issue, not a new one | Decode-reported positions (367051–367163) do not match RegulonDB's true coordinates for the same sequences (366323–366435). This is not a discovery of this report: the 2026-07-08 B1 re-anchoring notebook already documents it as a deferred hygiene item, with the correct transform for this minus-strand window already written down (`367343 − seq_pos + 1`). See §4. |
| Gate assignment (NOT gate), quantitative values, Class II question | Not assessed — biology track | Requires the annotation review and literature judgment this track is not scoped to make. |
| lacO2 (365922–365942) absence | Not a gap | Deliberately excluded from the scan window by design (B1 notebook Step 1: TSS−200/+1000 window, lacO2 explicitly marked "NO — deliberately excluded"). The first version of this report mischaracterized this as an open omission; it is a documented product choice. |

### 3b. Ara operon

| Item | Assessment | Notes |
|------|------------|-------|
| CRP site position | ✅ Correct | The single threshold-passing prediction (70158–70179) matches RegulonDB `RDBECOLIRIC04296` exactly, by both position and sequence — no coordinate-frame issue in this file (plus-strand window, unaffected by the minus-strand transform bug). |
| AraC sites | Expected absence, not an error | AraC is absent from JASPAR; the decoder made zero AraC predictions, exactly as `CRP_PWM_BIOLOGIST_REVIEW.md` and the task brief both anticipate. RegulonDB has 8 Confirmed AraC regulatory-interaction rows in this region the decoder cannot in principle detect. |
| Loop topology, Class III bistable classification | Not assessed — biology track | |

### 3c. Trp operon

| Item | Assessment | Notes |
|------|------------|-------|
| TrpR predictions | 10 clear the locked threshold, all 10 false positives against RegulonDB | TrpR's own lock is p ≤ 0.05 (not CRP's 1e-4 — correction from the first version of this report). All 10 raw hits pass it, but FIMO q-values run 0.68–1.0 — statistically indistinguishable from chance after multiple-testing correction. None correspond to a real RegulonDB site in-window. |
| Why: window, not motif quality | The decode file's scanned DNA (1319737–1320275) simply does not include RegulonDB's real `trpLp` TrpR sites (1323103–1323136, ~3.4 kb away). This is the same already-documented "metadata-only" manifest sync from the B1 notebook (Step 3) — known, already in the `glmp-f2` class of anchoring gaps, not discovered here. Whether TrpR's PWM itself is well-calibrated **cannot be assessed from this analysis** — the comparison window is wrong, so a fair test hasn't been run yet. |
| Repression fold, attenuation as separate layer | Not assessed — biology track | |

---

## 4. Discrepancies and flags

| Entry | Discrepancy | Evidence | Status |
|-------|------------|---------|---------------------|
| Lac — coordinate frame | 4 threshold-passing lac predictions have correct sequences but genomic coordinates that don't match RegulonDB for the same sequence. Offsets are not a single constant (636 bp, 677 bp, 820 bp) and the direction is inverted relative to RegulonDB, though internal spacing between sites matches exactly in both systems (20 bp, 72 bp). | Direct sequence match against `tfrsSeq`. Script output in `regulondb_crossref_results.json` (`coord_frame_flags`). | **Already known, not new.** B1 notebook (2026-07-08), Step 6, "Coordinate note": FIMO reports absolute coordinates on the minus-strand-fetched window; correct mapping is `367343 − seq_pos + 1`, not the additive mapping actually used. Notebook itself calls this a deferred "follow-up hygiene item." This report independently re-confirms it via a different method (RegulonDB cross-reference) and supplies the exact three offsets, which the notebook didn't have. |
| Trp — window gap | Decode file's scanned window (1319737–1320275) does not include the real `trpLp` TrpR sites (1323103–1323136). | RegulonDB `RDBECOLIRIC05054/05055/05056`, promoter `trpLp`. | **Already known, not new.** B1 notebook Step 3: trp manifest window synced to 1319700–1320400 as a "metadata only" change; TSS/`trpLp` listed separately at 1323108, already outside that window at the time of that sync. Same `glmp-f2`-class anchoring gap. |
| Trp — threshold correction | First version of this report applied CRP's 1e-4 lock to all three motifs, reporting trp as having zero threshold-passing predictions. | `custom_pwm_registry.yaml`: `TrpR_trpO locked_fimo_pvalue_threshold: 0.05`. | **Corrected in this revision**, flagged by Cursor 2026-08-20. All 10 raw trp hits actually clear TrpR's real threshold; none match RegulonDB in-window (see §3c). This is a real correction to this report, not a decoder issue. |
| Lac — lacO2 | First version flagged the LacI site at 365922–365942 as a possible unscanned gap worth reconsidering. | B1 notebook Step 1: lacO2 explicitly marked deliberately excluded from the TSS−200/+1000 window. | **Corrected in this revision.** Not a gap; a documented design choice. Removed as an open item. |

---

## 5. Computation track only — overlap statistics

*Counts below are RegulonDB regulatory-interaction (RI) *rows*, per the task brief's own protocol —
not deduplicated to unique physical DNA loci. This matters for interpreting recall: RegulonDB
records one RI row per (TF, promoter, activator/repressor role) combination, so a single physical
binding site is frequently counted 2–4× when it regulates more than one promoter or has more than
one recorded role. For lac, the 6 false-negative rows resolve to only 3 distinct physical loci; for
ara, 13 FN rows resolve to 6 distinct loci. A decoder that correctly finds every real physical site
in scanning range will still show recall well under 100% under this row-level counting for lac/ara —
that part is expected, not a decoder shortfall. Trp's false positives are a different kind of
artifact — driven by the window-anchoring gap in §4, not by RI-row multiplicity — and are not
subject to the same caveat.*

| Circuit | GLMP predicted sites (per-motif locked threshold) | RegulonDB validated sites (RI rows) | True positives | False positives | False negatives |
|---------|---------------------------------------------------|--------------------------------------|----------------|-----------------|-----------------|
| Lac operon | 4 | 9 | 4 | 0 | 6 (3 unique loci) |
| Ara operon | 1 | 14 | 1 | 0 | 13 (6 unique loci) |
| Trp operon | 10 | 3 | 0 | 10 | 3 (1 region, staggered footprints) |
| **Total** | **15** | **26** | **5** | **10** | **22** |

**Overall precision:** (5 / 15) × 100 = **33.3%**
**Overall recall:** (5 / 26) × 100 = **19.2%** (row-level; see note above on physical-locus recall being higher for lac/ara)

*Trp alone drags overall precision down from what would otherwise be 100% (lac+ara only, 5/5). Read
trp's 10 false positives as "compared against the wrong stretch of DNA, at a low-confidence
threshold" rather than "10 confidently wrong predictions" — the q-values (0.68–1.0) and the known
window gap (§4) both point the same direction. This is not an excuse to discount the number; it's
the correct explanation for it, which is what step 4 of the task brief asks this report to supply.*

---

## 6. Recommendations

1. **Lac and ara: no decoder-accuracy concern.** Every threshold-passing prediction that could be
   checked was correct by sequence identity, 0 false positives between them.
2. **Trp needs a re-anchored window before its PWM can be fairly judged.** Until the scan window
   reaches the real `trpLp` TrpR sites, this analysis cannot say whether TrpR's PWM is well- or
   poorly-calibrated — only that it hasn't been tested against the right DNA yet. Do not read the
   10 false positives as a PWM-quality finding.
3. **Route the lac coordinate-frame fix and the trp re-anchoring to whoever owns the decode
   pipeline** — both are already tracked (B1 notebook's deferred hygiene item; `glmp-f2`-class
   anchoring gap respectively). This report supplies additional confirming detail (exact lac
   offsets; a second, independent trp confirmation) but does not itself constitute new decoder work
   to open.
4. **When this analysis is redone in the future** (e.g. after the lac coordinate fix and/or trp
   re-anchoring), keep the per-motif threshold, the sequence-identity fallback, and the
   promoter-name-anchored FN search in the script — all three were necessary to reach an accurate
   answer here.
5. **The biology track's annotation checklist items (gate typing, Class II question, quantitative
   values, attenuation) remain unaddressed** — this report intentionally did not answer them. They
   still need a qualified reviewer; this track being complete does not substitute for that one.

---

## 7. References

- RegulonDB v14.5.0, `TF-RISet.tsv` — Santos-Zavaleta et al., Collado-Vides lab, UNAM
  (regulondb.ccg.unam.mx)
- `dna-decoder/motifs/custom_pwm_registry.yaml` — per-motif locked threshold source
- `dna-decoder/lab-notebook-2026-07-08-phase-b1-reanchor.md` — prior documentation of the lac
  coordinate-frame issue and the trp window sync, both predating this report
- `dna-decoder/docs/CRP_PWM_BIOLOGIST_REVIEW.md` — CRP's own locked threshold and review status
- `validation/task-brief-computation.md`, `validation/report-template.md` — task specification
  followed here
- Analysis script (this report's appendix): `dna-decoder/scripts/regulondb_crossref_analysis.py`
- Raw output: `dna-decoder/scripts/regulondb_crossref_results.json`

---

*Prepared by Claude Code at Gary Welz's direction, running the computation track directly in the
continued absence of a response from the assigned student reviewer, and revised the same day after
Cursor's independent cross-check against the registry and the B1 notebook. Not a substitute for the
biology track or for Prof. Krampis's/Lents's sign-off on the underlying PWM (item #26, tracked
separately in `GLMP_MASTER_TODO.md`).*
