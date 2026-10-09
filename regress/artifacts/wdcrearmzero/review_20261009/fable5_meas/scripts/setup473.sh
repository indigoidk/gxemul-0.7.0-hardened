#!/bin/bash
# fable5 late-review scratch for #473 / wdcrearmzero.  OWN scratch clone only:
# copies the three things the offline wdc differential needs out of GXEMUL-SEC
# into /tmp/fable473 and builds the UNMUTATED baseline there.  Nothing under
# /mnt/c is written.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
BLD=/mnt/c/DocumentNoSnc/cc/GXEMUL/build
W=/tmp/fable473
rm -rf "$W"
mkdir -p "$W/src/devices" "$W/regress" "$W/out"
cp -r "$SEC/src/include" "$W/src/"
cp "$SEC/src/devices/dev_wdc.c" "$W/src/devices/"
cp "$SEC/regress/diff_wdc_identify.c" "$W/regress/"
if [ -f "$SEC/config.h" ]; then cp "$SEC/config.h" "$W/"; echo "config.h from SEC";
elif [ -f "$BLD/config.h" ]; then cp "$BLD/config.h" "$W/"; echo "config.h from build/";
else echo "NO config.h found"; fi
echo "--- identity of the copied source against SEC ---"
md5sum "$W/src/devices/dev_wdc.c" "$SEC/src/devices/dev_wdc.c" "$W/regress/diff_wdc_identify.c" "$SEC/regress/diff_wdc_identify.c"
CC=$(command -v cc || command -v gcc)
echo "CC=$CC"; $CC --version | head -1
cd "$W/regress" || exit 9
$CC -O2 -std=c99 -I"$W/src/include" -I"$W/src/include/thirdparty" \
    -ffunction-sections -fdata-sections -Wl,--gc-sections \
    -o "$W/out/base" "$W/regress/diff_wdc_identify.c" > "$W/out/base.build" 2>&1
echo "build rc=$?"; head -5 "$W/out/base.build"
"$W/out/base" > "$W/out/base.log" 2>&1
echo "run rc=$?"
grep -E '^[0-9]+ rows|WDC_IDENTIFY_(PASS|FAIL)|FAIL' "$W/out/base.log" | head -20
echo "--- the #473 rows in the baseline log ---"
grep -n -E 're-arm|last chunk|arm:' "$W/out/base.log"
echo BASE_DONE
