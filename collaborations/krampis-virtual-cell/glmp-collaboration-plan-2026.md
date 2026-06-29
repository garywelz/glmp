# GLMP Collaboration Plan — Welz & Krampis
**Genome Logic Modeling Project · June 2026**
**Collaboration repository:** https://github.com/garywelz/glmp/tree/main/collaborations/krampis-virtual-cell

---

## The Big Picture Goal

The control layer of the genome — the regulatory program that determines when, where, and under what conditions each gene is expressed — is written in a language. Its alphabet consists of transcription factor binding motifs. Its syntax is encoded in the spatial arrangement of those motifs in promoter and enhancer sequences. Its semantics are the logical connectives AND, OR, NOT, IF-THEN, and their temporal and feedback extensions.

**The Big Picture Goal of GLMP and CopernicusAI is to decode that language: to build the training corpus, the computational infrastructure, and the analytical framework needed to read any regulatory sequence as a logical formula.**

This is not a metaphor. It is a research program with a concrete path. The codon table — the data layer of the genome — was decoded between 1961 and 1966. The regulatory grammar — the control layer — remains only partially decoded. GLMP is a systematic contribution toward completing that decoding.

The three components of the project serve this goal directly:

- **CopernicusAI** is the literature corpus — the raw material from which sequence-logic ground truth is extracted at scale. At 100K+ papers, it becomes one of the largest curated corpora focused on regulatory biology and sequence-to-logic evidence, systematically annotated for circuit topology and sequence content.
- **GLMP flowcharts** are the ground-truth logical formulas. Each flowchart, annotated with the DNA sequences that implement its nodes, becomes a training data point of the form: *this sequence arrangement implements this logical operation*. At thousands of charts, this is the training corpus for grammar-aware sequence models.
- **The theoretical papers** provide the grammar itself — the 22-primitive vocabulary (Paper II), the five-class complexity ladder (Papers I–III), and the formal framework that tells you what you are looking for when you scan a sequence. Without the theory, sequence scanning is pattern-matching. With the theory, it is grammar parsing.

---

## What Is Already Known

The hypothesis that DNA sequence encodes a readable logical grammar is substantially more than a conjecture. It is partially confirmed:

**NOT (repression)** is the most fully decoded. The *lac* operator sequence — the ~21 bp DNA sequence that LacI binds to block RNA polymerase — is known to nucleotide resolution. The operator *is* the NOT gate, readable directly from sequence. This has been established since Gilbert and Maxam (1973).

**AND (cooperative binding)** is substantially decoded for characterized cases. The interferon-β enhanceosome — an eight-protein AND gate — has its binding sites mapped to specific sequence motifs. The AND logic emerges from the spatial arrangement: sites must be within ~55 bp in correct orientation to allow cooperative assembly.

**Spacing encodes logic type.** Systematic studies of synthetic promoters have shown that inter-site distance determines whether TFs interact cooperatively (AND, ~15–50 bp), sterically exclude each other (XOR/competitive, <15 bp), or act independently (OR, >50 bp).

**The grammar is writable as well as readable.** Synthetic biologists have constructed promoters with specified logical behavior by arranging known binding site motifs at designed spacings.

**What remains hard:** Three-dimensional chromatin structure adds a layer not linearly readable from sequence alone. GLMP targets the linearly encodable fraction first — prokaryotic circuits, synthetic biology circuits, and simpler eukaryotic enhancers. Each decoded circuit is a real result regardless of what remains.

---

## Background: The GLMP Paper Series

