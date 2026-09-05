#!/bin/bash
T=/tmp/gxopus_p3
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p3_opus
BASE=/tmp/pcc2_p3_baseline.c
SRC=$T/src/devices/dev_pcc2.c
build () {
	rm -f "$T/src/devices/dev_pcc2.o" "$T/gxemul"
	( cd "$T" && make -j4 ) > /tmp/p3ne_build.log 2>&1
	[ -x "$T/gxemul" ] || { echo "  BUILD FAILED"; tail -15 /tmp/p3ne_build.log; return 1; }
	[ "$T/gxemul" -nt "$SRC" ] || { echo "  *** STALE BINARY ***"; return 1; }
	echo "  build ok, binary -nt source"; return 0
}
echo "=== NON-EQUIVALENCE CONTROLS + PROPOSED-ROW PREVIEW ==="; date
for M in BASE MA MB MC; do
	echo; echo "### $M"
	echo "$M dev_pcc2.c" > "$T/.MUTANT"
	cp "$BASE" "$SRC"
	python3 "$OUT/mutate.py" "$M" || { echo "  MUTATE FAILED"; continue; }
	build && python3 -u "$OUT/nonequiv_check.py" "$T/gxemul" "$M" 2>&1
done
echo; echo "### FINAL RESTORE + REBUILD"
cp "$BASE" "$SRC"
if cmp -s "$SRC" "$SEC/src/devices/dev_pcc2.c"; then
	echo "  part 1: source CLEAN vs SEC"
	if build; then rm -f "$T/.MUTANT"; echo "  part 2: rebuilt, binary -nt source -- sentinel CLEARED"
	else echo "  part 2: REBUILD FAILED -- sentinel KEPT"; fi
else echo "  part 1: *** cmp FAILED -- sentinel KEPT ***"; fi
echo "### GXEMUL-SEC status (must be unchanged):"; ( cd "$SEC" && git status --porcelain | sed 's/^/    /' )
date; echo "NONEQ_ALL_DONE"
