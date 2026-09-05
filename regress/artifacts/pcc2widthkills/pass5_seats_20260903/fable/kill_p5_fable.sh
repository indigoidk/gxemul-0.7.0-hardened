#!/bin/bash
set -u
G=/mnt/c/DocumentNoSnc/CC/GXEMUL; SEC=$G/GXEMUL-SEC; T=/tmp/gxfable_p5; F=src/devices/dev_pcc2.c
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p5_fable
PROBE=pcc2_width_probe.py
say() { echo "[$(date +%H:%M:%S)] $*"; }
die() { echo "*** ABORT: $*"; exit 9; }
rm -rf "$T"; mkdir -p "$OUT"
cp -a "$G/build" "$T" || die "clone failed"
cmp -s "$T/$F" "$SEC/$F" || { cp "$SEC/$F" "$T/$F"; say "  clone's $F refreshed from SEC"; }
cp "$SEC/regress/$PROBE" "$OUT/frozen_probe.py" || die "cannot freeze probe"
say "  instrument frozen: $(wc -c < "$OUT/frozen_probe.py") bytes  md5 $(md5sum < "$OUT/frozen_probe.py" | cut -c1-8)"
build() { cd "$T" || die cd; rm -f src/devices/dev_pcc2.o; make -j4 > "$OUT/build_$1.log" 2>&1; [ "$T/gxemul" -nt "$T/$F" ] || die "$1: binary not newer than source"; }
score() {
    cd "$SEC/regress" || die cd
    python3 -u "$OUT/frozen_probe.py" "$T/gxemul" "$1" > "$OUT/$1.out" 2>&1
    grep -q PCC2W_PROBE_DONE "$OUT/$1.out" || die "$1: NO COMPLETION SENTINEL"
    say "  $1 [$2]: $(grep -m1 PCC2W_RESULT "$OUT/$1.out")"
    grep -m1 PCC2W_RED "$OUT/$1.out" | sed 's/PCC2W_RED=/      RED: /' || true
}
say "BASE -- 101/101 owed"; build BASE; score BASE CONTROL
say "RESTORE + REBUILD + verify, THEN clear sentinel"
echo "$F  mutant M_TEST_EQ" > "$T/.MUTANT"; cp "$SEC/$F" "$T/$F"
python3 - "$T/$F" <<'PYEOF'
import io, sys
p = sys.argv[1]; s = io.open(p, encoding='utf-8').read()
a = 'd->warned & (1u << bit)'
assert s.count(a) == 1, "TEST anchor count=%d" % s.count(a)
s = s.replace(a, 'd->warned == (1u << bit)')
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
PYEOF
cmp -s "$T/$F" "$SEC/$F" && die "M_TEST_EQ: file UNCHANGED"
say "    [M_TEST_EQ] mutant text: $(grep -c 'd->warned == (1u' "$T/$F") eqtest, $(grep -c 'd->warned & (1u' "$T/$F") andtest"
build M_TEST_EQ
say "    [M_TEST_EQ] binary $(date -r "$T/gxemul" +%H:%M:%S)  source $(date -r "$T/$F" +%H:%M:%S)"
score M_TEST_EQ "predict latch aba 3 RED"
cp "$SEC/$F" "$T/$F"; cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel KEPT"
build restore; rm -f "$T/.MUTANT"; say "  restored + REBUILT + verified, sentinel cleared"
say "KILL_P5_FABLE_DONE"
