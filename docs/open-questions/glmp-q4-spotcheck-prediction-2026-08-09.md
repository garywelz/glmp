# glmp-q4 spot-check prediction (written before the write, 2026-08-09)

## Rollback
- Pre-write: `acquisition_matches[].question == 'glmp-q4'` should be 0.
- Post-write: should be exactly the write-log count (1,241: 963 new + 278 merged).

## Scoped-retrieval check (the load-bearing prediction)
`search_semantic(question="glmp-q4", query="Which regulatory circuits exhibit
bistability or switch-like behaviour, and what evidence establishes the
switch rather than a graded response?", content_types=["papers"])` should
return exclusively glmp-q4-attributed papers, on-topic (toggle switches,
phenotypic switching, hysteresis, persister-cell bistability). Expect this
to pass cleanly, consistent with glmp-q3's confirmation of the same fixed
mechanism -- not a new test of the retrieval architecture itself.

## Known limitation of this particular question, stated in advance
"switch" is a heavily overloaded word: title-sampling found genuine false
positives from immunology (antibody class-switch recombination), chemistry
(molecular "carbon-silicon switches"), and optogenetics/plant biology
(light-responsive control systems that aren't bistable in the intended
sense). Unlike glmp-q3's pattern (clean recovery zone, then off), this
question's mixed zone never cleanly recovers -- genuine phenotypic-switching
and phase-variation hits keep appearing sparsely as late as ~p49, interleaved
with off-topic homonyms rather than separated from them. Cutoff (0.375) was
set where 5-point percentile blocks stopped having an on-topic majority
(~p27/p28), which is a stricter and lower-yield cut than glmp-q3's (27% of
candidates above cutoff here vs. 36% for q3) -- expected and named now, not
a surprise to explain away later. Some genuine bistability papers scoring
just below 0.375 are known to exist and are being left out by this cutoff;
that is the accepted cost of not hand-picking exceptions into an otherwise
principled percentile-based rule.
