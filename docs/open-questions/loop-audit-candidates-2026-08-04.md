# Open questions — duplicate-label candidates in the loop audit

**Registered:** 2026-08-04 · **Status:** open, unadjudicated · **Source:** `GLMP_MASTER_TODO.md` item 33

This is a pre-registration, not a request. The predictions below were recorded
**before** any qualified reviewer saw the candidates. When someone with the
relevant biology rules on them, the ruling goes in the Outcome column and the
pre-sort can be scored — which tells us whether this heuristic's priors are
worth trusting on the next corpus, and that is worth more than the nine answers
themselves.

Deliberately addressed to nobody. Any qualified reviewer can rule on any row,
at any time, and rows can be adjudicated independently.

---

## What the audit was looking for

GLMP computes a `loops` statistic mechanically from each process's flowchart
graph by counting directed cycles. The lac operon exposed a false negative: a
real feedback loop was invisible to the count because the permease was drawn as
two nodes (`Lactose Permease LacY` and `Lactose Permease`) rather than one, so
the cycle rendered as a straight line. A human curator caught it by eye.

Scanning the corpus for that signature: **217 processes**, of which **85 report
`loops: 0`** and **77 were unflagged for review**. A duplicate-node-label
heuristic — verified against the known `ecoli_lac_operon` case before being
trusted elsewhere — narrowed those to **11 exact-label-duplicate candidates**.
A substring tier produced 24 more; spot-checking found them to be mostly
biosynthesis-naming noise, and they are not carried here.

**The question for each candidate:** is the duplicated label one entity or event
modeled twice — the real defect, in which case a feedback loop is being missed —
or the same named step legitimately recurring at two different points in the
process, which is not a defect?

---

## Characterized error mode of the heuristic

Two of the 11 were resolved internally as false positives. Both share a cause,
and it is a property of the method rather than of the data:

**Label normalization strips characters that carry meaning in this domain.**

- `ecoli_trp_operon` — flagged "Tryptophan Synthase β" and "Tryptophan Synthase
  α" as duplicates. They are a genuine two-subunit enzyme complex. Non-ASCII
  stripping collapsed β and α to the same string.
- `yeast_peroxisome_biogenesis` — flagged "PMP Receptor" and "Fission Dynamin"
  as duplicates. The full labels are `Pex3 (PMP Receptor)` / `Pex16 (PMP
  Receptor)` and `Dnm1 (Fission Dynamin)` / `Vps1 (Fission Dynamin)`: distinct
  named proteins sharing a role description.

Greek letters are load-bearing throughout molecular biology — α/β/γ subunits,
σ factors, Δ mutants — so this error mode should be assumed to recur in any
label-matching over this corpus. A check confirmed the offending normalization
exists only in the audit script and **not anywhere in production code**, so no
shipped pipeline is silently merging distinct entities. The audit heuristic
itself has not been corrected; the two known false positives are recorded here
instead.

**Second known limitation:** the heuristic's `normalize()` step already lowercases
and collapses whitespace before comparing, so case and whitespace variants are
*not* the gap. What's actually missed is same-entity-different-wording with no
shared substring at all — two labels for the same thing that don't literally
contain one another. The lac operon case that started this audit doesn't
illustrate the gap; it illustrates what the heuristic *can* catch: `Lactose
Permease LacY` and `Lactose Permease` share a substring, which is exactly why
it was found. A genuine synonym pair — two names for the same entity with no
overlapping text — would pass through undetected. **The nine candidates below
are a floor, not a ceiling.**

---

## Candidates

Node IDs refer to the flowchart graph for each process. Predictions are the
audit's own, from graph shape and general biology — not expert rulings.

### Predicted: probably not defects

Same named step legitimately recurring.

| Process | Duplicate label(s) | Prediction rationale | Outcome |
|---|---|---|---|
| Yeast Glycolysis | "Phosphorylation" (G, O); "Isomerization" (J, AL); "Substrate-Level Phosphorylation" (AH, AR); "ATP Produced" (AJ, AT) | Glycolysis genuinely has two kinase phosphorylations (hexokinase, PFK-1), two isomerizations, two substrate-level phosphorylation steps, two ATP-producing steps | *open* |
| Bacillus Sporulation Initiation | "Dephosphorylates Spo0F~P" (AD, AF) | Multiple Rap phosphatases act on Spo0F~P | *open* |
| E. coli Heat Shock Response | "Protein Refolding" (AU, AY) | DnaK and GroEL are separate refolding systems | *open* |
| E. coli Flagellar Assembly | "FlgK, FlgL" (Proteins, Export) | Reads as entity-vs-export-event — a modeling-style duplicate rather than a cycle | *open* |

### Predicted: plausible missed cycle

These are the ones where the defect signature looks real.

| Process | Duplicate label(s) | Prediction rationale | Outcome |
|---|---|---|---|
| E. coli Pentose Phosphate Pathway | "Glucose-6-Phosphate" (A, AU); "AND: NADP+ Available?" (G, N); "Enzyme Inhibited" (H, O) | The non-oxidative branch regenerates G6P — a real cycle. Two G6P nodes is precisely what a missing feedback edge looks like | *open* |
| Yeast PKA Pathway | "PKA Inactive" (AA, BX) | Reads like negative feedback (PDE lowering cAMP) drawn as a second terminal node rather than an edge returning home | *open* |
| E. coli Acid Resistance | "Proton Consumed" (AF, AR); "Continuous Cycle" (AK, AW) | A node labeled "Continuous Cycle" appearing twice is close to self-reporting | *open* |
| Yeast GCN4 Starvation Response | "40S Scans from Cap" (AE, AO); "Initiates at uORF1" (AF, AP); "Translates uORF1" (AG, AQ); "40S Reinitiation" (AH, AR) | Reinitiation after uORF1 is a genuine cycle in the canonical model; all four duplicates cluster on it | *open* |

### Unsorted — mixed evidence within one process

| Process | Duplicate label(s) | What was observed | Outcome |
|---|---|---|---|
| E. coli Two-Component Signaling (EnvZ/OmpR) | "High Osmolarity" (J, AD — direct edge J→AD); "Low Osmolarity" (K, AI); "OR: ompF or ompC?" (AF, AK) | The ompF/ompC decision recurring under both osmolarity branches reads like real EnvZ/OmpR biology. But J flowing directly into a second "High Osmolarity" node looks like the artifact pattern. Genuinely mixed; not forced into a bucket | *open* |

---

## Scoring, when rulings arrive

Fill the Outcome column as `defect` / `not a defect` / `other`, with the ruling's
date and source. Then compare against the tier each row was placed in. Three
things become answerable that are not answerable now:

1. **Are the priors calibrated?** If most "probably not defects" hold and most
   "plausible missed cycle" rows are confirmed, the pre-sort is doing real work
   and can triage future corpora. If not, it is noise wearing a table.
2. **What is the heuristic's precision?** Two of eleven were false positives
   before review. The post-review number is the real figure, and it belongs in
   any methods write-up alongside the known error mode above.
3. **Which tier deserves automation?** Confirmed defects with a shared graph
   signature may be fixable by rule rather than by eye.

## Related

- Audit methodology, corpus scan numbers, heuristic verification against
  `ecoli_lac_operon`, the 24 substring-tier candidates, and the
  production-code check: `GLMP_MASTER_TODO.md` item 33.
- Adjudication does not require this document. Each canonical process entry
  carries an "Improve this process" form, and a ruling made there is equally
  valid — this register exists to hold the predictions, not to gate the answers.
