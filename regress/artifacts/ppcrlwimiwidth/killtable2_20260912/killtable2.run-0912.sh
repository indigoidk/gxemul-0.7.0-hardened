#!/bin/bash
#  PowerPC rlwimi + rldimi JOINT kill table 2 -- the PROMOTED detectors.  Scratch clone of build/,
#  clone-local sentinel, frozen instruments, baseline NAMED as the current SEC cpu_ppc_instr.c.  Each leg
#  is ONE build; BOTH probes run against it (the cross-check).  Logs land in this directory.
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
A=$SEC/regress/artifacts
K=$A/ppcrlwimiwidth/killtable2_20260912
PW=$A/ppcrlwimiwidth/base_20260912/ppc_rlwimi_probe.py.frozen
PD=$A/ppcrldimimask/base_20260912/ppc_rldimi_probe.py.frozen
MR=$K/mut_rlwimi_t2.py
MD=$A/ppcrldimimask/killtable_20260911/mutate_rldimi.py
MDN=$A/ppcrldimimask/killtable_nullmedium_20260911/mutate_rldimi.py
C=/tmp/gxppc2
F=src/cpus/cpu_ppc_instr.c
HEADF=$K/cpu_ppc_instr.HEAD.c
SCORES=$K/SCORES.txt
LEGS="BASE HEAD R_REV_COND R_ONLY_CAST R_ONLY_HIGH R_POST_LOOP R_ORIG R_NULL D_MUT63 D_NOCIRC D_NOKEEP_SH D_NOWRAP D_NO_MERGE D_ORIG D_NULL"

rm -rf "$C"; cp -a "$R/build" "$C" || exit 9
echo "$F PPC joint kill table 2 in progress" > "$C/.MUTANT"
{ echo "PPC rlwimi+rldimi JOINT KILL TABLE 2   $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "baseline = SEC $F   instruments = FROZEN rlwimi 28-row + rldimi 27-row"
  cmp -s "$C/$F" "$SEC/$F" && echo "baseline cmp: CLEAN" || echo "baseline cmp: DIRTY -- clone copied from SEC below"
  echo "SENTINEL DROPPED (clone-local)"; } > "$SCORES"
cp "$SEC/$F" "$C/$F"

for leg in $LEGS; do
    echo "" >> "$SCORES"; echo "=== LEG $leg ===" >> "$SCORES"
    case $leg in
      BASE) cp "$SEC/$F" "$C/$F"; rc=0 ;;
      HEAD) cp "$HEADF" "$C/$F"; rc=0 ;;
      R_*)  python3 "$MR" "$SEC/$F" "$C/$F" "${leg#R_}" > "$K/mutate_$leg.txt" 2>&1; rc=$?
            [ "$leg" = R_NULL ] && { python3 "$MR" "$SEC/$F" "$C/$F" NULL_MEDIUM > "$K/mutate_$leg.txt" 2>&1; rc=$?; } ;;
      D_NULL) cp "$SEC/$F" "$C/$F"; python3 "$MDN" NULL_MEDIUM "$C/$F" "$SEC/$F" "$HEADF" > "$K/mutate_$leg.txt" 2>&1; rc=$? ;;
      D_*)  cp "$SEC/$F" "$C/$F"; python3 "$MD" "M_${leg#D_}" "$C/$F" "$SEC/$F" "$HEADF" > "$K/mutate_$leg.txt" 2>&1; rc=$? ;;
    esac
    ch=$(diff "$SEC/$F" "$C/$F" | grep -c '^[<>]')
    echo "  mutate rc=$rc  changed-lines-vs-SEC=$ch" >> "$SCORES"
    if [ $rc != 0 ]; then echo "  MUTATOR REFUSED -- leg NOT measured" >> "$SCORES"; continue; fi
    if [ "$leg" != BASE ] && [ "$ch" = 0 ]; then echo "  MUTANT IDENTICAL TO BASE -- leg NOT measured" >> "$SCORES"; continue; fi
    ( cd "$C" && rm -f src/cpus/*.o && make -j4 > "$K/build_$leg.log" 2>&1 ); brc=$?
    fresh=STALE; [ "$C/gxemul" -nt "$C/$F" ] && fresh=FRESH
    echo "  build rc=$brc binary=$fresh" >> "$SCORES"
    if [ $brc != 0 ] || [ $fresh != FRESH ]; then echo "  BUILD FAILED -- leg NOT measured (not a kill)" >> "$SCORES"; continue; fi
    timeout 1200 python3 -u "$PW" "$C/gxemul" "$leg" > "$K/probe_rlwimi_$leg.raw" 2>&1
    timeout 1200 python3 -u "$PD" "$C/gxemul" "$leg" > "$K/probe_rldimi_$leg.raw" 2>&1
    for p in rlwimi rldimi; do
        P=$(echo $p | tr a-z A-Z)
        echo "  $p: $(grep -oE "PPC_${P}_RESULT=[0-9]+/[0-9]+" "$K/probe_${p}_$leg.raw" | tail -1)  $(grep -oE "PPC_${P}_CONTROL=[A-Z]+" "$K/probe_${p}_$leg.raw" | tail -1)  sentinel=[$(tail -1 "$K/probe_${p}_$leg.raw")]" >> "$SCORES"
        echo "    $(grep -E '^FAILING:' "$K/probe_${p}_$leg.raw" | tail -1)" >> "$SCORES"
    done
done

echo "" >> "$SCORES"; echo "=== RESTORE ===" >> "$SCORES"
cp "$SEC/$F" "$C/$F"
( cd "$C" && rm -f src/cpus/*.o && make -j4 > "$K/build_RESTORE.log" 2>&1 )
p1=DIRTY; cmp -s "$C/$F" "$SEC/$F" && p1=CLEAN
p2=STALE; [ "$C/gxemul" -nt "$C/$F" ] && p2=FRESH
echo "  restore cmp-vs-SEC=$p1 binary=$p2" >> "$SCORES"
if [ $p1 = CLEAN ] && [ $p2 = FRESH ]; then rm -f "$C/.MUTANT"; echo "  SENTINEL CLEARED (both parts)" >> "$SCORES"
else echo "  SENTINEL LEFT IN PLACE" >> "$SCORES"; fi
echo KILLTABLE2_DONE >> "$SCORES"
cat "$SCORES"
