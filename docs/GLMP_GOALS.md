# GLMP Goals Statement
## Version: 1.1 — June 30, 2026
## Shared reference for Gary Welz, Claude (claude.ai), and Cursor

**v1.1 changes:** Align operon class examples with `glmp-v2` catalog JSON;
add two-field decoder schema (`dna_topology_class` vs `glmp_biological_class`);
soften “3 validated decodes” to match current Firestore/decoder status.

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

A corpus of decoded regulatory circuits — starting with three E. coli
operons (lac, ara, trp) plus the yeast GAL bistable switch as a
two-layer reference case — expanding toward 300 then 1,000+ decoded
processes. Each process is linked to source papers, rendered as a Mermaid
logic-gate flowchart, and stored in a Firestore-backed knowledge engine.
Ground-truth decoder outputs live in `dna-decoder/results/` (v0.2.2).

The target user experience: a researcher queries a biological process
and receives a logic-gate flowchart, source papers, DNA decoding, and
eventually a podcast and knowledge graph — in one query.

---

## What the DNA decoder does and doesn't do

**Can decode (DNA topology):** circuits whose regulatory logic is
geometrically encoded in DNA — primarily prokaryotic repressor/operator
systems where a repressor physically occupies a sequence overlapping the
RNAP binding region. Current pipeline status (parser v0.2.2):

| Process | DNA topology (`dna_topology_class`) | Curated biological class (`glmp_biological_class`, from catalog) |
|---|---|---|
| trp operon | I/II (high confidence) | II |
| lac operon | II (high confidence) | II |
| ara operon | INSUFFICIENT_EVIDENCE (no AraC PWM yet) | III |
| GAL bistable switch | I (partial — activator sites only) | III / IIIa |

Biological class always comes from the YAML manifest / `glmp-v2` catalog —
never inferred from FIMO. See **Two-field circuit classification** below.

**Cannot decode (full mechanism):** circuits whose logic depends on protein-protein
interactions with no DNA sequence signature — e.g. the yeast GAL
bistable switch, where Gal80 represses Gal4 by binding its activation
domain, and Gal3 sequesters Gal80 in the cytoplasm. These circuits
require a protein-network layer and curated annotation alongside any
partial DNA-level decode. This boundary is a documented scientific
finding, not a limitation to hide — it sharpens what the decoder
claims and strengthens the methods paper.

---

## Circuit complexity classes

These are **biological** complexity classes (I–V), as assigned in the
`glmp-v2` process catalog (`circuitClass` → Firestore `glmp_biological_class`).
They are distinct from **DNA topology class**, which the decoder infers
from FIMO binding-site geometry and may differ (e.g. GAL: biological IIIa,
DNA topology I).

| Class | Structure | Catalog example (`glmp-v2`) |
|---|---|---|
| I | Feed-forward, no feedback | Simple inducible promoter |
| II | Single negative feedback | trp operon; lac operon* |
| III | Bistable / positive feedback | ara operon |
| IV | Oscillatory | Circadian clock |
| V | Self-modifying | DNMT3A self-methylation |

\* **lac operon:** catalog assigns Class II (Jacob–Monod negative feedback);
`circuitClassNeedsReview: true` — Mermaid topology currently shows `loops: 0`
despite Class II. Resolve in catalog QA before using lac as the primary
worked example in papers.

**Authoritative source:** `glmp-v2/processes/{organism}/{process_id}.json`.
If this goals doc and the catalog disagree, the catalog wins until Gary
updates one or the other deliberately.

Class III circuits are empirically harder for AI perturbation models
to predict — a finding with direct implications for the RegVelo and
K562 collaboration work.

---

## Two-field circuit classification (decoder schema)

As of parser v0.2.2 (June 2026), every decode distinguishes:

| Field | Source | Meaning |
|---|---|---|
| `dna_topology_class` | Parser (FIMO + grammar rules) | What binding-site geometry supports (I, I/II, II, `INSUFFICIENT_EVIDENCE`, etc.) |
| `dna_topology_confidence` | Parser | `high` / `medium` / `partial` / `insufficient` |
| `dna_topology_note` | Parser | Human-readable caveat when evidence is weak |
| `glmp_biological_class` | YAML manifest / catalog only | Curated GLMP complexity class (I–V) |
| `glmp_biological_subclass` | Manifest / catalog | e.g. `IIIa` for GAL |
| `glmp_biological_class_source` | Fixed | `curated_catalog` when manifest supplied |
| `circuit_class` | Deprecated mirror | Same value as `dna_topology_class` (Jetson JSON backward compat) |

Manifests live in `dna-decoder/manifests/`. Custom PWMs for TFs absent
from JASPAR are tracked in `dna-decoder/motifs/custom_pwm_registry.yaml`
(LacI and TrpR active; AraC pending).

For protein-network-dependent circuits, Firestore also carries nested
`dna_decodable_layer` + `protein_network_layer` objects (established on
`yeast_gal_bistable_switch`).

---

## Scale and timeline

- **Now:** 3 E. coli operons with decoder runs + Firestore entries (lac/trp:
  confident DNA topology; ara: DNA-level insufficient pending AraC PWM);
  GAL two-layer reference decode in Firestore. Catalog QA and Layer 1–3
  biological validation still in progress — decoder outputs are ground truth
  for the pipeline, not yet publication-validated annotations
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
Scale from 4 reference decodes (lac, ara, trp, GAL) to 300 via YAML
manifest-driven batch runner (`run_batch.py`, not yet built). Prioritize
prokaryotic/bacterial circuits before eukaryotic ones. Each decode uses
`--manifest` for biological class; writes update `glmp_processes` with the
two-field flat schema (and nested two-layer objects where applicable).
Granular binding-site collection (`glmp_circuits`) is planned but not
yet wired.

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
