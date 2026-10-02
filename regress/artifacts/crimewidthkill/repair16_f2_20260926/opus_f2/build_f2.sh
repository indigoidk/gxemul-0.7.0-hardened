#!/bin/bash
# build_f2.sh NAME... -- build each named leg of mutants_f2.py in the Opus seat's scratch clone /tmp/gxopus_r15p2,
# binaries to /tmp/gxopus_r15p2_bins/<NAME>.  Sentinel before the first mutation; cleared only after the restore is
# VERIFIED (cmp against GXEMUL-SEC AND a rebuilt binary newer than the restored source, byte-identical to table 14's base).
set -u
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/repair16_f2_20260926/opus_f2
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus_r15p2
B=/tmp/gxopus_r15p2_bins
F=src/devices/dev_sgi_ip32.c
MUT=$A/mutants_f2.py
mkdir -p "$B" "$A/builds" "$A/mutants"
cd "$C" || { echo "clone missing"; exit 1; }
if [ -e .MUTANT ]; then echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; fi
cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN $(md5sum "$F" | cut -c1-8)" || { echo "clone differs from SEC -- abort"; exit 1; }
echo "$F  opus F2 mutant builds -- restore from GXEMUL-SEC, then REBUILD" > .MUTANT

build() {
    rm -f src/devices/dev_sgi_ip32.o
    nice -n 5 make -j4 > "$A/builds/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1 $(md5sum "$B/$1" | cut -c1-8) $(date '+%T')"
    else echo "BUILD_FAIL $1 rc=$rc"; tail -25 "$A/builds/build_$1.log"; return 1; fi
}

for m in "$@"; do
    python3 "$MUT" "$m" "$SEC/$F" "$F" || { echo "APPLY FAILED $m"; continue; }
    diff -u "$SEC/$F" "$F" > "$A/mutants/$m.diff"
    build "$m" || echo "NOTE $m DID NOT BUILD"
done

cp "$SEC/$F" "$F"
if build restored && cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ] && cmp -s gxemul /tmp/gxopus_r14_bins14/base; then
    rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes binary==table14-base $(md5sum "$F" | cut -c1-8)"
else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; fi
for m in "$@"; do
    [ -f "$B/$m" ] && cmp -s "$B/$m" "$B/restored" && echo "NOTE $m BINARY IDENTICAL TO restored -- EQUIVALENT BUILD"
done
cmp -s "$B/P_ist1r_set" /tmp/gxopus_r14_bins16/W_istlb 2>/dev/null && echo "P_ist1r_set == table-16 W_istlb (byte-identical)"
cmp -s "$B/P_imk1r_set" /tmp/gxopus_r14_bins16/W_imklb 2>/dev/null && echo "P_imk1r_set == table-16 W_imklb (byte-identical)"
cmp -s "$B/D_doglatch" /tmp/gxopus_r14_bins16/L_dogclr 2>/dev/null && echo "D_doglatch == table-16 L_dogclr (byte-identical)" \
    || echo "D_doglatch differs from table-16 L_dogclr (different text; not expected to be byte-identical)"
echo "BUILD_F2_DONE $(date '+%F %T')"
