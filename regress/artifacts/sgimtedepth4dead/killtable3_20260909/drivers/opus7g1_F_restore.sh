#!/bin/bash
# Stage F: RESTORE FROM SEC (never from a local backup), rebuild, verify BOTH parts, clear sentinel.
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CL=/tmp/gxopus7g1
F=src/devices/dev_sgi_re.c
echo "=== STAGE F (RESTORE)  $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
cp "$SEC/$F" "$CL/$F" || { echo "F-FAIL cp"; exit 9; }
echo "-- PART 1: source cmp vs SEC --"
if cmp -s "$CL/$F" "$SEC/$F"; then echo "PART1=CLEAN"; else echo "F-FAIL part1"; exit 9; fi
echo "SEC_MD5   $(md5sum $SEC/$F | cut -c1-32)"
echo "CLONE_MD5 $(md5sum $CL/$F | cut -c1-32)"
echo "line 1519: $(sed -n '1519p' $CL/$F)"

echo "-- PART 2: REBUILD (the sentinel protects the source; the thing measured is the BINARY) --"
cd "$CL" || exit 9
rm -f src/devices/dev_sgi_re.o
make -j4 > /tmp/gxopus7g1_buildF.log 2>&1; echo "MAKE_RC=$?"
if [ -x "$CL/gxemul" ] && [ "$CL/gxemul" -nt "$CL/$F" ]; then echo "PART2=OK  [ gxemul -nt $F ]"; else
  echo "F-FAIL part2 -- LEAVING SENTINEL IN PLACE"; ls -la --time-style=full-iso "$CL/gxemul" "$CL/$F"; exit 9; fi
cp "$CL/gxemul" "$CL/bin_BASE"
echo "bin_BASE md5 $(md5sum $CL/bin_BASE | cut -c1-32)  (must equal stage B's e113ca7193a91b8953c4c10f37417ab2)"

echo "-- BOTH PARTS PASSED -> clearing the sentinel --"
rm -f "$CL/.MUTANT"
ls -la "$CL/.MUTANT" 2>&1 | head -1
echo "-- the three preserved binaries --"
md5sum "$CL"/bin_BASE "$CL"/bin_M_tlbA "$CL"/bin_M_tlbAB
echo "-- PROJECT TREES UNTOUCHED?  (build/ must still be cmp-clean and sentinel-free) --"
cmp -s /mnt/c/DocumentNoSnc/CC/GXEMUL/build/$F "$SEC/$F" && echo "build/ dev_sgi_re.c CMP CLEAN vs SEC" || echo "*** build/ DIFFERS ***"
ls -la /mnt/c/DocumentNoSnc/CC/GXEMUL/build/.MUTANT 2>&1 | head -1
echo "STAGE_F_DONE"
