#!/bin/bash
# kill14.sh -- Opus pass-1 seat, #529 repair 14.  SCRATCH CLONE /tmp/gxopus_r14 ONLY.
# No project tree is written except this round's own artifacts dir.  Launch from a FROZEN COPY.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
A=$SEC/regress/artifacts/crimewidthkill/repair14_20260916/opus_pass1_work
C=/tmp/gxopus_r14
B=/tmp/gxopus_r14_bins
F=src/devices/dev_sgi_ip32.c
PROBE=/tmp/crime_width_probe.r14.py
MUT=/tmp/mutants14.frozen.py
LIST="base M4_timeplain M3_timelatch"

mkdir -p "$B" "$A/logs" "$A/builds" "$A/mutants"
cp "$SEC/regress/crime_width_probe.py" "$PROBE"
cp "$A/mutants14.py" "$MUT"
md5sum "$PROBE" "$MUT" "$SEC/$F" | tee "$A/logs/INSTRUMENT.md5"

cd "$C" || exit 1
if [ -e .MUTANT ]; then echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; fi
echo "$F  #529 repair-14 Opus pass-1 seat -- restore from GXEMUL-SEC, then REBUILD" > .MUTANT

build() {
    rm -f src/devices/dev_sgi_ip32.o
    make -j4 > "$A/builds/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1"
    else
        echo "BUILD_FAIL $1 rc=$rc"; tail -25 "$A/builds/build_$1.log"; return 1
    fi
}
restore_and_exit() {
    cp "$SEC/$F" "$F"
    build restored && cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ] && rm -f .MUTANT && echo "CLONE RESTORED after failure"
    exit 1
}

for m in $LIST; do
    python3 "$MUT" "$m" "$SEC/$F" "$F" || { echo "APPLY FAILED $m"; restore_and_exit; }
    diff -u "$SEC/$F" "$F" > "$A/mutants/$m.diff"
    if [ "$m" = base ]; then
        if cmp -s "$F" "$SEC/$F"; then echo "BASELINE_CMP CLEAN"; else echo "BASELINE_CMP DIFFERS"; restore_and_exit; fi
    fi
    build "$m" || restore_and_exit
done

cp "$SEC/$F" "$F"
build restored || exit 1
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"; else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; fi
for m in $LIST; do
    if [ "$m" != base ] && cmp -s "$B/base" "$B/$m"; then echo "WARN $m BINARY IDENTICAL TO base"; fi
done

#  the positive control: close-8's ALREADY-BUILT G_clr_imk4r binary, re-run under MY driver
:

lane() {
    n=$1; shift
    for m in "$@"; do
        log="$A/logs/probe_$m.raw"
        python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1
        echo "$m $(grep '^CRIMEP_RESULT=' "$log") $(grep '^CRIMEP_CONTROL=' "$log") done=$(grep -c '^CRIMEP_DONE' "$log") FAILING:$(grep '^FAILING:' "$log" | cut -c9-)"
    done > "$A/logs/lane$n.out"
}
lane 4 M4_timeplain &
lane 5 M3_timelatch &
:
:
wait
cat "$A/logs"/lane4.out "$A/logs"/lane5.out | tee "$A/logs/table14b.out"
echo KILL14B_DONE
