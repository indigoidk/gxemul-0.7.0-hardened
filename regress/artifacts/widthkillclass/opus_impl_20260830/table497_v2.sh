#!/bin/bash
#  #497 kill table driver, v2.
#
#  *** THE ONE CHANGE FROM v1 IS THE FREEZE, AND IT MATTERS. ***  v1 froze the
#  DRIVER and the PROBE but pointed MUT at the live scratchpad mutator, which it
#  re-reads once per mutant -- so editing the mutator mid-table would silently
#  have changed the instrument between rows, which is exactly the hazard the
#  frozen-copy rule exists to stop.  v2 runs a frozen mutator as well.
T=/tmp/gx497impl
SRC=$T/src/devices/dev_sgi_re.c
MUT=/tmp/gx497_mutator_frozen.py          # FROZEN, not the scratchpad copy
OUT=/tmp/gx497tab
mkdir -p "$OUT"

if [ ! -f "$MUT" ]; then echo "FROZEN MUTATOR MISSING -- stop"; exit 1; fi

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
