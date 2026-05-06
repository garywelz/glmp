# Mathematics Database — Review Report & Recommendations

**Date:** 2026-03-15  
**Scope:** Full database review, Cite coverage, inconsistency fixes.

---

## Summary

- **Cite badges:** Added to every chart page (all 195 charts with `header-meta` now have attribution-wrap). 160 new attributions added to `attributions.json` and injected via `add_attributions.py`.
- **Broken link fixed:** `number_theory.html` frontier link updated from `number-theory-research-frontier.html` to `../../number-theory-research-frontier.html` for no-JS fallback.
- **Color legend fixes:**  
  - `foundations-axiomatic-set-theory-axioms-basic.html` — legend now matches Mermaid (Violet Definitions, Green Theorems).  
  - `spectral_theory-spectrum.html` — color legend added.
- **Metadata:** `subcategoryCounts` and `totalProcesses` are currently lower than actual file counts; see §Metadata below.

---

## Fixes Applied

| Issue | Fix |
|-------|-----|
| Broken frontier link | `number_theory.html` static href set to `../../number-theory-research-frontier.html` |
| Color legend mismatch | `foundations-axiomatic-set-theory-axioms-basic.html` legend updated to Violet/Green |
| Missing color legend | `spectral_theory-spectrum.html` — legend added |
| Cite on every page | 160 new attributions; all chart pages now have Cite badges |

---

## Recommendations for Additions

### Content Gaps (from NEXT_PASS_CHECKLIST)

1. **Primality tests** — Add charts for Miller–Rabin, Fermat, AKS (number theory).
2. **Named collections** — Consider `namedCollections` in metadata for cross-linking (e.g. Sullivan, Euclid, Peano).
3. **Formal verification & AI** — Lean, Coq, AlphaProof, AlphaGeometry links already in Number Theory and Foundations; consider expanding to other areas.
4. **math.HO / math.LO** — Already in nav where relevant; ensure all index pages have appropriate arXiv links.

### Structural

1. **Metadata reconciliation**  
   `metadata.json` reports `totalProcesses: 212` but there are ~275 chart HTML files. Either:  
   - Add the 63 orphan charts to metadata so they appear in the main table, or  
   - Document that the main table intentionally shows a curated subset and orphans are reachable via subcategory indices only.

2. **Subcategory count updates**  
   If orphan charts are to be included in the main table, update `subcategoryCounts`:
   - `abstract_algebra`: 9 → 12  
   - `discrete_mathematics`: 22 → 28  
   - `geometry_topology`: 26 → 78  
   - `number_theory`: 13 → 21  

3. **Color scheme consistency**  
   - Use standard 5-color (Def/Lem/Thm/Cor/Ref) for axiomatic charts.  
   - Keep GLMP 6-color (Red/Yellow/Green/Light Blue/Violet/Lavender) for algorithm flowcharts.  
   - Audit charts for legend/diagram mismatches and apply the palette from `apply_palette.py`.

### Quality

1. **Cross-links** — Add “See also” or “Related” to charts that reference others (e.g. Peano → Gödel, CRT → Extended Euclidean).
2. **DOI links** — Where primary sources have DOIs, add them to attributions (e.g. Gödel incompleteness already has DOI).
3. **Year precision** — Prefer specific years in attributions when known (e.g. “1929” vs “1920s”).

---

## Files Modified (This Session)

- `attributions.json` — 160 new entries
- `processes/number_theory/number_theory.html` — frontier link
- `processes/foundations/foundations-axiomatic-set-theory-axioms-basic.html` — color legend
- `processes/spectral_theory/spectral_theory-spectrum.html` — color legend added
- 160 chart HTML files — Cite badges injected via `add_attributions.py`

---

## Mermaid & Links

- **Mermaid:** No syntax errors in sampled charts (binary-search, quicksort, sieve, bisection, spectral-theory-spectrum, foundations-axioms, point-set-topology).
- **Internal links:** All prev/next and cross-subcategory links resolve correctly after frontier link fix.
- **External links:** NIST DADS, Wikipedia, Joyce (Clark), Stanford SEP, arXiv — structure verified; no automated check for dead URLs.

---

## Implemented (2026-03-15)

- **Named Collections:** 45 mathematician pages + 21 theorem pages in `collections/`; index linked from Start Here.
- **Primality tests:** Fermat, Miller–Rabin, AKS charts added; linked from Number Theory index.
- **namedCollections in metadata:** 70 processes updated; search includes collection names (e.g. "Euclid", "Fermat").
- **Cross-links:** See also sections in primality charts; CRT already had Extended Euclidean link.

## Next Steps

1. Run `python3 add_attributions.py` after any new charts are added.
2. Run `python3 generate_collections.py` to regenerate collection pages after edits.
3. Run `python3 add_named_collections.py` after adding new charts to collections.
4. Decide metadata policy: main table = curated subset vs. full catalog for remaining orphans.
5. Run a periodic link checker on external URLs if desired.
