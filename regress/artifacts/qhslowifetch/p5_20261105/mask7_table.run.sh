#!/bin/bash
# ac_table.sh -- qhslowifetch: the repair-5 ruling's premise and repair, measured (p4_20261105/ADJ_MYTHOS.md R2: "memory_rw returns failure
# on a non-existent FETCH when -T is off" is unsettled and load-bearing).  The guest blr witness at 0x02040001 and 0x02040000, with -T
# and without, on the fix and on AC (arm (b)'s test made the aligned compare `(cpu->pc & ~(uint64_t)3) != addr`); the 69-row probe on
# AC.  Mutates ONLY /tmp/gxqhs7 (a cp -a of build/) under a clone-local .MUTANT sentinel; cleared only after the restore cmp's against
# GXEMUL-SEC and rebuilds fresh.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
C=/tmp/gxqhs9
OUT=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/p5_20261105/mask7_table
FIX=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/r5_20261105/cpu_ppc_instr.c.fix5
W=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/p5_20261105/blr_witness.py
P=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/r5_20261105/table5/probe79_frozen.py
S1=src/cpus/cpu_ppc_instr.c
mkdir -p $OUT
rm -rf $C && cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$S1: qhslowifetch mask7 table; baseline $FIX" > .MUTANT
cmp -s $S1 $FIX || { echo "clone source = baseline: NO"; exit 4; }
build() {
    rm -f src/cpus/cpu_ppc*.o
    make -j4 > $OUT/build_$1.log 2>&1
    rc=$?
    if [ $rc = 0 ] && [ src/cpus/cpu_ppc.o -nt $S1 ] && [ gxemul -nt src/cpus/cpu_ppc.o ]; then echo fresh; else echo "STALE_rc$rc"; fi
}
wit() {
    for a in 0x2040003 0x2040007; do
        (cd $OUT && timeout 120 python3 $W $C/gxemul $1 $a | grep '^BLR ')
        (cd $OUT && timeout 120 python3 $W $C/gxemul $1 $a noT | grep '^BLR ')
    done
}
echo "base build: $(build base)"; wit base
python3 - "$FIX" "$S1" <<'PYEOF'
import io, sys
T, NL = chr(9), chr(10)
s = io.open(sys.argv[1], encoding="latin-1", newline="").read()
B = T * 3 + "if ((cpu->pc & ~(uint64_t)3) != addr) {" + NL
assert s.count(B) == 1
io.open(sys.argv[2], "w", encoding="latin-1", newline="").write(s.replace(B, T * 3 + "if ((cpu->pc & ~(uint64_t)7) != addr) {" + NL))
PYEOF
echo "M7 build: $(build M7)"; wit M7
python3 -u $P $C/gxemul M7 > $OUT/probe79_M7.out 2>&1
grep -E '^PPC_IFETCH_(RESULT|CONTROL|SYMPTOM|RED)=' $OUT/probe79_M7.out
cp $FIX $S1
echo "restore build: $(build restore)"
if cmp -s $S1 $G/GXEMUL-SEC/$S1 && [ gxemul -nt $S1 ]; then rm -f .MUTANT; echo "clone restored and rebuilt; sentinel cleared"; else echo "RESTORE NOT VERIFIED -- sentinel kept"; fi
echo MASK7_TABLE_DONE
