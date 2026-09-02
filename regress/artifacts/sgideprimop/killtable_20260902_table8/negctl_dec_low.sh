#!/bin/bash
#  NEGATIVE CONTROL for `dec low', built from the seat's OWN mutant.
#
#  codex's clause-(d) escape: qualify this round's latch predicate with a bit of
#  `op' --
#
#      if (!(d->warned & SGIRE_W_PRIM_OP) &&
#          !(op & DE_PRIM_RL)) {
#
#  Every op this probe sent to `default:' had bit 16 CLEAR, so the guard was
#  unchanged for all of them and the 41-row table scored a CLEAN SWEEP -- while a
#  real TRIANGLE|RL reached `default:' and was SILENTLY declined.
#
#  THIS RUN MUST SHOW BOTH HALVES: `dec low' reds, AND the pre-existing decline
#  rows stay GREEN.  If the old rows red too, the mutant is not the one claimed
#  and the finding is mischaracterised; if `dec low' does not red, the repair is
#  a story.
#
#  PRODUCT-CODE mutant, so it needs a BUILD -- and the restore is not finished
#  until the binary is rebuilt.  Runs in its own clone; the project trees are
#  never touched.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
T=/tmp/gx_declow
F=src/devices/dev_sgi_re.c
say(){ echo "[$(date +%H:%M:%S)] $*"; }
die(){ say "*** ABORT: $* ***"; exit 1; }

rm -rf "$T"; cp -a "$G/build" "$T" || die clone
mkdir -p "$T/rg"
cp "$SEC/regress/sgi_de_primop_probe.py" "$T/rg/probe.py" || die "probe copy"
cmp -s "$T/$F" "$SEC/$F" || die "clone source differs from SEC"
echo M_QUALIFY > "$T/.MUTANT"

python3 - "$T/$F" <<'PYEOF'
import io, sys
P = sys.argv[1]
s = io.open(P, encoding='utf-8').read()
a = "\t\tif (!(d->warned & SGIRE_W_PRIM_OP)) {"
n = s.count(a)
print("  latch-guard sites: %d" % n)
assert n == 1, "expected exactly one"
b = "\t\tif (!(d->warned & SGIRE_W_PRIM_OP) &&\n\t\t    !(op & DE_PRIM_RL)) {"
io.open(P, 'w', encoding='utf-8', newline='').write(s.replace(a, b))
print("  applied codex's qualification: && !(op & DE_PRIM_RL)")
PYEOF

echo "  --- proof the mutant is in the source (blank = mutator did nothing) ---"
diff "$SEC/$F" "$T/$F" | sed 's/^/    /'

cd "$T" && rm -f src/devices/dev_sgi_re.o && make -j4 > /tmp/declow_build.log 2>&1
[ "$T/gxemul" -nt "$T/$F" ] || die "build stale -- binary not newer than source"
say "  built"

( cd "$T/rg" && timeout 900 python3 -u probe.py "$T/gxemul" M_QUALIFY > /tmp/declow_out.txt 2>&1 )
echo
echo "  --- every decline row under codex's mutant ---"
grep -E '^dec ' /tmp/declow_out.txt
grep -a OPUS500_RESULT /tmp/declow_out.txt
echo
echo "  --- every RED ---"
grep -a ' FAIL$' /tmp/declow_out.txt | cut -c1-16 | sed 's/^/    /'

say "RESTORE + REBUILD + verify"
cp "$SEC/$F" "$T/$F"
cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel kept"
cd "$T" && rm -f src/devices/dev_sgi_re.o && make -j4 > /tmp/declow_restore.log 2>&1
if [ "$T/gxemul" -nt "$T/$F" ]; then rm -f "$T/.MUTANT"; say "  restored + rebuilt, sentinel cleared"
else say "  *** REBUILD STALE -- SENTINEL KEPT ***"; fi
say "NEGCTL_DECLOW_DONE"
