#!/bin/bash
# Stage G: the TLB reachability CONTROL, run against all three preserved binaries.
# NO mutation happens here -- the clone's source is already restored and cmp-clean.
CL=/tmp/gxopus7g1
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
OUT=$CL/logs
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
echo "=== STAGE G  $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "-- no mutation in flight: --"
cmp -s "$CL/src/devices/dev_sgi_re.c" "$SEC/src/devices/dev_sgi_re.c" && echo "clone source CMP CLEAN vs SEC" || echo "*** G-FAIL: clone dirty ***"
ls -la "$CL/.MUTANT" 2>&1 | head -1

cp "$SP/tlb_reach_control.py" "$CL/probe/" || exit 9
cd "$CL/probe" || exit 9
echo "CONTROL_MD5 $(md5sum tlb_reach_control.py | cut -c1-32)  (ONE frozen instrument for all three runs)"

for b in BASE M_tlbA M_tlbAB; do
  echo; echo "########## $b  ($(md5sum $CL/bin_$b | cut -c1-32)) ##########"
  python3 -u ./tlb_reach_control.py "$CL/bin_$b" "$b" > "$OUT/reach_$b.raw" 2>&1
  echo "RC=$?"
  cat "$OUT/reach_$b.raw"
  echo "SENTINEL: $(tail -1 $OUT/reach_$b.raw)"
done
echo
echo "STAGE_G_DONE"
