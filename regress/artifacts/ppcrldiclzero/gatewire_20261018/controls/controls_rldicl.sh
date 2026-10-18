#!/bin/bash
# controls_rldicl.sh <file holding the block> <green log> [<pre-fix log>] -- negative control 3 (and 2) for the rldicl
# gate block: its SCORING text (everything after the probe's exec line) is extracted from the file named -- the same
# text that ships -- and evaluated against doctored copies of a green log.  Each variant must red exactly the checks
# that should catch it.  check/count/note mirror regress/lib.sh's semantics (exact compare; grep -ac; print).
set -u
BLOCK=$1; GREEN=$2; PRE=${3:-}
W=$(mktemp -d)
awk '/python3 -u ppc_rldicl_probe.py/{on=1; next} on{print} on && /^fi$/{exit}' "$BLOCK" > "$W/score.sh"
[ -s "$W/score.sh" ] && grep -q '^fi$' "$W/score.sh" || { echo "EXTRACT FAILED"; exit 9; }
count() { [ -f "$1" ] || { echo 0; return; }; local c; c=$(grep -ac -- "$2" "$1" 2>/dev/null); echo "${c:-0}"; }
check() { _checks=$((_checks+1)); [ "$2" = "$3" ] || { _fails=$((_fails+1)); _red="$_red [$1 got=$2]"; }; }
note() { :; }
run() {   # run <label> <log> <expected fails>
    RLCLOG=$2; _checks=0; _fails=0; _red=""
    . "$W/score.sh"
    local v="ok"; [ "$_fails" = "$3" ] || v="UNEXPECTED"
    printf '%-34s checks=%-3s fails=%-2s want=%-2s %s%s\n' "$1" "$_checks" "$_fails" "$3" "$v" "$_red"
}
G=$W/g.log; cp "$GREEN" "$G"
mk() { cp "$G" "$W/$1.log"; }
mk v1;  sed -i '/^PPC_RLDICL_PROBE_DONE$/d' "$W/v1.log"
mk v2;  echo PPC_RLDICL_PROBE_DONE >> "$W/v2.log"
mk v3;  sed -i 's/^live  /livex /' "$W/v3.log"
mk v4;  sed -i '/^census zero /s/ ok$/ FAIL/' "$W/v4.log"
mk v5;  sed -i '/^census zero /d' "$W/v5.log"
mk v6;  sed -i '/^SCORE /i stray line that ends ok' "$W/v6.log"
mk v7;  grep '^census zero ' "$G" > "$W/dup"; sed -i "/^SCORE /e cat $W/dup" "$W/v7.log"
mk v8;  sed -i '/^SCORE /d' "$W/v8.log"
mk v9;  sed -i 's/^SCORE 24\/24 /SCORE 23\/24 /' "$W/v9.log"
mk v10; grep '^SCORE ' "$G" >> "$W/v10.log"
mk v11; echo 'SCORE 0/24  elapsed=0.0s  binary=x  label=y' >> "$W/v11.log"
run "V0  green log"                    "$G"          0
run "V1  DONE removed"                 "$W/v1.log"   1
run "V2  DONE duplicated"              "$W/v2.log"   1
run "V3  one row renamed"              "$W/v3.log"   1
run "V4  one row ok -> FAIL"           "$W/v4.log"   3
run "V5  one row deleted (23 rows)"    "$W/v5.log"   3
run "V6  stray line ending ok"         "$W/v6.log"   2
run "V7  one row duplicated"           "$W/v7.log"   3
run "V8  SCORE removed"                "$W/v8.log"   2
run "V9  SCORE 23/24"                  "$W/v9.log"   1
run "V10 valid SCORE duplicated"       "$W/v10.log"  2
run "V11 contradictory SCORE appended" "$W/v11.log"  1
if [ -n "$PRE" ]; then
    RLCLOG=$PRE; _checks=0; _fails=0; _red=""; . "$W/score.sh"
    printf '%-34s checks=%-3s fails=%-2s want=>0 %s\n' "V12 PRE-FIX binary's log" "$_checks" "$_fails" \
        "$([ "$_fails" -gt 0 ] && echo ok || echo UNEXPECTED)"
    echo "     red:$_red"
fi
rm -rf "$W"
echo CONTROLS_DONE
