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

The near-term empirical priorities below all serve this goal. Each paper advances the framework, expands the training data, or validates the grammar-decoding approach on characterized circuits. Nothing in the plan is bibliographic for its own sake.

---

## What Is Already Known

The hypothesis that DNA sequence encodes a readable logical grammar is substantially more than a conjecture. It is partially confirmed:

**NOT (repression)** is the most fully decoded. The *lac* operator sequence — the ~21 bp DNA sequence that LacI binds to block RNA polymerase — is known to nucleotide resolution. The operator *is* the NOT gate, readable directly from sequence. This has been established since Gilbert and Maxam (1973).

**AND (cooperative binding)** is substantially decoded for characterized cases. The interferon-β enhanceosome — an eight-protein AND gate — has its binding sites mapped to specific sequence motifs (NF-κB binds GGGRNNTCC; IRF3/7 binds GAAA cores; AP-1 binds TGASTCA). The AND logic emerges from the spatial arrangement: sites must be within ~55 bp in correct orientation to allow cooperative assembly. The sequence encodes both the input identities and the combinatorial logic.

**Spacing encodes logic type.** Systematic studies of synthetic promoters have shown that inter-site distance determines whether TFs interact cooperatively (AND, ~15–50 bp), sterically exclude each other (XOR/competitive, <15 bp), or act independently (OR, >50 bp). The syntax of the grammar is partly encoded in geometry.

**The grammar is writable as well as readable.** Synthetic biologists have constructed promoters with specified logical behavior by arranging known binding site motifs at designed spacings. This demonstrates that the sequence → logic relationship is real and bidirectional.

**What remains hard:** Three-dimensional chromatin structure adds a layer not linearly readable from sequence alone. Enhancers acting through long-range looping encode logic in 3D architecture rather than 1D sequence. This is a real obstacle — but not fatal. For prokaryotic circuits, simple eukaryotic enhancers, and synthetic biology circuits, linear sequence is sufficient. The 3D-dependent fraction is a longer-term challenge addressed as multiome and chromatin conformation technologies mature. GLMP targets the linearly encodable fraction first. Each decoded circuit is a real result regardless of what remains.

---

## Background: The GLMP Paper Series

Five working papers form the existing foundation of the series. The table below is the definitive cross-reference: the short names used throughout this document, the full titles, the current GitHub filenames, and the GCS HTML preview URLs.

| Short name used in this document | Full title | GitHub filename | GCS preview |
|---|---|---|---|
| **Paper I** | *Primitive Relations, Computational Complexity, and a Conjecture on the Genomic Computational Class* | `paper-I-foundational-typology.md` | [HTML](https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/GLMP_Foundational_Typology.html) |
| **Paper II** | *The Genome as Computer: Logical Primitives, Runtime States, and the Limits of Biological Prediction* | `paper-II-genome-as-computer.md` | [HTML](https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/genome_as_computer_v2.html) |
| **Paper III** | *Circuit Class Predicts Virtual Cell Model Accuracy: An Empirical Test of the Genomic Computational Class Conjecture* | `paper-III-empirical-sequel.md` | [HTML](https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/empirical_sequel_draft.html) |
| **Synthesis** | *Genomic Regulatory Complexity and the Limits of Perturbation Prediction* | `synthesis-biorxiv.md` | [HTML](https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/GLMP_Genomic_Complexity_Synthesis_bioRxiv.html) |
| **Methods paper** | *Mermaid Flowcharts for Smarter Perturbation Design: A Hybrid Literature–Database Approach* | `methods-mermaid-perturbation-design.md` | [HTML](https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/bioRxiv_Mermaid_Flowcharts_Perturbation_Methods_Draft.html) |

All five are working drafts. The canonical versions are the Markdown files in this GitHub repository — edits should happen here via pull request, not in the GCS HTML files.

**What the series establishes:**

Paper I introduces the five-class computational complexity ladder and the core conjecture: that gene regulatory circuits can be located on this ladder by their topology, with measurable consequences for biological behavior. Paper II develops the full logical vocabulary (22 primitives), treats the transcriptome as a runtime state, and generates nine falsifiable predictions — including the grammar-aware AI program that is the long-horizon goal of this collaboration. Paper III delivers the first empirical test: 780 genes classified by circuit topology, evaluated against 16 virtual cell models on K562 Perturb-seq data (14 of which support the DE20 accuracy metric used in the primary benchmark). The central finding — Class III (persistent bistable) genes are systematically harder to predict (*t* = −3.55, *p* = 0.0015) — is the load-bearing empirical result that this collaboration extends. The Synthesis translates the full argument for a general biology audience. The Methods paper documents the Mermaid flowchart pipeline and is under active revision to add the sequence annotation layer.

**Planned future papers** from this collaboration are listed in the Full Paper Trajectory section below. They are new work — none of them exist yet.

