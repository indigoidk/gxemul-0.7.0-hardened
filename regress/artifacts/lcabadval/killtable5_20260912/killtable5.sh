#!/bin/bash
#  #518 kill table 5 -- scratch clone of build/, clone-local sentinel, one frozen instrument,
#  baseline NAMED as the current SEC dev_lca.c.  Logs land here before any record cites them.
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
K=$SEC/regress/artifacts/lcabadval/killtable5_20260912
PROBE=$SEC/regress/artifacts/lcabadval/base_20260912/lca_badval_probe.py.frozen
C=/tmp/gx518k5
F=src/devices/dev_lca.c
SCORES=$K/SCORES.txt
LEGS="BASE HEAD M43_mask1_widen M44_mask1_idata M47_base1_widen M_RULE2 M_STORE01 M_CONF_B4 M_TBENA_B8"

rm -rf "$C"; cp -a "$R/build" "$C" || exit 9
echo "$F #518 kill table 5 in progress" > "$C/.MUTANT"
{ echo "#518 KILL TABLE 5   $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "baseline = SEC $F (post-fix working set)   probe = FROZEN 75-row ($(basename $PROBE))"
  cmp -s "$C/$F" "$SEC/$F" && echo "baseline cmp: CLEAN" || echo "baseline cmp: DIRTY -- clone copied from SEC below"
  echo "SENTINEL DROPPED (clone-local)"; } > "$SCORES"
cp "$SEC/$F" "$C/$F"

for leg in $LEGS; do
    echo "" >> "$SCORES"; echo "=== LEG $leg ===" >> "$SCORES"
    if [ "$leg" = HEAD ]; then cp "$K/dev_lca.HEAD.c" "$C/$F"; rc=0
    else python3 "$K/mut518t5.py" "$SEC/$F" "$C/$F" "$leg" > /dev/null; rc=$?; fi
    if [ $rc != 0 ]; then echo "  MUTATOR REFUSED rc=$rc -- leg NOT measured" >> "$SCORES"; continue; fi
    ( cd "$C" && rm -f src/devices/dev_lca.o && make -j4 > "$K/build_$leg.log" 2>&1 ); brc=$?
    fresh=STALE; [ "$C/gxemul" -nt "$C/$F" ] && fresh=FRESH
    echo "  build rc=$brc binary=$fresh" >> "$SCORES"
    if [ $brc != 0 ] || [ $fresh != FRESH ]; then echo "  BUILD FAILED -- leg NOT measured (not a kill)" >> "$SCORES"; continue; fi
    timeout 3600 python3 -u "$PROBE" "$C/gxemul" "$leg" > "$K/probe_$leg.raw" 2>&1
    echo "  $(grep -oE 'LCABADVAL_RESULT=[0-9]+/[0-9]+' "$K/probe_$leg.raw" | tail -1)  sentinel=[$(tail -1 "$K/probe_$leg.raw")]" >> "$SCORES"
    echo "  FAILING: $(grep -E ' FAIL$' "$K/probe_$leg.raw" | cut -c1-40 | sed 's/  */ /g' | paste -sd'|' -)" >> "$SCORES"
done

echo "" >> "$SCORES"; echo "=== RESTORE ===" >> "$SCORES"
cp "$SEC/$F" "$C/$F"
( cd "$C" && rm -f src/devices/dev_lca.o && make -j4 > "$K/build_RESTORE.log" 2>&1 )
p1=DIRTY; cmp -s "$C/$F" "$SEC/$F" && p1=CLEAN
p2=STALE; [ "$C/gxemul" -nt "$C/$F" ] && p2=FRESH
echo "  restore cmp-vs-SEC=$p1 binary=$p2" >> "$SCORES"
if [ $p1 = CLEAN ] && [ $p2 = FRESH ]; then rm -f "$C/.MUTANT"; echo "  SENTINEL CLEARED (both parts)" >> "$SCORES"
else echo "  SENTINEL LEFT IN PLACE" >> "$SCORES"; fi
echo KILLTABLE5_DONE >> "$SCORES"
cat "$SCORES"
