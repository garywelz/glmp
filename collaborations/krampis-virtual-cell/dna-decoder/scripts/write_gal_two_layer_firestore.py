#!/usr/bin/env python3
"""Backup and update yeast_gal_bistable_switch with two-layer DNA decode schema."""

import json
import sys
from datetime import datetime
from pathlib import Path

from google.cloud import firestore

PROJECT = "regal-scholar-453620-r7"
DATABASE = "copernicusai"
DOC_ID = "yeast_gal_bistable_switch"
BACKUP = Path(__file__).resolve().parent.parent / "results" / "gal_bistable_switch_backup_pre_dna_layer_20260630.json"

DNA_DECODABLE_LAYER = {
    "status": "partial",
    "decode_date": "2026-06-30",
    "decoded_elements": [
        "Gal4 UASg activator sites — 2 of 3 canonical cluster sites confirmed at q<=0.05"
    ],
    "binding_sites_found": [
        {
            "tf": "GAL4",
            "jaspar_id": "MA0299.1",
            "genomic_position": "278587-278601",
            "strand": "+",
            "q_value": 0.0014,
            "matched_sequence": "CGGGCGACAGCCCTC",
            "maps_to_uasg_site": 2,
        },
        {
            "tf": "GAL4",
            "jaspar_id": "MA0299.1",
            "genomic_position": "278607-278621",
            "strand": "-",
            "q_value": 0.0050,
            "matched_sequence": "CGGAGGAGAGTCTTC",
            "maps_to_uasg_site": 3,
        },
    ],
    "circuit_class_at_dna_level": "I",
    "circuit_class_dna_level_note": (
        "Activator binding sites only; no repression geometry detectable at "
        "DNA level for this circuit"
    ),
    "sequence_source": "SGD S000000224, S. cerevisiae S288C, Chr II 278021-281607",
    "fasta_file": "dna-decoder/sequences/gal1_promoter_1kb.fa",
    "decode_result_file": "dna-decoder/results/gal1_promoter_logic.json",
    "known_limitation": (
        "Raw parser run also produced spurious Class II classification from MIG1 "
        "motif noise and non-validated repressor-distance heuristics. This result "
        "was REJECTED as a known false positive. See protein_network_layer for "
        "the validated circuit class."
    ),
    "organism_db": "ecoli_only",
    "organism_db_note": (
        "Parser TF lists were extended with GAL4/MA0299.1 and MIG1/MA0337.2 for "
        "this decode but promoter geometry (RNAP_BINDING_REGION) still uses "
        "prokaryotic -35/-10 assumptions. Yeast-specific promoter geometry "
        "(TATA/Inr) not yet implemented."
    ),
}

PROTEIN_NETWORK_LAYER = {
    "status": "curated_not_dna_decoded",
    "mechanism_summary": (
        "Gal3p (activated by galactose) sequesters Gal80p in the cytoplasm, "
        "relieving Gal80p repression of Gal4p's activation domain. Freed Gal4p "
        "activates GAL1, GAL3, and GAL2 transcription, creating positive "
        "feedback that produces bistability and hysteresis."
    ),
    "circuit_class": "IIIa",
    "circuit_class_name": "Bistable switch (protein-level positive feedback)",
    "not_gate": (
        "Gal80p represses Gal4p via protein-protein binding to the activation "
        "domain, not via DNA operator occupancy"
    ),
    "why_not_dna_decodable": (
        "The repression mechanism (Gal80-Gal4 protein binding) and induction "
        "mechanism (Gal3-Gal80 cytoplasmic sequestration) involve no DNA sequence "
        "motifs. Bistability and hysteresis are emergent population-level dynamics "
        "not encoded in any single promoter sequence."
    ),
    "source": "Curated description, GLMP v2 catalog",
    "validation_status": (
        "Pending Layer 1/2/3 review (Lents hand-review, RegulonDB-equivalent "
        "cross-reference, Evo2 cross-validation) per GLMP validation architecture"
    ),
}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    db = firestore.Client(project=PROJECT, database=DATABASE)
    ref = db.collection("glmp_processes").document(DOC_ID)
    doc = ref.get()
    if not doc.exists:
        raise SystemExit(f"Document {DOC_ID} not found")

    data = doc.to_dict()
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    BACKUP.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    print(f"Backed up to {BACKUP}")
    print(f"Current fields: {sorted(data.keys())}")

    if mode == "backup":
        return

    ref.update(
        {
            "dna_decodable_layer": DNA_DECODABLE_LAYER,
            "protein_network_layer": PROTEIN_NETWORK_LAYER,
            "two_layer_schema_added": "2026-06-30",
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
    )
    print(f"Updated {DOC_ID} with two-layer schema")

    if mode == "verify" or mode == "all":
        updated = ref.get().to_dict()
        print("\ndna_decodable_layer status:", updated.get("dna_decodable_layer", {}).get("status"))
        print("protein_network_layer status:", updated.get("protein_network_layer", {}).get("status"))
        print("Original fields still intact:")
        print(f"  mermaid present: {bool(updated.get('mermaid') or updated.get('mermaid_code'))}")
        print(f"  embedding present: {bool(updated.get('embedding'))}")
        print(f"  description present: {bool(updated.get('description'))}")


if __name__ == "__main__":
    main()
