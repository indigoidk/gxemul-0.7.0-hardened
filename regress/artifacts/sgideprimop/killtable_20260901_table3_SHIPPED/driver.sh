#!/bin/bash
#  #500 pass-7 KILL TABLE (table 3) -- 34 rows, and the LATCH-ALIAS space verified by
#  ENUMERATION rather than sampled.
#
#  WHY THERE IS A PASS 6.  The pass-5 table ran 16 mutants with 16 exact
#  predictions and zero surprises -- and then the MANDATORY PRE-TABLE BLOCK,
#  which I had skipped and ran late, found a floor breach in one grep:
#
#      grep -c 'd->warned |=' src/devices/dev_sgi_re.c   ->   10
#
#  TEN writers of the guard field, bits 0..9.  The 32-row detector pre-set THREE
#  of them (1<<6, 1<<7, 1<<8).  Aliasing SGIRE_W_PRIM_OP onto any of 1<<0..1<<5
#  -- the six *_LEN latches -- escaped all 32 rows.  One-token edit to the
#  constant this round ADDED: floor clause (d), L2, repaired in-round.
#
#  THE REPAIR IS ONE ROW, NOT NINE.  `xlatch all' raises bits 0-8 in a single
#  session (every *_LEN latch fires on a wrong access length at its own window),
#  so an alias onto ANY of them goes silent and the row reds.  The closure is
#  over the FIELD, not over the individual bits.
#
#  THIS TABLE VERIFIES THAT ENUMERATION by building all nine alias mutants.
#  That is the amendment's own instruction -- the closing pass verifies the
#  enumeration rather than hunting cells.
#
#  PREDICTIONS, written BEFORE the run so the order is provable by mtime:
#
#    BASE            35/35
#    PREFIX          floor (a): many red   [baseline 840f3d0^, a NAMED commit]
#    M_EXIT0         the EIGHT * live / * liv rows; every surv row GREEN
#    M_BANG          every decl row, incl. xlatch all
#    M_ASSIGN        two once ALONE                                     34/35
#    M_ALIAS0..5     *** xlatch all ALONE, 34/35.  ON TABLE 2 THESE SIX EACH SCORED A
#                    CLEAN 35/35 -- the row was MIS-BUILT, not the closure wrong.
#                    DEVICE_ACCESS(sgi_re) does relative_addr += 0x1000 (:303) because
#                    the device is registered at baseaddr+0x1000 with length 0x1000, so
#                    CRIME_RE_TLB_A is at device offset 0x000.  The row used the
#                    CONSTANTS as offsets and all six accesses landed past the end of
#                    the device.  Offsets corrected by -0x1000.
#                    *** IF ANY OF THESE SIX STILL SCORES 35/35, THE CLOSURE IS A STORY
#                    AND THE ROW MUST BE REPLACED, NOT RE-AIMED AGAIN. *** 
#    M_ALIAS6        xlatch decl + xlatch all                           33/35
#    M_ALIAS7        xlatch unm  + xlatch all                           33/35
#    M_ALIAS8        xlatch unm  + xlatch all                           33/35
#    M_WIDE_FF/_17/_LO/_1923   both acc * mod                           33/35
#    M_NARROW_26/_27/_31       dec b26 / dec b27 / dec b31 ALONE        34/35
#    M_NARROW_25     *** PREDICTED CLEAN SWEEP 35/35 -- DISCLOSED, NOT A BREACH.
#                    Collapses RECTANGLE onto LINE; no row's channel can vary,
#                    because a successful draw writes nothing at reset. ***
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
T=/tmp/gx500p7
F=src/devices/dev_sgi_re.c
OUT=/tmp/kill500p7
BASELINE=840f3d0
say(){ echo "[$(date +%H:%M:%S)] $*"; }
die(){ say "*** ABORT: $* ***"; exit 1; }

mkdir -p "$OUT"
say "clone build/ -> $T   (kill tables run in a SCRATCH CLONE by default)"
rm -rf "$T"; cp -a "$G/build" "$T" || die clone
mkdir -p "$T/rg"
cp "$SEC/regress/sgi_de_primop_probe.py" "$T/rg/probe.py" || die "probe copy"
say "  instrument frozen: $(wc -c < "$T/rg/probe.py") bytes"
cmp -s "$T/$F" "$SEC/$F" || die "clone source differs from the SEC working tree"
say "  baseline: SEC working tree (post-fix).  PREFIX control = $BASELINE^"

