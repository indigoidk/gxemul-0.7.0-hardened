#!/bin/bash
# cleanup.sh -- verify /tmp/gxopus530c4 is restored (two-part clearance), then DELETE the clone and its bins.
C=/tmp/gxopus530c4
B=/tmp/gxopus530c4_bins
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
F=src/devices/dev_lca.c
cd "$C" || { echo "NO CLONE"; exit 1; }
ok=1
if [ -e .MUTANT ]; then echo "SENTINEL PRESENT"; cat .MUTANT; ok=0; else echo "no .MUTANT"; fi
if cmp -s "$F" "$SEC/$F"; then echo "dev_lca.c CMP_CLEAN vs GXEMUL-SEC"; else echo "dev_lca.c DIFFERS"; ok=0; fi
if [ gxemul -nt "$F" ]; then echo "gxemul -nt dev_lca.c: yes"; else echo "gxemul NOT newer"; ok=0; fi
if cmp -s gxemul "$B/base"; then echo "clone gxemul == base binary"; else echo "clone gxemul != base"; ok=0; fi
for m in Wpure dataA dataB L1gate L3gate WT6 WTsplit R2w R2w2 RD2L0; do
    if cmp -s "$B/base" "$B/$m"; then echo "WARNING $m identical to base"; else echo "$m differs from base (as a mutant must)"; fi
done
md5sum "$SEC/$F"
if [ "$ok" = 1 ]; then
    cd /tmp && rm -rf "$C" "$B" && echo "CLONE AND BINS DELETED"
else
    echo "NOT DELETED -- clearance failed"
fi
ls -d "$C" "$B" 2>&1
echo CLEANUP_DONE
