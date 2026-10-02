#!/bin/bash
# kill8b.sh -- #529 closing pass 8, SUPPLEMENTARY table: the two questions the coordinator forwarded.
#   (1) is CONTROL 4R really EQUIVALENT, or is table 11's C_ctl4r leg merely vacuous?   -> ctl4r.py
#   (2) does the glm seat's LATCH-CLEAR bypass at TIME 4W/4R escape the shipped 188-row probe?
#                                                                                      -> the shipped probe + t4clear.py
# SCRATCH CLONE /tmp/gxopusc8 only.  Launch from a FROZEN COPY.
set -u
A=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close8_20260916
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
K11=$SEC/regress/artifacts/crimewidthkill/killtable11_20260916
C=/tmp/gxopusc8
B=/tmp/gxopusc8_bins
F=src/devices/dev_sgi_ip32.c
PROBE=/tmp/crime_width_probe.close8.py
CTL=/tmp/ctl4r.frozen.py
T4C=/tmp/t4clear.frozen.py
RST=/tmp/ctlreset.frozen.py
MUT=/tmp/mutants8b.frozen.py
LIST="C_ctl4r G_lane_ctl G_glm_tim4clear G_clr_ist4r G_clr_ctl4r G_clr_imk4r K_ctl4w_reset_post K_ctl8w_reset_post"
mkdir -p "$B" "$A/logs2" "$A/builds" "$A/mutants"
cp "$SEC/regress/crime_width_probe.py" "$PROBE"
cp "$A/scripts/ctl4r.py" "$CTL"
cp "$A/scripts/t4clear.py" "$T4C"
cp "$A/scripts/ctlreset.py" "$RST"
cp "$A/scripts/mutants8b.py" "$MUT"
md5sum "$PROBE" "$CTL" "$T4C" "$RST" "$MUT" "$SEC/$F" | tee "$A/logs2/INSTRUMENT.md5"
cd "$C" || exit 1
if [ -e .MUTANT ]; then echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; fi
echo "$F  #529 closing pass 8 SUPPLEMENTARY -- restore from GXEMUL-SEC, then REBUILD" > .MUTANT
build() {
    rm -f src/devices/dev_sgi_ip32.o
    make -j4 > "$A/builds/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1"
    else
        echo "BUILD_FAIL $1 rc=$rc"; tail -25 "$A/builds/build_$1.log"; return 1
    fi
}
restore_and_exit() {
    cp "$SEC/$F" "$F"
    build restored && cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ] && rm -f .MUTANT && echo "CLONE RESTORED after failure"
    exit 1
}
for m in $LIST; do
    python3 "$MUT" "$m" "$SEC/$F" "$F" || { echo "APPLY FAILED $m"; restore_and_exit; }
    diff -u "$SEC/$F" "$F" > "$A/mutants/$m.diff"
    build "$m" || restore_and_exit
done
cp "$SEC/$F" "$F"
build restored2 || exit 1
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"; else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; fi
if cmp -s "$B/base" "$B/restored2"; then echo "restored2 == base (byte-identical)"; else echo "restored2 differs from base"; fi
#  CROSS-CHECK: my C_ctl4r must be the same edit table 11 built.  A re-derivation that silently differs would make
#  this whole supplementary table a measurement of something else.
echo "--- cross-check my C_ctl4r against killtable11's own diff (hunk bodies only) ---"
grep '^[+-][^+-]' "$A/mutants/C_ctl4r.diff" > /tmp/c8_mine.hunk
grep '^[+-][^+-]' "$K11/logs/C_ctl4r.diff" > /tmp/c8_theirs.hunk
if cmp -s /tmp/c8_mine.hunk /tmp/c8_theirs.hunk; then echo "C_CTL4R_EDIT IDENTICAL to killtable11"; else echo "C_CTL4R_EDIT DIFFERS"; diff -u /tmp/c8_theirs.hunk /tmp/c8_mine.hunk; fi
#  ---- probes ----
echo "=== ctl4r.py: base / C_ctl4r / G_lane_ctl ==="
for m in base C_ctl4r G_lane_ctl; do
    python3 -u "$CTL" "$B/$m" "$m" > "$A/logs2/ctl4r_$m.out" 2>&1
    echo "$m $(grep '^CTL4R_RESULT=' "$A/logs2/ctl4r_$m.out") last=[$(tail -1 "$A/logs2/ctl4r_$m.out")] FAILING:$(grep '^FAILING:' "$A/logs2/ctl4r_$m.out" | cut -c9-)"
done
echo "=== t4clear.py: base / G_glm_tim4clear (and C_ctl4r as an off-cell negative control) ==="
for m in base G_glm_tim4clear C_ctl4r; do
    python3 -u "$T4C" "$B/$m" "$m" > "$A/logs2/t4clear_$m.out" 2>&1
    echo "$m $(grep '^T4CLEAR_RESULT=' "$A/logs2/t4clear_$m.out") last=[$(tail -1 "$A/logs2/t4clear_$m.out")] FAILING:$(grep '^FAILING:' "$A/logs2/t4clear_$m.out" | cut -c9-)"
done
echo "=== t4clear.py on the whole latch-clear class, to show which members the owed row catches ==="
for m in G_clr_ist4r G_clr_ctl4r G_clr_imk4r; do
    python3 -u "$T4C" "$B/$m" "$m" > "$A/logs2/t4clear_$m.out" 2>&1
    echo "$m $(grep '^T4CLEAR_RESULT=' "$A/logs2/t4clear_$m.out") last=[$(tail -1 "$A/logs2/t4clear_$m.out")] FAILING:$(grep '^FAILING:' "$A/logs2/t4clear_$m.out" | cut -c9-)"
done
echo "=== ctlreset.py: the codex cell's OWED ROW, base against both K_ctl*w_reset_post ==="
for m in base K_ctl4w_reset_post K_ctl8w_reset_post G_glm_tim4clear; do
    python3 -u "$RST" "$B/$m" "$m" > "$A/logs2/ctlreset_$m.out" 2>&1
    echo "$m $(grep '^CTLRESET_RESULT=' "$A/logs2/ctlreset_$m.out") last=[$(tail -1 "$A/logs2/ctlreset_$m.out")] FAILING:$(grep '^FAILING:' "$A/logs2/ctlreset_$m.out" | cut -c9-)"
done
echo "=== the SHIPPED 188-row probe on the class, FOUR lanes ==="
run188() {
    python3 -u "$PROBE" "$B/$1" "$1" > "$A/logs2/probe188_$1.raw" 2>&1
    echo "$1 $(grep '^CRIMEP_RESULT=' "$A/logs2/probe188_$1.raw") $(grep '^CRIMEP_CONTROL=' "$A/logs2/probe188_$1.raw") done=$(grep -c '^CRIMEP_DONE' "$A/logs2/probe188_$1.raw") FAILING:$(grep '^FAILING:' "$A/logs2/probe188_$1.raw" | cut -c9-)"
}
( run188 G_glm_tim4clear; run188 G_clr_imk4r;         run188 G_lane_ctl ) > "$A/logs2/p188_a.out" &
( run188 G_clr_ist4r;     run188 G_clr_ctl4r                            ) > "$A/logs2/p188_b.out" &
( run188 K_ctl4w_reset_post                                             ) > "$A/logs2/p188_c.out" &
( run188 K_ctl8w_reset_post                                             ) > "$A/logs2/p188_d.out" &
wait
cat "$A/logs2/p188_a.out" "$A/logs2/p188_b.out" "$A/logs2/p188_c.out" "$A/logs2/p188_d.out"
echo KILL8B_DONE
