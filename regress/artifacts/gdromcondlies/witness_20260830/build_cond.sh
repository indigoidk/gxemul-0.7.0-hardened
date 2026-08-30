#!/bin/bash
#  Build the gdromcondlies WITNESS baseline: an UNMODIFIED copy of GXEMUL-SEC HEAD 8404520.
#  NO MUTATION -- this tree is never edited, so no .MUTANT sentinel is owed.
T=/tmp/gxopus_cond
SRC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC

cd "$T" || exit 9

echo "=== BASELINE IDENTITY (must be clean against GXEMUL-SEC HEAD) ==="
cmp "$T/src/devices/dev_dreamcast_gdrom.c" "$SRC/src/devices/dev_dreamcast_gdrom.c" \
  && echo "CMP_CLEAN dev_dreamcast_gdrom.c" || echo "CMP_DIRTY dev_dreamcast_gdrom.c"

echo "=== CONFIGURE ==="
./configure > /tmp/gxopus_cond_conf.log 2>&1
echo "CONF_RC=$?"
tail -3 /tmp/gxopus_cond_conf.log

echo "=== CLEAN CPU OBJECTS (conservative, per carrier) ==="
rm -f src/cpus/*.o

echo "=== MAKE ==="
make -j4 > /tmp/gxopus_cond_make.log 2>&1
echo "MAKE_RC=$?"
tail -5 /tmp/gxopus_cond_make.log

echo "=== FRESHNESS: MAKE_RC has been observed lying, so check the binary ==="
ls -la "$T/gxemul" 2>/dev/null || echo "NO BINARY"
if [ -f "$T/gxemul" ] && [ "$T/gxemul" -nt "$T/src/devices/dev_dreamcast_gdrom.c" ]; then
    echo "BINARY_FRESH yes"
else
    echo "BINARY_FRESH NO -- DO NOT MEASURE"
fi
echo "BUILD_COND_DONE"