---

## File Renaming — Complete

Working paper filenames have already been updated in the repository to match the short names and GCS navigation labels used in this document. No further renaming is required.

---

## Near-Term Empirical Priorities

### Priority 1 — RPE1 Replication (~1–2 months)

**What:** Run the identical K562 protocol on the Replogle et al. RPE1 Perturb-seq dataset.

- Apply TRRUST-based GLMP circuit classification to the RPE1 benchmark gene set
- Re-use published per-gene accuracy scores from the same 14-method benchmark
- Compute C3 − C1 meta-analysis under DE20 metric
- Test whether the Class III difficulty signal replicates in a non-cancer, non-leukemic cell context

**Why it matters:** The entire program currently rests on a single cancer cell line. Cross-context replication is the minimum standard for a bioRxiv result worth defending. RPE1 is already deeply profiled and benchmarked — this is a computational task, not a new experiment.

**Success criterion:** At least 10 of 14 methods show C3 < C1 in RPE1, directionally consistent with K562.

**Krampis contribution:** Computational biology expertise for RPE1-specific regulatory context classification; interpretation of any discordances with K562.

---

### Priority 2 — Grammar-Aware Comparison with RegVelo (~2–3 months)

**What:** Replace CellOracle (TF-only, limited coverage) with RegVelo as the grammar-aware comparator.

- RegVelo (RNA velocity + GRN) supports perturbation simulation for non-TF genes
- Apply to the same K562 780-gene benchmark
- Test Hypothesis 2: does a grammar-aware model show a smaller Class III accuracy deficit?

**Why it matters:** Hypothesis 2 — topology-aware models outperform topology-blind models specifically on Class III targets — is the most consequential untested prediction in the series. The CellOracle test was incomplete due to TF-only coverage. RegVelo closes that gap.

**Connection to Big Picture:** If RegVelo shows a smaller Class III penalty, it is the first evidence that grammar awareness — knowing the regulatory topology — reduces the hidden-state problem. This directly motivates the grammar-aware sequence model that is the endpoint of the grammar-decoding program.

**Expected outcome:** Either (a) RegVelo shows a smaller C3 penalty → direct confirmation; or (b) same or larger penalty → the hidden-state problem requires richer state representation beyond network topology alone. Either result is publishable and informative.

**Krampis contribution:** RegVelo expertise; GRN configuration for K562; biological interpretation.

---

### Priority 3 — Persistent vs. Transient Bistability (Short paper, ~2 months)

**What:** Develop the key theoretical refinement from the K562 robustness test (Paper III, Section 8.5) into a focused standalone paper.

**The finding:** The difficulty effect is specific to *persistent* bistable circuits — those where the product sustains the conditions for its own continued production after the initiating signal is gone (MYC autoactivation, GATA1/PU.1 mutual repression). Transient cell-cycle bistable switches (ESPL1, FBXO5, INCENP) do not show the effect.

**Paper structure:**
- Define the persistent vs. transient distinction via the "attractive conditional" and nucleation framework (Paper III Section 10.5)
- Propose Class IIIa (persistent fate bistability) vs. IIIb (transient cycling bistability)
- Generate specific empirical predictions distinguishing IIIa from IIIb
- Short (~3,000 words), theory-focused, Letters format

**Connection to Big Picture:** The IIIa/IIIb distinction has a sequence-level correlate: IIIa circuits have autoregulatory binding sites (the TF product binds its own promoter) that are readable from sequence. This makes IIIa circuits a high-priority target for the sequence annotation pipeline.

**Krampis contribution:** Biological validation of the IIIa/IIIb distinction; identification of additional candidate circuits in each sub-class.

---

### Priority 4 — Multiome Bimodality Analysis (~3–4 months)

**What:** Retest Hypothesis 4 using the correct instrument.

**Problem:** scRNA-seq dropout dominated the bimodality coefficient (*r* = −0.98), rendering mRNA snapshots uninformative for attractor state detection.

**Solution:** Public K562 multiome (RNA + ATAC) datasets, CITE-seq, or hematopoietic differentiation time courses.

**Specific prediction:** Persistent bistable Class IIIa circuits should show bimodal chromatin accessibility at key regulatory elements (GATA1 promoter, MYC enhancer) even when mRNA distributions appear unimodal. The attractor state is encoded in chromatin, not mRNA.

**Connection to Big Picture:** This directly tests whether the hidden attractor states postulated by the grammar-decoding framework are visible in chromatin accessibility data — the same data type that will be used to validate sequence-logic annotations in the grammar-decoding pipeline.

**Krampis contribution:** Multiome data analysis; chromatin accessibility interpretation; hematopoietic differentiation biology.

---

### Methods Paper — Parallel Track (~2–3 months to revised draft; post alongside replication paper)

