#!/bin/bash
# nullmedium.sh -- #565's floor clause (c) leg for regress/ppc_rldicl_probe.py, MEASURED rather than claimed by
# construction: the committed probe (as edited by #565 -- comments, plus after pass 2 one printed note string; this
# header said "comment-only" until F2) is run exactly as gate_ppc.sh runs it, against
# two NULL MEDIA -- an ABSENT binary and a NON-EMULATOR binary (/bin/true) -- and each log is then scored by the
# gate block's own scoring text, extracted from regress/gate_ppc.sh (the text that ships).  The clause holds iff
# every leg reds at least one gate check.  Read-only on every tree; writes only into $OUT.
set -u
R=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
OUT=$R/regress/artifacts/ppcrldiclzero/gatewire_20261018/nullmedium
mkdir -p "$OUT"
W=$(mktemp -d)
awk '/python3 -u ppc_rldicl_probe.py/{on=1; next} on{print} on && /^fi$/{exit}' "$R/regress/gate_ppc.sh" > "$W/score.sh"
grep -q '^fi$' "$W/score.sh" || { echo "EXTRACT FAILED"; exit 9; }
count() { [ -f "$1" ] || { echo 0; return; }; local c; c=$(grep -ac -- "$2" "$1" 2>/dev/null); echo "${c:-0}"; }
check() { _checks=$((_checks+1)); [ "$2" = "$3" ] || { _fails=$((_fails+1)); _red="$_red [$1 got=$2]"; }; }
note() { :; }
{
echo "probe: $(md5sum "$R/regress/ppc_rldicl_probe.py" | cut -c1-32)  regress/ppc_rldicl_probe.py"
echo "gate:  $(md5sum "$R/regress/gate_ppc.sh" | cut -c1-32)  regress/gate_ppc.sh"
for leg in absent:/nonexistent/gxemul nonemu:/bin/true; do
    lab=${leg%%:*}; bin=${leg#*:}
    cd "$R/regress" || exit 9
    t0=$(date +%s)
    timeout 300 python3 -u ppc_rldicl_probe.py "$bin" gate > "$OUT/null_$lab.log" 2>&1; prc=$?
    RLCLOG=$OUT/null_$lab.log; _checks=0; _fails=0; _red=""
    tail -5 "$RLCLOG" | sed 's/^/       /' > /dev/null
    . "$W/score.sh" > /dev/null 2>&1
    printf 'LEG %-7s binary=%-20s probe_rc=%-3s %3ss  gate checks=%-3s fails=%-3s %s\n' \
        "$lab" "$bin" "$prc" "$(( $(date +%s) - t0 ))" "$_checks" "$_fails" \
        "$([ "$_fails" -gt 0 ] && echo 'RED (clause c holds)' || echo 'GREEN (CLAUSE C BREACH)')"
    echo "     red:$_red"
    echo "     log tail: $(tail -2 "$RLCLOG" | tr '\n' '|' | cut -c1-200)"
done
} | tee "$OUT/NULLMEDIUM.out"
rm -rf "$W"
echo NULLMEDIUM_DONE | tee -a "$OUT/NULLMEDIUM.out"
