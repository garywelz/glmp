# Knowledge Engine interface — integration assessment (2026-08-15)

**For:** Gary, Claude Chat, Cursor
**Trigger:** the papers corpus grew from ~62k to 117,581 over the last week (glmp-q3–q11 resumed sweeps, the glmp-q8 prune, glmp-q10 re-verification, glmp-f1). Gary asked whether the new papers are well-integrated into `https://copernicus-frontend-phzp4ie2sq-uc.a.run.app/knowledge-engine`, which is "not now working as intended."
**Method:** every claim below marked "confirmed live" was checked directly against the production `copernicus-podcast-api` backend and its `openapi.json` (which lists the real routes — no guessing at URLs), or against the actual source in the local `copernicus-web` checkout (`cloud-run-backend/`, `app/knowledge-engine/`, `components/knowledge-engine/`). Nothing here is inferred from documentation alone.

---

## Headline finding

**The corpus/retrieval pipeline itself is healthy. This is not a "the new papers didn't get indexed" problem.** Every backend endpoint tested returned correct, on-topic, current data reflecting the full 117,581-paper corpus, including papers from sweeps that finished within the last 24–48 hours. Gary independently confirmed the same from the live UI: Build Map produces a correct graph and node clicks produce accurately-grounded explanations. The actual problems are three specific, now-root-caused bugs (two backend, one frontend) plus a couple of items that still need a clean human look.

---

## What's confirmed working (backend, direct live calls)

| Check | Result |
|---|---|
| `GET /api/content/stats` | `papers_total: 117581`, `papers_with_embedding: 117581`, **100.0%** embedding coverage |
| `GET /api/content/browse?content_type=papers&limit=5` | **200 OK**, correct pagination (`total: 117581`, `pages: 23517`), real titled papers from yesterday's `glmp-f1` sweep |
| `GET /api/vector-search/semantic?query=...&content_types=papers` | Genuinely on-topic results for a real query (CRP/Class I promoter activation) |
| `GET /api/rag/answer?question=...&mode=general` | Accurate, grounded answer citing real papers/podcasts/processes across all content types |
| `GET /api/rag/answer?...&mode=paper_explanation&focus_id=pubmed_9895284` | **Re-verified item 34's fix (2026-08-04) against a paper that didn't exist when that fix was written** — citation `[1]` correctly grounds on the clicked paper, `similarity_score: 1.0`. The fix generalizes to new content. |
| `GET /api/knowledge-map/graph?keyword=...&content_types=papers` | 200 OK in ~4–5s, returns a real graph (21 nodes, 101 edges, all on-topic) |

Claude Chat independently hit `content_type=papers&limit=5` and got a 422; a clean call from this environment got 200 with correct data. Given the identical URL worked here, that 422 was very likely a transient or tool-side issue on Claude Chat's end (it also reported its own fetch tool serving stale/cached results on a retry), not a reproducible backend fault — but worth Claude Chat re-confirming from a fresh session if there's any doubt.

---

## Confirmed bugs

### 1. `similarity_score` is always exactly `0.0` on non-scoped semantic search — root cause found, one-line fix per call site

This was first flagged as a minor, unfixed side-note in `GLMP_MASTER_TODO.md` item 34 (2026-08-04: "the field is never populated, not just low"). It's still live today, confirmed on every single result across **every content type** (papers, podcasts, and all six process families) in both `/api/vector-search/semantic` and `/api/rag/answer` (general mode). This is highly user-visible — anyone looking at a relevance/match score in Search, Ask Questions, or the Knowledge Map sees `0` on everything, which reads as "broken" even though the underlying ranking is actually correct.

**Root cause, found in `cloud-run-backend/mcp_server/tools/vector_search.py`:** the function `search_semantic()` has two code paths per content type. The **question-scoped path** (used when a `question=glmp-qN` param is set, e.g. during acquisition scoring) correctly computes real cosine similarity (`paper_data["similarity_score"] = similarity`, line 505). The **generic/global path** — what `/api/vector-search/semantic`, the Knowledge Map, and RAG's general mode all actually use — instead does:

