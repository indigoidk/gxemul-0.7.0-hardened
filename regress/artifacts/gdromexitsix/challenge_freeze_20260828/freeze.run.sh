#!/bin/bash
#  FREEZE THE CHALLENGE SET for gdromexitsix Round 2, per the ratified STRENGTHENING order:
#  build the probe mutants BEFORE the product edit, measure them CAUGHT on the committed
#  build via the old channel (exit1 -> pty EOF -> alive=False), then edit, then show the
#  SAME mutants STILL caught via the named replacement channel.
#
#  The packet word 0x2030 gives cmd[0]=0x30 (read sectors), cmd[1]=0x20 (the only silently
#  accepted format).  Two mis-assemblies, each one hex digit:
#     0x2031 -> cmd[0]=0x31, unimplemented    -> handle_command's `default:`  -> exit(1) TODAY
#     0x2130 -> cmd[1]=0x21, bad data format  -> the 0x30 arm's format check  -> exit(1) TODAY
#  After Round 2 BOTH decline and survive, so `alive` can no longer tell them from a good run.
R=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$R/GXEMUL-SEC
P=$SEC/regress/gdrom_default_probe.py
K=$R/_images/openbsd76-landisk-bsd.rd
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/40fd4ccc-4c3b-4ad6-91dc-122d039ab5a2/scratchpad/chal
B=$R/build/gxemul

run_one () {   # $1 = label, $2 = packet word
    cp "$P" "$OUT/p_$1.py"
    if [ "$2" != "KEEP" ]; then
        python3 - "$OUT/p_$1.py" "$2" <<'PY'
import sys
p, w = sys.argv[1], sys.argv[2]
s = open(p).read()
old = 'r8=0x2030'
assert s.count(old) == 1, "packet anchor count %d" % s.count(old)
open(p, 'w').write(s.replace(old, 'r8=' + w, 1))
PY
        [ $? -eq 0 ] || { echo "$1  *** PATCH FAILED ***"; return 1; }
    fi
    python3 -u "$OUT/p_$1.py" "$B" "$K" > "$OUT/$1.raw" 2>&1
    local res ctl trip
    res=$(grep -o "GDROM_DEF_RESULT=[0-9]*/[0-9]*" "$OUT/$1.raw" | tail -1 | cut -d= -f2)
    ctl=$(grep -c "GDROM_DEF_CONTROL=OK" "$OUT/$1.raw")
    trip=$(grep -E "^(nodata stale|stale says|stale idle)" "$OUT/$1.raw" | sed 's/  */ /g' | cut -d' ' -f1-4 | tr '\n' '|')
    printf '%-14s %-10s ctlOK=%s\n    triple: %s\n' "$1" "${res:-NONE}" "$ctl" "$trip"
}

echo "=== C0  correct packet (0x2030) -- the baseline the mutants are measured against ==="
run_one C0_correct KEEP
echo "=== C1  cmd[0]=0x31 -> default: arm  (must be CAUGHT today) ==="
run_one C1_badcmd0 0x2031
echo "=== C2  cmd[1]=0x21 -> format check  (must be CAUGHT today) ==="
run_one C2_badcmd1 0x2130
echo FREEZE_DONE
