#!/bin/bash
#  #519 KILL TABLE 4 -- the CLASS CLOSURE.  Opus measuring seat.
#  Scratch clone only.  Writes no project tree except the artifacts directory.
#  Launch from a FROZEN COPY.
#
#  LEG ORDER IS BY PRIORITY, not alphabetical: BASE, then the six pass-2 escapes (which MUST
#  now die), then the three coordinate mutants the 59-row instrument already killed (which must
#  STILL die), then the three new-axis discriminators, then M38, then the table-3 regression set
#  for comparability.  So the load-bearing result lands first.

SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/p2
OUT=$SEC/regress/artifacts/sgirandomcolour/killtable4_20260911
CLONE=/tmp/gxop519p2
BL=$OUT/BASELINE_FIX519_T4.c
PROBE=$OUT/sgi_re_colourdefault_probe.T4FROZEN.py
MUT=$OUT/mut519d.T4FROZEN.py
SRC=$CLONE/src/devices/dev_sgi_re.c
SCORES=$OUT/SCORES4.txt

mkdir -p "$OUT"
cp "$SEC/src/devices/dev_sgi_re.c"            "$BL"
cp "$SEC/regress/sgi_re_colourdefault_probe.py" "$PROBE"
cp "$SP/mut519d.py"                            "$MUT"
cp "$SP/table4.run-t4.sh"                      "$OUT/table4.run-t4.sh" 2>/dev/null

exec > >(tee -a "$OUT/TABLE4.out") 2>&1
echo "=== #519 KILL TABLE 4 (class closure) start $(date) ==="
echo "clone      $CLONE"
echo "baseline   $(md5sum "$BL"   | cut -c1-8)   (dev_sgi_re.c -- UNCHANGED product code)"
echo "instrument $(md5sum "$PROBE"| cut -c1-8)   (the 77-row closure)"
echo "mutator    $(md5sum "$MUT"  | cut -c1-8)"
echo "PRETABLE.out mtime: $(stat -c %y "$OUT/PRETABLE.out" 2>/dev/null)"

#  the product file must be the one table 3 named, or this table measures something else
if [ "$(md5sum "$BL" | cut -c1-32)" = "6e2c68731a6fc73ee656596816d5ec46" ]; then
    echo "baseline IS table 3's named baseline (6e2c6873): product code untouched by pass 4"
else
    echo "*** BASELINE IS NOT table 3's -- ABORTING ***"; exit 1
fi
if cmp -s "$PROBE" "$SEC/regress/sgi_re_colourdefault_probe.py"; then
    echo "frozen instrument vs live probe: IDENTICAL"
else
    echo "*** instrument DIFFERS from live probe -- ABORTING ***"; exit 1
fi

printf '%s\n' "src/devices/dev_sgi_re.c -- #519 KILL TABLE 4 (class closure), Opus seat" \
  "RESTORE FROM: $BL  (the frozen baseline, NEVER this script's own backup)" \
  "written $(date)" > "$CLONE/.MUTANT"
echo "sentinel: $(test -f "$CLONE/.MUTANT" && echo PRESENT || echo MISSING)"

: > "$SCORES"
echo "=== #519 KILL TABLE 4 (class closure)  $(date) ===" >> "$SCORES"

build_leg () {
    rm -f "$CLONE/src/devices/dev_sgi_re.o" "$CLONE/gxemul"
    ( cd "$CLONE" && make -j4 ) > "$OUT/build_$1.log" 2>&1
    [ -x "$CLONE/gxemul" ] && [ "$CLONE/gxemul" -nt "$SRC" ]
}

run_leg () {
    local nm=$1
    python3 -u "$PROBE" "$CLONE/gxemul" "$nm" > "$OUT/$nm.raw" 2>&1
    local score sent reds n t
    score=$(grep -o 'SGICOLOUR_RESULT=[0-9]*/[0-9]*' "$OUT/$nm.raw" | tail -1)
    sent=$(tail -1 "$OUT/$nm.raw")
    n=$(grep -c ' FAIL$' "$OUT/$nm.raw"); t=$(grep -cE ' (ok|FAIL)$' "$OUT/$nm.raw")
    reds=$(grep ' FAIL$' "$OUT/$nm.raw" | cut -c1-16 | sed 's/ *$//' | paste -sd, -)
    printf '%-26s %-9s %2d red of %2d   sentinel=%s\n' \
        "$nm" "${score#SGICOLOUR_RESULT=}" "$n" "$t" "$sent" | tee -a "$SCORES"
    if [ -n "$reds" ]; then echo "    reds: $reds" | tee -a "$SCORES"; fi
}

