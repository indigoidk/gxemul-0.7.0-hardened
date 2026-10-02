#!/bin/bash
# kill529e.sh -- #529 kill table 5 (TARGETED), scratch clone /tmp/gxopuscrime, baseline = the #529 working set.
# Instrument: regress/crime_width_probe.py after the SECOND closing pass's repair (repair 6), frozen as
# crime_width_probe.table5.py.  Runs: BASE; every earlier kill whose recorded red rows ALL sit in a session
# this repair changed (PRETABLE 4 names them and the rule); the Opus closing seat's non-duplicate mutants; the
# closing panel's mutants -- all on the NEW instrument -- and the panel's claimed undetected changes ALSO on table 3's
# 111-row instrument, so each claim is MEASURED.  (The Opus seat measured its own on the 111-row version.)
# Builds are serial in the one clone; the PROBE runs go in THREE lanes (PRETABLE 5 states why that is safe here).
# Launch from a frozen copy.
set -u
K=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable5_20260913
K4=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable4_20260913
K3=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable3_20260913
K2=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable2_20260913
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopuscrime
B=/tmp/gxcrime529e_bins
F=src/devices/dev_sgi_ip32.c
PROBE=/tmp/crime_width_probe.table5.py
OLDPROBE=/tmp/crime_width_probe.table4.frozen.py
FZ=/tmp/k529e                       # frozen mutator tree: the three mutators import each other by relative path
MUT=$FZ/killtable5_20260913/mutants529e.py
NEW="${NEW:-base acc4low x_mc4 x_mc8 imaskft a_istat istat2 imask2 istatsh remap h_imask lt_len c_dog o_rearm4 o_pre4 o_ctl_collide o_rd_hi o_hi_gate o_pa_gate o_acc4_210 lt_ctl c_endian istat_od1 dogft ctlrdft c2_lbl_imask c2_lbl_istat c2_lbl_ctl c2_dog100 c2_reg_imask c2_reg_istat c2_reg_dog c2_land_or c2_rearm_dog c2_rearm_txt c2_rearm_rev c2_pre_irq c2_pre_rev c2_bit7_ans c2_bit8_land c2_bit7_quiet c2_bit8_ft c2_bit8_rearm c2_bit8_latch p_rd_hi_lh p_soft_gate p_rd_hi_lb p_rd_lh_all}"
OLD="${OLD:-c2_lbl_imask c2_lbl_istat c2_lbl_ctl c2_dog100 c2_rearm_dog c2_reg_imask c2_reg_istat c2_reg_dog c2_land_or c2_pre_irq c2_pre_rev c2_bit7_ans}"
mkdir -p "$B" "$K/logs" "$K/builds"
rm -rf "$FZ"; mkdir -p "$FZ/killtable2_20260913" "$FZ/killtable3_20260913" "$FZ/killtable4_20260913" "$FZ/killtable5_20260913"
cp "$K2/mutants529b.py" "$FZ/killtable2_20260913/"
cp "$K3/mutants529c.py" "$FZ/killtable3_20260913/"
cp "$K4/mutants529d.py" "$K4/mutants_close_opus.py" "$FZ/killtable4_20260913/"
cp "$K/mutants529e.py" "$K/mutants_close2_opus.py" "$FZ/killtable5_20260913/"
cp "$SEC/regress/crime_width_probe.py" "$PROBE"
cp "$PROBE" "$K/crime_width_probe.table5.py"
cp "$K4/crime_width_probe.table4.py" "$OLDPROBE"
md5sum "$PROBE" "$OLDPROBE" "$MUT" "$FZ"/killtable*/*.py "$SEC/$F" | tee "$K/logs/INSTRUMENT.md5"
cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
echo "$F #529 kill table 5 (main loop) -- restore from GXEMUL-SEC" > .MUTANT
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
# ---- probe runs, three lanes: NEW runs dealt round-robin, then the OLD runs the same way ----
lane() {    # lane <n> <list of TAG:mutant>
    n=$1; shift
    for tm in "$@"; do
        tag=${tm%%:*}; m=${tm#*:}
        if [ "$tag" = NEW ]; then p=$PROBE; log="$K/logs/probe_$m.raw"; else p=$OLDPROBE; log="$K/logs/probe_T4INSTR_$m.raw"; fi
        python3 -u "$p" "$B/$m" "$m" > "$log" 2>&1
        echo "$tag $m $(grep '^CRIMEP_RESULT=' "$log") $(grep '^CRIMEP_CONTROL=' "$log") $(grep -c '^CRIMEP_DONE' "$log") FAILING:$(grep '^FAILING:' "$log" | cut -c9-)"
    done > "$K/logs/lane$n.out"
}
L0=(); L1=(); L2=(); i=0
for tm in $(for m in $NEW; do echo "NEW:$m"; done; for m in $OLD; do echo "T4INSTR:$m"; done); do
    case $((i % 3)) in 0) L0+=("$tm");; 1) L1+=("$tm");; 2) L2+=("$tm");; esac; i=$((i + 1))
done
lane 0 "${L0[@]}" &
lane 1 "${L1[@]}" &
lane 2 "${L2[@]}" &
wait
for m in $NEW; do grep -h "^NEW $m " "$K/logs/lane0.out" "$K/logs/lane1.out" "$K/logs/lane2.out"; done
for m in $OLD; do grep -h "^T4INSTR $m " "$K/logs/lane0.out" "$K/logs/lane1.out" "$K/logs/lane2.out"; done
echo KILL529E_DONE
