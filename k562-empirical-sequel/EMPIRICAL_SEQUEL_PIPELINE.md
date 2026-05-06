# Empirical Sequel: Virtual Cell Model Stratification by Circuit Class

## Research Question

**Does virtual cell model prediction accuracy correlate with the computational
complexity class of the target gene's regulatory circuit?**

This tests Prediction 5 (accuracy correlates with circuit class) and
Prediction 8 (grammar-aware models outperform grammar-blind models) from
*The Genome as Computer* (Welz, 2026).

---

## Core Hypothesis

- **Class I–II circuits** (feed-forward, negative feedback): models should
  predict perturbation responses accurately — the circuits are decidable.
- **Class III circuits** (bistable): accuracy drops — response depends on
  which attractor the cell occupies, invisible to many models.
- **Class IV–V circuits** (oscillatory, self-modifying): accuracy lowest —
  response depends on phase or epigenetic state; Rice's theorem sets a
  hard ceiling if Turing-complete.

If this gradient appears, it constitutes empirical evidence that
computational complexity class is a biologically real distinction,
not merely a theoretical analogy.

---

## Pipeline Overview

```
┌──────────────────────────────────────────────────────────┐
│  PHASE 1: Gene Circuit Classification                    │
│                                                          │
│  Input:  List of perturbed genes from benchmark dataset  │
│  Method: Classify each gene's regulatory circuit by      │
│          GLMP complexity class (I–V)                     │
│  Output: gene_circuit_classes.tsv                        │
│          (gene_id, circuit_class, evidence, confidence)  │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│  PHASE 2: Run Virtual Cell Models                        │
│                                                          │
│  Models:  (A) STATE      — grammar-blind transformer     │
│           (B) CellOracle — grammar-aware (uses GRN)      │
│           (C) RegVelo    — GRN + RNA velocity (optional)  │
│                                                          │
│  Input:   Benchmark Perturb-seq dataset(s)               │
│  Output:  Per-gene prediction scores from each model     │
│           (predicted vs. observed expression changes)     │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│  PHASE 3: Stratified Analysis                            │
│                                                          │
│  Join:    gene_circuit_classes + model_predictions        │
│  Test:    Does prediction accuracy (correlation, DEG     │
│           recovery, etc.) decrease from Class I → V?      │
│  Compare: STATE vs. CellOracle accuracy per class        │
│  Output:  Stratified accuracy table, figures, stats      │
└──────────────────────────────────────────────────────────┘
```

---

## Phase 1: Gene Circuit Classification

### 1.1 Source: Benchmark Gene Lists

The primary benchmark dataset is the **Replogle et al. (2022) K562
Perturb-seq** dataset — genome-scale CRISPRi perturbations in K562 human
leukemia cells. This is the standard benchmark used by STATE, CellOracle,
and the Nature Methods 27-method comparison. Available on CZI Virtual Cells
Platform and scPerturb.

The dataset perturbs ~5,000 essential genes. Of these, a subset are
transcription factors and signaling genes whose regulatory circuits are
classifiable.

### 1.2 Classification Method

For each perturbed gene that is a TF or signaling component:

1. **Check GLMP database** — Does GLMP already have a flowchart for this
   gene or its E. coli ortholog? If yes, read circuit class directly.

2. **Check RegulonDB / TRRUST / ENCODE** — Look up known regulatory
   interactions. Classify by topology:
   - No feedback edges → **Class I**
   - Negative autoregulation → **Class II**
   - Positive feedback / mutual activation → **Class III**
   - Mixed feedback with delays → **Class IV**
   - Epigenetic self-modification → **Class V**

3. **Check literature** — For well-studied circuits (lac operon, toggle
   switch, repressilator, Yamanaka factors), classification is established.

4. **LLM-assisted classification** — For genes with known interactions but
   no existing GLMP chart, use the GLMP pipeline to generate a typed
   flowchart and classify.

### 1.3 Expected Distribution

Based on known network motif frequencies (Shen-Orr et al. 2002, Alon 2006):
- Class I (feed-forward): ~40–50% of TF circuits
- Class II (negative autoregulation): ~30–40%
- Class III (bistable): ~10–15%
- Class IV (oscillatory): ~2–5%
- Class V (epigenetic): ~1–3%

