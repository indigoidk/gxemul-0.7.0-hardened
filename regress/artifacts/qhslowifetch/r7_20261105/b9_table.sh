#!/bin/bash
# b9_table.sh -- qhslowifetch repair 9, MEASURED before any row is added: the 137-row probe (table9/probe137_frozen.py, the table-9
# record) on the fix and on b9_variant.py's five edits -- pass 8's B1 (an MSR[ME] toggle on pc's low bits 01 at the top of the block), its
# 00/10/11 forms and an SRR0 toggle at 01.  Same discipline as b7b_table.sh: ONLY /tmp/gxqhs12 is mutated (a fresh cp -a of build/), under a
# clone-local .MUTANT sentinel cleared only after the restore cmp's against GXEMUL-SEC and the rebuilt binary is newer than the source.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
C=/tmp/gxqhs12
R7=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/r7_20261105
OUT=$R7/b9_table
P=$R7/table9/probe137_frozen.py
VP=$R7/b9_variant.py
S1=src/cpus/cpu_ppc_instr.c
S2=src/include/cpu_ppc.h
mkdir -p $OUT
rm -rf $C && cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$S1: qhslowifetch b9 table (repair 9: pass-8 B1 family); baseline = GXEMUL-SEC's $S1" > .MUTANT
cmp -s $S1 $G/GXEMUL-SEC/$S1 || { echo "clone $S1 = GXEMUL-SEC: NO"; exit 4; }
cmp -s $S2 $G/GXEMUL-SEC/$S2 || { echo "clone $S2 = GXEMUL-SEC: NO"; exit 4; }
cmp -s $S1 $R7/cpu_ppc_instr.c.fix7 || { echo "GXEMUL-SEC's $S1 != fix7: NO"; exit 4; }
echo "clone sources = GXEMUL-SEC = fix7: yes"
cp $S1 $OUT/cpu_ppc_instr.c.base
build() {
    rm -f src/cpus/cpu_ppc*.o
    make -j4 > $OUT/build_$1.log 2>&1
    rc=$?
    if [ $rc = 0 ] && [ src/cpus/cpu_ppc.o -nt $S1 ] && [ gxemul -nt src/cpus/cpu_ppc.o ]; then echo fresh; else echo "STALE_rc$rc"; fi
}
probe() {
    python3 -B -u $P $C/gxemul $1 $OUT/sessions137_$1 > $OUT/probe137_$1.out 2>&1
    echo "$1 $(grep '^PPC_IFETCH_RESULT=' $OUT/probe137_$1.out | cut -d= -f2) $(grep '^PPC_IFETCH_CONTROL=' $OUT/probe137_$1.out) $(grep '^PPC_IFETCH_SYMPTOM=' $OUT/probe137_$1.out) $(tail -n 1 $OUT/probe137_$1.out) $(grep '^PPC_IFETCH_RED=' $OUT/probe137_$1.out)"
}
f=$(build base); echo "base build: $f"
[ "$f" = fresh ] || { echo "BASE BUILD NOT FRESH -- stopping; sentinel kept"; exit 5; }
probe base
for V in R9_tog_me1 R9_tog_me2 R9_tog_me0 R9_tog_me3 R9_tog_srr0_1; do
    python3 -B $VP $OUT/cpu_ppc_instr.c.base $S1 $V || { echo "VARIANT $V NOT APPLIED"; continue; }
    f=$(build $V)
    [ "$f" = fresh ] || { echo "$V BUILD NOT FRESH ($f) -- not measured"; continue; }
    probe $V
done
cp $OUT/cpu_ppc_instr.c.base $S1
echo "restore build: $(build restore)"
if cmp -s $S1 $G/GXEMUL-SEC/$S1 && cmp -s $S2 $G/GXEMUL-SEC/$S2 && [ gxemul -nt $S1 ] && [ gxemul -nt src/cpus/cpu_ppc.o ]; then
    rm -f .MUTANT; echo "clone restored cmp-clean against GXEMUL-SEC and rebuilt; sentinel cleared"
else
    echo "RESTORE NOT VERIFIED -- sentinel kept"
fi
md5sum $VP $P $OUT/cpu_ppc_instr.c.base > $OUT/MD5.txt
echo B9_TABLE_DONE
