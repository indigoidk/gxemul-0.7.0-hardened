#!/bin/bash
T=/tmp/gxfable_p5; S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_pcc2.c
cmp -s "$T/src/devices/dev_pcc2.c" "$S" && echo "clone dev_pcc2.c cmp-CLEAN vs SEC" || echo "clone DIVERGES from SEC"
[ -e "$T/.MUTANT" ] && echo "clone: SENTINEL PRESENT" || echo "clone: no sentinel"
[ "$T/gxemul" -nt "$T/src/devices/dev_pcc2.c" ] && echo "clone binary newer than source" || echo "clone binary STALE"
for B in /mnt/c/DocumentNoSnc/CC/GXEMUL/build /mnt/c/DocumentNoSnc/CC/GXEMUL/build-asan; do [ -e "$B/.MUTANT" ] && echo "$B: SENTINEL PRESENT" || echo "$B: no sentinel"; done
