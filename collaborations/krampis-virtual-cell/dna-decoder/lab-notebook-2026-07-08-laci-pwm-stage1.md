# Lab notebook — LacI PWM Stage 1 (2026-07-08)

**Status:** PWM built and validated internally; **pending biologist sign-off**. **Stage 2 NOT
started** — parser unchanged, no re-decode, no class labels.

## Objective

Replace the crude nsites=1 LacI consensus (`laci_motif.meme`) with a validated multi-site PWM
so lac's NOT gate evidence is as rigorous as the CRP AND gate (Stage 2, bada1d1). Stage 1 only:
recon → build → validate → package.

## Part A — data landscape recon

### RegulonDB v14.5 TF-RISet (LacI, Confirmed|Strong)

| RI ID | Operator | Coords | Core (21 bp) | Conf |
|-------|----------|--------|--------------|------|
| RDBECOLIRIC04260 | lacO1 | 366323–366343 | `AATTGTGAGCGGATAACAATT` | C |
| RDBECOLIRIC04258 | lacO2_genomic | 365922–365942 | `GGTTGTTACTCGCTCACATTT` | S |
| RDBECOLIRIC04259 | lacO3 | 366415–366435 | `GGCAGTGAGCGCAACGCAATT` | S |

**Total: 3 sites — all lacZp1 / lacZ scope.** No separate lacIp autoregulatory row.

### External sources (not machine-ingested)

- **CollecTF / PRODORIC:** not exported into this pipeline.
- **Spec-seq / SELEX / Osym variant literature:** rich but not staged in GCS; noted as
  safety-valve if RegulonDB-only PWM insufficient.

### VERDICT

| Question | Answer |
|----------|--------|
| Pool large enough for CRP-style train-on-others / hold-out-lac? | **NO** |
| Chosen validation | Known-operator recovery, LOO within 3 operators, specificity panel, 420 NOT collapse |
| Safety valve triggered? | **Partial** — PWM built but 420 collapse modest; biologist to judge Stage 2 |

Full recon YAML: `motifs/laci_pwm_recon.yaml`

## Part B — build

- **Method:** 21 bp cores GCG-centered alignment; count matrix + 0.1 pseudocount; E. coli
  background; **training = 3 RegulonDB operators only** (literature supplements dropped after
  alignment degraded consensus).
- **Output:** `motifs/laci_lacO.meme` — `MOTIF LacI_lacO`, **nsites=3**
- **Consensus:** `GGTTGTGAGCGGATCACAATT`
- **Legacy preserved:** `motifs/laci_motif_nsites1_legacy.meme` (crude LacI + TrpR; parser still
  uses `laci_motif.meme` until Stage 2)

## Part C — validation

### Locked FIMO threshold: **p ≤ 1×10⁻⁵**

Calibrated from known-operator recovery + non-lac specificity panel **before** any decoder
class inspection.

### Known-operator recovery (at locked threshold)

- **lacO1:** p≈1.5×10⁻¹⁰ — rank **1** (expected strongest) ✓
- **lacO3:** p≈3.0×10⁻¹⁰ — rank 2
- **lacO2_genomic:** p≈1.6×10⁻⁹ — rank 3
- **lacO2_classic (textbook):** not recovered at locked threshold

Affinity ordering partially matches biology (O1 strongest); classic O2 mismatch vs RegulonDB
genomic annotation flagged for biologist.

### Leave-one-out (within-operon — NOT CRP-equivalent holdout)

| Held out | Recovered? |
|----------|------------|
| lacO1 | Yes |
| lacO2_genomic | **No** |
| lacO3 | **No** |

With only three correlated operators, LOO is weak evidence; reported honestly.

### The 420 check

Eligible LacI NOT gates in lac promoter (JASPAR + custom FIMO → parser grammar):

| FIMO threshold | Legacy nsites=1 | New nsites=3 | Δ |
|----------------|-----------------|--------------|---|
| **0.01** (parser custom load) | 420 | **371** | −12% |
| **1×10⁻⁵** (locked validation) | 50 (1 custom hit) | 260 (5 custom hits) | worse |

**Honest read:** The new PWM **does not** deliver the hoped-for collapse to ~3 operators. At
parser-relevant load threshold there is a **modest** reduction (420→371). The legacy single-site
matrix is accidentally strict at the locked validation threshold (1 hit). Stage 2 integration
must pair the new PWM with an explicit per-motif locked threshold (as CRP_CAP) and re-decode
before any class claim.

### Specificity

See `motifs/laci_pwm_validation.yaml` → `specificity` (7 non-lac circuit promoters + 20 random
200 bp negatives).

## Part D — honest validation statement

**Achieved:**

- Multi-site PWM (nsites=3) from experimental RegulonDB operators
- Locked threshold before decoder
- lacO1 strongest in known-operator panel
- Modest 420→371 reduction at parser load threshold
- Legacy motif archived for provenance

**Not achieved (and not claimed):**

- CRP-equivalent non-circular holdout
- Large 420→~3 collapse
- LOO recovery for all three operators
- Automated palindrome shape pass
- Spec-seq-scale variant training

**Implication for lac Class II (PROVISIONAL):** Stage 2 LacI integration + re-decode required;
biologist must re-evaluate whether NOT evidence is sufficient after integration.

## Artifacts

| File | Role |
|------|------|
| `scripts/build_laci_pwm.py` | Build + validate driver |
| `motifs/laci_lacO.meme` | Stage 1 candidate PWM |
| `motifs/laci_motif_nsites1_legacy.meme` | Provenance archive |
| `motifs/laci_site_lists.yaml` | Training sites + provenance |
| `motifs/laci_pwm_validation.yaml` | Quantitative validation |
| `motifs/laci_pwm_recon.yaml` | Part A recon verdict |
| `docs/LACI_PWM_BIOLOGIST_REVIEW.md` | Review packet |

Raw FIMO scratch: `_laci_pwm_validation/` (gitignored).

## Open for Gary / biologist

1. Proceed to Stage 2 integration with `laci_lacO.meme` + locked p≤1e-5, or adopt published PSSM?
2. Accept 420→371 as sufficient NOT tightening, or require stricter gate logic?
3. Resolve lacO2 genomic vs textbook sequence.
4. Split LacI/TrpR MEME files at Stage 2?
