# GLMP + CopernicusAI — Master To-Do List
## Last updated: July 2, 2026 (SOS Class II decodes + batch queue expansion)
## Paper count (API): **62,173** (was 62,119 PM June 30 — **+54** overnight)
## For: Cursor (shared from Gary + Claude, Cross Platform Workflow session)
## Read alongside: docs/GLMP_GOALS.md (v1.1, commit 0f74ec7)

### July 1 scout status — **v2 confirmed working in production**

| Scout | Fired? | Fetched (daily log) | New JSON (`doc_delta`) | Ingest → Firestore |
|-------|--------|---------------------|------------------------|-------------------|
| pubmed_pm (Jun 30 ~8 PM ET) | ✅ | 500 + 79 GLMP supplement | low (dedup) | see ingest log |
| pubmed_am (Jul 1 ~10:15 AM ET) | ✅ | 500 + 79 GLMP supplement | +2 | **53 new** @ 10:30 AM ingest |
| biorxiv_am | ✅ | — | +13 | — |
| arxiv_am/pm | ✅ | v2 config loaded | +0 | — |

- **v2 GLMP queries confirmed:** `daily_scout_config.json` v2.0, `config_queries=yes`, 10 biology MeSH queries, 500 papers/run, exit code 0
- **Sample titles:** gene regulation, TF binding, chromatin — not math arXiv noise
- **Low +54 overnight explained:** ingest scanned 49,822 JSON files, wrote **53** to Firestore, skipped **49,769** duplicates (~99.9% skip rate)
- **Split log misleading:** subprocess detail in `paper_acquisition_logs/daily_scout/pubmed_*_YYYYMMDD.log`; stdout buffering can place startup banner after success line
- **~~Open issue (closed):~~** v2 runs not completing — **incorrect**; see daily scout logs

---

## PRIORITY 1 — GLMP Phase 3 (Decoder Automation)

The schema is clean, the catalog is fully synced at 217 processes,
four reference decodes are in Firestore (lac, ara, trp, GAL).
Phase 3 batch runner **live** July 1, 2026 — cron at 2 AM ET on Jetson.

- [x] Design batch runner architecture — `select_batch.py` + `queue/` + `run_batch.py`
- [x] Build `select_batch.py` — ranks glmp_processes, writes manifests from glmp-v2 catalog
      (`circuitClass` mapping, `--yes` for cron, fixed `_status` check, tie-break: class then alpha)
- [x] Build `run_batch.py` — manifest queue processor, NCBI fetch, FIMO, parser, Firestore
      (FIMO path resolves meme-env bin on Jetson)
- [x] Queue directory structure — pending/running/completed/failed under `dna-decoder/queue/`
- [x] First batch manifests queued (4) with RegulonDB/literature coordinates:
      `ecoli_flhdc_flagellar`, `ecoli_sos_reca`, `ecoli_sos_lexa`, `ecoli_lambda_switch`
- [x] Fetch + commit first-batch `.fa` sequences to `dna-decoder/sequences/`
- [x] GLMP repo on Jetson at `/media/sdcard/glmp/`; motifs symlink → `/media/sdcard/decoder/motifs`
- [x] `run_batch_cron.sh` wrapper + PyYAML/Firestore in meme-env
- [x] **Cron 2 AM ET** — installed via `run_batch_cron.sh` (limit 10/night)
- [x] **First live test (July 1):** `ecoli_flhdc_flagellar` — pipeline COMPLETE end-to-end;
      `glmp_circuits/ecoli_flhdc_flagellar` written; `dna_topology_class=INSUFFICIENT_EVIDENCE`
      (JASPAR eukaryote-weighted hits only — no σ70/CAP prokaryotic PWM match yet);
      `glmp_biological_class=I` from manifest/catalog preserved correctly
- [x] Build LexA custom PWM (`lexA_sos.meme`, 16 bp) — **done July 1**; FIMO validated on recA promoter;
      **July 2 cron:** `ecoli_sos_reca` + `ecoli_sos_lexa` both `dna_topology_class: II` in
      `glmp_circuits` — LexA PWM production-validated
- [x] Fix `phage_lambda` parser organism enum + geometry warning — **July 2**; `ecoli_lambda_switch`
      re-queued for cron (expect `INSUFFICIENT_EVIDENCE` until CI/Cro PWMs built)
- [x] Fix `select_batch.py` `--organism ecoli_k12` filter (`ecoli` ≡ `ecoli_k12`); add `--circuits`
- [x] Queue second E. coli batch (10 manifests, `_status: coordinates_needed`) — **July 2**;
      Gary-approved list: catabolite_repression, amino_acid/arginine biosynthesis,
      anaerobic/aerobic respiration, dna_damage_checkpoint, cold_shock, antibiotic_efflux,
      base_excision_repair, osmotic_stress — **11 pending on Jetson** (+ lambda_switch)
