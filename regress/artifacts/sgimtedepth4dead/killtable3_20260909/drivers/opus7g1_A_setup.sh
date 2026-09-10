#!/bin/bash
# Stage A: clone build/ -> /tmp/gxopus7g1, verify baseline identity, freeze probe, build baseline.
# NO `set -e': the probe exits 1 on a non-perfect score and a comparison must not kill the driver.
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SRC=/mnt/c/DocumentNoSnc/CC/GXEMUL/build
CL=/tmp/gxopus7g1
F=src/devices/dev_sgi_re.c

echo "=== STAGE A  $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="

if [ -e "$CL" ]; then echo "A-FAIL: $CL already exists; refusing to reuse"; exit 9; fi

echo "-- cloning (cp -a) --"
cp -a "$SRC" "$CL"; RC=$?
echo "CP_RC=$RC"
[ $RC -ne 0 ] && { echo "A-FAIL: clone failed"; exit 9; }

echo "-- BASELINE IDENTITY: the one file to be mutated, vs SEC (the named baseline) --"
if cmp -s "$CL/$F" "$SEC/$F"; then echo "BASELINE_CMP=CLEAN  ($F identical to SEC)"; else
  echo "BASELINE_CMP=DIFFERS -- copying SEC over it (SEC is the baseline)"
  cp "$SEC/$F" "$CL/$F" || { echo "A-FAIL: cp failed"; exit 9; }
  cmp -s "$CL/$F" "$SEC/$F" && echo "BASELINE_CMP=CLEAN after copy" || { echo "A-FAIL: still differs"; exit 9; }
fi
echo "SEC_MD5:   $(md5sum "$SEC/$F" | cut -c1-32)"
echo "CLONE_MD5: $(md5sum "$CL/$F" | cut -c1-32)"
echo "EDIT LINE 1519: $(sed -n '1519p' "$CL/$F")"

echo "-- FREEZE THE INSTRUMENT (one probe for the whole comparison) --"
mkdir -p "$CL/probe"
cp "$SEC/regress/sgi_mte_fill_probe.py" "$CL/probe/"
cp "$SEC/regress/sgi_mte_dummy.bin" "$CL/probe/" 2>/dev/null
echo "PROBE_MD5: $(md5sum "$CL/probe/sgi_mte_fill_probe.py" | cut -c1-32)"
echo "PROBE_SEC_MD5: $(md5sum "$SEC/regress/sgi_mte_fill_probe.py" | cut -c1-32)"

echo "-- NO SENTINEL YET: nothing has been mutated.  Proving that: --"
ls -la "$CL/.MUTANT" 2>&1 | head -1

echo "-- BASELINE BUILD --"
cd "$CL" || exit 9
rm -f src/devices/dev_sgi_re.o
make -j4 > /tmp/gxopus7g1_buildA.log 2>&1; MAKE_RC=$?
echo "MAKE_RC=$MAKE_RC   (NOT trusted alone -- has been observed 0 on a failed build)"
tail -3 /tmp/gxopus7g1_buildA.log
if [ -x "$CL/gxemul" ] && [ "$CL/gxemul" -nt "$CL/$F" ]; then
  echo "FRESHNESS=OK  binary NEWER than source"
else
  echo "FRESHNESS=FAIL"; ls -la --time-style=full-iso "$CL/gxemul" "$CL/$F"; exit 9
fi
ls -la --time-style=full-iso "$CL/gxemul" "$CL/$F"
echo "STAGE_A_DONE"