**What:** Revise and post the existing methods primer — *Mermaid Flowcharts for Perturbation Design* — to serve as the documented methods foundation for the entire grammar-decoding program, not merely a flowchart tutorial.

**Current state:** The paper exists as a complete draft. It describes three encodings of the lac operon (literature-first, RegulonDB-emphasis, hybrid), a layered hybridization workflow, and practical guidance on LLM prompt sensitivity. The content is sound. The framing is too narrow — it presents Mermaid diagrams as a convenience tool for perturbation planning rather than as the representational core of a grammar-decoding research program.

**What needs to be added (Welz lead, ~2–3 weeks of writing):**

- **Reframed abstract and introduction** — the opening should position typed flowcharts as the unit of representation in a grammar-decoding program, not as a diagramming convenience. The Big Picture Goal statement anchors this.
- **Sequence annotation section using the lac operon as worked example** — the *lacO* operator sequence (~21 bp, the physical encoding of the NOT gate), the CRP binding site sequence, and the spatial relationship between them (their ~60 bp separation encoding logical independence rather than cooperative AND) should be shown explicitly. This is the first concrete demonstration that a flowchart node can be linked to a DNA sequence. The lac operon is the intended worked example because it is completely characterized and instantiates the simplest grammar primitives (NOT, CONDITIONAL) in their purest form. *However, before finalizing this section, a QA pass is required on the existing lac operon flowchart in the collection — specifically verifying class assignment, loop topology, and sequence annotation consistency. The lac operon should not be used as the anchor example until this check is complete (see Krampis contribution below).*
- **Five-class connection** — a section explicitly linking the flowchart classification method to the complexity ladder, showing how you read Class I vs. II vs. III topology from a Mermaid diagram. The lac operon (Class II, negative feedback via allolactose depletion) is the worked example.
- **Sequence annotation schema** — the field definitions for binding site annotations: DNA sequence, position weight matrix source (JASPAR/HOCOMOCO), inter-site distances, orientation, genomic coordinates, confidence level, source paper DOI. This documents the pipeline described in the Infrastructure section of this plan and makes the paper a living reference other groups can use to contribute annotations.

**What needs Krampis specifically:**

- **QA and biological review of the lac operon flowchart and sequence annotation section** — before the lac operon is used as the canonical worked example, Krampis validates: (a) that the existing GLMP lac operon flowchart has correct class assignment, loop topology, and node labeling; (b) that the *lacO* sequence, CRP binding site, and spatial context are correctly described; and (c) that the logical interpretation (NOT gate, CONDITIONAL) accurately reflects the molecular biology. This QA step gates the methods paper sequence annotation section.
- **Joint definition of the sequence annotation schema** — the field definitions need molecular biology input to ensure they capture the right information for circuits beyond prokaryotes, particularly for the human Class IIIa circuits in Batch 3. Schema definition is a one-session working call task.

**Posting strategy — two-track, not sequential:**

Revision begins now and runs in parallel with the RPE1 replication. The paper is *not* posted immediately — it is held until the replication paper is nearly complete, then posted 2–4 weeks ahead of it. This sequencing means the methods paper lands with a live application already in progress: the bioRxiv audience reads "here is the method" and within weeks sees "here is what the method found." A methods paper without a demonstrated application is a tutorial. A methods paper with a companion results paper is a foundation.

**Connection to Big Picture:** The methods paper, once revised, is the public-facing documentation of the grammar-decoding unit of representation. It establishes the claim — typed flowcharts annotated with sequence data are training data for grammar-aware sequence models — on the record before anyone else frames it that way. This is intellectual territory worth staking early.

**Target venue:** bioRxiv (methods/systems biology category), then journal submission to *Nucleic Acids Research* Web Software or *PLOS Computational Biology* Methods.

---

## Infrastructure Expansion — Serving the Big Picture Goal

The flowchart expansion and database scale-up are not bibliographic projects. They are the **training data construction phase** of the grammar-decoding program. Every flowchart annotated with sequence data is a training pair. Every paper indexed contributes to the corpus from which sequence-logic ground truth is extracted.

### CopernicusAI — toward 100K+ papers

Expansion is organized by value to grammar decoding, not uniform coverage:

**Tier 1 — Sequence-logic ground truth papers (target: ~10,000 papers)**
Papers that explicitly link DNA sequence to regulatory logic outcomes: MPRA studies (each generates hundreds of sequence-logic pairs), systematic promoter dissection studies, synthetic biology papers describing designed logic gates. These are the highest-value papers for grammar decoding and are ingested first.

**Tier 2 — Characterized circuit papers (target: ~35,000 papers)**
Papers describing well-characterized regulatory circuits with known topology — the literature underlying existing GLMP flowcharts and the TRRUST/RegulonDB databases. Comprehensive coverage of the core regulatory biology literature.

