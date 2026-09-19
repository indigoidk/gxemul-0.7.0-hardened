#!/bin/bash
#  #536 gate_arm.sh sections: a DRY RUN of their check expressions against prepared logs, using
#  a COPY of lib.sh's check/count.  Runs NO probe and NO emulator: the two `python3 -u <probe>`
#  lines are removed from the extracted text and each log is supplied instead.
#  Also: Q2(c)'s full link error, and Q2(e)'s mechanism (subprocess.run on argv[0]="gate").
set -u
ROOT=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$ROOT/GXEMUL-SEC
FROZ=$ROOT/_scratchpad/p2_536_537/frozen
OPUS=$ROOT/_scratchpad/p2_536_537/opus5
T536=$ROOT/_scratchpad/t536
OUT=$OPUS/out/sections
W=/tmp/gxopus536p2/sections
rm -rf "$OUT" "$W"; mkdir -p "$OUT" "$W"
S=$OUT/SUMMARY.txt
say() { echo "$*" | tee -a "$S"; }

#  ---- extract the two sections, by anchor, from the FROZEN staged gate_arm.sh ----
A=$(grep -n 'mk48nvramkill (#521) + #536' "$FROZ/gate_arm.staged.sh" | cut -d: -f1)
Z=$(grep -n 'check "hpcmips ctor verdict"' "$FROZ/gate_arm.staged.sh" | cut -d: -f1)
say "section lines $A..$((Z+1)) of the frozen gate_arm.staged.sh"
sed -n "${A},$((Z+1))p" "$FROZ/gate_arm.staged.sh" > "$W/sections.raw.sh"
say "probe invocations removed: $(grep -c '^python3 -u ' "$W/sections.raw.sh")"
grep -v '^python3 -u ' "$W/sections.raw.sh" | grep -v '^MK48LOG=\|^HPCLOG=' > "$W/sections.sh"
tail -1 "$W/sections.sh" | grep -q '^fi$' && say "extracted text ends at the hpcmips section's closing fi"

run_sections() {  # tag mk48log hpclog
    (
        export LOGDIR=$W/logdir; mkdir -p "$LOGDIR"
        . "$SEC/regress/lib.sh"
        MK48LOG=$2; HPCLOG=$3; PMAX=/nonexistent
        . "$W/sections.sh"
        echo "SECTIONS: $_checks checks, $_fails failed"
    ) > "$OUT/run_$1.txt" 2>&1
    say "  [$1] $(tail -1 "$OUT/run_$1.txt")"
    grep -E 'FAIL' "$OUT/run_$1.txt" | grep -v '^SECTIONS' | sed 's/^/        /' | tee -a "$S"
}

#  ---- the logs ----
cp "$T536/mk48_nvram.log" "$W/mk48.flipped.log"
cp "$T536/hpcmips_ctor.log" "$W/hpc.flipped.log"
say "t536 logs (the brief's dry-run inputs) carry these non-ok lines:"
grep -nE ' FAIL$|\[FAIL\]|_FAIL$' "$W/mk48.flipped.log" "$W/hpc.flipped.log" | sed 's/^/    /' | tee -a "$S"
#  Reconstruct the unflipped logs: exactly the flipped lines restored, verified by counting.
sed -E '/^live /s/ FAIL$/ ok/' "$W/mk48.flipped.log" > "$W/mk48.green.log"
sed -E 's/^  \[FAIL\] S1 /  [ok] S1 /; s/^HPCMIPS_CTOR_FAIL$/HPCMIPS_CTOR_PASS/' "$W/hpc.flipped.log" > "$W/hpc.green.log"
say "reconstruction: mk48 lines changed $(diff "$W/mk48.flipped.log" "$W/mk48.green.log" | grep -c '^>'), hpc lines changed $(diff "$W/hpc.flipped.log" "$W/hpc.green.log" | grep -c '^>')"

say "=== dry run: reconstructed GREEN logs (want 93 checks, 0 failed) ==="
run_sections green "$W/mk48.green.log" "$W/hpc.green.log"
say "=== dry run: the t536 FLIPPED logs as they sit on disk ==="
run_sections flipped "$W/mk48.flipped.log" "$W/hpc.flipped.log"

say "=== Q2(e): what the probe does with argv[1]='gate' (mechanism only; the probe itself is NOT run) ==="
#  mk48_nvram_probe.py: BIN = sys.argv[1]; session() calls subprocess.run([BIN, ...]) and catches ONLY
#  TimeoutExpired.  Reproduce that one call, with the same argv shape, in isolation.
python3 - > "$W/mk48.e.log" 2>&1 <<'PYEOF'
import subprocess, sys
BIN = "gate"
print("mk48nvramkill RUNG-3 WITNESS -- binary=%s label=%s" % (BIN, "local"))
try:
    p = subprocess.run([BIN, "-V", "-x", "-E", "mvme88k", "-e", "mvme187", "-M", "64", "0x10000:/dev/null"],
                       input=b"quit\n", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=5)
except subprocess.TimeoutExpired:
    print("TIMEOUT")
PYEOF
say "  rc of the isolated call: $? ; last line: $(tail -1 "$W/mk48.e.log")"
say "  sentinel present: $(grep -c MK48_WITNESS_DONE "$W/mk48.e.log")"
run_sections e_nopmax "$W/mk48.e.log" "$W/hpc.green.log"

say "=== Q2(c): the full link error when dev_footbridge.o stays in the object list ==="
M=/tmp/gxopus536p2/armtree
OBJS_WITHFB=$(find "$SEC/../build/src" -name '*.o' ! -name 'main.o' 2>/dev/null | sort | tr '\n' ' ')
( cd "$M/regress" && gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -I../src -I../src/include -I../src/include/thirdparty \
    -ffunction-sections -fdata-sections -Wl,--gc-sections -std=gnu99 -I../src/include -I../src/include/thirdparty -I../src/devices \
    $OBJS_WITHFB -L/usr/X11R6/lib -lX11 -o "$W/fb_withfb" diff_fbpending_bound.c -lm ) > "$OUT/Qc_link.txt" 2>&1
say "  rc=$?  multiple-definition lines: $(grep -c 'multiple definition' "$OUT/Qc_link.txt")"
grep 'multiple definition' "$OUT/Qc_link.txt" | sed -E 's/.*multiple definition of/multiple definition of/' | sort -u | head -8 | sed 's/^/    /' | tee -a "$S"
say "SECTIONS_DONE"
