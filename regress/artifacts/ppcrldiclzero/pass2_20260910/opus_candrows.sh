#!/bin/bash
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/op522
CLONE=/tmp/gxop522
SRC=src/cpus/cpu_ppc_instr.c
exec > >(tee "$SP/candrows.log") 2>&1
python3 "$SP/patch_probe.py" "$SEC/regress/ppc_rldicl_probe.py" "$SP/probe_plus3.py" || exit 9
echo "CANDIDATE-ROW TABLE: does +3 rows close BOTH measured escapes?"
for leg in BASE M_SH5 M_CR0 M_ORIG; do
    echo "===== $leg ====="
    cp "$SP/baseline_cpu_ppc_instr.c" "$CLONE/$SRC"
    echo "$SRC $leg-candrows" > "$CLONE/.MUTANT"
    python3 "$SP/mutate_op.py" "$CLONE/$SRC" "$leg" || exit 9
    rm -f "$CLONE"/src/cpus/*.o "$CLONE/gxemul"; ( cd "$CLONE" && make -j4 ) > "$SP/build_cr_$leg.log" 2>&1
    if [ "$CLONE/gxemul" -nt "$CLONE/$SRC" ]; then echo "  binary=FRESH"; else echo "  binary=STALE ABORT"; exit 2; fi
    python3 "$SP/probe_plus3.py" "$CLONE/gxemul" "$leg" > "$SP/plus3_$leg.raw" 2>&1
    grep -E '^sh63|^sh32|^rc cr0' "$SP/plus3_$leg.raw" | sed 's/^/  /'
    grep -E '^SCORE ' "$SP/plus3_$leg.raw" | sed 's/^/  /'
    grep -E '^FAILING' "$SP/plus3_$leg.raw" | sed 's/^/  /'
    tail -1 "$SP/plus3_$leg.raw" | sed 's/^/  sentinel=/'
done
echo "===== RESTORE ====="
cp "$SP/baseline_cpu_ppc_instr.c" "$CLONE/$SRC"
cmp -s "$CLONE/$SRC" "$SEC/$SRC" && echo "  cmp-vs-SEC: CLEAN" || echo "  cmp-vs-SEC: DIRTY"
rm -f "$CLONE"/src/cpus/*.o "$CLONE/gxemul"; ( cd "$CLONE" && make -j4 ) > "$SP/build_cr_RESTORE.log" 2>&1
if [ "$CLONE/gxemul" -nt "$CLONE/$SRC" ]; then echo "  binary=FRESH"; rm -f "$CLONE/.MUTANT"; echo "  SENTINEL CLEARED (both parts verified)"; else echo "  binary=STALE -- SENTINEL KEPT"; fi
python3 "$SP/probe_plus3.py" "$CLONE/gxemul" RESTORED > "$SP/plus3_RESTORED.raw" 2>&1
grep -E '^SCORE ' "$SP/plus3_RESTORED.raw" | sed 's/^/  /'
echo "CANDROWS_DONE"
