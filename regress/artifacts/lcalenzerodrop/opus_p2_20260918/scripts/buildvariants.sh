#!/bin/bash
#  Build every variant in the scratch clone.  The clone carries a .MUTANT sentinel from setup.sh.
set -u
WIN=/mnt/c/Users/User00/AppData/Local/Temp/opus530p2
CL=/tmp/gxopus530p2
BINS=/tmp/gxopus530p2_bins
LOGS=/tmp/gxopus530p2_logs
cd "$CL" || exit 2
[ -f .MUTANT ] || { echo "NO SENTINEL -- refusing to mutate"; exit 3; }
md5sum "$BINS/base" | tee "$LOGS/bins.md5"
for v in "$@"; do
    echo "== $(date '+%F %T') variant $v"
    cp "$WIN/variants/dev_lca.c.$v" src/devices/dev_lca.c || exit 4
    rm -f src/devices/dev_lca.o gxemul
    make -j2 > "$LOGS/build_$v.log" 2>&1
    echo "make rc=$?"
    grep -iE "error|warning" "$LOGS/build_$v.log" | head -5
    if [ -f gxemul ] && [ gxemul -nt src/devices/dev_lca.c ] && [ src/devices/dev_lca.o -nt src/devices/dev_lca.c ]; then
        cp -p gxemul "$BINS/$v"
        md5sum "$BINS/$v" src/devices/dev_lca.o | tee -a "$LOGS/bins.md5"
        if cmp -s "$BINS/$v" "$BINS/base"; then echo "!! $v binary IDENTICAL to base -- edit not live"; else echo "$v binary DIFFERS from base"; fi
    else
        echo "!! $v NOT FRESH -- build failed or stale"; exit 5
    fi
done
echo "BUILDVARIANTS_DONE $(date '+%F %T')"
