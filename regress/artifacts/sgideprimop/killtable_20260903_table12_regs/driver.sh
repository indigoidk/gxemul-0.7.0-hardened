#!/bin/bash
#  #500 pass 14 -- VERIFY THE REGISTER-FAMILY CLOSURE (`dec regs') and PIN THE CONTRACT.
#
#  Pass 13's measuring seat found four clean sweeps.  Two are a FAMILY the new
#  `dec regs' session closes (five pre-switch registers, all-ones, POINT twice);
#  two are magic-value picks the CONTRACT now declares deliberately uncovered.
#
#  So this table has THREE kinds of cell and says which is which:
#    CLOSE   the five register bit-tests + op==0     -> must go RED (was 47/47)
#    LIMIT   op==0x07000000, fg&0x80                 -> EXPECTED to stay 50/50; that is
#            the contract's stated limit being MEASURED, not an escape
#    CONTROL B25 (already observable) must keep 3 red; BASE must be 50/50
#
#  A closure that verifies the two demonstrated cells is a cell repair in closure
#  clothing, so all five registers are built, not just the two the seat measured.
set -u

G=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$G/GXEMUL-SEC
T=/tmp/gx500p14
F=src/devices/dev_sgi_re.c
OUT=/tmp/kill500p14
PROBE=sgi_de_primop_probe.py

say() { echo "[$(date +%H:%M:%S)] $*"; }
die() { echo "*** ABORT: $*"; exit 9; }

rm -rf "$T" "$OUT"; mkdir -p "$OUT"
say "clone build/ -> $T"
cp -a "$G/build" "$T" || die "clone failed"
cmp -s "$T/$F" "$SEC/$F" || die "clone's $F is NOT the SEC baseline"
cp "$SEC/regress/$PROBE" "$OUT/frozen_probe.py" || die "cannot freeze probe"
say "  instrument frozen: $(wc -c < "$OUT/frozen_probe.py") bytes"

build() {
    cd "$T" || die "cd"
    rm -f src/devices/dev_sgi_re.o
    make -j4 > "$OUT/build_$1.log" 2>&1
    [ "$T/gxemul" -nt "$T/$F" ] || die "$1: binary NOT newer than source"
}
score() {
    cd "$SEC/regress" || die "cd regress"
    python3 -u "$OUT/frozen_probe.py" "$T/gxemul" "$1" > "$OUT/$1.out" 2>&1
    grep -q OPUS500_DONE "$OUT/$1.out" || die "$1: NO COMPLETION SENTINEL"
    say "  $1 [$2]: $(grep -m1 OPUS500_RESULT "$OUT/$1.out")"
    grep -m1 OPUS500_RED "$OUT/$1.out" | sed 's/OPUS500_RED=/      RED: /' || true
}
#  $1 name, $2 kind (CLOSE/LIMIT/CONTROL), $3 the C condition appended with ||
mut() {
    echo "$F  bypass mutant $1" > "$T/.MUTANT"
    cp "$SEC/$F" "$T/$F"
    python3 - "$T/$F" "$3" <<'PYEOF'
import io, sys
p, cond = sys.argv[1], sys.argv[2]
s = io.open(p, encoding='utf-8').read()
a = "\t\tif (!(d->warned & SGIRE_W_PRIM_OP)) {"
b = "\t\tif (!(d->warned & SGIRE_W_PRIM_OP) || %s) {" % cond
assert s.count(a) == 1, "anchor count %d" % s.count(a)
io.open(p, 'w', encoding='utf-8', newline='\n').write(s.replace(a, b))
PYEOF
    [ $? -eq 0 ] || die "$1: mutator failed"
    cmp -s "$T/$F" "$SEC/$F" && die "$1: file UNCHANGED after mutation"
    build "$1"
    score "$1" "$2"
}
restore() {
    cp "$SEC/$F" "$T/$F"
    cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel KEPT"
    build restore
    rm -f "$T/.MUTANT"
}

say "BASE -- must be 50/50 on the repaired probe"
build BASE
score BASE CONTROL

say "=== CLOSE: the five register bit-tests + the reset-value equality.  ALL must RED. ==="
mut M_XFER     CLOSE '(drawmode & DE_DRAWMODE_XFER_EN)'
mut M_SRCMODE  CLOSE '(src_mode & 0x00001c00)'
mut M_DSTMODE  CLOSE '(dst_mode & 0x00000300)'
mut M_ROP      CLOSE '(rop & 0xff)'
mut M_STIPPLE  CLOSE '(stipple_mode & 0x1f000000)'
mut M_OPEQ0    CLOSE '(op == 0x00000000)'

say "=== LIMIT: declared uncovered by the contract.  EXPECTED 50/50 -- a measured limit, not an escape. ==="
mut M_OPEQ07   LIMIT '(op == 0x07000000)'
mut M_FG80     LIMIT '(fg & 0x80)'

say "=== CONTROL: already-observable, must keep its old score (3 red) ==="
mut M_FLOOD_B25 CONTROL '(op & 0x02000000)'

say "RESTORE from SEC + REBUILD + verify, THEN clear the sentinel"
restore
say "  restored + REBUILT + verified, sentinel cleared"
say "KILL500P14_DONE"

#  =====================================================================
#  ANNOTATION, written after the run -- NOT BACKDATED.
#  BASE measured 49/50: `dec regs set' was RED on the fixed build because its
#  want was 1 and the entry announcement prints once PER DRAW in a two-draw
#  session.  The instrument defect was in the FROZEN copy this table scored,
#  so every cell carries that one row red; the live probe was corrected to
#  want=2 while the table ran, and a single BASE re-run against the corrected
#  instrument is preserved beside this as base_corrected.out.
#  READ THE TABLE WITH THAT ROW SUBTRACTED: all six CLOSE cells red `dec regs'
#  (five register bit-tests + op==0), both LIMIT cells escape as the contract
#  declares, B25 keeps its three rows.
#  AND THIS DRIVER PROCEEDED PAST A BASE THAT WAS NOT FULL SCORE.  That is the
#  print-only-control finding from pass 13 in its second instance.  A `die' on
#  BASE < full would have cost the table; a `say' let it run.  Filed.
#  =====================================================================
