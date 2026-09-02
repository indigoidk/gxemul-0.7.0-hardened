#!/bin/bash
#  #500 L2 DISCHARGE.  A repair is discharged by a MEASURED KILL, never by existing.
#
#  A measuring seat swept the 19-row detector 19/19 with one hex digit and measured its
#  own repair in ITS clone with ITS rows.  This reproduces the kill against MY 21-row
#  file, which is the thing that actually ships.
#
#  PREDICTION, written HERE before the run:
#      BASE         21/21
#      M8_maskwide  19/21 -- RED = `acc rect rl' and `acc line se' AND NOTHING ELSE.
#  If any OTHER row reds, my account of the channel is wrong.  If those two do NOT red,
#  the repair is vacuous and the L2 is still open.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
T=/tmp/gx500p
F=src/devices/dev_sgi_re.c
OUT=/tmp/m9
say(){ echo "[$(date +%H:%M:%S)] $*"; }
die(){ say "*** ABORT: $* ***"; exit 1; }

mkdir -p "$OUT"
say "clone + freeze ONE instrument"
rm -rf "$T"; cp -a "$G/build" "$T" || die clone
mkdir -p "$T/rg"
cp "$SEC/regress/sgi_de_primop_probe.py" "$T/rg/probe.py" || die "probe copy"
cmp -s "$T/$F" "$SEC/$F" || die "clone source differs from SEC"
say "  instrument: $(wc -c < "$T/rg/probe.py") bytes"

score () {
    local label="$1"
    cd "$T" && rm -f src/devices/dev_sgi_re.o && make -j4 > "$OUT/build_$label.log" 2>&1
    [ "$T/gxemul" -nt "$T/$F" ] || { say "  $label: binary not newer -- SKIP"; return 1; }
    ( cd "$T/rg" && timeout 500 python3 -u probe.py "$T/gxemul" "$label" > "$OUT/$label.out" 2>&1 )
    say "  $label: $(grep -a OPUS500_RESULT "$OUT/$label.out" | head -1)"
    grep -a OPUS500_RED "$OUT/$label.out" | sed 's/^/      /'
    return 0
}

say "BASE -- expect 23/23"
cp "$SEC/$F" "$T/$F"; score BASE

say "M8_maskwide -- op mask widened to cover the modifier bits.  Expect a RED."
cd "$T"; echo "M8_maskwide" > "$T/.MUTANT"; cp "$SEC/$F" "$T/$F"
python3 - <<'PY'
import io
p = 'src/devices/dev_sgi_re.c'
s = io.open(p, encoding='utf-8').read()
a = 'switch (op & 0xff000000) {'
assert s.count(a) == 1, 'anchor matched %d times' % s.count(a)
io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(a, 'switch (op & 0xffff0000) {'))
print('  M8_maskwide applied (anchor unique)')
PY
score M8_maskwide

say "M9_bit17 -- widen the mask by EXACTLY the bit the last repair missed."
say "  (0xff000000 -> 0xff020000.  This swept the 21-row version CLEAN.)"
cd "$T"; echo "M9_bit17" > "$T/.MUTANT"; cp "$SEC/$F" "$T/$F"
python3 - <<'PYX'
import io
p='src/devices/dev_sgi_re.c'
s=io.open(p,encoding='utf-8').read()
a='switch (op & 0xff000000) {'
assert s.count(a)==1, 'anchor %d' % s.count(a)
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a,'switch (op & 0xff020000) {'))
print('  M9_bit17 applied')
PYX
score M9_bit17

say "RESTORE from SEC + REBUILD + clear"
cp "$SEC/$F" "$T/$F"
cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED, sentinel kept"
cd "$T" && rm -f src/devices/dev_sgi_re.o && make -j4 > "$OUT/build_restore.log" 2>&1
if [ "$T/gxemul" -nt "$T/$F" ]; then rm -f "$T/.MUTANT"; say "  restored + REBUILT, sentinel cleared"
else say "  *** rebuild stale -- SENTINEL KEPT ***"; fi
say "M8_DONE"