- [ ] Build λ CI/Cro custom PWMs (`lambda_ci_or.meme`, `lambda_cro_or.meme`) — two separate matrices
- [ ] Build AraC custom PWM — two separate matrices:
      AraC_repressor (araI1-araO2 loop binding geometry)
      AraC_activator (araI1-araI2 binding geometry)
      See custom_pwm_registry.yaml — AraC is marked pending
- [ ] Begin batch decoding: priority order is
      1. 66 remaining E. coli circuits (same pipeline as lac/ara/trp)
      2. 39 synthetic circuits (designed logic-gate circuits)
      3. 6 Bacillus (prokaryotic, needs custom PWMs)
      See DECODER_EDGE_CASES.md for full priority rationale
- [ ] Design and create glmp_circuits Firestore collection —
      granular binding-site-level data separate from the process
      registry (glmp_processes holds summary; glmp_circuits holds
      full binding site coordinates, q-values, FIMO details)
      **Status:** collection exists (`_schema` placeholder); run_batch wired to write per-decode docs
- [ ] Add source_paper_ids to decoded circuit documents in
      glmp_processes — linking layer connecting circuits to papers
- [ ] Scale to 300 decoded circuits (target: ~1 month),
      then 1000+ (target: ~3 months)

---

## PRIORITY 2 — Research Papers → 100,000

Scout query redesign is live as of June 29 but the split scheduler
on Jetson had a config mismatch that was fixed June 30. First clean
production run should be tonight (10:15 PM ET) or tomorrow AM.

- [x] Verify Jul 1 AM scout run — **done:** v2 working, 500/run, GLMP biology
      titles verified; low Firestore delta = dedup + ingest skip rate
- [x] Wire `PUBMED_API_KEY` into cron env (`pubmed-api-key` secret)
- [x] Improve acquire logging: fetched vs new vs updated JSON in logs
- [ ] Design targeted ingest — scout writes manifest of new JSON paths;
      ingest processes manifest only, not full 50k-file tree
- [ ] Re-run corpus audit in ~1 week to measure quality improvement
      from 2% GLMP-relevant baseline (Grade D) toward target 40%+
- [ ] Design and build ingest_queue Firestore collection —
      allows flowchart/podcast generation to trigger targeted paper
      ingestion by DOI/PMID
- [ ] Build queue_worker.py on Jetson — reads ingest_queue,
      ingests specific papers, marks complete
- [ ] Add process_ids and used_in_flowcharts reverse index fields
      to research_papers documents (linking layer)
- [ ] Targeted PubMed backfill — three passes:
      Pass 1: landmark papers only (pre-2018, ~500-1000 papers)
      Pass 2: methods era 2018-2021 (~15,000 papers)
      Pass 3: recent gap fill 2022-2023 (~25,000 papers)
