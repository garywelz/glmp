# DNA Decoder — Ground Truth Reference (v0.2.2+)

Regression targets for eight E. coli / phage circuits decoded through
`run_batch.py` + `glmp_logic_parser.py` v0.2.2 (classification fix
2026-07-05). Use `dna_topology_class` as the primary pass/fail field.
`glmp_biological_class` is manifest-curated and unchanged by the fix.

| circuit_id | `dna_topology_class` (expected) | `glmp_biological_class` | Reference JSON |
|------------|-----------------------------------|-------------------------|----------------|
| `ecoli_lac_operon` | **I/II** | II | `results/ecoli_lac_operon_logic_20260705.json` |
| `ecoli_ara_operon` | **INSUFFICIENT_EVIDENCE** | III | `results/ecoli_ara_operon_logic_20260705.json` |
| `ecoli_trp_operon` | **I/II** | II | `results/ecoli_trp_operon_logic_20260705.json` |
| `ecoli_sos_lexa` | **I/II** | II | `results/ecoli_sos_lexa_logic_20260705.json` |
| `ecoli_sos_reca` | **I/II** | II | `results/ecoli_sos_reca_logic_20260705.json` |
| `ecoli_flhdc_flagellar` | **INSUFFICIENT_EVIDENCE** | I | `results/ecoli_flhdc_flagellar_logic_20260705.json` |
| `ecoli_lambda_switch` | **INSUFFICIENT_EVIDENCE** | III | `results/ecoli_lambda_switch_logic_20260705.json` |
| `ecoli_dna_damage_checkpoint` | **I/II** | II | `results/ecoli_dna_damage_checkpoint_logic_20260705.json` |

## Classification fix (2026-07-05)

Prior to the fix, `has_not` / `has_and` / `proposed_class` were derived
from raw all-pairs `logic_type_counts` (including spurious JASPAR AND
pairs with no known TF). `supporting_gates_total` used a narrower
eligible identified-regulator filter — a consistency bug that falsely
assigned Class **II** when only repressor NOT evidence was present.

After the fix, class labels are sequence-derived from the same eligible
identified-regulator gate set. **Class II is currently unreachable** on
all eight circuits: zero eligible AND gates involving a known activator
(CRP, AraC, etc.) at confidence threshold. The decoder presently behaves
as a **repression detector** (max label I/II) until activator PWMs are
built.

See `lab-notebook-2026-07-05-classification-fix.md` for full reasoning.

## ara operon — blind-spot annotation

**Expected:** `INSUFFICIENT_EVIDENCE`

AraC is not in JASPAR CORE and no custom AraC PWM is active yet. The
manifest `pending_custom_pwms` field carries the blind-spot annotation
only — it does **not** influence `dna_topology_class`:

```yaml
pending_custom_pwms:
  - name: AraC
    status: pending
```

See EC-1 in `DECODER_EDGE_CASES.md`.

**Superseded prototype value (v0.2.0, 2026-06-24):** topology hint
"Class I candidate — combinatorial activation" from manual decode
(`results/ara_operon_logic.json`, parser v0.1.0-prototype). Not a
regression target.

## lac / trp / SOS notes

- **lac:** LacI custom PWM yields confident NOT gates only → **I/II**
  (not II; no confident activator AND without CAP PWM).
- **trp:** TrpR custom PWM + repressor geometry → **I/II**.
- **SOS (lexA, recA, dna_damage):** LexA custom PWM → NOT-only → **I/II**.

**Last verified:** 2026-07-05 (Jetson full re-decode, post classification fix)
