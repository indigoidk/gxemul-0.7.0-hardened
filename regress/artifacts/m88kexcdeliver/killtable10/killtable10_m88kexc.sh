#!/bin/bash
# m88kexcdeliver KILL TABLE 5: the v5 probe (41 fault rows + 2 controls; 2 rows EXPECT HALT) against the pass-2 escapes and the
# repaired rows.  SCRATCH CLONE (/tmp/gxm88kexc_kill, a cp -a of build/ = the FIX build), frozen probe copy, sentinel per
# mutant, restore FROM GXEMUL-SEC (never a backup), cmp + rebuild before the sentinel is cleared.  Never touches a project tree.
set -u
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC; C=/tmp/gxm88kexc_kill; f=src/cpus/cpu_m88k.c
OUT=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/m88kexc/killtable10
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
PROBE=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/m88kexc/m88k_exc_probe.v10.frozen.py
WANT=41/41
mkdir -p "$OUT"; echo "KILLTABLE10_START $(date +%H:%M:%S)"
[ -d "$C" ] || { echo "clone absent"; exit 1; }
[ -e "$C/.MUTANT" ] && { echo "clone carries a sentinel -- restore first"; exit 1; }
cmp -s "$C/$f" "$S/$f" && echo "clone baseline == SEC (the fix)" || { echo "clone DIVERGES from SEC -- re-baselining from SEC"; cp "$S/$f" "$C/$f"; }
cp "$PROBE" "$OUT/m88k_exc_probe.frozen10.py"; echo "frozen10 md5 $(md5sum "$OUT/m88k_exc_probe.frozen10.py" | cut -c1-8)"
if ! [ "$C/gxemul" -nt "$C/$f" ]; then echo "clone binary stale -- rebuilding the baseline"; ( cd "$C/src/cpus" && rm -f cpu_m88k.o && make -s -j4 >"$OUT/build_BASE.log" 2>&1 ); ( cd "$C" && make -s -j4 >>"$OUT/build_BASE.log" 2>&1 ); fi
[ "$C/gxemul" -nt "$C/$f" ] || { echo "BASE rebuild did not produce a fresh binary"; exit 1; }
python3 -u "$OUT/m88k_exc_probe.frozen10.py" "$C/gxemul" > "$OUT/BASE.out" 2>&1; echo "BASE rc=$?"
grep -E 'M88KEXC_RESULT|SELFTEST|CONTROLS' "$OUT/BASE.out"
grep -q "M88KEXC_RESULT=$WANT" "$OUT/BASE.out" || { echo "BASE is not $WANT -- the baseline or a row is wrong, aborting"; grep -E 'M88KEXC_ROW' "$OUT/BASE.out" | grep -v 'RESULT=DELIVER\|RESULT=DONE' | cut -c1-140; exit 1; }
for M in M_ERRORFRZOFF M_SFRZTRAP10 M_FB_LO M_FBIND M_FBNOC M_SFRZTRAPUSER; do
	echo "=== $M $(date +%H:%M:%S) ==="
	echo "$f $M" > "$C/.MUTANT"
	if ! python3 "$SP/mut_m88kexc.py" "$C" "$M" > "$OUT/mut_$M.log" 2>&1; then
		echo "$M: MUTANT-TEXT-NOT-FOUND (see mut_$M.log)"; tail -2 "$OUT/mut_$M.log"; cp "$S/$f" "$C/$f"; rm -f "$C/.MUTANT"; continue
	fi
	( cd "$C/src/cpus" && rm -f cpu_m88k.o && make -s -j4 >"$OUT/build_$M.log" 2>&1 ); ( cd "$C" && make -s -j4 >>"$OUT/build_$M.log" 2>&1 )
	if [ "$C/gxemul" -nt "$C/$f" ]; then
		python3 -u "$OUT/m88k_exc_probe.frozen10.py" "$C/gxemul" > "$OUT/$M.out" 2>&1
		python3 -u /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kexcdeliver/killtable8/m88k_exc_probe.frozen8.py "$C/gxemul" > "$OUT/${M}_on_v8.out" 2>&1; echo "$M on the v8 instrument: $(grep -o 'M88KEXC_RESULT=[0-9]*/[0-9]*' "$OUT/${M}_on_v8.out")"
		echo "$M $(grep -o 'M88KEXC_RESULT=[0-9]*/[0-9]*' "$OUT/$M.out") $(grep -o 'M88KEXC_CONTROLS=BAD.*' "$OUT/$M.out")"
		python3 - "$OUT/$M.out" <<'PY'
import sys,re
exp={"resid50":"HALT","resid127":"HALT","resid11":"HALT","resid50ind":"HALT","resid50c":"HALT","sfu1h":"HALT","usfu1":"HALT"}
for l in open(sys.argv[1],encoding="utf-8",errors="replace"):
    m=re.match(r"M88KEXC_ROW=(\S+)\s+RESULT=(\S+)(.*)",l)
    if not m: continue
    name,res,rest=m.groups()
    want=exp.get(name,"DELIVER") if name not in ("live","attrib") else "DONE"
    if res!=want:
        bad=re.search(r"bad=(\S+)",rest); print("    RED %-10s %-8s %s"%(name,res,bad.group(0) if bad else ""))
PY
	else
		echo "$M: BUILD FAILED (binary not newer than source) -- see build_$M.log"; tail -3 "$OUT/build_$M.log"
	fi
	cp "$S/$f" "$C/$f"
	cmp -s "$C/$f" "$S/$f" || { echo "RESTORE FAILED -- sentinel left in place"; exit 1; }
	( cd "$C/src/cpus" && rm -f cpu_m88k.o && make -s -j4 >"$OUT/restore_$M.log" 2>&1 ); ( cd "$C" && make -s -j4 >>"$OUT/restore_$M.log" 2>&1 )
	[ "$C/gxemul" -nt "$C/$f" ] && rm -f "$C/.MUTANT" || { echo "restore rebuild stale -- sentinel left in place"; exit 1; }
done
python3 -u "$OUT/m88k_exc_probe.frozen10.py" "$C/gxemul" > "$OUT/BASE_final.out" 2>&1; grep -o 'M88KEXC_RESULT=[0-9]*/[0-9]*' "$OUT/BASE_final.out"
[ -e "$C/.MUTANT" ] && echo "SENTINEL PRESENT" || echo "clone clean: no sentinel"
echo "KILLTABLE10_DONE $(date +%H:%M:%S)"
echo "--- HEAD v10 measurement (floor a, final instrument): /tmp/gxopus501p4"
H=/tmp/gxopus501p4; git -C "$S" show HEAD:src/cpus/cpu_m88k.c > /tmp/head_cpu_m88k.c; cmp -s "$H/$f" /tmp/head_cpu_m88k.c && echo "$H cpu_m88k.c == HEAD" || echo "$H != HEAD"
python3 -u "$OUT/m88k_exc_probe.frozen10.py" "$H/gxemul" > "$OUT/../probe_v10_head.out" 2>&1; grep -E 'M88KEXC_RESULT|SELFTEST' "$OUT/../probe_v10_head.out"; grep 'M88KEXC_ROW' "$OUT/../probe_v10_head.out" | grep -v 'RESULT=HALT' | cut -c1-100
echo "--- final v10 run on the rebuilt build/ (must be 41/41)"
python3 -u "$OUT/m88k_exc_probe.frozen10.py" /mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul > "$OUT/../probe_v10_fix_final.out" 2>&1; grep -E 'M88KEXC_RESULT' "$OUT/../probe_v10_fix_final.out"
echo "KILLTABLE10_ALL_DONE $(date +%H:%M:%S)"
