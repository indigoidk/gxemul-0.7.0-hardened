#!/bin/bash
for T in /tmp/gxopus_lax_base /tmp/gxopus_lax_fix; do
  echo "== $T"
  grep -v '^make\|^cd \|^$' "$T.build.log" | head -8
  ls -la --time-style=full-iso "$T/gxemul" "$T/src/devices/dev_wdc.o" "$T/src/devices/dev_wdc.c" | awk '{print $6, $7, $9}'
done
cmp /tmp/gxopus_lax_base/gxemul /tmp/gxopus_lax_fix/gxemul; echo "cmp_rc=$? (1 = binaries differ, as they must)"
cmp /tmp/gxopus_lax_base/src/devices/dev_wdc.o /tmp/gxopus_lax_fix/src/devices/dev_wdc.o; echo "obj_cmp_rc=$?"
