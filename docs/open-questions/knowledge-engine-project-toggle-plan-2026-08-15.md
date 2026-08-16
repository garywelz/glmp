# Knowledge Engine: GLMP/ATAP project toggle — plan (2026-08-15)

**For:** Gary, Claude Chat, Cursor — for discussion before commitment, per Gary's request.
**Goal:** make the shared Knowledge Engine frontend feel customized for GLMP and ATAP researchers, via a toggle rather than separate frontends (decided against forking: both projects share the same backend, corpus, and Knowledge Map/Search/RAG infrastructure, so a fork would mostly duplicate UI chrome while doubling the maintenance cost we felt firsthand today fixing three bugs across one frontend instance). Claude Chat adds a stronger reason than maintenance cost alone: the Constitution already frames GLMP and ATAP as domain applications of one shared Core, not separate umbrellas (§1, §7) — a fork wouldn't just cost more, it would work against the suite's own stated architecture.

> **Revision note:** the first draft of this plan got two things wrong, corrected here after Cursor read it against the actual source (`page.tsx`, all five tab components, `constants.ts`, the browse/knowledge-map backend mappings) rather than taking the draft's claims on faith. Both corrections are load-bearing, not cosmetic — see below. Claude Chat independently re-verified every claim in the corrected plan against the same source and confirmed it holds, plus surfaced one more concrete finding and one open question — folded in below.

---

## Current state, checked directly against the source

**Correction 1 — "already ~80% there" was overstated; true for Knowledge Map only.**

- **Knowledge Map** has the preset pattern (`KnowledgeMapView.tsx` "Quick Examples," ~lines 867–935): buttons that pre-fill existing filter params (content types, disciplines, sources, keyword). Purely frontend, no new API needed.
- **Search and Ask Questions do not filter by project, discipline, or process family at all today.** Search sends `content_types=papers,podcasts,glmp,math,chemistry,physics,computer_science,biology` unconditionally; RAG always sends the same full list. Their only "project" difference right now is placeholder text that mixes both corpora into one string.
- **Browse Content already has a real project split** — process-family chips, and the Mermaid viewer is GLMP-only. This is functionally closer to a genuine project toggle than anything in Knowledge Map.
- **Statistics is suite-wide** (692 charts across six families) and has no project concept at all.
- **There is no shared project context anywhere** — `page.tsx` only switches tabs.
- **The duplication this causes is already visibly broken today, not hypothetical** (Claude Chat, verified directly): `StatsDashboard.tsx` line 120 has a stat box headed "Process Charts (6 families)" whose sub-label reads `Firestore GLMP only: {engineStatus?.processes}` — the box's own title promises six families, the value it shows is the 217-chart GLMP-only count. Confirmed directly against the source. The shared-config proposal below is a direct fix for a problem already visible in production, not a preventive measure for a hypothetical one.

**Correction 2 — GLMP ≠ biology, ATAP ≠ mathematics. Do not build the toggle around discipline labels.**

| Project | What it actually is | What a naive discipline-only toggle would show instead |
|---|---|---|
| GLMP | The `glmp` process family (217 charts) + papers scoped by `question_scope_ids` (`glmp-q1`…`glmp-q11`, `glmp-f1`) | All 80,138 `discipline=biology` papers — the general biology corpus, not GLMP's actual scope, plus the separate 55-chart `biology` process family that isn't GLMP either |
| ATAP | `content_type=math` → the `atap_graphs` collection specifically | All 18,321 `discipline=mathematics` papers — broader than just ATAP's own graphs |

The backend already distinguishes these correctly (Browse maps `math` → `atap_graphs`; GLMP papers are scoped by `question_scope_ids`, not by discipline). A toggle that just flips `disciplines.biology` on would feel like "the biology library," not GLMP specifically — a real identity mismatch, not a minor imprecision.

## Decided: chrome-first for v1, null/both stays the default

Gary decided both open questions (2026-08-15), agreeing with Cursor's and Claude Chat's recommendation on both:

- **v1 is chrome-first**, not scoped retrieval: header framing line, per-project Quick Examples, per-project Search placeholder text. No changes to what Search/RAG actually retrieve — small, safe, frontend-only, ships fast. Doesn't yet make GLMP "feel" scoped when you actually search, just when you look at the examples. **Scoped retrieval** (Search/RAG actually passing `discipline`, process-family `content_types`, and for GLMP specifically `question`/`question_scope`, so selecting a project changes real results) is deferred as an explicit later decision, not built now.
- **`null`/both stays the default landing state.** No forced GLMP/ATAP pick on arrival — matches the count-honesty fix philosophy from yesterday (a forced pick would hide chemistry/physics/CS/non-GLMP-biology by default, the same failure shape as the "594" bug). A `?project=glmp` query param is still worth adding for direct links; sticky `localStorage` is optional, not required.

## Proposed design (chrome-first scope)

