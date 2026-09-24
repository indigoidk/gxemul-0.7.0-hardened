#!/bin/bash
# fbd5 opus p1 step 1: clone build/ -> /tmp/gxopusfbd5, restore src to HEAD, rebuild.
set -u
SECG=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
T=/tmp/gxopusfbd5
echo "=== HEAD ==="
git -C "$SECG" log --oneline -1
echo "=== cp -a build -> $T ==="
rm -rf "$T"
cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$T" || exit 9
cd "$T" || exit 9
mkdir -p out
echo "=== restore uncommitted src/ files to HEAD ==="
for f in $(git -C "$SECG" status --porcelain -- src | awk '{print $2}'); do
  if [ -f "$T/$f" ]; then
    git -C "$SECG" show "HEAD:$f" > "$T/$f.head" 2>/dev/null || { echo "  EXTRACT FAILED $f"; exit 9; }
    if cmp -s "$T/$f.head" "$T/$f"; then echo "  already-at-HEAD  $f"; rm -f "$T/$f.head";
    else mv "$T/$f.head" "$T/$f"; echo "  restored         $f"; fi
  else
    echo "  ABSENT in clone (divergence path?)  $f"
  fi
done
echo "=== dev_footbridge.c == HEAD ? ==="
git -C "$SECG" show HEAD:src/devices/dev_footbridge.c > out/fb_head.c
cmp -s out/fb_head.c src/devices/dev_footbridge.c && echo "  CLEAN == HEAD" || { echo "  *** DIVERGES ***"; exit 9; }
echo "=== rm objects + binary ==="
rm -f src/devices/*.o src/cpus/*.o src/machines/*.o gxemul
echo "=== make -j6 ==="
make -j6 > out/build1.log 2>&1
echo "MAKE_RC=$?"
tail -4 out/build1.log
ls -la gxemul 2>/dev/null || { echo "NO BINARY"; exit 9; }
if [ gxemul -nt src/devices/dev_footbridge.c ]; then echo "FRESH: binary newer than fb source"; else echo "*** STALE ***"; exit 9; fi
printf '\x00\x00\xa0\xe1' > out/arm_stub.bin
ls -la out/arm_stub.bin
echo "=== sanity: version ==="
./gxemul -V 2>&1 | head -2 || true
echo "S1_DONE"
