#!/bin/bash
T=/tmp/gxopus_p5
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p5_opus
M="$1"
echo "=============== MUTANT $M ==============="
echo "opus p5 kill table: $M -- baseline = GXEMUL-SEC working tree (b78bb0f + uncommitted)" > "$T/.MUTANT"
cp "$SEC/src/devices/dev_pcc2.c" "$T/src/devices/dev_pcc2.c" || exit 9
python3 "$SP/mutate.py" "$M" || exit 9
echo "--- mutation proof in SOURCE ---"
grep -n 'warned & (1u <<' "$T/src/devices/dev_pcc2.c" | head -20
grep -c 'if (len != 1 && writeflag == MEM_WRITE' "$T/src/devices/dev_pcc2.c" | sed 's/^/guards remaining: /'
cd "$T" || exit 9
rm -f src/devices/dev_pcc2.o
make -j4 > "$T/build_$M.log" 2>&1
echo "MAKE_RC=$?"
if [ "$T/gxemul" -nt "$T/src/devices/dev_pcc2.c" ]; then echo "PART2 FRESH"; else echo "PART2 STALE -- ABORT"; exit 9; fi
bash "$SP/runprobe.sh" "$M"
