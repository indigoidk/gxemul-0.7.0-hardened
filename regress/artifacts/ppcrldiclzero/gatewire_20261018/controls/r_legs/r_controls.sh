#!/bin/bash
# r_controls.sh <out dir> -- section R (check_probe_wiring.py) controls for #565.  Legs:
#   G   commit checker  (tuple deleted)  + wired gate          -> PASS
#   S   HEAD checker    (tuple kept)     + wired gate          -> FAIL naming ppc_rldicl (STALE EXEMPTION)
#   U   commit checker  (tuple deleted)  + exec line commented -> FAIL naming ppc_rldicl (UNWIRED DETECTOR)
#   H0  HEAD checker    (tuple kept)     + exec line commented -> PASS (the exemption still covers it today)
#   H1  as H0 with --today 2026-10-23                          -> FAIL naming ppc_rldicl (the cliff #565 discharges)
#   G1  as G with --today 2026-10-23                           -> no ppc_rldicl line (other expiries may red; named)
# The exec line is commented IN PLACE for U/H0/H1 and restored by a trap; the restore is verified by cmp against a
# backup taken first AND against the block text, so a crash cannot leave the gate mutant unnoticed.
set -u
OUT=$1; mkdir -p "$OUT"
R=/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
P=/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/ppcw
NEW=$(cygpath -w "$P/cpw_commit.py"); OLD=$(cygpath -w "$P/cpw_head.py"); RG=$(cygpath -w "$R/regress")
G=$R/regress/gate_ppc.sh; BK=$OUT/gate_ppc.sh.bak
git -C "$R" diff --cached --quiet || { echo "ABORT: the real index has staged changes"; exit 9; }
cp "$G" "$BK"
run() { # run <label> <checker> [extra args]
    local lab=$1 chk=$2; shift 2
    ( cd "$R/regress" && python "$chk" --regress "$RG" "$@" ) > "$OUT/R_$lab.out" 2>&1
    local rc=$?
    printf '%-4s rc=%s  last: %s\n' "$lab" "$rc" "$(tail -1 "$OUT/R_$lab.out")"
    grep -n 'ppc_rldicl' "$OUT/R_$lab.out" | head -4 | sed 's/^/        /'
}
run G  "$NEW"
run S  "$OLD"
run G1 "$NEW" --today 2026-10-23
restore() { cp "$BK" "$G"; }
trap restore EXIT INT TERM
n=$(grep -c '^python3 -u ppc_rldicl_probe.py "\$PMAX" gate > "\$RLCLOG" 2>&1 || true$' "$G")
[ "$n" = 1 ] || { echo "ABORT: exec line matched $n times"; exit 8; }
sed -i 's/^python3 -u ppc_rldicl_probe.py "\$PMAX" gate/#MUTANT# python3 -u ppc_rldicl_probe.py "$PMAX" gate/' "$G"
[ "$(grep -c '^#MUTANT# python3 -u ppc_rldicl_probe.py' "$G")" = 1 ] || { echo "ABORT: mutation did not land"; exit 7; }
run U  "$NEW"
run H0 "$OLD"
run H1 "$OLD" --today 2026-10-23
restore; trap - EXIT INT TERM
cmp -s "$BK" "$G" && echo "RESTORE: gate_ppc.sh cmp-clean against its backup" || echo "RESTORE FAILED"
grep -c '^python3 -u ppc_rldicl_probe.py "\$PMAX" gate' "$G" | sed 's/^/RESTORE: exec lines now /'
echo R_CONTROLS_DONE