```python
vector_query = papers_ref.find_nearest(
    vector_field="embedding",
    query_vector=Vector(query_embedding),
    limit=limit,
    distance_measure=DistanceMeasure.COSINE,
    distance_threshold=distance_threshold
)
...
paper_data["similarity_score"] = 1.0 - paper_data.get("distance", 1.0)
```

`find_nearest()` only attaches a `distance` field to each returned document if you pass `distance_result_field=<name>` — confirmed directly against the installed `google-cloud-firestore` SDK (`inspect.signature`: `distance_result_field: Optional[str] = None`, keyword-only, defaults to not set). None of the 12 `find_nearest()` calls in this file pass it. So `paper_data.get("distance", 1.0)` **always** hits the `1.0` default, and `1.0 - 1.0 = 0.0`, every single time. This exactly matches the observed symptom (always precisely `0.0`, not a range of low values).

**Fix:** add `distance_result_field="distance"` to each `find_nearest()` call, or compute the similarity from the embedding directly before it's popped from the response (same pattern already used correctly in the scoped branch). All 12 call sites in `mcp_server/tools/vector_search.py` need it:

```
lines 520, 552, 584, 620, 654, 685, 716, 747  (papers/podcasts/glmp/math/chemistry/physics/cs/bio — first function)
lines 1036, 1063, 1090, 1121                  (same pattern, second function later in the file)
```

This is a Cloud Run backend fix — Cursor's domain per `AGENT_ROLES.md`, not attempted here.

### 2. Hardcoded, stale "594 process charts" in the page header

`app/knowledge-engine/page.tsx:72`:
```tsx
Papers, podcasts, videos, and 594 process charts across six scientific families
```
This is a literal static string, not fetched from anything live. The actual live counts (checked against `knowledge-engine-status.json` right now) don't match it either way: `process_databases.sum` is **692** across all six families, or **217** for the `glmp_v2` family alone (`processes` field / what `/api/content/browse?content_type=processes` actually returns). None of the three numbers agree — same failure class as the biology-paper-count bug fixed yesterday (`GLMP_MASTER_TODO.md` item 54): a hardcoded number that drifts from reality over time.

This is front-end copy — my domain per `AGENT_ROLES.md`, not Cursor's. I can fix it (either update the static number or wire it to `knowledge-engine-status.json` the same way the biology-papers stat already is) once there's agreement on which of 692/217/something-else is the number that should actually be shown, and Gary's go-ahead to push it live.

### 3. Knowledge Map nodes have no link out to the actual paper — data is already there, just discarded

Gary confirmed "Build Map" works correctly (21 nodes, 101 edges, matching this session's own direct API test exactly) and clicking a node produces a real, accurately-grounded RAG explanation (re-confirms bug-free retrieval and item 34's focus_id fix, live, from the actual UI). But the node/explanation panel gives no way to open the real source paper — a user can read an AI summary but can't verify it or read the original.

**Root cause, found in `components/knowledge-engine/KnowledgeMapView.tsx`:** the `/api/knowledge-map/graph` response already includes `doi` and `arxiv_id` on every paper node (confirmed directly — e.g. `{"id": "pubmed_10860739", ..., "doi": "10.1006/jmbi.2000.3736", "arxiv_id": null}`), and the node's own `id` carries the PMID for PubMed papers (`pubmed_<pmid>`). But the click handler (line 588 `cyRef.current.on('tap', 'node', ...)`) narrows the full node data down to just three fields before storing it:

```tsx
// line 593-595
const nodeId = data.id || data.paper_id || data.concept_id
const nodeType = data.type || data.nodeType || 'unknown'
const nodeLabel = data.label || data.title || 'Untitled'
// line 602
setSelectedNode({ id: nodeId, type: nodeType, label: nodeLabel })
```

`selectedNode`'s state type (line 59) is literally `{ id: string; type: string; label: string }` — `doi`/`arxiv_id`/`pmid` are available on `data` at the point of the click (line 590: `const data = node.data()`) but never carried through, and the Node Explanation panel (lines 1206–1252) never renders a link.

