#!/bin/bash
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CL=/tmp/gxfable_p3
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p3_fable
echo "=== 1. clone build/ ==="
rm -rf "$CL"
cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$CL" || { echo "CLONE FAILED"; exit 9; }
touch "$CL/.MUTANT"   # sentinel: throwaway clone, will be rm -rf'd
echo "=== 2. put the REPAIRED (uncommitted) dev_pcc2.c into the clone ==="
cp "$SEC/src/devices/dev_pcc2.c" "$CL/src/devices/dev_pcc2.c"
cp "$SEC/regress/pcc2_width_probe.py" "$CL/pcc2_width_probe.frozen.py"
echo "probe md5: $(md5sum "$CL/pcc2_width_probe.frozen.py" | cut -c1-8) (want cd22f951)"
echo "=== 3. build BASE (repaired source, unmutated) ==="
cd "$CL" || exit 9
rm -f src/devices/dev_pcc2.o
make -j4 >"$OUT/build_base.log" 2>&1
if [ ! -x gxemul ] || [ ! gxemul -nt src/devices/dev_pcc2.c ]; then echo "BASE BUILD STALE/FAILED"; tail -8 "$OUT/build_base.log"; exit 9; fi
[ -x gxemul ] && echo "BASE binary built: $(ls -la gxemul | awk '{print $5, $6, $7, $8}')" || { echo "NO BASE BINARY"; exit 9; }
echo "--- BASE probe (expect 82/82) ---"
python3 -u pcc2_width_probe.frozen.py "$CL/gxemul" base > "$OUT/probe_base.out" 2>&1
grep -E 'PCC2W_RESULT|PCC2W_RED|PCC2W_PROBE_DONE' "$OUT/probe_base.out"
echo "=== 4. apply M_FALL_VECBASE: remove the VECBASE arm's decline break ==="
python3 - <<'PY'
f="src/devices/dev_pcc2.c"
s=open(f).read()
orig=s
# Target the break; immediately after the VECBASE width-decline call.
needle='pcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);\n\t\t\tbreak;'
repl ='pcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);\n\t\t\t/* M_FALL_VECBASE: break removed */'
assert needle in s, "NEEDLE NOT FOUND"
s=s.replace(needle,repl,1)
assert s!=orig, "UNCHANGED"
open(f,"w").write(s)
print("mutation applied: VECBASE decline break removed")
PY
if ! cmp -s src/devices/dev_pcc2.c "$SEC/src/devices/dev_pcc2.c"; then echo "mutator DID change the file (good)"; else echo "MUTATOR NO-OP -- ABORT"; exit 9; fi
echo "=== 5. build M_FALL_VECBASE ==="
rm -f src/devices/dev_pcc2.o
make -j4 >"$OUT/build_mfall.log" 2>&1
[ gxemul -nt src/devices/dev_pcc2.c ] && echo "MUTANT binary fresh" || { echo "MUTANT BUILD STALE/FAILED"; tail -5 "$OUT/build_mfall.log"; exit 9; }
echo "--- M_FALL_VECBASE probe (escape => 82/82; caught => <82) ---"
python3 -u pcc2_width_probe.frozen.py "$CL/gxemul" mfall_vecbase > "$OUT/probe_mfall_vecbase.out" 2>&1
grep -E 'PCC2W_RESULT|PCC2W_RED|PCC2W_PROBE_DONE' "$OUT/probe_mfall_vecbase.out"
echo "=== 6. direct evidence: op vecbase session under mutant lands into VECBASE ==="
grep -nE '^(op vecbase|op vecbase dcl|rb vecbase|latch all|latch all lv)  ' "$OUT/probe_mfall_vecbase.out"
echo "=== 7. cleanup: delete clone (never touched GXEMUL-SEC) ==="
cd /tmp && rm -rf "$CL" && echo "clone removed; GXEMUL-SEC untouched by construction"
echo "MFALL_VECBASE_DONE"
