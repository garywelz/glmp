# GLMP Validation Report — Computation Track
## Genome Logic Modeling Project
---

**Reviewer name:** Claude Code (Anthropic), running the computation track directly at Gary Welz's
request in place of the assigned student reviewer (no response received; see note below)
**Date:** 2026-08-20
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

---

## 1. Summary

Ran the full computation-track protocol (task-brief-computation.md steps 1–4) against all three
circuits. After correcting two methodological issues discovered during the analysis (below), the
locked decoder — i.e. only FIMO hits passing the review packet's own locked threshold, p ≤ 0.0001 —
made **5 predictions across the three circuits, all 5 of which correspond to real, experimentally
Confirmed or Strong RegulonDB binding sites** (precision 100%, recall 19.2% against RegulonDB's raw
count of regulatory-interaction rows; see §5 for why raw RI-row recall understates true site
recovery). Zero false positives were found at the locked threshold. Two discrepancies were found
that are not decoder-accuracy problems but do need engineering attention: (a) the lac and trp
decode files report genomic coordinates that do not match RegulonDB's true `NC_000913.3`
coordinates for the same DNA sequences — a coordinate-frame issue specific to those two files, not
present in the ara file — and (b) the trp circuit produced zero predictions above the locked
threshold, despite RegulonDB confirming three real TrpR sites at `trpLp` in the correct region once
found by promoter name. Full detail in §3–§6.

---

## 2. Methods

**Files used:**
- Decoder output: `dna-decoder/results/ecoli_{lac,ara,trp}_operon_logic_20260708.json`
- RegulonDB: `.tmp/regulondb-v14/TF-RISet.tsv` (5,785 data rows; 3,973 Confirmed/Strong)
- Threshold reference: `dna-decoder/docs/CRP_PWM_BIOLOGIST_REVIEW.md` (locked FIMO p ≤ 0.0001)

**Script:** `dna-decoder/scripts/regulondb_crossref_analysis.py` (attached; full source in the repo
at that path). Run with a stock Python 3 interpreter, no external dependencies.

**Criteria used:**

1. **Threshold filter.** Each decode JSON's `binding_sites` array is FIMO's *full* scan output, not
   pre-filtered — it includes many sub-threshold hits never meant to be read as real predictions.
   Verified this directly (not assumed) by sequence cross-checking: no raw hit below the review
   packet's locked p ≤ 0.0001 threshold has a matching sequence anywhere in RegulonDB; every hit
   passing it does. Comparing all raw hits (an earlier pass of this script, since corrected) gives a
   misleading, deflated precision figure by counting sub-threshold noise as if it were a real
   prediction. Only threshold-passing sites are scored below.

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
     match). This check exists because of finding (a) below — position matching alone silently
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
| Binding site sequence (CRP + LacI, both threshold-passing sites) | ✅ Correct | All 4 threshold-passing sequences match RegulonDB `tfrsSeq` exactly (forward or reverse-complement) for real Confirmed/Strong lacZp1/2/3 sites. |
| Genomic coordinates | ❌ Incorrect for this file | Decode-reported positions (367051–367163) do not match RegulonDB's true coordinates for the same sequences (366323–366435) — see §4, coordinate-frame flag. Sequence identity is unambiguous; the numeric coordinates in this decode file are not usable as-is against `NC_000913.3`. |
| Gate assignment (NOT gate), quantitative values, Class II question | Not assessed — biology track | Requires the annotation review and literature judgment this track is not scoped to make. |
| Material omissions | One found | A Confirmed LacI site at 365922–365942 (`lacZp1`) falls outside the decode file's scanned window entirely (not merely mis-coordinated) — never scanned, not just mis-anchored. |

### 3b. Ara operon

| Item | Assessment | Notes |
|------|------------|-------|
| CRP site position | ✅ Correct | The single threshold-passing prediction (70158–70179) matches RegulonDB `RDBECOLIRIC04296` exactly, by both position and sequence — no coordinate-frame issue in this file. |
| AraC sites | Expected absence, not an error | AraC is absent from JASPAR; the decoder made zero AraC predictions, exactly as `CRP_PWM_BIOLOGIST_REVIEW.md` and the task brief both anticipate. RegulonDB has 8 Confirmed AraC regulatory-interaction rows in this region the decoder cannot in principle detect. |
| Loop topology, Class III bistable classification | Not assessed — biology track | |

### 3c. Trp operon

| Item | Assessment | Notes |
|------|------------|-------|
| TrpR predictions | None above locked threshold | All 10 raw FIMO hits fall well short of p ≤ 0.0001 (best p = 0.001). Zero true or false positives possible at the locked threshold — there is nothing to score. |
| RegulonDB ground truth | 3 Confirmed TrpR sites exist at `trpLp` (1323103–1323136) | Outside the decode file's scanned window (1319737–1320275) by ~3.4 kb — a second, independent coordinate-frame discrepancy from lac's (see §4). Recovered only via promoter-name anchoring, not position. |
| Repression fold, attenuation as separate layer | Not assessed — biology track | |

---

## 4. Discrepancies and flags

