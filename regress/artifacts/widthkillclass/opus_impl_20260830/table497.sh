#!/bin/bash
#  #497 kill table driver.  Runs from a FROZEN copy (/tmp/gx497_table_frozen.sh).
#  Every mutant: restore fixed source -> apply -> rebuild -> freshness -> probe.
T=/tmp/gx497impl
SRC=$T/src/devices/dev_sgi_re.c
MUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/gx497/mutate497.py
OUT=/tmp/gx497tab
mkdir -p "$OUT"

echo "dev_sgi_re.c  #497 kill table in progress" > "$T/.MUTANT"

for m in "$@"; do
  echo "=== $m  $(date +%H:%M:%S) ==="
  cp /tmp/gx497_fix_src.c "$SRC"
  if ! python3 "$MUT" "$m" "$SRC" > "$OUT/apply_$m.log" 2>&1; then
      echo "$m  APPLY_FAILED (presence pin) -- see apply_$m.log"
      tail -2 "$OUT/apply_$m.log"
      continue
  fi
  rm -f "$T/src/devices/dev_sgi_re.o"
  ( cd "$T" && make -j8 ) > "$OUT/build_$m.log" 2>&1
  echo "  MAKE_RC=$?"
  if [ ! "$T/gxemul" -nt "$SRC" ]; then
      echo "$m  FRESH=NO  *** binary older than source, SKIPPING ***"
      continue
  fi
  python3 -u /tmp/gx497_probe_frozen.py "$T/gxemul" "$m" > "$OUT/probe_$m.out" 2>&1
  grep -h "OPUS497T_RESULT\|OPUS497T_CONTROL" "$OUT/probe_$m.out"
  echo "  FAILED ROWS:"
  grep "FAIL" "$OUT/probe_$m.out" | sed "s/^/    /" | head -40
done

# ---- restore the fixed source and REBUILD, then clear the sentinel ----
cp /tmp/gx497_fix_src.c "$SRC"
rm -f "$T/src/devices/dev_sgi_re.o"
( cd "$T" && make -j8 ) > "$OUT/build_restore.log" 2>&1
echo "restore MAKE_RC=$?"
if cmp -s "$SRC" /tmp/gx497_fix_src.c && [ "$T/gxemul" -nt "$SRC" ]; then
    rm -f "$T/.MUTANT"
    echo "RESTORE=VERIFIED (cmp clean AND binary newer) -- sentinel cleared"
else
    echo "RESTORE=FAILED -- sentinel KEPT"
fi
echo "TABLE497_DONE"
