# Biochemical Process Modeling Project

**Backbone-constrained flowcharts for multi-organism regulatory networks**

Gary Welz & Prof. Konstantin Krampis — 3-year NSF-oriented proposal

March 18, 2026

## The opportunity

- **Interpretable AI + constrained visualization:** Convert literature/DB text into backbone-anchored flowcharts (Mermaid/JSON) with provenance.
- **Four backbone databases:** RegulonDB, EcoCyc/BioCyc, KEGG, Abasy Atlas — gene/TU wiring for mechanistic structure.
- **Perturbation & Virtual Cell targets (transcriptome):** The diagrams encode “what changes when”: which gene/TU programs respond to a perturbation, yielding structured RNA-seq / scRNA-seq targets.
- **Agent + human loop:** Long-running agents draft; students validate. Output becomes benchmark-ready “synthetic data” (and exploratory TDA).

## What we’ve built — demo

Four E. coli processes, each with **six versions (V1–V6)**:

- Lac operon, SOS response, Ara operon, EnvZ–OmpR
- V1 = paper/LLM logic-rich · V2 = hybrid (paper + RegulonDB) · V3–V6 = DB-only (RegulonDB, EcoCyc, KEGG, Abasy)

<a href="https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer_demo/index.html" target="_blank" rel="noopener">Open demo → GLMP Process Demo Hub</a>

Same color/shape standard; rectangles + diamonds for decisions.

## Two-layer model (per process)

- **Backbone layer:** Non-negotiable wiring — regulators, genes, operons, reactions — from RegulonDB, EcoCyc, KEGG, Abasy (and Reactome later).
- **Logic/diagram layer:** Signals, AND/OR decisions, feedback loops, outcomes — from papers, reviews, LLM-assisted summaries.

**Explicit fit to BIO 37105 / 77105 (Spring 2026):** your course predicts cellular responses to perturbations from bulk and single-cell transcriptomics. Our backbone specifies which gene/TU programs are regulated; the logic encodes which regulatory programs respond under a perturbation—so the diagram implies which transcriptomic units should change (up/down) in RNA-seq / scRNA-seq, i.e. “what changes when”.

## Scale: agents vs validation

- **Generation:** Agents can draft 2,000+ V1–V6 families in weeks; then extract graph features + perturbation-response rules.
- **Validation:** Will take years — cross-checking DBs/literature and ensuring the perturbation logic is accurate and consistent.
- **Target:** 2,000–3,000 fully validated process families over 3 years (stretch: up to ~5,000 with more capacity).

## Validation: students + community

- **Two graduate students** as primary reviewers/editors (~15 h/week each on validation), with transparent provenance for every edge/node.
- **Public drafts** — viewable by all; suggestions via structured channels (e.g. GitHub PRs / lightweight UI / Slack/wiki).
- **Democratizing the inputs** for AI/virtual-cell workflows: students and researchers can reuse the same backbone wiring without re-deriving it.
- Moderation and triage convert community input into validated diagrams that serve as interpretable training/evaluation targets.

## Budget, hours & pay

- **PIs:** Welz, Krampis — ~1 month summer salary/year each.
- **Total budget (36 months):** \$691,184 request (Direct \$453,029; Indirect \$238,155).
- **Graduate student hours & pay (budgeted):** 2 grad students × \$15/hour × 10 hrs/week × 20 weeks/year = 400 paid hours/year; 1,200 paid hours total over 3 years.
- **Other costs:** cloud compute for DB mirrors + LLM pipelines, plus travel for NSF meetings and evaluation work.

Student compensation uses the budgeted \$15/hour fair-compensation rate; training/validation hours are planned beyond this paid testing component.

## 3-year roadmap (draft)

- **Year 1:** Agent pipeline stable; pilot 50–100 processes; generate first synthetic perturbation/evaluation targets.
- **Year 2:** Scale to ~500–1,000 validated processes; expand community validation; begin model evaluation/benchmarking.
- **Year 3:** 2,000–3,000 validated families; additional organisms; release corpus + evaluation reports aligned with virtual-cell challenge style.

## Next steps

- Decide target NSF program (and whether to prepare NIH pivot later).
- Lock scope: 2K vs 5K processes; organism list; student roles at each institution.
- Draft full Project Description, Budget Justification, References — and internal guide (already started).
- Propose a short “virtual perturbation” student mini-challenge using the validated diagrams as structured hypotheses.

Thank you — looking forward to building this with you.

<span id="cur">1</span> / <span id="tot">9</span>

Previous

Next
