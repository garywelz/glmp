# Lab notebook — CRP PWM Stage 1 (2026-07-07)

**Status:** Internally validated; **pending biologist site-quality sign-off**.  
**Stage 2 NOT started** — parser unchanged, no re-decode, no class labels.

## Objective

Build a non-circular CRP/CAP custom PWM (`motifs/crp_cap.meme`) from RegulonDB v14.5.0,
with explicit train/holdout split for the 8 regression circuits.

## Data source

- RegulonDB **v14.5.0** `TF-RISet.tsv` (GCS: `validation/regulondb-v14/`)
- CRP rows: `tfName=CRP`, `confidenceLevel ∈ {Confirmed, Strong}`
- 178 deduped TFRS sites before holdout/quality filters

## Holdout (non-circularity)

**4 held-out sites** (zero overlap with training):

| circuit | promoter | coords | core (22 bp) | reason |
|---------|----------|--------|--------------|--------|
| `ecoli_lac_operon` | lacZp1 | 366394–366415 | `TAATGTGAGTTAGCTCACTCAT` | first_gene:lacZ (canonical lac CRP) |
| `ecoli_lac_operon` | lacZp1 | 366322–366343 | `AATTGTGAGCGGATAACAATTT` | first_gene:lacZ (**RegulonDB CRP row overlapping lacO — confound**) |
| `ecoli_ara_operon` | araBp | 70158–70179 | `TTATTTGCACGGCGTCACACTT` | first_gene:araB |
| `ecoli_flhdc_flagellar` | flhDp | 1978456–1978477 | `TTGTGTGATCTGCATCACGCAT` | genomic_overlap |

**No CRP holdouts** for: `ecoli_trp_operon`, `ecoli_sos_lexa`, `ecoli_sos_reca`,
`ecoli_lambda_switch`, `ecoli_dna_damage_checkpoint` (no Confirmed/Strong CRP TFRS at
circuit scope in RegulonDB).

Full lists: `motifs/crp_site_lists.yaml`.

## Training set

- **54 sites** after:
  1. Holdout removal
  2. TGTGA-aligned 22 bp cores
  3. `EXP-` in `tfrs_evidence` (experimental binding/expression support)
  4. Literal `TGTGA` in aligned core
  5. Exclusion of lacO-overlap cores from **training** (not from holdout log)

Build: count matrix + 0.1 pseudocount, E. coli background (A/C/G/T = 0.247/0.252/0.252/0.249).

## Validation summary

| Check | Result |
|-------|--------|
| **(a) Consensus shape** | `ATTTGTGATCCGAATCACATTT` — **strict TGTGA-N6-TCACA shape check FAIL** (degenerate spacer); FIMO still recovers canonical sites |
| **(b) Holdout FIMO** @ p≤1e-4 | lac CRP p=7.34e-6; ara p=3.21e-5; flhD p=3.11e-7 |
| **(c) Positive controls** | galP, fadL, ptsH recovered (p=2.5e-7 – 4.2e-5) |
| **(d) Negative control** | 20 random E. coli 200 bp windows: **0 hits** @ p≤1e-4 |
| **(e) Locked threshold** | **FIMO p-value ≤ 0.0001** (0% negative FPR on calibration panel) |

Details: `motifs/crp_pwm_validation.yaml`. Raw FIMO dirs under `_crp_pwm_validation/` (gitignored).

## Judgment calls / confounds (honest)

1. **lacO overlap (RDBECOLIRIC06347):** RegulonDB annotates a CRP site whose core matches
   lacO; held out but flagged for biologist review — may be curation artifact.
2. **ara CRP core** lacks literal `TGTGA` in RegulonDB uppercase annotation; recovered by
   PWM via `TGTG`/`TCAC` family match.
3. **Strict shape check** fails on consensus string even though holdout lac site matches
   textbook `TAATGTGAGTTAGCTCACTCAT` — PWM is empirically calibrated, not consensus-perfect.
4. **cAMP effector** not modeled (two-layer biology); PWM is sequence-only Stage 1 artifact.

## Tooling

- Jetson: MEME/FIMO 5.5.9 (`meme-env`), `scripts/build_crp_pwm.py`
- Build run on Jetson; artifacts committed from Yoga

## Next (Stage 2 — blocked on Gary OK)

- Register in parser custom PWM path
- Wire `ecoli_lac_operon` manifest
- Re-decode regression set only after biologist sign-off
