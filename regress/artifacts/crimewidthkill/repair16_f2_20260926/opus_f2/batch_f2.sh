#!/bin/bash
# batch_f2.sh TAG NAME... -- repair 16's frozen 226-row probe (5f770991) against each named binary of
# /tmp/gxopus_r15p2_bins, one lane per name (at most four).  Launch a FROZEN COPY of this file, with run_in_background.
set -u
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/repair16_f2_20260926/opus_f2
T16=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/table16_20260926
B=/tmp/gxopus_r15p2_bins
TAG=$1; shift
P=/tmp/crimep_f2_$TAG.frozen.py
cp "$T16/crime_width_probe.table16.py" "$P"
case "$(md5sum "$P" | cut -c1-8)" in 5f770991) echo "INSTRUMENT OK 5f770991";; *) echo "INSTRUMENT MISMATCH -- abort"; exit 1;; esac
mkdir -p "$A/runs"
echo "BATCH $TAG START $(date '+%F %T')  lanes: $*  load: $(cut -d' ' -f1-3 /proc/loadavg)"
for m in "$@"; do
    ( python3 -u "$P" "$B/$m" "$m" > "$A/runs/probe_$m.raw" 2>&1
      echo "$m $(grep '^CRIMEP_RESULT=' "$A/runs/probe_$m.raw") $(grep '^CRIMEP_CONTROL=' "$A/runs/probe_$m.raw") done=$(grep -c '^CRIMEP_DONE' "$A/runs/probe_$m.raw") FAILING:$(grep '^FAILING:' "$A/runs/probe_$m.raw" | cut -c9-) $(date '+%T')" ) &
done
wait
echo "BATCH $TAG DONE $(date '+%F %T')  load: $(cut -d' ' -f1-3 /proc/loadavg)"