score () {
    label="$1"
    cd "$T" && rm -f src/devices/dev_sgi_re.o && make -j4 > "$OUT/build_$label.log" 2>&1
    if [ ! "$T/gxemul" -nt "$T/$F" ]; then
        say "  $label: BINARY NOT NEWER THAN SOURCE -- SKIP (stale build)"
        return 1
    fi
    ( cd "$T/rg" && timeout 900 python3 -u probe.py "$T/gxemul" "$label" > "$OUT/$label.out" 2>&1 )
    say "  $label: $(grep -a OPUS500_RESULT "$OUT/$label.out" | head -1)"
    grep -a ' FAIL$' "$OUT/$label.out" | cut -c1-16 | sed 's/ *$//' | sed 's/^/      RED: /' | head -40
    return 0
}

mut () {
    cd "$T"; echo "$1" > "$T/.MUTANT"; cp "$SEC/$F" "$T/$F"
    python3 -c "$2" || die "mutator $1"
}

maskmut () {
    say "$1 -- switch mask -> $2"
    mut "$1" "
import io
p = 'src/devices/dev_sgi_re.c'
s = io.open(p, encoding='utf-8').read()
a = 'switch (op & 0xff000000) {'
assert s.count(a) == 1, s.count(a)
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a, 'switch (op & $2) {'))
print('  applied')
"
    score "$1"
}

bitmut () {
    say "$1 -- SGIRE_W_PRIM_OP -> 1 << $2"
    mut "$1" "
import io
p = 'src/devices/dev_sgi_re.c'
s = io.open(p, encoding='utf-8').read()
a = chr(9) + 'SGIRE_W_PRIM_OP   = 1 << 9,'
assert s.count(a) == 1, s.count(a)
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a, chr(9) + 'SGIRE_W_PRIM_OP   = 1 << $2,'))
print('  applied')
"
    score "$1"
}

say "BASE"
cp "$SEC/$F" "$T/$F"; rm -f "$T"/src/cpus/*.o; score BASE

say "PREFIX -- floor clause (a), against the NAMED commit $BASELINE^"
echo PREFIX > "$T/.MUTANT"
git -C "$SEC" show "$BASELINE^:$F" > "$T/$F" || die "checkout $BASELINE^"
score PREFIX

say "M_EXIT0 -- the exit-status trap"
mut M_EXIT0 "
import io
p = 'src/devices/dev_sgi_re.c'
s = io.open(p, encoding='utf-8').read()
T9 = chr(9)
a = T9*3 + '    op, x1, y1, x2, y2, fg, bg, pattern);' + chr(10) + T9*2 + '}' + chr(10) + T9*2 + 'break;'
assert s.count(a) == 1, s.count(a)
b = a.replace(T9*2 + 'break;', T9*2 + 'exit(0);' + chr(10) + T9*2 + 'break;')
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a, b))
print('  applied')
"
score M_EXIT0

say "M_BANG -- latch test inverted (SILENT)"
mut M_BANG "
import io
p = 'src/devices/dev_sgi_re.c'
s = io.open(p, encoding='utf-8').read()
a = 'if (!(d->warned & SGIRE_W_PRIM_OP))'
assert s.count(a) == 1, s.count(a)
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a, 'if ((d->warned & SGIRE_W_PRIM_OP))'))
print('  applied')
"
score M_BANG

say "M_ASSIGN -- latch never set (FLOOD)"
mut M_ASSIGN "
import io
p = 'src/devices/dev_sgi_re.c'
s = io.open(p, encoding='utf-8').read()
a = chr(9)*3 + 'd->warned |= SGIRE_W_PRIM_OP;' + chr(10)
assert s.count(a) == 1, s.count(a)
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a, ''))
print('  applied')
"
score M_ASSIGN

say "=== THE ALIAS SWEEP: all nine other bits in the field ==="
bitmut M_ALIAS0 0
bitmut M_ALIAS1 1
bitmut M_ALIAS2 2
bitmut M_ALIAS3 3
bitmut M_ALIAS4 4
bitmut M_ALIAS5 5
bitmut M_ALIAS6 6
bitmut M_ALIAS7 7
bitmut M_ALIAS8 8

maskmut M_WIDE_FF    0xffff0000
maskmut M_WIDE_17    0xff020000
maskmut M_WIDE_LO    0xff0000ff
maskmut M_WIDE_1923  0xfff00000
maskmut M_NARROW_26  0xfb000000
maskmut M_NARROW_27  0xf7000000
maskmut M_NARROW_31  0x7f000000
maskmut M_NARROW_25  0xfd000000

say "RESTORE from SEC + REBUILD + verify, THEN clear the sentinel"
cp "$SEC/$F" "$T/$F"
cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel KEPT"
cd "$T" && rm -f src/devices/dev_sgi_re.o && make -j4 > "$OUT/build_restore.log" 2>&1
if [ "$T/gxemul" -nt "$T/$F" ]; then
    rm -f "$T/.MUTANT"; say "  restored + REBUILT + verified, sentinel cleared"
else
    say "  *** REBUILD STALE -- SENTINEL KEPT ***"
fi
say "KILL500P7_DONE"
