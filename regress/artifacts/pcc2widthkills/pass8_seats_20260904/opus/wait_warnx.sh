n=0
until grep -q "M_WARNX|" /tmp/gxopus_p8/p8/TABLE.txt 2>/dev/null || [ $n -ge 55 ]; do sleep 2; n=$((n+1)); done
echo "### TABLE ###"; cat /tmp/gxopus_p8/p8/TABLE.txt
echo "### rows so far ###"; wc -l /tmp/gxopus_p8/p8/probe_M_WARNX.txt 2>/dev/null
