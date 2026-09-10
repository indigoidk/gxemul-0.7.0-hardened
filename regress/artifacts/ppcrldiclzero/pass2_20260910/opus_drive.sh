#!/bin/bash
#  Opus pass-2 seat, #522.  Runs ENTIRELY in a /tmp clone.  Never writes GXEMUL-SEC.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/op522
CLONE=/tmp/gxop522
SRC=src/cpus/cpu_ppc_instr.c
OUT=$SP/table.txt

exec > >(tee "$SP/drive.log") 2>&1
echo "OPUS PASS-2 INDEPENDENT KILL TABLE -- #522 ppcrldiclzero  $(date -u +%FT%TZ)"

rm -rf "$CLONE"; mkdir -p "$CLONE"
echo "cloning (excluding .git and _scratchpad) ..."
( cd "$SEC" && tar cf - --exclude=./.git --exclude=./_scratchpad . ) | ( cd "$CLONE" && tar xf - )
echo "clone done: $(du -sh "$CLONE" | cut -f1)"

#  NAME THE BASELINE: the round's post-fix WORKING SET (GXEMUL-SEC as it stands),
#  which is what pass 2 is reviewing.  cmp it before mutant 1.
if cmp -s "$CLONE/$SRC" "$SEC/$SRC"; then echo "BASELINE cmp-vs-SEC: CLEAN"; else echo "BASELINE cmp-vs-SEC: DIRTY -- ABORT"; exit 1; fi
cp "$CLONE/$SRC" "$SP/baseline_cpu_ppc_instr.c"
cp "$SEC/regress/ppc_rldicl_probe.py" "$SP/probe.frozen.py"   # frozen-copy rule

: > "$OUT"
for leg in BASE M_ORIG M_SH5 M_MB5 M_ROTAMT M_CR0; do
    echo "===== LEG $leg  $(date -u +%T) ====="
    cp "$SP/baseline_cpu_ppc_instr.c" "$CLONE/$SRC"
    echo "$SRC $leg" > "$CLONE/.MUTANT"
    python3 "$SP/mutate_op.py" "$CLONE/$SRC" "$leg"; mrc=$?
    if [ "$mrc" != 0 ]; then echo "  MUTATE FAILED rc=$mrc -- ABORT"; exit 9; fi
    rm -f "$CLONE"/src/cpus/*.o "$CLONE/gxemul"
    ( cd "$CLONE" && make -j4 ) > "$SP/build_$leg.log" 2>&1
    brc=$?
    if [ -f "$CLONE/gxemul" ] && [ "$CLONE/gxemul" -nt "$CLONE/$SRC" ]; then fresh=FRESH; else fresh=STALE; fi
    echo "  build rc=$brc  binary=$fresh"
    if [ "$fresh" != FRESH ]; then echo "  BINARY NOT FRESH -- ABORT"; exit 2; fi
    python3 "$SP/probe.frozen.py" "$CLONE/gxemul" "$leg" > "$SP/probe_$leg.raw" 2>&1
    sc=$(grep -E '^SCORE ' "$SP/probe_$leg.raw" | tail -1)
    fl=$(grep -E '^FAILING: ' "$SP/probe_$leg.raw" | tail -1)
    sn=$(tail -1 "$SP/probe_$leg.raw")
    echo "  $sc"
    echo "  $fl"
    echo "  sentinel=[$sn]"
    printf '%-10s %-22s %s\n' "$leg" "$sc" "${fl#FAILING: }" >> "$OUT"
done

echo "===== RESTORE ====="
cp "$SP/baseline_cpu_ppc_instr.c" "$CLONE/$SRC"
if cmp -s "$CLONE/$SRC" "$SEC/$SRC"; then echo "  restore cmp-vs-SEC: CLEAN"; else echo "  restore cmp-vs-SEC: DIRTY"; fi
rm -f "$CLONE"/src/cpus/*.o "$CLONE/gxemul"
( cd "$CLONE" && make -j4 ) > "$SP/build_RESTORE.log" 2>&1
if [ -f "$CLONE/gxemul" ] && [ "$CLONE/gxemul" -nt "$CLONE/$SRC" ]; then echo "  binary=FRESH"; rm -f "$CLONE/.MUTANT"; echo "  SENTINEL CLEARED (both parts verified)"; else echo "  binary=STALE -- SENTINEL KEPT"; fi
python3 "$SP/probe.frozen.py" "$CLONE/gxemul" RESTORED > "$SP/probe_RESTORED.raw" 2>&1
grep -E '^SCORE ' "$SP/probe_RESTORED.raw" | tail -1
printf '%-10s %-22s %s\n' RESTORED "$(grep -E '^SCORE ' "$SP/probe_RESTORED.raw" | tail -1)" "" >> "$OUT"

echo "===== SUMMARY ====="
cat "$OUT"
echo "OPUS522_TABLE_DONE"
