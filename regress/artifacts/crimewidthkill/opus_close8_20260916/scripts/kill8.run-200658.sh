#!/bin/bash
# kill8.sh -- #529 CLOSING PASS 8 kill table, Opus MEASURING seat.  SCRATCH CLONE /tmp/gxopusc8 only; no project
# tree is written.  Instrument: the SHIPPED 188-row probe, frozen once.  Launch from a FROZEN COPY of this file.
set -u
A=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close8_20260916
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopusc8
B=/tmp/gxopusc8_bins
F=src/devices/dev_sgi_ip32.c
PROBE=/tmp/crime_width_probe.close8.py
MUT=/tmp/mutants8.frozen.py
LIST="${LIST:-base L_dfl4w_hi L_dfl4w_lo L_dfl4r_hi L_dfl4r_lo W_rev8r_out W_rev8w_out W_rev4w_out W_rev4r_out G_lane_ist G_lane_tim G_lane_all D1_landpost D2_remappost}"
mkdir -p "$B" "$A/logs" "$A/builds" "$A/mutants"
cp "$SEC/regress/crime_width_probe.py" "$PROBE"
cp "$A/scripts/mutants8.py" "$MUT"
md5sum "$PROBE" "$MUT" "$SEC/$F" "$SEC/regress/crime_width_probe.py" | tee "$A/logs/INSTRUMENT.md5"
cd "$C" || exit 1
if [ -e .MUTANT ]; then echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; fi
echo "$F  #529 closing pass 8 (Opus measuring seat) -- restore from GXEMUL-SEC, then REBUILD" > .MUTANT
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
if cmp -s "$B/base" "$B/restored"; then echo "restored == base (byte-identical)"; else echo "restored differs from base"; fi
for m in $LIST; do
    if [ "$m" != base ] && cmp -s "$B/base" "$B/$m"; then echo "WARN $m BINARY IDENTICAL TO base"; fi
done
lane() {
    n=$1; shift
    for m in "$@"; do
        log="$A/logs/probe_$m.raw"
        python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1
        echo "$m $(grep '^CRIMEP_RESULT=' "$log") $(grep '^CRIMEP_CONTROL=' "$log") done=$(grep -c '^CRIMEP_DONE' "$log") FAILING:$(grep '^FAILING:' "$log" | cut -c9-)"
    done > "$A/logs/lane$n.out"
}
L0=(); L1=(); L2=(); L3=(); i=0
for m in $LIST; do
    case $((i % 4)) in 0) L0+=("$m");; 1) L1+=("$m");; 2) L2+=("$m");; 3) L3+=("$m");; esac; i=$((i + 1))
done
lane 0 "${L0[@]}" & lane 1 "${L1[@]}" & lane 2 "${L2[@]}" & lane 3 "${L3[@]}" &
wait
for m in $LIST; do grep -h "^$m " "$A/logs/lane0.out" "$A/logs/lane1.out" "$A/logs/lane2.out" "$A/logs/lane3.out"; done
echo KILL8_DONE
