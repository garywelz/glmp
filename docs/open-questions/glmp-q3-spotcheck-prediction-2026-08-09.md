# glmp-q3 spot-check prediction (written before the write, 2026-08-09)

## Rollback
- Pre-write: `acquisition_matches[].question == 'glmp-q3'` should be 0.
- Post-write: should be exactly the write-log count (candidates above cutoff),
  new + merged onto already-in-corpus docs.

## Scoped-retrieval check (the actually load-bearing prediction)
`search_semantic(question="glmp-q3", query="What network motifs recur across
transcriptional regulatory networks, and what dynamic behaviour does each
motif produce?", content_types=["papers"])` should return exclusively
glmp-q3-attributed papers, on-topic (feed-forward loops, autoregulation,
Boolean network dynamics, E. coli regulatory network structure) — this is
the now-fixed mechanism (item 53's three bugs), not something new being
tested for the first time. Expect this to pass cleanly; if it doesn't,
that's a regression in the fix, not a q3-specific finding.

## What should NOT be treated as a new finding
An *unscoped* global-similarity query for glmp-q1/glmp-q11's text may still
show some q3-adjacent volume effect, exactly as glmp-q5's write demonstrated
against glmp-q1 before scoped retrieval existed. That risk is already
understood and already the reason scoped retrieval was built — re-discovering
it here would not be new information, so it's not being re-tested as if it
were.

## Known limitation of this particular question, stated in advance
q3's term set ("network motif", "regulatory network", "network topology") is
more generic than q5's ("synthetic gene circuit", "repressilator") — title
sampling found off-topic content mixed in as early as p21 (immune/disease
networks, protein-domain networks, PPI networks, physiological networks),
recovering to a genuine bacterial-regulatory-network-dominated zone through
p35, then trending off-topic again from p36 onward. Cutoff (0.395) was set
at that p35/p36 transition. This means glmp-q3's corpus, more than q5's, will
contain some minority of papers whose relevance is real but generic-network
adjacent rather than motif-specific — expected and named now, not a surprise
to explain away later if a spot-checked title looks looser than glmp-q1's or
glmp-q5's did.
