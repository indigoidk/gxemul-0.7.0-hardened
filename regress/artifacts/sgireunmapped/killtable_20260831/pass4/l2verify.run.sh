#!/bin/bash
#  #499 pass 4 L2 REPAIR VERIFICATION.
#
#  The repair is discharged only by a MEASURED KILL, never by existing.  Required:
#      base  50/50   (the two new rows pass on the fix)
#      E0W   < 50    (it scored 48/48 TOTAL ESCAPE against the 48-row version)
#      E0    < 50
#
#  Re-freezes the instrument first: the clone still holds the 48-row copy, and a
#  comparison run owes ONE instrument.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
T=/tmp/gx499f
F=src/devices/dev_sgi_re.c
OUT=/tmp/kill50
say(){ echo "[$(date +%H:%M:%S)] $*"; }
die(){ say "*** ABORT: $* ***"; exit 1; }

mkdir -p "$OUT"
cd "$T" || die cd
cmp -s "$T/$F" "$SEC/$F" || die "clone is not at baseline"
say "baseline cmp vs SEC: CLEAN"

cp "$SEC/regress/sgi_re_unmapped_probe.py" "$T/rg/probe.py" || die "probe copy"
say "instrument RE-FROZEN: $(wc -c < "$T/rg/probe.py") bytes"

score () {
    local label="$1"
    rm -f src/devices/dev_sgi_re.o
    make -j4 > "$OUT/build_$label.log" 2>&1
    [ "$T/gxemul" -nt "$T/$F" ] || { say "  $label: binary not newer -- SKIP"; return 1; }
    ( cd "$T/rg" && timeout 700 python3 -u probe.py "$T/gxemul" "$label" > "$OUT/$label.out" 2>&1 )
    local ok fail
    ok=$(grep -ac " ok\$" "$OUT/$label.out"); fail=$(grep -ac " FAIL\$" "$OUT/$label.out")
    say "  $label: ok=$ok fail=$fail  $(grep -a OPUS499T_RESULT "$OUT/$label.out" | head -1)"
    [ "$fail" -gt 0 ] && grep -a ' FAIL$' "$OUT/$label.out" | cut -c1-18 | sed 's/^/      RED /'
    return 0
}

say "BASE -- expect 50/50, both new rows green on the fix"
cp "$SEC/$F" "$T/$F"
rm -f src/cpus/*.o
score base

say "E0W -- the mutant that swept 48 rows CLEAN.  It must now REDDEN."
echo "E0W announce-then-exit0 write arm only" > "$T/.MUTANT"
cp "$SEC/$F" "$T/$F"
python3 "$SEC/../_scratchpad/e0_mut.py" write || die "E0W mutator"
score E0W

say "E0 -- both directions"
echo "E0 announce-then-exit0 both directions" > "$T/.MUTANT"
cp "$SEC/$F" "$T/$F"
python3 "$SEC/../_scratchpad/e0_mut.py" both || die "E0 mutator"
score E0

say "RESTORE from SEC + REBUILD + verify both clearance parts"
cp "$SEC/$F" "$T/$F"
cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED, sentinel kept"
rm -f src/devices/dev_sgi_re.o; make -j4 > "$OUT/build_restore.log" 2>&1
if [ "$T/gxemul" -nt "$T/$F" ]; then rm -f "$T/.MUTANT"; say "  restored + REBUILT, sentinel cleared"
else say "  *** rebuild stale -- SENTINEL KEPT ***"; fi
say "L2VERIFY_DONE"
