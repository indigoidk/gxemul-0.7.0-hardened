#!/bin/bash
#  PASS 3b -- the ONE shape the repair's own PRETABLE discloses as un-rowed:
#  "A guard edit that lands the write AND still announces (the M_FALL_MASK shape)
#   at one of those four [PSCALEADJ/SCCICR/SCCRX/SCSIICR] would escape."
#  Disclosed is not the same as above the floor: clause (d) says the detector MUST
#  fail when the guard is kept and its repair nulled.  Measured, not argued.
T=/tmp/gxopus_pcc2
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p2_opus/pass3
BASE2=$OUT/dev_pcc2.base2.c
PROBE=$OUT/probe.frozen.py
SRC=$T/src/devices/dev_pcc2.c
build () {
	rm -f "$T/src/devices/dev_pcc2.o" "$T/gxemul"
	( cd "$T" && make ) > /tmp/pcc2_build.log 2>&1
	[ -x "$T/gxemul" ] || { echo "  BUILD FAILED"; grep -m5 -E 'error' /tmp/pcc2_build.log; return 1; }
	[ "$T/gxemul" -nt "$SRC" ] || { echo "  *** STALE BINARY ***"; return 1; }
	echo "  build ok, binary -nt source"; return 0
}
runprobe () {
	( cd /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress \
	  && timeout 1800 python3 -u "$PROBE" "$T/gxemul" "$1" ) > "$OUT/p3_$1.out" 2>&1
	grep -E '^PCC2W_(RESULT|RED|PROBE_DONE)' "$OUT/p3_$1.out" | sed 's/^/  /'
	grep -q PCC2W_PROBE_DONE "$OUT/p3_$1.out" || echo "  *** NO SENTINEL ***"
}
for ARM in SCCICR SCCRX SCSIICR PSCALEADJ; do
	echo; echo "### M_FALL_$ARM  (announce kept, break removed -- the write LANDS)"
	echo "M_FALL_$ARM dev_pcc2.c" > "$T/.MUTANT"
	cp "$BASE2" "$SRC"
	python3 - "$ARM" <<'PYEOF'
import sys
arm = sys.argv[1]
p = "/tmp/gxopus_pcc2/src/devices/dev_pcc2.c"
s = open(p).read()
old = 'pcc2_width_decline(d, PCC2_W_%s_LEN, "PCCTWO_%s", len);\n\t\t\tbreak;' % (arm, arm)
n = s.count(old)
assert n == 1, "COUNT %d for %s" % (n, arm)
open(p, "w").write(s.replace(old,
    'pcc2_width_decline(d, PCC2_W_%s_LEN, "PCCTWO_%s", len);' % (arm, arm)))
print("  mutated: M_FALL_%s (break removed)" % arm)
PYEOF
	if build; then runprobe "M_FALL_$ARM"; fi
done
echo; echo "### RESTORE to the b78bb0f blob"
cp /tmp/pcc2_baseline.c "$SRC"
if cmp -s "$SRC" "$OUT/../dev_pcc2.b78bb0f.c"; then echo "  PART 1 OK"; build && rm -f "$T/.MUTANT" && echo "  SENTINEL CLEARED"; else echo "  PART 1 FAIL -- sentinel KEPT"; fi
echo "PASS3B_DONE"
