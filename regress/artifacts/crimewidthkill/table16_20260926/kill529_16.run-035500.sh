#!/bin/bash
# kill529_16.sh -- #529 KILL TABLE 16: repair 16 (the HARD_RESET residue pair; the CONTROL arm's class closure), against
#   TWENTY-FIVE legs across SEVEN frozen mutators: table 14's eighteen, the L2 cell (H_noresetclear), the new halt row's
#   channel check (S_rst8clr), the disclosed sibling (E_noendianclear), and four measured deltas for the F2 rule
#   questions (W_istlb, W_imklb, L_dogclr, L_rstclr).  PRETABLE16.out and check16.py were written FIRST.
#
#   *** LAUNCH FROM A FROZEN COPY (cp kill529_16.sh kill529_16.run-<stamp>.sh) AND WITH run_in_background. ***
#   *** NOTHING ELSE CPU-HEAVY WHILE IT RUNS (the probe carries wall-clock rows). ***
#   SCRATCH CLONE /tmp/gxopus_r14 ONLY.  No project tree is written except this artifacts directory.
#   usage: kill529_16.run-<stamp>.sh [NLANES]   (default 4)
set -u
NL=${1:-4}
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/table16_20260926
R14=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/repair14_20260916
T13A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/table13a_20260925
T14=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/table14_20260926
T15A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/table15a_20260926
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus_r14
B=/tmp/gxopus_r14_bins16
F=src/devices/dev_sgi_ip32.c
PROBE=$A/crime_width_probe.table16.py
M_8B=$R14/mutants8b.frozen.py
M_14=$R14/mutants14.frozen.py
M_ADJ=$R14/mutants_adj.frozen.py
M_R14=$R14/mutants_r14.frozen.py
M_13A=$T14/mutants_13a.frozen.py
M_14B=$T14/mutants_14b.frozen.py
M_16=$A/mutants_16.frozen.py

LIST="base G_glm_tim4clear G_clr_ist4r G_clr_ctl4r G_clr_imk4r G_lane_ctl K_ctl4w_reset_post \
K_ctl8w_reset_post M1_gotolatch M2_ld278clr M3_timelatch M4_timeplain M5_revlatch M6_istlatch W_ctl8w \
M7_intmasklatch M8_ctllatch D_nodogclear H_noresetclear S_rst8clr E_noendianclear W_istlb W_imklb L_dogclr L_rstclr"

echo "KILL529_16_START $(date '+%F %T') lanes=$NL"
mkdir -p "$B" "$A/logs" "$A/builds" "$A/mutants"

#  ---- freeze the new mutator, and PROVE the instrument is the one PRETABLE16.out names ----
cp "$A/mutants_16.py" "$M_16"
md5sum "$PROBE" "$M_8B" "$M_14" "$M_ADJ" "$M_R14" "$M_13A" "$M_14B" "$M_16" "$SEC/$F" | tee "$A/logs/INSTRUMENT.md5"
want_md5() { case "$(md5sum "$1" | cut -c1-8)" in "$2") return 0;; *) echo "INSTRUMENT MISMATCH: $1 is not $2 -- abort"; return 1;; esac; }
want_md5 "$PROBE" 5f770991 && want_md5 "$M_8B" ed69e4ed && want_md5 "$M_14" 8da33e01 && want_md5 "$M_ADJ" 712d236c \
    && want_md5 "$M_R14" 1e701d38 && want_md5 "$M_13A" 03c2b95e && want_md5 "$M_14B" 17669e44 \
    && want_md5 "$M_16" 8fb8c068 && want_md5 "$SEC/$F" 8c1d1545 || exit 1
echo "INSTRUMENT OK -- probe 5f770991, seven mutators, source 8c1d1545, as PRETABLE16.out names them"

