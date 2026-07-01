#!/usr/bin/env python3
"""Fetch genomic subsequence from NCBI nuccore by accession and coordinates."""

import re
import ssl
import textwrap
import time
import urllib.error
import urllib.request
from pathlib import Path

ENTREZ_EMAIL = "gwelz@gc.cuny.edu"
USER_AGENT = f"glmp-decoder/1.0 ({ENTREZ_EMAIL})"


def _ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_genomic_slice(
    accession: str,
    start: int,
    end: int,
    strand: str = "+",
    retries: int = 3,
) -> str:
    """Return FASTA sequence (single sequence string, uppercased)."""
    if start > end:
        raise ValueError(f"genomic start {start} > end {end}")
    strand_param = "2" if strand == "-" else "1"
    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        f"?db=nuccore&id={accession}&seq_start={start}&seq_stop={end}"
        f"&strand={strand_param}&rettype=fasta&retmode=text"
    )
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, context=_ssl_context(), timeout=120) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
            lines = raw.strip().splitlines()
            if not lines or not lines[0].startswith(">"):
                raise ValueError(f"Unexpected NCBI response for {accession}:{start}-{end}")
            seq = "".join(line.strip() for line in lines[1:]).upper()
            if not seq:
                raise ValueError(f"Empty sequence returned for {accession}:{start}-{end}")
            return seq
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError) as exc:
            last_err = exc
            time.sleep(1.0 + attempt)
    raise RuntimeError(f"NCBI fetch failed for {accession}:{start}-{end}: {last_err}")


def write_fasta(path: Path, header: str, sequence: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    wrapped = "\n".join(textwrap.wrap(sequence, width=80))
    path.write_text(f">{header}\n{wrapped}\n", encoding="utf-8")
    return path


def fetch_from_manifest(manifest: dict, output_path: Path) -> Path:
    region = manifest.get("genomic_region") or {}
    start = region.get("start")
    end = region.get("end")
    strand = region.get("strand", "+")
    accession = manifest.get("ncbi_accession", "")

    if not accession or accession == "TBD":
        raise ValueError(f"ncbi_accession is TBD for {manifest.get('circuit_id')}")
    if start is None or end is None:
        raise ValueError(f"genomic_region start/end required for {manifest.get('circuit_id')}")

    seq = fetch_genomic_slice(accession, int(start), int(end), strand)
    tss = region.get("tss")
    header = (
        f"{manifest['circuit_id']} {accession}:{start}-{end} strand={strand}"
        + (f" TSS={tss}" if tss else "")
        + f" {region.get('coordinates_source', '')[:120]}"
    )
    header = re.sub(r"\s+", " ", header).strip()
    return write_fasta(output_path, header, seq)
