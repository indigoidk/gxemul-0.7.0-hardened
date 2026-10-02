#!/bin/bash
# kill529r14.sh -- #529 KILL TABLE 12: repair 14, the accept-side class closure Fable ruled.
#
#   FIFTEEN legs across FOUR frozen mutators, against the repaired probe.  PRETABLE.out and check_pred.py
#   beside this file were both written FIRST and their mtimes prove it.
#
#   *** LAUNCH FROM A FROZEN COPY (cp kill529r14.sh kill529r14.run-<stamp>.sh) AND WITH run_in_background. ***
#   Bash reads a script incrementally, so editing this file while it runs corrupts the run.
#
#   *** DO NOT START THIS WHILE #530's TABLE 7 IS RUNNING. ***  Both carry wall-clock oracles -- this one's
#   `c t4w/c t4r gap' and `p t4w/p t4r gap' rows measure a clock advance across the debugger's own pause --
#   and this project has a recorded gate failure from two concurrent CPU-heavy jobs.
#
#   SCRATCH CLONE /tmp/gxopus_r14 ONLY.  No project tree is written except this artifacts directory.
set -u
A=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/repair14_20260916
C8=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close8_20260916
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus_r14
B=/tmp/gxopus_r14_bins
F=src/devices/dev_sgi_ip32.c
PROBE=$A/crime_width_probe.table12.py
M_8B=$A/mutants8b.frozen.py
M_14=$A/mutants14.frozen.py
M_ADJ=$A/mutants_adj.frozen.py
M_R14=$A/mutants_r14.frozen.py

LIST="base G_glm_tim4clear G_clr_ist4r G_clr_ctl4r G_clr_imk4r G_lane_ctl K_ctl4w_reset_post \
K_ctl8w_reset_post M1_gotolatch M2_ld278clr M3_timelatch M4_timeplain M5_revlatch M6_istlatch W_ctl8w"

mkdir -p "$B" "$A/logs" "$A/builds" "$A/mutants"

#  ---- freeze the instrument and all four mutators, and PROVE the probe is the shipped one ----
cp "$SEC/regress/crime_width_probe.py"                   "$PROBE"
cp "$C8/scripts/mutants8b.py"                            "$M_8B"
cp "$A/opus_pass1_work/mutants14.py"                     "$M_14"
cp "$A/opus_adj_work/mutants_adj.py"                     "$M_ADJ"
cp "$A/mutants_r14.py"                                   "$M_R14"
md5sum "$PROBE" "$M_8B" "$M_14" "$M_ADJ" "$M_R14" "$SEC/$F" | tee "$A/logs/INSTRUMENT.md5"
cmp -s "$PROBE" "$SEC/regress/crime_width_probe.py" \
    && echo "PROBE frozen == shipped" || { echo "PROBE mismatch -- abort"; exit 1; }

#  ---- the leg -> mutator map, VERIFIED AT RUN TIME against each mutator's own list ----
mutof() {
    case "$1" in
        base|G_glm_tim4clear|G_clr_ist4r|G_clr_ctl4r|G_clr_imk4r|G_lane_ctl|K_ctl4w_reset_post|K_ctl8w_reset_post)
            echo "$M_8B";;
        M1_gotolatch|M2_ld278clr|M3_timelatch|M4_timeplain) echo "$M_14";;
        M5_revlatch|M6_istlatch)                            echo "$M_ADJ";;
        W_ctl8w)                                            echo "$M_R14";;
        *) echo ""; return 1;;
    esac
}
echo "--- leg -> mutator map, re-derived at run time ---"
for m in $LIST; do
    want=$(mutof "$m") || { echo "NO MUTATOR FOR $m -- abort"; exit 1; }
    if python3 "$want" list 2>/dev/null | tr ' ' '\n' | grep -qx "$m"; then
        :
    else
        #  mutants8b.py and mutants14.py predate the `list' action, so absence of a list is NOT a failure --
        #  but a WRONG dispatch is.  Fall back to grepping the mutator's own M dict for the name.
        grep -q "\"$m\":" "$want" || { echo "MAP WRONG: $m not known to $(basename "$want") -- abort"; exit 1; }
    fi
done
echo "MAP OK -- every leg is known to the mutator it is dispatched to"