**This isn't a new problem to solve — `ContentBrowser.tsx` already solved it**, for the Browse Content tab, in the 2026-07-17 session (`docs/KNOWLEDGE_ENGINE_BROWSE_LINKS_HANDOFF_2026-07-17.md`): a small resolver function, `paperExternalUrl()` (`ContentBrowser.tsx` lines 40–68), does exactly DOI → PubMed → arXiv → raw `url` priority-ordered link resolution. The Knowledge Map's node-click path just never got the same treatment.

**Fix:** widen `selectedNode`'s type to also carry `doi`, `arxiv_id`, `url` (already present on `data` at line 590 — just stop discarding them at line 602), then render a link in the Node Explanation panel using the same `paperExternalUrl()` priority logic (import/reuse it, or reimplement the same four-line priority chain).

---

## Needs a clean human check, not more automated probing

- **`/api/knowledge-map/stats` returns all-zero (`papers: 0, concepts: 0, nodes: 0, edges: 0`) until a graph has actually been built by a query** (`"note": "Load the Knowledge Map tab to build/cache the graph."` — this is by-design lazy caching, confirmed live). If the Statistics tab displays this literally before any search has run, a first-time visitor would see an all-zero knowledge graph and reasonably conclude the engine is empty/broken, even though the underlying corpus is fully healthy. Worth Claude Chat checking the Statistics tab's component source to see whether it triggers a build before displaying, or just renders whatever `/stats` currently reports.

---

## Existing known gaps (already tracked, not new findings — surfaced here because they're directly relevant)

- **Item 42** (`GLMP_MASTER_TODO.md`, proposed, never built): the RAG `focus_id` grounding fix (item 34) silently falls back to semantic-only retrieval whenever a `focus_id` doesn't resolve against any known collection, logging only a `structured_logger.warning` with no counter or dashboard surface. If any of this week's new content ends up with an ID shape `_FOCUS_ID_COLLECTIONS` doesn't expect, nobody would know without manually reading Cloud Run logs. Worth prioritizing now that the corpus has grown this much, this fast.
- **Item 21's findability probe**, current live status (`GLMP_STATUS.html`, refreshed ~hourly by Jetson cron): `Overall: ⚠️ WARNING`, `14/14 anchor queries passing`, but **`2 coverage/index warnings`** — same count as when this was first built weeks ago. I could not find the actual content of those 2 warnings in anything published to GCS (only the count, not the detail); they likely live in Jetson's local published copy of `GLMP_MASTER_TODO.md` or in the probe's own logs. **Ask for Cursor:** pull the actual warning text from Jetson and report what they are — could easily be related to this week's corpus growth, or could be the same pre-existing `podcast_jobs`/`math_processes` warnings from the original build. Worth knowing which.

---

## Suggested division of labor

- **Cursor:** fix the 12 `find_nearest()` call sites (bug #1) in `cloud-run-backend/mcp_server/tools/vector_search.py`; fix the Knowledge Map node-link gap (bug #3) in `components/knowledge-engine/KnowledgeMapView.tsx` (both are Cloud Run/`copernicus-web` deploys, matching how the original Browse-card-linking work in the 2026-07-17 handoff was done); SSH to Jetson to pull the actual text of the 2 findability coverage/index warnings.
- **Claude Chat:** check the Statistics tab's frontend source for the zero-stats-on-first-load question; independently re-confirm the papers-browse 422 was transient, not reproducible.
- **Claude Code (me):** fix the hardcoded "594 process charts" string (bug #2) once there's agreement on the right live number, pending Gary's go-ahead — same pattern as yesterday's biology-paper-count fix.

**Gary already confirmed live** that Build Map completes correctly and node explanations are accurately grounded — that closed the one open question from the original draft of this report, and surfaced bug #3 in the process.

---

## Bottom line

Nothing about this week's corpus growth (117,581 papers, 100% embedded) broke the Knowledge Engine's ability to find and use the new content — every retrieval path tested returns correct, current, on-topic results including papers from sweeps that finished yesterday, confirmed both by direct API calls and by Gary's own use of the live UI. What's actually wrong is three specific, now-fixable bugs — a since-August-4th relevance-score bug, a stale hardcoded header number, and a missing link-out on Knowledge Map nodes (each root-caused down to the exact line) — plus one open question (the findability warnings) that needs Jetson access to resolve.
