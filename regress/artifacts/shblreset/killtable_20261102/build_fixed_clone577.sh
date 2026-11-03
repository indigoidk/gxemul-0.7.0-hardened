#!/bin/bash
# build_fixed_clone577.sh -- /tmp/gxfix577 = /tmp/gxdivw (HEAD 987cb596) + the #577 shblreset fix in src/cpus/cpu_sh.c.  Scratch clone only.
set -u
B=/tmp/gxdivw; F=/tmp/gxfix577
rm -rf "$F"; cp -a "$B" "$F"; cd "$F" || exit 1
echo "MUTANT: src/cpus/cpu_sh.c #577 fix (scratch clone, intentional)" > .MUTANT
python3 /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w577/apply_fix577.py "$F/src/cpus/cpu_sh.c" || exit 1
rm -f src/cpus/cpu_sh*.o
make -j4 > make_fix.log 2>&1; rc=$?; echo "make rc=$rc"
if [ -x gxemul ] && [ gxemul -nt src/cpus/cpu_sh.c ]; then echo "BINARY_FRESH $(ls -la --time-style=+%T gxemul | awk '{print $5, $6}')"; else echo "BINARY_STALE_OR_MISSING"; tail -5 make_fix.log; fi
diff -u "$B/src/cpus/cpu_sh.c" "$F/src/cpus/cpu_sh.c" > /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w577/product.diff; wc -l /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w577/product.diff
