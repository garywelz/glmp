#!/usr/bin/env python3
"""
Fast data preparation: reads h5ad sequentially in row chunks
instead of random-access per gene (10x faster).

Output:
  benchmark_data/k562_perturbation_means.npz
"""

import time
import numpy as np
import h5py
from pathlib import Path
from collections import defaultdict

DATA = Path("benchmark_data/ReplogleWeissman2022_K562_essential.h5ad")

def main():
    print("Fast perturbation means computation")
    print("=" * 50)

    f = h5py.File(str(DATA), "r")
    X = f["X"]
    n_cells, n_genes = X.shape
    print(f"Matrix: {n_cells:,} × {n_genes:,}")

    codes = f["obs"]["gene"]["codes"][:]
    cats_raw = f["obs"]["gene"]["categories"][:]
    cats = [c.decode() for c in cats_raw]

    var_key = f["var"].attrs.get("_index", "gene_name")
    var_names = [v.decode() if isinstance(v, bytes) else v
                 for v in f["var"][var_key][:]]

    nt_idx = cats.index("non-targeting")

    # Accumulators for each perturbation group
    gene_sums = defaultdict(lambda: np.zeros(n_genes, dtype=np.float64))
    gene_counts = defaultdict(int)
    ctrl_sum = np.zeros(n_genes, dtype=np.float64)
    ctrl_count = 0

    # Read sequentially in large chunks (fast!)
    chunk_size = 5000
    t0 = time.time()

    for start in range(0, n_cells, chunk_size):
        end = min(start + chunk_size, n_cells)
        chunk = X[start:end]  # reads contiguous block = fast
        chunk_codes = codes[start:end]

        for local_i in range(end - start):
            code = chunk_codes[local_i]
            if code == nt_idx:
                ctrl_sum += chunk[local_i]
                ctrl_count += 1
            else:
                gene_name = cats[code]
                gene_sums[gene_name] += chunk[local_i]
                gene_counts[gene_name] += 1

        elapsed = time.time() - t0
        pct = end / n_cells * 100
        rate = end / elapsed
        eta = (n_cells - end) / rate if rate > 0 else 0
        if end % 50000 < chunk_size:
            print(f"  {end:>7,}/{n_cells:,} ({pct:.0f}%)  "
                  f"{elapsed:.0f}s elapsed, ~{eta:.0f}s remaining")

    f.close()

    # Compute means
    ctrl_mean = (ctrl_sum / ctrl_count).astype(np.float32)
    print(f"\nControl cells: {ctrl_count:,}")
    print(f"Perturbation targets: {len(gene_sums)}")

    gene_names = sorted(gene_sums.keys())
    pert_means = np.array([(gene_sums[g] / gene_counts[g]).astype(np.float32) for g in gene_names])
    counts = np.array([gene_counts[g] for g in gene_names])

    out_path = Path("benchmark_data/k562_perturbation_means.npz")
    np.savez_compressed(
        str(out_path),
        ctrl_mean=ctrl_mean,
        gene_names=np.array(gene_names),
        pert_means=pert_means,
        pert_counts=counts,
        var_names=np.array(var_names),
    )
    print(f"\nSaved {out_path} ({out_path.stat().st_size/1e6:.1f} MB)")
    print(f"Total time: {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
