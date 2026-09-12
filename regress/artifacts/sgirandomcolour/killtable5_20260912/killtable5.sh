#!/bin/bash
#  #519 kill table 5 -- in a SCRATCH CLONE of build/ (the default per owner decision 2026-08-28).
#  Baseline NAMED: the post-fix working set (SEC dev_sgi_re.c).  Clone-local sentinel.  One frozen
#  instrument for every leg.  Every log is written here, beside the PRETABLE, before any record cites it.
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
K=$SEC/regress/artifacts/sgirandomcolour/killtable5_20260912
PROBE=$SEC/regress/artifacts/sgirandomcolour/base_20260912/sgi_re_colourdefault_probe.py.frozen
C=/tmp/gx519k5
F=src/devices/dev_sgi_re.c
SCORES=$K/SCORES.txt
LEGS="BASE HEAD FIRST_A2_ZERO FIRST_A8_ZERO FIRST_B2_ZERO FIRST_B4_ZERO FIRST_B8_ZERO FIRST_C2_ZERO FIRST_C4_ZERO FIRST_C8_ZERO FIRST_L2_ZERO FIRST_L8_ZERO REPEAT_L1_ZERO NIB_OTHER_ZERO TAIL8_ZERO"

rm -rf "$C"; cp -a "$R/build" "$C" || exit 9
echo "$F kill table 5 in progress" > "$C/.MUTANT"
{ echo "#519 KILL TABLE 5   $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "baseline = SEC $F (post-fix working set)   probe = FROZEN ($(basename $PROBE))"
  cmp -s "$C/$F" "$SEC/$F" && echo "baseline cmp: CLEAN" || echo "baseline cmp: DIRTY -- clone copied from SEC below"
  echo "SENTINEL DROPPED (clone-local)"; } > "$SCORES"
cp "$SEC/$F" "$C/$F"

for leg in $LEGS; do
    echo "" >> "$SCORES"; echo "=== LEG $leg ===" >> "$SCORES"
    if [ "$leg" = HEAD ]; then cp "$K/dev_sgi_re.HEAD.c" "$C/$F"; rc=0
    else python3 "$K/mutate519k5.py" "$SEC/$F" "$C/$F" "$leg" > /dev/null; rc=$?; fi
    if [ $rc != 0 ]; then echo "  MUTATOR REFUSED rc=$rc -- leg NOT measured" >> "$SCORES"; continue; fi
    ( cd "$C" && rm -f src/devices/dev_sgi_re.o && make -j4 > "$K/build_$leg.log" 2>&1 ); brc=$?
    fresh=STALE; [ "$C/gxemul" -nt "$C/$F" ] && fresh=FRESH
    echo "  build rc=$brc binary=$fresh" >> "$SCORES"
    if [ $brc != 0 ] || [ $fresh != FRESH ]; then echo "  BUILD FAILED -- leg NOT measured (not a kill)" >> "$SCORES"; continue; fi
    timeout 3600 python3 -u "$PROBE" "$C/gxemul" "$leg" > "$K/probe_$leg.raw" 2>&1
    echo "  $(grep -oE 'SGICOLOUR_RESULT=[0-9]+/[0-9]+' "$K/probe_$leg.raw" | tail -1)  sentinel=[$(tail -1 "$K/probe_$leg.raw")]" >> "$SCORES"
    echo "  FAILING: $(grep -E ' FAIL$' "$K/probe_$leg.raw" | cut -c1-16 | sed 's/ *$//' | paste -sd, -)" >> "$SCORES"
done

echo "" >> "$SCORES"; echo "=== RESTORE ===" >> "$SCORES"
cp "$SEC/$F" "$C/$F"
( cd "$C" && rm -f src/devices/dev_sgi_re.o && make -j4 > "$K/build_RESTORE.log" 2>&1 )
p1=DIRTY; cmp -s "$C/$F" "$SEC/$F" && p1=CLEAN
p2=STALE; [ "$C/gxemul" -nt "$C/$F" ] && p2=FRESH
echo "  restore cmp-vs-SEC=$p1 binary=$p2" >> "$SCORES"
if [ $p1 = CLEAN ] && [ $p2 = FRESH ]; then rm -f "$C/.MUTANT"; echo "  SENTINEL CLEARED (both parts)" >> "$SCORES"
else echo "  SENTINEL LEFT IN PLACE" >> "$SCORES"; fi
echo KILLTABLE5_DONE >> "$SCORES"
cat "$SCORES"
