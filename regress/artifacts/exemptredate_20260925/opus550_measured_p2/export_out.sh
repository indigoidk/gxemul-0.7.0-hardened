set -u
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/exemptredate_20260925/opus550_measured_p2
cd /tmp/opus550p2 || exit 1
cp schedule_daily.out selftest_550v2.out control_and_lists.out lists.sh "$O/"
cp sched550v2.py "$O/sched550v2.py.txt"
