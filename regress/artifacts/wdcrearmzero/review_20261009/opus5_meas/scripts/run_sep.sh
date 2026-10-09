#!/bin/bash
# opus5 late seat: the separability measurement.  Four builds, directed tests only
# (0 random sessions): pre473 (parent 00d546d), pre473+REARM-ONLY (= 0 -> = 32768, no
# clamp move, no refill), 1f1a02b, HEAD.  Each is the instrumented copy (one hook line).
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opuswdc
T=/tmp/gxopuswdc
OUT=$S/fuzz_opus
D=$T/f_rearmonly
rm -rf "$D"; mkdir -p "$D/regress"
cp -a "$T/f_pre473/src" "$T/f_pre473/config.h" "$D/"
python3 "$S/rearm_only.py" "$D/src/devices/dev_wdc.c" > "$OUT/rearmonly.build" 2>&1 || { cat "$OUT/rearmonly.build"; exit 3; }
diff "$T/f_pre473/src/devices/dev_wdc.c" "$D/src/devices/dev_wdc.c" >> "$OUT/rearmonly.build"
for rev in pre473 rearmonly 1f1a02b HEAD; do
  B=$T/f_$rev
  cp "$S/opus_rearm_fuzz.c" "$B/regress/"
  ( cd "$B/regress" && gcc -O2 -std=c99 -Wall -I../src/include -I../src/include/thirdparty \
      -ffunction-sections -fdata-sections -Wl,--gc-sections \
      -o fuzzd opus_rearm_fuzz.c ) >> "$OUT/$rev.sep.build" 2>&1
  [ "$B/regress/fuzzd" -nt "$B/regress/opus_rearm_fuzz.c" ] || { echo "$rev BUILD FAILED"; continue; }
  ( cd "$B/regress" && ./fuzzd 0 ) > "$OUT/$rev.directed.out" 2>&1
  echo "=== $rev"; grep -E '^  D' "$OUT/$rev.directed.out"
done
cat "$OUT/rearmonly.build"
echo RUN_SEP_DONE
