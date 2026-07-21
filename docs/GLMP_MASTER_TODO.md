# GLMP + CopernicusAI — Master To-Do

Hand-maintained priorities with live AUTO-STATUS appended below.
Read alongside: `docs/GLMP_GOALS.md`.

<!-- CURATED:START -->
## Where things stand — 2026-07-05

**Decoder honesty milestone (committed a9eb66d).** Fixed the class-assignment bug where
spurious JASPAR density produced false Class II calls. All 8 known circuits re-decoded:
5 flipped II→I/II (lac, sos_lexa, sos_reca, dna_damage now honestly read I/II — repression
detected, activation undetectable without activator PWMs). ara/flhdc/lambda =
INSUFFICIENT_EVIDENCE; trp = I/II. **Class II is currently unreachable** — the decoder is
presently a *repression detector*, because there are zero activator PWMs. This is the honest
finding, not a regression.

**Security + consolidation chapter closed.** ElevenLabs key rotated (scoped, verified);
exposed GCP copernicusai-tts key deleted; dormant copernicus-podcast-api-v2 service deleted;
legacy repos Copernicus_AI + copernicus_backup deleted, copernicus-podcast-api archived.
OpenAI / GitHub-PAT / Twitter leaked creds were already dead.

**Untitled-husk corpus sweep closed (2026-07-21).** 1,543 Untitled husks (no
identifiers, no abstract/URL/sources) archived then deleted from `research_papers`;
corpus left at 63,059. Rollback: full export at
`gs://regal-scholar-453620-r7-podcast-storage/research_data/corpus_hygiene/untitled_sweep_20260721/`.
Deleted via `cloud-run-backend/scripts/sweep_untitled_husks.py`,
copernicus-web commit `b38170ff5`.

## Top priorities (next)
1. **CRP PWM** — highest-leverage science move. Would let lac reach a *legitimate,
   evidence-backed* Class II and turn the decoder from repression-only into
   repression+activation. NOT a quick task: needs validated CRP binding sites
   (RegulonDB/literature) + biologist-grade judgment on their quality. Own focused session.
2. **sciencevideodb quality pass** — the Claude Code evaluation still not run (today was all
   decoder + infra). The actual "can Claude Code improve my HF Spaces" test.
3. **MASTER_TODO cron install** — this file is currently hand-generated; automate it
   (Jetson→GCS→Yoga-push, ~6 AM ET) as its own calm step.
4. **GitHub housekeeping** — glmp Pages build failing repeatedly (#110–158); two Dependabot
   alerts (form-data, protobufjs).

## Parked / backlog
- Decoder follow-ups: operon re-anchoring (5/9 batch circuits mis-anchored on TF
  autoregulatory promoters, not regulated operons); trp LacI motif contamination (defer —
  doesn't change class); σ32 promoters out of decoder scope (mutM); the RegulonDB-grounded
  3-bucket decodability categorization is PROVISIONAL/CONFOUNDED — needs a re-anchored re-run
  + biologist review before it's a finding.
- Build AraC PWM (recover an evidence-backed ara decode).
- Deferred free-key rotations: YouTube (multi-service), Zenodo (scope check), NASA-ADS.
- copernicusai-tts IAM too broad (project-level owner+editor) — tighten.
- Descript API parallel experiment (TTS / post-prod / transcription / clips; never replace
  ElevenLabs; key straight to Secret Manager).
- Rename papers-database-table.html → metadata-database.html.
- Biologist engagement: re-approach Nathan Lents AFTER the Krampis call (decodability finding
  as the hook); widen the biologist pool (Krampis's students TBD).

## Reminder to self
Gary is a logician, not a biologist. Biological claims (bucket assignments, mechanism, PWM
site quality) require a qualified biologist. The evolutionary-complexity hypothesis stays a
downstream test OUTPUT, never a decoder-design INPUT.
<!-- CURATED:END -->

---

## AUTO-STATUS

AUTO-GENERATED 2026-07-05T22:30:00-04:00 — rebuilt each run.

### CopernicusAI corpus

| Signal | Value |
|--------|-------|
| Paper count | **62,312** |
| Status source | `knowledge-engine-status.json` on GCS (`count_source: api`) |
| Status JSON `last_updated` | 2026-07-03T13:04:47Z |
| Embedding coverage | 59,499 / 62,312 (97.26%) |
| GLMP v2 processes (metadata) | 217 |
| Last scout run (status JSON) | ⚠️ not published in `knowledge-engine-status.json` |
| Last scout run (Jetson logs) | pubmed_am log mtime **2026-07-05 10:15 ET**; ingest log **2026-07-05 11:27 ET** |

### GLMP decoder (8 known circuits — 2026-07-05 re-decode)

Source: Jetson `results/*_logic_20260705.json` (parser fix a9eb66d).

| circuit_id | `dna_topology_class` |
|------------|----------------------|
| `ecoli_lac_operon` | I/II |
| `ecoli_ara_operon` | INSUFFICIENT_EVIDENCE |
| `ecoli_trp_operon` | I/II |
| `ecoli_sos_lexa` | I/II |
| `ecoli_sos_reca` | I/II |
| `ecoli_flhdc_flagellar` | INSUFFICIENT_EVIDENCE |
| `ecoli_lambda_switch` | INSUFFICIENT_EVIDENCE |
| `ecoli_dna_damage_checkpoint` | I/II |

**Class II reachable on any circuit:** no (zero activator PWMs at confidence threshold).

| Batch / queue | Value |
|---------------|-------|
| Last regression summary | `regression_redecode_20260705.json` — **8/8** circuits |
| Queue pending | 0 |
| Queue completed | 17 |
| Queue failed | 0 |
| Last batch decoder log | `batch_decoder_20260705.log` (manual 8-circuit regression run) |
