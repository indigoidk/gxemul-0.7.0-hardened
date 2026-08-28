#!/bin/bash
#  ASAN reports through a pty are easy to lose.  log_path makes each process write its own
#  report file, so nothing depends on the probe capturing stderr.
set -u
R=/mnt/c/DocumentNoSnc/cc/GXEMUL
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/40fd4ccc-4c3b-4ad6-91dc-122d039ab5a2/scratchpad
rm -f /tmp/asanrep.*
export ASAN_OPTIONS="log_path=/tmp/asanrep:detect_leaks=0:abort_on_error=0"
echo "=== M0 (guard deleted) under the 19-row detector, ASAN reports to /tmp/asanrep.* ==="
python3 -u $R/GXEMUL-SEC/regress/gdrom_toclen_probe.py /tmp/gxasan_m0/gxemul \
    $R/_images/openbsd76-landisk-bsd.rd > /tmp/asan_m0c_probe.log 2>&1
echo "TOCLEN: $(grep -oE 'TOCLEN_RESULT=[0-9]+/[0-9]+' /tmp/asan_m0c_probe.log | tail -1)"
echo "=== ASAN report files written: $(ls /tmp/asanrep.* 2>/dev/null | wc -l) ==="
if ls /tmp/asanrep.* >/dev/null 2>&1; then
  echo "--- distinct error kinds ---"
  cat /tmp/asanrep.* | grep -oE 'ERROR: AddressSanitizer: [a-z-]+' | sort | uniq -c
  echo "--- first report, head ---"
  head -16 "$(ls /tmp/asanrep.* | head -1)"
  cp /tmp/asanrep.* $S/ 2>/dev/null
fi
cp /tmp/asan_m0c_probe.log $S/ 2>/dev/null
echo ASAN_M0C_DONE
