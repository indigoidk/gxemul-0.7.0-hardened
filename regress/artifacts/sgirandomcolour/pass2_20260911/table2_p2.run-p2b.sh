#!/bin/bash
#  #519 PASS-2 KILL TABLE -- Opus measuring seat.
#  Runs in a SCRATCH CLONE.  Writes NO project tree except the artifacts directory.
#  Launch from a FROZEN COPY of this file.

SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/p2
T3=$SEC/regress/artifacts/sgirandomcolour/killtable3_20260910
OUT=$SEC/regress/artifacts/sgirandomcolour/pass2_20260911
CLONE=/tmp/gxop519p2
BL=$OUT/BASELINE_FIX519_P2.c
PROBE=$OUT/sgi_re_colourdefault_probe.P2FROZEN.py
CTRL=$OUT/ctrl519p2.P2FROZEN.py
MUT=$OUT/mut519p2b.P2FROZEN.py
SRC=$CLONE/src/devices/dev_sgi_re.c
SCORES=$OUT/SCORES_P2B.txt

mkdir -p "$OUT"

#  ---- freeze everything this table runs, into the artifacts dir (durable path) ----
cp "$T3/BASELINE_FIX519_T3.c" "$BL"
cp "$SEC/regress/sgi_re_colourdefault_probe.py" "$PROBE"
cp "$SP/ctrl519p2.py" "$CTRL"
cp "$SP/mut519p2.py" "$MUT"

exec > >(tee -a "$OUT/TABLE_P2B.out") 2>&1
echo "=== #519 PASS-2 TABLE B (negative controls) start $(date) ==="
echo "clone      $CLONE"
echo "baseline   $(md5sum "$BL" | cut -c1-8)   (T3 named baseline, copied here)"
echo "instrument $(md5sum "$PROBE" | cut -c1-8)   (the round's live 59-row probe, frozen)"
echo "control    $(md5sum "$CTRL" | cut -c1-8)"
echo "mutator    $(md5sum "$MUT" | cut -c1-8)"

#  ---- the named baseline must equal SEC right now, or the table is measuring the wrong thing ----
if cmp -s "$BL" "$SEC/src/devices/dev_sgi_re.c"; then
    echo "baseline vs SEC now: IDENTICAL"
else
    echo "*** baseline vs SEC now: DIFFERS -- ABORTING ***"; exit 1
fi
if cmp -s "$PROBE" "$SEC/regress/sgi_re_colourdefault_probe.py"; then
    echo "frozen instrument vs live probe: IDENTICAL"
else
    echo "*** frozen instrument vs live probe: DIFFERS -- ABORTING ***"; exit 1
fi

#  ---- CLONE-LOCAL SENTINEL, written BEFORE mutant 1, naming the frozen baseline ----
printf '%s\n' \
  "src/devices/dev_sgi_re.c -- #519 PASS-2 kill table, Opus measuring seat" \
  "RESTORE FROM: $BL  (the frozen baseline, NEVER this script's own backup)" \
  "written $(date)" > "$CLONE/.MUTANT"
echo "sentinel: $(test -f "$CLONE/.MUTANT" && echo PRESENT || echo MISSING)"

: > "$SCORES"
echo "=== #519 PASS-2 TABLE B (negative controls)  $(date) ===" >> "$SCORES"

build_leg () {
    #  $1 = leg name.  Returns 0 on a build whose BINARY IS NEWER THAN ITS SOURCE.
    rm -f "$CLONE/src/devices/dev_sgi_re.o" "$CLONE/gxemul"
    ( cd "$CLONE" && make -j4 ) > "$OUT/build_$1.log" 2>&1
    #  the make return code is NOT the test; the timestamp pair is
    if [ -x "$CLONE/gxemul" ] && [ "$CLONE/gxemul" -nt "$SRC" ]; then
        return 0
    fi
    return 1
}

