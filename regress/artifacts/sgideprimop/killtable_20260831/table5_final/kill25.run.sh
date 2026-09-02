#!/bin/bash
#  #500 FULL KILL TABLE over the 25-row detector.
#
#  The row set grew 17 -> 19 -> 21 -> 23 -> 25 across three passes.  Added rows perturb
#  every earlier mutant's score, so the previous tables no longer describe this file and
#  ONLY THIS TABLE MAY BE CITED.
#
#  PREDICTIONS, written here BEFORE the run so the order is provable:
#
#    BASE          25/25
#    PREFIX        floor clause (a) -- MANY red, incl. every `surv'/`live' pair
#    M_EXIT0       the `live' rows red; every `surv' row GREEN (that is the whole point)
#    M_BANG        the `decl'/`once' rows red   (latch `!' dropped -- SILENT)
#    M_ASSIGN      `two once' ALONE             (latch `|=' dropped -- FLOOD)
#    M_BITALIAS    `xlatch decl' ALONE          (bit aliased onto #498's 1 << 6)
#    M8_maskwide   the two `acc * mod' rows     (mask widened over ALL modifier bits)
#    M9_bit17      the two `acc * mod' rows     (widened by bit 17 ALONE -- the gap
#                                                that swept the 21-row version clean)
#    M10_narrow    `dec hi bit' ALONE           (mask NARROWED: 0x05 aliases onto LINE
#                                                and is DRAWN instead of declined)
#
#  If M9 and M10 do not red, the class closure is a story rather than a fix.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
T=/tmp/gx500q
F=src/devices/dev_sgi_re.c
OUT=/tmp/kill25
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
    ( cd "$T/rg" && timeout 600 python3 -u probe.py "$T/gxemul" "$label" > "$OUT/$label.out" 2>&1 )
    say "  $label: $(grep -a OPUS500_RESULT "$OUT/$label.out" | head -1)"
    grep -a OPUS500_RED "$OUT/$label.out" | sed 's/^/      /'
    return 0
}

mut () { cd "$T"; echo "$1" > "$T/.MUTANT"; cp "$SEC/$F" "$T/$F"; python3 -c "$2" || die "mutator $1"; }

say "BASE"
cp "$SEC/$F" "$T/$F"; rm -f src/cpus/*.o; score BASE

say "PREFIX -- the committed build.  Floor clause (a)."
echo PREFIX > "$T/.MUTANT"
git -C "$SEC" show "HEAD:$F" > "$T/$F" || die checkout
score PREFIX

say "M_EXIT0"
mut M_EXIT0 "
import io
p='src/devices/dev_sgi_re.c'; s=io.open(p,encoding='utf-8').read()
a='\t\t\t    op, x1, y1, x2, y2, fg, bg, pattern);\n\t\t}\n\t\tbreak;'
assert s.count(a)==1, s.count(a)
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a,a.replace('\t\tbreak;','\t\texit(0);\n\t\tbreak;')))
print('  applied')
"
score M_EXIT0

say "M_BANG"
mut M_BANG "
import io
p='src/devices/dev_sgi_re.c'; s=io.open(p,encoding='utf-8').read()
a='if (!(d->warned & SGIRE_W_PRIM_OP))'
assert s.count(a)==1, s.count(a)
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a,'if ((d->warned & SGIRE_W_PRIM_OP))'))
print('  applied')
"
score M_BANG

say "M_ASSIGN"
mut M_ASSIGN "
import io
p='src/devices/dev_sgi_re.c'; s=io.open(p,encoding='utf-8').read()
a='\t\t\td->warned |= SGIRE_W_PRIM_OP;\n'
assert s.count(a)==1, s.count(a)
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a,''))
print('  applied')
"
score M_ASSIGN

say "M_BITALIAS"
mut M_BITALIAS "
import io
p='src/devices/dev_sgi_re.c'; s=io.open(p,encoding='utf-8').read()
a='\tSGIRE_W_PRIM_OP   = 1 << 9,'
assert s.count(a)==1, s.count(a)
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a,'\tSGIRE_W_PRIM_OP   = 1 << 6,'))
print('  applied')
"
score M_BITALIAS

for m in "M8_maskwide 0xffff0000" "M9_bit17 0xff020000" "M10_narrow 0x03000000"; do
    set -- $m
    say "$1 -- switch mask -> $2"
    mut "$1" "
import io
p='src/devices/dev_sgi_re.c'; s=io.open(p,encoding='utf-8').read()
a='switch (op & 0xff000000) {'
assert s.count(a)==1, s.count(a)
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a,'switch (op & $2) {'))
print('  applied')
"
    score "$1"
done

say "RESTORE from SEC + REBUILD + clear"
cp "$SEC/$F" "$T/$F"
cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED, sentinel kept"
cd "$T" && rm -f src/devices/dev_sgi_re.o && make -j4 > "$OUT/build_restore.log" 2>&1
if [ "$T/gxemul" -nt "$T/$F" ]; then rm -f "$T/.MUTANT"; say "  restored + REBUILT, sentinel cleared"
else say "  *** rebuild stale -- SENTINEL KEPT ***"; fi
say "KILL25_DONE"
