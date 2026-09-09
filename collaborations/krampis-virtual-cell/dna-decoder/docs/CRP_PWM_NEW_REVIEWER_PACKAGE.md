# CRP/CAP PWM — Biologist Review Package (Stage 1, reviewer #2)

> **Status: internally validated, pending biologist site-quality sign-off.**
> Do not integrate into decoder or interpret Class II claims until signed off.
> This package supersedes the earlier round sent to Prof. Nathan Lents — see
> "Prior review round" below for what's already settled.

## What this project is

GLMP (Genome Logic Modeling Project) is building a pipeline that reads
bacterial regulatory DNA sequence and outputs a logical circuit description
(AND/OR/NOT/feedback) for that region, validated against RegulonDB. The
immediate question below is narrow and self-contained: does one specific
computational PWM (position-weight matrix) for the CRP/CAP transcription
factor meet basic quality and validation standards before it's trusted
downstream. No prior familiarity with the project is needed to answer it.

## Prior review round (credit + status)

Prof. Nathan Lents (CUNY) reviewed an earlier version of this package and,
in August 2026, sent 10 foundational CRP-lac binding-site papers (DNase
footprinting, EMSA, the original PWM method paper, the first consensus-site +
3-D model, ChIP-chip, and a massively parallel binding assay) that fill the
methodology/evidence gap this review draws on. Those papers are cited
throughout and their authors credited; his contribution stands regardless of
what follows. He was not able to complete formal sign-off on the three
questions below, and this round is proceeding independently rather than
waiting further on that reply.

## Artifact

| Item | Path |
|------|------|
| PWM (MEME 4) | `motifs/crp_cap.meme` |
| Training + holdout provenance | `motifs/crp_site_lists.yaml` |
| Validation numbers | `motifs/crp_pwm_validation.yaml` |
| Build script | `scripts/build_crp_pwm.py` |

**Motif ID:** `CRP_CAP` · **Width:** 22 bp · **Training sites:** 54
**Locked FIMO threshold:** p-value ≤ **0.0001** (calibrated before any decode)

## What we need from you — Part 1: PWM sign-off (unchanged from the original ask)

1. **Training site quality** — Are the 54 RegulonDB CRP sites in
   `crp_site_lists.yaml` (`training_sites`) appropriate for a K-12 CRP/CAP PWM?
2. **lacO confound** — RegulonDB row `RDBECOLIRIC06347` annotates CRP at
   lacZp1 with a core overlapping **lacO**
   (`AATTGTGAGCGGATAACAATTT`). Accept as holdout only, or reject as
   curation noise?
3. **Holdout sufficiency** — Holdouts cover lac, ara, flhDC only. No CRP
   sites were found for trp/SOS/lambda/dna_damage regression windows. OK
   for a non-circularity claim?

### Training vs. held-out

**Held-out (never in PWM):**
- lac (canonical): `TAATGTGAGTTAGCTCACTCAT` @ lacZp1 — recovered FIMO p=7.3e-6
- lac (lacO overlap): `AATTGTGAGCGGATAACAATTT` — **review flag, see Q2**
- ara: `TTATTTGCACGGCGTCACACTT` @ araBp — recovered p=3.2e-5
- flhD: `TTGTGTGATCTGCATCACGCAT` @ flhDp — recovered p=3.1e-7

**Training filters applied:** RegulonDB Confirmed/Strong only; experimental
evidence code (`EXP-`); TGTGA present in 22 bp aligned core; lacO-overlap
cores excluded from training.

### Validation controls

| Control | Result @ p≤1e-4 |
|---------|-----------------|
| (a) Consensus | `ATTTGTGATCCGAATCACATTT` — strict TGTGA/TCACA shape fail; see notebook |
| (b) Holdout | lac + ara + flhD sites recovered (see above) |
| (c) Known positives | galP, fadL, ptsH promoters — all recovered |
| (d) Negatives | 20 random E. coli sequences — 0 false positives |
| (e) Threshold | 0.0001 locked (0% neg FPR on calibration panel) |

## What we need from you — Part 2: biology-track annotation checklist (new)

A separate computational cross-check against RegulonDB (run 2026-08-20,
`regulondb_crossref_analysis.py`) confirmed binding-site sequence identity
for lac and ara but explicitly could not judge the following — they require
literature/biological judgment, not sequence comparison:

| Circuit | Item | What's needed |
|---|---|---|
| lac | Gate assignment (NOT gate), quantitative fold-change values, Class II classification | Does the annotated logic gate and its quantitative behavior match known lac biology? |
| ara | Loop topology / Class III bistable classification | Is the ara circuit's classification as (not) persistently bistable correct? |
| trp | Repression fold, attenuation as a separate regulatory layer | **Hold — see caveat below.** |

**Caveat on trp:** the decode file's scanned DNA window is ~3.4 kb away from
the real TrpR binding sites (`trpLp`, RegulonDB `RDBECOLIRIC05054-56`) — a
known pipeline anchoring bug, not a PWM-quality question. Please don't spend
review time on trp's attenuation/repression-fold item until that window is
fixed; it isn't a fair test yet. Flagged here for completeness only.

## Sign-off

- [ ] Training site set approved
- [ ] lacO-overlap holdout disposition: keep / drop / re-annotate
- [ ] Cleared for Stage 2 (parser integration + targeted re-decode)
- [ ] lac gate/quantitative/Class II annotation reviewed
- [ ] ara loop-topology/Class III annotation reviewed

Reviewer: _______________  Date: _______________

## Reference

- Full validation report:
  `dna-decoder/docs/crp_lac_ara_trp_regulondb_validation_report.md`
- 10 papers from the prior review round: see `research_focus.json` question
  `glmp-q1` ("What validated CRP/CAP binding-site sets exist in the
  literature?") in the CopernicusAI corpus for the full ingested list with
  citations.
