#!/bin/bash
# kill529d.sh -- #529 kill table 4 (TARGETED), scratch clone /tmp/gxopuscrime, baseline = the #529 working set.
# Instrument: regress/crime_width_probe.py after the closing-pass repair (repair 4 + the acc4_210 construction fix),
# frozen as crime_width_probe.table4.py.  Runs: BASE; every earlier kill whose recorded red rows ALL sit in a session
# this repair changed (PRETABLE 4 names them and the rule); the Opus closing seat's non-duplicate mutants; the
# closing panel's mutants -- all on the NEW instrument -- and the panel's claimed undetected changes ALSO on table 3's
# 85-row instrument, so each claim is MEASURED.  (The Opus seat measured its own on the 85-row version.)
# Builds are serial in the one clone; the PROBE runs go in two lanes (PRETABLE 4 states why that is safe here).
# Launch from a frozen copy.
set -u
K=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable4_20260913
K3=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable3_20260913
K2=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable2_20260913
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopuscrime
B=/tmp/gxcrime529d_bins
F=src/devices/dev_sgi_ip32.c
PROBE=/tmp/crime_width_probe.table4.py
OLDPROBE=/tmp/crime_width_probe.table3.frozen.py
FZ=/tmp/k529d                       # frozen mutator tree: the three mutators import each other by relative path
MUT=$FZ/killtable4_20260913/mutants529d.py
NEW="${NEW:-base len2only acc8dog acc4low annlow timeft imaskft a_istat l_addrmask x_mc4 x_mc8 dogft ctlrdft istat2 imask2 time2 istatsh remap h_imask h_lbl lt_len lt_addr wst_mc c_dog c_hrclr o_rearm4 o_pre4 o_rearm_time o_ctl_collide o_wst_mc2 o_rd_hi o_lt_blk o_lt_wl o_wnz_lbl o_hi_gate o_pa_gate o_acc4_210 near8 lt_ctl lt_rng lt_par c_endian c_bit1 rev_od1 istat_od1 time_od1 time_land}"
OLD="${OLD:-near8 lt_ctl lt_rng lt_par c_endian c_bit1 rev_od1 istat_od1 time_od1 time_land}"
mkdir -p "$B" "$K/logs" "$K/builds"
rm -rf "$FZ"; mkdir -p "$FZ/killtable2_20260913" "$FZ/killtable3_20260913" "$FZ/killtable4_20260913"
cp "$K2/mutants529b.py" "$FZ/killtable2_20260913/"
cp "$K3/mutants529c.py" "$FZ/killtable3_20260913/"
cp "$K/mutants529d.py" "$K/mutants_close_opus.py" "$FZ/killtable4_20260913/"
cp "$SEC/regress/crime_width_probe.py" "$PROBE"
cp "$PROBE" "$K/crime_width_probe.table4.py"
cp "$K3/crime_width_probe.table3.py" "$OLDPROBE"
md5sum "$PROBE" "$OLDPROBE" "$MUT" "$FZ"/killtable*/*.py "$SEC/$F" | tee "$K/logs/INSTRUMENT.md5"
cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
echo "$F #529 kill table 4 (main loop) -- restore from GXEMUL-SEC" > .MUTANT
build() {
    rm -f src/devices/dev_sgi_ip32.o
    make -j4 > "$K/builds/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1"
    else
        echo "BUILD_FAIL $1 rc=$rc"; tail -20 "$K/builds/build_$1.log"; return 1
    fi
}
for m in $NEW; do
    python3 "$MUT" "$m" "$SEC/$F" "$F" || { echo "APPLY FAILED $m"; exit 1; }
    diff -u "$SEC/$F" "$F" > "$K/logs/$m.diff"
    if [ "$m" = base ]; then cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN" || { echo "BASELINE_CMP DIFFERS"; exit 1; }; fi
    build "$m" || exit 1
done
cp "$SEC/$F" "$F"
build restored || exit 1
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"; else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; fi
cmp -s "$B/base" "$B/restored" && echo "restored == base (byte-identical)" || echo "restored differs from base"
for m in $NEW; do
    [ "$m" = base ] || { cmp -s "$B/base" "$B/$m" && echo "NOTE $m BINARY IDENTICAL TO base"; }
done
# ---- probe runs, two lanes: every other NEW run, then the OLD runs split the same way ----
lane() {    # lane <n> <list of TAG:mutant>
    n=$1; shift
    for tm in "$@"; do
        tag=${tm%%:*}; m=${tm#*:}
        if [ "$tag" = NEW ]; then p=$PROBE; log="$K/logs/probe_$m.raw"; else p=$OLDPROBE; log="$K/logs/probe_T3INSTR_$m.raw"; fi
        python3 -u "$p" "$B/$m" "$m" > "$log" 2>&1
        echo "$tag $m $(grep '^CRIMEP_RESULT=' "$log") $(grep '^CRIMEP_CONTROL=' "$log") $(grep -c '^CRIMEP_DONE' "$log") FAILING:$(grep '^FAILING:' "$log" | cut -c9-)"
    done > "$K/logs/lane$n.out"
}
L0=(); L1=(); i=0
for m in $NEW; do if [ $((i % 2)) = 0 ]; then L0+=("NEW:$m"); else L1+=("NEW:$m"); fi; i=$((i + 1)); done
for m in $OLD; do if [ $((i % 2)) = 0 ]; then L0+=("T3INSTR:$m"); else L1+=("T3INSTR:$m"); fi; i=$((i + 1)); done
lane 0 "${L0[@]}" &
lane 1 "${L1[@]}" &
wait
for m in $NEW; do grep -h "^NEW $m " "$K/logs/lane0.out" "$K/logs/lane1.out"; done
for m in $OLD; do grep -h "^T3INSTR $m " "$K/logs/lane0.out" "$K/logs/lane1.out"; done
echo KILL529D_DONE
