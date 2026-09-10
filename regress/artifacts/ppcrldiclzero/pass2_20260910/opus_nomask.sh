#!/bin/bash
#  One extra leg: the edit the CURRENT product comment warns about but no leg tests --
#  deleting `& tmp2' POST-FIX, which ships ROTL64 with the mask ignored.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/op522
CLONE=/tmp/gxop522
SRC=src/cpus/cpu_ppc_instr.c
exec > >(tee "$SP/nomask.log") 2>&1
#  re-baseline against SEC AS IT STANDS NOW (the main loop made a comment-only edit
#  mid-review; re-freeze so this leg is measured against the current file)
cp "$SEC/$SRC" "$SP/baseline2_cpu_ppc_instr.c"
python3 - <<'PY'
import io
p="/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/op522/baseline2_cpu_ppc_instr.c"
s=io.open(p,encoding="utf-8",newline="").read()
T=chr(9)
old=T+"cpu->cd.ppc.gpr[ra] = tmp & tmp2;\n"
new=T+"cpu->cd.ppc.gpr[ra] = tmp;\n"
assert s.count(old)==1, "MUTANT-TEXT-NOT-FOUND count=%d"%s.count(old)
io.open("/tmp/nomask.c","w",encoding="utf-8",newline="").write(s.replace(old,new))
print("M_NOMASK prepared")
PY
echo "$SRC M_NOMASK" > "$CLONE/.MUTANT"
cp /tmp/nomask.c "$CLONE/$SRC"
rm -f "$CLONE"/src/cpus/*.o "$CLONE/gxemul"; ( cd "$CLONE" && make -j4 ) > "$SP/build_NOMASK.log" 2>&1
[ "$CLONE/gxemul" -nt "$CLONE/$SRC" ] && echo "binary=FRESH" || { echo "binary=STALE ABORT"; exit 2; }
python3 "$SP/probe.frozen.py" "$CLONE/gxemul" M_NOMASK > "$SP/probe_M_NOMASK.raw" 2>&1
grep -E '^SCORE |^FAILING' "$SP/probe_M_NOMASK.raw"
tail -1 "$SP/probe_M_NOMASK.raw"
echo "=== RESTORE (to SEC AS IT STANDS NOW) ==="
cp "$SP/baseline2_cpu_ppc_instr.c" "$CLONE/$SRC"
cmp -s "$CLONE/$SRC" "$SEC/$SRC" && echo "  cmp-vs-SEC: CLEAN" || echo "  cmp-vs-SEC: DIRTY"
rm -f "$CLONE"/src/cpus/*.o "$CLONE/gxemul"; ( cd "$CLONE" && make -j4 ) > "$SP/build_NOMASK_RESTORE.log" 2>&1
if [ "$CLONE/gxemul" -nt "$CLONE/$SRC" ]; then echo "  binary=FRESH"; rm -f "$CLONE/.MUTANT"; echo "  SENTINEL CLEARED (both parts verified)"; else echo "  binary=STALE -- SENTINEL KEPT"; fi
python3 "$SP/probe.frozen.py" "$CLONE/gxemul" RESTORED2 > "$SP/probe_RESTORED2.raw" 2>&1
grep -E '^SCORE ' "$SP/probe_RESTORED2.raw"
echo "NOMASK_DONE"
