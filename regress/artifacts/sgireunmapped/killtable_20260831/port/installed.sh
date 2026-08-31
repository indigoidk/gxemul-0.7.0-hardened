#!/bin/bash
#  Run the INSTALLED artifact from the gate's own cwd, exactly as gate_arm.sh will.
set -u
cd /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress
echo "cwd=$(pwd)"
python3 sgi_re_unmapped_probe.py /tmp/gx499/gxemul.fix gate > /tmp/gx499_installed.log 2>&1
RC=$?
echo "PROBE_RC=$RC"
echo "SENTINELS=$(grep -c '^OPUS499T_DONE$' /tmp/gx499_installed.log)"
echo "RESULT=$(grep -h '^OPUS499T_RESULT=' /tmp/gx499_installed.log)"
echo "rows emitted = $(( $(grep -c ' ok$' /tmp/gx499_installed.log) + $(grep -c ' FAIL$' /tmp/gx499_installed.log) ))"
echo "rows green   = $(grep -c ' ok$' /tmp/gx499_installed.log)"
echo "rows red     = $(grep -c ' FAIL$' /tmp/gx499_installed.log)"
echo "--- the gate's padded-column matcher against every row name ---"
MISS=0
for v in "live" "devsig" "wr surv" "wr kill" "wr decl" "rd surv" "rd kill" "rd decl" "rd sent" "rd nodbe" "wr lat1" "rd lat1" "wr rd 2msg" "xwin7 pre" "xwin wr" "xwin rd" "tlba acc lo" "tlba acc hi" "tlbb acc lo" "tlbb acc hi" "tlbc acc lo" "tlbc acc hi" "tex acc lo" "tex acc hi" "lina acc lo" "lina acc hi" "linb acc lo" "linb acc hi"; do
  n=$(grep -c "^$v  .*ok$" /tmp/gx499_installed.log)
  if [ "$n" -ne 1 ]; then echo "  UNMATCHABLE ROW: [$v] -> $n"; MISS=1; fi
done
[ $MISS -eq 0 ] && echo "  all 28 row names match ^name<2+spaces>...ok$ exactly once (padded-column trap clear)"
echo "INSTALLED_DONE"
