#!/bin/bash
#  insitu567.sh -- F2's G4: gate 16 run IN SITU -- the real gate_mips_folds.sh, its launch line, lib.sh's check(), the
#  exit status, and #549's probe running beside #567's -- once on the gate's DEFAULT binary (build/gxemul, which holds the
#  fix: expect PASS, rc 0) and once on HEAD's binary (PMAX=/tmp/gx566/gxemul: expect FAIL, rc 1, #567's block red).
#  LOGDIR in scratch, so the battery's /tmp/gxregress is untouched.  Mutates nothing.
set -u
R=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
G=$R/regress/gate_mips_folds.sh
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbcmd
OUT=$S/insitu
mkdir -p "$OUT"
: > "$OUT/INSITU.log"
say() { echo "$*" | tee -a "$OUT/INSITU.log"; }
B=/mnt/c/DocumentNoSnc/cc/GXEMUL/build
say "INSITU start $(date '+%F %T')"
say "build/: $(cmp -s $B/src/devices/dev_fbctrl.c $R/src/devices/dev_fbctrl.c && echo 'part 1 ok' || echo 'part 1 DIVERGENT')," \
    "$([ $B/gxemul -nt $B/src/devices/dev_fbctrl.c ] && echo 'part 2 ok' || echo 'part 2 STALE');" \
    "/tmp/gx566: $(cmp -s /tmp/gx566/src/devices/dev_fbctrl.c $S/dev_fbctrl.head.c && echo 'HEAD source' || echo 'NOT HEAD'), " \
    "$([ /tmp/gx566/gxemul -nt /tmp/gx566/src/devices/dev_fbctrl.c ] && echo 'binary fresh' || echo 'binary STALE')"
say "probe in the tree: $(md5sum < $R/regress/fbctrl_cmd_probe.py | cut -c1-32); gate: $(md5sum < $G | cut -c1-32)"
for leg in fix head; do
    L=/tmp/gx567insitu_$leg
    rm -rf "$L"
    say "=== $leg $(date '+%T')"
    if [ "$leg" = fix ]; then
        ( unset PMAX; LOGDIR=$L bash "$G" ) > "$OUT/gate16_$leg.out" 2>&1
    else
        PMAX=/tmp/gx566/gxemul LOGDIR=$L bash "$G" > "$OUT/gate16_$leg.out" 2>&1
    fi
    rc=$?
    say "$leg: gate rc=$rc; $(grep -a 'gate 16: MIPS fold witness (#388): \(PASS\|FAIL\|SKIP\)' "$OUT/gate16_$leg.out" | tail -1)"
    say "$leg: fbctrl_cmd checks $(grep -ac 'fbctrl_cmd\|fbctrl command probe' "$OUT/gate16_$leg.out"), of them FAIL $(grep -a 'fbctrl_cmd\|fbctrl command probe' "$OUT/gate16_$leg.out" | grep -ac FAIL)"
    cp "$L/fbctrl_cmd_probe.log" "$OUT/fbctrl_cmd_probe_$leg.log" 2>/dev/null
    cp "$L/fbctrl_port_probe.log" "$OUT/fbctrl_port_probe_$leg.log" 2>/dev/null
done
say "INSITU end $(date '+%F %T')"
say INSITU_DONE
