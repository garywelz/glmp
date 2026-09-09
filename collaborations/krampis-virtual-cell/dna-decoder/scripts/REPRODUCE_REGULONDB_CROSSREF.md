# Reproducing the RegulonDB cross-reference analysis, independently

This is a request for an **independent replication**, not a review of
someone else's report. Please run the analysis yourself, from the raw
inputs, and report what you get — don't read
`crp_lac_ara_trp_regulondb_validation_report.md` first, so your result
isn't anchored on ours.

## What this checks

The GLMP decoder scans E. coli DNA sequence and predicts transcription-
factor binding sites (LacI, CRP, TrpR) for three operons (lac, ara, trp).
This script cross-references those predictions against RegulonDB — the
curated reference database of experimentally confirmed E. coli regulatory
sites — and reports precision/recall: of the sites the decoder predicted,
how many are real RegulonDB sites, and of RegulonDB's real sites in the
scanned regions, how many did the decoder find.

**No biology judgment is required for this task** — it's a mechanical
sequence/coordinate comparison. You need Python 3 and about 15 minutes.

## Steps

1. **Clone this repo** (if you haven't already):
   ```
   git clone https://github.com/garywelz/glmp.git
   ```

2. **Download RegulonDB v14.5.0's `TF-RISet.tsv`** from
   [regulondb.ccg.unam.mx](https://regulondb.ccg.unam.mx) — the "Regulatory
   Interactions" dataset (TF-RISet). Place it at:
   ```
   <repo root>/.tmp/regulondb-v14/TF-RISet.tsv
   ```
   This file is deliberately not committed to the repo — pull it fresh from
   the source yourself rather than using anyone else's copy.

3. **Run the script:**
   ```
   python collaborations/krampis-virtual-cell/dna-decoder/scripts/regulondb_crossref_analysis.py
   ```
   It reads the three decode files already committed at
   `collaborations/krampis-virtual-cell/dna-decoder/results/ecoli_{lac,ara,trp}_operon_logic_20260708.json`
   and writes `regulondb_crossref_results.json` next to itself.

4. **Compare your totals against ours** (printed to stdout as `=== TOTALS ===`,
   and in `regulondb_crossref_results.json`'s `"totals"` block):

   | Metric | Our result |
   |---|---|
   | True positives | 5 |
   | False positives | 10 |
   | False negatives | 21 |
   | Precision | 33.3% (5/15) |
   | Recall | 19.2% (5/26 RegulonDB regulatory-interaction rows) |

   Per-circuit: **lac and ara predictions were clean** — every threshold-
   passing prediction matched a real RegulonDB site by sequence identity, 0
   false positives. **trp was not clean**, but not because of a bad
   prediction — the scanned DNA window is ~3.4 kb away from RegulonDB's real
   TrpR sites (`trpLp`), so the 10 TrpR hits that clear their own threshold
   are comparing against the wrong stretch of genome. That's a decoder
   pipeline issue (already tracked separately), not something this script's
   numbers should be adjusted for.

## If your numbers don't match

Please report the discrepancy exactly as you found it — which circuit, what
you got instead, and anything in the script or inputs that looked off to
you. A different number is a useful result either way, not a failure on
your part; that's the whole point of asking someone else to run this.

## Questions

Contact Gary Welz (gwelz@gc.cuny.edu) with questions about the task itself.
The full technical writeup (for after you've run it yourself) is at
`../docs/crp_lac_ara_trp_regulondb_validation_report.md`.
