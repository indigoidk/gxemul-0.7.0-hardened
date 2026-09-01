#!/bin/bash
#  #500 KILL TABLE.  A detector is discharged by MEASURED KILLS, never by existing.
#
#  PREDICTIONS, written HERE before the run so the order is provable:
#    PREFIX  committed build (the kill still there)  -> floor clause (a): MANY red
#    M_EXIT0 exit(0) instead of the decline           -> `* live' rows RED, `* surv' GREEN
#                                                        (this is the whole point of pairing)
#    M_BANG  drop the `!' -> announce never fires     -> `* decl' rows RED (silent)
#    M_ASSIGN drop the `|=' -> announce every time    -> `two once' RED (flood), decl rows GREEN
#    M_WRONLY decline only when writeflag==MEM_WRITE  -> `rd *' RED, write rows GREEN
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
T=/tmp/gx500m
F=src/devices/dev_sgi_re.c
OUT=/tmp/kill500b
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

say "BASE -- expect 19/19 (two repairs added: full-literal decl rows + cross-latch)"
cp "$SEC/$F" "$T/$F"; score BASE

say "PREFIX -- the committed build.  FLOOR CLAUSE (a): the detector MUST fail."
echo "PREFIX" > "$T/.MUTANT"
git -C "$SEC" show "HEAD:$F" > "$T/$F" || die checkout
score PREFIX

mut () {  # $1 label, $2 python
    cd "$T"; echo "$1" > "$T/.MUTANT"; cp "$SEC/$F" "$T/$F"
    python3 -c "$2" || die "mutator $1"
}

say "M_EXIT0 -- announce then exit(0).  `* live' rows must RED; `* surv' will NOT."
mut M_EXIT0 "
import io
p='src/devices/dev_sgi_re.c'; s=io.open(p,encoding='utf-8').read()
a='\t\t\t    op, x1, y1, x2, y2, fg, bg, pattern);\n\t\t}\n\t\tbreak;'
assert s.count(a)==1, s.count(a)
b='\t\t\t    op, x1, y1, x2, y2, fg, bg, pattern);\n\t\t}\n\t\texit(0);\n\t\tbreak;'
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a,b)); print('  M_EXIT0 applied')
"
score M_EXIT0

say "M_BANG -- drop the '!' so the latch never sets: a SILENT decline."
mut M_BANG "
import io
p='src/devices/dev_sgi_re.c'; s=io.open(p,encoding='utf-8').read()
a='if (!(d->warned & SGIRE_W_PRIM_OP))'
assert s.count(a)==1, s.count(a)
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a,'if ((d->warned & SGIRE_W_PRIM_OP))'))
print('  M_BANG applied')
"
score M_BANG

say "M_ASSIGN -- drop the '|=' so the announce FLOODS."
mut M_ASSIGN "
import io
p='src/devices/dev_sgi_re.c'; s=io.open(p,encoding='utf-8').read()
a='\t\t\td->warned |= SGIRE_W_PRIM_OP;\n'
assert s.count(a)==1, s.count(a)
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a,''))
print('  M_ASSIGN applied')
"
score M_ASSIGN

say "M_BITALIAS -- SGIRE_W_PRIM_OP aliased onto #498's used bit.  Only xlatch can see it."
mut M_BITALIAS "
import io
p='src/devices/dev_sgi_re.c'; s=io.open(p,encoding='utf-8').read()
a='	SGIRE_W_PRIM_OP   = 1 << 9,'
assert s.count(a)==1, s.count(a)
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a,'	SGIRE_W_PRIM_OP   = 1 << 6,'))
print('  M_BITALIAS applied')
"
score M_BITALIAS

say "RESTORE + REBUILD + clear"
cp "$SEC/$F" "$T/$F"
cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED, sentinel kept"
cd "$T" && rm -f src/devices/dev_sgi_re.o && make -j4 > "$OUT/build_restore.log" 2>&1
if [ "$T/gxemul" -nt "$T/$F" ]; then rm -f "$T/.MUTANT"; say "  restored + REBUILT, sentinel cleared"
else say "  *** rebuild stale -- SENTINEL KEPT ***"; fi
say "KILL500_DONE"
