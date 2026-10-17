#!/bin/bash
#  The controls' KILL TABLE: every one-edit mutant of the landed launcher (mut_launcher.py) run through run_controls_v2.sh as the
#  AFTER column.  A pinned mutant must turn at least one AFTER expectation red, and it must be the control its line names;
#  an UNPINNED one is measured too, so its escape is a recorded result rather than a guess.
#  Usage: bash run_mutants.sh [launcher]     (default: tools/cxlaunch.sh; writes only to a scratch dir it removes)
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
L="${1:-$REPO/tools/cxlaunch.sh}"
M=$(mktemp -d)
trap 'rm -rf "$M"' EXIT
PYW=$(command -v python || command -v python3)
"$PYW" "$HERE/mut_launcher.py" "$(cygpath -w "$L" 2>/dev/null || echo "$L")" "$(cygpath -w "$M" 2>/dev/null || echo "$M")" || { echo "APPARATUS FAIL: mutant generation"; exit 9; }
echo "# kill table for $L ($(md5sum < "$L" | cut -c1-32)), $(date '+%Y-%m-%d %H:%M:%S')"
CXL_AFTER="$L" bash "$HERE/run_controls_v2.sh" > "$M/base.out" 2>&1
echo "BASE      $(grep '^CONTROLS:' "$M/base.out")"
grep -q 'CXLAND_CONTROLS_DONE' "$M/base.out" && grep -q '^CONTROLS: \([0-9]*\)/\1 ' "$M/base.out" || { echo "APPARATUS FAIL: the base run is not clean"; exit 9; }
ok=0; n=0
while IFS="$(printf '\t')" read -r name catches; do
    CXL_AFTER="$M/$name.sh" bash "$HERE/run_controls_v2.sh" > "$M/$name.out" 2>&1
    tally=$(grep '^CONTROLS:' "$M/$name.out" | cut -d' ' -f2)
    red=$(grep -E '^[A-Z][0-9A-Z]? +after +exit=.*NO$|^[A-Z][0-9A-Z]? +after +.*  NO$' "$M/$name.out" | awk '{print $1}' | sort -u | tr '\n' ' ')
    n=$((n + 1))
    case "$catches" in
        UNPINNED*) verdict=$([ -z "$red" ] && echo "escapes (as recorded)" || echo "CAUGHT by: $red(unexpected)"); [ -z "$red" ] && ok=$((ok + 1)) ;;
        *) miss=""; for c in $catches; do case " $red " in *" $c "*) ;; *) miss="$miss $c";; esac; done
           if [ -n "$red" ] && [ -z "$miss" ]; then verdict="killed by: $red"; ok=$((ok + 1)); else verdict="NOT KILLED as named (red: ${red:-none}; missing:$miss)"; fi ;;
    esac
    printf '%-13s %-8s %-62s %s\n' "$name" "$tally" "$verdict" "[$catches]"
done < "$M/MUTANTS.list"
echo "KILL TABLE: $ok/$n as recorded"
echo "CXLAND_MUTANTS_DONE"
[ "$ok" = "$n" ]
