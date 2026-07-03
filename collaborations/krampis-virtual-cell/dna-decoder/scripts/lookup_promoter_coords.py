#!/usr/bin/env python3
"""
lookup_promoter_coords.py
Parses RegulonDB PromoterSet.tsv to find TSS positions for
the 10 failed E. coli manifests.
"""

import csv
from collections import defaultdict
from pathlib import Path

PROMOTER_FILE = Path(r"C:\Users\garyw\Downloads\PromoterSet.tsv")

# Key genes to look up per circuit (manifest process_id keys)
CIRCUIT_GENES = {
    "ecoli_aerobic_respiration": ["arcA", "fnr", "cyoA", "cydA"],
    "ecoli_amino_acid_biosynthesis": ["trpR", "argR", "leuO", "ilvC"],
    "ecoli_anaerobic_respiration": ["fnr", "narL", "narG", "arcA"],
    "ecoli_antibiotic_efflux_pumps": ["marA", "soxS", "rob", "acrA"],
    "ecoli_arginine_biosynthesis": ["argR", "carA", "carB", "argC"],
    "ecoli_base_excision_repair": ["mutM", "mutY", "nth", "xthA"],
    "ecoli_catabolite_repression": ["crp", "cyaA", "cya"],
    "ecoli_cold_shock_response": ["cspA", "cspB", "cspC", "cspE"],
    "ecoli_dna_damage_checkpoint": ["lexA", "recA", "sulA", "umuD"],
    "ecoli_e._coli_osmotic_stress_response": ["ompR", "envZ", "ompC", "ompF"],
}

GENE_COLUMNS = (
    "7)firstGeneName",
    "firstGeneName",
    "firstGene",
    "gene",
    "geneName",
)
TSS_COLUMNS = ("4)posTSS", "posTSS", "pos+1", "tss", "promoterPos", "position")
STRAND_COLUMNS = ("3)strand", "strand", "direction")
NAME_COLUMNS = ("2)name", "name", "promoterName")
SIGMA_COLUMNS = ("5)sigmaFactor", "sigmaFactor", "sigma")
CONF_COLUMNS = ("15)confidenceLevel", "confidenceLevel")


def _get(row: dict, candidates: tuple[str, ...]) -> str:
    for key in candidates:
        if key in row and row[key]:
            return str(row[key]).strip()
    return ""


def parse_promoters(filepath: Path) -> dict[str, list[dict]]:
    """Parse RegulonDB PromoterSet.tsv and return promoter records by gene."""
    promoters: dict[str, list[dict]] = defaultdict(list)

    with open(filepath, encoding="utf-8", errors="ignore") as f:
        lines = [line for line in f if not line.startswith("#")]

    reader = csv.DictReader(lines, delimiter="\t")
    print(f"Columns found: {reader.fieldnames}\n")

    for row in reader:
        gene = _get(row, GENE_COLUMNS).lower()
        tss_pos = _get(row, TSS_COLUMNS)
        if not gene or not tss_pos:
            continue

        promoters[gene].append(
            {
                "promoter": _get(row, NAME_COLUMNS),
                "tss": tss_pos,
                "strand": _get(row, STRAND_COLUMNS),
                "sigma": _get(row, SIGMA_COLUMNS),
                "confidence": _get(row, CONF_COLUMNS),
            }
        )

    return promoters


def main() -> None:
    print(f"Parsing {PROMOTER_FILE}...\n")
    promoters = parse_promoters(PROMOTER_FILE)
    print(f"Total genes with promoter data: {len(promoters)}\n")

    print("=" * 70)
    print("COORDINATE LOOKUP RESULTS")
    print("=" * 70)

    circuits_with_data = 0
    circuits_without_data = 0

    for circuit, genes in CIRCUIT_GENES.items():
        print(f"\n--- {circuit} ---")
        found_any = False

        for gene in genes:
            matches = promoters.get(gene.lower(), [])
            if matches:
                found_any = True
                # Prefer Confirmed, then Strong; stable sort by TSS
                ranked = sorted(
                    matches,
                    key=lambda m: (
                        0 if m["confidence"] == "Confirmed" else 1 if m["confidence"] == "Strong" else 2,
                        int(m["tss"]) if m["tss"].isdigit() else 0,
                    ),
                )
                for m in ranked[:2]:
                    print(
                        f"  {gene}: TSS={m['tss']} strand={m['strand']} "
                        f"promoter={m['promoter']} sigma={m['sigma']} "
                        f"confidence={m['confidence']}"
                    )

        if found_any:
            circuits_with_data += 1
        else:
            circuits_without_data += 1
            print(f"  WARNING: No promoter data found for genes: {genes}")

    print("\n" + "=" * 70)
    print(
        f"Summary: {circuits_with_data}/10 circuits had promoter data; "
        f"{circuits_without_data}/10 had no matches"
    )
    print("Done.")


if __name__ == "__main__":
    main()
