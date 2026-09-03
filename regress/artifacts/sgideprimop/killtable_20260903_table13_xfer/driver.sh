#!/bin/bash
#  #500 pass 15 -- VERIFY THE ELEVEN-REGISTER CLOSURE, PIN THE GENERALISED CONTRACT.
#
#  Cells, each labelled so the reader knows which expectation applies:
#    CONTROL  BASE must be 51/51.  ANNOUNCE-CONTINUE-ANNOTATE if not: say which rows.
#    CLOSE    the six XFER registers -- M_STEPX was MEASURED 50/50 on the 50-row probe
#             (gapB_20260903/); all six must now RED `dec regs'.
#    LIMIT    two declared-uncovered shapes, EXPECTED to stay 51/51: the seat's bit
#             RELATION on op, and register equality to an unpinned value.  A red here
#             would mean the contract UNDER-claims, which is safe but must be recorded.
#    CONTROL  B25 must keep exactly its 3 rows.
set -u
G=/mnt/c/DocumentNoSnc/CC/GXEMUL; SEC=$G/GXEMUL-SEC; T=/tmp/gx500p16; F=src/devices/dev_sgi_re.c
OUT=/tmp/kill500p16; PROBE=sgi_de_primop_probe.py
say() { echo "[$(date +%H:%M:%S)] $*"; }
die() { echo "*** ABORT: $*"; exit 9; }
rm -rf "$T" "$OUT"; mkdir -p "$OUT"
say "clone build/ -> $T"; cp -a "$G/build" "$T" || die "clone failed"
cmp -s "$T/$F" "$SEC/$F" || die "clone's $F is NOT the SEC baseline"
cp "$SEC/regress/$PROBE" "$OUT/frozen_probe.py" || die "cannot freeze probe"
say "  instrument frozen: $(wc -c < "$OUT/frozen_probe.py") bytes"
build() { cd "$T" || die cd; rm -f src/devices/dev_sgi_re.o; make -j4 > "$OUT/build_$1.log" 2>&1; [ "$T/gxemul" -nt "$T/$F" ] || die "$1: binary not newer than source"; }
score() {
    cd "$SEC/regress" || die cd
    python3 -u "$OUT/frozen_probe.py" "$T/gxemul" "$1" > "$OUT/$1.out" 2>&1
    grep -q OPUS500_DONE "$OUT/$1.out" || die "$1: NO COMPLETION SENTINEL"
    say "  $1 [$2]: $(grep -m1 OPUS500_RESULT "$OUT/$1.out")"
    grep -m1 OPUS500_RED "$OUT/$1.out" | sed 's/OPUS500_RED=/      RED: /' || true
}
mut() {
    echo "$F  bypass mutant $1" > "$T/.MUTANT"; cp "$SEC/$F" "$T/$F"
    python3 - "$T/$F" "$3" <<'PYEOF'
import io, sys
p, cond = sys.argv[1], sys.argv[2]; s = io.open(p, encoding='utf-8').read()
a = "\t\tif (!(d->warned & SGIRE_W_PRIM_OP)) {"; b = "\t\tif (!(d->warned & SGIRE_W_PRIM_OP) || %s) {" % cond
assert s.count(a) == 1, "anchor count %d" % s.count(a)
io.open(p, 'w', encoding='utf-8', newline='\n').write(s.replace(a, b))
PYEOF
    [ $? -eq 0 ] || die "$1: mutator failed"
    cmp -s "$T/$F" "$SEC/$F" && die "$1: file UNCHANGED after mutation"
    build "$1"; score "$1" "$2"
}
restore() { cp "$SEC/$F" "$T/$F"; cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel KEPT"; build restore; rm -f "$T/.MUTANT"; }

say "BASE -- must be 51/51"; build BASE; score BASE CONTROL
BASE_RES=$(grep -m1 OPUS500_RESULT "$OUT/BASE.out" | cut -d= -f2)
[ "$BASE_RES" = "51/51" ] || say "*** BASE IS NOT FULL ($BASE_RES): $(grep -m1 OPUS500_RED "$OUT/BASE.out") -- CONTINUING; read every cell with those rows SUBTRACTED ***"

say "=== CLOSE: the six XFER registers.  ALL must RED dec regs. ==="
mut M_STEPX    CLOSE 'step_x'
mut M_ADDRSRC  CLOSE '(d->de_reg[(CRIME_DE_XFER_ADDR_SRC - 0x2000) / sizeof(uint32_t)] & 0x1)'
mut M_STRDSRC  CLOSE '(d->de_reg[(CRIME_DE_XFER_STRD_SRC - 0x2000) / sizeof(uint32_t)] & 0x1)'
mut M_STEPY    CLOSE '(d->de_reg[(CRIME_DE_XFER_STEP_Y - 0x2000) / sizeof(uint32_t)] & 0x1)'
mut M_ADDRDST  CLOSE '(d->de_reg[(CRIME_DE_XFER_ADDR_DST - 0x2000) / sizeof(uint32_t)] & 0x1)'
mut M_STRDDST  CLOSE '(d->de_reg[(CRIME_DE_XFER_STRD_DST - 0x2000) / sizeof(uint32_t)] & 0x1)'

say "=== LIMIT: declared uncovered.  EXPECTED 51/51 -- a measured limit, not an escape. ==="
mut M_OP_PAIRXOR  LIMIT '(((op & 1) != 0) != (((op >> 1) & 1) != 0))'
mut M_DRAWMODE_EQ LIMIT '(drawmode == 0x1234)'

say "=== CONTROL ==="
mut M_FLOOD_B25 CONTROL '(op & 0x02000000)'

say "RESTORE from SEC + REBUILD + verify, THEN clear the sentinel"; restore; say "  restored + REBUILT + verified, sentinel cleared"
say "KILL500P16_DONE"
