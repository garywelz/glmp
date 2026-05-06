#!/usr/bin/env python3
"""
Memory-efficient data preparation for CellOracle.
Extracts control cells and computes per-perturbation mean expression
without ever loading the full dense matrix.

Output:
  benchmark_data/k562_control_cells.h5ad    (~40 MB, for CellOracle GRN)
  benchmark_data/k562_perturbation_means.npz (per-gene mean expression for scoring)
"""

import sys
import time
import numpy as np
import h5py
from pathlib import Path

DATA = Path("benchmark_data/ReplogleWeissman2022_K562_essential.h5ad")
OUT_DIR = Path("benchmark_data")


def main():
    print("=" * 60)
    print("Memory-Efficient Data Preparation for CellOracle")
    print("=" * 60)

    f = h5py.File(str(DATA), "r")
    X = f["X"]  # shape (310385, 8563), chunked, NOT loaded into memory
    n_cells, n_genes = X.shape
    print(f"Full matrix: {n_cells:,} cells × {n_genes:,} genes")

    # Decode gene perturbation labels
    codes = f["obs"]["gene"]["codes"][:]
    cats = f["obs"]["gene"]["categories"][:]
    cats_dec = [c.decode() for c in cats]

    # Decode variable (gene) names
    if "var" in f and "_index" in f["var"]:
        var_names = [v.decode() if isinstance(v, bytes) else v for v in f["var"]["_index"][:]]
    else:
        var_names = [f"gene_{i}" for i in range(n_genes)]

    # Identify control cells
    nt_idx = cats_dec.index("non-targeting")
    control_mask = codes == nt_idx
    control_indices = np.where(control_mask)[0]
    print(f"Control cells: {len(control_indices):,}")

    # Step 1: Extract control cells (read in chunks to save memory)
    print("\nExtracting control cells...")
    t0 = time.time()
    chunk_size = 1000
    control_data = np.zeros((len(control_indices), n_genes), dtype=np.float32)

    for start in range(0, len(control_indices), chunk_size):
        end = min(start + chunk_size, len(control_indices))
        idx_chunk = sorted(control_indices[start:end])
        control_data[start:end] = X[idx_chunk]
        if (start + chunk_size) % 5000 == 0:
            print(f"  {start + chunk_size:,}/{len(control_indices):,} control cells read")

    print(f"  Done in {time.time()-t0:.1f}s")
    print(f"  Control data shape: {control_data.shape}, size: {control_data.nbytes/1e6:.0f} MB")

    # Save control cells as a lightweight h5ad-compatible file
    import scipy.sparse as sp
    ctrl_sparse = sp.csr_matrix(control_data)
    del control_data

    # Write minimal h5ad for CellOracle
    ctrl_path = OUT_DIR / "k562_control_cells.h5ad"
    write_minimal_h5ad(ctrl_path, ctrl_sparse, var_names, n_ctrl=len(control_indices))
    print(f"  Saved {ctrl_path} ({ctrl_path.stat().st_size/1e6:.1f} MB)")

    # Step 2: Compute control mean (for scoring later)
    ctrl_mean = np.array(ctrl_sparse.mean(axis=0)).flatten()

    # Step 3: Compute per-perturbation mean expression (streaming)
    print("\nComputing per-perturbation mean expression...")
    t0 = time.time()
    pert_means = {}
    pert_counts = {}

    perturbation_groups = {}
    for i, code in enumerate(codes):
        gene_name = cats_dec[code]
        if gene_name == "non-targeting":
            continue
        if gene_name not in perturbation_groups:
            perturbation_groups[gene_name] = []
        perturbation_groups[gene_name].append(i)

    print(f"  {len(perturbation_groups)} perturbation targets")

    batch_size = 500  # read this many cells at a time from h5py
    done = 0
    for gene_name, indices in perturbation_groups.items():
        indices = sorted(indices)
        n = len(indices)

        gene_sum = np.zeros(n_genes, dtype=np.float64)
        for start in range(0, n, batch_size):
            end = min(start + batch_size, n)
            chunk_indices = indices[start:end]
            chunk_data = X[chunk_indices]
            gene_sum += chunk_data.sum(axis=0)

        pert_means[gene_name] = (gene_sum / n).astype(np.float32)
        pert_counts[gene_name] = n

        done += 1
        if done % 200 == 0:
            print(f"  {done}/{len(perturbation_groups)} genes processed")

    print(f"  Done in {time.time()-t0:.1f}s")

    # Save perturbation means
    means_path = OUT_DIR / "k562_perturbation_means.npz"
    np.savez_compressed(
        str(means_path),
        ctrl_mean=ctrl_mean,
        gene_names=np.array(list(pert_means.keys())),
        pert_means=np.array(list(pert_means.values())),
        pert_counts=np.array(list(pert_counts.values())),
        var_names=np.array(var_names),
    )
    print(f"  Saved {means_path} ({means_path.stat().st_size/1e6:.1f} MB)")

    f.close()
    print("\nDone! Ready for CellOracle.")


def write_minimal_h5ad(path, X_sparse, var_names, n_ctrl):
    """Write a minimal h5ad file that scanpy/CellOracle can read."""
    import h5py
    import scipy.sparse as sp

    with h5py.File(str(path), "w") as out:
        # Store as CSR sparse
        g = out.create_group("X")
        g.attrs["encoding-type"] = "csr_matrix"
        g.attrs["encoding-version"] = "0.1.0"
        g.attrs["shape"] = X_sparse.shape
        g.create_dataset("data", data=X_sparse.data, compression="gzip")
        g.create_dataset("indices", data=X_sparse.indices, compression="gzip")
        g.create_dataset("indptr", data=X_sparse.indptr, compression="gzip")

        # obs (cell metadata)
        obs = out.create_group("obs")
        obs.attrs["encoding-type"] = "dataframe"
        obs.attrs["encoding-version"] = "0.2.0"
        obs.attrs["_index"] = "_index"
        obs.attrs["column-order"] = np.array(["cell_type"], dtype="S")
        obs.create_dataset("_index", data=np.array([f"ctrl_{i}" for i in range(n_ctrl)], dtype="S20"))

        # cell_type as categorical
        ct = obs.create_group("cell_type")
        ct.attrs["encoding-type"] = "categorical"
        ct.attrs["encoding-version"] = "0.2.0"
        ct.attrs["ordered"] = False
        ct.create_dataset("categories", data=np.array(["K562"], dtype="S10"))
        ct.create_dataset("codes", data=np.zeros(n_ctrl, dtype=np.int8))

        # var (gene metadata)
        var = out.create_group("var")
        var.attrs["encoding-type"] = "dataframe"
        var.attrs["encoding-version"] = "0.2.0"
        var.attrs["_index"] = "_index"
        var.attrs["column-order"] = np.array([], dtype="S1")
        var.create_dataset("_index", data=np.array(var_names, dtype="S30"))


if __name__ == "__main__":
    main()
