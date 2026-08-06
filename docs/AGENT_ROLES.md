# Agent Roles and Division of Labor
## GLMP + CopernicusAI Research Program

**Version:** 1.7 — August 6, 2026
**Lives in:** `glmp` repo at `docs/AGENT_ROLES.md`
**Read alongside:** `docs/GLMP_GOALS.md`, `docs/GLMP_MASTER_TODO.md`

---

## Purpose

This document defines who does what across the human and AI agents working on the
GLMP + CopernicusAI research program, on which hardware, and against which repositories.
It exists so that any agent — or Gary — opening a session knows the division of labor and
the canonical repo↔Space map without re-deriving it, and so that handoffs between agents
are clean.

Roles and boundaries marked **(evaluating)** are not yet fixed. They describe how a tool
is currently being used and tested, and are expected to change as we learn what each tool
does best.

---

## The four agents

| Agent | Role | Strengths |
|---|---|---|
| **Gary Welz** | Author, PI, decision-maker | Domain expertise, scientific judgment, strategic vision, final approval on all decisions |
| **Claude Chat** (claude.ai) | Consultant / strategy | Architecture design, strategy, document drafting, cross-session memory, handoff documents, paper editing, cross-project thinking |
| **Cursor** | Coding and task agent | Full codebase indexing, multi-file edits, SSH to Jetson, cron deployment, complex git operations, pipeline debugging. Gary's primary coding tool at present. |
| **Claude Code** | Publishing / quality agent **(evaluating)** | Autonomous file reading, targeted single-file edits, HuggingFace deployment, GCS uploads; finds deployment patterns autonomously. Currently the least-utilized tool and under active evaluation for a broader role (see below). |

### Gary + Claude Chat: the decision loop
High-level decisions — architecture, scope, publication strategy, what to build next —
are made by Gary in dialogue with Claude Chat. Claude Chat proposes and asks about goals
before proposing solutions; Gary decides. No significant work is executed before this
dialogue happens.

### Claude Code: current scope and evaluation
Claude Code is presently the underutilized tool. Its **proven** use so far is targeted,
self-contained deployment work (single-file HTML edits, HF Space pushes, GCS uploads).

Its **intended and under-evaluation** role is broader: improving the *quality* of the
science-suite HuggingFace Spaces — not just deploying them, but improving the writing,
presentation, and overall polish of each Space. Claude Code can participate in that
quality work even though high-level decisions remain with Gary and Claude Chat.

We may also discover or invent other functions for Claude Code as we go. Where its remit
is not yet settled, this document says **(evaluating)** rather than fixing a boundary
prematurely.

### Cursor / Claude Code boundary — **(evaluating)**
The working split, subject to revision as we learn:

- **Cursor** owns anything needing full-repo context or SSH-to-Jetson: multi-file
  refactors, cron deployment, pipeline debugging, complex git operations.
- **Claude Code** owns self-contained, per-Space work it can read and act on
  autonomously: quality improvements, presentation, single-file edits, HF/GCS deploys,
  and repeatable setup tasks (e.g. wiring a repo to a new Space).

This boundary is a starting hypothesis, not a rule. Overlap is expected while we evaluate
where each tool is strongest.

### CI / GitHub Actions ownership — **(evaluating)**
Established by precedent, not yet a settled rule: **Claude Code authors and maintains
GitHub Actions workflows** for repos it already does self-contained quality/deployment
work in — this fits the same "reads and acts autonomously on a single repo" profile as
its other work, and needs no Jetson/SSH access. First instance: `glmp`'s
`published-drift-check.yml` (added 2026-08-03), a read-only check that curls each
published artifact and diffs it against the repo source.

This does **not** extend to workflows that touch Jetson, cron, or the ingest/decode
pipeline — that stays Cursor's, per the boundary above.

**Read-only vs. side-effecting CI is the load-bearing distinction, not "who wrote it":**
- A read-only check (drift detection, link validation, lint) can run unattended on a
  schedule or every push — no dialogue needed per-run, the same way a passing test suite
  doesn't need Gary's sign-off each time.
- Any workflow that would *deploy*, *publish*, or otherwise change GCS/HF/production state
  needs the same propose-then-wait approval as a manual deploy would, whether or not a
  human is literally typing the command. Nothing like this exists yet — flagging it now so
  the first one doesn't get waved through just because it's "just CI."