| Short name | Full title | GitHub filename | GCS preview |
|---|---|---|---|
| **Paper I** | *Primitive Relations, Computational Complexity, and a Conjecture on the Genomic Computational Class* | `paper-I-foundational-typology.md` | [HTML](https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/GLMP_Foundational_Typology.html) |
| **Paper II** | *The Genome as Computer: Logical Primitives, Runtime States, and the Limits of Biological Prediction* | `paper-II-genome-as-computer.md` | [HTML](https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/genome_as_computer_v2.html) |
| **Paper III** | *Circuit Class Predicts Virtual Cell Model Accuracy: An Empirical Test of the Genomic Computational Class Conjecture* | `paper-III-empirical-sequel.md` | [HTML](https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/empirical_sequel_draft.html) |
| **Synthesis** | *Genomic Regulatory Complexity and the Limits of Perturbation Prediction* | `synthesis-biorxiv.md` | [HTML](https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/GLMP_Genomic_Complexity_Synthesis_bioRxiv.html) |
| **Methods paper** | *Reading Regulatory Logic from Sequence: Typed Flowcharts as the Unit of Representation* | `methods-mermaid-perturbation-design.md` | Zenodo: https://doi.org/10.5281/zenodo.20831780 |

Paper III delivers the first empirical test: 780 genes classified by circuit topology, evaluated against 16 virtual cell models (14 supporting the DE20 metric) on K562 Perturb-seq data. The central finding — Class III genes are systematically harder to predict (*t* = −3.55, *p* = 0.0015) — is the load-bearing empirical result that this collaboration extends.

The Methods paper is on Zenodo. bioRxiv declined it as a methods-only submission (they accept research articles only; no endorser is required). The replication paper will be the right bioRxiv submission once the RPE1 analysis is complete.

The Synthesis paper is a GitHub working draft; not yet posted to bioRxiv.

---

## Near-Term Empirical Priorities

### Priority 1 — RPE1 Replication (~1–2 months) — Joint computational task

**What:** Run the identical K562 protocol on the Replogle et al. RPE1 Perturb-seq dataset.

- Apply TRRUST-based GLMP circuit classification to the RPE1 benchmark gene set
- Re-use published per-gene accuracy scores from the same 14-method benchmark
- Compute C3 − C1 meta-analysis under DE20 metric
- Test whether the Class III difficulty signal replicates in a non-cancer, non-leukemic cell context

**Why it matters:** The entire program currently rests on a single cancer cell line. Cross-context replication is the minimum standard for a bioRxiv result worth defending.

**Success criterion:** At least 10 of 14 methods show C3 < C1 in RPE1, directionally consistent with K562.

**Krampis contribution:** Computational biology expertise for RPE1-specific regulatory context classification; interpretation of any discordances with K562. This is a purely computational task well-suited to Krampis's bioinformatics profile.

---

### Priority 2 — Grammar-Aware Comparison with RegVelo (~2–3 months) — Krampis lead

**What:** Replace CellOracle (TF-only, limited coverage) with RegVelo as the grammar-aware comparator.

- RegVelo (RNA velocity + GRN) supports perturbation simulation for non-TF genes
- Apply to the same K562 780-gene benchmark
- Test Hypothesis 2: does a grammar-aware model show a smaller Class III accuracy deficit?

**Why it matters:** Hypothesis 2 is the most consequential untested prediction in the series. The CellOracle test was incomplete due to TF-only coverage. RegVelo closes that gap.

**Krampis contribution:** RegVelo expertise; GRN configuration for K562; biological interpretation. This is the task most directly suited to Krampis's computational biology expertise and is the highest-value contribution he can make to the collaboration.

---

### Priority 3 — Persistent vs. Transient Bistability (Short paper, ~2 months) — Welz lead

**What:** Develop the IIIa/IIIb distinction (persistent vs. transient bistability) into a focused standalone paper. The finding from Paper III Section 8.5: the difficulty effect is specific to *persistent* bistable circuits. Transient cell-cycle bistable switches do not show the effect.

**Krampis contribution:** Review of computational methodology; co-author credit if he contributes to the analysis.

---

### Priority 4 — Multiome Bimodality Analysis (~3–4 months) — Krampis lead

