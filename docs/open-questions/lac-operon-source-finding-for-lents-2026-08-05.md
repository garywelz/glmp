# A finding on the lac operon chart's citation, for Prof. Lents

**Status: not being sent (Gary's call, 2026-08-05).** Two reasons, both
good: (1) Lents already has direct access to the canonical `ecoli_lac_operon`
record via the Layer-2 viewer link in the shared teaching-diagrams document,
with its own "Improve this process" form built in — a standalone email would
be a redundant channel, not a needed one. (2) The finding's own analysis
(see `GLMP_MASTER_TODO.md` item 25) concluded the current citation, Jacob &
Monod 1961, is very likely already correct — the embedding flag here looks
like a false positive (a review book's title lexically matching the query),
not a real error. There's no live problem on this specific circuit to
report. Kept below for the record, not deleted, since the analysis behind it
is real and may be useful context later.

---

Hi [Prof. Lents],

While looking into how our flowchart citations are attached, I found something specific to the lac operon circuit you've been looking at for the cAMP-CRP question — flagging it directly rather than folding it into a larger batch.

**What we found:** the lac operon flowchart has more than one candidate source attached. A semantic-similarity check (comparing the chart's own description against each candidate source's title) ranks one of the other candidates well above the one currently listed first — a large enough gap to flag, but I want to be upfront about a real limitation of the check before you look at it.

**The two titles, and why I'm not calling a winner:**
- Currently listed first: *"Genetic regulatory mechanisms in the synthesis of proteins"* — this reads like it could be Jacob & Monod's foundational 1961 paper, which would make it a legitimate, arguably the canonical, citation for this circuit regardless of what a similarity score says.
- Ranked higher by the check: *"The lactose operon"* — a title that literally contains the query terms, which can make a similarity score look stronger than the source actually is. That's the failure mode I'm worried about here, not a reason to trust the ranking.

**What this is, and isn't:** a machine-measured signal, not a verified correction. Nothing has been changed. This is exactly the kind of case where the metric could be pointing at a lexical coincidence rather than a real problem — which is why it needs your read rather than ours.

If you have a moment: is the current citation (Jacob & Monod, if that's what it is) the right one for this chart, or does "The lactose operon" turn out to be the better source for some reason the title alone doesn't show?

Happy to send the DOIs and the full comparison if useful.