| Entry | Discrepancy | Evidence | Suggested correction |
|-------|------------|---------|---------------------|
| Lac — coordinate frame | 4 threshold-passing lac predictions have correct sequences but genomic coordinates that don't match RegulonDB for the same sequence. Offsets are not a single constant (636 bp, 677 bp, 820 bp for three different sites) — the direction of coordinate change is also inverted relative to RegulonDB (decoder positions increase where RegulonDB's decrease, though the *magnitude* of internal spacing between sites matches exactly in both systems: 20 bp and 72 bp). This points to a coordinate-frame or strand-anchoring artifact specific to how this file's positions were generated, not a sequence-identification error. | Direct sequence match against `tfrsSeq`, `RDBECOLIRIC04251/04259/04260/05746`. Script output in `regulondb_crossref_results.json` (`coord_frame_flags`). | Decoder-side investigation of how `ecoli_lac_operon_logic_20260708.json`'s coordinates were derived (this is engineering, not biology, work — flagging for whoever owns the decode pipeline, not fixing here per this session's explicit scope boundary against touching decoder internals). |
| Trp — coordinate frame / window | Decode file's scanned window (1319737–1320275) does not include the real `trpLp` TrpR sites (1323103–1323136). Unlike lac, there's no threshold-passing prediction to sequence-match against, so this can't yet be characterized as an offset the way lac's was — only that the scanned window itself misses the correct region. | RegulonDB `RDBECOLIRIC05054/05055/05056`, promoter `trpLp`. | Same decoder-side flag as above — worth checking whether trp's decode window was built from the same code path as lac's. |
| Lac — omitted region | A Confirmed LacI site (365922–365942) sits outside the decode file's scanned window regardless of the coordinate-frame issue — a genuine "never looked here" gap, not a mis-anchoring. | RegulonDB `RDBECOLIRIC04258`. | Consider whether the lac scan window should extend further upstream of `lacZp1`. |
| Trp — zero threshold-passing predictions | All 10 raw TrpR FIMO hits fail the locked p ≤ 0.0001 threshold by a wide margin (best p = 0.001, ~10x too weak). | `ecoli_trp_operon_logic_20260708.json` raw `binding_sites`. | Worth flagging to whoever owns the TrpR PWM/motif — either the locked threshold is appropriately conservative and trp genuinely needs a different confirmation route, or the TrpR motif itself needs review. Not a call for this report to make. |

---

## 5. Computation track only — overlap statistics

*Counts below are RegulonDB regulatory-interaction (RI) *rows*, per the task brief's own protocol —
not deduplicated to unique physical DNA loci. This matters for interpreting recall: RegulonDB
records one RI row per (TF, promoter, activator/repressor role) combination, so a single physical
binding site is frequently counted 2–4× when it regulates more than one promoter or has more than
one recorded role. For lac, the 6 false-negative rows resolve to only 3 distinct physical loci; for
ara, 13 FN rows resolve to 6 distinct loci. A decoder that correctly finds every real physical site
in scanning range will still show recall well under 100% under this row-level counting — that is
expected, not a decoder shortfall, and is exactly the kind of caveat step 4 of the task brief asks
this report to surface.*

| Circuit | GLMP predicted sites (locked threshold) | RegulonDB validated sites (RI rows) | True positives | False positives | False negatives |
|---------|---------------------------------------|--------------------------------------|----------------|-----------------|-----------------|
| Lac operon | 4 | 9 | 4 | 0 | 6 (3 unique loci) |
| Ara operon | 1 | 14 | 1 | 0 | 13 (6 unique loci) |
| Trp operon | 0 | 3 | 0 | 0 | 3 (1 region, staggered footprints) |
| **Total** | **5** | **26** | **5** | **0** | **22** |

**Overall precision:** (5 / 5) × 100 = **100.0%**
**Overall recall:** (5 / 26) × 100 = **19.2%** (row-level; see note above on physical-locus recall being higher)

*For reference: comparing every raw FIMO hit (no threshold filter) instead of only locked-threshold
predictions gives precision 8.6% / recall 18.8% — the threshold filter is what turns this from a
noisy-looking result into a clean one. That raw-hit comparison is not the decoder's real behavior
and should not be quoted as its accuracy; it's included here only to explain why an earlier,
uncorrected pass of this script produced a much worse-looking number.*

---

## 6. Recommendations

1. **Do not read this report as a lac/trp decoder-accuracy problem.** Every threshold-passing
   prediction that could be checked was correct by sequence identity. The issues found are in how
   two of the three decode files' genomic coordinates were generated/reported, not in which DNA the
   decoder identified as a binding site.
2. **Route the lac and trp coordinate-frame findings to whoever owns the decode pipeline** (this
   report's author was explicitly out of scope to touch `crp_cap.meme` or re-decode anything, per
   this session's own constraints — this is flagged, not fixed, here).
3. **Investigate the trp PWM/threshold gap separately** from the coordinate issue — it's possible
   both fixes land in the same pipeline work, but they are two different findings and shouldn't be
   conflated into one ticket.
4. **When this analysis is redone in the future** (e.g. after a coordinate fix), keep the
   sequence-identity fallback and promoter-name-anchored FN search in the script — both were
   necessary to get an accurate answer here and would silently reintroduce this report's original,
   misleading first-pass numbers (TP=1, FP=4, FN=15) if removed.
5. **The biology track's annotation checklist items (gate typing, Class II question, quantitative
   values, attenuation) remain unaddressed** — this report intentionally did not answer them. They
   still need a qualified reviewer; this track being complete does not substitute for that one.

---

## 7. References

- RegulonDB v14.5.0, `TF-RISet.tsv` — Santos-Zavaleta et al., Collado-Vides lab, UNAM
  (regulondb.ccg.unam.mx)
- `dna-decoder/docs/CRP_PWM_BIOLOGIST_REVIEW.md` — locked FIMO threshold source
- `validation/task-brief-computation.md`, `validation/report-template.md` — task specification
  followed here
- Analysis script (this report's appendix): `dna-decoder/scripts/regulondb_crossref_analysis.py`
- Raw output: `dna-decoder/scripts/regulondb_crossref_results.json`

---

*Prepared by Claude Code at Gary Welz's direction, running the computation track directly in the
continued absence of a response from the assigned student reviewer. Not a substitute for the
biology track or for Prof. Krampis's/Lents's sign-off on the underlying PWM (item #26, tracked
separately in `GLMP_MASTER_TODO.md`).*
