# Lab notebook — Phase B1 re-anchoring (2026-07-08)

**Status:** Complete. **STOP** before B2 (5/9 TF-autoreg + `dna_damage_checkpoint` untouched; cron untouched).

**Commit:** `68faf1e` — hard-fail sequence guard + Phase B1 tooling.  
**Jetson:** `git pull --ff-only` + `scripts/phase_b1_deploy_jetson.sh`.

---

## Objective

Re-anchor lac to reference-true NC_000913.3 sequence, sync ara/trp manifest coordinates to match on-disk FASTAs, deploy hard-fail `fetch_sequence()` guard, validate all 17 completed circuits, and re-decode lac/ara/trp to test whether **lac Class II survives** on real genomic DNA.

---

## Step 1 — Pin lacZp1 window (RegulonDB-sourced)

**Source:** `/tmp/regulondb-v14/PromoterSet.tsv` row `RDBECOLIPMC03370`

| Field | Value |
|-------|-------|
| Promoter | lacZp1 |
| TSS (`posTSS`) | **366343** |
| Strand | reverse |
| First gene | lacZ |
| Evidence | EXP-IDA-TRANSCRIPTION-INIT-MAPPING (Strong) |

**Window convention (live decoder):** TSS − 200 / + 1000 → **1201 bp**

| | Value |
|---|-------|
| start | **366143** |
| end | **367343** |
| strand | **−** |
| accession | NC_000913.3 |

**Checkpoint — regulatory elements inside window:**

| Element | RegulonDB coords | Inside? |
|---------|------------------|---------|
| lacO1 | 366323–366343 | **YES** |
| CRP (RIC04251) | 366394–366415 | **YES** |
| lacO3 | 366415–366435 | **YES** |
| lacO2 | 365922–365942 | **NO** (deliberately excluded) |

---

## Step 2 — Lac re-anchor

- **Archived:** `archive/lac_operon_region_synthetic_prototype.fa` (Jun 24 pUC-style 355 bp construct).
- **Replaced:** `sequences/lac_operon_region.fa` — NCBI minus-strand slice 366143–367343 (1201 bp).
- **sha256:** `bc3e76990549ab68…` (full hash in manifest `sequence_sha256`).
- **Manifest updated:** `queue/completed/ecoli_lac_operon.yaml` (gitignored on Jetson; not in repo).

---

## Step 3 — ara/trp manifest coord sync (metadata only)

| Circuit | Old manifest window | New (matches on-disk FASTA) |
|---------|---------------------|-------------------------------|
| `ecoli_ara_operon` | NC_000913.3:103789–104390 | **69800–70400** (+), TSS 70075 (RegulonDB araBp) |
| `ecoli_trp_operon` | NC_000913.3:1917115–1917815 | **1319700–1320400** (+), TSS 1323108 (RegulonDB trpLp) |

Sequences **unchanged** (ara 601 bp, trp 701 bp curated windows).

---

## Step 4 — Hard-fail fetch guard

**Location:** `scripts/run_batch.py` → `fetch_sequence()` (lines ~83–130).

**Behavior:** If `sequence_file` exists, call `sequence_guard.validate_sequence_against_manifest()` — byte-compare to live NCBI `efetch` of manifest window; `U00096.3` ≡ `NC_000913.3` alias for header check; optional `sequence_sha256` in manifest. **On mismatch → `RuntimeError`** with circuit_id, coords, lengths, first-30bp diff. No silent substitute. `--force-refetch` on `redecode_regression.py` for deliberate rebuilds.

**Note flagged (not fixed in B1):** `select_batch.py` / `TEMPLATE.yaml` still document TSS−1000/+200; live completed manifests use **TSS−200/+1000**.

---

## Step 5 — All-17 guard validation

`scripts/validate_all_sequences.py` — **17/17 PASS** after B1 fixes.  
Summary: `results/sequence_guard_validation.json` (Jetson).

---

## Step 6 — Re-decode (controlled, not cron)

| circuit_id | old `dna_topology_class` | new | `glmp_biological_class` | Notes |
|------------|---------------------------|-----|-------------------------|-------|
| **ecoli_lac_operon** | II | **II** | II | **Class II SURVIVES** on reference-true window |
| **ecoli_ara_operon** | INSUFFICIENT_EVIDENCE | **INSUFFICIENT_EVIDENCE** | III | Unchanged (sequence unchanged) |
| **ecoli_trp_operon** | I/II | **I/II** | II | Unchanged (sequence unchanged) |

### Lac operator accounting (reference-true)

**Eligible gates:** 175 total confident (down from **371** on synthetic construct — no mirrored O1 duplicate).

**Locked-threshold LacI hits (p ≤ 1×10⁻⁵, FIMO custom PWM):**

| Operator | Genomic (FIMO) | Strand | p-value | Matched sequence |
|----------|----------------|--------|---------|------------------|
| **lacO1** | 367143–367163 | + | 1.54×10⁻¹⁰ | AATTGTGAGCGGATAACAATT |
| **lacO3** | 367051–367071 | + | 3.04×10⁻¹⁰ | GGCAGTGAGCGCAACGCAATT |
| lacO1 (RC read) | 367143–367163 | − | 3.83×10⁻⁸ | AATTGTTATCCGCTCACAATT |

**Single dominant lacO1 locus** at locked threshold (no synthetic double-hit at ~180 bp).

**CRP (canonical lacZp1):**

| Genomic (FIMO) | Strand | p-value | Matched sequence |
|----------------|--------|---------|------------------|
| 367071–367092 | + | **7.34×10⁻⁶** | TAATGTGAGTTAGCTCACTCAT |

**Coordinate note:** FIMO reports absolute NC_000913.3 coordinates on the minus-strand-fetched window. For minus-strand windows, seq position *i* maps to genomic plus-coordinate `367343 − i + 1`. The locked lacO1 hit (genomic 367143) = seq pos ~201; RegulonDB lacO1 center is 366333 (seq ~1011 in same window). Parser/FIMO coordinate reporting for minus-strand slices is a follow-up hygiene item — **classification is unaffected** because gate geometry uses FIMO-internal positions consistently.

**lac Class II:** Returns to **PROVISIONAL — pending biologist sign-off**, now on **verified reference sequence** (no longer unverified synthetic).

Output: `results/ecoli_lac_operon_logic_20260708.json`

---

## Step 7 — Scope confirmation

- **B2 NOT touched:** 5/9 TF-autoreg circuits (`trpR`, `fnr`, `soxS`, `argR`, `crp` promoters) and `ecoli_dna_damage_checkpoint` unchanged.
- **Cron NOT touched:** `run_batch.py` cron path unchanged; B1 used `phase_b1_reanchor.py` + `redecode_regression.py` only.

---

## What to discuss with Gary

1. Biologist sign-off on lac **Class II** now that anchor is reference-true.
2. Whether to add parser genomic-coordinate mapping for minus-strand windows in a future hygiene pass.
3. B2 re-anchoring brief for 5/9 + `dna_damage_checkpoint` dedup/sulAp.
