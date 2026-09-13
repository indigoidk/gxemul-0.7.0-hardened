#!/bin/bash
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
A=$SEC/regress/artifacts/mapledmaaddr/opus_final_20260912
SDW=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
IMG=$R/_images/openbsd76-landisk-bsd.rd
C=/tmp/gxopus528f
F=src/devices/dev_dreamcast_maple.c
PROBE=$A/maple_dmaaddr_probe.FROZEN.py
S=$A/SCORES.txt
LEGS="BASE M_STDERR M_FILE M_ATEXITPRINTF M_TICKDEFER M_TICKDEFER2"

cp "$SEC/regress/maple_dmaaddr_probe.py" "$PROBE" || exit 9
rm -rf "$C"; cp -a "$R/build" "$C" || exit 9
echo "$F opus_final in progress" > "$C/.MUTANT"
{ echo "mapledmaaddr OPUS FINAL kill table RUN 2 $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "probe FROZEN cmp vs regress/: $(cmp -s "$PROBE" "$SEC/regress/maple_dmaaddr_probe.py" && echo IDENTICAL || echo DIFFERS)"
  cmp -s "$C/$F" "$SEC/$F" && echo "clone baseline cmp: CLEAN" || echo "clone baseline cmp: DIRTY"
  echo "SENTINEL DROPPED (clone-local)"; } > "$S"
cp "$SEC/$F" "$C/$F"

for leg in $LEGS; do
  echo "" >> "$S"; echo "=== LEG $leg ===" >> "$S"
  case $leg in
    BASE) cp "$SEC/$F" "$C/$F"; rc=0 ;;
    *)    python3 "$SDW/mut_final2.py" "$SEC/$F" "$C/$F" "$leg" > "$A/mutate_$leg.txt" 2>&1; rc=$? ;;
  esac
  ch=$(diff "$SEC/$F" "$C/$F" | grep -c '^[<>]')
  echo "  mutate rc=$rc changed-lines-vs-SEC=$ch" >> "$S"
  [ $rc != 0 ] && { echo "  MUTATOR REFUSED" >> "$S"; continue; }
  ( cd "$C" && rm -f src/devices/dev_dreamcast_maple.o && make -j4 > "$A/build_$leg.log" 2>&1 ); brc=$?
  fresh=STALE; [ "$C/gxemul" -nt "$C/$F" ] && fresh=FRESH
  echo "  build rc=$brc binary=$fresh" >> "$S"
  [ $brc != 0 ] || [ $fresh != FRESH ] && { echo "  BUILD FAILED -- not measured" >> "$S"; continue; }
  rm -f /tmp/maple_leak_final
  timeout 540 python3 -u "$PROBE" "$C/gxemul" "$IMG" "$leg" > "$A/probe_$leg.raw" 2>&1
  echo "  $(grep -oE 'MAPLE_DMAADDR_RESULT=[0-9]+/[0-9]+' "$A/probe_$leg.raw" | tail -1)  $(grep -oE 'MAPLE_DMAADDR_CONTROL=[A-Z]+' "$A/probe_$leg.raw" | tail -1)  sentinel=[$(tail -1 "$A/probe_$leg.raw")]" >> "$S"
  echo "    $(grep -E '^FAILING:' "$A/probe_$leg.raw" | tail -1)" >> "$S"
  case $leg in BASE|M_TICK*) timeout 60 python3 -u "$A/noneq_tick.py" "$C/gxemul" "$IMG" > "$A/noneq_$leg.txt" 2>&1;
    echo "    noneq: $(grep -E '^IN_' "$A/noneq_$leg.txt" | tr '
' ' ') [$(tail -1 "$A/noneq_$leg.txt")]" >> "$S" ;; esac
  [ -f /tmp/maple_leak_final ] && echo "    off-channel file /tmp/maple_leak_final EXISTS ($(wc -l < /tmp/maple_leak_final) lines) -- output left the console" >> "$S"
done

echo "" >> "$S"; echo "=== RESTORE ===" >> "$S"
cp "$SEC/$F" "$C/$F"
( cd "$C" && rm -f src/devices/dev_dreamcast_maple.o && make -j4 > "$A/build_RESTORE.log" 2>&1 )
p1=DIRTY; cmp -s "$C/$F" "$SEC/$F" && p1=CLEAN
p2=STALE; [ "$C/gxemul" -nt "$C/$F" ] && p2=FRESH
echo "  restore cmp-vs-SEC=$p1 binary=$p2" >> "$S"
[ $p1 = CLEAN ] && [ $p2 = FRESH ] && { rm -f "$C/.MUTANT"; echo "  SENTINEL CLEARED (both parts)" >> "$S"; } || echo "  SENTINEL LEFT IN PLACE" >> "$S"
echo OPUS_FINAL_DONE >> "$S"
