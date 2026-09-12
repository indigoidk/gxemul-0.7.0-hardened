#!/bin/bash
#  xscaleinten kill table 3 (pass 2 adds RD0_ALLONES: 30 rows) -- scratch clone of build/, clone-local sentinel, one frozen instrument,
#  baseline NAMED as the current SEC cpu_arm_coproc.c.  cpu_arm_coproc.c compiles into the CPU objects,
#  so each leg removes ALL of src/cpus/*.o (the carrier's conservative rule).
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
K=$SEC/regress/artifacts/xscaleinten/killtable3_20260912
B=$SEC/regress/artifacts/xscaleinten/base_20260912
PROBE=$K/xscale_inten_probe.T3FROZEN.py
STUB=$B/xscale_stub.bin
C=/tmp/gxxs3
F=src/cpus/cpu_arm_coproc.c
SCORES=$K/SCORES.txt
LEGS="BASE HEAD M1 M5 M_OPCODE2 M_RD15 M_NREAD M_OP1 M_ISTEER_WR M_CRM M_RD0 M_MAGICBIT"

cp "$SEC/regress/xscale_inten_probe.py" "$PROBE" || exit 9     # freeze the 30-row instrument at launch
rm -rf "$C"; cp -a "$R/build" "$C" || exit 9
echo "$F xscale kill table 3 in progress" > "$C/.MUTANT"
{ echo "xscaleinten KILL TABLE 3   $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "baseline = SEC $F (post-fix working set)   probe = FROZEN 30-row ($(basename $PROBE))"
  cmp -s "$C/$F" "$SEC/$F" && echo "baseline cmp: CLEAN" || echo "baseline cmp: DIRTY -- clone copied from SEC below"
  echo "SENTINEL DROPPED (clone-local)"; } > "$SCORES"
cp "$SEC/$F" "$C/$F"

for leg in $LEGS; do
    echo "" >> "$SCORES"; echo "=== LEG $leg ===" >> "$SCORES"
    if [ "$leg" = HEAD ]; then cp "$K/cpu_arm_coproc.HEAD.c" "$C/$F"; rc=0
    else python3 "$K/mut_xscale_t3.py" "$SEC/$F" "$C/$F" "$leg" > /dev/null; rc=$?; fi
    if [ $rc != 0 ]; then echo "  MUTATOR REFUSED rc=$rc -- leg NOT measured" >> "$SCORES"; continue; fi
    ( cd "$C" && rm -f src/cpus/*.o && make -j4 > "$K/build_$leg.log" 2>&1 ); brc=$?
    fresh=STALE; [ "$C/gxemul" -nt "$C/$F" ] && fresh=FRESH
    echo "  build rc=$brc binary=$fresh" >> "$SCORES"
    if [ $brc != 0 ] || [ $fresh != FRESH ]; then echo "  BUILD FAILED -- leg NOT measured (not a kill)" >> "$SCORES"; continue; fi
    timeout 3600 python3 -u "$PROBE" "$C/gxemul" "$leg" "$STUB" > "$K/probe_$leg.raw" 2>&1
    echo "  $(grep -oE 'XSCALE_RESULT=[0-9]+/[0-9]+' "$K/probe_$leg.raw" | tail -1)  $(grep -oE 'XSCALE_CONTROL=[A-Z]+' "$K/probe_$leg.raw" | tail -1)  sentinel=[$(tail -1 "$K/probe_$leg.raw")]" >> "$SCORES"
    echo "  $(grep -E '^FAILING:' "$K/probe_$leg.raw" | tail -1)" >> "$SCORES"
    echo "  $(grep -E '^BLOCKED:' "$K/probe_$leg.raw" | tail -1)" >> "$SCORES"
done

echo "" >> "$SCORES"; echo "=== RESTORE ===" >> "$SCORES"
cp "$SEC/$F" "$C/$F"
( cd "$C" && rm -f src/cpus/*.o && make -j4 > "$K/build_RESTORE.log" 2>&1 )
p1=DIRTY; cmp -s "$C/$F" "$SEC/$F" && p1=CLEAN
p2=STALE; [ "$C/gxemul" -nt "$C/$F" ] && p2=FRESH
echo "  restore cmp-vs-SEC=$p1 binary=$p2" >> "$SCORES"
if [ $p1 = CLEAN ] && [ $p2 = FRESH ]; then rm -f "$C/.MUTANT"; echo "  SENTINEL CLEARED (both parts)" >> "$SCORES"
else echo "  SENTINEL LEFT IN PLACE" >> "$SCORES"; fi
echo KILLTABLE3_DONE >> "$SCORES"
cat "$SCORES"
