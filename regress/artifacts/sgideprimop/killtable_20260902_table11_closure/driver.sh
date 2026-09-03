#!/bin/bash
#  #500 pass 12 -- VERIFY THE L2 CLASS CLOSURE.
#
#  Pass 11's panel measured M_FLOOD_B27 and M_FLOOD_B31 as 47/47 TOTAL ESCAPES of
#  the shipped detector: a latch bypass keyed on a high bit that no session could
#  observe, because the six `dec b*' sessions drew only ONCE.
#
#  The repair makes that loop two-draw.  THIS TABLE MEASURES WHETHER IT WORKED, and
#  it measures the WHOLE open set rather than the two cells that were demonstrated:
#  the seat MEASURED 27 and 31 and DERIVED 24, 28, 29, 30.  A class closure that
#  verifies two of six is a cell repair wearing closure clothes.
#
#  NEGATIVE CONTROLS, both directions:
#    * B25 and B26 were ALREADY observable and must keep their exact old scores --
#      if the repair changed them it perturbed rows it had no business touching.
#    * BASE must stay 47/47 -- a two-draw session that reds its own row on the fixed
#      build would be a broken repair that looks like a working detector.
set -u

G=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$G/GXEMUL-SEC
T=/tmp/gx500p12
F=src/devices/dev_sgi_re.c
OUT=/tmp/kill500p12
PROBE=sgi_de_primop_probe.py

say() { echo "[$(date +%H:%M:%S)] $*"; }
die() { echo "*** ABORT: $*"; exit 9; }

rm -rf "$T" "$OUT"; mkdir -p "$OUT"
say "clone build/ -> $T   (kill tables run in a SCRATCH CLONE by default)"
cp -a "$G/build" "$T" || die "clone failed"

#  NAME THE BASELINE and cmp the file-to-be-mutated against it BEFORE mutant 1.
cmp -s "$T/$F" "$SEC/$F" || die "clone's $F is NOT the SEC baseline -- refusing to measure"
say "  baseline: SEC working tree, $F cmp-clean"

#  FROZEN INSTRUMENT: one instrument for the whole comparison.  A driver that
#  re-copies the live probe between runs gives run 1 and run 2 different tools.
cp "$SEC/regress/$PROBE" "$OUT/frozen_probe.py" || die "cannot freeze probe"
say "  instrument frozen: $(wc -c < "$OUT/frozen_probe.py") bytes"

build() {
    cd "$T" || die "cd"
    rm -f src/devices/dev_sgi_re.o
    make -j4 > "$OUT/build_$1.log" 2>&1
    [ "$T/gxemul" -nt "$T/$F" ] || die "$1: binary NOT newer than source -- build failed silently"
}

score() {
    cd "$SEC/regress" || die "cd regress"
    python3 -u "$OUT/frozen_probe.py" "$T/gxemul" "$1" > "$OUT/$1.out" 2>&1
    grep -q OPUS500_DONE "$OUT/$1.out" || die "$1: NO COMPLETION SENTINEL"
    say "  $1: $(grep -m1 OPUS500_RESULT "$OUT/$1.out")"
    grep -m1 OPUS500_RED "$OUT/$1.out" | sed 's/OPUS500_RED=/      RED: /' || true
}

#  Every mutation drops the sentinel FIRST and clears it only after a VERIFIED
#  restore -- cmp against SEC (never the script's own backup) AND a rebuild.
mut() {
    echo "$F  flood-bypass mutant $1" > "$T/.MUTANT"
    cp "$SEC/$F" "$T/$F"
    python3 - "$T/$F" "$2" <<'PYEOF'
import io, sys
p, bit = sys.argv[1], sys.argv[2]
s = io.open(p, encoding='utf-8').read()
a = "\t\tif (!(d->warned & SGIRE_W_PRIM_OP)) {"
b = "\t\tif (!(d->warned & SGIRE_W_PRIM_OP) || (op & %s)) {" % bit
assert s.count(a) == 1, "anchor count %d" % s.count(a)
io.open(p, 'w', encoding='utf-8', newline='\n').write(s.replace(a, b))
PYEOF
    [ $? -eq 0 ] || die "$1: mutator failed"
    #  DIFF-PROOF: a mutator that matched nothing and a mutant that survived print
    #  the same score.  Refuse to measure an unmutated file.
    cmp -s "$T/$F" "$SEC/$F" && die "$1: file UNCHANGED after mutation -- would measure a phantom"
    build "$1"
    score "$1"
}

restore() {
    cp "$SEC/$F" "$T/$F"
    cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel KEPT"
    build restore
    rm -f "$T/.MUTANT"
}

say "BASE -- must be 47/47 on the repaired probe"
build BASE
score BASE

say "=== THE SIX PREVIOUSLY-OPEN BITS.  ALL SIX must now RED. ==="
mut M_FLOOD_B24 0x01000000
mut M_FLOOD_B27 0x08000000
mut M_FLOOD_B28 0x10000000
mut M_FLOOD_B29 0x20000000
mut M_FLOOD_B30 0x40000000
mut M_FLOOD_B31 0x80000000

say "=== NEGATIVE CONTROLS: already-observable bits must keep their OLD scores ==="
mut M_FLOOD_B25 0x02000000
mut M_FLOOD_B26 0x04000000

say "RESTORE from SEC + REBUILD + verify, THEN clear the sentinel"
restore
say "  restored + REBUILT + verified, sentinel cleared"
say "KILL500P12_DONE"
