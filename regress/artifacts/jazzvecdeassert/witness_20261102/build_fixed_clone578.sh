#!/bin/bash
# build_fixed_clone578.sh -- /tmp/gxfix578 = /tmp/gxdivw (HEAD product tree) + the tentative #578 fix in src/devices/dev_jazz.c.  Scratch only.
set -u
B=/tmp/gxdivw; F=/tmp/gxfix578; W=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w578
rm -rf "$F"; cp -a "$B" "$F"; cd "$F" || exit 1
echo "MUTANT: src/devices/dev_jazz.c #578 fix (scratch clone, intentional)" > .MUTANT
python3 "$W/apply_fix578.py" "$F/src/devices/dev_jazz.c" || exit 1
rm -f src/devices/dev_jazz.o
make -j4 > make_fix.log 2>&1; rc=$?; echo "make rc=$rc"
if [ -x gxemul ] && [ gxemul -nt src/devices/dev_jazz.c ]; then echo "BINARY_FRESH $(ls -la --time-style=+%T gxemul | awk '{print $5, $6}')"; else echo "BINARY_STALE_OR_MISSING"; tail -5 make_fix.log; fi
diff -u "$B/src/devices/dev_jazz.c" "$F/src/devices/dev_jazz.c" > "$W/product.diff"; echo "product.diff lines: $(wc -l < "$W/product.diff")"
bash "$W/run_witness578.sh" "$F/gxemul" fixed
