# CRP/CAP PWM — Biologist Review Package (Stage 1)

> **Status: internally validated, pending biologist site-quality sign-off**  
> Do not integrate into decoder or interpret Class II claims until signed off.

## Artifact

| Item | Path |
|------|------|
| PWM (MEME 4) | `motifs/crp_cap.meme` |
| Training + holdout provenance | `motifs/crp_site_lists.yaml` |
| Validation numbers | `motifs/crp_pwm_validation.yaml` |
| Build script | `scripts/build_crp_pwm.py` |

**Motif ID:** `CRP_CAP` · **Width:** 22 bp · **Training sites:** 54  
**Locked FIMO threshold:** p-value ≤ **0.0001** (calibrated before any decode)

## What we need from you

1. **Training site quality** — Are the 54 RegulonDB CRP sites in `crp_site_lists.yaml`
   (`training_sites`) appropriate for a K-12 CRP/CAP PWM?
2. **lacO confound** — RegulonDB row `RDBECOLIRIC06347` annotates CRP at lacZp1 with a
   core overlapping **lacO** (`AATTGTGAGCGGATAACAATTT`). Accept as holdout only, or
   reject as curation noise?
3. **Holdout sufficiency** — Holdouts cover lac, ara, flhDC only. No CRP sites were found
   for trp/SOS/lambda/dna_damage regression windows. OK for non-circularity claim?

## Training vs held-out

### Held-out (never in PWM)

- **lac (canonical):** `TAATGTGAGTTAGCTCACTCAT` @ lacZp1 — recovered FIMO p=7.3e-6
- **lac (lacO overlap):** `AATTGTGAGCGGATAACAATTT` — **review flag**
- **ara:** `TTATTTGCACGGCGTCACACTT` @ araBp — recovered p=3.2e-5
- **flhD:** `TTGTGTGATCTGCATCACGCAT` @ flhDp — recovered p=3.1e-7

### Training filters applied

- RegulonDB Confirmed or Strong only
- Experimental evidence code (`EXP-` in `tfrs_evidence`)
- TGTGA present in 22 bp aligned core
- lacO-overlap cores excluded from training

## Validation (four controls + threshold)

| Control | Result @ p≤1e-4 |
|---------|-----------------|
| **(a) Consensus** | `ATTTGTGATCCGAATCACATTT` — strict TGTGA/TCACA shape **fail**; see notebook |
| **(b) Holdout** | lac + ara + flhD sites recovered (see above) |
| **(c) Known positives** | galP, fadL, ptsH promoters — all recovered |
| **(d) Negatives** | 20 random E. coli sequences — **0 false positives** |
| **(e) Threshold** | **0.0001** locked (0% neg FPR on calibration panel) |

## Sign-off

- [ ] Training site set approved  
- [ ] lacO-overlap holdout disposition: keep / drop / re-annotate  
- [ ] Cleared for Stage 2 (parser integration + targeted re-decode)

Reviewer: _______________  Date: _______________
