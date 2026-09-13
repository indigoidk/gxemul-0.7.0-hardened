#!/bin/bash
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
A=$SEC/regress/artifacts/mapledmaaddr/opus_final_20260912
SDW=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
IMG=$R/_images/openbsd76-landisk-bsd.rd
C=/tmp/gxopus528f
F=src/devices/dev_dreamcast_maple.c
PROBE=$A/maple_dmaaddr_probe.FROZEN3.py
PREP=$A/maple_dmaaddr_probe.REPAIR_HOW.FROZEN3.py
S=$A/SCORES3.txt
LEGS="BASE M_EXITATQUIT M_ABORTATQUIT M_EXITATQUIT0 M_TICKDEFER3 M_TICKPERIODIC4"
cp "$SEC/regress/maple_dmaaddr_probe.py" "$PROBE" || exit 9
cp "$A/maple_dmaaddr_probe.REPAIR_HOW.py" "$PREP" || exit 9
rm -rf "$C"; cp -a "$R/build" "$C" || exit 9
echo "$F opus_final run3 in progress" > "$C/.MUTANT"
{ echo "mapledmaaddr OPUS FINAL kill table RUN 3 (deferred abnormal end) $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "probe FROZEN3 cmp vs regress/: $(cmp -s "$PROBE" "$SEC/regress/maple_dmaaddr_probe.py" && echo IDENTICAL || echo DIFFERS)"
  echo "repair probe = REPAIR_HOW (diff: REPAIR_HOW.diff, one statement in the read-silent row)"
  cmp -s "$C/$F" "$SEC/$F" && echo "clone baseline cmp: CLEAN" || echo "clone baseline cmp: DIRTY"
  echo "SENTINEL DROPPED (clone-local)"; } > "$S"
for leg in $LEGS; do
  echo "" >> "$S"; echo "=== LEG $leg ===" >> "$S"
  case $leg in
    BASE) cp "$SEC/$F" "$C/$F"; rc=0 ;;
    *)    python3 "$A/mut_final3.py" "$SEC/$F" "$C/$F" "$leg" > "$A/mutate3_$leg.txt" 2>&1; rc=$? ;;
  esac
  ch=$(diff "$SEC/$F" "$C/$F" | grep -c '^[<>]')
  echo "  mutate rc=$rc changed-lines-vs-SEC=$ch" >> "$S"
  [ $rc != 0 ] && { echo "  MUTATOR REFUSED" >> "$S"; continue; }
  ( cd "$C" && rm -f src/devices/dev_dreamcast_maple.o && make -j4 > "$A/build3_$leg.log" 2>&1 ); brc=$?
  fresh=STALE; [ "$C/gxemul" -nt "$C/$F" ] && fresh=FRESH
  echo "  build rc=$brc binary=$fresh" >> "$S"
  if [ $brc != 0 ] || [ $fresh != FRESH ]; then echo "  BUILD FAILED -- not measured" >> "$S"; continue; fi
  INSTS="SHIPPED REPAIR"; case $leg in M_TICK*) INSTS=SHIPPED ;; esac
  for inst in $INSTS; do
    P=$PROBE; [ $inst = REPAIR ] && P=$PREP
    timeout 540 python3 -u "$P" "$C/gxemul" "$IMG" "$leg" > "$A/probe3_${inst}_$leg.raw" 2>&1
    echo "  $inst $(grep -oE 'MAPLE_DMAADDR_RESULT=[0-9]+/[0-9]+' "$A/probe3_${inst}_$leg.raw" | tail -1)  $(grep -oE 'MAPLE_DMAADDR_CONTROL=[A-Z]+' "$A/probe3_${inst}_$leg.raw" | tail -1)  sentinel=[$(tail -1 "$A/probe3_${inst}_$leg.raw")]" >> "$S"
    echo "    $(grep -E '^FAILING:' "$A/probe3_${inst}_$leg.raw" | tail -1)   $(grep -E '^exit status' "$A/probe3_${inst}_$leg.raw" | awk '{print "exit-status-row got="$3}')" >> "$S"
  done
  case $leg in BASE|M_TICK*) timeout 60 python3 -u "$A/noneq_tick.py" "$C/gxemul" "$IMG" > "$A/noneq3_$leg.txt" 2>&1
    echo "    noneq: $(grep -E '^IN_' "$A/noneq3_$leg.txt" | tr '
' ' ') [$(tail -1 "$A/noneq3_$leg.txt")]" >> "$S" ;; esac
done
echo "" >> "$S"; echo "=== RESTORE ===" >> "$S"
cp "$SEC/$F" "$C/$F"
( cd "$C" && rm -f src/devices/dev_dreamcast_maple.o && make -j4 > "$A/build3_RESTORE.log" 2>&1 )
p1=DIRTY; cmp -s "$C/$F" "$SEC/$F" && p1=CLEAN
p2=STALE; [ "$C/gxemul" -nt "$C/$F" ] && p2=FRESH
echo "  restore cmp-vs-SEC=$p1 binary=$p2" >> "$S"
if [ $p1 = CLEAN ] && [ $p2 = FRESH ]; then rm -f "$C/.MUTANT"; echo "  SENTINEL CLEARED (both parts)" >> "$S"; else echo "  SENTINEL LEFT IN PLACE" >> "$S"; fi
echo OPUS_FINAL3_DONE >> "$S"
