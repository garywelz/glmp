#!/usr/bin/env bash
# Read-only drift check: compares each repo_path/public_url pair in the
# manifest and reports whether the published GCS copy still matches the
# repo source. Never publishes anything and needs no credentials -- every
# object in this manifest is world-readable, so this only ever curls the
# public URL.
#
# Exit codes:
#   0  clean -- every entry matches
#   1  drift -- at least one entry's published copy differs from its repo
#      source (and no entry hit a fetch failure or bad-manifest problem)
#   2  couldn't tell -- at least one entry could not be fetched (network/
#      HTTP issue); no confirmed drift and no bad-manifest problem
#   3  bad manifest -- missing file, malformed line, or a listed repo path
#      that doesn't exist. This means the check itself can't run correctly,
#      independent of whether anything actually drifted.
#
# Priority when a run has more than one kind of problem: bad-manifest (3)
# beats drift (1) beats fetch-failure (2). A broken manifest means we can't
# trust anything else this run reported, so it wins. Confirmed drift beats a
# same-run fetch hiccup on some other file, so a real problem never gets
# masked by an unrelated network blip.
set -uo pipefail

MANIFEST="${1:-.github/published-artifacts.tsv}"
BUCKET_PREFIX="https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/"

bad_manifest=0
fetch_failed=0
drift_found=0
any_checked=0

if [[ ! -f "$MANIFEST" ]]; then
  echo "BAD MANIFEST: $MANIFEST not found" >&2
  exit 3
fi

line_no=0
while IFS= read -r line || [[ -n "$line" ]]; do
  line_no=$((line_no + 1))
  [[ -z "$line" || "$line" == \#* ]] && continue

  IFS=$'\t' read -r repo_path public_url <<< "$line"
  if [[ -z "${repo_path:-}" || -z "${public_url:-}" ]]; then
    echo "BAD MANIFEST line $line_no: expected 'repo_path<TAB>public_url', got: $line" >&2
    bad_manifest=1
    continue
  fi
  if [[ ! -f "$repo_path" ]]; then
    echo "BAD MANIFEST line $line_no: repo path does not exist: $repo_path" >&2
    bad_manifest=1
    continue
  fi

  any_checked=1
  tmp="$(mktemp)"

  if ! curl -fsS "$public_url" -o "$tmp"; then
    echo "COULD NOT FETCH: $public_url (network/HTTP error -- not counted as drift)" >&2
    fetch_failed=1
    rm -f "$tmp"
    continue
  fi

  # Strip CR before comparing. The repo checkout's line endings depend on the
  # machine (Windows core.autocrlf vs a Linux CI runner) and don't reliably
  # match the GCS object's line endings either way -- normalizing both sides
  # to LF is what makes this comparison mean anything on any machine.
  if diff -q <(tr -d '\r' < "$repo_path") <(tr -d '\r' < "$tmp") > /dev/null; then
    echo "OK: $repo_path == $public_url"
  else
    drift_found=1
    gcs_path="${public_url#$BUCKET_PREFIX}"
    echo ""
    echo "DRIFT: $repo_path != $public_url"
    echo "--- published (live) vs repo (< live, > repo) ---"
    diff -u <(tr -d '\r' < "$tmp") <(tr -d '\r' < "$repo_path") | head -40
    echo ""
    echo "  To redeploy:"
    echo "  gsutil -h \"Content-Type:text/html; charset=utf-8\" -h \"Cache-Control:public, max-age=300\" \\"
    echo "         cp $repo_path gs://regal-scholar-453620-r7-podcast-storage/$gcs_path"
    echo ""
  fi

  rm -f "$tmp"
done < "$MANIFEST"

if [[ "$any_checked" -eq 0 && "$bad_manifest" -eq 0 ]]; then
  echo "BAD MANIFEST: no valid entries found in $MANIFEST" >&2
  bad_manifest=1
fi

if [[ "$bad_manifest" -eq 1 ]]; then
  exit 3
elif [[ "$drift_found" -eq 1 ]]; then
  exit 1
elif [[ "$fetch_failed" -eq 1 ]]; then
  exit 2
else
  exit 0
fi
