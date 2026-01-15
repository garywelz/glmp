### Cursor Agent Task: Sanitize Mermaid Tokens and Deploy to GCS

Goal
- Sanitize Mermaid strings in GLMP process JSONs by replacing short bracketed chemistry tokens (e.g., [4Fe-4S], [2Fe-2S], [O2]) with parentheses.
- Deploy only changed files to GCS with aggressive no-cache headers.
- Verify server-side content and viewer rendering with a cache-buster.

Context
- Workspace root: `/home/gdubs/glmp`
- Processes live at: `gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/`
- Viewer: `https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html`

What to do (Agent)
1) Run sanitizer (dry-run first, then write)
```
python3 scripts/sanitize_mermaid_tokens.py --root .
python3 scripts/sanitize_mermaid_tokens.py --root . --write
```

2) List changed files (from sanitizer output). For each changed local file under `processes_with_not_gates/<org>/<name>.json`, deploy to the matching GCS path:
```
# Example mapping (keep subdirectories and filenames identical)
gsutil -h "Content-Type:application/json" cp \
  ./processes_with_not_gates/ecoli/ecoli_anaerobic_respiration.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/ecoli_anaerobic_respiration.json

gsutil setmeta -h "Cache-Control:no-cache, no-store, must-revalidate, max-age=0" \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/ecoli_anaerobic_respiration.json
```

3) Verify server copy is sanitized (no remaining short bracketed tokens in `.mermaid`)
```
curl -s "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/ecoli_anaerobic_respiration.json" \
  | jq -r .mermaid | grep -n '\\[[0-9A-Za-z+\-.]\\{1,12\\}\\]' || echo "Server mermaid clean ✅"
```

4) Spot-check in Viewer with cache-buster
```
# Replace process id below per file tested
echo "${EPOCHSECONDS}"  # or use $(date +%s)

xdg-open "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_anaerobic_respiration&ts=$(date +%s)"
```

Acceptance Criteria
- No "Syntax error in text" on sanitized processes in the viewer.
- `curl|jq|grep` check returns "Server mermaid clean ✅" for each changed process.
- Cache headers set to `no-cache, no-store, must-revalidate, max-age=0` on changed objects.

Notes
- Only transform inside the `.mermaid` field; the sanitizer already scopes to it.
- The regex targets short bracketed tokens `[0-9A-Za-z+-.]{1,12}` to avoid altering legitimate Mermaid syntax.
- If no files change, report "No changes needed" and skip deployment.



