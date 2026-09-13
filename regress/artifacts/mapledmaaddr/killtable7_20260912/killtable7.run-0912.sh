#!/bin/bash
#  mapledmaaddr (#528) kill table 7 (TARGETED) -- scratch clone of build/, clone-local sentinel, instruments frozen at
#  launch, baseline NAMED as the current SEC dev_dreamcast_maple.c (the fix).  Logs land in this directory.
#  TWO instruments: FROZEN7 (the full-line / EOF / exit-status probe, copied from regress/ at launch) for every leg, and
#  FROZEN6 (table 6's whole-transcript probe, preserved) for the legs in OLD4, so the final pass's survivors of table 6's oracle are
#  MEASURED against that oracle rather than inferred.
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
K=$SEC/regress/artifacts/mapledmaaddr/killtable7_20260912
PROBE=$K/maple_dmaaddr_probe.FROZEN7.py
PROBEOLD=$K/maple_dmaaddr_probe.FROZEN6.py
IMG=$R/_images/openbsd76-landisk-bsd.rd
C=/tmp/gxmaple7
F=src/devices/dev_dreamcast_maple.c
SCORES=$K/SCORES.txt
LEGS="BASE HEAD M_EXITATQUIT M_ABORTATQUIT M_ABORTAT4 M_SLOWATEXIT4 M_DISASMHOOK M_TICKPERIODIC4 M_ATEXIT M_KEEPFATAL M_EXITONLY M_GLUEPROMPT M_QUITLINE M_HEXDIAG BASE2 BASE3"
OLD4=" BASE M_EXITATQUIT M_ABORTAT4 M_SLOWATEXIT4 M_DISASMHOOK "

cp "$SEC/regress/maple_dmaaddr_probe.py" "$PROBE" || exit 9
rm -rf "$C"; cp -a "$R/build" "$C" || exit 9
echo "$F mapledmaaddr kill table 7 in progress" > "$C/.MUTANT"
{ echo "mapledmaaddr KILL TABLE 7 (targeted)   $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "baseline = SEC $F (the fix)   probe = FROZEN at launch ($(basename $PROBE)), cmp vs regress/: $(cmp -s "$PROBE" "$SEC/regress/maple_dmaaddr_probe.py" && echo IDENTICAL || echo DIFFERS)"
  echo "second instrument = $(basename $PROBEOLD), cmp vs killtable6's frozen copy: $(cmp -s "$PROBEOLD" "$SEC/regress/artifacts/mapledmaaddr/killtable6_20260912/maple_dmaaddr_probe.FROZEN6.py" && echo IDENTICAL || echo DIFFERS)"
  cmp -s "$C/$F" "$SEC/$F" && echo "baseline cmp: CLEAN" || echo "baseline cmp: DIRTY -- clone copied from SEC below"
  echo "SENTINEL DROPPED (clone-local)"; } > "$SCORES"
cp "$SEC/$F" "$C/$F"

for leg in $LEGS; do
    echo "" >> "$SCORES"; echo "=== LEG $leg ===" >> "$SCORES"
    case $leg in
      BASE*) cp "$SEC/$F" "$C/$F"; rc=0 ;;
      HEAD)  cp "$K/dev_dreamcast_maple.HEAD.c" "$C/$F"; rc=0 ;;
      *)     python3 "$K/mut_maple7.py" "$SEC/$F" "$C/$F" "$leg" > "$K/mutate_$leg.txt" 2>&1; rc=$? ;;
    esac
    ch=$(diff "$SEC/$F" "$C/$F" | grep -c '^[<>]')
    echo "  mutate rc=$rc  changed-lines-vs-SEC=$ch" >> "$SCORES"
    if [ $rc != 0 ]; then echo "  MUTATOR REFUSED -- leg NOT measured" >> "$SCORES"; continue; fi
    case $leg in BASE*) ;; *) if [ "$ch" = 0 ]; then echo "  MUTANT IDENTICAL TO BASE -- leg NOT measured" >> "$SCORES"; continue; fi ;; esac
    ( cd "$C" && rm -f src/devices/dev_dreamcast_maple.o && make -j4 > "$K/build_$leg.log" 2>&1 ); brc=$?
    fresh=STALE; [ "$C/gxemul" -nt "$C/$F" ] && fresh=FRESH
    echo "  build rc=$brc binary=$fresh" >> "$SCORES"
    if [ $brc != 0 ] || [ $fresh != FRESH ]; then echo "  BUILD FAILED -- leg NOT measured (not a kill)" >> "$SCORES"; continue; fi
    timeout 1200 python3 -u "$PROBE" "$C/gxemul" "$IMG" "$leg" > "$K/probe_$leg.raw" 2>&1
    echo "  FROZEN7 $(grep -oE 'MAPLE_DMAADDR_RESULT=[0-9]+/[0-9]+' "$K/probe_$leg.raw" | tail -1)  $(grep -oE 'MAPLE_DMAADDR_CONTROL=[A-Z]+' "$K/probe_$leg.raw" | tail -1)  sentinel=[$(tail -1 "$K/probe_$leg.raw")]" >> "$SCORES"
    echo "    $(grep -E '^FAILING:' "$K/probe_$leg.raw" | tail -1)" >> "$SCORES"
    case "$OLD4" in *" $leg "*)
        timeout 1200 python3 -u "$PROBEOLD" "$C/gxemul" "$IMG" "$leg" > "$K/probe6_$leg.raw" 2>&1
        echo "  FROZEN6 $(grep -oE 'MAPLE_DMAADDR_RESULT=[0-9]+/[0-9]+' "$K/probe6_$leg.raw" | tail -1)  $(grep -oE 'MAPLE_DMAADDR_CONTROL=[A-Z]+' "$K/probe6_$leg.raw" | tail -1)  sentinel=[$(tail -1 "$K/probe6_$leg.raw")]" >> "$SCORES"
        echo "    $(grep -E '^FAILING:' "$K/probe6_$leg.raw" | tail -1)" >> "$SCORES" ;;
    esac
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
