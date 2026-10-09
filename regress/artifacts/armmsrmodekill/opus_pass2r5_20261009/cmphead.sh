# cmphead.sh -- compare MY clone's tracked src files against HEAD ef577140 (git archive export).
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/msr/opus5
T=/tmp/gxopus562r5/LANE1/tree
cd $S/headexport
n=0; d=0
for f in $(find src -type f); do
  n=$((n+1))
  if ! cmp -s $f $T/$f; then d=$((d+1)); echo "DIFFERS: $f"; fi
done
echo "compared $n HEAD files; $d differ"
