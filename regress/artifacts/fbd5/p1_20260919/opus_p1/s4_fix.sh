#!/bin/bash
# Apply a variant to the clone's dev_footbridge.c, rebuild, verify freshness.
# $1 = variant name.  Drops the .MUTANT sentinel FIRST.
set -u
V="${1:-fix}"
T=/tmp/gxopusfbd5
SECG=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/fbd5/opus_p1_20260919
cd "$T" || exit 9
echo "=== sentinel FIRST ==="
echo "$T/.MUTANT: src/devices/dev_footbridge.c variant=$V (fbd5 opus p1); restore: git -C $SECG show HEAD:src/devices/dev_footbridge.c" > "$T/.MUTANT"
cat "$T/.MUTANT"
echo "=== restore the file to HEAD before applying ==="
git -C "$SECG" show HEAD:src/devices/dev_footbridge.c > src/devices/dev_footbridge.c || exit 9
cmp -s out/fb_head.c src/devices/dev_footbridge.c && echo "  at HEAD" || { echo "  *** restore failed"; exit 9; }
echo "=== apply variant $V ==="
python3 "$D/mkfix.py" src/devices/dev_footbridge.c "$V" || exit 9
echo "=== diff vs HEAD ==="
diff -u out/fb_head.c src/devices/dev_footbridge.c | sed -n '1,200p'
echo "=== rebuild ==="
rm -f src/devices/dev_footbridge.o gxemul
make -j6 > "out/build_$V.log" 2>&1
echo "MAKE_RC=$?"
grep -iE 'error|warning' "out/build_$V.log" | head -10
ls -la gxemul 2>/dev/null || { echo "NO BINARY"; exit 9; }
if [ gxemul -nt src/devices/dev_footbridge.c ]; then echo "FRESH"; else echo "*** STALE ***"; exit 9; fi
echo "S4_DONE variant=$V"
