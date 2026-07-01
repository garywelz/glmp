# GLMP Decoder Queue

File-system queue for the batch decoder pipeline.

## States
- pending/   — manifests waiting to run (add new circuits here)
- running/   — manifest moved here when picked up by run_batch.py
- completed/ — manifest + result summary after successful decode
- failed/    — manifest + error log after failed decode

## How to queue a new circuit
Run select_batch.py to auto-generate manifests, or manually create
a YAML manifest in pending/ using the template in manifests/TEMPLATE.yaml.

## Important
Do not manually move files between queue directories — run_batch.py
manages state transitions. If a run was interrupted, check running/
for stuck manifests and move back to pending/ to retry.

## Jetson deployment
- Repo: `/media/sdcard/glmp/`
- Working dir: `/media/sdcard/glmp/collaborations/krampis-virtual-cell/dna-decoder/`
- Python: `/media/sdcard/miniforge3/envs/meme-env/bin/python3`
- Optional legacy sequences path: set `GLMP_SEQUENCES_DIR=/media/sdcard/decoder/sequences`
