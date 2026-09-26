set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
cd /tmp/opus550p2 || exit 1
{
  echo "== CONTROL: HEAD's checker on this export (apparatus must go red on 09-28)"
  cp exp/tools/pipeline/check_probe_wiring.py cpw_550v2_staged.py
  cp cpw_HEAD_export.py exp/tools/pipeline/check_probe_wiring.py
  for d in 2026-09-27 2026-09-28; do printf '%s ' $d; python3 exp/tools/pipeline/check_probe_wiring.py --regress exp/regress --today $d 2>&1 | grep -E 'PROBEWIRING_(PASS|FAIL)'; done
  cp cpw_550v2_staged.py exp/tools/pipeline/check_probe_wiring.py
  cmp -s exp/tools/pipeline/check_probe_wiring.py $S/exempt550/cpw_550v2_onHEAD.py && echo "restored: export checker == cpw_550v2_onHEAD.py (cmp clean)"
  echo
  echo "== gate 2 exempt_expired() (from goff_550v2.sh) beside gate 9 AB_EXEMPT (HEAD), every day 09-25..12-31; lines print on change"
  bash lists.sh
  echo "LISTS_DONE"
} > control_and_lists.out 2>&1
tail -1 control_and_lists.out
