#!/bin/bash
# probe_batch.sh TAG NAME... -- the frozen 218-row probe (f5e915f6) against each named binary of /tmp/gxopus_r15p2_bins,
# ONE LANE PER NAME (at most four), logs to this seat's runs/.  Launch with run_in_background; never edit while running.
set -u
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_r15p2_20260926
T14=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/table14_20260926
B=/tmp/gxopus_r15p2_bins
TAG=$1; shift
P=/tmp/crimep_r15p2_$TAG.frozen.py
cp "$T14/crime_width_probe.table14.py" "$P"
case "$(md5sum "$P" | cut -c1-8)" in f5e915f6) echo "INSTRUMENT OK f5e915f6";; *) echo "INSTRUMENT MISMATCH -- abort"; exit 1;; esac
mkdir -p "$A/runs"
echo "BATCH $TAG START $(date '+%F %T')  lanes: $*  load: $(cut -d' ' -f1-3 /proc/loadavg)"
for m in "$@"; do
    ( python3 -u "$P" "$B/$m" "$m" > "$A/runs/probe_$m.raw" 2>&1
      echo "$m $(grep '^CRIMEP_RESULT=' "$A/runs/probe_$m.raw") $(grep '^CRIMEP_CONTROL=' "$A/runs/probe_$m.raw") done=$(grep -c '^CRIMEP_DONE' "$A/runs/probe_$m.raw") FAILING:$(grep '^FAILING:' "$A/runs/probe_$m.raw" | cut -c9-) $(date '+%T')" ) &
done
wait
echo "BATCH $TAG DONE $(date '+%F %T')  load: $(cut -d' ' -f1-3 /proc/loadavg)"
