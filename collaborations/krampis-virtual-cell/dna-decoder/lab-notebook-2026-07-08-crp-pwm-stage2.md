# Lab notebook — CRP PWM Stage 2 (2026-07-08)

**Status:** CRP PWM integrated into the decoder and re-decoded across the 8-circuit
regression set. **lac Class II is PROVISIONAL** pending biologist sign-off (lacO/CRP
overlap disposition + canonical-site confirmation). No external claim; awaiting Gary.

Parser: `glmp_logic_parser.py` **v0.2.3** (commit `69e3120`). CRP registry entry flipped
`pending → active`. Locked FIMO threshold **p ≤ 1e-4** (from Stage 1).

## Objective

Integrate the Stage 1 CRP/CAP PWM (`motifs/crp_cap.meme`) into the custom prokaryotic PWM
scan at the locked p ≤ 1e-4, re-decode all 8 known circuits, and label honestly — class
labels must derive from **actual sequence detection**, and a lone CRP hit must not
auto-promote ara/flhDC to a confident class while their primary regulators are unmodeled.

## Integration (what changed in the parser)

- `CRP_CAP` added to `CUSTOM_PWM_MOTIF_IDS`.
- `CUSTOM_PWM_PVALUE_THRESHOLDS = {"CRP_CAP": 1e-4}` — CRP hits count as confident /
  eligible evidence only at the locked p ≤ 1e-4 (not the generic 0.05). This is what keeps
  the sub-threshold lacO-overlap CAP site (p ≈ 3.1e-4) out of the evidence set.
- Non-repressor site filter now uses the confidence function, so custom-PWM activators
  survive by their p-value (custom q-values ≈ 1 would otherwise drop CRP at the q ≤ 0.05 cap).
- **Lone-activator honesty guard:** an AND-only result (has_and, no NOT) supported *solely*
  by a single activator paired with non-regulator sites resolves to `INSUFFICIENT_EVIDENCE`
  with a "primary regulator unmodeled" note. Genuinely combinatorial AND evidence
  (≥2 distinct identified regulators, or a regulator–regulator AND) is not suppressed.
- JSON now records `gate_flag_class` and `gate_flag_downgraded` for transparency.

`crp_cap.meme` was wired into the `custom_pwm_files` of the lac, ara, and flhDC completed
manifests (Jetson runtime; `queue/completed/` is gitignored). The 5 non-CRP circuits were
left untouched.

## Environment findings (material — the git clone was not a runnable pipeline)

Running the harness on the Jetson git clone (`/media/sdcard/glmp/.../dna-decoder`) at the
Stage 1 commit exposed gaps that had to be fixed before any honest baseline was possible:

- `motifs/JASPAR2024_CORE_non-redundant_pfms_meme.txt` was **missing** from the clone
  (untracked, ~1.2 MB). Symlinked from `/media/sdcard/decoder/motifs/` for runtime.
- `motifs/laci_motif.meme` was **not in git at all** — present only in the separate non-git
  tree `/media/sdcard/decoder/motifs/`. It contains **both** `LacI_lacO1` (crude, nsites=1)
  **and** `TrpR_trpO` (nsites=5). Without it, the lac and trp custom-PWM scans were silently
  skipped. **This file is now tracked** (with the LacI nsites=1 quality caveat below).
- Jetson default `python3` is 3.6 (crashes on `capture_output`); the harness must run under
  `meme-env` Python 3.11 (`/media/sdcard/miniforge3/envs/meme-env/bin/python`), which also
  provides FIMO as a sibling binary.

**Consequence:** the harness's hard-coded `old_class` reference values (e.g. lac=II,
sos=II) came from the older non-git `/media/sdcard/decoder/` runs and are **stale**. The
honest BEFORE below is a fresh re-decode of the git-tracked pipeline with LacI/TrpR/LexA
present and **no CRP**.

## BEFORE / AFTER — `dna_topology_class`

Both runs 2026-07-08, Jetson, `meme-env` Python. BEFORE = parser `fc7ee42`, LacI/TrpR/LexA
present, no CRP. AFTER = parser `69e3120` (v0.2.3), CRP integrated.

| circuit | BEFORE | AFTER | Δ | glmp_biological_class (unchanged) |
|---|---|---|---|---|
| **ecoli_lac_operon** | I/II | **II** | **MOVED** | II |
| **ecoli_flhdc_flagellar** | INSUFFICIENT_EVIDENCE | **INDETERMINATE** | **MOVED** | I |
| ecoli_ara_operon | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | — | III |
| ecoli_trp_operon | I/II | I/II | — | II |
| ecoli_sos_lexa | I/II | I/II | — | II |
| ecoli_sos_reca | I/II | I/II | — | II |
| ecoli_lambda_switch | INSUFFICIENT_EVIDENCE | INSUFFICIENT_EVIDENCE | — | III |
| ecoli_dna_damage_checkpoint | I/II | I/II | — | II |

