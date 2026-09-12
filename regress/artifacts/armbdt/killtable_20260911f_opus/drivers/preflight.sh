#!/usr/bin/env bash
set -euo pipefail
for leg in BASE M_MASK1 M_MASK15 M_POPP_NONE M_POPP_WEAK M_POPW_WEAK M_SBIT_NONE M_NPMASK; do
  python3 /tmp/opus524_frozen/mutate_opus.py "$leg" /tmp/opus524_pf.c /tmp/opus524_baseline.c > /dev/null
  printf '%-14s ' "$leg"
  grep -o 'memory_rw(cpu, cpu->mem, [^,]*\(, *[^,]*\)\?, data,' /tmp/opus524_pf.c | tr '\n' '|' 
  echo
done
