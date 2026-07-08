# Lab notebook — honest re-decode (JASPAR off for E. coli)

**Date:** 2026-07-08  
**Phase:** Motif-set cleanup + parser hygiene + honest re-decode  
**Decoder version:** glmp_logic_parser v0.2.5  
**Jetson run:** 2026-07-08T20:47:37Z (`honest_redecode_summary_20260708.json`)

## What we found (prior session)

- Loaded JASPAR CORE non-redundant MEME: **2346 motifs, 0 bacterial** (100% eukaryotic).
- All **7 eligible AND gates** in the 17-circuit suite were **lac-only** and **100% JASPAR-involved** (CRP_CAP × vertebrate/plant JASPAR; *Drosophila* MA2303.1 “crp” × JASPAR).
- Excluding JASPAR ANDs, lac is honestly **I/II** (LacI NOT only).
- `MA2303.1` in `ACTIVATOR_TFS` was a species error: JASPAR names it `crp` but species is *Drosophila melanogaster*.

## What we changed

### 1. Motif set (E. coli path)

- **`run_batch.py`:** `jaspar_enabled()` — JASPAR **OFF by default** for `ecoli_k12` (`JASPAR_DEFAULT_OFF_ORGANISMS`). Override with manifest `use_jaspar: true`.
- JASPAR file remains on disk for yeast/lambda; not scanned for E. coli decodes.
- Decode uses **custom prokaryotic PWMs only:** `CRP_CAP`, `LacI_lacO`, `TrpR_trpO`, `LexA_SOS_box` per manifest `custom_pwm_files`.
- **`motifs/empty_fimo.tsv`:** header-only stub when no JASPAR + no hits (parser emits INSUFFICIENT_EVIDENCE).

### 2. Parser hygiene (v0.2.5)

| Entry | Action |
|-------|--------|
| `MA2303.1` | **Removed** from `ACTIVATOR_TFS` (Drosophila, not E. coli) |
| `CRP_CAP` | **Added** explicitly to `ACTIVATOR_TFS` (custom PWM id) |
| `REPRESSOR_TFS` | **Audited** — all prokaryotic names; no JASPAR matrix ids |
| `ORGANISM_TF_EXTENSIONS` | **Unchanged** — `MA0299.1`/`MA0337.2` only for `s_cerevisiae` |
| Zero binding sites | **Graceful** INSUFFICIENT_EVIDENCE (no hard exit) |

No other eukaryotic or species-mismatched entries found in `ACTIVATOR_TFS` or `REPRESSOR_TFS`.

### 3. Registry / templates

- `custom_pwm_registry.yaml`: CRP `jaspar_id` → `null`; legacy note documents MA2303.1 mis-attribution.
- `manifests/TEMPLATE.yaml` + `select_batch.py`: `use_jaspar: false` for new E. coli manifests.

### 4. Re-decode harness

- **`scripts/redecode_honest.py`:** re-decodes all 17 `queue/completed/` manifests; no Firestore; writes `results/*_logic_YYYYMMDD.json` + summary JSON.
- **Bugfix (`e7c30dd`):** `fimo = _fimo_bin()` moved before JASPAR/custom branches so custom-PWM-only decodes work when JASPAR is off.

## Before / after `dna_topology_class` (17 circuits)

| circuit_id | before | after | glmp_biological_class | eligible AND |
|------------|--------|-------|----------------------|--------------|
| ecoli_aerobic_respiration | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | I | 0 |
| ecoli_amino_acid_biosynthesis | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | II | 0 |
| ecoli_anaerobic_respiration | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | II | 0 |
| ecoli_antibiotic_efflux_pumps | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | I | 0 |
| ecoli_ara_operon | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | III | 0 |
| ecoli_arginine_biosynthesis | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | II | 0 |
| ecoli_base_excision_repair | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | I | 0 |
| ecoli_catabolite_repression | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | II | 0 |
| ecoli_cold_shock_response | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | II | 0 |
| ecoli_dna_damage_checkpoint | I/II | I/II | II | 0 |
| ecoli_e._coli_osmotic_stress_response | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | II | 0 |
| ecoli_flhdc_flagellar | INDETERMINATE | INDETERMINATE | I | 0 |
| **ecoli_lac_operon** | **II** | **I/II** | II | 0 |
| ecoli_lambda_switch | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | III | 0 |
| ecoli_sos_lexa | I/II | I/II | II | 0 |
| ecoli_sos_reca | I/II | I/II | II | 0 |
| ecoli_trp_operon | I/II | I/II | II | 0 |

**Suite totals:** eligible AND = 0, JASPAR-involved AND = 0, custom-PWM-only AND = 0.

**Only topology change:** lac **II → I/II** (spurious Class II from JASPAR ANDs removed; LacI NOT + CRP activator without cooperative AND).

## Confirmations (acceptance)

- [x] **lac → I/II** (LacI NOT, no legitimate AND)
- [x] **Zero eligible ANDs** suite-wide (no JASPAR contamination)
- [x] **`glmp_biological_class` unchanged** on all manifests (two-field schema)
- [x] **Class II criterion unchanged** (dual-control deferred to Gary)

## Surprises / notes

- **flhdc_flagellar** stays **INDETERMINATE**: CRP_CAP hits present but single-activator typing does not resolve to I or II (pending single-activator semantics).
- **ara_operon** stays **INSUFFICIENT_EVIDENCE**: only CRP PWM wired; AraC custom PWM still pending.
- **10 catalog circuits** with empty `custom_pwm_files` honestly emit **INSUFFICIENT_EVIDENCE** without JASPAR — expected until more prokaryotic PWMs are assigned per circuit.
- **lambda_switch** (`phage_lambda`) still runs JASPAR by design; INSUFFICIENT_EVIDENCE (CI/Cro PWMs pending).

## Characterization (honest)

> **Validated repression detector** on reference-true E. coli windows with RegulonDB-trained custom PWMs (LacI, TrpR, LexA). Legitimate activation / cooperative AND detection is **pending** a prokaryotic motif set and resolution of single-activator typing. `dna_topology_class` is sequence-derived; `glmp_biological_class` remains curated catalog metadata.

## Deploy

```bash
# Yoga: commit + push
# Jetson:
cd /media/sdcard/glmp && git pull --ff-only
bash collaborations/krampis-virtual-cell/dna-decoder/scripts/deploy_honest_redecode_jetson.sh
```

Commits: `dec5fc7` (motif cleanup + parser hygiene + harness), `e7c30dd` (FIMO bin fix).

Raw FIMO output remains gitignored under `results/*_jaspar/` and `results/*_prok_*`.

## STOP

No model-semantics change (dual-control / Class II criterion). B2-B re-anchoring unchanged.
