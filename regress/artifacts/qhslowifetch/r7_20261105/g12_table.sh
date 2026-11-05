#!/bin/bash
# g12_table.sh -- qhslowifetch pass 6, the Gemini 4 Argon seat's G1 and G2 (_scratchpad/gweb/jobs_20261105_rounds/p6_qhs/), MEASURED
# before any row is added for them: the 82-row probe (r6_20261105/table6/probe82_frozen.py, AST-equal to the in-tree probe) on the fix
# and on G1 (arm (b)'s compare made `cpu->pc < addr`) and G2 (arm (d)'s test made `cpu->cd.ppc.msr`), one exact edit each
# (g12_variant.py); plus g12_explore.py's two MSR[IP] sessions on the ISI setup on the fix and on G1.  Same discipline as
# b123_table.sh: ONLY /tmp/gxqhs12 is mutated (a fresh cp -a of build/), under a clone-local .MUTANT sentinel cleared only after the
# restore cmp's against GXEMUL-SEC and the rebuilt binary is newer than the source.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
C=/tmp/gxqhs12
R7=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/r7_20261105
OUT=$R7/g12_table
X=$R7/g12_explore.py
P=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/r6_20261105/table6/probe82_frozen.py
VP=$R7/g12_variant.py
S1=src/cpus/cpu_ppc_instr.c
S2=src/include/cpu_ppc.h
mkdir -p $OUT
rm -rf $C && cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$S1: qhslowifetch g12 table (Gemini pass-6 G1 G2); baseline = GXEMUL-SEC's $S1" > .MUTANT
cmp -s $S1 $G/GXEMUL-SEC/$S1 || { echo "clone $S1 = GXEMUL-SEC: NO"; exit 4; }
cmp -s $S2 $G/GXEMUL-SEC/$S2 || { echo "clone $S2 = GXEMUL-SEC: NO"; exit 4; }
echo "clone sources = GXEMUL-SEC: yes ($S1, $S2)"
cp $S1 $OUT/cpu_ppc_instr.c.base
build() {
    rm -f src/cpus/cpu_ppc*.o
    make -j4 > $OUT/build_$1.log 2>&1
    rc=$?
    if [ $rc = 0 ] && [ src/cpus/cpu_ppc.o -nt $S1 ] && [ gxemul -nt src/cpus/cpu_ppc.o ]; then echo fresh; else echo "STALE_rc$rc"; fi
}
probe() {
    python3 -u $P $C/gxemul $1 $OUT/sessions82_$1 > $OUT/probe82_$1.out 2>&1
    grep -E '^PPC_IFETCH_(RESULT|CONTROL|SYMPTOM|RED)=' $OUT/probe82_$1.out | tr '\n' ' '; echo; tail -n 1 $OUT/probe82_$1.out
}
f=$(build base); echo "base build: $f"
[ "$f" = fresh ] || { echo "BASE BUILD NOT FRESH -- stopping; sentinel kept"; exit 5; }
probe base; timeout 200 python3 $X $C/gxemul base $OUT/explore
for V in G1 G2; do
    python3 $VP $OUT/cpu_ppc_instr.c.base $S1 $V || { echo "VARIANT $V NOT APPLIED"; continue; }
    f=$(build $V); echo "$V build: $f"
    [ "$f" = fresh ] || { echo "$V BUILD NOT FRESH -- not measured"; continue; }
    probe $V
    [ $V = G1 ] && timeout 200 python3 $X $C/gxemul $V $OUT/explore
done
cp $OUT/cpu_ppc_instr.c.base $S1
echo "restore build: $(build restore)"
if cmp -s $S1 $G/GXEMUL-SEC/$S1 && cmp -s $S2 $G/GXEMUL-SEC/$S2 && [ gxemul -nt $S1 ] && [ gxemul -nt src/cpus/cpu_ppc.o ]; then
    rm -f .MUTANT; echo "clone restored cmp-clean against GXEMUL-SEC and rebuilt; sentinel cleared"
else
    echo "RESTORE NOT VERIFIED -- sentinel kept"
fi
md5sum $X $VP $P $OUT/cpu_ppc_instr.c.base > $OUT/MD5.txt
echo G12_TABLE_DONE
