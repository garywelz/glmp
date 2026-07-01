#!/usr/bin/env python3
"""Fetch and write FASTA files for the first-batch queue manifests."""

import sys
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).parent
DECODER_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from genbank_fetch import fetch_from_manifest  # noqa: E402

BATCH_MANIFESTS = [
    "ecoli_flhdc_flagellar.yaml",
    "ecoli_sos_reca.yaml",
    "ecoli_sos_lexa.yaml",
    "ecoli_lambda_switch.yaml",
]


def main():
    pending = DECODER_DIR / "queue" / "pending"
    for name in BATCH_MANIFESTS:
        manifest_path = pending / name
        with open(manifest_path, encoding="utf-8") as f:
            manifest = yaml.safe_load(f)
        out = DECODER_DIR / manifest["sequence_file"]
        print(f"Fetching {manifest['circuit_id']} -> {out.name} ...")
        fetch_from_manifest(manifest, out)
        print(f"  Wrote {out} ({out.stat().st_size} bytes)")
    print("Done.")


if __name__ == "__main__":
    main()
