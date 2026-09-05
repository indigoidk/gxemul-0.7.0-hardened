#!/bin/bash
#  OPUS SEAT pass-2, TABLE 2: per-arm scoped mutants + validation of the proposed repair.
T=/tmp/gxopus_pcc2
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p2_opus
BASE=/tmp/pcc2_baseline.c
SRC=$T/src/devices/dev_pcc2.c
mkdir -p "$OUT"

restore () {
	cp "$BASE" "$SRC"
	if cmp -s "$SRC" "$SEC/src/devices/dev_pcc2.c"; then
		rm -f "$T/.MUTANT"; echo "  restore: source CLEAN vs SEC"
	else echo "  restore: *** FAILED -- sentinel KEPT ***"; fi
}
build () {
	rm -f "$T/src/devices/dev_pcc2.o" "$T/gxemul"
	( cd "$T" && make ) > /tmp/pcc2_build.log 2>&1
	if [ ! -x "$T/gxemul" ]; then echo "  BUILD FAILED"; tail -20 /tmp/pcc2_build.log; return 1; fi
	if [ "$T/gxemul" -nt "$SRC" ]; then echo "  build ok, binary -nt source"; else
		echo "  *** STALE BINARY ***"; return 1; fi
	return 0
}
runprobe () {
	L="$1"
	( cd "$SEC/regress" && timeout 1800 python3 -u pcc2_width_probe.py "$T/gxemul" "$L" ) \
	    > "$OUT/probe_$L.out" 2>&1
	grep -E '^PCC2W_(RESULT|RED|PROBE_DONE)' "$OUT/probe_$L.out" | sed 's/^/  /'
	grep -q PCC2W_PROBE_DONE "$OUT/probe_$L.out" || echo "  *** NO SENTINEL -- truncated ***"
}
mutate () {
	python3 - "$1" <<'PYEOF'
import sys
tag = sys.argv[1]
p = "/tmp/gxopus_pcc2/src/devices/dev_pcc2.c"
s = open(p).read()
G = "if (len != 1 && writeflag == MEM_WRITE) {"
def one(old, new):
    global s
    n = s.count(old)
    assert n == 1, "PATTERN COUNT %d (want 1) for %r" % (n, old[:70])
    s = s.replace(old, new)
if tag == "M1":
    one('pcc2_width_decline(d, PCC2_W_SCCTX_LEN, "PCCTWO_SCCTX", len);',
        'pcc2_width_decline(d, PCC2_W_SCCRX_LEN, "PCCTWO_SCCTX", len);')
elif tag == "M8":
    one('\t\t' + G + '\n\t\t\tpcc2_width_decline(d, PCC2_W_SCCTX_LEN, "PCCTWO_SCCTX", len);\n\t\t\tbreak;\n\t\t}\n', '')
elif tag == "M9":
    one('\t\t' + G + '\n\t\t\tpcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);\n\t\t\tbreak;\n\t\t}\n', '')
elif tag == "M10":
    one("\tif (!(d->warned & (1u << bit))) {\n\t\td->warned |= (1u << bit);",
        "\tstatic uint32_t gwarned = 0;\n\t(void) d;\n\tif (!(gwarned & (1u << bit))) {\n\t\tgwarned |= (1u << bit);")
else:
    raise SystemExit("unknown tag " + tag)
open(p, "w").write(s)
print("  mutated: " + tag)
PYEOF
}
echo "=== TABLE 2 (per-arm scoped) ==="; date
for M in M8 M9 M10; do
	echo; echo "### $M"
	echo "$M dev_pcc2.c" > "$T/.MUTANT"
	cp "$BASE" "$SRC"
	if mutate "$M"; then if build; then runprobe "$M"; fi; else echo "  MUTATE FAILED"; fi
	restore
done

echo; echo "=== PROPOSED REPAIR, VALIDATED IN BOTH DIRECTIONS ==="
echo "### repair row on BASE (want 12/12)"
restore; build && python3 -u "$OUT/latchall_check.py" "$T/gxemul" BASE 2>&1 | sed 's/^/  /'
echo "### repair row on M1 (the clean-sweep mutant -- want a DROP)"
echo "M1 dev_pcc2.c" > "$T/.MUTANT"
cp "$BASE" "$SRC"; mutate M1 && build && python3 -u "$OUT/latchall_check.py" "$T/gxemul" M1 2>&1 | sed 's/^/  /'
echo "### repair row on M9 (MASK guard deleted -- want a DROP)"
echo "M9 dev_pcc2.c" > "$T/.MUTANT"
cp "$BASE" "$SRC"; mutate M9 && build && python3 -u "$OUT/latchall_check.py" "$T/gxemul" M9 2>&1 | sed 's/^/  /'

echo; echo "### FINAL RESTORE + REBUILD"
restore; build
echo "KILLTABLE2_DONE"