**Tier 3 — Regulatory genomics at scale (target: ~5,000 papers)**
ENCODE, Roadmap Epigenomics, GTEx, and related large-scale regulatory mapping studies. Population-level context for which sequences are active in which cell types.

**Tier 4 — Computational regulatory biology (target: ~15,000 papers)**
Sequence models, motif databases, GRN inference methods, virtual cell models. The tools used for grammar decoding.

**Tier 5 — Broad systems and molecular biology**
General coverage filling remaining capacity.

**New metadata field:** Every paper in Tiers 1–3 is tagged *sequence_logic_content* (boolean) — whether it contains primary sequence-to-logic data. This single field makes the grammar-decoding subset instantly queryable across 100K papers.

---

### GLMP-Relevant Paper Tagging and Ingest Strategy

The CopernicusAI database is a general scientific corpus spanning biology, mathematics, computer science, physics, and other disciplines. For grammar decoding, a curated GLMP-relevant subset is needed as the embedding index for retrieval — the papers that underlie the flowcharts and the broader regulatory biology literature. The architecture keeps one database with two logical views: the general browsing interface shows everything; the GLMP embedding index filters to `glmp_relevant == true`.

**Firestore tagging field**

Every paper document receives a new boolean field: `glmp_relevant`. The GLMP embedding index is built exclusively from documents where `glmp_relevant == true`. This requires no structural change to the database — it is a filter field added to existing documents.

**Backfill pass over existing 59K papers**

A one-time classification script sets `glmp_relevant: true` for existing documents matching any of:
- `discipline == "biology"` AND categories include any of: gene regulation, transcription, chromatin, epigenetics, systems biology, synthetic biology, regulatory genomics, computational biology, perturbation, single-cell, RNA, protein binding, promoter, enhancer, operon, signal transduction
- `discipline == "computer science"` AND categories include: computational biology, bioinformatics, sequence models, machine learning genomics
- Paper is listed in the GLMP flowchart source paper manifest (see below) — regardless of discipline

**Flowchart source paper manifest — joint task with Krampis**

Every GLMP flowchart must have a canonical source paper whose DOI is recorded in a manifest file (`flowchart-source-papers.tsv` in the GitHub repo). This manifest drives both the tagging pass and targeted ingestion of missing source papers. Some source papers predate modern crawls (e.g. Gilbert & Maxam 1973 on the lac operon sequence) and must be explicitly ingested by DOI. Building the manifest is a joint task: Welz provides circuit names and initial DOIs; Krampis validates and fills gaps for circuits in the virtual cell and hematopoietic domains.

**Ingest script modifications going forward**

Two additions to the existing ingest pipeline:

1. *Discipline classifier at ingestion time* — sets `glmp_relevant` automatically on new papers using the same category logic as the backfill, so the tag is maintained without manual passes
2. *Curated DOI list ingestion mode* — alongside the existing crawl mode, a targeted mode that accepts a list of DOIs (the five-tier priority list from this plan, plus the flowchart source paper manifest), fetches metadata and full text, tags `glmp_relevant: true`, and generates embeddings. This ensures priority papers enter the corpus on a defined schedule rather than waiting for the crawl to find them

**HuggingFace Dataset publication**

Once the `glmp_relevant` subset reaches sufficient coverage (estimated at 20K–30K papers with embeddings), it should be published as a HuggingFace Dataset — a citable, downloadable resource for the sequence modeling community. This is the training-adjacent corpus that makes the grammar-aware sequence model tractable for other groups to build on. Dataset publication also generates a DOI and establishes priority on the corpus curation approach.

---

### Infrastructure Expansion — Jetson Nano (reComputer J1010)

**Hardware:** Jetson Nano (Seeed Studio reComputer J1010, 128GB microSD)

The Jetson is now operational as a dedicated edge compute node with two confirmed production roles:

**Daily Scout** — A scheduled pipeline that monitors arXiv, PubMed, bioRxiv, and CORE for new papers matching GLMP-relevant criteria. The scout runs locally on the Jetson, pre-filters candidates, and queues them for full ingest. This offloads routine polling and filtering from GCP entirely. The pipeline runs daily at 10:15 AM ET via cron, pulling from PubMed (600 papers/run), BioRxiv/MedRxiv (250), and arXiv (150). As of June 2026, the scout is in production: on the first full scout run, 47,536 documents were processed against the existing Firestore index (which at that point held 47,532 documents), yielding 4 net new papers written. The total Firestore index as of the most recent embedding run stands at 59,702 documents — this larger figure reflects papers ingested across all sources prior to the Jetson scout going live, not the scout run alone.

**Paper Ingest** — Local pre-processing of incoming papers: PDF parsing, metadata extraction, and preparation for cloud submission. Raw documents are processed on the Jetson before being pushed to the GCP pipeline, reducing cloud compute consumption on routine tasks.

