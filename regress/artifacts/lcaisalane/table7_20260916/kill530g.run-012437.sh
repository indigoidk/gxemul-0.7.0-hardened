#!/bin/bash
# kill530g.sh -- #530 KILL TABLE 7: closing pass 5's REPAIR 6 (the forward-COUNT CHANNEL repair, 352 rows).
#
#   Eighteen legs -- base + the seventeen mutants spanning the eight-cell product
#   {write arm, read arm} x {DROP, SWAP, DUPLICATE, ADD-OTHER} -- against the REPAIRED 352-row instrument.
#   PRETABLE.out beside this file was written FIRST and its mtime proves the order.
#
#   *** LAUNCH FROM A FROZEN COPY (cp kill530g.sh kill530g.run-<stamp>.sh) AND WITH run_in_background. ***
#   Bash reads a script incrementally, so editing this file while it runs corrupts the run.
#
#   *** EXPECT ~4-6 HOURS.  A 352-row leg is ~32 min (the c5 seat measured 19 min for 185 rows and 13 for 150),
#   nine legs per lane, TWO probe lanes -- the c5 seat's own recorded constraint ("never more than two probe
#   lanes").  A long run is not a hang; check the lane files' mtimes, not the wall clock. ***
#
#   SCRATCH CLONE /tmp/gxopus530c5 ONLY.  No project tree is written except this artifacts directory.
#   THREE source files are mutated across the leg set and ALL THREE are restored and cleared together.
set -u
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/lcaisalane
A=$D/table7_20260916
C5=$D/opus_c5_20260915
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus530c5
B=/tmp/gxopus530c5_bins
F1=src/devices/dev_lca.c
F2=src/devices/dev_pckbc.c
F3=src/devices/dev_8253.c
PROBE=$A/lca_isalane_probe.table7.py
M_A=$A/mut530c5.frozen.py
M_B=$A/mut530c5b.frozen.py
M_C=$A/mut530c5c.frozen.py
M_D=$A/mut530c5d.frozen.py

LIST="base RD2z WWtail WWall dNZtail W23 RWtail nox WW6 RD2post cdxZL3 Wpure RWall noff Wdrop WXR RXW Rdrop"

mkdir -p "$A/logs" "$A/builds" "$A/mutants" "$B"

#  ---- freeze the instrument and the four mutators, and PROVE the probe is the shipped one ----
cp "$SEC/regress/lca_isalane_probe.py" "$PROBE"
cp "$C5/instrument/mut530c5.frozen.py"   "$M_A"
cp "$C5/instrument/mut530c5b.frozen.py"  "$M_B"
cp "$C5/instrument2/mut530c5c.frozen.py" "$M_C"
cp "$C5/instrument2/mut530c5d.frozen.py" "$M_D"
md5sum "$PROBE" "$M_A" "$M_B" "$M_C" "$M_D" "$SEC/$F1" "$SEC/$F2" "$SEC/$F3" | tee "$A/logs/INSTRUMENT.md5"
cmp -s "$PROBE" "$SEC/regress/lca_isalane_probe.py" \
    && echo "PROBE frozen == shipped" || { echo "PROBE mismatch -- abort"; exit 1; }

#  ---- the leg -> mutator map, DERIVED from each mutator's own `list' action and asserted here ----
mutof() {
    case "$1" in
        base|RD2z|WWtail|WWall|dNZtail|W23|RWtail|nox) echo "$M_A";;
        WW6|RD2post|cdxZL3|Wpure)                      echo "$M_B";;
        RWall|noff)                                    echo "$M_C";;
        Wdrop|WXR|RXW|Rdrop)                           echo "$M_D";;
        *) echo ""; return 1;;
    esac
}
echo "--- leg -> mutator map, re-derived from the frozen mutators at run time ---"
for m in $LIST; do
    want=$(mutof "$m") || { echo "NO MUTATOR FOR $m -- abort"; exit 1; }
    python3 "$want" list 2>/dev/null | tr ' ' '\n' | grep -qx "$m" \
        || { echo "MAP WRONG: $m is not in $(basename "$want") list -- abort"; exit 1; }
done
echo "MAP OK -- every leg is listed by the mutator it is dispatched to"

cd "$C" || exit 1
if [ -e .MUTANT ]; then echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; fi
if cmp -s "$F1" "$SEC/$F1" && cmp -s "$F2" "$SEC/$F2" && cmp -s "$F3" "$SEC/$F3"; then
    echo "BASELINE_CMP CLEAN (clone, all THREE files)"
else echo "clone differs from SEC -- abort"; exit 1; fi
echo "$F1 $F2 $F3 -- #530 kill table 7; restore all three from GXEMUL-SEC, rebuild, cmp + [ gxemul -nt ] each" > .MUTANT

