#!/bin/bash
# setup.sh -- opus closing pass 4 (#530): scratch clone /tmp/gxopus530c4, baseline = GXEMUL-SEC working-tree dev_lca.c
set -u
D=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus530c4
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus530c4
B=/tmp/gxopus530c4_bins
F=src/devices/dev_lca.c
[ -e "$C" ] && { echo "clone exists -- abort"; exit 1; }
cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$C" || exit 1
mkdir -p "$B"
cd "$C" || exit 1
rm -f .MUTANT
cp "$SEC/$F" "$F"
cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN" || { echo "BASELINE_CMP DIFFERS"; exit 1; }
md5sum "$F" "$SEC/$F"
rm -f src/cpus/*.o src/devices/dev_lca.o
make -j6 > "$D/logs/build_base.log" 2>&1
rc=$?
if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_lca.o -nt "$F" ]; then
    cp gxemul "$B/base"; echo "BUILD_OK base"; ls -la --time-style=full-iso gxemul "$F" src/devices/dev_lca.o
else echo "BUILD_FAIL base rc=$rc"; tail -20 "$D/logs/build_base.log"; fi
echo SETUP_DONE
