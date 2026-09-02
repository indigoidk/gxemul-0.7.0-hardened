#!/bin/bash
#  #500 pass-13 KILL TABLE (table 9) -- 34 rows, and the LATCH-ALIAS space verified by
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
T=/tmp/gx500pd
F=src/devices/dev_sgi_re.c
OUT=/tmp/kill500pd
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
#  *** M_NARROW_24 -- THE CELL I NEVER TESTED, AND THE ONE MY RECORDS DESCRIBED
#  WRONGLY.  A packet-fed seat did the arithmetic I had not: clearing bit 24 does
#  NOT collapse the primitives onto each other.  LINE 0x01 -> 0x00 and RECT 0x03
#  -> 0x02, so BOTH fall to `default:' and are DECLINED.  PREDICTION: the two
#  accept rows red (`acc rect' and `acc line'), NOT the n25 rows -- it was covered
#  from the start by rows that predate this whole repair.  If instead an n25 row
#  reds, my corrected understanding is still wrong. ***
maskmut M_NARROW_24  0xfe000000

say "M_SWAP -- PROBE-SIDE: neuter the rectangle session's drawmode store"
#  The seat's clean sweep, made a permanent cell.  It swaps that store's value
#  operand for a value already present in the edited body, so XFER is never
#  enabled: `n25 rect' then counts zero FOR THE WRONG REASON.  Measured at 38/39
#  against the 39-row detector -- ONLY `n25 rectset' reds -- and it was a CLEAN
#  SWEEP of the 38-row version.  PREDICTION: 38/39, RED on `n25 rectset' ALONE.
#  If it reds anything else, or nothing, the witness is not doing what is claimed.
cp "$SEC/$F" "$T/$F"
cd "$T" && rm -f src/devices/dev_sgi_re.o && make -j4 > "$OUT/build_M_SWAP.log" 2>&1
#  *** FROZEN COPY, NOT SEC.  Table 5 copied this from the LIVE tree at run time
#  and picked up a row added mid-table -- M_SWAP measured 39/40 while every other
#  cell measured /39.  A comparison run owes ONE instrument, and the driver that
#  exists to enforce that broke it.  The impossible denominator was the tell.
cp "$T/rg/probe.py" "$T/rg/probe_swap.py"
python3 -c "
import io
p = '$T/rg/probe_swap.py'
s = io.open(p, encoding='utf-8').read()
a = 'session(store(A, DE + DRAWMODE, val=XFER_EN)'
assert s.count(a) == 2, s.count(a)
i = s.index(a)
io.open(p,'w',encoding='utf-8',newline='').write(
    s[:i] + 'session(store(A, DE + DRAWMODE, val=\"0x03000000\")' + s[i+len(a):])
print('  M_SWAP applied to the rectangle session only')
" || die "M_SWAP mutator"
if diff -q "$T/rg/probe.py" "$T/rg/probe_swap.py" > /dev/null; then
    die "M_SWAP: mutated probe is IDENTICAL to the original -- the mutator did nothing"
fi
( cd "$T/rg" && timeout 900 python3 -u probe_swap.py "$T/gxemul" M_SWAP > "$OUT/M_SWAP.out" 2>&1 )
say "  M_SWAP: $(grep -a OPUS500_RESULT "$OUT/M_SWAP.out" | head -1)"
grep -a ' FAIL$' "$OUT/M_SWAP.out" | cut -c1-16 | sed 's/ *$//' | sed 's/^/      RED: /'

#  ---------------------------------------------------------------- probe-side
#  Two more INSTRUMENT mutants, both named by seats in pass 7, both now permanent
#  cells.  Every row in this detector reads a TRANSCRIPT, and every transcript is
#  produced by stores that nothing pinned -- pass 6 closed that for the rectangle
#  session and left the mirror open in the line session.  These two cells exist so
#  no seat has to find it a third time.
probe_mut () {
    label="$1"; from="$2"; to="$3"; expect="$4"; nocc="${5:-1}"
    say "$label -- PROBE-SIDE: $from -> $to   (expect RED on $expect)"
    cp "$T/rg/probe.py" "$T/rg/probe_$label.py"
    python3 -c "
import io
p = '$T/rg/probe_$label.py'
s = io.open(p, encoding='utf-8').read()
a = '$from'
n = s.count(a)
assert n == $nocc, 'expected $nocc occurrence(s), found %d' % n
i = s.index(a)
io.open(p,'w',encoding='utf-8',newline='').write(s[:i] + '$to' + s[i+len(a):])
" || die "$label mutator"
    if diff -q "$T/rg/probe.py" "$T/rg/probe_$label.py" > /dev/null; then
        die "$label: mutated probe IDENTICAL to the frozen original -- mutator did nothing"
    fi
    ( cd "$T/rg" && timeout 900 python3 -u "probe_$label.py" "$T/gxemul" "$label" > "$OUT/$label.out" 2>&1 )
    say "  $label: $(grep -a OPUS500_RESULT "$OUT/$label.out" | head -1)"
    grep -a ' FAIL$' "$OUT/$label.out" | cut -c1-16 | sed 's/ *$//' | sed 's/^/      RED: /'
}