This means Classes IV and V will have small sample sizes — acknowledged as
a limitation but still testable.

### 1.4 Output

```
gene_id          circuit_class  topology           evidence           confidence
TP53             III            mutual_repression  MDM2-p53 toggle    high
MYC              III            positive_feedback  autoactivation     high
GATA1            III            mutual_repression  GATA1-PU.1 toggle  high
HIF1A            II             negative_feedback  VHL-HIF1A loop     high
JUN              I              feed_forward       AP-1 cascade       medium
DNMT3A           V              epigenetic         self_methylation   high
KLF4             III            positive_feedback  Yamanaka circuit   high
CLOCK            IV             oscillatory        circadian loop     high
NFKB1            II             negative_feedback  IkB-NFkB loop      high
...
```

---

## Phase 2: Run Virtual Cell Models

### 2.1 Benchmark Dataset

**Primary:** Replogle et al. 2022, K562 Perturb-seq
- Available via CZI Virtual Cells Platform (processed H5AD)
- Also on scPerturb (harmonized format)
- ~5,000 gene perturbations with single-cell readout
- Standard benchmark for all major models

**Secondary (validation):** Norman et al. 2019 (combinatorial perturbations
in K562) — tests multi-gene perturbation prediction, relevant to
AND/OR gate circuits.

### 2.2 Model A: STATE (Grammar-Blind)

- **What it is:** Transformer trained on 100M+ perturbed cells.
  Predicts perturbation response from expression context alone —
  no explicit regulatory network representation.
- **Code:** github.com/ArcInstitute/state
- **Pre-trained models:** HuggingFace (ST-Parse, ST-Tahoe, SE-600M)
- **Evaluation:** Cell-Eval framework (github.com/ArcInstitute/cell-eval)
- **What we measure:** Per-gene prediction accuracy (correlation between
  predicted and observed expression change vectors)
- **GPU requirements:** Moderate — runs on single A100 or similar

### 2.3 Model B: CellOracle (Grammar-Aware)

- **What it is:** GRN inference from scATAC-seq + scRNA-seq, then
  simulates TF perturbation by propagating through inferred network.
  Explicitly represents regulatory topology.
- **Code:** github.com/morris-lab/CellOracle (published Nature 2023)
- **What we measure:** Same per-gene prediction accuracy metrics
- **Key advantage:** The inferred GRN *is* the circuit topology.
  We can directly compare CellOracle's inferred network motifs
  against GLMP classifications.
- **GPU requirements:** Low — mostly CPU, some GPU for GRN inference

### 2.4 Model C: RegVelo (Optional, Grammar-Aware)

- **What it is:** Combines GRN inference with RNA velocity dynamics.
  Already validated on toggle-switch (Class III) circuits.
- **Code:** Public (preprint stage)
- **Value:** Provides a third data point and specifically tests
  Class III circuit prediction.

### 2.5 Metrics (from Cell-Eval / Nature Methods benchmark)

For each perturbed gene, measure:
1. **Pearson correlation** — predicted vs. observed mean expression change
2. **DEG recovery** — fraction of true differentially expressed genes
   recovered by the model (precision, recall, F1)
3. **Direction accuracy** — fraction of genes where predicted direction
   (up/down) matches observed
4. **E-distance** — distributional distance between predicted and observed
   single-cell populations (from scPerturb)

---

## Phase 3: Stratified Analysis

### 3.1 Primary Analysis

For each model, compute mean accuracy (all four metrics) stratified by
circuit class:

```
            Pearson   DEG-F1   Direction   E-distance
Class I      0.72      0.65     0.81        0.12
Class II     0.68      0.61     0.78        0.15
Class III    0.54      0.48     0.65        0.24
Class IV     0.41      0.35     0.55        0.38
Class V      0.33      0.28     0.48        0.45
```

(Hypothetical values — the gradient is the prediction.)

### 3.2 Head-to-Head: Grammar-Blind vs. Grammar-Aware