**What:** Retest Hypothesis 4 using public K562 multiome (RNA + ATAC) datasets. Specific prediction: persistent bistable Class IIIa circuits should show bimodal chromatin accessibility at key regulatory elements even when mRNA distributions appear unimodal.

**Krampis contribution:** Multiome data analysis; chromatin accessibility interpretation. This is computational biology work in Krampis's domain.

---

### Methods Paper — Parallel Track — Welz lead

The methods paper (*Reading Regulatory Logic from Sequence*) is on Zenodo (DOI: 10.5281/zenodo.20831780) and will be submitted to a peer-reviewed journal. bioRxiv will be the right venue for the replication paper once RPE1 data is included.

---

## Infrastructure — Current State

### DNA Decoder — Prototype Complete (June 2026)

The DNA Decoder is a five-stage pipeline that takes raw DNA sequences as input and outputs structured logical formulas describing the regulatory circuits encoded in those sequences. Stages 1–3 are functional on the Jetson Nano edge compute node as of June 24, 2026.

**Validated results — three E. coli ground-truth circuits:**

| Circuit | NOT gate | AND gate | Topology | Status |
|---|---|---|---|---|
| lac operon | LacI at lacO1, p=1.28e-6 | CRP confirmed | Class II | ✅ Correct |
| ara operon | AraC absent from JASPAR | Activator geometry found | Class I | ✅ Correct |
| trp operon | TrpR found at correct coordinates | CRP AND input confirmed | Class II | ✅ Correct |

**Pipeline architecture (candidate prototype — tool choices subject to revision):**

1. Raw DNA string in — sequence input, organism and genomic context metadata
2. Feature identification — FIMO motif scanning against JASPAR 2024 CORE (2,346 motifs) for eukaryotic TFs; custom prokaryotic PWMs for repressors (LacI, TrpR)
3. Regulatory logic extraction — GLMP grammar rule parser (v0.2.0) applying spacing rules: AND ~15–50 bp; XOR <15 bp; OR >50 bp; NOT = repressor site present
4. Protein product prediction — UniProt/RefSeq lookup (planned)
5. Logical structure output — Biolink-compliant property graph in KGX format (planned)

**Key architectural insight from trp operon work:** JASPAR (eukaryote-focused) and custom prokaryotic PWMs must be scanned separately and combined at the parser level. The v0.2.0 parser implements a `--repressor-qvalue-threshold` flag that guarantees prokaryotic repressor sites are included before the max-sites cap applies.

**Parser:** `collaborations/krampis-virtual-cell/dna-decoder/glmp_logic_parser.py` (v0.2.0)

**Krampis contribution opportunity:** Technical review of the decoder pipeline architecture — FIMO configuration, motif database strategy, Biolink/KGX output design. A one-pass review from a bioinformatics perspective would be genuinely useful. This is optional and can be done asynchronously.

---

### CopernicusAI — toward 100K+ papers

~59,700 papers indexed as of June 2026. Daily scout pipeline running on Jetson Nano at 10:15 AM ET, pulling from PubMed (600/day), BioRxiv (250/day), arXiv (150/day). OpenAI text-embedding-3-small (1536d) is the embedding provider (nDCG@10 = 0.828). Firestore database: `regal-scholar-453620-r7 / copernicusai`.

---

### GLMP Flowcharts — Current Status

**Live collection as of June 17, 2026:** 217 flowcharts across 8 organisms.

| Class | Count |
|---|---|
| I (linear cascade) | 70 |
| II (negative feedback) | 72 |
| III (persistent bistable) | 52 |
| IV (oscillator) | 16 |
| V (complex nonlinear) | 7 |
| **Total loops** | **527** |

**QA status:** A correction pass was completed June 17, 2026 (commit `aecd8db`). The `ecoli_lac_operon` flowchart carries `circuitClassNeedsReview: true` pending biological validation — biological validation outreach is underway via Biostars and direct contact with molecular biologists. This is not a task for Krampis.