echo "--- leg BASE $(date) ---"
cp "$BL" "$SRC"
if build_leg BASE; then run_leg BASE; else
    echo "*** BASE BUILD FAILED -- ABORTING ***" | tee -a "$SCORES"; exit 1; fi

ESCAPES="M30_tilenrdecline M31_tilenrguard M32_tilenrxdecline M33_tiledorigin M37_fgvalue M28_permit_othernibbles"
CONTROLS="M34_ofsguard M35_xguard M36_yguard"
NEWAXES="M39_xofsguard M40_tilenrydecline M41_jointtileY M38_acceptannounce"
REGRESS="M1_reinstate M11_null M2_noguard M3_zerofill M4_okinlatch M5_nolatch M6_sharedbit \
M7_silent M8_declineall M9_dropcase_ci M10_dropcase_abgr M12_prefix_reworded M16_dropcase_rgb \
M17_dropcase_rgba M13_widthdecline M14_lineardecline M15_jointwidthlin M20_permit_tlba \
M21_permit_tlbb M22_permit_tlbc M23_permit_tiled_d4 M24_permit_d2d8 M25_permit_d8 \
M26_permit_d2 M27_permit_bc_d2d8"

for grp in "THE SIX PASS-2 ESCAPES -- these MUST now die:$ESCAPES" \
           "ALREADY-KILLED COORDINATE MUTANTS -- must STILL die:$CONTROLS" \
           "NEW-AXIS DISCRIMINATORS:$NEWAXES" \
           "TABLE-3 REGRESSION SET (comparability):$REGRESS"; do
    echo "=== ${grp%%:*} ===" | tee -a "$SCORES"
    for m in ${grp#*:}; do
        echo "--- leg $m $(date) ---"
        cp "$BL" "$SRC"
        if ! python3 "$MUT" "$SRC" "$m" > "$OUT/mutate_$m.log" 2>&1; then
            echo "$m *** MUTATE FAILED ***" | tee -a "$SCORES"; cat "$OUT/mutate_$m.log"; continue
        fi
        if build_leg "$m"; then run_leg "$m"; else
            echo "$m *** BUILD FAILED (binary not newer than source) ***" | tee -a "$SCORES"
            tail -15 "$OUT/build_$m.log"
        fi
    done
done

echo "=== RESTORE from the frozen baseline, then the TWO-PART clearance ===" | tee -a "$SCORES"
cp "$BL" "$SRC"
rm -f "$CLONE/src/devices/dev_sgi_re.o" "$CLONE/gxemul"
( cd "$CLONE" && make -j4 ) > "$OUT/build_RESTORE.log" 2>&1
if cmp -s "$SRC" "$SEC/src/devices/dev_sgi_re.c"; then P1=CLEAN; else P1="*** DIFFERS ***"; fi
if [ -x "$CLONE/gxemul" ] && [ "$CLONE/gxemul" -nt "$SRC" ]; then P2=FRESH; else P2="*** STALE ***"; fi
echo "PART1 clone source vs SEC:        $P1" | tee -a "$SCORES"
echo "PART2 [ gxemul -nt dev_sgi_re.c ]: $P2" | tee -a "$SCORES"
if [ "$P1" = "CLEAN" ] && [ "$P2" = "FRESH" ]; then
    rm -f "$CLONE/.MUTANT"; echo "sentinel CLEARED -- both parts clean" | tee -a "$SCORES"
else
    echo "*** SENTINEL LEFT IN PLACE ***" | tee -a "$SCORES"; fi

echo "=== log sentinel audit ===" | tee -a "$SCORES"
for f in "$OUT"/*.raw; do
    printf '  %-30s %s\n' "$(basename "$f")" "$(tail -1 "$f")" | tee -a "$SCORES"
done
echo "=== TABLE 4 done $(date) ===" | tee -a "$SCORES"
echo "TABLE4_DONE"
