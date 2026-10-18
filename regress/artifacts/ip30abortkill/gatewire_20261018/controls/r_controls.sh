#!/bin/bash
# r_controls.sh <out dir> -- section R (check_probe_wiring.py) controls for #566, modelled on #565's.  Legs:
#   G   commit checker (tuple deleted) + wired gate          -> PASS
#   S   HEAD checker   (tuple kept)    + wired gate          -> FAIL naming ip30_abort (STALE EXEMPTION)
#   G1  as G with --today 2026-10-31                         -> no ip30_abort line (other expiries red; named)
#   U   commit checker (tuple deleted) + exec line commented -> FAIL naming ip30_abort (UNWIRED DETECTOR)
#   H0  HEAD checker   (tuple kept)    + exec line commented -> PASS (the exemption still covers it today)
#   H1  as H0 with --today 2026-10-31                        -> FAIL naming ip30_abort (the cliff #566 discharges)
# The exec line is commented IN PLACE for U/H0/H1 and restored by a trap; the restore is verified by cmp against a
# backup taken first, so a crash cannot leave the gate mutant unnoticed.
set -u
OUT=$1; mkdir -p "$OUT"
R=/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
P=/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/w566
NEW=$(cygpath -w "$P/check_probe_wiring.py"); OLD=$(cygpath -w "$P/check_probe_wiring.HEAD.py"); RG=$(cygpath -w "$R/regress")
G=$R/regress/gate_arm.sh; BK=$OUT/gate_arm.sh.bak
git -C "$R" diff --cached --quiet || { echo "ABORT: the real index has staged changes"; exit 9; }
echo "commit checker md5 $(md5sum < "$P/check_probe_wiring.py" | cut -c1-32); HEAD checker md5 $(md5sum < "$P/check_probe_wiring.HEAD.py" | cut -c1-32)"
git -C "$R" show HEAD:tools/pipeline/check_probe_wiring.py | cmp -s - "$P/check_probe_wiring.HEAD.py" && echo "HEAD checker == git show HEAD:" || { echo "ABORT: HEAD checker copy differs"; exit 9; }
echo "gate_arm.sh md5 $(md5sum < "$G" | cut -c1-32)"
cp "$G" "$BK"
run() { # run <label> <checker> [extra args]
    local lab=$1 chk=$2; shift 2
    ( cd "$R/regress" && python "$chk" --regress "$RG" "$@" ) > "$OUT/R_$lab.out" 2>&1
    local rc=$?
    printf '%-4s rc=%s  last: %s\n' "$lab" "$rc" "$(tail -1 "$OUT/R_$lab.out")"
    grep -n 'ip30_abort' "$OUT/R_$lab.out" | grep -v SELFLABEL | head -4 | sed 's/^/        /'
}
run G  "$NEW"
run S  "$OLD"
run G1 "$NEW" --today 2026-10-31
restore() { cp "$BK" "$G"; }
trap restore EXIT INT TERM
n=$(grep -c '^python3 -u artifacts/ip30abortkill/ip30_abort_probe.py "\$PMAX" gate > "\$IP30LOG" 2>&1 || ip30rc=\$?$' "$G")
[ "$n" = 1 ] || { echo "ABORT: exec line matched $n times"; exit 8; }
sed -i 's/^python3 -u artifacts\/ip30abortkill\/ip30_abort_probe.py "\$PMAX" gate/#MUTANT# python3 -u artifacts\/ip30abortkill\/ip30_abort_probe.py "$PMAX" gate/' "$G"
[ "$(grep -c '^#MUTANT# python3 -u artifacts/ip30abortkill/ip30_abort_probe.py' "$G")" = 1 ] || { echo "ABORT: mutation did not land"; exit 7; }
run U  "$NEW"
run H0 "$OLD"
run H1 "$OLD" --today 2026-10-31
restore; trap - EXIT INT TERM
cmp -s "$BK" "$G" && echo "RESTORE: gate_arm.sh cmp-clean against its backup" || echo "RESTORE FAILED"
grep -c '^python3 -u artifacts/ip30abortkill/ip30_abort_probe.py "\$PMAX" gate' "$G" | sed 's/^/RESTORE: exec lines now /'
rm -f "$BK"
echo R_CONTROLS_DONE
