#!/bin/bash
#  Restore the scratch clone's dev_lca.c from GXEMUL-SEC, rebuild, verify BOTH parts, then clear the sentinel.
set -u
SRC=/mnt/c/DocumentNoSnc/CC/GXEMUL
CL=/tmp/gxopus530p2
BINS=/tmp/gxopus530p2_bins
LOGS=/tmp/gxopus530p2_logs
cd "$CL" || exit 2
echo "== $(date '+%F %T') restore from GXEMUL-SEC"
cp "$SRC/GXEMUL-SEC/src/devices/dev_lca.c" src/devices/dev_lca.c || exit 3
rm -f src/devices/dev_lca.o gxemul
make -j2 > "$LOGS/build_restore.log" 2>&1
echo "make rc=$?"
cmp src/devices/dev_lca.c "$SRC/GXEMUL-SEC/src/devices/dev_lca.c"; P1=$?
echo "part 1 (source cmp vs GXEMUL-SEC) rc=$P1"
if [ -f gxemul ] && [ gxemul -nt src/devices/dev_lca.c ] && [ src/devices/dev_lca.o -nt src/devices/dev_lca.c ]; then P2=0; else P2=1; fi
echo "part 2 (gxemul -nt dev_lca.c, dev_lca.o -nt dev_lca.c) rc=$P2"
md5sum gxemul "$BINS/base" src/devices/dev_lca.c
cmp -s gxemul "$BINS/base" && echo "restored binary IDENTICAL to the base binary measured" || echo "restored binary differs from bins/base (check)"
if [ $P1 -eq 0 ] && [ $P2 -eq 0 ]; then
    rm -f .MUTANT && echo "SENTINEL REMOVED"
else
    echo "SENTINEL KEPT -- restore not verified"
fi
ls -la .MUTANT 2>&1
echo "RESTORE_DONE $(date '+%F %T')"
