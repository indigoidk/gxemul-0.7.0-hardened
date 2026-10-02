#!/bin/bash
# kill529b.sh -- #529 kill table 2 (TARGETED), scratch clone /tmp/gxopuscrime, baseline = the #529 working set.
# Superset warrant: table 2's instrument only ADDS rows or makes a row stricter (the `said' pattern now includes the
# `(once) ]' marker); every table-1 session's commands are unchanged, so every table-1 kill stands -- re-measured on
# BASE for a false red.  NEW mutants run on the NEW instrument; the pass-2 seats' claimed ESCAPES also run on the
# table-1 instrument, so each escape is MEASURED, not inferred (the Opus seat already measured its own on it:
# opus_pass2_20260913/logs/, so those are not repeated).  Launch from a frozen copy.
set -u
K=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable2_20260913
K1=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable_20260913
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopuscrime
B=/tmp/gxcrime529b_bins
F=src/devices/dev_sgi_ip32.c
PROBE=/tmp/crime_width_probe.table2.py
OLDPROBE=$K1/crime_width_probe.table1.py
MUT=/tmp/mutants529b.table2.py
NEW="${NEW:-base revwrite addrrc mmreads fdebug wstore acc8dog acc4low annlow only1r only2r only1w only2w dogft timeft imaskft ctlrdft acc8mid a_lo10 a_istat l_noonce l_addrmask x_mc4 x_mc8}"
OLD="${OLD:-addrrc mmreads fdebug wstore acc8dog acc4low annlow}"
mkdir -p "$B" "$K/logs" "$K/builds"
cp "$SEC/regress/crime_width_probe.py" "$PROBE"
cp "$PROBE" "$K/crime_width_probe.table2.py"
cp "$K/mutants529b.py" "$MUT"
md5sum "$PROBE" "$OLDPROBE" "$MUT" "$SEC/$F" | tee "$K/logs/INSTRUMENT.md5"
cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
echo "$F #529 kill table 2 (main loop) -- restore from GXEMUL-SEC" > .MUTANT
build() {
    rm -f src/devices/dev_sgi_ip32.o
    make -j4 > "$K/builds/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1"
    else
        echo "BUILD_FAIL $1 rc=$rc"; tail -20 "$K/builds/build_$1.log"; return 1
    fi
}
for m in $NEW; do
    python3 "$MUT" "$m" "$SEC/$F" "$F" || { echo "APPLY FAILED $m"; exit 1; }
    diff -u "$SEC/$F" "$F" > "$K/logs/$m.diff"
    if [ "$m" = base ]; then cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN" || { echo "BASELINE_CMP DIFFERS"; exit 1; }; fi
    build "$m" || exit 1
done
for m in $NEW; do
    [ "$m" = base ] || { cmp -s "$B/base" "$B/$m" && echo "NOTE $m BINARY IDENTICAL TO base"; }
done
for m in $NEW; do
    python3 -u "$PROBE" "$B/$m" "$m" > "$K/logs/probe_$m.raw" 2>&1
    echo "NEW $m $(grep '^CRIMEP_RESULT=' "$K/logs/probe_$m.raw") $(grep '^CRIMEP_CONTROL=' "$K/logs/probe_$m.raw") $(grep -c '^CRIMEP_DONE' "$K/logs/probe_$m.raw")"
done
for m in $OLD; do
    python3 -u "$OLDPROBE" "$B/$m" "$m" > "$K/logs/probe_T1INSTR_$m.raw" 2>&1
    echo "T1INSTR $m $(grep '^CRIMEP_RESULT=' "$K/logs/probe_T1INSTR_$m.raw") $(grep '^CRIMEP_CONTROL=' "$K/logs/probe_T1INSTR_$m.raw") $(grep -c '^CRIMEP_DONE' "$K/logs/probe_T1INSTR_$m.raw")"
done
cp "$SEC/$F" "$F"
build restored || exit 1
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"; else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; fi
cmp -s "$B/base" "$B/restored" && echo "restored == base (byte-identical)" || echo "restored differs from base"
echo KILL529B_DONE
