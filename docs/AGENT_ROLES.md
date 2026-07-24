# Agent Roles and Division of Labor
## GLMP + CopernicusAI Research Program

**Version:** 1.2 — July 23, 2026
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
| `biology-database` | `biology-database` | Repo created (CC0). **HF Space not yet created.** |
| `chemistry-database` | `chemistry-database` | Repo created (CC0). **HF Space not yet created.** |
| `computer-science-database` | `computer-science-database` | Repo created (CC0). **HF Space not yet created.** |
| `physics-database` | `physics-database` | Repo created (CC0). **HF Space not yet created.** |

### Discipline-database pattern
Each science discipline gets its own repo *and* (eventually) its own HF Space, in a clean
1:1. `progframe` is the **generator/tooling** repo that produces the databases; it is no
longer their host. This keeps `progframe` lean and lets each discipline Space be improved
independently by Claude Code.

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
2. **Discipline HF Spaces** — create/wire Spaces for `biology-database`,
   `chemistry-database`, `computer-science-database`, `physics-database` (math Space
   already exists). Candidate first real Claude Code task.
3. **Copernicus legacy audit** — inventory `Copernicus_AI`, `copernicus-podcast-api`,
   `copernicus_backup`; report live vs. dead vs. worth-keeping before any move/archive.
   Candidate Claude Code read-only test.

---

## Change log
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
