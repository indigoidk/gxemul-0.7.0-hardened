#!/bin/bash
#  rescore.sh -- re-score the four preserved leg logs (base, prefix, absent, nonemu) with the block's scoring text as it
#  stands NOW in gate_arm.sh, and tie the receipt to the bytes: md5 of the gate file, of the extracted scoring text, and
#  of the probe.  The probe is not re-run: the legs' logs are the measurement; only the scoring text moved (comments).
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
L=$SEC/regress/artifacts/ip30abortkill/gatewire_20261018/legs
T=$(mktemp -d)
awk '/python3 -u artifacts\/ip30abortkill\/ip30_abort_probe.py/{on=1; next} on{print} on && /^fi$/{exit}' "$SEC/regress/gate_arm.sh" > "$T/score.sh"
grep -q '^fi$' "$T/score.sh" || { echo "EXTRACT FAILED"; exit 9; }
echo "gate_arm.sh md5 $(md5sum < "$SEC/regress/gate_arm.sh" | cut -c1-32)"
echo "scoring text: $(wc -l < "$T/score.sh") lines, md5 $(md5sum < "$T/score.sh" | cut -c1-32)"
echo "probe md5 now $(md5sum < "$SEC/regress/artifacts/ip30abortkill/ip30_abort_probe.py" | cut -c1-32) (the legs ran 5bf04f2de35af34d517bd286499d5b98, before #566's docstring note)"
count() { [ -f "$1" ] || { echo 0; return; }; local c; c=$(grep -ac -- "$2" "$1" 2>/dev/null); echo "${c:-0}"; }
check() { _checks=$((_checks+1)); [ "$2" = "$3" ] || { _fails=$((_fails+1)); _red="$_red [$1 got=$2]"; }; }
note() { :; }
for leg in base prefix absent nonemu; do
    IP30LOG=$L/probe_$leg.log; ip30rc=$(cat "$L/probe_$leg.rc"); _checks=0; _fails=0; _red=""
    . "$T/score.sh" > /dev/null 2>&1
    want=$([ "$leg" = base ] && echo GREEN || echo RED); got=$([ "$_fails" -gt 0 ] && echo RED || echo GREEN)
    printf 'LEG %-7s rc=%s gate checks=%-3s fails=%-3s %-5s %s\n' "$leg" "$ip30rc" "$_checks" "$_fails" "$got" "$([ "$got" = "$want" ] && echo "as required" || echo "*** NOT AS REQUIRED ***")"
done
rm -rf "$T"
echo RESCORE_DONE
