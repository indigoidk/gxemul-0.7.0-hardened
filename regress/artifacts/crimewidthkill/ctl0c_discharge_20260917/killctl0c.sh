#!/bin/bash
#  #529 L1 -- the ctl0c DISCHARGE leg.  SCRATCH CLONE ONLY; no project tree is written
#  except this artifacts directory.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
A=$SEC/regress/artifacts/crimewidthkill/ctl0c_discharge_20260917
C=/tmp/gxctl0c
F=src/devices/dev_sgi_ip32.c
PROBE=$A/crime_width_probe.frozen.py
MUT=$A/mutants_ctl0c.py
mkdir -p "$A/logs" "$A/bin"

#  ---- freeze the instrument, and PROVE it is the shipped one ----
cp "$SEC/regress/crime_width_probe.py" "$PROBE"
cmp -s "$PROBE" "$SEC/regress/crime_width_probe.py" \
  && echo "PROBE FROZEN cmp=clean" || { echo "PROBE FREEZE FAILED"; exit 9; }

#  ---- clone ----
[ -d "$C" ] && rm -rf "$C"
cp -a /tmp/gxsec-build "$C" || { echo "CLONE FAILED"; exit 9; }
cd "$C" || exit 9
if [ -e .MUTANT ]; then echo "SENTINEL PRESENT AT START -- ABORT"; cat .MUTANT; exit 1; fi

#  ---- NAME THE BASELINE and prove clone identity before mutant 1 ----
if cmp -s "$F" "$SEC/$F"; then echo "CLONE START: $F cmp CLEAN against SEC"
else echo "CLONE START: $F DIFFERS from SEC -- ABORT"; exit 9; fi

build () {
    rm -f src/devices/dev_sgi_ip32.o gxemul
    make -j4 > "$A/logs/build_$1.log" 2>&1; rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
        cp gxemul "$A/bin/$1"; echo "BUILD_OK $1"
    else
        echo "BUILD_FAILED $1 rc=$rc  (MAKE_RC has been seen to lie; the -nt checks are the oracle)"
        return 1
    fi
}
restore () {
    cp "$SEC/$F" "$F"
    build restored > /dev/null 2>&1
    if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then
        rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"
    else
        echo "CLONE RESTORE INCOMPLETE -- SENTINEL KEPT"; return 1
    fi
}

#  ---- base ----
build base || exit 9
python3 -u "$PROBE" "$A/bin/base" base > "$A/logs/probe_base.raw" 2>&1
echo "base $(grep -oE 'CRIMEP_RESULT=[0-9]+/[0-9]+' "$A/logs/probe_base.raw" | tail -1)"

#  ---- the one mutant ----
m=M_ctl0c_decline
echo "$m  #529 ctl0c discharge -- restore from GXEMUL-SEC, then REBUILD" > .MUTANT
python3 "$MUT" "$m" "$SEC/$F" "$F" || { echo "APPLY FAILED"; restore; exit 9; }
if build "$m"; then
    cmp -s "$A/bin/base" "$A/bin/$m" \
      && echo "NOTE $m BINARY IDENTICAL TO base -- EQUIVALENT MUTANT, the score means nothing" \
      || echo "NOTE $m binary DIFFERS from base -- the edit is live in the object"
    python3 -u "$PROBE" "$A/bin/$m" "$m" > "$A/logs/probe_$m.raw" 2>&1
    echo "$m $(grep -oE 'CRIMEP_RESULT=[0-9]+/[0-9]+' "$A/logs/probe_$m.raw" | tail -1)"
fi
restore

#  ---- THE ORACLE: did the two rows under test actually RED? ----
echo "---- ctl0c DISCHARGE VERDICT ----"
for r in "acc ctl0c" "p acc ctl0c" "acc ctl4r" "p acc ctl4r"; do
    b=$(grep -c "^$r .*ok$"   "$A/logs/probe_base.raw")
    n=$(grep -c "^$r .*FAIL$" "$A/logs/probe_$m.raw")
    printf '  %-14s base_ok=%s  mutant_FAIL=%s\n' "$r" "$b" "$n"
done
echo "KILLCTL0C_DONE $(date '+%Y-%m-%d %H:%M:%S')"
