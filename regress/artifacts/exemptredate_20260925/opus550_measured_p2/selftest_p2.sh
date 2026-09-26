set -u
cd /tmp/opus550p2 || exit 1
s=$(date +%s)
python3 exp/tools/pipeline/check_probe_wiring.py --selftest > selftest_550v2.out 2>&1
rc=$?
e=$(date +%s)
echo "rc=$rc wall=$((e-s))s"
grep -E 'M5a|M5b|SELFTEST_(PASS|FAIL)' selftest_550v2.out
grep -c '^  ok ' selftest_550v2.out
