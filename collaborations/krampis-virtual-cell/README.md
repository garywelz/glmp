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
| `mermaid-perturbation-design-zenodo.pdf` | **Posted Zenodo preprint (PDF)** — version 1.6, June 28, 2026; PDF-only on Zenodo (figures embedded); Voigt framing included. DOI: https://doi.org/10.5281/zenodo.20831780. |
| `mermaid-perturbation-design-zenodo.md` | **GitHub archive Markdown** — same content as Zenodo PDF; not uploaded to Zenodo (source lives here with figure PNG links). |
| `teaching-deck-krampis-biochemical-process-modeling.md` | Proposal slide deck — GLMP overview oriented toward the Krampis collaboration and biochemical process modeling context. |
| `flowchart-circuit-classes.tsv` | Machine-readable circuit-class assignment for every microbial flowchart: class (I–V), topology type, rationale, evidence source, confidence, and `needs_review` flag. **The `needs_review = yes` rows are the validation worklist for Prof. Krampis.** |
| `COPERNICUS_GLMP_INTEGRATION.md` | **CopernicusAI ↔ GLMP integration status** — manifest, corpus gap analysis, classifier preview, scripts, and Firestore backfill checklist. |
| `flowchart-source-papers.tsv` | Canonical source paper per flowchart (DOI/PMID, expected Firestore id, manifest status). Drives curated Copernicus ingest and `glmp_relevant` tagging. |
| `copernicus-corpus-gap-report.tsv` | Per-process coverage vs local Copernicus JSON corpus; 216/217 source papers need curated ingest. |
| `curated-doi-ingest-priority.txt` | De-duplicated DOI list (192) for Copernicus curated-ingest mode. |
| `glmp-relevant-corpus-preview.tsv` | Dry-run `glmp_relevant` / `sequence_logic_content` flags on local paper corpus (no Firestore writes). |
| `flowchart-quality-audit.tsv` | Per-chart quality tier (A_OK / B_REVIEW / C_EXPAND) for the 109-chart ground-truth expansion batch. |
| `flowchart-quality-audit-summary.md` | Audit summary — recent median 6 nodes vs legacy 64; 13 thin charts expanded. |
| `lac-operon-annotation-review.md` | **Expert review request** — three lac operon binding-site annotations (lacO1 NOT gate, CRP AND input, *lacI* source node) for biological validation. |
| `dna-decoder/CURSOR_BRIEFING_DECODER_AUTOMATION.md` | Implementation brief: manifest-driven decoder batch runner, scout split (AM/PM), Firestore `glmp_circuits` + `scheduler_status`. |
| `dna-decoder/` | **DNA Decoder prototype** — Stage 3 logic parser (`glmp_logic_parser.py`) and lac operon technical report (FIMO + grammar rules, Jetson-validated). |
| `jetson/` | Jetson Nano ingest worker bootstrap script and setup handoff (CopernicusAI daily scout). |
| `jetson/scheduler/status_writer.py` | Phase 1 — Firestore job heartbeats (`scheduler_status` collection). |
| `jetson/setup_firestore_collections.py` | Phase 1 — Firestore bootstrap (dry-run by default; `--apply` for schema seeds). |
| `jetson/scout/scout_pubmed.py` | Phase 2 — split PubMed scout (+ GLMP query supplement). |
| `jetson/scout/README.md` | Phase 2 deploy and test instructions. |
| `three-machine-workflow-handoff.md` | Machine roles, SSH, credentials, and workflow rules for Yoga 730 / Yoga 9i / Jetson. |
| `JETSON_DECODER_HANDOFF_2026-06-24.md` | Morning handoff — SD migration, decoder (lac/ara/trp), scheduler bootstrap. |
| `JETSON_PHASE2_HANDOFF_2026-06-24.md` | **Latest Jetson handoff** — split scouts tested, cron live, ingest numbers corrected, next steps. |

---

## Live Flowchart Collection (updated 2026-06-13)

The interactive collection is the empirical companion to the papers. It now holds **217 process flowcharts**, each tagged with its position on the five-class complexity ladder (Paper I/III) and, increasingly, a **sequence → logic** annotation that maps cis-regulatory binding sites to the Boolean operator they implement — the core training pair of the Big Picture goal.

- **Browse / query:** [database table](https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-database-table.html) — sortable **Circuit class** column, class filter buttons (I–V), class-distribution panel, and CSV export (now including `circuit_class` and `topology_type`).
- **Per-process viewer:** each diagram page shows a colored **Class I–V badge** and, where curated, a **Sequence → Logic** table.

**Collection composition (217 total, 9 organisms):**

