#!/usr/bin/env python3
"""Migrate yeast_gal_bistable_switch to canonical flat two-field schema."""

from google.cloud import firestore

PROJECT = "regal-scholar-453620-r7"
DATABASE = "copernicusai"
DOC_ID = "yeast_gal_bistable_switch"


def main():
    db = firestore.Client(project=PROJECT, database=DATABASE)
    ref = db.collection("glmp_processes").document(DOC_ID)
    ref.update({
        "dna_topology_class": "I",
        "dna_topology_note": (
            "Gal4 UASg activator sites only (2/3 at q<=0.05); "
            "no repression geometry decodable at DNA level"
        ),
        "dna_topology_confidence": "partial",
        "glmp_biological_class": "III",
        "glmp_biological_subclass": "IIIa",
        "glmp_biological_class_source": "curated_catalog",
        "glmp_biological_class_note": (
            "Bistable switch via Gal80/Gal3 protein sequestration — "
            "mechanism not DNA-encoded"
        ),
        "circuit_class": "I",
        "decoder_version": "v0.2.2",
        "updated_at": firestore.SERVER_TIMESTAMP,
    })
    print(f"Migrated flat fields on {DOC_ID}")


if __name__ == "__main__":
    main()
