# Lab notebook — LacI PWM Stage 2 (2026-07-08)

**Status:** Integrated `laci_lacO.meme` + split `trpr_motif.meme`; re-decoded 8 circuits.
**lac Class II remains PROVISIONAL.** No external claim.

Parser v0.2.4. Commit: `e6ace42` (+ notebook follow-up).

## Objective

Gate-accounting hygiene: adopt nsites=3 LacI PWM with per-motif locked threshold (mirroring
`CRP_CAP`), split LacI/TrpR MEME files, re-decode. **Not** re-litigating lac's class — lac II
is anchored by lacO1 (p≈1.5×10⁻¹⁰) + validated CRP AND.

## Step 1 — five-hit disambiguation (p ≤ 1×10⁻⁵, `laci_lacO.meme` on lac promoter)

| # | Seq pos | Genomic | Strand | p-value | Operator call | Matched sequence |
|---|---------|---------|--------|---------|---------------|------------------|
| 1 | 1–21 | 365394–365414 | + | 1.54×10⁻¹⁰ | **lacO1** (id=1.0) | AATTGTGAGCGGATAACAATT |
| 2 | 181–201 | 365574–365594 | − | 1.54×10⁻¹⁰ | **lacO1** (id=1.0) | AATTGTGAGCGGATAACAATT |
| 3 | 273–293 | 365666–365686 | − | 3.04×10⁻¹⁰ | **lacO3** (id=1.0) | GGCAGTGAGCGCAACGCAATT |
| 4 | 1–21 | 365394–365414 | − | 3.83×10⁻⁸ | lacO1-like (id=0.76) | AATTGTTATCCGCTCACAATT |
| 5 | 181–201 | 365574–365594 | + | 3.83×10⁻⁸ | lacO1-like (id=0.76) | AATTGTTATCCGCTCACAATT |

**Spurious hits: 0** at p ≤ 1×10⁻⁵. Hits 4–5 are weaker O1-family variants at the same loci as
hits 1–2 (opposite strand). **lacO2_genomic is absent** from the 350 bp decode window
(genomic 365922–365942 lies outside 365394–365744).

Effective operator loci in-sequence: **O1 (×2 positions), O3 (×1)** — not 5 independent sites.

## Step 2 — locked LacI threshold

| Control | Result at p ≤ 1×10⁻⁵ |
|---------|------------------------|
| lacO1 recovery | Yes (p≈1.5×10⁻¹⁰, rank 1) |
| lacO3 recovery | Yes (p≈3.0×10⁻¹⁰) |
| lacO2_genomic (isolated FASTA) | Yes (Stage 1 panel) |
| Non-lac specificity (27 seqs) | **0 hits** |
| lac class used to tune? | **No** — locked from Stage 1 operator/specificity sweep |

**Locked value:** `LacI_lacO` **p ≤ 1×10⁻⁵** in `CUSTOM_PWM_PVALUE_THRESHOLDS` (parser v0.2.4).

## Step 3–4 — adoption and split

| File | Role | Status |
|------|------|--------|
| `motifs/laci_lacO.meme` | LacI nsites=3 (`LacI_lacO`) | **active** (lac manifest) |
| `motifs/trpr_motif.meme` | TrpR nsites=5 (`TrpR_trpO`) | **active** (trp manifest) |
| `motifs/laci_motif_nsites1_legacy.meme` | Crude LacI+TrpR combined | archived provenance only |
| `motifs/laci_motif.meme` | Superseded combined file | **not wired** in manifests |

TrpR threshold: **p ≤ 0.05** (default custom-PWM confidence; nsites=5 matrix unchanged).

## Step 5 — 8-circuit re-decode

BEFORE = CRP Stage 2 decode (2026-07-08, `laci_motif.meme` crude LacI + combined TrpR).
AFTER = this Stage 2 (parser v0.2.4, `laci_lacO.meme` + `trpr_motif.meme`).

| circuit | BEFORE (CRP S2 + crude LacI) | AFTER (LacI S2) | Δ | bio_class |
|---------|-------------------------------|-----------------|---|-----------|
| **ecoli_lac_operon** | **II** | **II** | — | II |
| ecoli_ara_operon | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | — | III |
| **ecoli_trp_operon** | **I/II** | **I/II** | — | II |
| ecoli_sos_lexa | I/II | I/II | — | II |
| ecoli_sos_reca | I/II | I/II | — | II |
| ecoli_flhdc_flagellar | INDETERMINATE | INDETERMINATE | — | I |
| ecoli_lambda_switch | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | — | III |
| ecoli_dna_damage_checkpoint | I/II | I/II | — | II |

**All 8 `glmp_biological_class` values unchanged.**

### lac NOT accounting (eligible LacI NOT gates)

| Metric | BEFORE (`LacI_lacO1` nsites=1) | AFTER (`LacI_lacO` locked p≤1e-5) |
|--------|--------------------------------|-------------------------------------|
| Eligible LacI NOT gates | **420** | **371** (−12%) |
| Total NOT gates | 791 | 371 |
| Custom LacI binding sites in parser | 7 (loose load) | 5 at locked FIMO; parser uses locked confidence |
| TrpR spurious on lac | 420 pairs (combined file artifact) | **0** |

### trp split safety check

| Metric | BEFORE (combined `laci_motif.meme`) | AFTER (`trpr_motif.meme` only) |
|--------|--------------------------------------|--------------------------------|
| Class | I/II | **I/II** ✓ |
| TrpR NOT gates | 705 | **545** |
| Spurious LacI NOT on trp | **1080** | **0** ✓ |

## Permanent CRP-vs-LacI validation asymmetry

**CRP:** global regulator → train on non-holdout sites, hold out lac/ara/flhDC operators
(non-circular out-of-sample proof).

**LacI:** binds only lac operators (3 RegulonDB sites, all in lac operon) → **no independent
training pool** for holdout. Validation is operator-recovery + specificity + in-operon LOO,
not CRP-equivalent non-circularity. Documented in Stage 1 recon; unchanged here.

## Open for biologist

- lacO2 outside decode window — widen window in future?
- Hits 4–5 (76% O1-like) — acceptable at p ≤ 1×10⁻⁵?
- lac Class II PROVISIONAL sign-off unchanged.
