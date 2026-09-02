#!/bin/bash
#  #500 floor clause (a), RE-RUN against the TRUE pre-fix source.
#
#  The first attempt used `git show HEAD:...' and scored 25/25 -- a CLEAN SWEEP that
#  looked like a vacuous detector and was nothing of the kind.  #500 had been COMMITTED
#  between the script being written and being run, so HEAD *is* the fixed file: the
#  reference silently changed meaning underneath a control whose whole job is to be the
#  unfixed baseline.
#
#  *** A BASELINE NAMED BY A MOVING REFERENCE IS NOT A BASELINE.  Name the COMMIT. ***
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
T=/tmp/gx500r
F=src/devices/dev_sgi_re.c
OUT=/tmp/kill25
PREFIX_REF=840f3d0^
say(){ echo "[$(date +%H:%M:%S)] $*"; }
die(){ say "*** ABORT: $* ***"; exit 1; }

mkdir -p "$OUT"
rm -rf "$T"; cp -a "$G/build" "$T" || die clone
mkdir -p "$T/rg"; cp "$SEC/regress/sgi_de_primop_probe.py" "$T/rg/probe.py" || die probe
cmp -s "$T/$F" "$SEC/$F" || die "clone differs from SEC"

say "checking out the TRUE pre-fix source: $PREFIX_REF"
echo "PREFIX_TRUE" > "$T/.MUTANT"
git -C "$SEC" show "$PREFIX_REF:$F" > "$T/$F" || die checkout
say "  fix marker present in that file (0 = correctly pre-fix): $(grep -c SGIRE_W_PRIM_OP "$T/$F")"
cd "$T" && rm -f src/cpus/*.o && make -j4 > "$OUT/build_PREFIX_TRUE.log" 2>&1
[ "$T/gxemul" -nt "$T/$F" ] || die "binary not newer"
( cd "$T/rg" && timeout 600 python3 -u probe.py "$T/gxemul" PREFIX_TRUE > "$OUT/PREFIX_TRUE.out" 2>&1 )
say "  $(grep -a OPUS500_RESULT "$OUT/PREFIX_TRUE.out" | head -1)"
grep -a OPUS500_RED "$OUT/PREFIX_TRUE.out" | sed 's/^/      /'

say "RESTORE + REBUILD + clear"
cp "$SEC/$F" "$T/$F"
cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED, sentinel kept"
cd "$T" && rm -f src/devices/dev_sgi_re.o && make -j4 > "$OUT/build_restore2.log" 2>&1
if [ "$T/gxemul" -nt "$T/$F" ]; then rm -f "$T/.MUTANT"; say "  restored + REBUILT, sentinel cleared"
else say "  *** rebuild stale -- SENTINEL KEPT ***"; fi
say "PREFIX25_DONE"
