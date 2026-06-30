# GLMP Decoder — Known Edge Cases and Adjustments Log

Tracks pipeline limitations, their scope across the 217-process
catalog, and resolution status. Updated as new edge cases are found.

---

## EC-1: Repressor/Activator absent from JASPAR CORE

**First seen:** AraC (ara operon), TrpR (trp operon) — June 2026

**Cause:** JASPAR CORE is eukaryote-weighted; many prokaryotic TFs
have no matrix.

**Workaround:** Custom PWM file `motifs/laci_motif.meme` with
literature-derived LacI (`LacI_lacO1`) and TrpR (`TrpR_trpO`)
consensus sequences. Parser v0.2.2+ treats these as high-confidence
evidence using **p-value ≤ 0.05** (FIMO q-values are unreliable on
small custom motif sets where pi₀ ≈ 1).

**Estimated scale:** **75** bacterial/prokaryotic catalog processes
(69 `ecoli` + 2 `bacillus` + 4 `Bacillus subtilis`), of which only
3 operons have been DNA-decoded so far. **72** remaining bacterial
processes may require per-TF custom PWMs if decoded (AraC still
missing — see open gap below).

**Open gap:** No custom AraC PWM exists yet. Ara operon decode
remains JASPAR-only; `circuit_class` stays `INSUFFICIENT_EVIDENCE`
until an AraC matrix is added.

**Status:** Partial workaround (LacI/TrpR only); not systematized
for new TFs.

---

## EC-2: Protein-network-dependent circuits

**First seen:** Yeast GAL bistable switch — June 30, 2026

**Cause:** Circuit logic requires protein-protein interactions with
no DNA sequence signature (Gal80–Gal4 binding, Gal3–Gal80
sequestration). Bistability is emergent, not sequence-encoded.

**Workaround:** Two-layer schema in Firestore — `dna_decodable_layer`
+ `protein_network_layer`. DNA decode documents what FIMO can find;
curated description documents the full mechanism.

**Estimated scale:** **103** non-synthetic eukaryotic processes
(52 `human` + 41 `yeast` + 3 `arabidopsis` + 3 `mouse` + 2
`celegans` + 2 `drosophila`). Not all require protein-network
layering — many may have partial DNA-decodable promoter logic — but
signaling/bistability circuits are high-risk. **Confidence: Low–Medium.**

**Status:** Schema pattern established for GAL (`yeast_gal_bistable_switch`).
Needs proactive screening before eukaryotic decodes at scale.

---

## EC-3: Eukaryotic promoter geometry mismatch

**First seen:** Yeast GAL1 — June 30, 2026

**Cause:** Parser `RNAP_BINDING_REGION` assumes prokaryotic -35/−10
spacing. Eukaryotic promoters use TATA/Inr at different distances.

**Workaround:** `geometry_warning` field emitted for
`--organism s_cerevisiae`. NOT-gate promoter-overlap logic
unreliable for non-`ecoli_k12` runs.

**Estimated scale:** **148** non-`ecoli` processes (217 total − 69
ecoli), including 39 `synthetic` constructs. **109** non-ecoli,
non-synthetic processes if synthetic designs are excluded.
**Confidence: High** for organism-flag mismatch; **Medium** for
which specific processes will fail decode.

**Status:** Warning label only. Fix requires organism-specific
geometry profiles — scoped but not yet designed.

---

## Summary

| Edge case | Processes affected (of 217) | Confidence in estimate | Status |
|-----------|------------------------------|------------------------|--------|
| EC-1: Missing JASPAR TF | 75 bacterial; 72 undecoded | Medium | Partial workaround (LacI/TrpR) |
| EC-2: Protein-network-dependent | 103 eukaryotic (non-synthetic) | Low–Medium | Schema exists (GAL) |
| EC-3: Eukaryotic geometry | 148 non-ecoli (109 excl. synthetic) | High (flag); Medium (per-process) | Warning only |

**Phase 3 prioritization implication:** See Phase 3 Decode Priority Order below.

---

## Phase 3 Decode Priority Order

Based on organism counts and decoder confidence levels:

| Priority | Group | Count | Strategy |
|----------|-------|-------|----------|
| 1 | E. coli (remaining) | 66 | DNA-decodable, highest confidence — same pipeline as lac/ara/trp |
| 2 | Synthetic circuits | 39 | Designed logic-gate circuits, likely cleanly decodable |
| 3 | Bacillus | 6 | Prokaryotic, needs custom PWMs for key TFs |
| 4 | Yeast | 41 | Screen first: DNA-decodable vs protein-network; attempt only circuits with known operator motifs |
| 5 | Human / mouse / arabidopsis / other eukaryotes | 63 | Two-layer schema default; limited DNA decode value for most |

**High-confidence decode targets for first 300:** E. coli (66) +
synthetic (39) = 105 circuits. Combined with 3 already decoded =
108 total — well past the 300 target on solid ground before
touching harder eukaryotic territory.

**Decision made:** June 30, 2026 — Gary Welz and Claude.

---

## Organism counts (217 total)

| Organism | Count |
|----------|-------|
| E. coli | 69 |
| Human | 52 |
| Yeast | 41 |
| Synthetic | 39 |
| Bacillus subtilis | 4 |
| Arabidopsis | 3 |
| Mouse | 3 |
| Bacillus | 2 |
| C. elegans | 2 |
| Drosophila | 2 |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-06-30 | Initial log: EC-1/2/3 from lac/ara/trp/GAL decode work |
| 2026-06-30 | Parser v0.2.2: custom PWM p-value confidence for LacI/TrpR |
| 2026-06-30 | Real organism counts and Phase 3 priority order added |
