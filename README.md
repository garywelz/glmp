# Genome Logic Modeling Project (GLMP)

**Reading the logic of gene regulation directly from DNA.**

GLMP proposes that the DNA controlling when genes switch on and off can be read like a program. The spatial arrangement of transcription-factor binding sites in regulatory DNA encodes logical operations — AND, OR, NOT — the same primitives found in electronic circuits. We build annotated logic-gate flowcharts for regulatory circuits, decode the logic directly from sequence, and validate the result against the curated experimental record.

This is a working research project, not a finished dataset. Some of the most important questions are still open, and this page is where collaborators start.

*Gary Welz · CUNY Graduate Center / New Media Lab · [gwelz@gc.cuny.edu](mailto:gwelz@gc.cuny.edu)*

---

## What's here

- **A catalog of ~217 regulatory-logic flowcharts** across organisms (E. coli, yeast, and more), each rendering a circuit as gates and connections. Growing toward a target of 1,000+.
- **A DNA decoder** that reads regulatory logic directly from sequence using motif scanning and a custom parser — currently validated against a first set of E. coli circuits.
- **A corpus of ~62,700 indexed research papers**, searchable, that grounds the flowcharts in the primary literature.
- **A three-paper arc** developing the framework, plus a posted methods paper.

**See it live:** the public project page — with an interactive lac-operon flowchart, live counts, and the browsable circuit catalog — is at **[huggingface.co/spaces/garywelz/glmp](https://huggingface.co/spaces/garywelz/glmp)**.

---

## The open step — where collaborators come in

GLMP generates logic-gate flowcharts computationally, and decodes logic from sequence computationally. But the pivotal question — *do these flowcharts accurately reflect the molecular biology?* — needs biological judgment that neither PI can supply alone. That validation is the step that turns a promising method into trustworthy science, and it's where your expertise matters.

There are two ways to contribute, depending on your background. Both work with the same three E. coli circuits — the lac, ara, and trp operons, among the most-studied regulatory systems in biology.

### Biology track — review the annotations

Review our logic-gate annotations against the primary literature and your own knowledge: is each gate assignment right, each binding site correctly placed, each circuit class accurately called? The full review document lays out specific questions per circuit.

→ **[Annotation review](https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/lac-operon-annotation-review.html)** — interactive flowcharts, the specific asks, and links to the canonical database entries (each with an "Improve this process" form for submitting corrections).

### Computation track — cross-reference against RegulonDB

Compare our computationally predicted binding sites against RegulonDB, the gold-standard curated database of E. coli regulatory interactions. Write an analysis, produce a structured validation report.

→ **[Validation package](https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/validation/index.html)** — everything you need to download in one place: decode results, the RegulonDB flat files, the report template, and detailed task briefs. No credentials required.

*There's no deadline on either track. The work is worth doing well rather than quickly, and interim drafts are always welcome.*

---

## Using GLMP inside your own Claude

If you use Claude, you can give it live access to GLMP's current state — the project overview and its open research questions — so it can help you explore the corpus, understand the circuits, and shape your suggestions. It reads directly from this repository, so it's always current.

**Set it up once:**

1. In Claude, create a new Project (name it "GLMP" or similar).
2. Open the project's **instructions** and paste the block below.
3. That's it — every conversation in that project now reads GLMP's current context live from GitHub.

```
This project works with the Genome Logic Modeling Project (GLMP).
At the start of substantive work, fetch these from GitHub and treat them
as the current source of truth:
- https://raw.githubusercontent.com/garywelz/glmp/main/README.md
- https://raw.githubusercontent.com/garywelz/glmp/main/docs/research_focus.json

GLMP is Gary Welz's research project (CUNY Graduate Center / New Media Lab).
This is your window into the project: explore the regulatory-logic charts,
the corpus, and the open research questions, and use what you find to shape
suggestions and analysis. The project's canonical files live in GitHub and
are maintained by the project lead — so treat this as a rich read-only
context to think with, not a workspace to edit.
```

Nothing to upload, nothing to keep in sync — when the project updates, your Claude sees it the next time you start a conversation.

---

## The idea, in more depth

If you want the conceptual foundation — why regulatory DNA can be read as logic, how the circuit-complexity classes work, and what the decoder does — these are the places to go:

- **Methods paper (Zenodo):** [doi.org/10.5281/zenodo.20831780](https://doi.org/10.5281/zenodo.20831780)
- **From Inspiration to AI: Biology as Visual Programming** (Medium) — [essay](https://medium.com/@garywelz_47126/from-inspiration-to-ai-biology-as-visual-programming-520ee523029a)
- **Is the Genome Like a Computer Program?** (ResearchGate) — [PDF](https://www.researchgate.net/profile/Gary-Welz-2/publication/394255600_Is_the_Genome_Like_a_Computer_Program)
- **Google Scholar profile:** [publications](https://scholar.google.com/citations?view_op=list_works&hl=en&user=3wTcI6EAAAAJ)

A note on honesty, which the project takes seriously: the flowcharts distinguish what the sequence decoder can actually confirm from what is well-established textbook biology, and the open questions are stated as open. Where the evidence isn't yet there, the annotation says so. That calibration is deliberate — a clearly marked limit is a finding, not a gap to paper over.

---

## Citation

If you build on this work, please cite the methods paper:

> Welz, G. (2026). *Mermaid flowcharts for perturbation design: diagrams-as-code, curated databases, and the E. coli lac operon as a worked example.* Zenodo. [doi.org/10.5281/zenodo.20831780](https://doi.org/10.5281/zenodo.20831780)

## Contact

Gary Welz · CUNY Graduate Center / New Media Lab
[gwelz@gc.cuny.edu](mailto:gwelz@gc.cuny.edu) · ORCID [0009-0005-7806-0892](https://orcid.org/0009-0005-7806-0892)
