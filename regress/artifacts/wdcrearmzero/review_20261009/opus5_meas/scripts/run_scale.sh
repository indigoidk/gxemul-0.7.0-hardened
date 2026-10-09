#!/bin/bash
# opus5 late seat: scale the rung-1 search.  Rebuilds f_HEAD and f_1f1a02b from the
# current harness source (the instrumented dev_wdc.c copies made by run_fuzz.sh are
# reused unchanged), then runs HEAD at two seeds / two interference densities and
# 1f1a02b once for contrast.
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opuswdc
T=/tmp/gxopuswdc
OUT=$S/fuzz_opus
for rev in HEAD 1f1a02b; do
  D=$T/f_$rev
  cp "$S/opus_rearm_fuzz.c" "$D/regress/"
  ( cd "$D/regress" && gcc -O2 -std=c99 -Wall -I../src/include -I../src/include/thirdparty \
      -ffunction-sections -fdata-sections -Wl,--gc-sections \
      -o fuzz opus_rearm_fuzz.c ) > "$OUT/${rev}.scale.build" 2>&1
  [ "$D/regress/fuzz" -nt "$D/regress/opus_rearm_fuzz.c" ] || { echo "$rev BUILD FAILED"; cat "$OUT/${rev}.scale.build"; exit 3; }
done
run() {  # rev sessions seed heavy tag
  ( cd "$T/f_$1/regress" && timeout 3000 ./fuzz "$2" "$3" "$4" ) > "$OUT/$1.$5.out" 2>&1
  echo "rc=$?" >> "$OUT/$1.$5.out"
  echo "=== $1 $5 ($2 sessions, seed $3, heavy $4)"
  grep -E '^RESULT|dirty sig|^rc=' "$OUT/$1.$5.out" | head -40
}
run HEAD 10000 1 0 s1normal
run HEAD 10000 2 1 s2heavy
run 1f1a02b 1000 3 1 s3heavy
echo RUN_SCALE_DONE