1. **A shared project-context** at the page level (`app/knowledge-engine/page.tsx`) — `selectedProject: 'glmp' | 'atap' | null` — passed to all five tab components.
2. **A toggle UI element** in the header. Selecting a project swaps: the Knowledge Map Quick Examples set, Search's placeholder/example terms, and a short framing line under the header. It does **not** change what Search/RAG actually retrieve in v1 (see decision above).
3. **`null`/both stays the default landing state, not a forced pick.** The header currently tells the truth about six families and 692 charts (yesterday's fix); forcing a GLMP/ATAP choice on arrival would hide chemistry, physics, CS, and the non-GLMP biology charts — the same kind of misrepresentation as the "594" bug fixed yesterday, just in a new place. A `?project=glmp` query param (useful for sending a researcher a direct link) is worth adding; sticky `localStorage` is optional, not required.
4. **A per-project config object** keyed off **process family + example queries + framing** — not discipline. GLMP → `glmp` process family (question-scope is a later, deliberate decision, not v1). ATAP → `atap_graphs`/`content_type=math`. One file (e.g. `lib/knowledge-engine-projects.ts`) all five components read from.
5. **Statistics tab:** either stays suite-wide in both modes, or shows only the selected family when toggled — pick one and apply it consistently. Mixing the two would look exactly like the "594" count-honesty bug fixed yesterday.
6. **No backend or API changes for chrome-first.** Scoped retrieval, if/when decided later, is still frontend-only (the params already exist) but is real retrieval-scoping work, not "wire placeholders." Claude Chat separately checked `_FOCUS_ID_COLLECTIONS` in `rag_service.py` (the mechanism behind item 34/42's precise RAG grounding) — it already covers both `glmp_processes` and `atap_graphs`, so per-project `focus_id` grounding isn't GLMP-only and needs no change either way.

## What still needs real content, not code — and isn't mine to invent alone

- **Example queries per project.** This week's CRP/Class I promoter/lac-operon/catabolite-repression queries are good GLMP *candidates* (tested live today, known to return good results) — not an approved ship list. ATAP's set needs the same treatment from whoever knows that corpus best.
- **Framing copy** — the short "what is this" line for each project. Should reflect how each project's own researchers actually think about their corpus, not something invented from outside.
- **Open question, not yet answered:** would ATAP researchers want "mathematics papers + math process charts," or only `atap_graphs` specifically? Would GLMP eventually want `question_scope`-level scoping, or does the `glmp` process family alone represent it well enough? These affect the scoped-retrieval design if/when that's greenlit, not chrome-first.
- **Open question, flagged by Claude Chat, worth checking before ATAP's content pass specifically:** does ATAP have anything equivalent to GLMP's declared-question list (`research_focus.json`'s `active_questions`/`frontier`, the thing GLMP's `question_scope` mechanism and this week's precisely-verified CRP-promoter examples are anchored to)? Per the governance docs, ATAP's own version of that scaffolding may still be an open, uncommitted item. Doesn't block chrome-first (Quick Examples is pure filter-preset UI, no `question_scope` involved either way) — but means ATAP's example queries may not be able to reach the same anchored precision as GLMP's without that scaffolding existing first, and that gap shouldn't be assumed away.

## Execution ownership

**Mine to build (chrome-first scope):**
- Project-context/config plumbing and toggle UI.
- Wiring all five tabs to read from the shared config.
- A first-pass draft of example queries and framing copy, explicitly to be reviewed/corrected, not treated as final.

**Cursor's:**
- The Cloud Build deploy, same as every fix today.
- Flag anything here that turns out to need a backend change I haven't spotted (none anticipated for chrome-first).
- If/when scoped retrieval is greenlit, that's a bigger frontend change worth a second look before building.

**Gary's/the team's call, not mine:**
- Who actually writes the two example/framing lists before any code ships.
- Whether ATAP has its own declared-question scaffolding (Claude Chat's open question above) — worth checking before treating ATAP's content pass as equivalent in depth to GLMP's.
- The ATAP-scope and GLMP-question-scope questions above, whenever scoped retrieval comes up as a later decision.

## Status and next steps

**Decided (2026-08-15):** chrome-first for v1, `null`/both as the default landing state.

**Built and committed (2026-08-15), `copernicus-web@b04424784`:** the toggle plumbing, config, and all four component updates are done, including the `StatsDashboard.tsx` mislabel fix. Full production build verified clean before committing.

**Extended and deployed overnight, same day, in Cursor's broader KE-ingest session:** ATAP's identity corrected again and locked as a product decision ("Axiomatic Theories, Algorithms and Proofs," not mathematics) with new live-verified examples; `RAGInterface.tsx`/`StatsDashboard.tsx` wired in; Search and Ask Questions now scope process `content_types` per project ("Layer A" — a real, if narrow, departure from pure chrome-first, since papers stay unscoped/"Layer B"). Deployed and confirmed live. Full write-up, including independent verification, in `GLMP_MASTER_TODO.md` item 57.

1. ~~Gary (or whoever knows each project's audience) supplies or reviews example queries + framing copy per project~~ — current set is a tested-but-draft placeholder (GLMP's three queries were live-tested 2026-08-15; ATAP's two are unchanged from the original). **Still open:** final review, and whether ATAP has a declared-question equivalent to GLMP's.
2. ~~I build the chrome-first toggle + config plumbing, wire all five tabs~~ — done.
3. **Cursor deploys via Cloud Build — not yet done.**
4. Everyone spot-checks the live result before calling it done — same discipline as today's KE fixes (visually confirmed live, not just trusted from a commit).
