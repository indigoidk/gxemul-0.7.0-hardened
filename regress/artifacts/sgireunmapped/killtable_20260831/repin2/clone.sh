#!/bin/bash
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
CLONE=/tmp/gx500r
echo "CLONE start $(date +%H:%M:%S)"
rm -rf $CLONE
mkdir -p $CLONE
#  NAME THE BASELINE.  cp -a everything except .git and the artifacts tree.
( cd $SEC && tar cf - --exclude=.git --exclude=regress/artifacts . ) | ( cd $CLONE && tar xf - )
echo "  copied.  baseline cmp of the file to be mutated:"
cmp -s $CLONE/src/devices/dev_sgi_re.c $SEC/src/devices/dev_sgi_re.c \
  && echo "  BASELINE cmp vs SEC: CLEAN  md5 $(md5sum $CLONE/src/devices/dev_sgi_re.c | cut -d' ' -f1)" \
  || { echo "  BASELINE DIFFERS -- ABORT"; exit 1; }
cd $CLONE
./configure > /tmp/gx500r_conf.log 2>&1 || { echo "CONFIGURE FAILED"; tail -20 /tmp/gx500r_conf.log; exit 1; }
echo "  configured $(date +%H:%M:%S)"
rm -f src/cpus/*.o
make -j8 > /tmp/gx500r_b0.log 2>&1
if [ ! -f $CLONE/gxemul ]; then echo "  NO BINARY -- ABORT"; tail -30 /tmp/gx500r_b0.log; exit 1; fi
if [ $CLONE/gxemul -nt $CLONE/src/devices/dev_sgi_re.c ]; then
  echo "  BASELINE BUILD: FRESH ([ binary -nt source ] = YES)"
else
  echo "  BASELINE BUILD: STALE -- ABORT"; exit 1
fi
cp $CLONE/gxemul $CLONE/gxemul.base
echo "  gxemul.base md5 $(md5sum $CLONE/gxemul.base | cut -d' ' -f1)"
echo "CLONE_DONE $(date +%H:%M:%S)"