mutof() {
    case "$1" in
        base|G_glm_tim4clear|G_clr_ist4r|G_clr_ctl4r|G_clr_imk4r|G_lane_ctl|K_ctl4w_reset_post|K_ctl8w_reset_post)
            echo "$M_8B";;
        M1_gotolatch|M2_ld278clr|M3_timelatch|M4_timeplain) echo "$M_14";;
        M5_revlatch|M6_istlatch)                            echo "$M_ADJ";;
        W_ctl8w)                                            echo "$M_R14";;
        M7_intmasklatch|M8_ctllatch)                        echo "$M_13A";;
        D_nodogclear)                                       echo "$M_14B";;
        H_noresetclear|S_rst8clr|E_noendianclear|W_istlb|W_imklb|L_dogclr|L_rstclr) echo "$M_16";;
        *) echo ""; return 1;;
    esac
}
echo "--- leg -> mutator map, re-derived at run time ---"
for m in $LIST; do
    want=$(mutof "$m") || { echo "NO MUTATOR FOR $m -- abort"; exit 1; }
    if python3 "$want" list 2>/dev/null | tr ' ' '\n' | grep -qx "$m"; then
        :
    else
        grep -q "\"$m\"" "$want" || { echo "MAP WRONG: $m not known to $(basename "$want") -- abort"; exit 1; }
    fi
done
echo "MAP OK -- every leg is known to the mutator it is dispatched to"

cd "$C" || { echo "clone $C missing -- abort"; exit 1; }
if [ -e .MUTANT ]; then echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; fi
cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN" || { echo "clone differs from SEC -- abort"; exit 1; }
echo "$F  #529 kill table 16 (repair 16) -- restore from GXEMUL-SEC, then REBUILD" > .MUTANT

#  the conservative clean-build precaution, once, before the base leg
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

echo "--- cross-check rebuilt edits against preserved diffs ---"
for m in $LIST; do
    [ "$m" = base ] && continue
    old=""
    [ -f "$R14/mutants/$m.diff" ]  && old="$R14/mutants/$m.diff"
    [ -f "$T13A/mutants/$m.diff" ] && old="$T13A/mutants/$m.diff"
    [ -f "$T14/mutants/$m.diff" ]  && old="$T14/mutants/$m.diff"
    [ -f "$T15A/mutants/$m.diff" ] && old="$T15A/mutants/$m.diff"
    if [ -z "$old" ]; then echo "  $m NO PRESERVED DIFF (new to this table)"; continue; fi
    grep '^[+-][^+-]' "$A/mutants/$m.diff" > /tmp/t16_new.hunk
    grep '^[+-][^+-]' "$old"               > /tmp/t16_old.hunk
    if cmp -s /tmp/t16_new.hunk /tmp/t16_old.hunk; then echo "  $m EDIT IDENTICAL to $(basename "$(dirname "$(dirname "$old")")")"
    else echo "  *** $m EDIT DIFFERS ***"; diff -u /tmp/t16_old.hunk /tmp/t16_new.hunk; fi
done

leg() {
    for m in "$@"; do
        case " $OK " in *" $m "*) ;; *) echo "$m SKIPPED (no build)"; continue;; esac
        log="$A/logs/probe_$m.raw"
        python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1
        echo "$m $(grep '^CRIMEP_RESULT=' "$log") $(grep '^CRIMEP_CONTROL=' "$log") done=$(grep -c '^CRIMEP_DONE' "$log") FAILING:$(grep '^FAILING:' "$log" | cut -c9-) $(date '+%T')"
    done
}
declare -a LANE
i=0
for m in $LIST; do k=$((i % NL)); LANE[$k]="${LANE[$k]:-} $m"; i=$((i + 1)); done
echo "PROBES START $(date '+%F %T')"
for ((k = 0; k < NL; k++)); do
    # shellcheck disable=SC2086
    leg ${LANE[$k]} > "$A/logs/lane$k.out" 2>&1 &
done
wait
echo "==== TABLE 16 RESULTS ===="
for ((k = 0; k < NL; k++)); do cat "$A/logs/lane$k.out"; done
echo "--- mechanical scoring against PRETABLE16 ---"
python3 "$A/check16.py" 2>&1 | tee "$A/check16.out"
echo "KILL529_16_DONE $(date '+%F %T')"
