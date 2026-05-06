# Benchmark data (not in Git)

Large Replogle K562 Perturb-seq and derived files live **only on your machine**. Clone this repo, create this directory if needed, then download or generate the files below.

## 1. `ReplogleWeissman2022_K562_essential.h5ad` (~1.5 GB)

Primary AnnData for most K562 scripts and notebooks.

**Option A — Zenodo (direct file URL, used in several notebooks):**

https://zenodo.org/records/7041849/files/ReplogleWeissman2022_K562_essential.h5ad?download=1

**Option B — Figshare (dataset landing page):**

https://plus.figshare.com/articles/dataset/Mapping_information-rich_genotype-phenotype_landscapes_with_genome-scale_Perturb-seq/20029387

**Example (save into this folder):**

```bash
cd k562-empirical-sequel/benchmark_data
curl -L -o ReplogleWeissman2022_K562_essential.h5ad \
  'https://zenodo.org/records/7041849/files/ReplogleWeissman2022_K562_essential.h5ad?download=1'
```

*(Alternative mirror used in some Colab code:* `https://zenodo.org/api/records/10044268/files/ReplogleWeissman2022_K562_essential.h5ad/content` *)*

## 2. `k562_control_cells.h5ad` and `k562_perturbation_means.npz` (derived)

These are **generated** from the essential `.h5ad` for CellOracle / fast path workflows:

From repository root:

```bash
python3 k562-empirical-sequel/scripts/prepare_celloracle_data.py
# and/or (depending on your pipeline)
python3 k562-empirical-sequel/scripts/prepare_data_fast.py
```

After that, expect the two files under `k562-empirical-sequel/benchmark_data/`.

## Git

Patterns `*.h5ad` and `*.npz` in this directory are **gitignored** so normal `git push` stays code-sized.
