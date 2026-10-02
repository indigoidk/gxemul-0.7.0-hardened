#!/bin/bash
# kill529_14.sh -- #529 KILL TABLE 14: repair 15 (the TIME/REV latch-SET carriers and the entries-13/17 pair), against
#   EIGHTEEN legs across SIX frozen mutators: every mutant built for #529 since table 12, plus D_nodogclear.
#   PRETABLE14.out and check14.py beside this file were both written FIRST and their mtimes prove it.
#
#   *** LAUNCH FROM A FROZEN COPY (cp kill529_14.sh kill529_14.run-<stamp>.sh) AND WITH run_in_background. ***
#   Bash reads a script incrementally, so editing this file while it runs corrupts the run.
#
#   *** NOTHING ELSE CPU-HEAVY WHILE IT RUNS. ***  The probe carries wall-clock oracles (the `time'/`tl' magnitude rows,
#   `c t4w gap'/`c t4r gap'), and this project has a recorded gate failure from two concurrent CPU-heavy jobs.
#
#   SCRATCH CLONE /tmp/gxopus_r14 ONLY.  No project tree is written except this artifacts directory.
set -u
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/table14_20260926
R14=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/repair14_20260916
T13A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/table13a_20260925
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus_r14
B=/tmp/gxopus_r14_bins14
F=src/devices/dev_sgi_ip32.c
PROBE=$A/crime_width_probe.table14.py
M_8B=$R14/mutants8b.frozen.py
M_14=$R14/mutants14.frozen.py
M_ADJ=$R14/mutants_adj.frozen.py
M_R14=$R14/mutants_r14.frozen.py
M_13A=$A/mutants_13a.frozen.py
M_14B=$A/mutants_14b.frozen.py

LIST="base G_glm_tim4clear G_clr_ist4r G_clr_ctl4r G_clr_imk4r G_lane_ctl K_ctl4w_reset_post \
K_ctl8w_reset_post M1_gotolatch M2_ld278clr M3_timelatch M4_timeplain M5_revlatch M6_istlatch W_ctl8w \
M7_intmasklatch M8_ctllatch D_nodogclear"

echo "KILL529_14_START $(date '+%F %T')"
mkdir -p "$B" "$A/logs" "$A/builds" "$A/mutants"

#  ---- freeze the two mutators that live outside a frozen dir, and PROVE the instrument is the one PRETABLE14 names ----
cp "$T13A/mutants_13a.py" "$M_13A"
cp "$A/mutants_14b.py"    "$M_14B"
md5sum "$PROBE" "$M_8B" "$M_14" "$M_ADJ" "$M_R14" "$M_13A" "$M_14B" "$SEC/$F" | tee "$A/logs/INSTRUMENT.md5"
want_md5() { case "$(md5sum "$1" | cut -c1-8)" in "$2") return 0;; *) echo "INSTRUMENT MISMATCH: $1 is not $2 -- abort"; return 1;; esac; }
want_md5 "$PROBE" f5e915f6 && want_md5 "$M_8B" ed69e4ed && want_md5 "$M_14" 8da33e01 && want_md5 "$M_ADJ" 712d236c \
    && want_md5 "$M_R14" 1e701d38 && want_md5 "$M_13A" 03c2b95e && want_md5 "$M_14B" 17669e44 \
    && want_md5 "$SEC/$F" 8c1d1545 || exit 1
echo "INSTRUMENT OK -- probe f5e915f6, six mutators, source 8c1d1545, as PRETABLE14.out names them"

