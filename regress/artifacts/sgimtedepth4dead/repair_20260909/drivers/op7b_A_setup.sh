#!/bin/bash
# Stage A: clone build/ -> /tmp/gxopus7g1b, NAME and verify the baseline, freeze the REPAIRED
# probe, build the baseline binary.  NO `set -e': the probe exits 1 on a red row and a driver
# ending in a comparison is how a measurement silently does not happen.
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SRC=/mnt/c/DocumentNoSnc/CC/GXEMUL/build
CL=/tmp/gxopus7g1b
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
F=src/devices/dev_sgi_re.c

echo "=== STAGE A  $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="

echo "-- the SOURCE tree we are about to clone: is it clean and sentinel-free? --"
cmp -s "$SRC/$F" "$SEC/$F" && echo "build/ $F CMP CLEAN vs SEC" || echo "*** build/ $F DIFFERS from SEC ***"
ls -la "$SRC/.MUTANT" 2>&1 | head -1

if [ -e "$CL" ]; then echo "A-FAIL: $CL already exists; refusing to reuse"; exit 9; fi

echo "-- cloning (cp -a) --"
cp -a "$SRC" "$CL"; RC=$?
echo "CP_RC=$RC"
[ $RC -ne 0 ] && { echo "A-FAIL: clone failed"; exit 9; }

echo "-- BASELINE NAMED: GXEMUL-SEC/$F at HEAD.  Identity of the one file to be mutated: --"
if cmp -s "$CL/$F" "$SEC/$F"; then echo "BASELINE_CMP=CLEAN  ($F identical to SEC)"; else
  echo "BASELINE_CMP=DIFFERS -- copying SEC over it (SEC is the named baseline)"
  cp "$SEC/$F" "$CL/$F" || { echo "A-FAIL: cp failed"; exit 9; }
  cmp -s "$CL/$F" "$SEC/$F" && echo "BASELINE_CMP=CLEAN after copy" || { echo "A-FAIL: still differs"; exit 9; }
fi
echo "SEC_MD5:   $(md5sum "$SEC/$F" | cut -c1-32)"
echo "CLONE_MD5: $(md5sum "$CL/$F" | cut -c1-32)"
echo "HEAD:      $(cd $SEC && git rev-parse --short HEAD 2>/dev/null)"
echo "THE #509 LINE: $(grep -n 'if (depth == 32)' "$CL/$F")"

echo "-- FREEZE THE INSTRUMENT: ONE probe file for the whole table --"
mkdir -p "$CL/probe" "$CL/logs"
cp "$SP/out/sgi_mte_fill_probe.REPAIRED.py" "$CL/probe/" || { echo "A-FAIL probe cp"; exit 9; }
cp "$SEC/regress/sgi_mte_dummy.bin" "$CL/probe/" 2>/dev/null
echo "FROZEN_PROBE_MD5: $(md5sum "$CL/probe/sgi_mte_fill_probe.REPAIRED.py" | cut -c1-32)"
echo "SOURCE_COPY_MD5:  $(md5sum "$SP/out/sgi_mte_fill_probe.REPAIRED.py" | cut -c1-32)"
echo "SHIPPED_PROBE_MD5:$(md5sum "$SEC/regress/sgi_mte_fill_probe.py" | cut -c1-32)  (the 14-row one, for the record)"
echo "ROW CALL COUNT in the frozen probe: $(grep -c '^row(' "$CL/probe/sgi_mte_fill_probe.REPAIRED.py")"

echo "-- NO SENTINEL YET: nothing has been mutated.  Proving that rather than asserting it: --"
ls -la "$CL/.MUTANT" 2>&1 | head -1

echo "-- BASELINE BUILD --"
cd "$CL" || exit 9
rm -f src/devices/dev_sgi_re.o
make -j4 > /tmp/op7b_buildA.log 2>&1; MAKE_RC=$?
echo "MAKE_RC=$MAKE_RC   (NOT trusted alone -- observed 0 on a failed build before)"
tail -3 /tmp/op7b_buildA.log
if [ -x "$CL/gxemul" ] && [ "$CL/gxemul" -nt "$CL/$F" ]; then
  echo "FRESHNESS=OK  [ gxemul -nt $F ]"
else
  echo "FRESHNESS=FAIL"; ls -la --time-style=full-iso "$CL/gxemul" "$CL/$F"; exit 9
fi
ls -la --time-style=full-iso "$CL/gxemul" "$CL/$F"
echo "BASE_BIN_MD5: $(md5sum $CL/gxemul | cut -c1-32)"
echo "STAGE_A_DONE"