| Group | Count | Notes |
|---|---|---|
| E. coli | 68 | microbial regulatory + execution circuits (incl. ground-truth SOS, flagellar cascade) |
| Homo sapiens | 52 | **Batches 2–9** — curated human circuits (see breakdown below) |
| S. cerevisiae | 41 | yeast circuits (incl. ground-truth GAL, Whi5–SBF Start, Sup35 prion) |
| Synthetic circuit | 39 | **Batches 1–9** — ground-truth synthetic biology (see breakdown below) |
| Bacillus subtilis | 6 | developmental switches (incl. ground-truth ComK competence, Spo0A sporulation) |
| Mus musculus | 3 | **mouse ortholog ground-truth** — Gata1/Spi1 switch, Sox2/Oct4 pluripotency, p53–Mdm2 oscillator |
| Arabidopsis thaliana | 3 | **plant ground-truth** — circadian clock, FLC vernalization memory, ABA guard-cell homeostat |
| Drosophila melanogaster | 2 | **developmental ground-truth** — gap-gene network, wg/en/hh segment-polarity module |
| Caenorhabditis elegans | 2 | **developmental ground-truth** — dauer decision, lin-4/let-7 heterochronic timing |
| Bacteriophage λ | 1 | ground-truth CI/Cro lysis–lysogeny switch |

**Circuit-class distribution:** Class I 70 · Class II 72 · Class III 52 · Class IV 16 · Class V 7.

**Feedback topology:** across the 217 charts the collection carries a per-chart **loop count** (back-edges in the diagram) — **527 feedback nodes total, ~2.4 per process, 180 charts with at least one loop** — surfaced in the database table's *Loops* column and Σ/avg panel.

**Classification confidence:** of the 108 heuristically-classified microbial charts, **98 are high-confidence** (curated from literature) and **10 remain flagged `needs_review`** for expert validation after the 2026-06 QA pass. The open heuristic items are `ecoli_amino_acid_biosynthesis`, `ecoli_cell_division`, `ecoli_lac_operon`, `ecoli_mal_regulon`, `ecoli_sigma_factor_competition`, `ecoli_starvation_response`, `ecoli_transcription_regulation`, `yeast_cell_wall_integrity`, `yeast_yeast_cell_polarity`, and `yeast_yeast_glycolysis_regulation`. One authored human chart (`human_tnf_survival_death_decision`) is also flagged for topology/class review. The collection currently includes **121 charts with `sequenceAnnotation` blocks**; remaining legacy charts require sequence-level curation before being treated as training data.

**Ground-truth microbial/phage circuits (4)** anchor the ladder in classic organisms: the **GAL galactose** bistable switch and the **Whi5–SBF Start** switch (both Class IIIa, hysteretic cell-fate memory), the **phage λ CI/Cro** lysis–lysogeny switch (Class IIIa, the archetypal natural genetic switch), and the **[PSI+] Sup35 prion** — a genuine biological **Class V** self-modifying/epigenetic memory carried by protein conformation rather than DNA.

**Human circuits (47), classed by their real biology — not forced to one label.** Batch 8 adds innate-immunity and cell-fate circuits: RIG-I/MAVS antiviral amplification (III), the NLRP3 inflammasome (III), and the TNF survival-vs-death decision (III); cGAS–STING DNA sensing and the PERK–ATF4 integrated stress response (II); and the pancreatic β-cell glucose–insulin oscillator (IV). Batch 6 adds the PD-1/PD-L1 immune checkpoint, the IRE1–XBP1 unfolded-protein response, mTOR–ULK1 autophagy, and the PTEN–PI3K–AKT tumor-suppressor loop (all Class II negative-feedback homeostats), an estrogen-receptor positive-autoregulation switch (Class IIIa), and the IP3/Ca²⁺ CICR oscillator (Class IV). Batch 7 adds the AMPK energy homeostat, the iron IRP/IRE homeostat, cAMP/PKA GPCR desensitization, and glucocorticoid HPA-axis feedback (Class II), the p53 arrest-vs-apoptosis decision switch (Class III, complementing the p53–MDM2 oscillator), and the IL-6/STAT3 inflammatory positive-feedback switch (Class IIIa).
- **Class IIIa persistent bistable switches (7):** GATA1/PU.1 (hematopoiesis), OCT4–SOX2–NANOG (pluripotency), MyoD (myogenesis), T-bet/GATA3 (Th1/Th2), Rb–E2F (restriction point), p16–Rb (irreversible senescence), and ZEB/miR-200 (EMT).
- **Other Class III bistable / all-or-none switches (6):** Cdk1 mitotic trigger, caspase apoptosis, BCL-2/BAX MOMP, Notch–Delta lateral inhibition, ERK ultrasensitive switch, IRF7 interferon amplifier, SNAIL/miR-34 (EMT).
- **Class IV oscillators (4):** p53–MDM2, NF-κB/IκB, circadian BMAL1-CLOCK/PER-CRY, HES1 ultradian clock.
- **Class II negative-feedback / homeostats (11):** MYC, VHL–HIF, Wnt/β-catenin, TGF-β/SMAD, Hippo–YAP, JAK-STAT/SOCS, mTORC1, insulin–AKT–FOXO, SHH–GLI, NRF2–KEAP1, HSF1 heat-shock.

