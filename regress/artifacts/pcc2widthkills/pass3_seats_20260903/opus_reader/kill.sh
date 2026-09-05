#!/bin/bash
#  OPUS SEAT pass-3 kill table.  Runs ENTIRELY in the scratch clone /tmp/gxopus_p3.
#  Never touches GXEMUL-SEC, build/, est/ or build-asan/.
T=/tmp/gxopus_p3
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p3_opus
BASE=/tmp/pcc2_p3_baseline.c
SRC=$T/src/devices/dev_pcc2.c
PROBE=/tmp/p3_probe.frozen.py

build () {
	rm -f "$T/src/devices/dev_pcc2.o" "$T/gxemul"
	( cd "$T" && make -j4 ) > /tmp/p3_build_$1.log 2>&1
	if [ ! -x "$T/gxemul" ]; then echo "  BUILD FAILED"; tail -20 /tmp/p3_build_$1.log; return 1; fi
	if [ "$T/gxemul" -nt "$SRC" ]; then echo "  build ok, binary -nt source"; else
		echo "  *** STALE BINARY ***"; return 1; fi
	return 0
}

runprobe () {
	( cd /tmp && timeout 1800 python3 -u "$PROBE" "$T/gxemul" "$1" ) > "$OUT/p3_$1.out" 2>&1
	grep -E '^PCC2W_(RESULT|RED|PROBE_DONE)' "$OUT/p3_$1.out" | sed 's/^/  /'
	if ! grep -q PCC2W_PROBE_DONE "$OUT/p3_$1.out"; then
		echo "  *** NO COMPLETION SENTINEL -- log truncated ***"; fi
}

echo "=============================================================="
echo "pcc2widthkills OPUS pass-3 (panel seat) kill table"
echo "baseline: SEC working tree dev_pcc2.c md5 $(md5sum $BASE | cut -c1-8)"
echo "instrument frozen: $(md5sum $PROBE | cut -c1-8)"
date
echo "=============================================================="

for M in BASE MD MA MB MC; do
	echo; echo "### $M"
	echo "$M dev_pcc2.c" > "$T/.MUTANT"
	cp "$BASE" "$SRC"
	python3 "$OUT/mutate.py" "$M" || { echo "  MUTATE FAILED"; continue; }
	build "$M" && runprobe "$M"
	date +"  %H:%M:%S"
done

echo; echo "### FINAL RESTORE + REBUILD (two-part clearance)"
cp "$BASE" "$SRC"
if cmp -s "$SRC" "$SEC/src/devices/dev_pcc2.c"; then
	echo "  part 1: source CLEAN vs SEC"
	if build FINAL; then rm -f "$T/.MUTANT"; echo "  part 2: binary rebuilt and newer -- sentinel CLEARED"
	else echo "  part 2: REBUILD FAILED -- sentinel KEPT"; fi
else
	echo "  part 1: *** cmp FAILED -- sentinel KEPT ***"
fi
echo "### GXEMUL-SEC untouched check:"
( cd "$SEC" && git status --porcelain | sed 's/^/    /' )
date
echo "P3_KILL_DONE"
