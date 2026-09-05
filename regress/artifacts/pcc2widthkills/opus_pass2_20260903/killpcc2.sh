#!/bin/bash
#  OPUS SEAT pass-2 kill table for pcc2widthkills (b78bb0f).
#  Runs ENTIRELY in the scratch clone /tmp/gxopus_pcc2.  Never touches GXEMUL-SEC,
#  build/, est/ or build-asan/.
T=/tmp/gxopus_pcc2
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p2_opus
BASE=/tmp/pcc2_baseline.c
SRC=$T/src/devices/dev_pcc2.c

mkdir -p "$OUT"

restore () {
	cp "$BASE" "$SRC"
	if cmp -s "$SRC" "$SEC/src/devices/dev_pcc2.c"; then
		rm -f "$T/.MUTANT"
		echo "  restore: source CLEAN vs SEC"
	else
		echo "  restore: *** FAILED -- sentinel KEPT ***"
	fi
}

build () {
	rm -f "$T/src/devices/dev_pcc2.o" "$T/gxemul"
	( cd "$T" && make ) > /tmp/pcc2_build.log 2>&1
	if [ ! -x "$T/gxemul" ]; then
		echo "  BUILD FAILED"; tail -20 /tmp/pcc2_build.log; return 1
	fi
	if [ "$T/gxemul" -nt "$SRC" ]; then echo "  build ok, binary -nt source"; else
		echo "  *** STALE BINARY ***"; return 1; fi
	return 0
}

runprobe () {
	L="$1"
	( cd "$SEC/regress" && timeout 1800 python3 -u pcc2_width_probe.py "$T/gxemul" "$L" ) \
	    > "$OUT/probe_$L.out" 2>&1
	grep -E '^PCC2W_(RESULT|RED|PROBE_DONE)' "$OUT/probe_$L.out" | sed 's/^/  /'
	if ! grep -q PCC2W_PROBE_DONE "$OUT/probe_$L.out"; then
		echo "  *** NO COMPLETION SENTINEL -- log is truncated ***"; fi
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
elif tag == "M2":
    one(G + '\n\t\t\tpcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);',
        'if (len > 2 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);')
elif tag == "M3":
    assert s.count(G) == 12, s.count(G)
    s = s.replace(G, "if (len > 2 && writeflag == MEM_WRITE) {")
elif tag == "M4":
    assert s.count(G) == 12, s.count(G)
    s = s.replace(G, "if (len != 1 && writeflag != MEM_READ) {")
elif tag == "M5":
    one("if (!(d->warned & (1u << bit))) {",
        "if (!(d->warned & (1u << bit)) || len) {")
elif tag == "M6":
    one('pcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);\n\t\t\tbreak;',
        'pcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);')
elif tag == "M7":
    one(G + '\n\t\t\tpcc2_width_decline(d, PCC2_W_IPL_LEN, "PCCTWO_IPL", len);\n\t\t\tbreak;',
        'if (len != 1) {\n\t\t\tfatal("TODO: pcc2: non-byte access to PCCTWO_IPL\n");\n\t\t\texit(1);')
else:
    raise SystemExit("unknown tag " + tag)
open(p, "w").write(s)
print("  mutated: " + tag)
PYEOF
}

echo "=============================================================="
echo "pcc2widthkills OPUS pass-2 kill table"
echo "baseline: b78bb0f dev_pcc2.c, cmp-clean vs SEC before mutant 1"
date
echo "=============================================================="

echo; echo "### BASE (unmodified clone)"
build && runprobe BASE

for M in M1 M2 M3 M4 M5 M6 M7; do
	echo; echo "### $M"
	echo "$M dev_pcc2.c" > "$T/.MUTANT"
	cp "$BASE" "$SRC"
	if mutate "$M"; then
		if build; then runprobe "$M"; fi
	else
		echo "  MUTATE FAILED"
	fi
	restore
done

echo; echo "### FINAL RESTORE + REBUILD"
restore
build
echo "KILLTABLE_DONE"
