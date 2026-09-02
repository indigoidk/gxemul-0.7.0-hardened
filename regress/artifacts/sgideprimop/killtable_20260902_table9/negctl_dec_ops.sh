#!/bin/bash
#  NEGATIVE CONTROL for `dec ops', and it runs the seat's mutant TWICE ON
#  DIFFERENT OPERANDS to prove the CLASS is closed rather than one cell.
#
#  The seat's finding: the latch's guarded body reads eight values -- op plus the
#  seven the fatal() prints -- so clause (d) admits `&& !x1', `&& !fg', and five
#  more.  Every decline session left all seven at ZERO, so every one of those
#  qualifications was invisible.
#
#  It also named how the repair goes wrong: "do not pin only x1 -- a row that
#  only sets x1=1 leaves && !fg as pass 10."  So this control builds BOTH the x1
#  form and the fg form.  If `dec ops' reds under both, the class is closed; if it
#  reds under only one, I have repaired a cell again.
#
#  PREDICTION, before the run: M_QUAL_X1 -> 44/45 RED on `dec ops' alone;
#                             M_QUAL_FG -> 44/45 RED on `dec ops' alone.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
T=/tmp/gx_decops
F=src/devices/dev_sgi_re.c
say(){ echo "[$(date +%H:%M:%S)] $*"; }
die(){ say "*** ABORT: $* ***"; exit 1; }

rm -rf "$T"; cp -a "$G/build" "$T" || die clone
mkdir -p "$T/rg"
cp "$SEC/regress/sgi_de_primop_probe.py" "$T/rg/probe.py" || die "probe copy"
cmp -s "$T/$F" "$SEC/$F" || die "clone source differs from SEC"

qual () {
    label="$1"; cond="$2"
    say "$label -- latch qualified with $cond"
    echo "$label" > "$T/.MUTANT"
    cp "$SEC/$F" "$T/$F"
    python3 -c "
import io
p = '$T/$F'
s = io.open(p, encoding='utf-8').read()
a = chr(9)*2 + 'if (!(d->warned & SGIRE_W_PRIM_OP)) {'
assert s.count(a) == 1, s.count(a)
b = chr(9)*2 + 'if (!(d->warned & SGIRE_W_PRIM_OP) &&' + chr(10) + chr(9)*2 + '    $cond) {'
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a, b))
print('  applied')
" || die "$label mutator"
    if diff -q "$SEC/$F" "$T/$F" > /dev/null; then die "$label: source unchanged"; fi
    cd "$T" && rm -f src/devices/dev_sgi_re.o && make -j4 > "/tmp/decops_build_$label.log" 2>&1
    [ "$T/gxemul" -nt "$T/$F" ] || die "$label: build stale"
    ( cd "$T/rg" && timeout 900 python3 -u probe.py "$T/gxemul" "$label" > "/tmp/decops_$label.out" 2>&1 )
    say "  $label: $(grep -a OPUS500_RESULT "/tmp/decops_$label.out" | head -1)"
    grep -a ' FAIL$' "/tmp/decops_$label.out" | cut -c1-16 | sed 's/ *$//' | sed 's/^/      RED: /'
}

qual M_QUAL_X1 '!x1'
qual M_QUAL_FG '!fg'

say "RESTORE + REBUILD + verify"
cp "$SEC/$F" "$T/$F"
cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel kept"
cd "$T" && rm -f src/devices/dev_sgi_re.o && make -j4 > /tmp/decops_restore.log 2>&1
if [ "$T/gxemul" -nt "$T/$F" ]; then rm -f "$T/.MUTANT"; say "  restored + rebuilt, sentinel cleared"
else say "  *** REBUILD STALE -- SENTINEL KEPT ***"; fi
say "NEGCTL_DECOPS_DONE"
