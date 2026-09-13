#!/bin/bash
#  mapledmaaddr (#528) kill table 3 -- scratch clone of build/, clone-local sentinel, instrument frozen at launch,
#  baseline NAMED as the current SEC dev_dreamcast_maple.c (the fix).  Logs land in this directory.
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
K=$SEC/regress/artifacts/mapledmaaddr/killtable3_20260912
PROBE=$K/maple_dmaaddr_probe.FROZEN3.py
IMG=$R/_images/openbsd76-landisk-bsd.rd
C=/tmp/gxmaple3
F=src/devices/dev_dreamcast_maple.c
SCORES=$K/SCORES.txt
LEGS="BASE HEAD M_KEEPFATAL M_REWORD M_LATCHED M_TOKENFREE M_EXITONLY M_RET0 M_DECLINE M_HOIST M_READCLEAR M_EQ4 M_BIT30 M_ZEROEXIT M_MASKLOW M_ALIAS08 M_ALIAS20 M_ALIAS40 M_AND4 M_LEN M_ALIGNDECLINE M_ENDECLINE M_ALIGNEXIT M_ENEXIT M_THIRDREAD M_ALIAS01 M_ALIAS02 M_CASE00 M_HEXDIAG M_JOINTDECLINE M_SIBLING M_LEN1"

cp "$SEC/regress/maple_dmaaddr_probe.py" "$PROBE" || exit 9
rm -rf "$C"; cp -a "$R/build" "$C" || exit 9
echo "$F mapledmaaddr kill table 3 in progress" > "$C/.MUTANT"
{ echo "mapledmaaddr KILL TABLE 3   $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "baseline = SEC $F (the fix)   probe = FROZEN at launch ($(basename $PROBE)), cmp vs regress/: $(cmp -s "$PROBE" "$SEC/regress/maple_dmaaddr_probe.py" && echo IDENTICAL || echo DIFFERS)"
  cmp -s "$C/$F" "$SEC/$F" && echo "baseline cmp: CLEAN" || echo "baseline cmp: DIRTY -- clone copied from SEC below"
  echo "SENTINEL DROPPED (clone-local)"; } > "$SCORES"
cp "$SEC/$F" "$C/$F"

for leg in $LEGS; do
    echo "" >> "$SCORES"; echo "=== LEG $leg ===" >> "$SCORES"
    case $leg in
      BASE) cp "$SEC/$F" "$C/$F"; rc=0 ;;
      HEAD) cp "$K/dev_dreamcast_maple.HEAD.c" "$C/$F"; rc=0 ;;
      *)    python3 "$K/mut_maple3.py" "$SEC/$F" "$C/$F" "$leg" > "$K/mutate_$leg.txt" 2>&1; rc=$? ;;
    esac
    ch=$(diff "$SEC/$F" "$C/$F" | grep -c '^[<>]')
    echo "  mutate rc=$rc  changed-lines-vs-SEC=$ch" >> "$SCORES"
    if [ $rc != 0 ]; then echo "  MUTATOR REFUSED -- leg NOT measured" >> "$SCORES"; continue; fi
    if [ "$leg" != BASE ] && [ "$ch" = 0 ]; then echo "  MUTANT IDENTICAL TO BASE -- leg NOT measured" >> "$SCORES"; continue; fi
    ( cd "$C" && rm -f src/devices/dev_dreamcast_maple.o && make -j4 > "$K/build_$leg.log" 2>&1 ); brc=$?
    fresh=STALE; [ "$C/gxemul" -nt "$C/$F" ] && fresh=FRESH
    echo "  build rc=$brc binary=$fresh" >> "$SCORES"
    if [ $brc != 0 ] || [ $fresh != FRESH ]; then echo "  BUILD FAILED -- leg NOT measured (not a kill)" >> "$SCORES"; continue; fi
    timeout 1200 python3 -u "$PROBE" "$C/gxemul" "$IMG" "$leg" > "$K/probe_$leg.raw" 2>&1
    echo "  $(grep -oE 'MAPLE_DMAADDR_RESULT=[0-9]+/[0-9]+' "$K/probe_$leg.raw" | tail -1)  $(grep -oE 'MAPLE_DMAADDR_CONTROL=[A-Z]+' "$K/probe_$leg.raw" | tail -1)  sentinel=[$(tail -1 "$K/probe_$leg.raw")]" >> "$SCORES"
    echo "    $(grep -E '^FAILING:' "$K/probe_$leg.raw" | tail -1)" >> "$SCORES"
done

echo "" >> "$SCORES"; echo "=== RESTORE ===" >> "$SCORES"
cp "$SEC/$F" "$C/$F"
( cd "$C" && rm -f src/devices/dev_dreamcast_maple.o && make -j4 > "$K/build_RESTORE.log" 2>&1 )
p1=DIRTY; cmp -s "$C/$F" "$SEC/$F" && p1=CLEAN
p2=STALE; [ "$C/gxemul" -nt "$C/$F" ] && p2=FRESH
echo "  restore cmp-vs-SEC=$p1 binary=$p2" >> "$SCORES"
if [ $p1 = CLEAN ] && [ $p2 = FRESH ]; then rm -f "$C/.MUTANT"; echo "  SENTINEL CLEARED (both parts)" >> "$SCORES"
else echo "  SENTINEL LEFT IN PLACE" >> "$SCORES"; fi
echo KILLTABLE_DONE >> "$SCORES"
