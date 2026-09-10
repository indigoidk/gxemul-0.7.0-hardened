#!/bin/sh
#  ctlq step 6: RESTORE FROM SEC (never from a backup), REBUILD, verify BOTH parts, clear sentinel.
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CL=/tmp/gxopusctlq
cp "$SEC/src/devices/dev_pcc2.c" "$CL/src/devices/dev_pcc2.c"
cd "$CL" || exit 9
rm -f src/devices/dev_pcc2.o
make -j4 > /tmp/ctlq_build_restore.log 2>&1
echo "MAKE_RC=$?"
echo "=== PART 1: cmp clone source against SEC ==="
if cmp "$CL/src/devices/dev_pcc2.c" "$SEC/src/devices/dev_pcc2.c"; then
    echo "CMP=CLEAN (no output above = identical)"
    P1=ok
else
    echo "CMP=DIFFERS"; P1=bad
fi
echo "=== PART 2: [ binary -nt source ] ==="
ls -la "$CL/gxemul" "$CL/src/devices/dev_pcc2.c"
if [ "$CL/gxemul" -nt "$CL/src/devices/dev_pcc2.c" ]; then echo "NT=OK"; P2=ok; else echo "NT=STALE"; P2=bad; fi
if [ "$P1" = ok ] && [ "$P2" = ok ]; then
    rm -f "$CL/.MUTANT"
    echo "SENTINEL CLEARED"
else
    echo "SENTINEL KEPT -- clearance failed"
fi
ls -la "$CL/.MUTANT" 2>/dev/null || echo "ls: /tmp/gxopusctlq/.MUTANT: No such file or directory"
echo "=== the project build tree was never touched; prove it ==="
cmp /mnt/c/DocumentNoSnc/CC/GXEMUL/build/src/devices/dev_pcc2.c "$SEC/src/devices/dev_pcc2.c" && echo "build/ CMP=CLEAN"
[ /mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul -nt /mnt/c/DocumentNoSnc/CC/GXEMUL/build/src/devices/dev_pcc2.c ] && echo "build/ NT=OK" || echo "build/ NT=STALE"
ls -la /mnt/c/DocumentNoSnc/CC/GXEMUL/build/.MUTANT 2>/dev/null || echo "build/.MUTANT: absent"