**Embedding:** OpenAI text-embedding-3-small (1536d) remains the embedding provider for all documents. The Jetson does not perform embedding. This preserves the integrity of the existing 59,702-document Firestore index (nDCG@10 = 0.828 on dense retrieval benchmark) and avoids vector space fragmentation from mixed embedding models.

**Key paths on Jetson:**

| Item | Path |
|---|---|
| Repo | `/home/gary/copernicus-worker/copernicus-web` |
| Venv | `/home/gary/copernicus-worker/venv` |
| Credentials | `~/.config/copernicus/gcp-sa.json` |
| Env file | `~/.config/copernicus/env` |
| Cron log | `.../paper_acquisition_logs/daily_scout/cron.log` |

**Known constraints:** The SD card is exFAT — git cannot operate on it. All worker files live on eMMC (~3 GB used of 14 GB). If space becomes tight, the fix is to create an ext4 loop image on the SD card. Python 3.8 is in use (Ubuntu 18.04 constraint); upgrade to 3.10+ is worth doing before Google drops 3.8 support.

---

### The DNA Decoder — Near-Term Infrastructure Component

The DNA Decoder is a near-term infrastructure component that operationalizes the core claim of GLMP: that regulatory DNA sequence encodes a readable logical grammar. The decoder takes raw DNA strings as input and outputs machine-readable, queryable logical structure — the regulatory logic, protein products, and control relationships encoded in the sequence — in a format interoperable with the major biomedical knowledge graph ecosystem.

This is not a long-horizon goal. It is the next infrastructure build. The architecture described below is a **candidate prototype design** — tool choices and the division of compute between Jetson and GCP are working assumptions to be validated during Month 1 development, not settled production decisions.

The theoretical framework is already in place (Papers I–II), the ground-truth training circuits are being assembled (Batches 1–3 of the flowchart expansion), and the edge compute node (Jetson) is operational. The decoder is the component that closes the loop between sequence input and logical structure output.

**Pipeline architecture — five stages:**

1. **Raw DNA string in** — sequence input, organism and genomic context metadata
2. **Feature identification** — promoters, operators, ribosome binding sites, coding sequences, terminators; for eukaryotes, enhancers and CTCF boundary elements. Candidate tools: FIMO (motif scanning against JASPAR/HOCOMOCO), prokka (prokaryotic annotation), or MEME suite for de novo discovery.
3. **Regulatory logic extraction** — identification of TF binding site arrangements; spatial geometry (inter-site distances and orientations) parsed against the GLMP grammar rules:
   - AND: ~15–50 bp cooperative spacing
   - XOR/competitive: <15 bp steric exclusion
   - OR: >50 bp independent action
   - NOT: repressor binding site overlapping or adjacent to RNAP binding site
4. **Protein product prediction** — coding sequence identification and translation product annotation via UniProt/RefSeq lookup
5. **Logical structure output** — Biolink Model-compliant property graph: nodes typed as Gene, Protein, BiologicalProcess, MolecularActivity; edges typed as *regulates*, *produces*, *controlled_by*, *inhibits*; serialized in KGX format (TSV) for interoperability with Monarch Initiative, NCBI Knowledge Graph, RTX-KG2, and related resources

**Jetson's role in the decoder pipeline:**

The Jetson handles stages 1–3: sequence intake, feature identification, and regulatory logic extraction. These are computationally bounded, parallelizable tasks well-suited to edge compute. Stages 4–5 — protein annotation and knowledge graph output — are pushed to GCP. The result is a clean division: local sequence parsing on the Jetson, cloud-side knowledge graph assembly and storage.

This architecture means the decoder can process raw DNA strings continuously without GCP compute costs on the parsing-intensive upstream stages.

**Output representation:**

The canonical output is a Biolink-compliant property graph stored in Neo4j (AuraDB managed on GCP). Biolink Model is the shared semantic layer used by the major bio knowledge graph projects, making decoder output natively queryable alongside existing curated biological knowledge. KGX format (TSV) is the interchange standard.

Mermaid flowcharts remain the visualization and publication layer — generated from the property graph on demand, not stored as canonical representation. The property graph is what gets queried at scale; the Mermaid diagram is what appears in papers and demos.

**Interoperability target:**

The decoder's output is designed from the start to plug into the existing bio KG ecosystem: Monarch Initiative, NCBI Knowledge Graph, RTX-KG2, and Biolink-compatible projects. Standard identifiers (NCBI Gene IDs, UniProt accessions, GO terms, SO terms for sequence features) are used throughout. This makes decoded circuits citable, queryable, and combinable with external biological knowledge without ETL work.

**Krampis contribution:**

Biological validation of the decoded logical expressions is the critical quality gate. For each circuit class in the ground-truth batches, Krampis validates that the decoder's output accurately reflects the molecular biology — that the identified binding sites, spatial geometry interpretations, and logical connective assignments are correct. This validation loop is what distinguishes the DNA decoder from a pattern-matcher: the grammar rules are empirically grounded, not just computationally inferred.

