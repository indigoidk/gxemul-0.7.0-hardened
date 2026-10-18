#!/bin/bash
#  run_gate14.sh -- #566's one full gate 14 run before commit, alone, on a HEAD binary: PMAX = the scratch clone
#  /tmp/gx566/gxemul (restored to HEAD and cleared both parts, legs/RESTORE.out), because build/'s binary carries another
#  session's uncommitted sources.  The gate file, the probe and the binary are hashed before and after.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
O=$SEC/regress/artifacts/ip30abortkill/gatewire_20261018/gate14
B=/tmp/gx566/gxemul
LD=/tmp/gx566gate; rm -rf "$LD"; mkdir -p "$LD"
{
echo "gate14 start $(date '+%F %T')"
echo "binary $B md5 $(md5sum < "$B" | cut -c1-32)"
echo "gate_arm.sh md5 $(md5sum < "$SEC/regress/gate_arm.sh" | cut -c1-32)  probe md5 $(md5sum < "$SEC/regress/artifacts/ip30abortkill/ip30_abort_probe.py" | cut -c1-32)"
[ -e /tmp/gx566/.MUTANT ] && echo "*** CLONE SENTINEL PRESENT -- not a HEAD binary" || echo "clone sentinel absent"
} > "$O/RUN.txt"
cd "$SEC/regress" && PMAX="$B" LOGDIR="$LD" bash gate_arm.sh > "$O/gate_arm.out" 2>&1
rc=$?
cp "$LD/ip30_abort.log" "$O/ip30_abort.log" 2>/dev/null
{
echo "gate14 rc=$rc end $(date '+%F %T')"
grep -a 'gate 14:' "$O/gate_arm.out" | tail -1
echo "binary md5 after $(md5sum < "$B" | cut -c1-32)"
echo "ip30_abort checks: $(grep -ac 'ip30_abort' "$O/gate_arm.out") lines; failing: $(grep -a 'ip30_abort' "$O/gate_arm.out" | grep -vc '  ok  ')"
[ "$rc" = 0 ] && grep -aq 'gate 14:.*PASS' "$O/gate_arm.out" && echo GATE14_PASS || echo GATE14_NOT_PASS
} >> "$O/RUN.txt"
cat "$O/RUN.txt"
