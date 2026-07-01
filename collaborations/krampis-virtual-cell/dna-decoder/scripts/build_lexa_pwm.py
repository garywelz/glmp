#!/usr/bin/env python3
"""
build_lexa_pwm.py — Build LexA SOS box PWM from experimentally
validated binding site sequences.

Outputs a MEME-format motif file for use with FIMO.
"""

from __future__ import annotations

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DECODER_DIR = SCRIPT_DIR.parent
MOTIFS_DIR = DECODER_DIR / "motifs"

# Validated LexA SOS box sequences; Fernandez de Henestrosa et al. 2000.
# recA from ecoli_sos_reca.fa. Normalized to CTGT-N8-ACAG (16 bp) at build time.
LEXA_SITES = [
    ("recA", "CTGTATGAGCATACAG"),
    ("lexA", "CTGTATATATTTACAG"),
    ("uvrA", "CTGTATATACTCCACAG"),
    ("uvrB", "CTGTATAAATCCACAG"),
    ("uvrD", "CTGTAAAAATTTACAG"),
    ("sulA", "CTGTATATAAACCACAG"),
    ("dinB", "CTGTAAAGAAACACAG"),
    ("dinI", "CTGTATAAAACCACAG"),
    ("polB", "CTGTATATTTCACACAG"),
    ("ruvA", "CTGTATATAATCCACAG"),
    ("ssb", "CTGTATAATATCCACAG"),
    ("dinD", "CTGTATAAATCCACAG"),
    ("umuDC", "CTGTATATATACACAG"),
    ("ruvAB", "CTGTATATAAACCACAG"),
    ("recN", "CTGTATATAATCACAG"),
    ("ydjQ", "CTGTAAAGACCCACAG"),
    ("sbmC", "CTGTATAAATATACAG"),
    ("molR", "CTGTAAATAAAAACAG"),
    ("tisB", "CTGTATAAATCAACAG"),
    ("yebG", "CTGTATAAATCCACAG"),
    ("ftsK", "CTGTATATATATACAG"),
]

TARGET_LEN = 16
MOTIF_ID = "LexA_SOS_box"
MOTIF_NAME = "LexA SOS box repressor E. coli K-12"
OUTPUT_FILE = MOTIFS_DIR / "lexA_sos.meme"


def normalize_to_target(site: str, target_len: int = TARGET_LEN) -> str | None:
    """Align SOS boxes to CTGT-N8-ACAG (16 bp) by trimming one spacer base if 17 bp."""
    site = site.upper().strip()
    if not site.startswith("CTGT") or not site.endswith("ACAG"):
        return None
    if len(site) == target_len:
        return site
    if len(site) == target_len + 1:
        return site[:8] + site[9:]
    return None


def build_pfm(sites: list[str]) -> tuple[dict[str, list[int]], int]:
    if not sites:
        raise ValueError("No sites to build PFM from")
    length = len(sites[0])
    bases = ["A", "C", "G", "T"]
    pfm = {b: [0] * length for b in bases}
    for site in sites:
        for i, base in enumerate(site.upper()):
            if base in pfm:
                pfm[base][i] += 1
    return pfm, length


def pfm_to_ppm(pfm: dict[str, list[int]], n_sites: int, pseudocount: float = 0.1) -> dict[str, list[float]]:
    bases = ["A", "C", "G", "T"]
    denom = n_sites + 4 * pseudocount
    return {b: [(count + pseudocount) / denom for count in pfm[b]] for b in bases}


def write_meme(
    ppm: dict[str, list[float]],
    length: int,
    n_sites: int,
    output_file: Path,
    motif_id: str = MOTIF_ID,
    motif_name: str = MOTIF_NAME,
) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as f:
        f.write("MEME version 4\n\n")
        f.write("ALPHABET= ACGT\n\n")
        f.write("strands: + -\n\n")
        f.write("Background letter frequencies\n")
        f.write("A 0.25 C 0.25 G 0.25 T 0.25\n\n")
        f.write(f"MOTIF {motif_id} {motif_name}\n\n")
        f.write(
            f"letter-probability matrix: alength= 4 w= {length} "
            f"nsites= {n_sites} E= 0\n"
        )
        for pos in range(length):
            f.write(
                f"  {ppm['A'][pos]:.6f}  {ppm['C'][pos]:.6f}  "
                f"{ppm['G'][pos]:.6f}  {ppm['T'][pos]:.6f}\n"
            )
        f.write("\n")
    print(f"Written: {output_file}")
    print(f"Motif: {motif_id} ({motif_name}), width={length}, sites={n_sites}")


def validate_pwm(ppm: dict[str, list[float]], length: int) -> None:
    print("\nPWM validation:")
    print(f"  Width: {length} bp (CTGT-N8-ACAG)")
    print("  Expected: CTGT at positions 1-4, ACAG at positions 13-16")
    print()
    bases = ["A", "C", "G", "T"]
    for pos in range(length):
        dominant = max(bases, key=lambda b: ppm[b][pos])
        confidence = ppm[dominant][pos]
        if confidence > 0.6:
            flag = "OK"
        elif confidence > 0.4:
            flag = "WARN"
        else:
            flag = "LOW"
        print(f"  Position {pos + 1:2d}: {dominant} ({confidence:.2f}) [{flag}]")


def main() -> None:
    print(f"Building LexA SOS box PWM from {len(LEXA_SITES)} candidate sequences\n")

    labeled: list[tuple[str, str]] = []
    for gene, raw in LEXA_SITES:
        site = normalize_to_target(raw, target_len=TARGET_LEN)
        if site is None:
            print(f"  WARNING: {gene} site {raw!r} could not be normalized to {TARGET_LEN} bp — skipping")
            continue
        if site != raw:
            print(f"  Normalized {gene}: {raw} -> {site}")
        labeled.append((gene, site))
    sites = [seq for _, seq in labeled]
    print(f"Using {len(sites)} sequences after normalization\n")

    print("Aligned sequences:")
    for i, (gene, site) in enumerate(labeled, start=1):
        print(f"  {i:2d}. {gene:6s} {site}")

    pfm, length = build_pfm(sites)
    ppm = pfm_to_ppm(pfm, len(sites))
    validate_pwm(ppm, length)
    write_meme(ppm, length, len(sites), OUTPUT_FILE)

    print("\nDone. Test with:")
    print(
        f"  fimo --thresh 0.001 --oc results/test_lexa {OUTPUT_FILE} "
        "sequences/ecoli_sos_reca.fa"
    )


if __name__ == "__main__":
    main()
