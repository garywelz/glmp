#!/usr/bin/env python3
"""
Map top 5 H1 persistent loops to specific GLMP processes using Ripser cocycles.
"""

import numpy as np
import pandas as pd
from ripser import ripser
from sklearn.preprocessing import StandardScaler

def main():
    df = pd.read_csv("glmp_features.csv")
    num_cols = ["node_count", "conditional_count", "or_gates", "and_gates", "not_gates"]
    X = StandardScaler().fit_transform(df[num_cols].fillna(0).astype(float))

    # Run Ripser with cocycles to get which vertices form each H1 loop
    result = ripser(X, maxdim=2, do_cocycles=True)

    dgms = result["dgms"]
    cocycles = result["cocycles"]
    h1 = dgms[1]
    h1_cycles = cocycles[1]

    # Sort H1 by persistence (death - birth) descending, get top 5
    persistences = h1[:, 1] - h1[:, 0]
    top5_idx = np.argsort(-persistences)[:5]

    # Known feedback circuits (from biological literature)
    feedback_keywords = [
        "lac_operon", "trp_operon", "ara_operon",
        "two_component", "signal_transduction", "chemotaxis",
        "sos", "heat_shock", "stress_response", "dna_damage",
        "cell_cycle", "biofilm", "stringent", "catabolite"
    ]

    def has_feedback(process_id):
        pid = process_id.lower()
        return any(kw in pid for kw in feedback_keywords)

    rows = []
    for rank, idx in enumerate(top5_idx, 1):
        birth, death = h1[idx, 0], h1[idx, 1]
        pers = persistences[idx]
        cocycle = h1_cycles[idx]

        # Cocycle format: each row [v0, v1, coeff] for edge (v0,v1)
        vertices = set()
        if cocycle.ndim == 2:
            for row in cocycle:
                vertices.add(int(row[0]))
                vertices.add(int(row[1]))
        else:
            vertices = set(cocycle.astype(int).tolist())

        process_names = [df.iloc[i]["process_name"] for i in sorted(vertices)]
        process_ids = [df.iloc[i]["process_id"] for i in sorted(vertices)]
        organisms = [df.iloc[i]["organism"] for i in sorted(vertices)]
        categories = [df.iloc[i]["category"] for i in sorted(vertices)]

        n_feedback = sum(1 for pid in process_ids if has_feedback(pid))

        rows.append({
            "rank": rank,
            "birth": birth,
            "death": death,
            "persistence": pers,
            "n_processes": len(vertices),
            "process_names": process_names,
            "process_ids": process_ids,
            "organisms": organisms,
            "categories": categories,
            "n_feedback": n_feedback,
        })

    return rows, df, feedback_keywords


if __name__ == "__main__":
    rows, df, _ = main()
    import json
    out = []
    for r in rows:
        out.append({
            "rank": r["rank"],
            "birth": float(r["birth"]),
            "death": float(r["death"]),
            "persistence": float(r["persistence"]),
            "n_processes": r["n_processes"],
            "process_names": r["process_names"],
            "process_ids": r["process_ids"],
            "organisms": list(set(r["organisms"])),
            "categories": list(set(r["categories"])),
            "n_feedback": r["n_feedback"],
        })
    with open("h1_loop_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("Saved h1_loop_results.json")