```
            STATE (blind)   CellOracle (aware)   Δ (aware−blind)
Class I       0.72              0.74                +0.02
Class II      0.68              0.71                +0.03
Class III     0.54              0.62                +0.08  ← biggest gap
Class IV      0.41              0.46                +0.05
Class V       0.33              0.35                +0.02  ← both fail
```

The prediction: grammar-aware models gain most on Class III (bistable)
where knowing the toggle-switch topology helps predict which attractor
the cell is in. Both models converge to low accuracy on Class V.

### 3.3 Statistical Tests

- **Spearman rank correlation:** accuracy vs. circuit class (ordinal)
- **Kruskal-Wallis test:** accuracy differs across classes
- **Paired Wilcoxon:** STATE vs. CellOracle within each class
- **Bootstrap confidence intervals** on per-class means

### 3.4 Figures for Paper

1. **Box plot:** Prediction accuracy (y) by circuit class (x), separate
   panels or colors for each model
2. **Scatter plot:** Per-gene accuracy vs. circuit class, with regression
   line showing the gradient
3. **Heatmap:** Models × Classes, colored by accuracy
4. **Bar chart:** Accuracy gap (CellOracle − STATE) by class

---

## Data Sources Summary

| Resource | URL | What We Need |
|---|---|---|
| K562 Perturb-seq (Replogle 2022) | CZI Virtual Cells Platform | Benchmark perturbation data |
| scPerturb | scperturb.org | Harmonized perturbation datasets |
| Nature Methods benchmark (29 datasets) | Figshare DOIs in paper | Pre-computed results for 27 methods |
| STATE + Cell-Eval | github.com/ArcInstitute/state | Grammar-blind model + evaluation |
| CellOracle | github.com/morris-lab/CellOracle | Grammar-aware model |
| RegulonDB | regulondb.ccg.unam.mx | E. coli regulatory network for classification |
| TRRUST v2 | grnpedia.org/trrust | Human TF-target interactions |
| ENCODE TF targets | encodeproject.org | ChIP-seq validated TF binding |
| GLMP database | GLMP database table | Existing circuit classifications |

---

## Timeline and Division of Labor

### Computational (Krampis lab)
- Download and preprocess K562 Perturb-seq data
- Run STATE predictions using pre-trained models
- Run CellOracle GRN inference + perturbation simulation
- Compute all metrics via Cell-Eval framework

### Biological / Theoretical (Welz)
- Phase 1 gene circuit classification (GLMP + literature + databases)
- Interpretation of results in context of complexity ladder
- Writing: connecting results to companion paper framework

### Joint
- Phase 3 stratified analysis and statistics
- Figures and paper writing

### Estimated Timeline
- **Weeks 1–3:** Phase 1 — classify ~200–500 TF/signaling genes by circuit class
- **Weeks 2–4:** Phase 2 — run STATE and CellOracle on K562 benchmark
- **Weeks 4–6:** Phase 3 — stratified analysis, statistics, figures
- **Weeks 6–8:** Paper writing and revision

---

## What This Paper Would Be

**Title (working):** *Prediction Accuracy of Virtual Cell Models Correlates
with Gene Regulatory Circuit Complexity Class: An Empirical Test*

**Contribution:** First empirical test of the conjecture that computational
complexity class — as defined by regulatory circuit topology — is a
biologically real distinction with measurable consequences for AI model
performance. Provides evidence that grammar-aware models (using explicit
GRN topology) outperform grammar-blind models on circuits where topology
matters most.

**Novelty:** Nobody has stratified virtual cell model predictions by
regulatory circuit class. The Nature Methods benchmark (27 methods, 29
datasets) reports aggregate accuracy. We re-stratify by circuit class —
a fundamentally new axis of evaluation.

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Too few Class IV–V genes in K562 | Weak statistics for high classes | Acknowledge; supplement with Norman et al. combinatorial data |
| Circuit classification is subjective | Reviewer challenge | Use multiple evidence sources; publish classification with confidence scores |
| No accuracy gradient observed | Null result | Still publishable — constrains the conjecture; shows where analogy breaks down |
| CellOracle and STATE not directly comparable | Apples-to-oranges | Use identical benchmark, identical metrics, identical gene set |
| K562 is a cancer cell line | Limited generalizability | Acknowledge; propose follow-up with primary cell datasets |
