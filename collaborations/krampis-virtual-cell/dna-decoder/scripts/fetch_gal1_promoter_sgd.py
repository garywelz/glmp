#!/usr/bin/env python3
"""Fetch GAL1 ±1 kb promoter window from SGD (S288C, S000000224)."""

import json
import textwrap
import urllib.request
from pathlib import Path

SGD_URL = "https://www.yeastgenome.org/backend/locus/S000000224/sequence_details"
OUTPUT = Path(__file__).resolve().parent.parent / "sequences" / "gal1_promoter_1kb.fa"


def main():
    with urllib.request.urlopen(SGD_URL, timeout=60) as resp:
        data = json.load(resp)

    for item in data["1kb"]:
        if item.get("strain", {}).get("display_name") == "S288C":
            seq = item["residues"]
            start, end = item["start"], item["end"]
            contig = item["contig"]["display_name"]
            strand = item["strand"]
            break
    else:
        raise SystemExit("S288C 1kb entry not found in SGD response")

    header = (
        f">gal1_promoter_1kb S288C GAL1 (SGD:S000000224) {contig}:{start}-{end} "
        f"strand={strand} SGD 1kb window (ORF +/- 1000bp, captures UASg)"
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    wrapped = "\n".join(textwrap.wrap(seq, width=80))
    OUTPUT.write_text(f"{header}\n{wrapped}\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} ({len(seq)} bp)")


if __name__ == "__main__":
    main()
