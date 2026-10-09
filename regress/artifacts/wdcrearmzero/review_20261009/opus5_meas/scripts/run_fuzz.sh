#!/bin/bash
# opus5 late seat (wdcrearmzero), 2026-10-09.  Build the rung-1 invariant search against
# INSTRUMENTED COPIES of dev_wdc.c at three revisions and run it.  The only source change
# in each copy is the hook call OPUS_REARM_PRE(d) inserted at the head of the re-arm
# branch; the diff against the revision is printed so it can be checked.  Private
# scratch only (/tmp/gxopuswdc/f_<rev>); outputs to the session scratchpad.
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opuswdc
T=/tmp/gxopuswdc
OUT=$S/fuzz_opus
SESS=${1:-3000}
mkdir -p "$OUT"
cd "$T" || exit 9
tar -xf "$S/t_pre473.tar"; cp "$S/config.h" t_pre473/config.h
for rev in pre473 1f1a02b HEAD; do
  D=$T/f_$rev
  rm -rf "$D"; mkdir -p "$D/regress"
  cp -a "$T/t_$rev/src" "$T/t_$rev/config.h" "$D/"
  python3 "$S/mutate.py" "$D/src/devices/dev_wdc.c" 'data_in_len) {' \
      'data_in_len) { OPUS_REARM_PRE(d);' > "$OUT/${rev}.build" 2>&1 || {
      echo "$rev: hook anchor not unique"; continue; }
  diff "$T/t_$rev/src/devices/dev_wdc.c" "$D/src/devices/dev_wdc.c" >> "$OUT/${rev}.build"
  cp "$S/opus_rearm_fuzz.c" "$D/regress/"
  ( cd "$D/regress" && gcc -O2 -std=c99 -Wall -I../src/include -I../src/include/thirdparty \
      -ffunction-sections -fdata-sections -Wl,--gc-sections \
      -o fuzz opus_rearm_fuzz.c ) >> "$OUT/${rev}.build" 2>&1
  if [ ! -x "$D/regress/fuzz" ] || [ ! "$D/regress/fuzz" -nt "$D/src/devices/dev_wdc.c" ]; then
    echo "$rev: BUILD FAILED"; tail -20 "$OUT/${rev}.build"; continue
  fi
  echo "=== $rev"
  ( cd "$D/regress" && timeout 1500 ./fuzz "$SESS" ) > "$OUT/${rev}.out" 2>&1
  echo "rc=$?" >> "$OUT/${rev}.out"
  grep -E '^  D[0-9]|^RESULT|dirty sig|FUZZ_DONE|^rc=' "$OUT/${rev}.out"
done
echo RUN_FUZZ_DONE
