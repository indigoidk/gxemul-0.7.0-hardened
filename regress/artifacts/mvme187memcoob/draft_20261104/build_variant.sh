#!/bin/bash
# build_variant.sh <clonedir> <variant>
# Fresh-copies dev_mvme187.c from SEC into the clone, patches it, rebuilds dev_mvme187.o, relinks.
set -e
CLONE="$1"; V="$2"
B=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC="$B/GXEMUL-SEC/src/devices/dev_mvme187.c"
SCR="$B/_scratchpad/opus_20261104/m_memc"
DST="$CLONE/src/devices/dev_mvme187.c"

echo "$V : dev_mvme187.c exits->declines / bound, built in $CLONE" > "$CLONE/.MUTANT"
cp -a "$SEC" "$DST"
python3 "$SCR/patch_mvme187.py" "$V" "$DST"
diff -u "$SEC" "$DST" > "$SCR/${V}_$(basename "$CLONE").diff" || true
echo "--- diff head ---"; sed -n '1,60p' "$SCR/${V}_$(basename "$CLONE").diff"

cd "$CLONE"
rm -f src/devices/dev_mvme187.o
make -j4 >/tmp/build_${V}_$(basename "$CLONE").log 2>&1 || { echo BUILD_FAILED; tail -40 /tmp/build_${V}_$(basename "$CLONE").log; exit 1; }
if [ gxemul -nt src/devices/dev_mvme187.c ]; then
    echo "FRESH: gxemul newer than source"
else
    echo "STALE: gxemul NOT newer than source -- STOP"; exit 1
fi
ls -la gxemul src/devices/dev_mvme187.o
echo "BUILD_DONE_${V}"
