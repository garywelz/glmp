*Status: DRAFT — pending Gary's review. Not yet sent to Prof. Lents.*

# Two GLMP questions for Prof. Lents (draft, 2026-08-04)

Two separate items queued up for his input — bundled into one message
rather than two, since both need the same kind of judgment call, and both
are currently blocking a `GLMP_MASTER_TODO.md` item (#26, #33).

---

## 1. CRP PWM (the higher-leverage one)

Building a position-weight-matrix for CRP binding sites from RegulonDB data
would let the lac operon reach an evidence-backed Class II call from
sequence directly, rather than resting on curated biology alone. This is
on hold until he's had a chance to weigh in — is this worth doing, and if
so, does the RegulonDB CRP site set look like the right source to build it
from?

## 2. Flowchart candidates that may be hiding real feedback loops

Background: GLMP computes a `loops` statistic mechanically from each
process's flowchart graph — it counts directed cycles. We found one case
(the lac operon) where a real feedback loop was invisible to this count:
the permease was drawn as two separate nodes (`Lactose Permease LacY` and
`Lactose Permease`) instead of one, so the cycle rendered as a straight
line instead of a loop. A human curator caught that one by eye.

We scanned the rest of the corpus (217 processes) for the same pattern and
found candidates worth a look — pre-sorted below so his time goes to the
ones that actually need biology, not the ones we can check ourselves.

Two we already ruled out, shown as worked examples of what we're *not*
asking him to check:
- `ecoli_trp_operon` flagged "Tryptophan Synthase β" and "Tryptophan
  Synthase α" as a duplicate. They're not — a real two-subunit enzyme
  complex. Our text-matching stripped the Greek letters before comparing,
  which is why it looked like a match.
- `yeast_yeast_peroxisome_biogenesis` flagged "PMP Receptor" (twice) and
  "Fission Dynamin" (twice). Also not real — the full node labels are
  `Pex3 (PMP Receptor)` / `Pex16 (PMP Receptor)` and `Dnm1 (Fission
  Dynamin)` / `Vps1 (Fission Dynamin)`: two different named proteins
  sharing a role description, not one protein under two IDs.

**Four we think are probably not defects** (same named step legitimately
recurring, not one entity duplicated) — flag only if he disagrees:

| Process | Duplicate label(s) | Why we think it's fine |
|---|---|---|
| Yeast Glycolysis | "Phosphorylation" (x2), "Isomerization" (x2), "Substrate-Level Phosphorylation" (x2), "ATP Produced" (x2) | Glycolysis genuinely has two kinase phosphorylations (hexokinase, PFK-1), two isomerizations, two substrate-level-phosphorylation steps — textbook, not an artifact |
| Bacillus Sporulation Initiation | "Dephosphorylates Spo0F~P" (nodes AD, AF) | Multiple Rap phosphatases act on Spo0F~P |
| E. coli Heat Shock Response | "Protein Refolding" (AU, AY) | DnaK and GroEL are separate refolding systems |
| E. coli Flagellar Assembly | "FlgK, FlgL" (Proteins, Export) | Reads as entity-vs-export-event, a modeling-style duplicate rather than a cycle |

**Four where a missed cycle looks genuinely plausible — the real ask:**

| Process | Duplicate label(s) | Why we flagged it |
|---|---|---|
| E. coli Pentose Phosphate Pathway | "Glucose-6-Phosphate" (A, AU); "AND: NADP+ Available?" (G, N); "Enzyme Inhibited" (H, O) | The non-oxidative branch regenerates G6P — that's a real cycle, and two G6P nodes is exactly what a missing feedback edge would look like |
| Yeast PKA Pathway | "PKA Inactive" (AA, BX) | Reads like negative feedback (PDE lowering cAMP) drawn as a second terminal node instead of an edge home |
| E. coli Acid Resistance | "Proton Consumed" (AF, AR); "Continuous Cycle" (AK, AW) | A node literally labeled "Continuous Cycle" appearing twice is close to self-reporting |
| Yeast GCN4 Starvation Response | "40S Scans from Cap" (AE, AO); "Initiates at uORF1" (AF, AP); "Translates uORF1" (AG, AQ); "40S Reinitiation" (AH, AR) | Reinitiation after uORF1 is a genuine cycle in the canonical model; all four duplicates cluster on it |

**One we couldn't confidently sort either way — his call on which bucket it
belongs in, or a third:**

| Process | Duplicate label(s) | What we saw |
|---|---|---|
| E. coli Two-Component Signaling (EnvZ/OmpR) | "High Osmolarity" (J, AD, direct edge J→AD); "Low Osmolarity" (K, AI); "OR: ompF or ompC?" decision (AF, AK) | The ompF/ompC decision recurring under both the high- and low-osmolarity branches reads like real EnvZ/OmpR biology, not a defect — but J flowing directly into a second "High Osmolarity" node (AD) looks more like the artifact pattern. Genuinely mixed within one process; didn't want to force a guess |

No rush on either — whenever he has time.

---

*Source: `GLMP_MASTER_TODO.md` items 26 and 33. Full audit methodology
(corpus scan numbers, heuristic verification against the known
`ecoli_lac_operon` case, the substring-tier candidates not included here,
and the production-pipeline check confirming the trp/peroxisome
normalization issue doesn't exist anywhere in real code) is recorded
there in full.*
