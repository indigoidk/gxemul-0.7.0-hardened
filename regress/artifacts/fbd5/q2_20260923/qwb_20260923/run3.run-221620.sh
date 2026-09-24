#!/bin/bash
# qwb: reproduce QWBVEND/QWBTMRV in a scratch clone; never touches GXEMUL-SEC, build/, est/.
set -u
X=/tmp/gxqwb3
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2h/qwb
rm -rf "$X"; mkdir -p "$X/regress"; cp -a "$SEC/src" "$X/src"; cp "$SEC/regress/diff_footbridge.c" "$X/regress/"; cp "$SEC/config.h" "$X/"
echo "qwb: dev_footbridge.c tail variants" > "$X/.MUTANT"
SRC="$X/src/devices/dev_footbridge.c"
echo "instrument md5 $(md5sum "$X/regress/diff_footbridge.c" | cut -c1-8); device md5 $(md5sum "$SEC/src/devices/dev_footbridge.c" | cut -c1-8)"
CF() { gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -I"$X/src" -I"$X/src/include" \
       -I"$X/src/include/thirdparty" -ffunction-sections -fdata-sections -Wl,--gc-sections -o "$2" "$1" -lm; }
run() { local nm=$1 new=$2
  cp "$SEC/src/devices/dev_footbridge.c" "$SRC"
  if [ -n "$new" ]; then
    python3 - "$SRC" "$new" <<'PY' || { echo "$nm: EDIT FAILED"; return; }
import io, sys
p, new = sys.argv[1], sys.argv[2]
old = "memory_writemax64(cpu, data, len, odata);"
if new == "SPECIAL_DLEN":
    old, new = "d->irq_enable &= ~idata;", "d->irq_enable &= ~idata; data[len] = 0;"
s = io.open(p, encoding="utf-8", newline="").read()
assert s.count(old) == (1 if old.startswith("d->") else 2), s.count(old)
i = s.rfind(old)
io.open(p, "w", encoding="utf-8", newline="").write(s[:i] + new + s[i + len(old):])
PY
  fi
  cd "$X/regress"; rm -f "d_$nm"
  CF diff_footbridge.c "d_$nm" > "$OUT/$nm.build" 2>&1 || { echo "$nm: BUILD FAILED"; return; }
  ./"d_$nm" > "$OUT/$nm.log" 2>&1; local rc=$?
  echo "$nm rc=$rc $(grep -oE '^[0-9]+ rows[^.]*' "$OUT/$nm.log" | head -1) | $(grep -c 'DIFF_FOOTBRIDGE_PASS' "$OUT/$nm.log") pass-line"
}
run base3   ""
run QDLEN   "SPECIAL_DLEN"
run QWBLOAD "memory_writemax64(cpu, data, relative_addr == TIMER_1_LOAD ? 8 : len, odata);"
run QWBT1CLR "memory_writemax64(cpu, data, relative_addr == TIMER_1_CLEAR ? 8 : len, odata);"
cp "$SEC/src/devices/dev_footbridge.c" "$SRC"
cmp -s "$SRC" "$SEC/src/devices/dev_footbridge.c" && rm -f "$X/.MUTANT" && echo "restored==SEC, sentinel cleared"
echo QWB3_DONE
