#!/bin/bash
# b7b_table.sh -- qhslowifetch repair 7b, MEASURED before any row is added: the 103-row probe (table7/probe103_frozen.py, the
# table-7 record) on the fix and on each of b7b_variant.py's eight edits -- the four channel-gap candidates (SRR0 written, the
# checkstop line printed, pc aligned, running restored -- each in arm (a) only when pc != addr) and the four failure-test
# narrowings (&& ME, && !ME, && translation_readahead, && pc != addr).  Same discipline as b123_table.sh: ONLY /tmp/gxqhs12 is
# mutated (a fresh cp -a of build/), under a clone-local .MUTANT sentinel cleared only after the restore cmp's against GXEMUL-SEC
# and the rebuilt binary is newer than the source.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
C=/tmp/gxqhs12
R7=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/r7_20261105
OUT=$R7/b7b_table
P=$R7/table7/probe103_frozen.py
VP=$R7/b7b_variant.py
S1=src/cpus/cpu_ppc_instr.c
S2=src/include/cpu_ppc.h
mkdir -p $OUT
rm -rf $C && cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$S1: qhslowifetch b7b table (repair 7b candidates); baseline = GXEMUL-SEC's $S1" > .MUTANT
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
    python3 -B -u $P $C/gxemul $1 $OUT/sessions103_$1 > $OUT/probe103_$1.out 2>&1
    echo "$1 $(grep '^PPC_IFETCH_RESULT=' $OUT/probe103_$1.out | cut -d= -f2) $(grep '^PPC_IFETCH_CONTROL=' $OUT/probe103_$1.out) $(grep '^PPC_IFETCH_SYMPTOM=' $OUT/probe103_$1.out) $(tail -n 1 $OUT/probe103_$1.out) $(grep '^PPC_IFETCH_RED=' $OUT/probe103_$1.out)"
}
f=$(build base); echo "base build: $f"
[ "$f" = fresh ] || { echo "BASE BUILD NOT FRESH -- stopping; sentinel kept"; exit 5; }
probe base
for V in R7b_a_srr0un R7b_a_chkun R7b_a_pcalign R7b_a_runun R7b_f_me R7b_f_meclr R7b_f_ra R7b_f_unal; do
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
echo B7B_TABLE_DONE
