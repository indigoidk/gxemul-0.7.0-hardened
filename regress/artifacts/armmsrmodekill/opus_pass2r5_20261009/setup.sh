# setup.sh -- Opus pass-2R5: create MY clones /tmp/gxopus562r5/{LANE1..4,HEADL} from my r4 clone.
# Never writes GXEMUL-SEC, est, build, build-asan or /tmp/gxsec-build.
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/msr/opus5
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
SRC=/tmp/gxopus562r4/LANE1/tree
R=/tmp/gxopus562r5
FILES="src/cpus/cpu_arm.c src/cpus/cpu_arm_instr.c src/cpus/cpu_arm_instr_dpi.c src/include/cpu_arm.h"
echo "--- setup $(date)"
for l in 1 2 3 4; do
  T=/tmp/gxopus562r4/LANE$l/tree
  if [ -e $T/.MUTANT ]; then echo "r4 LANE$l SENTINEL PRESENT: $(cat $T/.MUTANT)"; else echo "r4 LANE$l no sentinel"; fi
done
[ -x $SRC/gxemul ] || { echo "NO SOURCE TREE $SRC"; exit 5; }
mkdir -p $R
for L in LANE1 LANE2 LANE3 LANE4 HEADL; do
  rm -rf $R/$L; mkdir -p $R/$L
  cp -a $SRC $R/$L/tree || { echo "CP FAILED $L"; exit 6; }
  rm -f $R/$L/tree/.MUTANT
done
# baseline copies (fix = SEC working tree; head = git show HEAD exported from git-bash)
rm -rf $R/base $R/headsrc; mkdir -p $R/base/src/cpus $R/base/src/include
for f in $FILES; do cp $SEC/$f $R/base/$f; done
cp -a $S/headsrc $R/headsrc
for f in $FILES; do cmp -s $R/base/$f $SEC/$f && echo "base cmp-clean vs SEC: $f" || echo "BASE CMP FAIL $f"; done
md5sum $R/base/src/cpus/*.c $R/base/src/include/cpu_arm.h $R/headsrc/src/cpus/*.c $R/headsrc/src/include/cpu_arm.h
cp $S/probe_frozen.py $R/probe_frozen.py
md5sum $R/probe_frozen.py $SEC/regress/arm_msrmode_probe.py
df -h /tmp | tail -1
echo SETUP_DONE
