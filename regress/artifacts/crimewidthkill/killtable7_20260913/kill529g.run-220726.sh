#!/bin/bash
# kill529g.sh -- #529 kill table 7 (TARGETED), scratch clone /tmp/gxopuscrime, baseline = the #529 working set.
# Instrument: regress/crime_width_probe.py after repair 8 (the third closing pass's class closures), frozen as
# crime_width_probe.table7.py.  Runs: BASE; every earlier kill whose recorded red rows ALL sit in a session
# this repair changed (PRETABLE 4 names them and the rule); the Opus closing seat's non-duplicate mutants; the
# closing panel's mutants -- all on the NEW instrument -- and the panel's claimed undetected changes ALSO on table 3's
# 121-row repair-7 instrument (table 6's), so each claim is MEASURED.
# Builds are serial in the one clone; the PROBE runs go in THREE lanes (PRETABLE 5 states why that is safe here).
# Launch from a frozen copy.
set -u
K=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable7_20260913
K6=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable6_20260913
K5=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable5_20260913
K4=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable4_20260913
K3=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable3_20260913
K2=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable2_20260913
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopuscrime
B=/tmp/gxcrime529g_bins
F=src/devices/dev_sgi_ip32.c
PROBE=/tmp/crime_width_probe.table7.py
OLDPROBE=/tmp/crime_width_probe.table6.frozen.py
FZ=/tmp/k529g                       # frozen mutator tree: the three mutators import each other by relative path
MUT=$FZ/killtable7_20260913/mutants529g.py
NEW="${NEW:-base dogft ctlrdft l_ctl l_time c3_soft_land wstore imaskft a_istat istat2 imask2 h_imask istatsh istat_od1 static_od wst_mc o_wst_mc2 o_lt_blk o_rearm4 o_ctl_collide o_hi_gate o_pa_gate lt_rng lt_par c2_lbl_imask c2_lbl_istat c2_dog100 c2_reg_imask c2_reg_istat c2_reg_dog c2_land_or c2_rearm_dog c2_rearm_txt c2_rearm_rev c2_pre_irq c2_pre_rev c2_bit7_ans c2_bit8_land c2_bit7_quiet c2_bit8_ft c2_bit8_rearm c2_bit8_latch q_istat_leak q_istat_lane q_dog_leak l_imask l_dog c3_lat_b7 c3_lat_b8 c3_quiet_b1 c3_quiet_imask c3_pre_dog c3_pre_revbr c3_pre_istat c3_far_and c3_half_istat c3_half_imask c3_pre_ctl0 c3_pre_dogclr r_rearm_ctlrd r_rearm_dogclr r_rearm_ctl0 r_pre_istat r_pre_revbr r_pre_dogbr r_byp_rev r_byp_time r_ans_hi32_b5 r_land_b4clr r_ans_ctl_lb r_pre_ctlrd}"
OLD="${OLD:-c3_lat_b7 c3_lat_b8 c3_quiet_b1 c3_quiet_imask c3_far_and c3_half_istat c3_half_imask}"
mkdir -p "$B" "$K/logs" "$K/builds"
rm -rf "$FZ"; mkdir -p "$FZ/killtable2_20260913" "$FZ/killtable3_20260913" "$FZ/killtable4_20260913" "$FZ/killtable5_20260913" "$FZ/killtable6_20260913" "$FZ/killtable7_20260913"
cp "$K2/mutants529b.py" "$FZ/killtable2_20260913/"
cp "$K3/mutants529c.py" "$FZ/killtable3_20260913/"
cp "$K4/mutants529d.py" "$K4/mutants_close_opus.py" "$FZ/killtable4_20260913/"
cp "$K5/mutants529e.py" "$K5/mutants_close2_opus.py" "$FZ/killtable5_20260913/"
cp "$K6/mutants529f.py" "$K6/mutants_close2_opus_b3.py" "$FZ/killtable6_20260913/"
cp "$K/mutants529g.py" "$FZ/killtable7_20260913/"; [ -e "$K/mutants_close3_opus.py" ] && cp "$K/mutants_close3_opus.py" "$FZ/killtable7_20260913/"
cp "$SEC/regress/crime_width_probe.py" "$PROBE"
cp "$PROBE" "$K/crime_width_probe.table7.py"
cp "$K6/crime_width_probe.table6.py" "$OLDPROBE"
md5sum "$PROBE" "$OLDPROBE" "$MUT" "$FZ"/killtable*/*.py "$SEC/$F" | tee "$K/logs/INSTRUMENT.md5"
cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
echo "$F #529 kill table 7 (main loop) -- restore from GXEMUL-SEC" > .MUTANT
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
# ---- probe runs, FOUR lanes: NEW runs dealt round-robin, then the OLD runs the same way ----
lane() {    # lane <n> <list of TAG:mutant>
    n=$1; shift
    for tm in "$@"; do
        tag=${tm%%:*}; m=${tm#*:}
        if [ "$tag" = NEW ]; then p=$PROBE; log="$K/logs/probe_$m.raw"; else p=$OLDPROBE; log="$K/logs/probe_T6INSTR_$m.raw"; fi
        python3 -u "$p" "$B/$m" "$m" > "$log" 2>&1
        echo "$tag $m $(grep '^CRIMEP_RESULT=' "$log") $(grep '^CRIMEP_CONTROL=' "$log") $(grep -c '^CRIMEP_DONE' "$log") FAILING:$(grep '^FAILING:' "$log" | cut -c9-)"
    done > "$K/logs/lane$n.out"
}
L0=(); L1=(); L2=(); L3=(); i=0
for tm in $(for m in $NEW; do echo "NEW:$m"; done; for m in $OLD; do echo "T6INSTR:$m"; done); do
    case $((i % 4)) in 0) L0+=("$tm");; 1) L1+=("$tm");; 2) L2+=("$tm");; 3) L3+=("$tm");; esac; i=$((i + 1))
done
lane 0 "${L0[@]}" &
lane 1 "${L1[@]}" &
lane 2 "${L2[@]}" &
lane 3 "${L3[@]}" &
wait
for m in $NEW; do grep -h "^NEW $m " "$K/logs/lane0.out" "$K/logs/lane1.out" "$K/logs/lane2.out" "$K/logs/lane3.out"; done
for m in $OLD; do grep -h "^T6INSTR $m " "$K/logs/lane0.out" "$K/logs/lane1.out" "$K/logs/lane2.out" "$K/logs/lane3.out"; done
echo KILL529G_DONE
