#!/usr/bin/env bash
#  NON-EQUIVALENCE CONTROL: is the escaping mutant a LIVE DEFECT or an
#  equivalent mutant?  Build BASE and M_POPP_NONE and drive LDMDB at each.
set -euo pipefail
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
REL=src/cpus/cpu_arm_instr.c
CLONE=/tmp/gxopus524c
OUT=/tmp/opus524_out
touch "$CLONE/.MUTANT"
for leg in BASE M_POPP_NONE M_POPW_WEAK M_NPMASK; do
    echo "=================== control leg $leg"
    python3 /tmp/opus524_frozen/mutate_opus.py "$leg" "$CLONE/$REL" /tmp/opus524_baseline.c
    grep -n 'memory_rw(cpu, cpu->mem' "$CLONE/$REL" | sed 's/^/   built: /'
    rm -f "$CLONE/src/cpus/"*.o
    make -C "$CLONE" -j4 > "$OUT/cbuild_${leg}.log" 2>&1
    [ "$CLONE/gxemul" -nt "$CLONE/$REL" ] || { echo "ERROR: stale binary $leg"; exit 1; }
    python3 -u /tmp/opus524_frozen/ldmdb_control.py "$CLONE/gxemul" "$leg" | tee "$OUT/ldmdb_${leg}.out"
done
echo "=== restore ==="
git -C "$SEC" show 8d372aa:"$REL" > "$CLONE/$REL"
git -C "$SEC" show 8d372aa:"$REL" | cmp -s - "$CLONE/$REL" || { echo "ERROR: restore cmp"; exit 1; }
rm -f "$CLONE/src/cpus/"*.o
make -C "$CLONE" -j4 > "$OUT/cbuild_RESTORE.log" 2>&1
[ "$CLONE/gxemul" -nt "$CLONE/$REL" ] || { echo "ERROR: stale restored binary"; exit 1; }
rm -f "$CLONE/.MUTANT"
echo "[CLEARED] source == 8d372aa, binary newer, sentinel removed"
echo OPUS524_CONTROL_DONE
