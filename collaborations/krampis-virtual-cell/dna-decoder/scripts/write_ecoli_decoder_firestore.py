#!/usr/bin/env python3
"""Write first Firestore decoder entries for ecoli lac/ara/trp operons."""

import json
import sys
from pathlib import Path

from google.cloud import firestore

PROJECT = "regal-scholar-453620-r7"
DATABASE = "copernicusai"
DECODER_DIR = Path(__file__).resolve().parent.parent

CIRCUITS = [
    ("ecoli_lac_operon", "results/lac_operon_logic_v2.json"),
    ("ecoli_ara_operon", "results/ara_operon_logic_v3.json"),
    ("ecoli_trp_operon", "results/trp_operon_logic_v4.json"),
]


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "write"
    db = firestore.Client(project=PROJECT, database=DATABASE)

    if mode == "verify":
        for doc_id in [c[0] for c in CIRCUITS]:
            data = db.collection("glmp_processes").document(doc_id).get().to_dict()
            print(f"\n{doc_id}:")
            print(f"  dna_topology_class: {data.get('dna_topology_class')}")
            print(f"  glmp_biological_class: {data.get('glmp_biological_class')}")
            print(f"  circuit_class: {data.get('circuit_class')}")
            print(f"  original mermaid intact: {bool(data.get('mermaid') or data.get('mermaid_code'))}")
        return

    for circuit_id, result_rel in CIRCUITS:
        result_path = DECODER_DIR / result_rel
        if not result_path.exists():
            raise SystemExit(f"Missing decode result: {result_path}")
        with open(result_path, encoding="utf-8") as f:
            result = json.load(f)

        update = {
            "dna_topology_class": result.get("dna_topology_class"),
            "dna_topology_note": result.get("dna_topology_note"),
            "dna_topology_confidence": result.get("dna_topology_confidence"),
            "glmp_biological_class": result.get("glmp_biological_class"),
            "glmp_biological_subclass": result.get("glmp_biological_subclass"),
            "glmp_biological_class_source": result.get("glmp_biological_class_source"),
            "glmp_biological_class_note": result.get("glmp_biological_class_note"),
            "circuit_class": result.get("circuit_class"),
            "decoder_version": "v0.2.2",
            "decode_date": "2026-06-30",
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
        db.collection("glmp_processes").document(circuit_id).update(update)
        print(f"Updated {circuit_id}")


if __name__ == "__main__":
    main()
