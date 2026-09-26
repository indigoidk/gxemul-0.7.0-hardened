set -u
cd /tmp/opus550p2 || exit 1
echo "== CONTROL: HEAD's checker on the same export (swap in, run, swap back)"
cp exp/tools/pipeline/check_probe_wiring.py cpw_550v2_staged.py
cp cpw_HEAD_export.py exp/tools/pipeline/check_probe_wiring.py
for d in 2026-09-27 2026-09-28; do
  printf '%s ' $d; python3 exp/tools/pipeline/check_probe_wiring.py --regress exp/regress --today $d 2>&1 | grep -E 'PROBEWIRING_(PASS|FAIL)' | cut -c1-60
done
cp cpw_550v2_staged.py exp/tools/pipeline/check_probe_wiring.py
cmp -s exp/tools/pipeline/check_probe_wiring.py cpw_550v2_staged.py && echo "restored #550v2 checker (cmp clean)"
echo "== SCHEDULE: #550v2 checker, every day 2026-09-25..2026-12-31"
python3 -u sched550v2.py /tmp/opus550p2/exp > schedule_daily.out 2>&1
tail -16 schedule_daily.out
