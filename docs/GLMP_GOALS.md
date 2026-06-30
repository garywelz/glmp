# GLMP Goals Statement
## Version: 1.0 — June 30, 2026
## Shared reference for Gary Welz, Claude (claude.ai), and Cursor

This document establishes shared goal alignment across the three-way
working relationship. It should be read by Cursor at the start of any
new session involving GLMP or related projects, and updated when goals
or priorities meaningfully shift.

---

## What GLMP is

The Genome Logic Modeling Project proposes that the spatial arrangement
of transcription factor binding sites in regulatory DNA encodes logical
operations — AND, OR, NOT — analogous to gates in a circuit. GLMP
builds a computational framework for reading and formalizing that logic,
classifying regulatory circuits by complexity class (I–V), and making
the results queryable through a unified knowledge engine.

This approach is the inverse of synthetic biology work (Voigt et al.,
Science 2016), which compiles human-readable logic programs into novel
DNA sequences. GLMP reads the logic already written in natural regulatory
DNA by evolution. The two share a grammar; they differ in direction.

---

## What we are building

A corpus of decoded regulatory circuits — starting with three validated
E. coli operons (lac, ara, trp) and expanding toward 300 then 1,000+
decoded processes — linked to their source papers, rendered as Mermaid
logic-gate flowcharts, and stored in a Firestore-backed knowledge engine.

The target user experience: a researcher queries a biological process
and receives a logic-gate flowchart, source papers, DNA decoding, and
eventually a podcast and knowledge graph — in one query.

---

## What the DNA decoder does and doesn't do

**Can decode:** circuits whose regulatory logic is geometrically encoded
in DNA — primarily prokaryotic repressor/operator systems where a
repressor physically occupies a sequence overlapping the RNAP binding
region. Examples: lac operon (Class III), ara operon (Class III),
trp operon (Class II).

**Cannot decode:** circuits whose logic depends on protein-protein
interactions with no DNA sequence signature — e.g. the yeast GAL
bistable switch, where Gal80 represses Gal4 by binding its activation
domain, and Gal3 sequesters Gal80 in the cytoplasm. These circuits
require a protein-network layer and curated annotation alongside any
partial DNA-level decode. This boundary is a documented scientific
finding, not a limitation to hide — it sharpens what the decoder
claims and strengthens the methods paper.

---

## Circuit complexity classes

| Class | Structure | Biological example |
|---|---|---|
| I | Feed-forward, no feedback | Simple inducible promoter |
| II | Single negative feedback | trp operon |
| III | Bistable / positive feedback | lac operon, ara operon |
| IV | Oscillatory | Circadian clock |
| V | Self-modifying | DNMT3A self-methylation |

Class III circuits are empirically harder for AI perturbation models
to predict — a finding with direct implications for the RegVelo and
K562 collaboration work.

---

## Scale and timeline

- **Now:** 3 decoded circuits (lac, ara, trp) — validated, in Firestore
- **~1 month:** 300 decoded circuits — primarily remaining prokaryotic
  and bacterial circuits, which are the highest-confidence decode targets
- **~3 months:** 1,000+ decoded circuits — expanding to eukaryotic
  circuits with appropriate two-layer schema where needed

The key constraint at scale is **selection** — deciding which of the
217 cataloged processes to decode next, and in what order — rather
than production speed. Priority order: remaining E. coli circuits,
then other bacterial organisms, then eukaryotic circuits with
proactive protein-network screening before running the decoder.

---

## Current priorities in order

**Priority 1 — Decoder automation**
Scale from 3 to 300 decoded circuits via YAML manifest-driven batch
runner (run_batch.py, not yet built). Prioritize prokaryotic/bacterial
circuits before eukaryotic ones. Each decoded circuit writes to both
glmp_circuits (granular binding-site data) and updates glmp_processes
(registry entry with two-layer schema where applicable).

**Priority 2 — Research papers corpus**
Grow to 100,000+ high-relevance biology papers. Scout query redesign
is live as of June 29 — targeting GLMP-specific biology topics
(gene regulation, transcription factors, systems biology, synthetic
biology) rather than the previous generalist intake. Track paper
→ flowchart → podcast linking via source_paper_ids field.

**Priority 3 — Biological validation**
Three-layer validation architecture:
- Layer 1: Expert biological hand-review of lac/ara/trp annotations
  (subject matter expert, to be named at publication)
- Layer 2: RegulonDB cross-reference of decoded binding sites
  (computational biology collaborator, to be named at publication)
- Layer 3: Evo 2 cross-validation via Arc Institute API (stretch goal)
Human expert collaborators are engaged and working; names will be
included in authorship when we are ready to publish.

**Priority 4 — Linking layer**
Connect decoded circuits to their source papers via the
biology:process: identifier namespace. Every glmp_processes document
should carry source_paper_ids; research_papers documents should
carry process_ids. ingest_queue collection (not yet built) will
allow flowchart and podcast generation to trigger targeted paper
ingestion.

