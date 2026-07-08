#!/usr/bin/env python3
"""Disambiguate LacI_lacO hits on lac promoter at locked threshold."""
import re
import subprocess
import sys
from pathlib import Path

DECODER = Path(__file__).resolve().parent.parent
MEME = DECODER / "motifs" / "laci_lacO.meme"
LAC_FA = DECODER / "sequences" / "lac_operon_region.fa"
OUT = DECODER / "_laci_pwm_validation" / "disambig_1e5"
THRESH = 1e-5

OPERATORS = {
    "lacO1": "AATTGTGAGCGGATAACAATT",
    "lacO2_genomic": "GGTTGTTACTCGCTCACATTT",
    "lacO3": "GGCAGTGAGCGCAACGCAATT",
}

# Genomic window (manifest ecoli_lac_operon)
WIN_START = 365394


def fimo_bin():
    for p in (
        Path("/media/sdcard/miniforge3/envs/meme-env/bin/fimo"),
        Path(sys.executable).parent / "fimo",
    ):
        if p.exists():
            return str(p)
    return "fimo"


def load_seq():
    lines = LAC_FA.read_text().splitlines()
    return "".join(l for l in lines if not l.startswith(">"))


def overlap_identity(hit_seq, op_seq):
    hit = hit_seq.upper().replace("U", "T")
    op = op_seq.upper()
    best = 0
    for i in range(len(hit) - len(op) + 1):
        w = hit[i : i + len(op)]
        best = max(best, sum(a == b for a, b in zip(w, op)))
    return best / len(op)


def classify_hit(matched, start, stop):
    matched = matched.upper()
    best_name, best_id = None, 0.0
    for name, op in OPERATORS.items():
        ident = overlap_identity(matched, op)
        if ident > best_id:
            best_id, best_name = ident, name
    g_start = WIN_START + int(start) - 1
    g_end = WIN_START + int(stop) - 1
    spurious = best_id < 0.75
    return {
        "operator_call": "spurious" if spurious else best_name,
        "identity": round(best_id, 3),
        "seq_start": int(start),
        "seq_stop": int(stop),
        "genomic": f"{g_start}-{g_end}",
        "matched_sequence": matched,
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cmd = [fimo_bin(), "--thresh", str(THRESH), "--oc", str(OUT), str(MEME), str(LAC_FA)]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    tsv = OUT / "fimo.tsv"
    rows = []
    with tsv.open() as fh:
        header = None
        for line in fh:
            if not line.strip():
                continue
            parts = line.strip().split("\t")
            if parts[0] == "motif_id":
                header = parts
                continue
            if header and len(parts) >= 10:
                r = dict(zip(header, parts))
                if r["motif_id"] != "LacI_lacO":
                    continue
                info = classify_hit(r["matched_sequence"], r["start"], r["stop"])
                rows.append({
                    "pvalue": float(r["p-value"]),
                    "score": float(r["score"]),
                    "strand": r["strand"],
                    **info,
                })
    rows.sort(key=lambda x: x["pvalue"])
    print(f"LacI_lacO hits at p<={THRESH}: {len(rows)}")
    for i, h in enumerate(rows, 1):
        print(
            f"  {i}. pos {h['seq_start']}-{h['seq_stop']} ({h['strand']}) "
            f"genomic {h['genomic']} p={h['pvalue']:.2e} "
            f"-> {h['operator_call']} (id={h['identity']}) "
            f"seq={h['matched_sequence']}"
        )
    real = [h for h in rows if h["operator_call"] != "spurious"]
    spur = [h for h in rows if h["operator_call"] == "spurious"]
    print(f"  Real operators: {len(real)} | Spurious: {len(spur)}")


if __name__ == "__main__":
    main()
