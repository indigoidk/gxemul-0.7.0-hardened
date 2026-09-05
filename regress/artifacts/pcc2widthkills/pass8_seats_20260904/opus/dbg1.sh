cd /tmp/gxopus_p8
echo "=== err file ==="; wc -c p8/f1_err.txt; head -20 p8/f1_err.txt
echo "=== out file ==="; wc -c p8/f1_out.txt; head -20 p8/f1_out.txt
echo "=== usage line of probe ==="; sed -n '280,300p' p8/frozen_probe.py