**Priority 5 — Knowledge engine front end**
Honest, focused scope: computational genomics and regulatory biology.
Not presented as a general science search engine. CopernicusAI
front end to be recalibrated to reflect actual corpus focus.
Podcast generation and YouTube channel strategy deferred until
multimedia workflow is designed.

---

## What we are not doing right now

- Eukaryotic promoter geometry fixes in the parser (scoped, deferred)
- TDA / topological data analysis (set aside entirely)
- Mathematics, chemistry, physics knowledge engines (namespaced and
  reserved as future engines, not being built yet)
- Podcast generation at scale (waiting on multimedia workflow)
- Purging the existing 61,250-paper corpus (math arXiv papers are
  the seed corpus for the future mathematics knowledge engine)

---

## The paper program

GLMP is supported by an 8-paper research program. Cursor is an active
participant in the authorship workflow — it creates PDFs and final
submission versions of papers and should be kept current on all
manuscripts. Current paper status:

| Paper | Title (short) | Status |
|---|---|---|
| Methods paper | Mermaid Flowcharts for Perturbation Design | Zenodo DOI: 10.5281/zenodo.20831780; targeting PLOS Computational Biology or Briefings in Bioinformatics |
| Synthesis paper | Genomic Regulatory Complexity and Perturbation Prediction | In GLMP repo (synthesis-biorxiv.md); revision pending |
| Mathematics paper | Proof Graphs and Algorithm Capsules | Zenodo DOI: 10.5281/zenodo.20510602 v2.0; arXiv deposit pending via Hunter Johnson (John Jay/CUNY) |
| Programming Framework paper | AI Knowledge Engines as Research Infrastructure | Under review at Learned Publishing (Wiley/ALPSP) |
| Knowledge Engine paper | AI-Powered Knowledge Engines | Under review at Discover AI (Springer Nature) after major revision |
| Papers 1-5 (GLMP series) | Various — biological validation, empirical, eukaryotic extension | In progress |

All papers live in GitHub repos that Cursor has indexed:
- github.com/garywelz/glmp — primary GLMP repo
- github.com/garywelz/copernicus-web — knowledge engine infrastructure
- Additional repos may be referenced in future sessions

When Gary indicates a paper is approaching submission, Cursor should
expect to be asked to: check formatting and citation consistency,
generate the final PDF, verify all referenced URLs and DOIs resolve,
and prepare supplementary materials as needed.

---

## The working method

**Gary** — makes all strategic and scientific decisions; sets priorities;
engages human collaborators; is the corresponding author on all papers.

**Claude** (claude.ai, "Cross Platform Workflow" chat) — provides
architecture design, strategic analysis, editorial review, and
handoff documents. Does not execute code directly but drafts
all Cursor handoffs and interprets Cursor's reports. Maintains
the research log and to-do list across sessions.

**Cursor** — executes implementation with the full codebase indexed.
Has deep familiarity with all repo contents. Should use that knowledge
actively — if something in the existing code contradicts a handoff
assumption, flag it before proceeding. Preferred mode is dialogue
before execution on anything significant.

**Claude Code** — available for Jetson remote work, SSH pipeline
execution, and tasks that benefit from a terminal-first approach.

**Workflow protocol:**
1. Claude drafts handoff documents with strategic context
2. Cursor reads handoff, checks against indexed codebase knowledge,
   flags any contradictions or uncertainties BEFORE executing
3. Gary mediates — consults Claude when needed, gives final approval
4. Cursor executes, reports back in structured format:
   - What I found (before executing)
   - What I did
   - What I'm uncertain about
   - What to discuss with Claude

This dialogue model is deliberate. Cursor should never resolve
strategic ambiguity by picking an approach and running silently —
raise it, get alignment, then execute.

---

## Identifier namespace (established)

All knowledge engine objects use:
```
{discipline}:{object-type}:{slug}
```

Examples:
```
biology:process:lac-operon
biology:process:gal-system-yeast
math:algorithm:merge-sort
math:theory:group-theory
math:proof:godel-incompleteness
```

Project affiliation (e.g. glmp) is stored as a metadata field,
not baked into the identifier, to keep IDs lean and URL-safe.

---

## Key infrastructure

| Component | Location | Notes |
|---|---|---|
| Jetson Nano | gary@192.168.1.222 | Edge compute; runs cron scouts and decoder |
| Firestore | regal-scholar-453620-r7 / copernicusai | research_papers (62k+), glmp_processes (217) |
| GCS bucket | regal-scholar-453620-r7-podcast-storage | Static assets, HTML viewers, metadata |
| Cloud Run API | copernicus-podcast-api-phzp4ie2sq-uc.a.run.app | Browse/search API |
| GLMP GitHub | github.com/garywelz/glmp | Decoder pipeline, process catalog, papers |
| Copernicus GitHub | github.com/garywelz/copernicus-web | Knowledge engine infrastructure |
| Embeddings | OpenAI text-embedding-3-small (1536-d) | Frozen — do not change |
