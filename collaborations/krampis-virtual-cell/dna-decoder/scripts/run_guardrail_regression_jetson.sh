#!/bin/bash
set -e
cd /media/sdcard/decoder
COMMON="--qvalue-threshold 0.05 --repressor-qvalue-threshold 1.0 --max-sites 50"

python3.8 glmp_logic_parser.py --hits results/gal1_jaspar/fimo.tsv \
  --circuit gal1_promoter --organism s_cerevisiae \
  --output results/gal1_promoter_logic_v2.json $COMMON

python3.8 glmp_logic_parser.py --hits results/lac_test/fimo.tsv results/lac_test2/fimo.tsv \
  --circuit lac_operon --organism ecoli_k12 \
  --output results/lac_operon_logic_guardrail.json $COMMON

python3.8 glmp_logic_parser.py --hits results/ara_test/fimo.tsv \
  --circuit ara_operon --organism ecoli_k12 \
  --output results/ara_operon_logic_guardrail.json $COMMON

python3.8 glmp_logic_parser.py --hits results/trp_test/fimo.tsv results/trp_test2/fimo.tsv \
  --circuit trp_operon --organism ecoli_k12 \
  --output results/trp_operon_logic_guardrail.json $COMMON

for f in gal1_promoter_logic_v2.json lac_operon_logic_guardrail.json ara_operon_logic_guardrail.json trp_operon_logic_guardrail.json; do
  echo "=== $f ==="
  python3.8 -c "import json;d=json.load(open('results/$f'));ls=d['logic_summary'];print('topology:',ls['topology_hint']);print('class:',d.get('circuit_class'));print('note:',d.get('circuit_class_note','none'));print('geom:',d.get('geometry_warning','none'))"
done