run_leg () {
    #  $1 = leg name
    local nm=$1
    python3 -u "$PROBE" "$CLONE/gxemul" "$nm" > "$OUT/$nm.raw" 2>&1
    python3 -u "$CTRL"  "$CLONE/gxemul" "$nm" > "$OUT/$nm.ctrl" 2>&1
    local score sent csent cres
    score=$(grep -o 'SGICOLOUR_RESULT=[0-9]*/[0-9]*' "$OUT/$nm.raw" | tail -1)
    sent=$(tail -1 "$OUT/$nm.raw")
    cres=$(grep -o 'SGICTRL_RESULT=[0-9]*/[0-9]*' "$OUT/$nm.ctrl" | tail -1)
    csent=$(tail -1 "$OUT/$nm.ctrl")
    local reds
    reds=$(grep ' FAIL$' "$OUT/$nm.raw" | awk '{printf "%s,", $1}' | sed 's/,$//')
    local cvals
    cvals=$(grep -o 'CTRL_T1YCRCB=.*' "$OUT/$nm.ctrl" | tail -1)
    printf '%-22s %-9s sentinel=%-16s | CTRL %-9s sentinel=%-14s | %s\n' \
        "$nm" "${score#SGICOLOUR_RESULT=}" "$sent" "${cres#SGICTRL_RESULT=}" "$csent" "$cvals" | tee -a "$SCORES"
    if [ -n "$reds" ]; then echo "    probe reds: $reds" | tee -a "$SCORES"; fi
    local creds
    creds=$(grep ' FAIL$' "$OUT/$nm.ctrl" | awk '{printf "%s,", $1}' | sed 's/,$//')
    if [ -n "$creds" ]; then echo "    CTRL  reds: $creds" | tee -a "$SCORES"; fi
}

#  ================================================================= BASE
echo "--- leg BASE $(date) ---"
cp "$BL" "$SRC"
if build_leg BASE_B; then
    echo "BASE_B build: FRESH ($(ls -la "$CLONE/gxemul" | awk '{print $6,$7,$8}') over source $(ls -la "$SRC" | awk '{print $6,$7,$8}'))"
    run_leg BASE_B
else
    echo "*** BASE_B BUILD FAILED -- ABORTING ***" | tee -a "$SCORES"; exit 1
fi

#  ================================================================= MUTANTS
for m in M34_ofsguard M35_xguard M36_yguard M37_fgvalue; do
    echo "--- leg $m $(date) ---"
    cp "$BL" "$SRC"                       # restore from the FROZEN BASELINE, never a backup
    if ! python3 "$MUT" "$SRC" "$m" > "$OUT/mutate_$m.log" 2>&1; then
        echo "$m *** MUTATE FAILED rc=$? ***" | tee -a "$SCORES"
        cat "$OUT/mutate_$m.log"
        continue
    fi
    if build_leg "$m"; then
        run_leg "$m"
    else
        echo "$m *** BUILD FAILED (binary not newer than source) ***" | tee -a "$SCORES"
        tail -20 "$OUT/build_$m.log"
    fi
done

#  ================================================================= RESTORE + TWO-PART CLEARANCE
echo "=== RESTORE from the frozen baseline, then the TWO-PART clearance ===" | tee -a "$SCORES"
cp "$BL" "$SRC"
rm -f "$CLONE/src/devices/dev_sgi_re.o" "$CLONE/gxemul"
( cd "$CLONE" && make -j4 ) > "$OUT/build_RESTORE.log" 2>&1
if cmp -s "$SRC" "$SEC/src/devices/dev_sgi_re.c"; then
    P1="CLEAN"
else
    P1="*** DIFFERS ***"
fi
if [ -x "$CLONE/gxemul" ] && [ "$CLONE/gxemul" -nt "$SRC" ]; then P2="FRESH"; else P2="*** STALE ***"; fi
echo "PART1 clone source vs SEC:        $P1" | tee -a "$SCORES"
echo "PART2 [ gxemul -nt dev_sgi_re.c ]: $P2" | tee -a "$SCORES"
if [ "$P1" = "CLEAN" ] && [ "$P2" = "FRESH" ]; then
    rm -f "$CLONE/.MUTANT"
    echo "sentinel CLEARED -- both parts clean" | tee -a "$SCORES"
else
    echo "*** SENTINEL LEFT IN PLACE -- clearance incomplete ***" | tee -a "$SCORES"
fi

#  ================================================================= LOG SENTINEL AUDIT
echo "=== log sentinel audit (a preserved log is verified by its completion sentinel) ===" | tee -a "$SCORES"
for f in "$OUT"/*.raw; do
    printf '  %-28s %s\n' "$(basename "$f")" "$(tail -1 "$f")" | tee -a "$SCORES"
done
for f in "$OUT"/*.ctrl; do
    printf '  %-28s %s\n' "$(basename "$f")" "$(tail -1 "$f")" | tee -a "$SCORES"
done
echo "=== TABLE P2 done $(date) ===" | tee -a "$SCORES"
echo "TABLE_P2_DONE"
