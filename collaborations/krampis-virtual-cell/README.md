# Krampis–Welz GLMP Collaboration

**Gary Welz** · Researcher, New Media Lab, CUNY Graduate Center
**Prof. Konstantinos Krampis** · Hunter College / CUNY, Computational Biology
Email: gwelz@gc.cuny.edu · ORCID: https://orcid.org/0009-0005-7806-0892

---

## About This Collaboration

This folder is the source of truth for the Welz–Krampis collaboration on the **Genome Logic Modeling Project (GLMP)** — a research program aimed at decoding the regulatory grammar of the genome.

The central hypothesis: the control layer of the genome is written in a language whose alphabet consists of transcription factor binding motifs, whose syntax is encoded in the spatial arrangement of those motifs in promoter and enhancer sequences, and whose semantics are the logical connectives AND, OR, NOT, and IF-THEN. **The Big Picture Goal is to decode that language** — to build the training corpus, computational infrastructure, and analytical framework needed to read any regulatory sequence as a logical formula.

The collaboration focuses on four near-term priorities in service of that goal:

- **RPE1 replication** of the K562 Perturb-seq empirical results (Paper III)
- **Grammar-aware comparison** using RegVelo as the topology-aware virtual cell model
- **Persistent vs. transient bistability** sub-classification (Class IIIa/IIIb)
- **Multiome bimodality analysis** — testing attractor state detection via chromatin accessibility

The full collaboration plan, including paper trajectory, infrastructure expansion, and division of labor, is in `glmp-collaboration-plan-2026.md`.

---

## Contents

| File | Description |
|---|---|
| `glmp-collaboration-plan-2026.md` | **Start here.** Full collaboration plan: Big Picture Goal, near-term empirical priorities, infrastructure expansion, paper trajectory, division of labor, and immediate next steps. |
| `paper-I-foundational-typology.md` | **Paper I** — *Primitive Relations, Computational Complexity, and a Conjecture on the Genomic Computational Class.* Foundational typology; five-class complexity ladder; the Tarski/Peano contrast as precision instrument. |
| `paper-II-genome-as-computer.md` | **Paper II** — *The Genome as Computer.* 22-primitive logical vocabulary; transcriptome as runtime state; nine falsifiable predictions; grammar-aware AI research program. |
| `paper-III-empirical-sequel.md` | **Paper III** — *Circuit Class Predicts Virtual Cell Model Accuracy.* Empirical test: 780 genes, K562 Perturb-seq, 16 virtual cell models; Class III persistent bistable genes systematically harder to predict (*t* = −3.55, *p* = 0.0015). |
| `synthesis-biorxiv.md` | **Synthesis** — *Genomic Regulatory Complexity and the Limits of Perturbation Prediction.* Biology-facing bioRxiv draft for a general biology audience. |
| `methods-mermaid-perturbation-design.md` | **Methods paper** — *Mermaid Flowcharts for Smarter Perturbation Design.* Flowchart pipeline; under active revision to add sequence annotation layer and Big Picture framing. |
| `teaching-deck-krampis-biochemical-process-modeling.md` | Proposal slide deck — GLMP overview oriented toward the Krampis collaboration and biochemical process modeling context. |
| `flowchart-circuit-classes.tsv` | Machine-readable circuit-class assignment for every microbial flowchart: class (I–V), topology type, rationale, evidence source, confidence, and `needs_review` flag. **The `needs_review = yes` rows are the validation worklist for Prof. Krampis.** |

---

## Live Flowchart Collection (updated 2026-06-12)

The interactive collection is the empirical companion to the papers. It now holds **118 process flowcharts**, each tagged with its position on the five-class complexity ladder (Paper I/III) and, increasingly, a **sequence → logic** annotation that maps cis-regulatory binding sites to the Boolean operator they implement — the core training pair of the Big Picture goal.

- **Browse / query:** [database table](https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-database-table.html) — sortable **Circuit class** column, class filter buttons (I–V), class-distribution panel, and CSV export (now including `circuit_class` and `topology_type`).
- **Per-process viewer:** each diagram page shows a colored **Class I–V badge** and, where curated, a **Sequence → Logic** table.

**Collection composition (118 total):**

| Group | Count | Notes |
|---|---|---|
| E. coli | 66 | microbial regulatory + execution circuits |
| S. cerevisiae | 38 | yeast circuits |
| Bacillus subtilis | 4 | developmental switches |
| Homo sapiens | 4 | **Batch 2** — curated human circuits (GATA1/PU.1, p53–MDM2, MYC, VHL–HIF) |
| Synthetic circuit | 6 | **Batch 1** — ground-truth synthetic biology (toggle switch, repressilator, FFLs, autoregulation) |

**Circuit-class distribution:** Class I 49 · Class II 48 · Class III 15 · Class IV 4 · Class V 2.

**Classification confidence:** of the 108 microbial charts, **103 are now high-confidence** (curated from literature) and **5 remain flagged `needs_review`** for expert validation — down from 61 after the 2026-06 curation pass. The five open items (`ecoli_cell_division`, `ecoli_mal_regulon`, `ecoli_sigma_factor_competition`, `ecoli_transcription_regulation`, `yeast_yeast_glycolysis_regulation`) are genuinely ambiguous and are the priority validation worklist. The synthetic and human batches carry authored, ground-truth classes (not heuristic).

A note on the human batch: only **GATA1/PU.1** is a Class IIIa persistent bistable switch. On close reading **p53–MDM2** is a Class IV delayed-feedback oscillator, and **MYC** and **VHL–HIF** are Class II negative-feedback circuits — the ladder applied honestly to human circuits rather than forced to one class.

Reproducibility — the collection is regenerated by committed scripts: `scripts/classify_flowchart_circuits.py` (class assignment), `scripts/apply_circuit_classes.py` (write classes into JSON + metadata), `scripts/annotate_microbial_sequences.py` (sequence → logic on microbial circuits), `scripts/build_synthetic_batch1.py` and `scripts/build_human_batch2.py` (ground-truth batches), `scripts/integrate_synthetic_batch1.py` (metadata integration).

---

## Collaboration Workflow

Prof. Krampis's preferred workflow:

1. **Fork** the `garywelz/glmp` repository on GitHub
2. Edit Markdown files in the fork, either locally or via the GitHub web editor
3. Open a **pull request** back to `garywelz/glmp` for review

This keeps the main repository stable and makes it easy to discuss edits line by line. All substantive changes to the working papers should come through pull requests so both collaborators can review before merging.

The Markdown files in this folder are the canonical versions of all working papers. Legacy HTML snapshots on Google Cloud Storage exist for some assets but should not be edited — edits happen here.

---

## Draft Status

These documents are working drafts and collaboration materials, not final peer-reviewed publications. Suggested edits should focus on:

- Biological accuracy and terminology
- Single-cell and perturbation-data framing
- Virtual cell model evaluation design
- Claims that need stronger qualification or additional citation
- Datasets and references suitable for empirical validation

---

## Notes

- Mermaid diagrams are fenced as `mermaid` code blocks and render directly in GitHub Markdown preview.
- The HTML-to-Markdown conversion was automated with pandoc and lightly cleaned; some inline HTML may remain where source documents used styled links or custom layout.
- The methods paper (`mermaid-flowcharts-smarter-perturbation-design.md`) is under active revision and should not be considered stable until the next commit explicitly marks it as ready for review.
