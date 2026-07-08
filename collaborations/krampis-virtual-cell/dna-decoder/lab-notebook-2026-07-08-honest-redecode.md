# Lab notebook — honest re-decode (JASPAR off for E. coli)

**Date:** 2026-07-08  
**Phase:** Motif-set cleanup + parser hygiene + honest re-decode  
**Decoder version:** glmp_logic_parser v0.2.5

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

### 3. Registry / templates

- `custom_pwm_registry.yaml`: CRP `jaspar_id` → `null`; legacy note documents MA2303.1 mis-attribution.
- `manifests/TEMPLATE.yaml` + `select_batch.py`: `use_jaspar: false` for new E. coli manifests.

### 4. Re-decode harness

- **`scripts/redecode_honest.py`:** re-decodes all 17 `queue/completed/` manifests; no Firestore; writes `results/*_logic_YYYYMMDD.json` + summary JSON.

## Before / after `dna_topology_class` (17 circuits)

*Filled in after Jetson run — see `results/honest_redecode_summary_YYYYMMDD.json`.*

| circuit_id | before | after | glmp_biological_class | eligible AND |
|------------|--------|-------|----------------------|--------------|
| *(see Jetson summary)* | | | unchanged | 0 expected suite-wide |

## Confirmations (acceptance)

- [ ] **lac → I/II** (LacI NOT, no legitimate AND)
- [ ] **Zero eligible ANDs** suite-wide (no JASPAR contamination)
- [ ] **`glmp_biological_class` unchanged** on all manifests (two-field schema)
- [ ] **Class II criterion unchanged** (dual-control deferred to Gary)

## Characterization (honest)

> **Validated repression detector** on reference-true E. coli windows with RegulonDB-trained custom PWMs. Legitimate activation / cooperative AND detection is **pending** a prokaryotic motif set and resolution of single-activator typing. `dna_topology_class` is sequence-derived; `glmp_biological_class` remains curated catalog metadata.

## Deploy

```bash
# Yoga: commit + push
# Jetson:
bash scripts/deploy_honest_redecode_jetson.sh
```

Raw FIMO output remains gitignored under `results/*_jaspar/` and `results/*_prok_*`.

## STOP

No model-semantics change (dual-control / Class II criterion). B2-B re-anchoring unchanged.
