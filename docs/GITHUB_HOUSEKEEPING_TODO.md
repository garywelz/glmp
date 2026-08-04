# GitHub housekeeping — findings not executed under item #28

*Survey date 2026-08-04. Item #28 was scoped to Core execution only
(`copernicus-web`). Everything below was found during that survey but belongs to
another project's scope, or needs a decision before anyone acts.*

*Verified by read-only clone and raw fetch unless marked otherwise. `shadow` is
out of scope per `CLAUDE.md` rule 5.*

---

## A. Escalations — these are findings, not chores

**A1. Computational pattern counts may be overstated by 25–40%.**
Open PR `cursor/verify-and-correct-computational-pattern-counts-977c` documents
double-counting (a process with both an AND and an OR gate counted twice). Read
in full by Claude Code: docs-only, zero merge risk, distinct from item #33, open
since ~Sep 2025. **The merge is the small part.** The unasked question is
whether the inflated counts propagated into the Programming Framework Space, the
discipline database tables, the process-count claims in any paper, or a Zenodo
deposit. Trace before merging; if a deposited paper carries the inflated number,
this is an erratum, not a docs fix.

**A2. `atap` has no README.**
Repo is public with 4 commits (`docs/`, `.gitignore`, `LICENSE`). GitHub renders
the CC0 legal text as the landing body, so a visitor sees ~200 lines of Creative
Commons boilerplate instead of a description. Highest external-visibility defect
in the suite. Unblocks the SUITE_REORG_PLAN Part 1 item "retitle ATAP and update
its scope note." Owner: ATAP project.

**A3. Credential history scan is clean-with-a-limit, not clean.**
Claude Code scanned 9 secret-shape classes across full reachable history; all
hits were false positives (vendored `google-auth`/`python-rsa` source in
now-untracked venvs; a saved-webpage CDN URL). But `bfg-1.14.0.jar` is committed
twice in `copernicus-web`, and its commits carry no purge-referencing message —
so whether a history rewrite ever completed is unresolved, and a completed BFG
run is invisible to this scan by construction. Record as a marked limit (§5).

---

## B. Per-repo defects (owning project executes)

| Repo | Finding | Owner |
|---|---|---|
| `atap` | No README (see A2). No `research_focus.json` — confirms SUITE_REORG_PLAN Part 4 open item, verified live. | ATAP |
| `sciencevideodb` | README carries a **duplicated YAML front-matter block**, and declares `sdk: gradio` while the reorg plan records the Space as `sdk: static` with an inert Gradio vestige. Metadata contradicts reality; duplicated front-matter can break HF parsing. | Resources |
| `metadata-database` | README is one future-tense sentence ("This project *will* create a database…") for a live Resource backing ~62,900 papers. | Resources |
| `glmp` | README cites **~62,700 papers** against the engine's ~62,900. Consider a dated or generated figure rather than a hardcoded one. | GLMP |
| `progframe` | README labels the math corpus "Mathematics database" — predates the 2026-07-23 ATAP rename. GCS *paths* may legitimately retain the old name; check whether the prose should change even if the URLs don't. **Unverified — flagged for check, not asserted.** | Methods & Tools |

---

## C. Suite-wide decisions (Gary's call)

**C1. License posture is inconsistent and looks accidental.**
`copernicus-web` MIT · `atap` CC0 · `progframe` and `metadata-database` have
LICENSE files (type unchecked) · **`glmp` and `sciencevideodb` have none.**
`glmp` is the most public-facing research surface in the suite and currently
carries no license, which defaults to all-rights-reserved — at odds with the
collaborator posture in SUITE_REORG_PLAN §4. A CC0-for-corpora /
MIT-for-code split is defensible; the current spread isn't a choice, it's a gap.

**C2. No `CONTRIBUTING.md` in any suite repo.**
Relevant to the Part 4 collaborator-onboarding work: the suggestion channel and
the review gate are described in governance but not on the repos themselves.

**C3. Disposition for the 4 stale PRs on `copernicus-web`.**
Claude Code read all four and closed none (correctly — a visible GitHub action
outside its authority). Recommendations, per its review:
- `...computational-pattern-counts-977c` — **do not close.** See A1.
- `...flowchart-errors-d178` — real Mermaid bug, but against root-level scratch
  copies rather than the live `mathematics-processes-database/` path. Close with
  a note; the bug class may still deserve a fresh check.
- `...sync-rss-status-with-firestore-d6f6` — likely superseded (the script it
  recreates now lives in `archive/one_off_scripts/`); touches live `main.py`,
  high conflict risk. Close with a note.
- `...fix-podcast-generation-system-issues-a5f1` — patches
  `cloud-run-backend/main_google.py`, which no longer exists on main. Safe close.
- Record *why* each is closed. Two of the four were findings, not cruft.

**C4. No CI anywhere.** `copernicus-web` has no `.github/workflows/`; the only
Actions history is GitHub's own dependency-graph bot. Given the PI-control model
this may be deliberate. Flagged, not prescribed.

---

## D. Core-scoped residuals (this project, not yet executed)

- **`RESOURCE_MANIFEST.md` citation fix** — drafted, diff ready, uncommitted.
  Two dead citations (`cloud-run-backend/canonical_helpers.py:85`,
  `cloud-run-backend/check_sources.py:11-12,15` — neither file exists anywhere in
  the tree) replaced with verified paths. The underlying facts were correct;
  only the evidence pointers were wrong.
- **`CLAUDE.md` never mentions `governance/`.** It routes agents to
  `AGENT_ROLES.md`, `GLMP_GOALS.md`, and `GLMP_MASTER_TODO.md` in the `glmp`
  repo, so an agent following it would never find the Constitution sitting in
  its own repo root. Arguably a larger drift risk than the README was.
- **GitHub repo description** (web-UI only, Gary): *"Core monorepo of the
  CopernicusAI Knowledge Engine — backend, frontend, governance, and suite
  infrastructure."*
- **5 tracked media files** violating `CLAUDE.md` rule 2 — bumper MP3 pairs
  duplicated across `bumpers/` and `cloud-run-backend/bumpers/`, plus an
  apparent stray personal voice memo at
  `papers/iCloud~com~TapMediaLtd~VoiceRecorderFREE/`. Check the bumpers aren't
  load-bearing for the backend before removing.
- **`bfg-1.14.0.jar` committed twice** (`tools/`, `lib/`), 14 MB each.
- **`huggingface-space/papers-metadata.json` is 49 MB** in git.
- **231 tracked `.backup`/`.bak` files.** Two are clear cruft
  (`app/page.tsx.backup`, `app/api/spotify/route.ts.backup`); the other ~229 are
  `.json.backup` inside the discipline process databases and **may be deliberate
  snapshots** — needs a decision, not a sweep.
- **Confirmed already clean:** no tracked venvs or `node_modules` (the
  SUITE_REORG_PLAN §6 "venv untracking" item appears done for this repo); no
  credentials in the current tree.
