n=0
until grep -q "M_IPLR|" /tmp/gxopus_p8/p8/TABLE.txt 2>/dev/null || [ $n -ge 50 ]; do sleep 2; n=$((n+1)); done
echo "### TABLE ###"; cat /tmp/gxopus_p8/p8/TABLE.txt
echo "### M_IPLR tail ###"; tail -5 /tmp/gxopus_p8/p8/probe_M_IPLR.txt
wc -l /tmp/gxopus_p8/p8/probe_M_IPLR.txt