#  ---- the leg -> mutator map, VERIFIED AT RUN TIME against each mutator's own text ----
mutof() {
    case "$1" in
        base|G_glm_tim4clear|G_clr_ist4r|G_clr_ctl4r|G_clr_imk4r|G_lane_ctl|K_ctl4w_reset_post|K_ctl8w_reset_post)
            echo "$M_8B";;
        M1_gotolatch|M2_ld278clr|M3_timelatch|M4_timeplain) echo "$M_14";;
        M5_revlatch|M6_istlatch)                            echo "$M_ADJ";;
        W_ctl8w)                                            echo "$M_R14";;
        M7_intmasklatch|M8_ctllatch)                        echo "$M_13A";;
        D_nodogclear)                                       echo "$M_14B";;
        *) echo ""; return 1;;
    esac
}
echo "--- leg -> mutator map, re-derived at run time ---"
for m in $LIST; do
    want=$(mutof "$m") || { echo "NO MUTATOR FOR $m -- abort"; exit 1; }
    if python3 "$want" list 2>/dev/null | tr ' ' '\n' | grep -qx "$m"; then
        :
    else
        #  most mutators predate the `list' action; a WRONG dispatch is still caught by the name in the file's text
        grep -q "\"$m\"" "$want" || { echo "MAP WRONG: $m not known to $(basename "$want") -- abort"; exit 1; }
    fi
done
echo "MAP OK -- every leg is known to the mutator it is dispatched to"

cd "$C" || { echo "clone $C missing -- abort"; exit 1; }
if [ -e .MUTANT ]; then echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; fi
cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN" || { echo "clone differs from SEC -- abort"; exit 1; }
echo "$F  #529 kill table 14 (repair 15) -- restore from GXEMUL-SEC, then REBUILD" > .MUTANT

#  the conservative clean-build precaution, once, before the base leg (the carrier: KEEP the rm until depsrm is measured)
rm -f src/cpus/*.o
echo "src/cpus/*.o removed $(date '+%T')"

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

#  ---- CROSS-CHECK every rebuilt edit against the diff its earlier table PRESERVED ----
echo "--- cross-check rebuilt edits against preserved diffs ---"
for m in $LIST; do
    [ "$m" = base ] && continue
    old=""
    [ -f "$R14/mutants/$m.diff" ]  && old="$R14/mutants/$m.diff"
    [ -f "$T13A/mutants/$m.diff" ] && old="$T13A/mutants/$m.diff"
    if [ -z "$old" ]; then echo "  $m NO PRESERVED DIFF (new to this table)"; continue; fi
    grep '^[+-][^+-]' "$A/mutants/$m.diff" > /tmp/t14_new.hunk
    grep '^[+-][^+-]' "$old"               > /tmp/t14_old.hunk
    if cmp -s /tmp/t14_new.hunk /tmp/t14_old.hunk; then echo "  $m EDIT IDENTICAL to $(basename "$(dirname "$(dirname "$old")")")"
    else echo "  *** $m EDIT DIFFERS ***"; diff -u /tmp/t14_old.hunk /tmp/t14_new.hunk; fi
done

#  ---- probe: four lanes (table 12's measured-safe width) ----
leg() {
    for m in "$@"; do
        case " $OK " in *" $m "*) ;; *) echo "$m SKIPPED (no build)"; continue;; esac
        log="$A/logs/probe_$m.raw"
        python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1
        echo "$m $(grep '^CRIMEP_RESULT=' "$log") $(grep '^CRIMEP_CONTROL=' "$log") done=$(grep -c '^CRIMEP_DONE' "$log") FAILING:$(grep '^FAILING:' "$log" | cut -c9-) $(date '+%T')"
    done
}
L0=(); L1=(); L2=(); L3=(); i=0
for m in $LIST; do
    case $((i % 4)) in 0) L0+=("$m");; 1) L1+=("$m");; 2) L2+=("$m");; 3) L3+=("$m");; esac; i=$((i + 1))
done
echo "PROBES START $(date '+%F %T')"
leg "${L0[@]}" > "$A/logs/lane0.out" 2>&1 &
leg "${L1[@]}" > "$A/logs/lane1.out" 2>&1 &
leg "${L2[@]}" > "$A/logs/lane2.out" 2>&1 &
leg "${L3[@]}" > "$A/logs/lane3.out" 2>&1 &
wait
echo "==== TABLE 14 RESULTS ===="
cat "$A/logs/lane0.out" "$A/logs/lane1.out" "$A/logs/lane2.out" "$A/logs/lane3.out"
echo "--- mechanical scoring against PRETABLE14 ---"
python3 "$A/check14.py" 2>&1 | tee "$A/check14.out"
echo "KILL529_14_DONE $(date '+%F %T')"