**Near-term milestones:**

- **Month 1:** Decoder prototype on prokaryotic circuits (Batch 2 — E. coli lac operon, arabinose operon, trp operon). Fully characterized, linear sequence logic, ground truth available. Validates the pipeline architecture end to end.
- **Month 2–3:** Extend to synthetic biology ground-truth set (Batch 1 — repressilator, toggle switch, IFFL). Tests whether the grammar rules correctly parse designed circuits with known logical behavior.
- **Month 3–4:** First KGX output posted to HuggingFace Dataset. Citable, downloadable, visible to the sequence modeling community.
- **Month 6+:** Extension to human Class IIIa circuits (Batch 3) with chromatin accessibility context from multiome data.

*Note: Tool choices (FIMO, MEME, prokka, Neo4j AuraDB) are candidates rather than commitments — to be firmed up as the prototype is built. The Biolink/KGX interoperability framing positions this as infrastructure the bio community can build on, not just a GLMP internal tool.*

---

### Public Presence — HuggingFace, GitHub, and Project Home Page

The project is currently distributed across three platforms that serve different audiences and should be kept in explicit coordination:

**HuggingFace Space** — https://huggingface.co/spaces/garywelz/glmp
The interactive demo layer. Currently hosts the Mermaid flowchart browser. The space should be progressively expanded to reflect the grammar-decoding program:
- Near-term: add the GitHub repository link and paper DOIs prominently in the space description; rewrite the space metadata description to a one-sentence statement of the Big Picture Goal
- Medium-term: add a circuit class lookup tool (given a gene name, return its GLMP complexity class and the source flowchart)
- Longer-term: sequence annotation explorer; grammar-aware sequence model demo

The HuggingFace ecosystem is also a direct resource for the grammar-decoding program. The model hub hosts sequence models (Enformer, Nucleotide Transformer, DNABERT-2, and others) that are candidates for fine-tuning on the GLMP sequence-logic annotation corpus. As the annotated flowchart dataset grows, publishing it as a HuggingFace Dataset makes it citable, downloadable, and visible to the sequence modeling community — the primary potential users of the grammar-decoding training data.

**GitHub Repository** — https://github.com/garywelz/glmp/tree/main/collaborations/krampis-virtual-cell
The collaboration source of truth. Working papers, annotation schemas, classification protocols, and pull request workflow for Krampis. Not the public face of the project — the functional backbone.

**Project Home Page** — recommended addition: a simple static page served via GitHub Pages at `garywelz.github.io/glmp` (enabled by adding `docs/index.html` to the repository root). This serves as the research home for audiences arriving from bioRxiv, journal citations, or Google Scholar — biologists and reviewers who need to see a research project, not an app demo. Contents: Big Picture Goal statement, paper series with DOIs, links to GitHub repo, HuggingFace space, CopernicusAI, and ORCID. One page, no maintenance overhead.

**Division of platforms:**
- HuggingFace: ML community, computational biology tool users, model fine-tuning, dataset publication
- GitHub: active collaborators, version control, pull request review
- GitHub Pages project home: biologists, journal reviewers, potential collaborators arriving from papers
- GCP / CopernicusAI: paper ingestion, embedding retrieval, production infrastructure

---

### GLMP Flowcharts — Current Status and Expansion Plan

**Current live collection**

The GLMP flowchart collection is actively maintained and has grown substantially beyond the initial set. As of June 2026, the live collection contains **206 flowcharts across 8 organisms**, spanning prokaryotic circuits, human regulatory circuits, plant and animal developmental circuits, and selected synthetic biology examples. However, the collection requires a systematic QA pass before it can be used as a training corpus: known issues include class assignment inconsistencies, loop topology errors in some charts, and incomplete or unverified sequence annotations. A QA pass over the existing collection — particularly lac operon and related Class II circuits — is a prerequisite for the sequence annotation pipeline. This QA task is joint work with Krampis.

**Next expansion targets — after QA pass is complete**

New expansion resumes only after the QA/correction pass on the existing collection is complete. Expansion proceeds in priority order based on value to the grammar-decoding program:

**Batch 1 — Synthetic biology ground-truth set (~50 charts)**
Repressilator, toggle switch, incoherent feed-forward loop (IFFL), and variants. Completely characterized sequences, experimentally validated logic, known class assignment (I–IV). Every chart is a high-confidence sequence-logic training pair. This batch validates the sequence annotation pipeline before scaling.

**Batch 2 — Prokaryotic logic set (~150–200 charts)**
E. coli and related prokaryotes: SOS response, nitrogen regulation, arabinose operon, trp operon, phage lambda switch, sporulation network. Prokaryotic circuits have the cleanest sequence-to-logic mapping (no chromatin, no enhancers, mostly linear sequence logic) and are ideal for grammar decoding. RegulonDB covers ~4,500 regulatory interactions in E. coli alone. This batch provides the purest available ground truth. *The lac operon is the anchor circuit for this batch, pending QA completion.*

