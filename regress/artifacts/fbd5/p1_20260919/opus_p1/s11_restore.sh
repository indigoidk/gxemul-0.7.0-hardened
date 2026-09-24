#!/bin/bash
# Step 5: restore the clone to HEAD's source, cmp against SEC (never a local backup),
# REBUILD, and only then clear the sentinel.  The sentinel protects the SOURCE; the
# thing measured is the BINARY.
set -u
T=/tmp/gxopusfbd5
SECG=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
cd "$T" || exit 9
echo "=== sentinel before restore ==="; cat .MUTANT 2>/dev/null || echo "(none)"
echo "=== restore from GXEMUL-SEC (the repo), not from out/fb_head.c ==="
git -C "$SECG" show HEAD:src/devices/dev_footbridge.c > src/devices/dev_footbridge.c || exit 9
echo "=== cmp against the repo source ==="
git -C "$SECG" show HEAD:src/devices/dev_footbridge.c > /tmp/fb_check.c
if cmp -s /tmp/fb_check.c src/devices/dev_footbridge.c; then echo "  PART 1 OK: source cmps clean against HEAD"; else echo "  *** PART 1 FAILED"; exit 9; fi
echo "=== also confirm every other src/ file still matches HEAD ==="
BAD=0
for f in $(cd "$T" && find src -name '*.c' -o -name '*.h' | sed 's|^|  |' | head -0); do :; done
for f in src/cpus/cpu_alpha_palcode.c src/devices/dev_lca.c src/devices/dev_pcc2.c \
         src/devices/dev_sgi_ip32.c src/devices/dev_sh4.c src/include/thirdparty/mvme_pcctworeg.h; do
  git -C "$SECG" show "HEAD:$f" > /tmp/chk.f 2>/dev/null
  cmp -s /tmp/chk.f "$T/$f" && echo "  at HEAD  $f" || { echo "  *** DIVERGES $f"; BAD=1; }
done
[ "$BAD" = 0 ] || exit 9
echo "=== rebuild (PART 2 -- the restore is not finished until the binary is rebuilt) ==="
rm -f src/devices/dev_footbridge.o gxemul
make -j6 > out/restore_build.log 2>&1
echo "MAKE_RC=$?"
[ -x gxemul ] || { echo "NO BINARY"; exit 9; }
if [ gxemul -nt src/devices/dev_footbridge.c ]; then echo "  PART 2 OK: binary newer than source"; else echo "  *** PART 2 FAILED"; exit 9; fi
echo "  binary $(stat -c '%y' gxemul)"
echo "  source $(stat -c '%y' src/devices/dev_footbridge.c)"
echo "=== the restored binary is HEAD's: identical to the kept out/gxemul_HEAD? ==="
md5sum gxemul out/gxemul_HEAD
echo "=== the shipped sites probe on the restored build (expect 19 of 19) ==="
python3 -u "$SECG/regress/footbridge_sites_probe.py" ./gxemul out/arm_stub.bin | tail -8
echo "=== clearing the sentinel, both parts verified ==="
rm -f .MUTANT
ls -la .MUTANT 2>/dev/null || echo "  .MUTANT gone"
echo "S11_DONE"