**Synthetic circuits (33)** are ground-truth anchors whose topology *and* dynamics are known by construction: negative/positive autoregulation, the Gardner–Collins toggle and a double-positive mutual-activation switch, the Elowitz–Leibler repressilator and a five-node ring, the Atkinson and Stricker oscillators, the Danino synchronized quorum-of-clocks population oscillator, coherent/incoherent feed-forward loops, a fold-change detector, transcriptional AND/OR/NOR and three-input AND gates, the Bonnet recombinase XOR gate, a Cello-style layered NOR cascade and Tamsir distributed-consortium logic, RNA attenuator logic, the Basu band-pass detector, sender/receiver quorum sensing, the You population-control circuit, the Levskaya light sensor and the Tabor multicellular edge detector, an optogenetic light-switchable bistable toggle, the Fung metabolator, theophylline-riboswitch and toehold riboregulators, the antithetic integral-feedback controller, a CRISPRi toggle, and two **Class V** self-modifying-DNA devices — an **integrase recombinase memory** and a **recombinase DNA counter / state machine** — that anchor the otherwise rare top rung of the ladder.

**Ground-truth microbial circuits** beyond the heuristic set now include the *E. coli* SOS DNA-damage response (LexA/RecA, Class II) and flagellar FlhDC→FliA cascade (Class I), and the *B. subtilis* ComK competence switch (Class IIIa) and Spo0A sporulation commitment (Class III) — textbook bacterial decision circuits with authored classes.

**Ground-truth plant circuits (Arabidopsis thaliana)** extend the collection to a new kingdom: the CCA1/LHY–TOC1 circadian oscillator (Class IV), the FLC Polycomb **vernalization memory** (Class V — a heritable, self-maintaining chromatin switch that records winter), and the ABA guard-cell stomatal homeostat (Class II).

**Ground-truth animal-developmental circuits** add two classic model organisms: from *Drosophila*, the gap-gene cross-repression patterning network and the wg/en/hh segment-polarity module (both Class III); from *C. elegans*, the insulin/TGF-β **dauer** developmental decision (Class III) and the lin-4/let-7 **heterochronic** microRNA timing cascade (Class I).

**Batch 9 (2026-06-13)** adds synthetic phosphorelay AND, CRISPRa layered activation, and protease AND gates (Class I); human SCL/TAL1, C/EBPα, and Foxp3 Class IIIa persistent switches plus TLR4/LPS inflammatory and BCL6 GC/plasma bistable circuits (Class III); and the first **mouse ortholog ground-truth** set (Gata1/Spi1, Sox2/Oct4, p53–Mdm2) for cross-organism grammar validation.

Reproducibility — the collection is regenerated by committed scripts: `scripts/classify_flowchart_circuits.py` (class assignment), `scripts/apply_circuit_classes.py` (write classes into JSON + metadata), `scripts/annotate_microbial_sequences.py` (sequence → logic on microbial circuits), `scripts/build_synthetic_batch1.py`…`_batch9`, `scripts/build_human_batch2.py`…`_batch9`, `scripts/build_microbial_groundtruth.py`/`_groundtruth2.py`, `scripts/build_plant_groundtruth.py`, `scripts/build_developmental_groundtruth.py`, and `scripts/build_mouse_groundtruth.py` (ground-truth batches), with `scripts/integrate_synthetic_batch1.py`, `scripts/integrate_microbial_groundtruth.py`/`_groundtruth2.py`, `scripts/integrate_plant_groundtruth.py`, `scripts/integrate_developmental_groundtruth.py`, and `scripts/integrate_mouse_groundtruth.py` (metadata integration), plus `scripts/backfill_loops.py` (per-chart feedback-loop counts). **Copernicus integration:** `scripts/build_flowchart_source_papers_manifest.py`, `scripts/check_manifest_corpus_coverage.py`, `scripts/classify_glmp_relevant_preview.py`, `scripts/export_curated_doi_ingest_list.py`, and `scripts/link_glmp_processes_to_papers.py` (see `COPERNICUS_GLMP_INTEGRATION.md`).

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
- The posted Zenodo methods preprint is `mermaid-perturbation-design-zenodo.pdf` (v1.6, PDF-only on Zenodo); the Markdown archive and editable working draft are `mermaid-perturbation-design-zenodo.md` and `methods-mermaid-perturbation-design.md` on GitHub.