**Batch 3 — Human Class IIIa persistent bistable circuits (~100–200 charts)**
Hematopoietic fate switches (GATA1/PU.1, SCL/TAL1, C/EBPα, Ikaros), proliferative lock-in (MYC), oxygen sensing (VHL–HIF), DNA damage response (p53-MDM2). These are the circuits most important for cancer biology and drug resistance, and the circuits where grammar-aware models gain the most advantage. Each chart directly supports the RPE1 replication and RegVelo comparison.

**Batch 4 — Temporal logic circuits (~100 charts)**
Circadian clocks (CLOCK–BMAL1–PER–CRY), developmental oscillators (Notch–Hes1 segmentation clock, Wnt pulses), cell cycle oscillators. These implement the temporal logic operators from Paper II — NEXT, UNTIL, and their recursive extensions — requiring understanding of how delay is encoded in sequence (cascade depth, intronic delays, mRNA stability elements in 3′ UTRs).

**Batch 5 — Cross-organism comparative set (~200 charts)**
For circuits in Batches 1–4, generate equivalent charts for orthologous circuits in a second or third organism. Tests the universal grammar hypothesis directly: AND gate logic should be recoverable from homologous antiviral response circuits in mouse, zebrafish, and Drosophila despite different TF binding motifs. Topology more conserved than molecular identity is a falsifiable prediction.

**Batch 6 — Large-scale pipeline output (~1,000–2,000 charts)**
LLM-from-text pipeline applied systematically to Tier 1 and Tier 2 CopernicusAI papers. Lower individual confidence than curated batches, but provides statistical coverage for the literature-wide frequency distribution (Prediction 4, Paper II). Quality control: charts in Batches 1–4 circuit categories get manual review flag; others carry confidence annotation.

---

### The Sequence Annotation Layer — new infrastructure component

This is the component that does not yet exist and that transforms the GLMP flowchart collection into a grammar-decoding training corpus.

For each flowchart node representing a molecular binding event, annotation adds:
- The DNA sequence of the binding site
- The position weight matrix for the TF (from JASPAR/HOCOMOCO)
- Spatial context: distances to adjacent binding sites, orientation
- Organism and genomic coordinates
- Source paper (CopernicusAI DOI)

This transforms each node from a labeled box into a sequence-grounded data point. The logical connective at that node is now linked to a specific sequence arrangement. At scale, this is the training corpus for the grammar-aware sequence model.

Annotation is partially automated for TFs with known motifs in JASPAR. For less-characterized circuits, annotation requires literature curation from the Tier 1 CopernicusAI papers.

**Krampis contribution here:** For each circuit in the joint collaboration, provide or validate the sequence-level annotations linking flowchart logic to DNA sequence. This is a well-defined contribution leveraging molecular biology expertise directly in service of the grammar-decoding objective.

---

## Full Paper Trajectory

### Existing papers — foundation of the series

The five existing papers are fully described and cross-referenced in the Background section above, including GitHub filenames and GCS preview URLs. Their current status for this collaboration:

| Short name | Status |
|---|---|
| **Paper I** — *Primitive Relations, Computational Complexity, and a Conjecture on the Genomic Computational Class* | Draft complete; revision ongoing |
| **Paper II** — *The Genome as Computer* | Draft complete |
| **Paper III** — *Circuit Class Predicts Virtual Cell Model Accuracy* | Draft complete; RPE1 replication is Priority 1 of this collaboration |
| **Synthesis** — *Genomic Regulatory Complexity and the Limits of Perturbation Prediction* | GitHub working draft; not yet posted to bioRxiv |
| **Methods paper** — *Mermaid Flowcharts for Smarter Perturbation Design* | Draft complete; **under active revision** — sequence annotation layer and Big Picture framing being added; held for coordinated posting with replication paper |

---

### New papers — planned output of this collaboration

None of these exist yet. All are new work arising from the collaboration.

