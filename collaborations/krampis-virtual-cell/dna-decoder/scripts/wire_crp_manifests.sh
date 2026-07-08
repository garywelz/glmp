#!/usr/bin/env bash
# Wire crp_cap.meme into lac/ara/flhDC completed manifests (Jetson runtime only;
# queue/completed/ is gitignored). Idempotent: skips if already present.
set -euo pipefail

DECODER="${1:-/media/sdcard/glmp/collaborations/krampis-virtual-cell/dna-decoder}"

wire_one() {
  local manifest="$1"
  python3 - "$manifest" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
if "crp_cap.meme" in text:
    print(f"OK (already wired): {path.name}")
    raise SystemExit(0)

lines = text.splitlines(keepends=True)
out = []
in_custom = False
inserted = False
for line in lines:
    if line.startswith("custom_pwm_files:"):
        in_custom = True
        # Normalize an inline empty list ("custom_pwm_files: []") to a block
        # header so the appended "  - ..." item is valid YAML.
        out.append("custom_pwm_files:\n")
        continue
    if in_custom and not inserted:
        if line.startswith("  - "):
            out.append(line)
            continue
        out.append("  - motifs/crp_cap.meme\n")
        inserted = True
        in_custom = False
    out.append(line)

if in_custom and not inserted:
    out.append("  - motifs/crp_cap.meme\n")
    inserted = True

if not inserted:
    raise SystemExit(f"custom_pwm_files: block not found in {path}")

path.write_text("".join(out), encoding="utf-8")
print(f"WIRED: {path.name}")
PY
}

for circuit in ecoli_lac_operon ecoli_ara_operon ecoli_flhdc_flagellar; do
  wire_one "${DECODER}/queue/completed/${circuit}.yaml"
done

echo "Verify:"
grep -n crp_cap.meme \
  "${DECODER}/queue/completed/ecoli_lac_operon.yaml" \
  "${DECODER}/queue/completed/ecoli_ara_operon.yaml" \
  "${DECODER}/queue/completed/ecoli_flhdc_flagellar.yaml"
