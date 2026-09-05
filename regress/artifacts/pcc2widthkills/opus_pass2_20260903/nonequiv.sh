#!/bin/bash
#  NON-EQUIVALENCE CONTROLS for the two clean sweeps.  Runs LAST, alone.
T=/tmp/gxopus_pcc2
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p2_opus
BASE=/tmp/pcc2_baseline.c
SRC=$T/src/devices/dev_pcc2.c
build () {
	rm -f "$T/src/devices/dev_pcc2.o" "$T/gxemul"
	( cd "$T" && make ) > /tmp/pcc2_build.log 2>&1
	[ -x "$T/gxemul" ] || { echo "  BUILD FAILED"; tail -15 /tmp/pcc2_build.log; return 1; }
	[ "$T/gxemul" -nt "$SRC" ] || { echo "  *** STALE BINARY ***"; return 1; }
	echo "  build ok, binary -nt source"; return 0
}
edit () {
	python3 - "$1" <<'PYEOF'
import sys
tag = sys.argv[1]
p = "/tmp/gxopus_pcc2/src/devices/dev_pcc2.c"
s = open(p).read()
G = "if (len != 1 && writeflag == MEM_WRITE) {"
def one(old, new):
    global s
    n = s.count(old); assert n == 1, "COUNT %d for %r" % (n, old[:70])
    s = s.replace(old, new)
if tag == "M1":
    one('pcc2_width_decline(d, PCC2_W_SCCTX_LEN, "PCCTWO_SCCTX", len);',
        'pcc2_width_decline(d, PCC2_W_SCCRX_LEN, "PCCTWO_SCCTX", len);')
elif tag == "M2":
    one(G + '\n\t\t\tpcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);',
        'if (len > 2 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);')
elif tag != "BASE":
    raise SystemExit("unknown " + tag)
open(p, "w").write(s)
PYEOF
}
echo "=== NON-EQUIVALENCE CONTROLS ==="; date
for M in BASE M1 M2; do
	echo; echo "### $M"
	echo "$M dev_pcc2.c" > "$T/.MUTANT"
	cp "$BASE" "$SRC"
	edit "$M" || { echo "  EDIT FAILED"; continue; }
	build && python3 -u "$OUT/maskland_check.py" "$T/gxemul" "$M" 2>&1 | sed 's/^/  /'
done
echo; echo "### FINAL RESTORE + REBUILD"
cp "$BASE" "$SRC"
if cmp -s "$SRC" "$SEC/src/devices/dev_pcc2.c"; then rm -f "$T/.MUTANT"; echo "  restore: CLEAN vs SEC"
else echo "  restore: *** FAILED -- sentinel KEPT ***"; fi
build
echo "NONEQUIV_DONE"
