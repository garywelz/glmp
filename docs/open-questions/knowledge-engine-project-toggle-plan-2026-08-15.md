# Knowledge Engine: GLMP/ATAP project toggle — plan (2026-08-15)

**For:** Gary, Claude Chat, Cursor — for discussion before commitment, per Gary's request.
**Goal:** make the shared Knowledge Engine frontend feel customized for GLMP and ATAP researchers, via a toggle rather than separate frontends (decided against forking: both projects share the same backend, corpus, and Knowledge Map/Search/RAG infrastructure, so a fork would mostly duplicate UI chrome while doubling the maintenance cost we felt firsthand today fixing three bugs across one frontend instance).

---

## Current state, checked directly against the source (not assumed)

The infrastructure a toggle needs is **already about 80% there** — it was just never framed as "projects":

- Every tab already filters by `disciplines` (biology, chemistry, physics, mathematics, computer_science, interdisciplinary) and `sources` (pubmed, arxiv, nasa_ads, crossref, youtube, rss) against the same backend endpoints.
- The Knowledge Map tab already has a **"Quick Examples"** pattern (`KnowledgeMapView.tsx`, lines ~867–935) — hardcoded buttons that call `runQuickExample()` with a full filter preset (content types, disciplines, sources, keyword, max papers). Today it has two groups: **"📐 Mathematics"** (Nilpotent Groups, Spectral Sequences) and **"🧬 Biology"** (Aerobic Respiration, Acid Resistance) — which is already, functionally, an ATAP/GLMP split in everything but name. ATAP is the mathematics-domain sibling project (`atap_graphs` collection, `content_type=math`); GLMP is the biology/gene-regulation project (`glmp_processes`, `discipline=biology`).
- This pattern is **purely frontend, no backend dependency** — the presets just pre-fill existing filter params. No new API endpoints needed for a toggle.
- It is **not shared across tabs**: Search, Ask Questions, Browse Content, and Statistics each have their own hardcoded copy/placeholders (e.g. `SearchInterface.tsx`'s placeholder text already mixes both projects' example terms in one string) with no shared "current project" concept anywhere in the app.

## Proposed design

1. **A shared project-context**, held once at the page level (`app/knowledge-engine/page.tsx`) — `selectedProject: 'glmp' | 'atap' | null` — passed down to all five tab components (React context or simple prop-drilling; this app is small enough that either is fine).
2. **A toggle UI element** in the header, next to or below the existing tab nav — e.g. two buttons ("GLMP" / "ATAP") or a segmented control. Selecting one:
   - Pre-fills that project's disciplines/sources as the default filter state (not locked — a researcher can still broaden the search, the toggle just sets sensible starting defaults).
   - Swaps the "Quick Examples" set shown in Knowledge Map to that project's examples.
   - Swaps placeholder text / example terms in Search's search box.
   - Optionally swaps a short framing line under the page header (e.g. "Exploring GLMP's gene-regulation corpus" vs. "Exploring ATAP's mathematics corpus").
3. **A per-project config object**, one place (e.g. `lib/knowledge-engine-projects.ts`) holding each project's default disciplines/sources, example query set, and framing copy — so the five components read from one source instead of each hardcoding its own.
4. **No backend or API changes required** — confirmed by reading the actual filter/search code, not assumed.

## What still needs real content, not just code

The current two examples per discipline are thin and don't reflect this week's actual work. Before shipping, each project needs:
- **A fuller set of example queries** — GLMP's should draw on this week's actual sweeps (CRP/Class I promoter activation, lac operon, catabolite repression — we already know these return good results, tested live today) rather than just the original two. ATAP's should get the same treatment from whoever knows its corpus best.
- **A short "how to use this" description per project** — a sentence or two a researcher new to the tool reads before diving in. This is closer to product copy than code, and should reflect how each project's own researchers actually think about their corpus — not something I should just invent alone.

## Execution ownership

**I can do the large majority of this myself:**
- The project-context/config plumbing and toggle UI (frontend React/TypeScript, same domain as today's three KE fixes).
- Wiring each tab to read from the shared config instead of its own hardcoded copy.
- Drafting a first pass at example queries and framing copy, to be reviewed/corrected rather than written from scratch by someone else.

**What needs Cursor:**
- The actual Cloud Build deploy to `copernicus-frontend`, same as every fix today — I don't have that deploy access, by design (Cursor's domain per `AGENT_ROLES.md`).
- Nothing on the backend is anticipated, but Cursor should have a chance to flag it if something here turns out to need an API change I haven't spotted.

**What's actually Gary's/the team's call, not mine:**
- The example queries and framing copy for each project — I can draft, but this should be reviewed against what GLMP and ATAP researchers actually want to see first.
- Whether the toggle should be sticky (remembers your last choice) or reset each visit, and whether it's a hard requirement to pick one or "both/neither" stays a valid default view.

## Suggested next steps

1. Discuss this plan with Claude Chat and Cursor — flag anything about the design or scope that looks wrong before code starts.
2. Gary (or whoever knows each project's researcher audience) supplies or reviews a first draft of example queries + framing copy per project.
3. I build the toggle + config plumbing, wire all five tabs to it, commit.
4. Cursor deploys via Cloud Build, same pattern as today.
5. Everyone spot-checks the live result before calling it done — same discipline as today's KE fixes (visually confirmed live, not just trusted from a commit).
