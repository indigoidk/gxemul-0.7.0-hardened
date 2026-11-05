#!/bin/bash
# blr_table.sh -- qhslowifetch pass 4: the guest-made unaligned-pc route (BLR_NOTE.md) on the fix, V2 (arm (b) deleted), D11 (arm (b)'s
# refresh removed) and CB (a candidate repair: the park `if (!cpu->running)` tested BEFORE arm (b)); the 69-row probe also runs on CB.
# Mutates ONLY /tmp/gxqhs6 (a cp -a of build/) under a clone-local .MUTANT sentinel, cleared only after the restore cmp's against
# GXEMUL-SEC and rebuilds fresh.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
C=/tmp/gxqhs6
OUT=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/p4_20261105/blr_table
FIX=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/r3_20261105/cpu_ppc_instr.c.fix4
V4=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/r4_20261105/qhs_variants_4.py
W=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/p4_20261105/blr_witness.py
P=$G/GXEMUL-SEC/regress/ppc_ifetch_probe.py
S1=src/cpus/cpu_ppc_instr.c
mkdir -p $OUT
rm -rf $C && cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$S1: qhslowifetch pass-4 blr table; baseline $FIX" > .MUTANT
cmp -s $S1 $FIX || { echo "clone source = baseline: NO"; exit 4; }
build() {
    rm -f src/cpus/cpu_ppc*.o
    make -j4 > $OUT/build_$1.log 2>&1
    rc=$?
    if [ $rc = 0 ] && [ src/cpus/cpu_ppc.o -nt $S1 ] && [ gxemul -nt src/cpus/cpu_ppc.o ]; then echo fresh; else echo "STALE_rc$rc"; fi
}
wit() {   # label
    for a in 0x2040000 0x2040001; do
        (cd $OUT && timeout 120 python3 $W $C/gxemul $1 $a | grep '^BLR ')
    done
}
echo "base build: $(build base)"; wit base
for v in V2_b_del D11_b_noref; do
    python3 $V4 apply $v $FIX $S1 || { echo "$v APPLY FAILED"; continue; }
    echo "$v build: $(build $v)"; wit $v
done
python3 - "$FIX" "$S1" <<'PYEOF'
import io, sys
T, NL = chr(9), chr(10)
s = io.open(sys.argv[1], encoding="latin-1", newline="").read()
B = T * 3 + "if (cpu->pc != addr) {" + NL
assert s.count(B) == 1
park = T * 3 + "if (!cpu->running) {" + NL + T * 4 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL + T * 4 + "return;" + NL + T * 3 + "}" + NL
io.open(sys.argv[2], "w", encoding="latin-1", newline="").write(s.replace(B, park + B))
PYEOF
echo "CB build: $(build CB)"; wit CB
python3 -u $P $C/gxemul CB > $OUT/probe69_CB.out 2>&1
grep -E '^PPC_IFETCH_(RESULT|CONTROL|SYMPTOM|RED)=' $OUT/probe69_CB.out
cp $FIX $S1
echo "restore build: $(build restore)"
if cmp -s $S1 $G/GXEMUL-SEC/$S1 && [ gxemul -nt $S1 ]; then rm -f .MUTANT; echo "clone restored and rebuilt; sentinel cleared"; else echo "RESTORE NOT VERIFIED -- sentinel kept"; fi
echo BLR_TABLE_DONE
