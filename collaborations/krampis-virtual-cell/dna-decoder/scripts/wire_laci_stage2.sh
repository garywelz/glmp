#!/usr/bin/env bash
# Wire LacI Stage 2 PWMs into lac/trp completed manifests (Jetson runtime; gitignored).
set -euo pipefail

DECODER="${1:-/media/sdcard/glmp/collaborations/krampis-virtual-cell/dna-decoder}"

swap_pwm() {
  local manifest="$1"
  local old="$2"
  local new="$3"
  python3 - "$manifest" "$old" "$new" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
old, new = sys.argv[2], sys.argv[3]
text = path.read_text(encoding="utf-8")
if new in text and old not in text:
    print(f"OK (already wired): {path.name} -> {new}")
    raise SystemExit(0)
if old not in text:
    raise SystemExit(f"{old} not found in {path}")
path.write_text(text.replace(old, new), encoding="utf-8")
print(f"WIRED: {path.name}: {old} -> {new}")
PY
}

swap_pwm "${DECODER}/queue/completed/ecoli_lac_operon.yaml" \
  "motifs/laci_motif.meme" "motifs/laci_lacO.meme"

swap_pwm "${DECODER}/queue/completed/ecoli_trp_operon.yaml" \
  "motifs/laci_motif.meme" "motifs/trpr_motif.meme"

echo "Verify:"
grep -n "custom_pwm_files" -A5 \
  "${DECODER}/queue/completed/ecoli_lac_operon.yaml" \
  "${DECODER}/queue/completed/ecoli_trp_operon.yaml"