| Paper | Scope | Target venue | Timeline | Notes |
|---|---|---|---|---|
| **Replication paper** | RPE1 + RegVelo; grammar-aware comparison; Hypothesis 2 test | *PLOS Computational Biology* or *Genome Biology* | 3–4 months | First coordinated posting event; methods paper posts 2–4 weeks prior |
| **Bistability sub-classification** | IIIa/IIIb distinction; attractive conditionals; new predictions | *Cell Systems* Letters or *PLOS Biology* | 2–3 months | Can run in parallel with replication |
| **Multiome attractor paper** | Chromatin bimodality test; hidden state detection via ATAC/multiome | *Nature Methods* or *Genome Research* | 4–6 months | — |
| **Literature-scale circuit distribution** | CopernicusAI corpus annotation; class frequency across organisms and decades | *Bioinformatics* or *Nucleic Acids Research* | 12–18 months | — |
| **Sequence annotation paper** | Full annotation pipeline; first sequence-logic dataset from GLMP flowcharts; grammar recovery on ground-truth circuits | *Nucleic Acids Research* or *Genome Research* | 12–18 months | Builds on revised methods paper schema |
| **DNA Decoder paper** | Decoder pipeline end-to-end; prokaryotic + synthetic biology ground truth; KGX output; Biolink interoperability | *Nucleic Acids Research* or *PLOS Computational Biology* | 12–18 months | Directly reports the decoder infrastructure build |
| **Grammar-aware sequence model** | Sequence-to-logic classifier trained on annotated corpus; improvement over grammar-blind baselines on K562/RPE1 | *Nature Methods* or *Cell Systems* | 18–24 months | Long-horizon target; the grammar-decoding proof of concept |
| **Cross-organism topology conservation** | Batch 5 comparative analysis; topology more conserved than molecular identity across species | *Molecular Biology and Evolution* or *PLOS Genetics* | 18–24 months | — |

---

## Division of Labor (Proposed)

| Task | Welz | Krampis |
|---|---|---|
| Methods paper revision (reframing, new sections) | Primary | Review / biological validation |
| Sequence annotation schema definition | Pipeline design | Biological field validation |
| GLMP flowchart generation (Mermaid pipeline) | Primary | Review / validation |
| Sequence annotation (motif-to-logic linking) | Pipeline / automation | Biological validation |
| Circuit classification (TRRUST + literature) | Primary | Validation of edge cases |
| CopernicusAI database expansion and annotation | Primary | — |
| Jetson daily scout and ingest pipeline | Primary | — |
| DNA Decoder prototype (stages 1–3) | Primary | Biological validation of decoded output |
| Computational model evaluation (STATE, RegVelo) | Support | Primary |
| Multiome / chromatin analysis | Support | Primary |
| Biological interpretation and validation | Support | Primary |
| Cross-organism comparative analysis | Support | Primary |
| Theory, logic framework, paper writing | Primary | Review / co-author |

---

## Immediate Next Steps

**Working call agenda (suggested):**
- Review this document and align on priority order
- Define sequence annotation schema for GLMP flowchart nodes (joint task — one session)
- Agree on RegVelo configuration approach for K562 GRN
- Discuss DNA Decoder tool choices (FIMO vs. MEME vs. prokka for stage 2)
- Confirm forked repo workflow: Krampis forks https://github.com/garywelz/glmp and submits contributions via pull request

**Welz — begins immediately:**
1. Reframe methods paper abstract and introduction around the Big Picture Goal
2. Draft lac operon sequence annotation section (*lacO* sequence, CRP binding site, spatial context, logical interpretation)
3. Draft five-class connection section for methods paper
4. Download RPE1 benchmark data from scPerturb / Figshare and run RPE1 classification using existing `gene_circuit_classes.tsv` protocol
5. Run QA/correction pass on existing GLMP flowchart collection: class assignments, loop topology, complexity metadata, lac operon worked example, and sequence annotation consistency — prerequisite before any new batch expansion or sequence annotation pipeline work
6. Begin `flowchart-source-papers.tsv` manifest — circuit names and initial DOIs for existing flowcharts (can run in parallel with QA pass)
7. Script Firestore `glmp_relevant` backfill pass over existing 59K papers
8. Begin DNA Decoder prototype — prokaryotic circuits (Batch 2), FIMO/MEME evaluation

**Krampis — begins immediately:**
9. Co-lead QA/correction pass on existing GLMP flowchart collection — validate class assignments, loop topology, and complexity metadata; flag errors for correction before lac operon is used as worked example
10. Review lac operon sequence annotation section draft for biological accuracy (once QA pass is complete and Welz draft is ready)
11. Contribute to sequence annotation schema definition — field validation for human circuits beyond prokaryotes
12. Identify RegVelo configuration for K562 GRN
13. Review and extend `flowchart-source-papers.tsv` manifest — validate DOIs and fill gaps for hematopoietic and virtual cell circuits
14. Validate DNA Decoder output on Batch 2 prokaryotic circuits (Month 1 milestone)

**Joint — first coordinated deliverable (~3–4 months):**
- Methods paper revised draft → internal review → bioRxiv posting
- RPE1 replication results → combined with RegVelo comparison → replication paper submission
- DNA Decoder prototype on prokaryotic circuits → KGX output → HuggingFace Dataset posting

---

*Gary Welz · CUNY Graduate Center / New Media Lab · Genome Logic Modeling Project*
*gwelz@gc.cuny.edu · ORCID 0009-0005-7806-0892*
*Last updated: June 17, 2026*
