#!/bin/sh
#  ctlq_20260909 step 1: fresh scratch clone + baseline rebuild.
set -x
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CL=/tmp/gxopusctlq
rm -rf "$CL"
cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$CL"
echo "=== BASELINE IDENTITY: clone dev_pcc2.c vs SEC HEAD copy ==="
if cmp "$CL/src/devices/dev_pcc2.c" "$SEC/src/devices/dev_pcc2.c"; then
    echo "CMP_CLONE_VS_SEC=IDENTICAL"
else
    echo "CMP_CLONE_VS_SEC=DIFFERS -- copying SEC over the clone"
    cp "$SEC/src/devices/dev_pcc2.c" "$CL/src/devices/dev_pcc2.c"
    cmp "$CL/src/devices/dev_pcc2.c" "$SEC/src/devices/dev_pcc2.c" && echo "CMP_AFTER_COPY=IDENTICAL"
fi
echo "=== BASELINE REBUILD IN THE CLONE ==="
cd "$CL" || exit 9
rm -f src/devices/dev_pcc2.o
make -j4 > /tmp/ctlq_build_base.log 2>&1
echo "MAKE_RC=$?"
tail -3 /tmp/ctlq_build_base.log
ls -la "$CL/gxemul" "$CL/src/devices/dev_pcc2.c"
if [ "$CL/gxemul" -nt "$CL/src/devices/dev_pcc2.c" ]; then
    echo "FRESHNESS=OK  (binary -nt source)"
else
    echo "FRESHNESS=STALE"
fi