#  grok: the rectangle session's drawmode -> the TRIANGLE constant.  This one
#  ESCAPED the 40-row detector because the witness matched an UNANCHORED
#  substring (0x200000 sits inside 0x2000000).  Now anchored with ' src_mode='.
probe_mut M_SWAP_TRI 'session(store(A, DE + DRAWMODE, val=XFER_EN)' 'session(store(A, DE + DRAWMODE, val="0x02000000")' 'n25 rectset' 2

#  codex: the drawmode-CLEAR line session's op -> RECT.  Escaped the 40-row form;
#  closed by n25 noxset, which pins op = 0x01ffffff in that transcript.
probe_mut M_SWAP_NOX 'val="0x01ffffff"' 'val="0x03ffffff"' 'n25 noxset'

say "M_QUALIFY -- clause (d): qualify THIS ROUND'S OWN latch predicate with a bit of op"
#  codex, pass 8.  `if (X)' -> `if (X && !(op & DE_PRIM_RL))' -- the canonical
#  clause-(d) form, and it swept the 41-row detector CLEAN because every op this
#  file sent to `default:' had bit 16 clear while the accept ops (which do carry
#  it) never reach this guard.  A real TRIANGLE|RL was silently declined.
#
#  *** THE FINDING WAS THE ASYMMETRY, NOT THE BIT: the accept rows have carried
#  0x??ffffff since pass 4 so any widening reds them; the decline rows carried NO
#  low bits at all for four passes.  `dec low' (0x02ffffff) closes the mirror. ***
#
#  PREDICTION: 42/43, RED on `dec low' ALONE -- and the six `dec b*' rows must
#  stay GREEN, because the qualification is invisible to ops with bit 16 clear.
#  If they red too, the mutant is not the one claimed.
mut M_QUALIFY "
import io
p = 'src/devices/dev_sgi_re.c'
s = io.open(p, encoding='utf-8').read()
a = chr(9)*2 + 'if (!(d->warned & SGIRE_W_PRIM_OP)) {'
assert s.count(a) == 1, s.count(a)
b = chr(9)*2 + 'if (!(d->warned & SGIRE_W_PRIM_OP) &&' + chr(10) + chr(9)*2 + '    !(op & DE_PRIM_RL)) {'
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a, b))
print('  applied')
"
score M_QUALIFY

#  ------------------------------------------------- pass-9 guard-qualification
qualmut () {
    label="$1"; join="$2"; cond="$3"; expect="$4"
    say "$label -- latch $join $cond   (expect $expect)"
    mut "$label" "
import io
p = 'src/devices/dev_sgi_re.c'
s = io.open(p, encoding='utf-8').read()
a = chr(9)*2 + 'if (!(d->warned & SGIRE_W_PRIM_OP)) {'
assert s.count(a) == 1, s.count(a)
b = chr(9)*2 + 'if (!(d->warned & SGIRE_W_PRIM_OP) $join' + chr(10) + chr(9)*2 + '    $cond) {'
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a, b))
print('  applied')
"
    score "$label"
}

#  grok, pass 9: the guarded body reads EIGHT values -- op plus the seven the
#  fatal() prints -- and every decline session left all seven at ZERO, so a
#  qualification on any of them was invisible.  BOTH forms are cells, because the
#  seat also named how the repair goes wrong: pinning only x1 leaves && !fg open.
qualmut M_QUAL_X1 '&&' '!x1' 'RED on dec ops'
qualmut M_QUAL_FG '&&' '!fg' 'RED on dec ops'

#  codex, pass 9: the SILENCE direction was closed by dec low and the FLOOD
#  direction left open -- a low-bit op BYPASSES the latch and announces every
#  draw.  Invisible because every low-bit decline session drew exactly once.
qualmut M_FLOOD_RL '||' '(op & DE_PRIM_RL)' 'RED on dec flood'

#  *** AND THIS ONE MUST STAY GREEN.  dec flood's op (0x02010000) has bit 17
#  CLEAR, so a bypass on TB cannot reach it.  A row that reddened under BOTH
#  would be responding to something other than what it claims -- "green for the
#  wrong reason" inverted.  The GREEN is the honest half of the control. ***
qualmut M_FLOOD_TB '||' '(op & DE_PRIM_TB)' 'GREEN -- 47/47, see the contract'

say "RESTORE from SEC + REBUILD + verify, THEN clear the sentinel"
cp "$SEC/$F" "$T/$F"
cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel KEPT"
cd "$T" && rm -f src/devices/dev_sgi_re.o && make -j4 > "$OUT/build_restore.log" 2>&1
if [ "$T/gxemul" -nt "$T/$F" ]; then
    rm -f "$T/.MUTANT"; say "  restored + REBUILT + verified, sentinel cleared"
else
    say "  *** REBUILD STALE -- SENTINEL KEPT ***"
fi
say "KILL500PD_DONE"
