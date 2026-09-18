#!/bin/bash
#  opus530p2 setup: scratch clone of build/, source-identity checks, sentinel, base rebuild.
set -u
SRC=/mnt/c/DocumentNoSnc/CC/GXEMUL
WIN=/mnt/c/Users/User00/AppData/Local/Temp/opus530p2
CL=/tmp/gxopus530p2
BINS=/tmp/gxopus530p2_bins
PR=/tmp/gxopus530p2_probe
LOGS=/tmp/gxopus530p2_logs

if [ -e "$CL" ]; then echo "CLONE ALREADY EXISTS -- refusing to overwrite"; exit 2; fi
mkdir -p "$BINS" "$PR" "$LOGS"
echo "== $(date '+%F %T') cp -a build -> $CL"
cp -a "$SRC/build" "$CL" || { echo "CP FAILED"; exit 3; }
[ -e "$CL/.MUTANT" ] && echo "WARNING: clone inherited a .MUTANT sentinel: $(cat $CL/.MUTANT)"

echo "== source identity, dev_lca.c"
cmp "$CL/src/devices/dev_lca.c" "$SRC/GXEMUL-SEC/src/devices/dev_lca.c"; echo "cmp clone-vs-SEC-worktree rc=$?"
cmp "$CL/src/devices/dev_lca.c" "$WIN/ref/src_devices_dev_lca.c"; echo "cmp clone-vs-8bd97e4-blob rc=$?"
md5sum "$CL/src/devices/dev_lca.c" "$SRC/GXEMUL-SEC/src/devices/dev_lca.c" "$WIN/ref/src_devices_dev_lca.c"

echo "== source identity, the rest of the path (clone vs 8bd97e4 blob)"
for r in "$WIN"/ref/*; do
    b=$(basename "$r")
    f=$(echo "$b" | sed -e 's#^src_devices_#src/devices/#' -e 's#^src_cpus_#src/cpus/#' -e 's#^src_core_#src/core/#' -e 's#^src_machines_#src/machines/#')
    if cmp -s "$CL/$f" "$r"; then echo "SAME  $f"; else echo "DIFF  $f"; fi
done

echo "== sentinel"
echo "dev_lca.c: opus530p2 measuring seat -- variants of DEVICE_ACCESS(lca_isa); restore from GXEMUL-SEC then cmp + rebuild" > "$CL/.MUTANT"
cat "$CL/.MUTANT"

echo "== base rebuild in the clone ($(date '+%F %T'))"
cd "$CL" || exit 4
rm -f src/devices/dev_lca.o gxemul
make -j2 > "$LOGS/build_base.log" 2>&1
rc=$?
echo "make rc=$rc"
tail -3 "$LOGS/build_base.log"
ls -la --time-style=full-iso gxemul src/devices/dev_lca.o src/devices/dev_lca.c 2>&1
if [ -f gxemul ] && [ gxemul -nt src/devices/dev_lca.c ] && [ src/devices/dev_lca.o -nt src/devices/dev_lca.c ]; then
    echo "FRESH: gxemul and dev_lca.o are newer than dev_lca.c"
    cp -p gxemul "$BINS/base"
    md5sum "$BINS/base"
else
    echo "NOT FRESH -- build failed or stale"
    exit 5
fi
cp "$WIN/lca_widewrite_probe.8bd97e4.py" "$PR/lca_widewrite_probe.py"
cp "$WIN/alpha_dummy.bin" "$PR/alpha_dummy.bin"
md5sum "$PR/lca_widewrite_probe.py" "$PR/alpha_dummy.bin"
echo "SETUP_DONE $(date '+%F %T')"
