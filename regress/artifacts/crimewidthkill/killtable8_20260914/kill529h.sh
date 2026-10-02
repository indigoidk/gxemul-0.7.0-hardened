#!/bin/bash
# kill529h.sh -- #529 kill table 8 (TARGETED), scratch clone /tmp/gxopuscrime, baseline = the #529 working set.
# Instrument: regress/crime_width_probe.py after repair 8 (the third closing pass's class closures), frozen as
# crime_width_probe.table7.py.  Runs: BASE; every earlier kill whose recorded red rows ALL sit in a session
# this repair changed (PRETABLE 4 names them and the rule); the Opus closing seat's non-duplicate mutants; the
# closing panel's mutants -- all on the NEW instrument -- and the panel's claimed undetected changes ALSO on table 3's
# 121-row repair-7 instrument (table 6's), so each claim is MEASURED.
# Builds are serial in the one clone; the PROBE runs go in THREE lanes (PRETABLE 5 states why that is safe here).
# Launch from a frozen copy.
set -u
K=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable8_20260914
K7=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable7_20260913
K6=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable6_20260913
K5=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable5_20260913
K4=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable4_20260913
K3=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable3_20260913
K2=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable2_20260913
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopuscrime
B=/tmp/gxcrime529h_bins
F=src/devices/dev_sgi_ip32.c
PROBE=/tmp/crime_width_probe.table8.py
OLDPROBE=/tmp/crime_width_probe.table6.frozen.py
FZ=/tmp/k529h                       # frozen mutator tree: the three mutators import each other by relative path
MUT=$FZ/killtable8_20260914/mutants529h.py
NEW="${NEW:-base c2_pre_rev c2_rearm_dog c2_rearm_rev c2_rearm_txt c3_pre_ctl0 c3_pre_dog c3_pre_dogclr c3_pre_istat c3_pre_revbr lt_wset nolatch o_ctl_collide o_hi_gate o_pa_gate r_byp_rev r_land_b4clr r_pre_ctlrd r_pre_dogbr r_pre_istat r_pre_revbr r_rearm_ctl0 r_rearm_ctlrd r_rearm_dogclr rearm static_od c1_deepseek c2_kimik3 c3_codex_dbg c4_kimicli c5_codex_b1 d1_rearm_dog0200 d2_pre_dog0200 d3_rearm_wtime d4_pre_wistat d6_chan_len2 d7_rearm_wrev x_pre_dog4w x_rearm_rev8r x_pre_time4r x_rearm_ctl8w0200 x_chan_rev x_chan_write x_rearm_defhi x_pre_rev_wp}"
OLD="${OLD:-}"
mkdir -p "$B" "$K/logs" "$K/builds"
rm -rf "$FZ"; mkdir -p "$FZ/killtable2_20260913" "$FZ/killtable3_20260913" "$FZ/killtable4_20260913" "$FZ/killtable5_20260913" "$FZ/killtable6_20260913" "$FZ/killtable7_20260913" "$FZ/killtable8_20260914"
cp "$K2/mutants529b.py" "$FZ/killtable2_20260913/"
cp "$K3/mutants529c.py" "$FZ/killtable3_20260913/"
cp "$K4/mutants529d.py" "$K4/mutants_close_opus.py" "$FZ/killtable4_20260913/"
cp "$K5/mutants529e.py" "$K5/mutants_close2_opus.py" "$FZ/killtable5_20260913/"
cp "$K6/mutants529f.py" "$K6/mutants_close2_opus_b3.py" "$FZ/killtable6_20260913/"
cp "$K7/mutants529g.py" "$K7/mutants_close3_opus.py" "$FZ/killtable7_20260913/"
cp "$K/mutants529h.py" "$K/mutants_c4_opus.py" "$FZ/killtable8_20260914/"
cp "$SEC/regress/crime_width_probe.py" "$PROBE"
cp "$PROBE" "$K/crime_width_probe.table8.py"
md5sum "$PROBE" "$MUT" "$FZ"/killtable*/*.py "$SEC/$F" | tee "$K/logs/INSTRUMENT.md5"
cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
echo "$F #529 kill table 8 (main loop) -- restore from GXEMUL-SEC" > .MUTANT
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
restore_and_exit() {    # table 7's first launch died on a mutant that did not compile and LEFT THE CLONE MUTANT --
    cp "$SEC/$F" "$F"      # the build-failure path now restores before it exits
    build restored && cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ] && rm -f .MUTANT && echo "CLONE RESTORED after failure"
    exit 1
}
for m in $NEW; do
    python3 "$MUT" "$m" "$SEC/$F" "$F" || { echo "APPLY FAILED $m"; restore_and_exit; }
    diff -u "$SEC/$F" "$F" > "$K/logs/$m.diff.new"
    if [ "$m" = base ]; then cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN" || { echo "BASELINE_CMP DIFFERS"; restore_and_exit; }; fi
    #  REUSE=1: a binary from an earlier launch is reused ONLY when this mutant's diff is byte-identical to the one it
    #  was built from (same baseline, same tree, same edit) -- else rebuilt
    if [ "${REUSE:-0}" = 1 ] && [ -x "$B/$m" ] && [ -e "$K/logs/$m.diff" ] && cmp -s "$K/logs/$m.diff" "$K/logs/$m.diff.new"; then
        mv "$K/logs/$m.diff.new" "$K/logs/$m.diff"; echo "REUSED $m (diff identical)"; continue
    fi
    mv "$K/logs/$m.diff.new" "$K/logs/$m.diff"
    build "$m" || restore_and_exit
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
echo KILL529H_DONE
