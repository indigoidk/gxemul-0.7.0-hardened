#!/bin/bash
#  legb531.sh -- #531's clause (b) leg, measured at ip30abortkill's closure (2026-10-18): the removed fatal()+abort()
#  pair re-inserted VERBATIM at each fixed site of HEAD's dev_sgi_ip30.c (mutant_b_dev_sgi_ip30.c.txt), built in the
#  scratch clone /tmp/gx566 (at HEAD, both clearance parts verified before this run), the shipped 33-row probe run
#  against it, the log scored by gate 14's own block text, then the clone restored to HEAD, rebuilt, and both parts
#  re-verified before its sentinel is cleared.  build/ is not touched.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
O=$SEC/regress/artifacts/ip30abortkill/close_20261018
H=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/c531
C=/tmp/gx566
F=src/devices/dev_sgi_ip30.c
echo "LEGB start $(date '+%F %T')"
[ -e "$C/.MUTANT" ] && { echo "clone already carries a sentinel -- stop"; exit 9; }
cmp -s "$H/head_dev_sgi_ip30.c" "$C/$F" || { echo "clone's $F is not HEAD -- stop"; exit 9; }
echo "SCRATCH CLONE (#531 closure): $F carries the clause (b) mutant" > "$C/.MUTANT"
cp "$O/mutant_b_dev_sgi_ip30.c.txt" "$C/$F"
build() {
    (cd "$C" && rm -f src/cpus/*.o src/devices/dev_sgi_ip30.o && make -j4 > "$O/build_$1.log" 2>&1)
    echo "make rc=$? ($1)"
    [ "$C/gxemul" -nt "$C/$F" ] || { echo "BINARY NOT NEWER THAN $F ($1) -- stop, sentinel kept"; exit 9; }
    echo "binary fresh ($1): md5 $(md5sum < "$C/gxemul" | cut -c1-32)"
}
build mutant_b
echo "probe md5 $(md5sum < "$SEC/regress/artifacts/ip30abortkill/ip30_abort_probe.py" | cut -c1-32)"
t0=$(date +%s)
(cd "$SEC/regress" && timeout 1500 python3 -u artifacts/ip30abortkill/ip30_abort_probe.py "$C/gxemul" clause_b > "$O/probe_b.log" 2>&1)
prc=$?
echo "probe b: rc=$prc $(( $(date +%s) - t0 ))s  $(grep -a '^IP30ABORT_RESULT=' "$O/probe_b.log") last=[$(tail -1 "$O/probe_b.log")]"
T=$(mktemp -d)
awk '/python3 -u artifacts\/ip30abortkill\/ip30_abort_probe.py/{on=1; next} on{print} on && /^fi$/{exit}' "$SEC/regress/gate_arm.sh" > "$T/score.sh"
grep -q '^fi$' "$T/score.sh" || { echo "EXTRACT FAILED"; exit 9; }
echo "gate_arm.sh md5 $(md5sum < "$SEC/regress/gate_arm.sh" | cut -c1-32), scoring text md5 $(md5sum < "$T/score.sh" | cut -c1-32)"
count() { [ -f "$1" ] || { echo 0; return; }; local c; c=$(grep -ac -- "$2" "$1" 2>/dev/null); echo "${c:-0}"; }
check() { _checks=$((_checks+1)); [ "$2" = "$3" ] || { _fails=$((_fails+1)); _red="$_red [$1 got=$2]"; }; }
note() { :; }
IP30LOG=$O/probe_b.log; ip30rc=$prc; _checks=0; _fails=0; _red=""
. "$T/score.sh" > /dev/null 2>&1
echo "LEG b  gate checks=$_checks fails=$_fails $([ "$_fails" -gt 0 ] && echo 'RED (clause b holds)' || echo 'GREEN (CLAUSE B BREACH)')"
echo "     red:$_red"
rm -rf "$T"
echo "--- restore"
cp "$H/head_dev_sgi_ip30.c" "$C/$F"
build restore
cmp -s "$H/head_dev_sgi_ip30.c" "$C/$F" && echo "part 1: $F == HEAD" || { echo "part 1 FAILED -- sentinel kept"; exit 9; }
[ "$C/gxemul" -nt "$C/$F" ] && echo "part 2: binary newer than $F" || { echo "part 2 FAILED -- sentinel kept"; exit 9; }
rm -f "$C/.MUTANT"; echo "sentinel cleared"
echo "LEGB end $(date '+%F %T')"
echo LEGB_DONE
