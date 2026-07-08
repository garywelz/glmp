# LacI PWM — biologist review packet (Stage 1, 2026-07-08)

**Status:** Internally validated artifact `motifs/laci_lacO.meme` (nsites=3). **Not integrated**
into the decoder parser. lac `dna_topology_class` unchanged until Stage 2 + re-decode.

## Why this review

lac is **Class II (PROVISIONAL)** after CRP Stage 2. The NOT gate rests on `LacI_lacO1` in
`laci_motif.meme` — a **single-site hard consensus (nsites=1)** that produced **420 eligible
LacI NOT** relationships in the lac promoter decode. This Stage 1 build tests whether a
multi-site RegulonDB PWM can tighten that evidence.

## Part A verdict (data landscape)

| Source | LacI operator sites | Quality | Notes |
|--------|---------------------|---------|-------|
| RegulonDB v14.5 TF-RISet | **3** (Confirmed/Strong) | High (EXP, SELEX/CHIP) | All lacZp1 / lacZ — O1, O2, O3 |
| CollecTF / PRODORIC | Not ingested | — | No machine-readable pool in pipeline |
| Spec-seq / SELEX literature | 1000s of variants | High in papers | Not staged in GCS; supplements only |

**CRP-style non-circular holdout: NO.** All RegulonDB LacI sites are in the lac operon. There is
no independent training pool to hold out natural lac operators while training elsewhere.

**Validation approach:** known-operator recovery, leave-one-out among the three RegulonDB
operators, specificity on non-lac promoters, 420 eligible-NOT collapse vs legacy.

## Artifact

- **New PWM:** `motifs/laci_lacO.meme` — `LacI_lacO`, **nsites=3** (RegulonDB O1/O2/O3 only)
- **Legacy archive:** `motifs/laci_motif_nsites1_legacy.meme` (crude LacI + TrpR; provenance)
- **Site lists:** `motifs/laci_site_lists.yaml`
- **Validation:** `motifs/laci_pwm_validation.yaml`
- **Locked FIMO threshold:** **p ≤ 1×10⁻⁵** (calibrated from controls; not decoder-tested)

## Validation summary

### Known operators (at locked threshold)

| Operator | Expected rank | Observed p-rank | Recovered? |
|----------|---------------|-----------------|------------|
| lacO1 | 1 (strongest) | **1** | Yes (p≈1.5×10⁻¹⁰) |
| lacO3 | 3 | 2 | Yes |
| lacO2 (genomic RDB) | 2 | 3 | Yes |
| lacO2 (classic textbook) | 2 | — | **No** at locked threshold |

### Leave-one-out (within-operon only — NOT CRP-equivalent)

| Held out | Recovered at locked threshold? |
|----------|-------------------------------|
| lacO1 | Yes |
| lacO2_genomic | **No** |
| lacO3 | **No** |

### The 420 check (eligible LacI NOT gates)

| Condition | Legacy nsites=1 | New nsites=3 |
|-----------|-----------------|--------------|
| Parser load FIMO (p≤0.01) | **420** NOT | **371** NOT (−12%) |
| Locked custom FIMO (p≤1×10⁻⁵) | 50 NOT (1 custom hit) | 260 NOT (5 custom hits) |

**Interpretation:** At the threshold the parser actually uses to load hits (0.01), the new PWM
modestly reduces NOT-gate combinatorics (420→371) but does **not** collapse to ~3 operators.
At the locked validation threshold, the legacy motif is **stricter** (1 custom hit) than the
new PWM (5 hits). **Symmetric rigor with CRP is not yet achieved.**

### Specificity

See `laci_pwm_validation.yaml` → `specificity` block (non-lac promoter panel + random negatives).

### Consensus / shape

Consensus: `GGTTGTGAGCGGATCACAATT` — automated palindrome shape check **did not pass** (operators
are imperfect inverted repeats; manual review welcome).

## Questions for biologist

1. Accept **nsites=3 RegulonDB-only** PWM as Stage 2 integration candidate, or prefer a
   published Spec-seq / thermodynamic PSSM (safety-valve path)?
2. **lacO2:** RegulonDB genomic sequence (`GGTTGTTACTCGCTCACATTT`) vs classic textbook
   (`AAATTGTGAGCGCTCACAATT`) — which is the canonical O2 for validation?
3. Is **p ≤ 1×10⁻⁵** an appropriate locked threshold given LOO failures for O2/O3?
4. Given 420→371 at parser load threshold, is the NOT-gate evidence **tightened enough** to
   support lac Class II, or should lac revert to I/II / INSUFFICIENT until NOT evidence improves?
5. **TrpR** remains in `laci_motif.meme` (legacy file); splitting LacI/TrpR into separate MEME
   files at Stage 2?

## Sign-off checklist

- [ ] Training pool (3 RegulonDB sites) accepted
- [ ] Holdout / validation approach accepted as non-CRP-equivalent
- [ ] Locked threshold p ≤ 1×10⁻⁵ accepted
- [ ] 420-check outcome reviewed (modest improvement, not full collapse)
- [ ] Approve or reject Stage 2 parser integration