build() {
    rm -f src/devices/dev_lca.o src/devices/dev_pckbc.o src/devices/dev_8253.o
    nice -n 19 make -j2 > "$A/builds/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F1" ] && [ gxemul -nt "$F2" ] && [ gxemul -nt "$F3" ] \
       && [ src/devices/dev_lca.o -nt "$F1" ] && [ src/devices/dev_pckbc.o -nt "$F2" ] \
       && [ src/devices/dev_8253.o -nt "$F3" ]; then
        cp gxemul "$B/t7_$1"; echo "BUILD_OK $1"
    else echo "BUILD_FAIL $1 rc=$rc"; tail -25 "$A/builds/build_$1.log"; return 1; fi
}
restore() {
    cp "$SEC/$F1" "$F1"; cp "$SEC/$F2" "$F2"; cp "$SEC/$F3" "$F3"
    build restored7 || { echo "RESTORE BUILD FAILED -- sentinel kept"; return 1; }
    if cmp -s "$F1" "$SEC/$F1" && cmp -s "$F2" "$SEC/$F2" && cmp -s "$F3" "$SEC/$F3" \
       && [ gxemul -nt "$F1" ] && [ gxemul -nt "$F2" ] && [ gxemul -nt "$F3" ]; then
        rm -f .MUTANT; echo "CLONE RESTORED cmp=clean(all three) binary-nt-source=yes(all three)"
    else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; return 1; fi
}

OK=""
for m in $LIST; do
    MUT=$(mutof "$m")
    python3 "$MUT" "$m" "$SEC" "$C" || { echo "APPLY FAILED $m"; continue; }
    { diff -u "$SEC/$F1" "$F1"; diff -u "$SEC/$F2" "$F2"; diff -u "$SEC/$F3" "$F3"; } > "$A/mutants/$m.diff"
    if [ "$m" = base ]; then
        if cmp -s "$F1" "$SEC/$F1" && cmp -s "$F2" "$SEC/$F2" && cmp -s "$F3" "$SEC/$F3"; then
            echo "BASELINE_CMP CLEAN after applying 'base'"
        else echo "'base' is not a no-op -- abort"; restore; exit 1; fi
    fi
    if build "$m"; then OK="$OK $m"; else echo "NOTE $m DID NOT BUILD -- recorded as a RESULT, not retried"; fi
done
restore || exit 1
cmp -s "$B/t7_base" "$B/t7_restored7" && echo "restored7 == base (byte-identical)" \
    || echo "NOTE restored7 differs from base"
for m in $OK; do
    [ "$m" = base ] && continue
    cmp -s "$B/t7_base" "$B/t7_$m" && echo "NOTE $m BINARY IDENTICAL TO base -- EQUIVALENT MUTANT"
done
echo "BUILDS DONE ($OK) $(date '+%F %T')"

#  ---- CROSS-CHECK every rebuilt edit against the diff closing pass 5 PRESERVED.  A re-derivation that silently
#  ---- differs would make this whole table a measurement of something else.  (The kill8b.sh precedent.)
echo "--- cross-check rebuilt edits against the preserved closing-pass-5 diffs (hunk bodies only) ---"
for m in $LIST; do
    [ "$m" = base ] && continue
    old=""
    [ -f "$C5/logs/$m.diff" ]  && old="$C5/logs/$m.diff"
    [ -f "$C5/logs2/$m.diff" ] && old="$C5/logs2/$m.diff"
    if [ -z "$old" ]; then echo "  $m NO PRESERVED DIFF (new to this table)"; continue; fi
    grep '^[+-][^+-]' "$A/mutants/$m.diff" > /tmp/t7_new.hunk
    grep '^[+-][^+-]' "$old"               > /tmp/t7_old.hunk
    if cmp -s /tmp/t7_new.hunk /tmp/t7_old.hunk; then echo "  $m EDIT IDENTICAL to closing pass 5"
    else echo "  *** $m EDIT DIFFERS ***"; diff -u /tmp/t7_old.hunk /tmp/t7_new.hunk; fi
done

#  ---- probe: two lanes, nine legs each ----
leg() {
    for m in "$@"; do
        case " $OK " in *" $m "*) ;; *) echo "$m SKIPPED (no build)"; continue;; esac
        log="$A/logs/probe_$m.raw"
        ( cd "$A" && python3 -u "$PROBE" "$B/t7_$m" "$m" > "$log" 2>&1 )
        echo "$m $(grep '^LCAISALANE_RESULT=' "$log") $(grep '^LCAISALANE_RETRIED=' "$log") done=$(grep -c '^LCAISALANE_DONE' "$log") tail=[$(tail -1 "$log")] $(date '+%T')"
    done
}
leg base RD2z WWtail WWall dNZtail W23 RWtail nox WW6          > "$A/logs/lane0.out" 2>&1 &
leg RD2post cdxZL3 Wpure RWall noff Wdrop WXR RXW Rdrop        > "$A/logs/lane1.out" 2>&1 &
wait
echo "==== TABLE 7 RESULTS ===="
cat "$A/logs/lane0.out" "$A/logs/lane1.out"
echo "--- mechanical scoring against PRETABLE 7 ---"
python3 "$A/check_pred.py" 2>&1 | tee "$A/check_pred.out"
echo "KILL530G_DONE $(date '+%F %T')"
