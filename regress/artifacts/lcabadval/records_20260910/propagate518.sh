set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_lca.c
echo "=== #518 propagation + two-part clearance, $(date) ==="
for tree in /mnt/c/DocumentNoSnc/CC/GXEMUL/build-asan /tmp/gxsec-build; do
  cp $SEC $tree/src/devices/dev_lca.c
  cd $tree || { echo "$tree: MISSING"; continue; }
  rm -f src/devices/dev_lca.o
  make -j4 > /tmp/prop518_$(basename $tree).log 2>&1; rc=$?
  p1=$(cmp -s src/devices/dev_lca.c $SEC && echo CLEAN || echo DIVERGENT)
  p2=$([ gxemul -nt src/devices/dev_lca.c ] && echo FRESH || echo STALE)
  echo "$tree  make_rc=$rc  part1=$p1  part2=$p2"
done
cd /mnt/c/DocumentNoSnc/CC/GXEMUL/build; echo "build/  part1=$(cmp -s src/devices/dev_lca.c $SEC && echo CLEAN || echo DIVERGENT)  part2=$([ gxemul -nt src/devices/dev_lca.c ] && echo FRESH || echo STALE)"
echo "est/  part1=$(cmp -s /mnt/c/DocumentNoSnc/CC/GXEMUL/est/src/devices/dev_lca.c $SEC && echo CLEAN || echo DIVERGENT)  part2=N/A (source tree)"
echo "PROPAGATE518_DONE $(date)"