cd "$C" || { echo "clone $C missing -- abort"; exit 1; }
if [ -e .MUTANT ]; then echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; fi
cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN" || { echo "clone differs from SEC -- abort"; exit 1; }
echo "$F  #529 kill table 12 (repair 14) -- restore from GXEMUL-SEC, then REBUILD" > .MUTANT

build() {
    rm -f src/devices/dev_sgi_ip32.o
    nice -n 19 make -j2 > "$A/builds/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1"
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
    MUT=$(mutof "$m")
    python3 "$MUT" "$m" "$SEC/$F" "$F" || { echo "APPLY FAILED $m"; continue; }
    diff -u "$SEC/$F" "$F" > "$A/mutants/$m.diff"
    if [ "$m" = base ]; then
        cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN after applying base" \
            || { echo "base is not a no-op -- abort"; restore; exit 1; }
    fi
    if build "$m"; then OK="$OK $m"; else echo "NOTE $m DID NOT BUILD -- recorded as a RESULT, not retried"; fi
done
restore || exit 1
cmp -s "$B/base" "$B/restored" && echo "restored == base (byte-identical)" || echo "NOTE restored differs from base"
for m in $OK; do
    [ "$m" = base ] && continue
    cmp -s "$B/base" "$B/$m" && echo "NOTE $m BINARY IDENTICAL TO base -- EQUIVALENT MUTANT"
done
echo "BUILDS DONE ($OK) $(date '+%F %T')"

#  ---- CROSS-CHECK every rebuilt edit against the diff the earlier passes PRESERVED, where one exists.
#  ---- A re-derivation that silently differs would make this table a measurement of something else.
echo "--- cross-check rebuilt edits against preserved diffs ---"
for m in $LIST; do
    [ "$m" = base ] && continue
    old=""
    [ -f "$C8/mutants/$m.diff" ]             && old="$C8/mutants/$m.diff"
    [ -f "$A/opus_pass1_work/mutants/$m.diff" ] && old="$A/opus_pass1_work/mutants/$m.diff"
    [ -f "$A/opus_adj_work/mutants/$m.diff" ]   && old="$A/opus_adj_work/mutants/$m.diff"
    if [ -z "$old" ]; then echo "  $m NO PRESERVED DIFF (new to this table)"; continue; fi
    grep '^[+-][^+-]' "$A/mutants/$m.diff" > /tmp/r14_new.hunk
    grep '^[+-][^+-]' "$old"               > /tmp/r14_old.hunk
    if cmp -s /tmp/r14_new.hunk /tmp/r14_old.hunk; then echo "  $m EDIT IDENTICAL to the earlier pass"
    else echo "  *** $m EDIT DIFFERS ***"; diff -u /tmp/r14_old.hunk /tmp/r14_new.hunk; fi
done

#  ---- probe: four lanes ----
leg() {
    for m in "$@"; do
        case " $OK " in *" $m "*) ;; *) echo "$m SKIPPED (no build)"; continue;; esac
        log="$A/logs/probe_$m.raw"
        python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1
        echo "$m $(grep '^CRIMEP_RESULT=' "$log") $(grep '^CRIMEP_CONTROL=' "$log") done=$(grep -c '^CRIMEP_DONE' "$log") FAILING:$(grep '^FAILING:' "$log" | cut -c9-)"
    done
}
L0=(); L1=(); L2=(); L3=(); i=0
for m in $LIST; do
    case $((i % 4)) in 0) L0+=("$m");; 1) L1+=("$m");; 2) L2+=("$m");; 3) L3+=("$m");; esac; i=$((i + 1))
done
leg "${L0[@]}" > "$A/logs/lane0.out" 2>&1 &
leg "${L1[@]}" > "$A/logs/lane1.out" 2>&1 &
leg "${L2[@]}" > "$A/logs/lane2.out" 2>&1 &
leg "${L3[@]}" > "$A/logs/lane3.out" 2>&1 &
wait
echo "==== TABLE 12 RESULTS ===="
cat "$A/logs/lane0.out" "$A/logs/lane1.out" "$A/logs/lane2.out" "$A/logs/lane3.out"
echo "--- mechanical scoring against PRETABLE 12 ---"
python3 "$A/check_pred.py" 2>&1 | tee "$A/check_pred.out"
echo "KILL529R14_DONE $(date '+%F %T')"
