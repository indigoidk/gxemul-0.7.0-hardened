#!/bin/bash
# kill529_15a.sh -- #529 table 15a: the pass-2 adversarial candidate against repair 15 (H_noresetclear) and its
#   sibling (E_noendianclear), on the UNCHANGED table-14 probe.  PRETABLE15a.out and check15a.py were written FIRST.
#   LAUNCH FROM A FROZEN COPY, with run_in_background.  SCRATCH CLONE /tmp/gxopus_r14 ONLY.
set -u
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/table15a_20260926
T14=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/table14_20260926
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus_r14
B=/tmp/gxopus_r14_bins15a
F=src/devices/dev_sgi_ip32.c
PROBE=$T14/crime_width_probe.table14.py
MUT=$A/mutants_15a.frozen.py
LIST="H_noresetclear E_noendianclear"

echo "KILL529_15A_START $(date '+%F %T')"
mkdir -p "$B" "$A/logs" "$A/builds" "$A/mutants"
cp "$A/mutants_15a.py" "$MUT"
md5sum "$PROBE" "$MUT" "$SEC/$F" | tee "$A/logs/INSTRUMENT.md5"
want_md5() { case "$(md5sum "$1" | cut -c1-8)" in "$2") return 0;; *) echo "INSTRUMENT MISMATCH: $1 is not $2 -- abort"; return 1;; esac; }
want_md5 "$PROBE" f5e915f6 && want_md5 "$MUT" a614547c && want_md5 "$SEC/$F" 8c1d1545 || exit 1
echo "INSTRUMENT OK -- probe f5e915f6 (table 14's), mutator a614547c, source 8c1d1545"

cd "$C" || { echo "clone $C missing -- abort"; exit 1; }
if [ -e .MUTANT ]; then echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; fi
cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN" || { echo "clone differs from SEC -- abort"; exit 1; }
[ gxemul -nt "$F" ] && echo "BASELINE BINARY FRESH (gxemul newer than $F)" || { echo "baseline binary stale -- abort"; exit 1; }
cp gxemul "$B/base_inherited"
echo "$F  #529 table 15a -- restore from GXEMUL-SEC, then REBUILD" > .MUTANT

build() {
    rm -f src/devices/dev_sgi_ip32.o
    nice -n 19 make -j4 > "$A/builds/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1 $(date '+%T')"
    else echo "BUILD_FAIL $1 rc=$rc"; tail -25 "$A/builds/build_$1.log"; return 1; fi
}
restore() {
    cp "$SEC/$F" "$F"
    build restored || { echo "RESTORE BUILD FAILED -- sentinel kept"; return 1; }
    if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then
        rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"
    else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; return 1; fi
}

OK=""
for m in $LIST; do
    python3 "$MUT" "$m" "$SEC/$F" "$F" || { echo "APPLY FAILED $m"; continue; }
    diff -u "$SEC/$F" "$F" > "$A/mutants/$m.diff"
    if build "$m"; then OK="$OK $m"; else echo "NOTE $m DID NOT BUILD -- recorded as a RESULT, not retried"; fi
done
restore || exit 1
cmp -s "$B/base_inherited" "$B/restored" && echo "restored == the inherited base binary (byte-identical)" \
    || echo "NOTE restored differs from the inherited base binary"
for m in $OK; do cmp -s "$B/restored" "$B/$m" && echo "NOTE $m BINARY IDENTICAL TO base -- EQUIVALENT MUTANT"; done
echo "BUILDS DONE ($OK) $(date '+%F %T')"

leg() {
    m=$1
    case " $OK " in *" $m "*) ;; *) echo "$m SKIPPED (no build)"; return;; esac
    log="$A/logs/probe_$m.raw"
    python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1
    echo "$m $(grep '^CRIMEP_RESULT=' "$log") $(grep '^CRIMEP_CONTROL=' "$log") done=$(grep -c '^CRIMEP_DONE' "$log") FAILING:$(grep '^FAILING:' "$log" | cut -c9-) $(date '+%T')"
}
echo "PROBES START $(date '+%F %T')"
leg H_noresetclear > "$A/logs/lane0.out" 2>&1 &
leg E_noendianclear > "$A/logs/lane1.out" 2>&1 &
wait
echo "==== TABLE 15a RESULTS ===="
cat "$A/logs/lane0.out" "$A/logs/lane1.out"
python3 "$A/check15a.py" 2>&1 | tee "$A/check15a.out"
echo "KILL529_15A_DONE $(date '+%F %T')"