---

## The three hardware nodes

| Hardware | Primary role | What runs there |
|---|---|---|
| **Jetson Nano** (`gary@192.168.1.222`) | Edge compute | Scout cron (10:15 AM + 8 PM ET), batch decoder (2 AM ET), FIMO scanning, paper ingest pipeline |
| **Yoga 9i** (RTX 5060, 32GB) | Primary workstation | Cursor, Claude Code, all local repos, `gsutil`, `gcloud`, `gh`, git operations |
| **Yoga 730** | Mobile / secondary | Daily reading, email, remote access to Claude Chat and Cursor via browser. Travel machine. Not used for cron or pipeline work. |

### Mobile access
Gary accesses Claude Chat via iPhone and iPad (claude.ai app). Cursor and Claude Code are
desktop-only.

---

## Naming convention

**Naming has no single convention — consult the repo↔Space table below for each asset's
actual name.** Historically the aim was kebab-case for URL-facing names, but in practice:

- Single-token names (`copernicusai`, `glmp`, `sciencevideodb`, `atap`, `shadow`) have
  nothing to hyphenate.
- Two assets split repo and Space spelling: `progframe` (repo) / `programming_framework`
  (Space), and `metadata-database` (repo) / `metadata_database` (Space).
- The four discipline-database repos (`biology-database`, `chemistry-database`,
  `computer-science-database`, `physics-database`) are kebab-case but have no live Space
  yet to test the convention against.

**Never guess a name from the pattern — copy it from the table below.**

**License convention:** data/content collections use **CC0-1.0** (maximally reusable, no
attribution burden); code/tooling repos use **Apache-2.0** or **MIT**. This is why the five
discipline databases are CC0 while `metadata-database` (tooling-oriented) is Apache-2.0 —
a deliberate data/code split, not an inconsistency.

---

## The science suite: repo ↔ Space map

The canonical mapping. These are the repositories in scope for Claude Code quality work
and for the multi-agent workflow. GitHub (`garywelz`) is the source of truth.

| HF Space | GitHub repo | Status / notes |
|---|---|---|
| `copernicusai` | `copernicus-web` | **Monorepo.** Root = Eliza-framework AI-agent website (Python, MIT). Static `copernicusai` Space content lives in `copernicus-web/huggingface-space/` (`index.html`, `papers-database-table.html`). Claude Code must target that subfolder, not the root. |
| `glmp` | `glmp` | Project home / dashboard (HTML). Exact-name match. |
| `programming_framework` | `progframe` | Generator/tooling repo for the discipline databases (HTML, MIT). Underscore/legacy naming — see exceptions. Discipline data is migrating out to per-discipline repos. |
| `sciencevideodb` | `sciencevideodb` | YouTube-filtered science video DB, searchable by transcript (TypeScript). |
| `metadata_database` | `metadata-database` | Renamed from `copernicusai-research-metadata`. **Repo≠Space naming exception** (like `progframe`/`programming_framework`): GitHub repo is kebab-case, HF Space is snake_case. Apache-2.0. Its public face is the GCS-hosted table `papers-database-table.html` — a browsable/searchable view of the **same** 62,312-paper Firestore corpus that `copernicusai` surfaces. Division of labor: `copernicusai` = knowledge engine + podcast front end; `metadata_database` = the browse/search table. Not overlapping databases — two views of one corpus. Table file rename to `metadata-database.html` pending (see open items). |
| `atap` | `atap` | Renamed 2026-07-23 from `mathematics-database` (HF Space + GitHub repo, both live and no longer stubs). Algorithms, axiomatic theories, and proofs as dependency graphs. Math content continues to migrate out of `progframe`. |

### Engines vs. everything else
`glmp` and `atap` are the suite's only two **engines** — each has a frontier and a
`research_focus.json`. Everything else in the table above is infrastructure, a
browse/search surface, or Methods & Tools output, not a third or fourth engine.

Biology, chemistry, computer science, and physics are not engines — the four
discipline collections are Programming Framework demonstration corpus, worked
examples of applying the method, not discipline databases — per
`copernicus-web/huggingface-space/DISCIPLINE_DATABASES_PLAN.md`. No standalone repos
or Spaces. If these collections are built, they belong under Methods & Tools /
`progframe`, not as standalone per-discipline repos.

