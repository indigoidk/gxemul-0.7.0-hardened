#!/bin/bash
#  Opus pass-2 DISCRIMINATOR table: same clone, same mutator; runs discrim_opus2.py (the cells the 16 rows never
#  build) against BASE and every leg, to show a 16/16 survivor is NOT equivalent to the fix.
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
K=$SEC/regress/artifacts/mapledmaaddr/opus_pass2_20260912
PROBE=$K/discrim_opus2.FROZEN.py
IMG=$R/_images/openbsd76-landisk-bsd.rd
C=/tmp/gxopus_maple2
F=src/devices/dev_dreamcast_maple.c
OUT=$K/DISCRIM.txt
LEGS="BASE M_ALIGNDECLINE M_ENDECLINE M_ALIGNEXIT M_ENEXIT M_NOPREFIX M_LENEXIT M_THIRDREAD"
cp "$K/discrim_opus2.py" "$PROBE" || exit 9
echo "$F opus pass-2 discriminator in progress" > "$C/.MUTANT"
echo "mapledmaaddr OPUS PASS-2 DISCRIMINATOR   $(date -u +%Y-%m-%dT%H:%M:%SZ)  SENTINEL DROPPED" > "$OUT"
for leg in $LEGS; do
    echo "" >> "$OUT"; echo "=== LEG $leg ===" >> "$OUT"
    case $leg in
      BASE) cp "$SEC/$F" "$C/$F"; rc=0 ;;
      *)    python3 "$K/mut_opus2.py" "$SEC/$F" "$C/$F" "$leg" > /dev/null 2>&1; rc=$? ;;
    esac
    [ $rc != 0 ] && { echo "  MUTATOR REFUSED" >> "$OUT"; continue; }
    ( cd "$C" && rm -f src/devices/dev_dreamcast_maple.o && make -j4 > "$K/dbuild_$leg.log" 2>&1 ); brc=$?
    fresh=STALE; [ "$C/gxemul" -nt "$C/$F" ] && fresh=FRESH
    echo "  build rc=$brc binary=$fresh" >> "$OUT"
    if [ $brc != 0 ] || [ $fresh != FRESH ]; then echo "  BUILD FAILED" >> "$OUT"; continue; fi
    timeout 1200 python3 -u "$PROBE" "$C/gxemul" "$IMG" "$leg" > "$K/discrim_$leg.raw" 2>&1
    echo "  $(grep -oE 'DISCRIM_RESULT=[0-9]+/[0-9]+' "$K/discrim_$leg.raw" | tail -1)  sentinel=[$(tail -1 "$K/discrim_$leg.raw")]" >> "$OUT"
    echo "    $(grep -E '^FAILING:' "$K/discrim_$leg.raw" | tail -1)" >> "$OUT"
done
echo "" >> "$OUT"; echo "=== RESTORE ===" >> "$OUT"
cp "$SEC/$F" "$C/$F"
( cd "$C" && rm -f src/devices/dev_dreamcast_maple.o && make -j4 > "$K/dbuild_RESTORE.log" 2>&1 )
p1=DIRTY; cmp -s "$C/$F" "$SEC/$F" && p1=CLEAN
p2=STALE; [ "$C/gxemul" -nt "$C/$F" ] && p2=FRESH
echo "  restore cmp-vs-SEC=$p1 binary=$p2" >> "$OUT"
if [ $p1 = CLEAN ] && [ $p2 = FRESH ]; then rm -f "$C/.MUTANT"; echo "  SENTINEL CLEARED (both parts)" >> "$OUT"
else echo "  SENTINEL LEFT IN PLACE" >> "$OUT"; fi
echo DISCRIM_TABLE_DONE >> "$OUT"
