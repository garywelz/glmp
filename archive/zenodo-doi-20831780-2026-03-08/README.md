# Zenodo DOI 10.5281/zenodo.20831780 — cited-content snapshot

`mermaid-perturbation-design-zenodo.md` (deposited PDF:
`../../collaborations/krampis-virtual-cell/mermaid-perturbation-design-zenodo.pdf`)
cites this URL twice:

```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer_demo/glmp-viewer-demo-v1-v6.html?process=ecoli_lac_operon&version=v1
```

That URL is a live-rendering demo, not a static document: the HTML fetches
its data at request time from
`gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli_lac_operon.json`.
Neither file has ever had a source in this repo, and the repo's own copy of
this data has already evolved past what's live at that path (confirmed
2026-07-31: 300+ line diff against repo HEAD's current annotation).

The two files in this directory are byte-for-byte what was live at both GCS
paths as of 2026-07-31 (verified via MD5 against the live objects). Both
objects' GCS `Generation` numbers are unchanged since their creation on
2026-03-08 -- so, as of this snapshot, they are also unchanged since the
Zenodo deposit itself, and this snapshot is the deposit-state content, not
just "recently checked."

**This is a preservation copy, not a source of truth to redeploy from.**
Nothing in this repo should ever overwrite
`glmp-v2/viewer_demo/glmp-viewer-demo-v1-v6.html` or
`glmp-v2/processes/ecoli_lac_operon.json` from repo HEAD -- see the hard
exclusion in `.github/published-artifacts.tsv`. If this content ever needs
correcting, the durable fix is a new Zenodo record version with the data
deposited as an attached file (concept DOI resolving to latest), not a GCS
edit -- a live-rendering demo can't be a durable citation target no matter
how carefully the bucket is preserved.

Bucket versioning was enabled 2026-07-31 (previously Suspended) as a
structural safety net for this and every other object in the bucket, on top
of this snapshot.