All 8 `glmp_biological_class` values are `curated_catalog` and **unchanged** (manifest-only
field; the parser never derives it from FIMO). The 5 non-CRP circuits are **unchanged**.

## Moved circuits — driving evidence

### ecoli_lac_operon → Class II (confidence: high) — **PROVISIONAL**

- **CRP AND driver:** the single CRP site passing p ≤ 1e-4 is the **canonical lacZp1 CAP
  site** at pos **252–273 (−), p = 7.34e-06**, matched `TAATGTGAGTTAGCTCACTCAT`. It forms an
  AND (cooperative-spacing) gate at **d = 42 bp** with cooperating sites in the −35/−10 region.
- **NOT driver:** `LacI_lacO1` operator hits (420 eligible NOT gates) overlapping the RNAP
  region → NOT gate. Class II = **LacI NOT + canonical CRP AND**, exactly the expected topology.
- **lacO-overlap CAP site correctly excluded:** the RegulonDB CRP row overlapping lacO
  (`AATTGTGAGCGGATAACAATTT`, pos 1–22 / 180–201) scores **p ≈ 3.1e-4** — sub-threshold, and
  is **not** the driver. `gate_flag_downgraded = False`; `proposed_class = II`.
- **Why PROVISIONAL:** biologist to confirm (a) the canonical lacZp1 CAP site is the intended
  Class II driver, and (b) the lacO/CRP overlap disposition. The tracked LacI PWM is a crude
  single-site consensus (nsites = 1), adequate as a NOT-gate presence detector but not a
  quantitative operator model.

### ecoli_flhdc_flagellar → INDETERMINATE (confidence: insufficient) — no class claimed

- CRP is confidently detected (strongest hit pos **1979113–1979134 (+), p = 3.11e-07**; two
  further hits at p = 7.4e-5 and 9.1e-5, all ≤ 1e-4).
- **But** every CRP gate is `OR_INDEPENDENT` (distance ≈ 446–448 bp from the nearest eligible
  site) — independent action, no NOT/AND to resolve a topology. Result: `INDETERMINATE`
  ("confident identified-regulator gate present but does not resolve to a GLMP class").
- **Honesty:** `proposed_class = None`; `dna_topology_confidence = insufficient`. This is
  **not** a Class I claim. flhDC's primary regulator (the flhDC master operon's own
  activation cascade) is unmodeled, and the decoder does not pretend otherwise. Label changed
  from INSUFFICIENT_EVIDENCE only because CRP is now genuinely detected — it is the honest,
  non-committal state, not an over-claim.

### ecoli_ara_operon → INSUFFICIENT_EVIDENCE (unchanged) — no over-claim

- CRP is detected at **p = 3.21e-05** (passes the locked threshold) but is isolated: it forms
  **no eligible AND** with another identified regulator within the 15–50 bp cooperative
  window (`has_and = False`, `has_not = False`). AraC is unmodeled.
- Result stays `INSUFFICIENT_EVIDENCE`. The lone-activator guard was not even needed here (no
  AND gate formed at all), but it remains the backstop had CRP landed 15–50 bp from a
  non-regulator site.

## Over-claims caught / prevented

- **flhDC** carries a very strong CRP hit (p = 3.11e-07). On naïve spacing geometry a future
  in-range partner could have promoted it to Class I. It resolves to INDETERMINATE (no class),
  and the lone-activator guard would additionally block any AND-only Class I.
- **ara** CRP (p = 3.21e-05) did not promote to Class I — no eligible cooperative AND partner.
- Neither moved circuit's `glmp_biological_class` changed; the two-field schema keeps the
  sequence-only DNA-decode claim separate from the curated biological class.

## Artifacts

- Parser: `glmp_logic_parser.py` v0.2.3 (`69e3120`)
- Registry: `motifs/custom_pwm_registry.yaml` — CRP `active`, locked p ≤ 1e-4
- Tracked motif: `motifs/laci_motif.meme` (LacI_lacO1 + TrpR_trpO)
- Manifest wiring helper: `scripts/wire_crp_manifests.sh`
- Result JSONs (gitignored raw FIMO): `results/*_logic_20260708.json`,
  `results/regression_redecode_20260708.json`

## Open questions for Gary / biologist

1. **lac Class II sign-off:** confirm canonical lacZp1 CAP site as the Class II driver and the
   lacO/CRP overlap disposition (sub-threshold exclusion at p ≤ 1e-4).
2. **LacI PWM quality:** replace the nsites=1 LacI consensus with a proper multi-site PWM?
3. **flhDC INDETERMINATE:** accept as the honest label, or prefer INSUFFICIENT_EVIDENCE until
   the flhDC primary regulator is modeled?
4. **SOS reference drift:** fresh re-decode gives sos_lexa/sos_reca = I/II (NOT-only), not the
   stale II reference. Reconcile separately.
5. **JASPAR / pipeline provenance:** how should the git clone obtain the JASPAR CORE DB
   (runtime symlink vs GCS fetch vs tracked)?
