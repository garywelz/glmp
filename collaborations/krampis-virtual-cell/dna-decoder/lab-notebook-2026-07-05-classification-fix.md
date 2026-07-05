# Lab Notebook — 2026-07-05: Classification / evidence consistency fix

**Author:** Gary Welz (framework owner decision)  
**Platform:** Jetson (`gary@192.168.1.222`), parser `glmp_logic_parser.py` v0.2.2  
**Regression:** 8 circuits re-decoded via `scripts/redecode_regression.py`

---

## Problem

`build_circuit_summary()` set `has_not` / `has_and` from raw all-pairs
`logic_type_counts`. Those counts include spurious JASPAR AND geometry
between non-TF hits. `assess_classification_confidence()` counted
`supporting_gates_total` from a **different** set: pairs passing
`_relationship_eligible_for_classification` (known repressor or activator
TF, repressor confidence gate for NOT).

**Symptom:** lac operon assigned Class **II** (`has_not=True`,
`has_and=True` from 122 raw AND pairs) while `supporting_gates_total=371`
(all NOT, zero eligible AND). Class label contradicted its own evidence
counter.

---

## Fix (two parts)

### Part A — eligible gate flags (approved Part 1)

Added `_topology_gate_flags()` deriving `has_not` / `has_and` from the
eligible identified-regulator set (`_relationship_eligible_for_classification`).
Replaced raw-count flags in `build_circuit_summary()`. Raw
`logic_type_counts` remain in JSON as diagnostics only.

### Part B — discriminating class-label rule (approved Part 2)

Added `_derive_topology_class_label()` — **sequence-derived only**; does
not read `pending_custom_pwms` or manifest regulator lists.

| Eligible NOT | Eligible AND | Label |
|--------------|--------------|-------|
| yes | yes | **II** |
| yes | no | **I/II** |
| no | yes | **I** |
| no | no + confident OR/XOR/other with known TF | **INDETERMINATE** |
| no | no + zero confident TF gates | **INSUFFICIENT_EVIDENCE** |

Removed the old `None → INDETERMINATE` fallback; labels are assigned
explicitly by the rule above.

---

## Re-decode results (2026-07-05)

| circuit_id | old `dna_topology_class` | new | changed? | reason |
|------------|--------------------------|-----|----------|--------|
| `ecoli_lac_operon` | II | **I/II** | yes | 791 eligible NOT; 0 eligible AND |
| `ecoli_ara_operon` | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | no | zero confident TF gates; AraC blind spot in `pending_custom_pwms` only |
| `ecoli_trp_operon` | I/II | I/II | no | TrpR NOT only |
| `ecoli_sos_lexa` | II | **I/II** | yes | LexA NOT only |
| `ecoli_sos_reca` | II | **I/II** | yes | LexA NOT only |
| `ecoli_flhdc_flagellar` | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | no | no confident TF gates |
| `ecoli_lambda_switch` | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | no | no confident TF gates (CI/Cro PWMs pending) |
| `ecoli_dna_damage_checkpoint` | II | **I/II** | yes | LexA NOT only |

All predictions matched actual re-decode output. **lac confirmed I/II.**

`glmp_biological_class` unchanged on all 8 (manifest-curated).

---

## Key result

**Class II is currently unreachable** across all eight regression circuits.
Class II requires both eligible NOT and eligible AND from confident
identified-regulator gates. With zero activator PWMs at confidence
(CRP, AraC, FlhDC, CI/Cro, etc.), the decoder is presently a
**repression detector** — honest maximum label **I/II**.

Building activator PWMs is a separate deferred workstream (not part of
this fix).

---

## Not changed (deferred)

- trp LacI motif contamination  
- operon re-anchoring (RegulonDB promoter coords)  
- T1/T2/T3 geometry theories  
- PWM builds  

---

## ara `pending_custom_pwms` verification

Manifest `queue/completed/ecoli_ara_operon.yaml` still carries:

```yaml
pending_custom_pwms:
  - name: AraC
    status: pending
```

Batch log on re-decode: `Pending custom PWMs (may yield INSUFFICIENT_EVIDENCE): AraC`.
This annotation is **not** folded into `dna_topology_class`.

---

## Artifacts

- Parser diff: `glmp_logic_parser.py` (`_topology_gate_flags`, `_derive_topology_class_label`)
- Re-decode script: `scripts/redecode_regression.py`
- Summary JSON (Jetson): `results/regression_redecode_20260705.json`
- Updated ground truth: `GROUND_TRUTH_REFERENCE.md`
