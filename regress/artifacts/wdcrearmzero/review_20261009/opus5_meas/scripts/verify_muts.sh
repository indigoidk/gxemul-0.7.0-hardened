#!/bin/bash
# Show the mutated line in each HEAD mutant copy and diff it against the baseline.
T=/tmp/gxopuswdc
for m in Md_frozenj Md_revwalk Md_halfj Md_armfrozen Md_wrongoff Md_order; do
  echo "== $m"
  diff "$T/t_HEAD/src/devices/dev_wdc.c" "$T/m_HEAD_${m}/src/devices/dev_wdc.c"
done
echo VERIFY_DONE
