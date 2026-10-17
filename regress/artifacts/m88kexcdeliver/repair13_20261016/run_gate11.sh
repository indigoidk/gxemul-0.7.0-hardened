#!/bin/bash
# gate 11 (gate_m88k_rounding.sh, the WORKING-TREE copy = the committed form of repair 13) against a fresh HEAD build in the
# scratch clone /tmp/gxm88kv20, with its own LOGDIR so no other gate run's logs are touched.
set -u
D=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kexcdeliver/repair13_20261016
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
C=/tmp/gxm88kv20
cd $C || exit 9
[ -e $C/.MUTANT ] && { echo "SENTINEL PRESENT -- abort"; exit 9; }
cmp -s src/cpus/cpu_m88k.c $S/m88kv20/cpu_m88k.c.HEAD || { echo "clone source is not HEAD -- abort"; exit 9; }
rm -f src/cpus/cpu_m88k.o; make -j8 > $D/build_gate11_base.out 2>&1
[ gxemul -nt src/cpus/cpu_m88k.c ] || { echo "REBUILD STALE"; exit 9; }
md5sum src/cpus/cpu_m88k.c gxemul | tee $D/gate11_base.md5
export LOGDIR=/tmp/gxregress_m88kv20; rm -rf $LOGDIR; mkdir -p $LOGDIR
echo "== gate 11 start $(date '+%T')"
PMAX=$C/gxemul bash /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gate_m88k_rounding.sh > $D/gate11.out 2>&1
echo "gate rc=$?" | tee -a $D/gate11.out
mkdir -p $D/gate11_logs && cp $LOGDIR/*.log $D/gate11_logs/ 2>/dev/null
echo "== gate 11 end $(date '+%T')"; tail -5 $D/gate11.out
echo "GATE11_RUN_DONE"
