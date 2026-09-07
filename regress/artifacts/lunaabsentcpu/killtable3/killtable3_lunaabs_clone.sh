#!/bin/bash
# lunaabsentcpu (#503) kill table, SCRATCH-CLONE-WITH-FIX form: SEC does NOT yet carry #503 (the #502 round is uncommitted and shares
# the record files), so the baseline is RE-DERIVED inside the clone from SEC's dev_luna88k.c + fix_lunaabs.py -- at table start and after
# every mutant (a derivation from the repo source, never a backup).  Sentinel per mutant; cmp + rebuild before it is cleared.  Never
# touches a project tree.  Invoke: MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/.../killtable_lunaabs_clone.sh   (run_in_background)
set -u
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SRC=/mnt/c/DocumentNoSnc/CC/GXEMUL/build
C=/tmp/gxlunaabs_kill
OUT=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/lunaabs/killtable3
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
IMAGES=/mnt/c/DocumentNoSnc/CC/GXEMUL/_images
HEADBIN=/tmp/gxopus501p4
f=src/devices/dev_luna88k.c
mkdir -p "$OUT"
echo "KILLTABLE_START $(date +%H:%M:%S)"
cmp -s "$SRC/$f" "$S/$f" || { echo "build/ $f DIVERGES from SEC -- refusing"; exit 1; }
grep -q 'd->ncpus = devinit->machine->ncpus' "$S/$f" && { echo "SEC already carries #503 -- use the in-place driver instead"; exit 1; }
rm -rf "$C"; cp -a "$SRC" "$C" || exit 1
derive_baseline() {  # SEC source + the fix script == the baseline; verified against the first derivation
	cp "$S/$f" "$C/$f" && python3 "$SP/fix_lunaabs.py" "$C" > /dev/null || { echo "fix_lunaabs.py FAILED on the clone"; exit 1; }
}
derive_baseline; cp "$C/$f" "$OUT/baseline_dev_luna88k.c"; echo "baseline = SEC + fix_lunaabs.py, md5 $(md5sum "$OUT/baseline_dev_luna88k.c" | cut -c1-8)"
grep -c 'ncpus' "$OUT/baseline_dev_luna88k.c" | sed 's/^/baseline ncpus mentions: /'
cp /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/lunaabs/luna_absentcpu_probe.py "$OUT/luna_absentcpu_probe.frozen.py"
echo "frozen md5 $(md5sum "$OUT/luna_absentcpu_probe.frozen.py" | cut -c1-8)"
rebuild() { ( cd "$C/src/devices" && rm -f dev_luna88k.o && make -s -j4 >"$1" 2>&1 ); ( cd "$C" && make -s -j4 >>"$1" 2>&1 ); }
rebuild "$OUT/build_BASE.log"
[ "$C/gxemul" -nt "$C/$f" ] || { echo "BASE rebuild did not produce a fresh binary"; tail -3 "$OUT/build_BASE.log"; exit 1; }
python3 -u "$OUT/luna_absentcpu_probe.frozen.py" "$C/gxemul" "$IMAGES" > "$OUT/BASE.out" 2>&1; echo "BASE rc=$?"
grep -E 'LUNAABS_RESULT|LUNA_ABSENTCPU_WITNESS' "$OUT/BASE.out"
grep -q 'LUNA_ABSENTCPU_WITNESS=PASS' "$OUT/BASE.out" || { echo "BASE is not PASS -- the baseline or a row is wrong, aborting"; grep 'LUNAABS_ROW' "$OUT/BASE.out" | grep -v 'RESULT=OK' | cut -c1-160; exit 1; }
WANT=$(grep -o 'LUNAABS_RESULT=[0-9]*/[0-9]*' "$OUT/BASE.out" | cut -d= -f2)
for M in M_SWLATCH M_NODEASSERT M_NOCLEAR M_DEASSERT0 M_SKIP2 M_MASK30 M_SWONLY M_IRQACTIVE0 M_AND1 M_MIN2 M_REVERT M_OFFBY1 M_NOASSIGN M_HARD1 M_SKIP1 M_NULLA M_NULLAB M_LATCH M_GUARDASSERT M_CALLGUARD M_NOREASSERT; do
	echo "=== $M $(date +%H:%M:%S) ==="
	echo "$f $M" > "$C/.MUTANT"
	if ! python3 "$SP/mut_lunaabs.py" "$C" "$M" > "$OUT/mut_$M.log" 2>&1; then
		echo "$M: MUTANT-TEXT-NOT-FOUND (see mut_$M.log)"; tail -2 "$OUT/mut_$M.log"
		derive_baseline; rm -f "$C/.MUTANT"; continue
	fi
	rebuild "$OUT/build_$M.log"
	if [ "$C/gxemul" -nt "$C/$f" ]; then
		python3 -u "$OUT/luna_absentcpu_probe.frozen.py" "$C/gxemul" "$IMAGES" > "$OUT/$M.out" 2>&1
		echo "$M $(grep -o 'LUNAABS_RESULT=[0-9]*/[0-9]*' "$OUT/$M.out") (BASE $WANT) $(grep -o 'LUNA_ABSENTCPU_WITNESS=[A-Z_]*' "$OUT/$M.out")"
		grep 'LUNAABS_ROW' "$OUT/$M.out" | grep -v 'RESULT=OK' | awk '{print "    RED", $1, $2}' | head -14
	else
		echo "$M: BUILD FAILED (binary not newer than source) -- see build_$M.log"; tail -3 "$OUT/build_$M.log"
	fi
	derive_baseline
	cmp -s "$C/$f" "$OUT/baseline_dev_luna88k.c" || { echo "RESTORE FAILED (re-derivation differs from the first) -- sentinel left in place"; exit 1; }
	rebuild "$OUT/restore_$M.log"
	[ "$C/gxemul" -nt "$C/$f" ] && rm -f "$C/.MUTANT" || { echo "restore rebuild stale -- sentinel left in place"; exit 1; }
done
python3 -u "$OUT/luna_absentcpu_probe.frozen.py" "$C/gxemul" "$IMAGES" > "$OUT/BASE_final.out" 2>&1
grep -E 'LUNAABS_RESULT|LUNA_ABSENTCPU_WITNESS' "$OUT/BASE_final.out"
[ -e "$C/.MUTANT" ] && echo "SENTINEL PRESENT" || echo "clone clean: no sentinel"
echo "KILLTABLE_DONE $(date +%H:%M:%S)"
echo "--- HEAD witness with this instrument: $HEADBIN"
git -C "$S" show HEAD:src/devices/dev_luna88k.c > /tmp/head_dev_luna88k.c; cmp -s "$HEADBIN/$f" /tmp/head_dev_luna88k.c && echo "$HEADBIN $f == HEAD" || echo "$HEADBIN $f != HEAD -- witness NOT attributable"
python3 -u "$OUT/luna_absentcpu_probe.frozen.py" "$HEADBIN/gxemul" "$IMAGES" > "$OUT/../probe_v4_head.out" 2>&1
grep -E 'LUNAABS_RESULT|LUNA_ABSENTCPU_WITNESS' "$OUT/../probe_v4_head.out"; grep 'LUNAABS_ROW' "$OUT/../probe_v4_head.out" | grep -v 'RESULT=OK' | cut -c1-140
echo "KILLTABLE_ALL_DONE $(date +%H:%M:%S)"
