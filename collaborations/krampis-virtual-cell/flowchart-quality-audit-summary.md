# Flowchart quality audit — recent expansion batch

**Scope:** 109 charts created ≥ `2026-06-12` (ground-truth expansion batch)
**Legacy comparison:** 99 older charts — median **64** nodes vs recent median **7**

## Tier summary

| Tier | Count | Meaning |
|---|---:|---|
| A_OK | 94 | Intentionally minimal or adequately detailed |
| B_REVIEW | 15 | Thin but defensible topology schematic — Krampis review |
| C_EXPAND | 0 | Under-specified for claimed pathway — expanded in this PR |

## Expansions applied (2026-06-13)

13 thin pathway schematics expanded via `scripts/expand_thin_groundtruth_charts.py`:

- `human_tlr4_lps_amplification` (6→9), `human_rig_i_mavs_antiviral` (6→9), `human_nlrp3_inflammasome` (6→8)
- `human_il6_stat3_inflammation` (6→8), `human_irf7_interferon_amplifier` (7→8), `human_cgas_sting_dna_sensing` (6→8)
- `human_scl_tal1_hematopoietic_switch` (5→7), `human_foxp3_treg_switch` (5→7), `human_cebpa_myeloid_commitment` (5→6)
- `human_myod_myogenesis` (5→6), `human_estrogen_receptor_switch` (5→6)
- `drosophila_gap_gene_network` (6→8), `drosophila_segment_polarity` (6→9)

Post-expansion: **0** tier-C charts remain; median recent node count rose from **6** to **7**.

## C_EXPAND — priority expansion list


## B_REVIEW — flagged for expert validation

- `ecoli_flhdc_flagellar` — 6 nodes — minimal node count — verify intentional
- `human_apoptosis_caspase_switch` — 7 nodes — borderline thin — acceptable topology schematic
- `human_bcl2_bax_momp` — 6 nodes — borderline thin — acceptable topology schematic
- `human_cdk1_mitotic_switch` — 7 nodes — borderline thin — acceptable topology schematic
- `human_cebpa_myeloid_commitment` — 6 nodes — IIIa autoregulation schematic — correct topology, consider adding cofactors
- `human_erk_bistable_switch` — 7 nodes — borderline thin — acceptable topology schematic
- `human_estrogen_receptor_switch` — 6 nodes — IIIa autoregulation schematic — correct topology, consider adding cofactors
- `human_iron_irp_ire` — 7 nodes — borderline thin — acceptable topology schematic
- `human_jak_stat_socs` — 7 nodes — borderline thin — acceptable topology schematic
- `human_mtorc1_nutrient` — 6 nodes — borderline thin — acceptable topology schematic
- `human_myc_autoregulation` — 6 nodes — borderline thin — acceptable topology schematic
- `human_myod_myogenesis` — 6 nodes — IIIa autoregulation schematic — correct topology, consider adding cofactors
- `human_notch_delta_lateral_inhibition` — 6 nodes — borderline thin — acceptable topology schematic
- `human_oct4_sox2_nanog_pluripotency` — 7 nodes — borderline thin — acceptable topology schematic
- `mouse_sox2_oct4_pluripotency` — 7 nodes — borderline thin — acceptable topology schematic

## Collection context

The recent batch uses **topology schematics** for ground-truth circuits: correct class and feedback topology, but far fewer nodes than legacy LLM-expanded charts (median ~66). Synthetic Class I gates and oscillators are intentionally minimal. Human innate-immunity and developmental patterning charts in tier C were expanded to add named intermediates.

Full metrics: `flowchart-quality-audit.tsv`
