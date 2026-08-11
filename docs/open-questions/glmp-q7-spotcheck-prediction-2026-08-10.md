# glmp-q7 spot-check prediction (written before the write, 2026-08-10)

## Rollback
- Pre-write: `acquisition_matches[].question == 'glmp-q7'` should be 0.
- Post-write: should be exactly 12,400 (11,711 new + 689 merged).

## Scoped-retrieval check (the load-bearing prediction)
`search_semantic(question="glmp-q7", query="How do two-component systems and
phosphorelays transduce signals into transcriptional output?",
content_types=["papers"])` should return exclusively glmp-q7-attributed
papers, on-topic (two-component systems, histidine kinases, phosphorelays,
quorum sensing regulators). Expect this to pass cleanly, consistent with
glmp-q3/q4/q6's confirmation of the same fixed mechanism.

## Scale note, stated plainly before the write
This is by far the largest single-question write in the resumed sweeps
(11,711 new vs. 963-3,532 for glmp-q3/q4/q6) and the largest candidate pool
(19,745 vs. 4,575-6,896) -- both "two-component system" and "quorum sensing
regulation" are large, well-studied fields on their own, and the question
combines them. The 63% pass rate (12,400/19,745) is closer to glmp-q6's
74% than glmp-q3/q4's 27-36%, consistent with this being a moderately
clean but very broad term set rather than a noisy one -- checked against
actual title samples, not assumed from the percentage.

## Known limitation of this particular question, stated in advance
False positives found in title-sampling: "component" as a chemistry/
materials-science term (three-component/multicomponent reaction systems,
supramolecular hydrogels), generic "system" in physics contexts (Turing
systems, dissipative solitons), and QS-adjacent-but-host-side papers
(human respiratory response to quorum-sensing molecules, rather than the
bacterial signaling mechanism itself). These are excluded by the cutoff,
not systematically present within it, based on the samples read.
