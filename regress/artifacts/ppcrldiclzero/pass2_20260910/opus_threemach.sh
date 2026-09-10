#!/bin/bash
#  Opus pass-2 seat: settle the brief's/product comment's THREE-MACHINE claim.
#  Runs one rldicl and one srdi on each of the three machines the comment names,
#  on a PRE-FIX and a POST-FIX binary built in the same clone.  Read-only w.r.t. SEC.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/op522
CLONE=/tmp/gxop522
SRC=src/cpus/cpu_ppc_instr.c
exec > >(tee "$SP/threemach.log") 2>&1
printf '\x00\x00\x00\x00' > /tmp/op522_dummy.bin

run3 () {   # $1 = label
  for spec in "bareppc:" "testppc:" "macppc:g5"; do
    m=${spec%%:*}; sub=${spec##*:}
    args=(-V -x -E "$m" -M 64)
    [ -n "$sub" ] && args+=(-e "$sub")
    args+=("0x10000:/tmp/op522_dummy.bin")
    out=$(printf 'r3=0xdeadbeefcafef00d\nr4=0x5a5a5a5a5a5a5a5a\nr5=0x5a5a5a5a5a5a5a5a\nput w 0x10000, 0x78640020\nput w 0x10004, 0x7865f842\npc=0x10000\nstep 2\nreg\nquit\n' | "$CLONE/gxemul" "${args[@]}" 2>&1)
    cpu=$(echo "$out" | grep -o 'cpu: PPC[0-9A-Za-z]*' | head -1)
    r4=$(echo "$out" | grep -oE 'r04 = 0x[0-9a-f]+' | tail -1)
    r5=$(echo "$out" | grep -oE 'r05 = 0x[0-9a-f]+' | tail -1)
    unimpl=$(echo "$out" | grep -c 'UNIMPLEMENTED')
    printf '  %-8s %-4s %-16s %-24s %-24s unimpl=%s\n' "$m" "$sub" "$cpu" "${r4:-NONE}" "${r5:-NONE}" "$unimpl"
  done
}

echo "WANT (architecture, manual :29736/:29744):"
echo "  r4 = rldicl r4,r3,0,32  = 0xcafef00d          (clrldi r4,r3,32)"
echo "  r5 = rldicl r5,r3,63,1  = 0x6f56df77e57f7806  (srdi r5,r3,1 -- SH=63, NEEDS the sh5 bit)"
echo ""
echo "=== POST-FIX (the shipped repair) ==="
cp "$SP/baseline_cpu_ppc_instr.c" "$CLONE/$SRC"
rm -f "$CLONE"/src/cpus/*.o "$CLONE/gxemul"; ( cd "$CLONE" && make -j4 ) > "$SP/build_3M_FIX.log" 2>&1
[ "$CLONE/gxemul" -nt "$CLONE/$SRC" ] && echo "  binary=FRESH" || { echo "  binary=STALE ABORT"; exit 2; }
run3 fix

echo ""
echo "=== PRE-FIX (M_ORIG: the committed defect verbatim) ==="
echo "$SRC M_ORIG-3machine" > "$CLONE/.MUTANT"
python3 "$SP/mutate_op.py" "$CLONE/$SRC" M_ORIG || exit 9
rm -f "$CLONE"/src/cpus/*.o "$CLONE/gxemul"; ( cd "$CLONE" && make -j4 ) > "$SP/build_3M_ORIG.log" 2>&1
[ "$CLONE/gxemul" -nt "$CLONE/$SRC" ] && echo "  binary=FRESH" || { echo "  binary=STALE ABORT"; exit 2; }
run3 orig

echo ""
echo "=== M_SH5 (drop the sh5 bit: the mutant that scored 19/19) ==="
cp "$SP/baseline_cpu_ppc_instr.c" "$CLONE/$SRC"
python3 "$SP/mutate_op.py" "$CLONE/$SRC" M_SH5 || exit 9
rm -f "$CLONE"/src/cpus/*.o "$CLONE/gxemul"; ( cd "$CLONE" && make -j4 ) > "$SP/build_3M_SH5.log" 2>&1
[ "$CLONE/gxemul" -nt "$CLONE/$SRC" ] && echo "  binary=FRESH" || { echo "  binary=STALE ABORT"; exit 2; }
run3 sh5

echo ""
echo "=== RESTORE ==="
cp "$SP/baseline_cpu_ppc_instr.c" "$CLONE/$SRC"
cmp -s "$CLONE/$SRC" "$SEC/$SRC" && echo "  cmp-vs-SEC: CLEAN" || echo "  cmp-vs-SEC: DIRTY"
rm -f "$CLONE"/src/cpus/*.o "$CLONE/gxemul"; ( cd "$CLONE" && make -j4 ) > "$SP/build_3M_RESTORE.log" 2>&1
if [ "$CLONE/gxemul" -nt "$CLONE/$SRC" ]; then echo "  binary=FRESH"; rm -f "$CLONE/.MUTANT"; echo "  SENTINEL CLEARED (both parts verified)"; else echo "  binary=STALE -- SENTINEL KEPT"; fi
echo "THREEMACH_DONE"
