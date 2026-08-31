#!/bin/bash
set -u
CLONE=/tmp/gx500r
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
echo "FULL REBUILD start $(date +%H:%M:%S)"
echo "  reason: the tar inherited 224 .o files from SEC.  They are common-mode"
echo "  across all three variants and cannot create a false DIFFERENCE, but a"
echo "  stale object would make all three wrong the same way relative to HEAD."
echo "  Removing the question rather than reasoning about it."
cd $CLONE
find . -name '*.o' -delete
echo "  .o remaining: $(find . -name '*.o' | wc -l)"
make -j8 > /tmp/gx500r_bfull.log 2>&1
if [ ! -f $CLONE/gxemul ]; then echo "  NO BINARY -- ABORT"; tail -30 /tmp/gx500r_bfull.log; exit 1; fi
if [ $CLONE/gxemul -nt $CLONE/src/devices/dev_sgi_re.c ]; then
  echo "  FULL BUILD: FRESH ([ binary -nt source ] = YES)"
else
  echo "  FULL BUILD: STALE -- ABORT"; exit 1
fi
cp $CLONE/gxemul $CLONE/gxemul.base
echo "  gxemul.base md5 $(md5sum $CLONE/gxemul.base | cut -d' ' -f1)"
echo "  objects now: $(find . -name '*.o' | wc -l)"
echo ""
echo "=== SEPARATE AUDIT: is GXEMUL-SEC itself carrying STALE objects? ==="
echo "(reported for the coordinator; it changes nothing in this measurement)"
n=0
for c in $(find $SEC/src -name '*.c'); do
  o="${c%.c}.o"
  if [ -f "$o" ] && [ "$c" -nt "$o" ]; then
    echo "  STALE: $(echo $o | sed "s|$SEC/||")  (source newer than object)"
    n=$((n+1))
  fi
done
echo "  stale objects in SEC: $n"
echo "FULL_REBUILD_DONE $(date +%H:%M:%S)"
