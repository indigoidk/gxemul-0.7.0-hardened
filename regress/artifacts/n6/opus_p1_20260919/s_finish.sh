#!/bin/bash
set -u
T=/tmp/gxopus539p1
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/n6/opus_p1_20260919
cd "$T" || exit 9

echo "=== FINAL STATE OF THE SCRATCH CLONE BEFORE REMOVAL ==="
echo "sentinel present? : $( [ -f .MUTANT ] && cat .MUTANT || echo 'NO .MUTANT -- cleared' )"
echo "dev_footbridge.c vs GXEMUL-SEC HEAD:"
cmp -s src/devices/dev_footbridge.c out/fb_head.c && echo "  CLEAN" || echo "  *** DIRTY ***"
echo "binary fresh? : $( [ gxemul -nt src/devices/dev_footbridge.c ] && echo yes || echo NO )"
echo
echo "=== artifacts under $T/out ==="
ls -la out/
echo
echo "=== copying every artifact to the durable path ==="
mkdir -p "$D/artifacts"
cp -f out/*.raw out/*.log "$D/artifacts/" 2>/dev/null
cp -f out/fb_fixed.c "$D/artifacts/dev_footbridge.PROPOSED_FIX.c" 2>/dev/null
ls -la "$D/artifacts/"
echo
echo "=== verifying the project trees were NEVER written ==="
for t in /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC /mnt/c/DocumentNoSnc/CC/GXEMUL/est \
         /mnt/c/DocumentNoSnc/CC/GXEMUL/build /mnt/c/DocumentNoSnc/CC/GXEMUL/build-asan; do
  f=$t/src/devices/dev_footbridge.c
  [ -f "$f" ] && echo "  $(md5sum "$f")"
done
echo "  (all four must still be 7b4c8650fac235e2f67d8a8aed376b7e)"
echo "peer clones untouched (must still exist if they did):"
ls -d /tmp/gxkill540 /tmp/gxclose538 /tmp/gxkill541 /tmp/gxsec-build 2>/dev/null || echo "  none of the peer clones exist on this box"
echo
echo "=== REMOVING $T ==="
cd /tmp && rm -rf "$T"
[ -d "$T" ] && echo "*** REMOVAL FAILED ***" || echo "REMOVED: $T no longer exists"