- [ ] Fix papers-database-table.html — add no-JS fallback for
      static visitors (JS-rendered version works, static doesn't)
- [ ] Narrow CopernicusAI front-end scope description — honest
      framing as computational genomics / regulatory biology,
      not general science search engine

---

## PRIORITY 3 — Biological Validation

Three-layer validation architecture in progress. Waiting on
collaborator responses.

- [ ] Awaiting Krampis reply — next week evening Zoom,
      student background (biology-strong vs computation-strong)
- [ ] When confirmed: draft student-facing email with two
      assignment tracks clearly presented
      Track A (biology): lac/ara/trp annotation review,
        RegulonDB cross-reference
      Track B (computation): RPE1, RegVelo on K562,
        Evo 2 cross-validation via Arc Institute API
- [ ] Lac circuitClassNeedsReview: true — defer to validation
      team (Lents + student) — do not resolve unilaterally
- [ ] Arc Institute outreach — Evo 2 cross-validation proposal
      (CUNY institutional connection; frame around GLMP as
      inverse of synthetic biology compilation)

---

## PRIORITY 4 — Infrastructure and Linking Layer

- [ ] glmp_circuits collection — design schema, create in Firestore
      Field design:
        process_id (biology:process:lac-operon namespace)
        binding_sites (array of site objects with coordinates,
          TF, q-value, jaspar_id or custom_pwm_id)
        fimo_run_params (thresholds, motif files used)
        decoder_version
        source_paper_ids
        created_at, updated_at
- [ ] biology:process: identifier namespace — already designed,
      not yet written to documents; add process_id field to
      glmp_processes documents as the canonical slug
      (e.g. biology:process:lac-operon)
- [ ] Firestore composite index on research_papers.updated_at DESC
      — already created June 29, confirmed Enabled
- [ ] Fix papers-database-table.html pagination no-JS fallback
      (from todo list, lower urgency than above)

---

## PRIORITY 5 — Programming Framework Flowchart Growth

- [ ] Design overnight cron batch generator —
      ~10 new flowcharts per discipline per night,
      midnight-7 AM schedule, Jetson or Yoga 9i
      Disciplines: Mathematics, Chemistry, Biology,
      Computer Science, Physics
- [ ] Evaluate grammar-constrained local LLM for Mermaid
      flowchart generation (Ollama + Gemma 3 12B on Yoga 9i)
      Run 50-paper benchmark first; verify Blackwell CUDA
      compatibility before wiring into pipeline
- [ ] Larger-scale Math DB and GLMP DB enhancements —
      coordinate selections with Gary before automating

---

## PRIORITY 6 — Video DB and Podcast

- [ ] Audit sciencevideodb ingestion script
- [ ] Deploy video ingestion as overnight cron job on Jetson
- [ ] Develop enhanced podcast workflow —
      graphics, animations, video overlay — before scaling
- [ ] Plan multi-channel YouTube strategy for enhanced
      scientific podcasts
- [ ] Only then automate podcast generation at scale

---

## KNOWN ISSUES / OPEN QUESTIONS

- AraC custom PWM: two-matrix design confirmed (repressor +
  activator); build is next decoder task after batch runner
- Eukaryotic promoter geometry (EC-3): parser still uses
  prokaryotic -35/-10 assumptions; geometry_warning field
  added but real fix deferred
- 26-file deletion bundled in commit aa2ba0c22 (Windows-
  incompatible Crossref JSON filenames) — cleanup optional,
  not blocking anything
- Lac biological class: circuitClassNeedsReview: true in
  catalog — catalog wins until validation team resolves it
- Monitor arXiv API reliability — add retry logic if 500 errors
  persist across 3+ consecutive scout runs (Jul 2 AM: transient
  export.arxiv.org 500s on all 4 v2 queries; PM scout will retry)

---

## INFRASTRUCTURE REFERENCE

| Component | Location | Notes |
|-----------|----------|-------|
| Jetson | gary@192.168.1.222 | Edge compute; cron scouts + decoder |
| Firestore | regal-scholar-453620-r7/copernicusai | research_papers (62k+), glmp_processes (217) |
| GCS | regal-scholar-453620-r7-podcast-storage | Static assets, HTML viewers |
| Cloud Run API | copernicus-podcast-api-phzp4ie2sq-uc.a.run.app | Browse/search API, pagination fixed June 29 |
| GLMP GitHub | github.com/garywelz/glmp | Decoder pipeline, catalog, papers |
| Copernicus GitHub | github.com/garywelz/copernicus-web | Knowledge engine infrastructure |
| Embeddings | OpenAI text-embedding-3-small (1536-d) | Frozen — do not change |
| Scout logs | /media/sdcard/logs/ on Jetson | Check after each cron cycle |

---

## RECENT COMPLETED WORK (June 29 – July 1, 2026)

For context — do not redo any of these:

- ✅ API browse pagination bug fixed (order_by __name__ then
     restored to updated_at DESC with composite index)
- ✅ papers-database-table.html pagination + links fixed
- ✅ Scout query redesign — GLMP biology focus replacing
     generalist/math-heavy intake
- ✅ Split scheduler wired to v2.0 config (scout_common.py fix)
- ✅ glmp_processes synced to full 217 (was 108)
- ✅ 217/217 embeddings confirmed
- ✅ GAL1 exploratory decode — first eukaryotic circuit
- ✅ Two-layer schema (dna_decodable + protein_network) established
- ✅ Parser v0.2.2 — two-field circuit class schema
- ✅ First Firestore decoder entries: lac, ara, trp, GAL
- ✅ Custom PWM registry scaffold (+ LexA, λ CI/Cro pending entries July 1)
- ✅ Phase 3 batch runner live — cron 2 AM ET, first live decode flhDC July 1
- ✅ DECODER_EDGE_CASES.md with real organism counts
- ✅ GLMP_GOALS.md v1.1 committed and catalog-aligned
- ✅ Krampis email sent with GLMP From Square One PDF
- ✅ LexA SOS box custom PWM (`lexA_sos.meme`, 16 bp, 21 sites) — FIMO-validated on recA;
      sos_reca/sos_lexa manifests wired; Jetson synced for 2 AM cron SOS decode
- ✅ **July 2 batch:** SOS decodes Class II (`glmp_circuits`); LexA PWM production-validated;
      lambda organism enum fixed; 10 E. coli manifests queued (`coordinates_needed` baseline)
