#!/bin/bash
#  Two pass-1 binaries re-scored on the SHIPPED probe, to discharge the far-bound
#  rows at TLB_B and TLB_C rather than inherit their kills from the artifact
#  detector.  Same sentinel gate.
set -u
H=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/o499
OUT=$H/t2out
for V in m2_tlbb m3_tlbc; do
  echo "==================================================================="
  echo "VARIANT: $V   (binary reused from pass 1, md5 $(md5sum /tmp/gx499/gxemul.$V | cut -d' ' -f1))"
  python3 -u $H/sgi_re_unmapped_probe.run.py /tmp/gx499/gxemul.$V $V > $OUT/$V.txt 2>&1
  PRC=$?
  NDONE=$(grep -c '^OPUS499T_DONE$' $OUT/$V.txt)
  NRES=$(grep -c '^OPUS499T_RESULT=' $OUT/$V.txt)
  echo "  PROBE_RC=$PRC  SENTINELS=$NDONE  RESULT_LINES=$NRES"
  if [ "$PRC" -ne 0 ] || [ "$NDONE" -ne 1 ] || [ "$NRES" -ne 1 ]; then
    echo "  *** RUN DID NOT COMPLETE -- NOT SCORED, ABORTING ***"; exit 1
  fi
  grep -E 'FAIL$' $OUT/$V.txt | sed 's/^/  /'
  grep -E '^OPUS499T_(CONTROL|RESULT)' $OUT/$V.txt | sed 's/^/  /'
done
echo "TABLE4_DONE $(date +%H:%M:%S)"
