#!/bin/bash
#  PASS 3 -- the repair made in response to my pass 2 owes its own pass 2.
#  Re-runs my SIX clean sweeps against the REPAIRED 78-row detector.
#  Instrument FROZEN (probe.frozen.py) so all seven runs share one instrument.
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
mutate () {
	python3 - "$1" <<'PYEOF'
import sys
tag = sys.argv[1]; BS = chr(92)
p = "/tmp/gxopus_pcc2/src/devices/dev_pcc2.c"
s = open(p).read()
G = "if (len != 1 && writeflag == MEM_WRITE) {"
def one(old, new):
    global s
    n = s.count(old); assert n == 1, "COUNT %d for %r" % (n, old[:70])
    s = s.replace(old, new)
if tag == "BASE2":
    pass
elif tag == "M1":
    one('pcc2_width_decline(d, PCC2_W_SCCTX_LEN, "PCCTWO_SCCTX", len);',
        'pcc2_width_decline(d, PCC2_W_SCCRX_LEN, "PCCTWO_SCCTX", len);')
elif tag == "M2":
    one(G + '\n\t\t\tpcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);',
        'if (len > 2 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);')
elif tag == "M6":
    one('pcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);\n\t\t\tbreak;',
        'pcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);')
elif tag == "M7":
    one(G + '\n\t\t\tpcc2_width_decline(d, PCC2_W_IPL_LEN, "PCCTWO_IPL", len);\n\t\t\tbreak;',
        'if (len != 1) {\n\t\t\tfatal("TODO: pcc2: non-byte access to PCCTWO_IPL' + BS + 'n");\n\t\t\texit(1);')
elif tag == "M8":
    one('\t\t' + G + '\n\t\t\tpcc2_width_decline(d, PCC2_W_SCCTX_LEN, "PCCTWO_SCCTX", len);\n\t\t\tbreak;\n\t\t}\n', '')
elif tag == "M9":
    one('\t\t' + G + '\n\t\t\tpcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);\n\t\t\tbreak;\n\t\t}\n', '')
else:
    raise SystemExit("unknown " + tag)
open(p, "w").write(s)
print("  mutated: " + tag)
PYEOF
}
echo "=== PASS 3: six sweeps vs the REPAIRED 78-row detector ==="; date
for M in BASE2 M1 M2 M6 M7 M8 M9; do
	echo; echo "### $M"
	echo "$M dev_pcc2.c" > "$T/.MUTANT"
	cp "$BASE2" "$SRC"
	if mutate "$M"; then if build; then runprobe "$M"; fi; fi
done
echo; echo "### RESTORE to the b78bb0f blob"
cp /tmp/pcc2_baseline.c "$SRC"
if cmp -s "$SRC" "$OUT/../dev_pcc2.b78bb0f.c"; then echo "  PART 1 OK"; build && rm -f "$T/.MUTANT" && echo "  SENTINEL CLEARED"; else echo "  PART 1 FAIL -- sentinel KEPT"; fi
echo "PASS3_DONE"
