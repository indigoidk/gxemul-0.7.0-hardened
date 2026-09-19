#!/bin/bash
# Build a COMMITTED-baseline gxemul in the scratch clone.
set -u
SECG=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
T=/tmp/gxopus539p1
cd "$T" || exit 9
mkdir -p out

echo "=== restoring the 6 uncommitted other-round files to HEAD 408accf ==="
for f in src/cpus/cpu_alpha_palcode.c src/devices/dev_lca.c src/devices/dev_pcc2.c \
         src/devices/dev_sgi_ip32.c src/devices/dev_sh4.c src/include/thirdparty/mvme_pcctworeg.h; do
  git -C "$SECG" show "HEAD:$f" > "$T/$f.head" 2>/dev/null || { echo "FAILED to extract $f"; exit 9; }
  if cmp -s "$T/$f.head" "$T/$f"; then
    echo "  already-at-HEAD  $f"
    rm -f "$T/$f.head"
  else
    mv "$T/$f.head" "$T/$f"
    echo "  restored         $f"
  fi
done

echo "=== confirming dev_footbridge.c == HEAD ==="
git -C "$SECG" show HEAD:src/devices/dev_footbridge.c > "$T/out/fb_head.c"
if cmp -s "$T/out/fb_head.c" "$T/src/devices/dev_footbridge.c"; then
  echo "  CLEAN src/devices/dev_footbridge.c == HEAD:408accf"
else
  echo "  *** DIVERGES *** "; exit 9
fi

echo "=== removing objects ==="
rm -f src/cpus/*.o
rm -f src/devices/dev_lca.o src/devices/dev_pcc2.o src/devices/dev_sgi_ip32.o \
      src/devices/dev_sh4.o src/devices/dev_footbridge.o
BEFORE=$(date +%s)
echo "=== make -j4 ==="
make -j4 > out/build.log 2>&1
RC=$?
echo "MAKE_RC=$RC"
tail -5 out/build.log
ls -la gxemul
echo "=== freshness: [ gxemul -nt src/devices/dev_footbridge.c ] ==="
if [ gxemul -nt src/devices/dev_footbridge.c ]; then echo "  FRESH: binary newer than source"; else echo "  *** STALE ***"; exit 9; fi
echo "binary mtime : $(stat -c %y gxemul)"
echo "fb source    : $(stat -c %y src/devices/dev_footbridge.c)"
echo "build started: $BEFORE  now: $(date +%s)"
