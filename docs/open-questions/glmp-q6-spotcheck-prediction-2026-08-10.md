# glmp-q6 spot-check prediction (written before the write, 2026-08-09/10)

## Rollback
- Pre-write: `acquisition_matches[].question == 'glmp-q6'` should be 0.
- Post-write: should be exactly 3,583 (3,532 new + 51 merged).

## Scoped-retrieval check (the load-bearing prediction)
`search_semantic(question="glmp-q6", query="How are bacterial stress-response
regulons organised, and what governs the transition between the resting and
induced state?", content_types=["papers"])` should return exclusively
glmp-q6-attributed papers, on-topic (heat shock/sigma factor/oxidative
stress/envelope stress regulons, ppGpp stringent response). Expect this to
pass cleanly, consistent with glmp-q3/q4's confirmation of the same fixed
mechanism.

## This question's falloff was the cleanest of the three swept so far
Unlike glmp-q3 ("network"/"topology") and glmp-q4 ("switch"), this
question's terms (heat shock regulon, sigma factor regulon, oxidative
stress regulon, stringent response ppGpp, acid resistance regulon,
envelope stress response) are specific enough bacterial-biology vocabulary
that title-sampling found unambiguous on-topic content through roughly
p70, a real transition starting ~p74, and off-topic content dominating
cleanly afterward -- much closer to glmp-q5's original clean pattern than
q3/q4's noisier ones. Cutoff (0.36) yields the highest proportion of the
four questions swept so far (74% of candidates, vs. 36% for q3 and 27%
for q4) -- expected given the cleaner term set, not a red flag on its own,
but worth checking the actual write count against this reasoning rather
than accepting a large number uncritically.
