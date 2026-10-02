#!/bin/bash
# build6.sh -- clone build/ into /tmp/gxopuscrimec6, baseline from GXEMUL-SEC's working-tree dev_sgi_ip32.c, build the
# base and every mutant binary into /tmp/gxopuscrimec6_bins, restore + rebuild base + cmp at the end.
set -u
CLONE=/tmp/gxopuscrimec6
BINS=/tmp/gxopuscrimec6_bins
WD=/tmp/gxopuscrimec6_work
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opuscrimec6
MUT="$SP/mutate6.py"
rm -rf "$CLONE" "$BINS" "$WD"; mkdir -p "$BINS" "$WD"
cp -r /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$CLONE" || { echo CLONE FAILED; exit 1; }
rm -f "$CLONE/.MUTANT"
cp "$SEC/src/devices/dev_sgi_ip32.c" "$CLONE/src/devices/dev_sgi_ip32.c"
cp "$SEC/src/devices/dev_sgi_ip32.c" "$WD/dev_sgi_ip32.c.orig"
cmp -s "$CLONE/src/devices/dev_sgi_ip32.c" "$SEC/src/devices/dev_sgi_ip32.c" && echo "BASELINE cmp CLEAN vs SEC" || { echo "BASELINE cmp DIFFERS"; exit 1; }
md5sum "$SEC/src/devices/dev_sgi_ip32.c"
# frozen instrument + augmented instrument
cp "$SEC/regress/crime_width_probe.py" "$WD/probe.frozen.py"
cmp -s "$WD/probe.frozen.py" "$SEC/regress/crime_width_probe.py" && echo "PROBE frozen cmp CLEAN" || { echo PROBE DIFFERS; exit 1; }
md5sum "$WD/probe.frozen.py"
python3 "$SP/augprobe6.py" "$WD/probe.frozen.py" "$WD/probe.aug6.py" || exit 1
cd "$CLONE"
find . -name "*.o" -exec touch {} +
sleep 1
rm -f src/cpus/*.o src/devices/dev_sgi_ip32.o gxemul
echo "BUILDING BASE $(date +%T)"
make -j2 >"$WD/build_base.log" 2>&1; echo "MAKE_RC=$?"
if [ -f gxemul ] && [ gxemul -nt src/devices/dev_sgi_ip32.c ]; then echo "BASE BINARY FRESH"; else echo "BASE STALE/MISSING"; tail -8 "$WD/build_base.log"; exit 1; fi
cp gxemul "$BINS/base"
for name in $(python3 "$MUT" list); do
    [ "$name" = base ] && continue
    python3 "$MUT" "$name" "$WD/dev_sgi_ip32.c.orig" "$WD/mut_$name.c" || { echo "  $name MUTATE FAILED"; continue; }
    echo "$name: src/devices/dev_sgi_ip32.c mutated (restore from GXEMUL-SEC)" > "$CLONE/.MUTANT"
    cp "$WD/mut_$name.c" src/devices/dev_sgi_ip32.c
    rm -f src/devices/dev_sgi_ip32.o gxemul
    make >"$WD/build_$name.log" 2>&1
    if [ -f gxemul ] && [ gxemul -nt src/devices/dev_sgi_ip32.c ]; then
        cp gxemul "$BINS/$name"; echo "  $name BUILT $(diff "$WD/dev_sgi_ip32.c.orig" "$WD/mut_$name.c" | grep -c '^[<>]') diff lines"
    else
        echo "  $name BUILD FAILED/STALE"; tail -6 "$WD/build_$name.log"
    fi
    cp "$WD/dev_sgi_ip32.c.orig" src/devices/dev_sgi_ip32.c
done
# restore: source from SEC, rebuild, two-part clearance
cp "$SEC/src/devices/dev_sgi_ip32.c" src/devices/dev_sgi_ip32.c
rm -f src/devices/dev_sgi_ip32.o gxemul
make >"$WD/build_restore.log" 2>&1
if cmp -s src/devices/dev_sgi_ip32.c "$SEC/src/devices/dev_sgi_ip32.c" && [ gxemul -nt src/devices/dev_sgi_ip32.c ]; then
    rm -f "$CLONE/.MUTANT"; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"
    cmp -s gxemul "$BINS/base" && echo "restored binary == base (byte-identical)" || echo "restored binary differs from base (timestamps/paths?)"
else
    echo "CLONE RESTORE FAILED -- sentinel kept"
fi
ls -la "$BINS"
echo "BUILD6_DONE"
