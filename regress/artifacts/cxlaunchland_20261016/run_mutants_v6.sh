#!/bin/bash
#  The controls' KILL TABLE, v6: every one-edit mutant of the landed launcher (mut_launcher_v6.py) run through run_controls_v6.sh
#  as the AFTER column (CXL_AFTER_ONLY=1: a mutant changes only that column, so the tracked and before runs are spent once, in
#  the base run).  A mutant must turn at least one AFTER expectation red, and every control its line names must be among the
#  reds.  v5 adds two apparatus checks the v4 driver lacked (GPT-6 Astra, Grok 4.7, v4 pass): EVERY mutant run must carry the
#  controls' completion sentinel and the base run's after-column denominator, or it is reported INCOMPLETE and fails the table;
#  and a red check is read from ANY check line, not only from lines naming `after' (v4's parser dropped E0's red).
#  Mutants run CXL_JOBS at a time (default 4); each control run has its own scratch dir, so they share nothing.
#  Usage: bash run_mutants_v6.sh [launcher]     (default: tools/cxlaunch.sh; writes only to a scratch dir it removes)
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
L="${1:-$REPO/tools/cxlaunch.sh}"
JOBS="${CXL_JOBS:-4}"
#  CXL_CONTROLS names a FROZEN copy of the controls (the carrier's frozen-copy rule: every mutant run re-reads this file)
CTL="${CXL_CONTROLS:-$HERE/run_controls_v6.sh}"
M=$(mktemp -d)
trap 'rm -rf "$M"' EXIT
PYW=$(command -v python || command -v python3)
"$PYW" "$HERE/mut_launcher_v6.py" "$(cygpath -w "$L" 2>/dev/null || echo "$L")" "$(cygpath -w "$M" 2>/dev/null || echo "$M")" || { echo "APPARATUS FAIL: mutant generation"; exit 9; }
echo "# kill table for $L ($(md5sum < "$L" | cut -c1-32)), $(date '+%Y-%m-%d %H:%M:%S'), $JOBS at a time; controls $(md5sum < "$CTL" | cut -c1-32)"
CXL_AFTER="$L" bash "$CTL" > "$M/base.out" 2>&1
echo "BASE      $(grep '^CONTROLS:' "$M/base.out")"
grep -q 'CXLAND_CONTROLS_DONE' "$M/base.out" && grep -q '^CONTROLS: \([0-9]*\)/\1 ' "$M/base.out" || { echo "APPARATUS FAIL: the base run is not clean"; exit 9; }
#  the after-only denominator: the base total less the tracked and before row runs
btotal=$(grep '^CONTROLS:' "$M/base.out" | sed 's/^CONTROLS: [0-9]*\/\([0-9]*\) .*/\1/')
nrows=$(grep -cE '^[A-Z][0-9A-Z]* +after +exit=' "$M/base.out")
want=$((btotal - 2 * nrows))
echo "BASE      $nrows rows; a mutant's after-only run must total $want"
while IFS="$(printf '\t')" read -r name catches; do
    while [ "$(jobs -rp | wc -l)" -ge "$JOBS" ]; do wait -n; done
    CXL_AFTER_ONLY=1 CXL_AFTER="$M/$name.sh" bash "$CTL" > "$M/$name.out" 2>&1 &
done < "$M/MUTANTS.list"
wait
#  v6: the FLAKE re-run.  Under heavy concurrent load a run's first redirect can fail after `mkdir -p' printed nothing -- its
#  log says `stdout= b', the counts EMPTY (Fable 5.1, v5 pass: two in about 2,570 launcher runs, cause NOT established).  A
#  flake only ADDS reds, so it cannot hide a kill, but it can put a spurious name in a "killed by" list: a mutant run carrying
#  the signature is re-run ONCE, alone, and the re-run is the one scored.  A mutant whose own effect is that signature
#  (m_mkdirnop, on MP) shows it again, deterministically.
while IFS="$(printf '\t')" read -r name catches; do
    if grep -qE '^ +codex rc=[0-9]+ +stdout= b' "$M/$name.out"; then
        echo "RERUN     $name (the flake signature in its first run)"
        CXL_AFTER_ONLY=1 CXL_AFTER="$M/$name.sh" bash "$CTL" > "$M/$name.out" 2>&1
    fi
done < "$M/MUTANTS.list"
ok=0; n=0
while IFS="$(printf '\t')" read -r name catches; do
    n=$((n + 1))
    tally=$(grep '^CONTROLS:' "$M/$name.out" | cut -d' ' -f2)
    den=${tally#*/}
    if ! grep -q 'CXLAND_CONTROLS_DONE' "$M/$name.out" || [ "$den" != "$want" ]; then
        printf '%-15s %-8s %-62s %s\n' "$name" "${tally:-none}" "INCOMPLETE run (no sentinel, or a denominator other than $want)" "[$catches]"
        continue
    fi
    #  row names run to four characters (RC1A) and check labels carry lower case (E0b): `[0-9A-Za-z]*'
    red=$(grep -E '^[A-Z][0-9A-Za-z]* +(after|all) .* NO$' "$M/$name.out" | awk '{print $1}' | sort -u | tr '\n' ' ')
    miss=""; for c in $catches; do case " $red " in *" $c "*) ;; *) miss="$miss $c";; esac; done
    if [ -n "$red" ] && [ -z "$miss" ]; then verdict="killed by: $red"; ok=$((ok + 1)); else verdict="NOT KILLED as named (red: ${red:-none}; missing:$miss)"; fi
    printf '%-15s %-8s %-62s %s\n' "$name" "$tally" "$verdict" "[$catches]"
done < "$M/MUTANTS.list"
echo "KILL TABLE: $ok/$n as recorded"
echo "CXLAND_MUTANTS_DONE"
[ "$ok" = "$n" ]