### Out of scope
`garywelz/shadow` (**Shadow of Lillya**, a creative-writing completion of Audrey Berger
Welz's novel) is **not** part of the science suite and is **not** managed under this
workflow. No agent touches it as science-suite work.

---

## Legacy / support repos (not Space sources)

To be audited, consolidated, or archived. None of these back a science-suite Space.

| Repo | Visibility | What it is | Disposition |
|---|---|---|---|
| `Copernicus_AI` | Private | Eliza-framework AI agent (legacy) | Audit → fold anything worth keeping into `copernicus-web` → archive |
| `copernicus-podcast-api` | Private | Podcast generation system for CopernicusAI | Audit — **confirm whether it's a live deployed service before folding**; media artifacts stay in GCS, never in git |
| `copernicus_backup` | Private | Podcast-generator backup | Archive (read-only, reversible) |
| `GraciePCat` | Private | Virtuals.io creative agent (`GraciePCat`) | Ignore — not a science project |
| `kickflip-docs` | Public | Fork of an unrelated video-SDK docs project | Ignore |

### Copernicus consolidation (decided, pending execution)
`copernicus-web` becomes the single home for the Copernicus platform — Knowledge Engine,
podcasting and future media generation, the copernicusai.fyi site, and the `copernicusai`
static Space. **Hard rule:** media artifacts (audio, video, large assets) live in GCS
(`regal-scholar-453620-r7-podcast-storage`), never in the git repo. The repo holds code,
static HTML/CSS/JS, and configs only. This is what keeps the consolidation from bloating
the repo.

---

## Working preferences

- Gary prefers dialogue before execution on anything significant. Claude Chat proposes and
  asks about goals before proposing solutions; Gary approves before work begins.
- Cursor asks explicit questions before proceeding on ambiguous tasks.
- Cursor reports in a four-section format:
  **what I found / what I did / what I'm uncertain about / what to discuss with Gary.**
- GitHub (`garywelz`) is the canonical source of truth for all repositories.
- **Run `copernicus-web/governance/check_citations.py` after any cleanout that
  moves files out of the tree, and before committing governance edits.** Added
  2026-08-04 after a cleanout left two dead file-path citations in
  `RESOURCE_MANIFEST.md` (the underlying facts were correct; only the evidence
  pointers rotted). The cleanout is the actual trigger — it's the step that
  silently breaks a citation, not the governance edit itself.
- **Anything handed across between agents regenerates from a fresh fetch
  before it's applied — never trust the artifact in hand.** Added 2026-08-04
  after three instances of the same failure in one session: Claude Code's
  shallow clone gave a false "no conflicts" read; Claude Chat's own working
  copy had a blocked `git pull` that silently reverted a fix, briefly making
  a landed patch look unlanded; and a script patch was built on a pre-docstring
  base and would have silently dropped an unrelated addition if applied
  verbatim. All three cost nothing because the receiving side re-verified
  against live `main` before acting — that won't always happen unless it's
  the default, not a judgment call made fresh each time.
- **An empty or surprising result is a claim about the instrument until the
  instrument is checked.** Added 2026-08-06 after five instances in two
  days, all caught the same way — by someone asking whether the tool could
  produce that answer for a boring reason before believing the answer said
  something about the world: trp operon Greek letters dropped by an encoding
  step, peroxisome names failing a case-sensitive match, the SOS tokenizer
  splitting on the wrong boundary, a regex reporting zero DOIs because of an
  unescaped paren, and an arXiv feasibility sweep reporting "no literature"
  for several terms because every multi-word query was a single quoted
  phrase requiring exact word-adjacency (`GLMP_MASTER_TODO.md` item 50).
  Five in two days is a property of this kind of work, not a streak — a
  zero or an outlier is exactly as likely to be the measurement breaking as
  the thing being measured being empty, and it doesn't announce which.
  Check the instrument before writing the finding down as being about the
  world.
- **Agreement between instruments is only evidence if the instruments
  could have disagreed.** Added 2026-08-06, same day as the rule above,
  after the rule above wasn't enough on its own: ATAP's first-pass
  acquisition run had two independent checks both report zero overlap
  with the existing corpus — a sampled top-5-per-term check, and an
  ingest script's `--dry-run`. They agreed, which read as confirmation.
  It wasn't: the dry-run's skip count was structurally incapable of
  detecting overlap at all (`batch.create()` staged but never committed,
  so the existence check never ran), and the sample simply hadn't drawn
  the 0.2% of terms with pre-existing hits. Two blind spots produced the
  same wrong number by coincidence, not two measurements confirming each
  other. Before treating agreement across methods as corroboration, ask
  whether either method was actually capable of returning the other
  answer — if one of them couldn't have said "yes, overlap," its
  agreement with the one that could is not information.

---

## Credential handling — standing rule

**Never `cat`, `od`, `head`, or otherwise print the full contents of a file that may hold
credentials** — `*.env`, anything named `*credentials*`, `*-sa.json`, or anything under
`.config/`. This binds every agent (Cursor, Claude Code, Claude Chat), not just whoever is
in the current task — it's now been two different agents in as many days.

To check such a file, use a targeted read that reveals only what's needed and nothing that
could reconstruct the secret:
- Presence / shape check: `grep -c PATTERN file`, or match on the variable name only.
- Identifying suffix, to compare against a known-key table: `grep PATTERN file | tail -c 9`
  — enough characters to identify *which* key it is, never enough to be useful to anyone
  who shouldn't have it.

**If a credential reaches output anyway, say so immediately** in the same turn, the way
Claude Code did when it found a plaintext OpenAI key while grepping `copernicus-jetson.env`
for Cloud Run URL references (2026-07-23) — don't bury it, don't keep working past it
silently.

---

## Open items
1. **Rename the table file** — `papers-database-table.html` → `metadata-database.html` for
   naming consistency. This is a *live* file: update every reference in one pass (the Space
   `index.html` links, `knowledge-engine-status.json`, and the GCS copy under
   `regal-scholar-453620-r7-podcast-storage/`), and keep the old name reachable briefly so
   no inbound links break. Good careful Claude Code / Cursor task.
2. **Copernicus legacy audit** — inventory `Copernicus_AI`, `copernicus-podcast-api`,
   `copernicus_backup`; report live vs. dead vs. worth-keeping before any move/archive.
   Candidate Claude Code read-only test.

---

## Change log
- **v1.7** (2026-08-06) — Added a working preference: agreement between
  instruments is only evidence if the instruments could have
  disagreed, after two independent zero-overlap checks in the ATAP
  first-pass run turned out to be two unrelated blind spots agreeing
  by coincidence, not confirmation.
- **v1.6** (2026-08-06) — Added a working preference: an empty or surprising
  result is a claim about the instrument until the instrument is checked,
  after five same-shape catches in two days, the most recent being a
  feasibility sweep undercounting arXiv literature because of an overly
  strict phrase-query construction.
- **v1.5** (2026-08-04) — Added a working preference: regenerate anything
  handed across between agents from a fresh fetch before applying it, after
  three same-day instances of an out-of-date artifact silently producing a
  wrong verdict (a shallow clone, a blocked local `git pull`, a patch built
  on a pre-docstring base).
- **v1.4** (2026-08-04) — Added a working preference: run
  `copernicus-web/governance/check_citations.py` after any cleanout and before
  committing governance edits, after a cleanout left two dead citations in
  `RESOURCE_MANIFEST.md`.
- **v1.3** (2026-08-03) — Added CI/GitHub Actions ownership section: Claude Code owns
  workflows for repos it already does self-contained work in (not Jetson/cron/pipeline
  CI, which stays Cursor's); read-only vs. side-effecting CI is the approval-relevant
  distinction, not authorship. Anchored to the first instance, `glmp`'s
  `published-drift-check.yml`.
- **v1.2** (2026-07-23) — Added a standing credential-handling rule (never print
  secret-shaped files in full; targeted greps for presence/suffix only; flag immediately if
  a credential reaches output) after a live OpenAI key was found in a plaintext `.env` file
  during a Cloud Run audit.
- **v1.1** (2026-07-03) — Added authoritative GitHub repo↔Space map, five discipline
  databases, naming and license conventions, legacy/support repo audit table, Copernicus
  consolidation rule, open items.
- **v1.0** (2026-07-03) — Initial version. Four-agent model, three hardware nodes,
  six-Space science suite with Shadow of Lillya carved out, Claude Code documented as
  intent-with-evaluation.