**New batch expansion** is gated on completion of biological validation for existing circuits.

---

## Full Paper Trajectory

### Existing papers

| Short name | Status |
|---|---|
| **Paper I** | Draft complete; revision ongoing |
| **Paper II** | Draft complete |
| **Paper III** | Draft complete; RPE1 replication is Priority 1 |
| **Synthesis** | GitHub working draft; not yet posted to bioRxiv |
| **Methods paper** | On Zenodo (DOI: 10.5281/zenodo.20831780); journal submission pending |

### New papers — planned output of this collaboration

| Paper | Scope | Target venue | Timeline | Notes |
|---|---|---|---|---|
| **Replication paper** | RPE1 + RegVelo; grammar-aware comparison; Hypothesis 2 test | *PLOS Computational Biology* or *Genome Biology* | 3–4 months | First coordinated bioRxiv posting |
| **Bistability sub-classification** | IIIa/IIIb distinction; attractive conditionals; new predictions | *Cell Systems* Letters or *PLOS Biology* | 2–3 months | Can run in parallel |
| **Multiome attractor paper** | Chromatin bimodality test; hidden state detection via ATAC/multiome | *Nature Methods* or *Genome Research* | 4–6 months | — |
| **DNA Decoder paper** | Decoder pipeline; prokaryotic + synthetic biology ground truth; KGX output | *Nucleic Acids Research* or *PLOS Computational Biology* | 12–18 months | Stages 1–3 prototype complete |
| **Grammar-aware sequence model** | Sequence-to-logic classifier trained on annotated corpus | *Nature Methods* or *Cell Systems* | 18–24 months | Long-horizon target |
| **Cross-organism topology conservation** | Batch 5 comparative analysis | *Molecular Biology and Evolution* or *PLOS Genetics* | 18–24 months | — |

---

## Division of Labor (Revised June 2026)

| Task | Welz | Krampis |
|---|---|---|
| Methods paper | Primary author | Optional review |
| Sequence annotation (motif-to-logic linking) | Pipeline / automation | — |
| Biological validation of binding site annotations | Outreach to molecular biologists | — |
| GLMP flowchart generation and QA | Primary | — |
| Circuit classification (TRRUST + literature) | Primary | — |
| CopernicusAI database expansion | Primary | — |
| Jetson ingest pipeline and DNA Decoder | Primary | Optional technical review |
| **RPE1 replication** | Support / protocol | **Primary** |
| **RegVelo configuration for K562** | Support | **Primary** |
| **Multiome / chromatin analysis** | Support | **Primary** |
| Bistability sub-classification paper | Primary | Review / co-author |
| Theory, logic framework, paper writing | Primary | Review / co-author |

---

## Immediate Next Steps

**Welz — active now:**
1. Extend DNA Decoder to synthetic biology ground-truth circuits (Batch 1)
2. Acquire RegulonDB binding site data for prokaryotic TF coverage
3. Continue biological validation outreach for lac operon sequence annotations
4. Begin `flowchart-source-papers.tsv` manifest
5. Reframe methods paper for journal submission
6. Script Firestore `glmp_relevant` backfill pass

**Krampis — when ready:**
1. Confirm which contribution fits current work (RegVelo / RPE1 / Decoder review)
2. If RegVelo: identify configuration for K562 GRN and begin setup
3. If RPE1: download Replogle et al. dataset; apply GLMP classification protocol
4. Optional: one-pass technical review of DNA Decoder pipeline
5. Fork repo and submit contributions via pull request: https://github.com/garywelz/glmp

**Joint — first coordinated deliverable (~3–4 months):**
- RPE1 replication results + RegVelo comparison → replication paper submission to bioRxiv

---

*Gary Welz · CUNY Graduate Center / New Media Lab · Genome Logic Modeling Project*
*gwelz@gc.cuny.edu · ORCID 0009-0005-7806-0892*
*Last updated: June 24, 2026*
