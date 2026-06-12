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
