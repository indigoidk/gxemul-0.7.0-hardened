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
#  PREDICTION, before the run: M_FLOOD_RL -> RED on `dec flood' (its op carries
#  bit 16).  M_FLOOD_TB -> `dec flood' GREEN, because 0x02010000 has bit 17
#  CLEAR -- and that is the HONEST half: it shows the row keys on the bit its
#  own op carries, not on any bypass whatever.  A row that reddened under both
#  would be responding to something other than what it claims.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
T=/tmp/gx_latchfld
F=src/devices/dev_sgi_re.c
say(){ echo "[$(date +%H:%M:%S)] $*"; }
die(){ say "*** ABORT: $* ***"; exit 1; }

rm -rf "$T"; cp -a "$G/build" "$T" || die clone
mkdir -p "$T/rg"
cp "$SEC/regress/sgi_de_primop_probe.py" "$T/rg/probe.py" || die "probe copy"
cmp -s "$T/$F" "$SEC/$F" || die "clone source differs from SEC"

qual () {
    label="$1"; join="$2"; cond="$3"
    say "$label -- latch $join $cond"
    echo "$label" > "$T/.MUTANT"
    cp "$SEC/$F" "$T/$F"
    python3 -c "
import io
p = '$T/$F'
s = io.open(p, encoding='utf-8').read()
a = chr(9)*2 + 'if (!(d->warned & SGIRE_W_PRIM_OP)) {'
assert s.count(a) == 1, s.count(a)
b = chr(9)*2 + 'if (!(d->warned & SGIRE_W_PRIM_OP) $join' + chr(10) + chr(9)*2 + '    $cond) {'
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(a, b))
print('  applied')
" || die "$label mutator"
    if diff -q "$SEC/$F" "$T/$F" > /dev/null; then die "$label: source unchanged"; fi
    cd "$T" && rm -f src/devices/dev_sgi_re.o && make -j4 > "/tmp/latchfld_build_$label.log" 2>&1
    [ "$T/gxemul" -nt "$T/$F" ] || die "$label: build stale"
    ( cd "$T/rg" && timeout 900 python3 -u probe.py "$T/gxemul" "$label" > "/tmp/latchfld_$label.out" 2>&1 )
    say "  $label: $(grep -a OPUS500_RESULT "/tmp/latchfld_$label.out" | head -1)"
    grep -a ' FAIL$' "/tmp/latchfld_$label.out" | cut -c1-16 | sed 's/ *$//' | sed 's/^/      RED: /'
}









#  *** AND THIS ONE MUST STAY GREEN.  Bit 26 is CLEAR in 0x02ffffff, so a bypass
#  there cannot reach this row.  The green half is what stops the row's coverage
#  claim from being wider than the truth -- and it had to MOVE from TB, which the
#  widened op now legitimately reds. ***















#  `xlatch all' PRE-SETS d->warned bits 0-8 and now draws TWICE.  A bypass keyed
#  on any bit it pre-sets must make it announce twice and RED.
qual M_LF_DELEN '||' '(d->warned & SGIRE_W_DE_LEN)'
qual M_LF_TLBA  '||' '(d->warned & SGIRE_W_TLBA_LEN)'

#  *** GREEN BY DESIGN: bit 9 is SGIRE_W_PRIM_OP itself -- the latch under test,
#  which this session does NOT pre-set.  `|| (d->warned & SGIRE_W_PRIM_OP)' makes
#  the guard read `!(w & X) || (w & X)', ALWAYS TRUE, so it announces on every
#  draw and the row SHOULD red.  Predicting GREEN here would be wrong; predict
#  RED and say so, because the tautology is a different mutant from a foreign-bit
#  bypass.  The honest GREEN control is a bit NO session pre-sets and the guard
#  never sets: there is none in this enum, so this axis has NO green cell and
#  that is stated rather than faked. ***
qual M_LF_SELF  '||' '(d->warned & SGIRE_W_PRIM_OP)'

say "RESTORE + REBUILD + verify"
cp "$SEC/$F" "$T/$F"
cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel kept"
cd "$T" && rm -f src/devices/dev_sgi_re.o && make -j4 > /tmp/latchfld_restore.log 2>&1
if [ "$T/gxemul" -nt "$T/$F" ]; then rm -f "$T/.MUTANT"; say "  restored + rebuilt, sentinel cleared"
else say "  *** REBUILD STALE -- SENTINEL KEPT ***"; fi
say "NEGCTL_LATCHFLD_DONE"
