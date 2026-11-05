#!/bin/bash
# b123_table.sh -- qhslowifetch pass 6 (codex GPT-6 Astra, p6_20261105/codex_codex_qhs_p6.txt), MEASURED before its repair.  Adapted
# from p5_20261105/traodd_table.sh.  The read-ahead route at cpc700_pci's last word (the probe's `T ra' session: SRR0 sentinel, pc set,
# continue, -T, no breakpoint) crossed over pc's low two bits {00,01,10,11} x MSR[ME] {clear, set} = 8 cells (cell_witness.py), on the
# fix and on B1, B2, B3 (b123_variant.py, one exact edit each), plus the 82-row probe (r6_20261105/table6/probe82_frozen.py, AST-equal
# to the in-tree probe) on the clone's fix and on each variant.  Mutates ONLY /tmp/gxqhs12 (a cp -a of build/) under a clone-local
# .MUTANT sentinel; cleared only after the restore cmp's against GXEMUL-SEC and the rebuilt binary is newer than the source.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
C=/tmp/gxqhs12
R7=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/r7_20261105
OUT=$R7/b123_table
W=$R7/cell_witness.py
P=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/r6_20261105/table6/probe82_frozen.py
VP=$R7/b123_variant.py
S1=src/cpus/cpu_ppc_instr.c
S2=src/include/cpu_ppc.h
mkdir -p $OUT
rm -rf $C && cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$S1: qhslowifetch b123 table (pass-6 breaches B1 B2 B3); baseline = GXEMUL-SEC's $S1" > .MUTANT
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
wit() {
    for a in 0xfec00004 0xfec00005 0xfec00006 0xfec00007; do
        for m in 0x0 0x1000; do
            timeout 120 python3 $W $C/gxemul $1 $a $m $OUT/cells | grep '^CELL '
        done
    done
}
probe() {
    python3 -u $P $C/gxemul $1 $OUT/sessions82_$1 > $OUT/probe82_$1.out 2>&1
    grep -E '^PPC_IFETCH_(RESULT|CONTROL|SYMPTOM|RED)=' $OUT/probe82_$1.out | tr '\n' ' '; echo; tail -n 1 $OUT/probe82_$1.out
}
f=$(build base); echo "base build: $f"
[ "$f" = fresh ] || { echo "BASE BUILD NOT FRESH -- stopping; sentinel kept"; exit 5; }
wit base; probe base
for V in B1 B2 B3; do
    python3 $VP $OUT/cpu_ppc_instr.c.base $S1 $V || { echo "VARIANT $V NOT APPLIED"; continue; }
    f=$(build $V); echo "$V build: $f"
    [ "$f" = fresh ] || { echo "$V BUILD NOT FRESH -- not measured"; continue; }
    wit $V; probe $V
done
cp $OUT/cpu_ppc_instr.c.base $S1
echo "restore build: $(build restore)"
if cmp -s $S1 $G/GXEMUL-SEC/$S1 && cmp -s $S2 $G/GXEMUL-SEC/$S2 && [ gxemul -nt $S1 ] && [ gxemul -nt src/cpus/cpu_ppc.o ]; then
    rm -f .MUTANT; echo "clone restored cmp-clean against GXEMUL-SEC and rebuilt; sentinel cleared"
else
    echo "RESTORE NOT VERIFIED -- sentinel kept"
fi
md5sum $W $VP $P $OUT/cpu_ppc_instr.c.base > $OUT/MD5.txt
echo B123_TABLE_DONE
