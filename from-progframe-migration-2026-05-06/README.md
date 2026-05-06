# Files migrated from `progframe` (2026-05-06)

This folder holds material moved out of the [progframe](https://github.com/garywelz/progframe) repository so **GLMP / K562 / empirical-sequel** artifacts live under `glmp`.

## Layout

- **`duplicates/`** — Copies from `progframe` that were **byte-identical** to files already in this repo. Kept for audit; canonical copies remain in `k562-empirical-sequel/scripts/`, `k562-empirical-sequel/notebooks` (where applicable), and `results/`.
- **`snapshots/`** — Files that **differed** from the current canonical version in `glmp` (e.g. `gene_circuit_classes.tsv` vs root `gene_circuit_classes.tsv`). Resolve or discard after comparison.
- **`reference-downloads/`** — Non-code reference exports (e.g. Hugging Face GLMP Space PDF).

## Integrated into the repo tree

Unique notebooks, scripts, data, and docs from `progframe` were moved into:

- `k562-empirical-sequel/` — `regulatory_data/`, `scPerturBench_Results/` (local CSVs gitignored), extra notebooks, `classify_circuits.py`, markdown guides, and `benchmark_data/README.md` (large `.h5ad`/`.npz` stay **local** per that README).
- `k562-empirical-sequel/scripts/` — Scripts that existed only under `progframe` root (e.g. `run_state_k562.py`, `prepare_celloracle_data.py`).
- `results/` — `celloracle_gene_names.npy` only in Git; **`celloracle_grn_coefficients.pkl`** is gitignored (regenerate locally).

The [Programming Framework](https://github.com/garywelz/progframe) static site and math/chemistry tooling stay in **progframe**; this migration targeted the empirical / K562 / GLMP analysis stack.

**Note:** `k562-empirical-sequel/scPerturBench_Results/` was copied on disk from progframe, but most files are `*.csv` and this repo’s `.gitignore` ignores CSVs under that tree — they remain local-only unless you add an exception or use Git LFS for large benchmarks.
