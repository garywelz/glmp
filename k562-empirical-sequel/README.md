# K562 empirical sequel (GLMP)

Working paper HTML, Colab notebooks, and Python scripts for the K562 Perturb-seq class-stratified analysis. **Tabulated results and figures** live in the repository root [`../results/`](../results/).

## Layout

| Path | Contents |
|------|----------|
| `empirical_sequel_draft_v2.html` | Empirical sequel (working paper) |
| `scripts/` | Merge, meta-analysis, GRN propagation, bimodality, DE helpers |
| `STATE_K562_Benchmark_v4.ipynb` | STATE inference (Colab) |
| `STATE_Rescore_DE20.ipynb` | DE20 re-scoring (Colab) |
| `../results/*.tsv` | Per-gene scores, merged benchmark, bimodality, etc. |
| `../gene_circuit_classes.tsv` | GLMP circuit class (I–V) per benchmark gene |
| `benchmark_data/` | **Local only** — Replogle `.h5ad` and derived `.npz` (see [`benchmark_data/README.md`](benchmark_data/README.md)) |

## Re-running analyses

From the **repository root** (`glmp/`):

```bash
python3 k562-empirical-sequel/scripts/merge_state_results.py
python3 k562-empirical-sequel/scripts/merge_state_de20_results.py
python3 k562-empirical-sequel/scripts/merge_hypothesis2_meta.py
python3 k562-empirical-sequel/scripts/run_celloracle_grammar_advantage.py
python3 k562-empirical-sequel/scripts/run_bimodality_analysis.py
```

`run_grn_propagation.py` additionally expects `benchmark_data/ReplogleWeissman2022_K562_essential.h5ad` and `regulatory_data/trrust_rawdata.human.tsv` under the working directory (not shipped in this repo due to size); obtain the h5ad from [Figshare](https://plus.figshare.com/articles/dataset/Mapping_information-rich_genotype-phenotype_landscapes_with_genome-scale_Perturb-seq/20029387) and TRRUST from the Han et al. supplement.

Large intermediate CellOracle artifacts (`*.pkl`, `*.npy` in `results/`) are omitted from Git; scores are in `results/celloracle_k562_per_gene_scores.tsv`.
