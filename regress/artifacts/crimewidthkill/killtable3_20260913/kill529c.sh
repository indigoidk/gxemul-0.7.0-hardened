#!/bin/bash
# kill529c.sh -- #529 kill table 3 (TARGETED), scratch clone /tmp/gxopuscrime, baseline = the #529 working set.
# Warrant for targeting: table 3's instrument ADDS rows and appends accesses to existing sessions, and REORDERS one
# session (latch x5: lh first).  The mutants whose table-2 kill rested on a changed session (nolatch, latchinv on the
# latch session; wstore, acc8dog on the imask/istat controls) are RE-RUN here, and BASE is re-measured.  NEW mutants run
# on the NEW instrument; the F2 seats' claimed escapes not already measured by the Opus F2 seat also run on table 2's
# 71-row instrument, so each escape is MEASURED.  Launch from a frozen copy.
set -u
K=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable3_20260913
K1=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable2_20260913
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopuscrime
B=/tmp/gxcrime529c_bins
F=src/devices/dev_sgi_ip32.c
PROBE=/tmp/crime_width_probe.table3.py
OLDPROBE=$K1/crime_width_probe.table2.py
MUT=/tmp/mutants529c.table3.py
NEW="${NEW:-base istat2 imask2 time2 istatsh remap static_od rearm h_imask h_lbl lt_len lt_addr lt_wset wst_mc c_dog c_hrclr nolatch latchinv wstore acc8dog sft wstore31}"
OLD="${OLD:-istat2 imask2 time2 istatsh remap static_od rearm}"
mkdir -p "$B" "$K/logs" "$K/builds"
cp "$SEC/regress/crime_width_probe.py" "$PROBE"
cp "$PROBE" "$K/crime_width_probe.table3.py"
cp "$K/mutants529c.py" "$MUT"; cp "$K1/mutants529b.py" /tmp/mutants529b.py
md5sum "$PROBE" "$OLDPROBE" "$MUT" "$SEC/$F" | tee "$K/logs/INSTRUMENT.md5"
cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
echo "$F #529 kill table 3 (main loop) -- restore from GXEMUL-SEC" > .MUTANT
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
    python3 -u "$OLDPROBE" "$B/$m" "$m" > "$K/logs/probe_T2INSTR_$m.raw" 2>&1
    echo "T2INSTR $m $(grep '^CRIMEP_RESULT=' "$K/logs/probe_T2INSTR_$m.raw") $(grep '^CRIMEP_CONTROL=' "$K/logs/probe_T2INSTR_$m.raw") $(grep -c '^CRIMEP_DONE' "$K/logs/probe_T2INSTR_$m.raw")"
done
cp "$SEC/$F" "$F"
build restored || exit 1
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"; else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; fi
cmp -s "$B/base" "$B/restored" && echo "restored == base (byte-identical)" || echo "restored differs from base"
echo KILL529C_DONE
