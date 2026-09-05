#!/bin/bash
#  PASS 3c -- the 82-row repair (3 readbacks + op pscale noig) owes its own pass 2.
#  Does it KILL the announce-then-land shape at all four previously-uncovered arms?
#  Frozen 82-row instrument; product BASE3 = the same source pass 3 used.
T=/tmp/gxopus_pcc2
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p2_opus/pass3c
BASE3=$OUT/dev_pcc2.base3.c
PROBE=$OUT/probe82.frozen.py
REF=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p2_opus/dev_pcc2.b78bb0f.c
SRC=$T/src/devices/dev_pcc2.c
build () {
	rm -f "$T/src/devices/dev_pcc2.o" "$T/gxemul"
	( cd "$T" && make ) > /tmp/pcc2_build.log 2>&1
	[ -x "$T/gxemul" ] || { echo "  BUILD FAILED"; grep -m5 -E 'error' /tmp/pcc2_build.log; return 1; }
	[ "$T/gxemul" -nt "$SRC" ] || { echo "  *** STALE BINARY ***"; return 1; }
	echo "  build ok"; return 0
}
runprobe () {
	( cd /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress \
	  && timeout 1800 python3 -u "$PROBE" "$T/gxemul" "$1" ) > "$OUT/p3c_$1.out" 2>&1
	grep -E '^PCC2W_(RESULT|RED|PROBE_DONE)' "$OUT/p3c_$1.out" | sed 's/^/  /'
	grep -q PCC2W_PROBE_DONE "$OUT/p3c_$1.out" || echo "  *** NO SENTINEL ***"
}
echo "=== PASS 3c: announce-then-land vs the 82-row detector ==="; date
echo; echo "### BASE3 (want 82/82)"
echo "BASE3 dev_pcc2.c" > "$T/.MUTANT"; cp "$BASE3" "$SRC"; build && runprobe BASE3
for ARM in SCCICR SCCRX SCSIICR PSCALEADJ; do
	echo; echo "### M_FALL_$ARM vs 82 rows (want RED)"
	echo "M_FALL_$ARM dev_pcc2.c" > "$T/.MUTANT"
	cp "$BASE3" "$SRC"
	python3 - "$ARM" <<'PYEOF'
import sys
arm = sys.argv[1]
p = "/tmp/gxopus_pcc2/src/devices/dev_pcc2.c"
s = open(p).read()
old = 'pcc2_width_decline(d, PCC2_W_%s_LEN, "PCCTWO_%s", len);\n\t\t\tbreak;' % (arm, arm)
assert s.count(old) == 1, "COUNT %d for %s" % (s.count(old), arm)
open(p, "w").write(s.replace(old,
    'pcc2_width_decline(d, PCC2_W_%s_LEN, "PCCTWO_%s", len);' % (arm, arm)))
print("  mutated: M_FALL_%s" % arm)
PYEOF
	build && runprobe "M_FALL_$ARM"
done
echo; echo "### RESTORE to the b78bb0f blob"
cp /tmp/pcc2_baseline.c "$SRC"
if cmp -s "$SRC" "$REF"; then echo "  PART 1 OK"; build && rm -f "$T/.MUTANT" && echo "  SENTINEL CLEARED"; else echo "  PART 1 FAIL -- sentinel KEPT"; fi
echo "PASS3C_DONE"
