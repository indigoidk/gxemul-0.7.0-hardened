#!/bin/bash
# run the FROZEN 85-row probe against the baseline and each built mutant, one at a time
set -u
OUT=/tmp/close529
P=/tmp/crime_close.FROZEN.py
ART=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close_20260913
mkdir -p $OUT/logs "$ART/logs"
md5sum $P > $OUT/logs/INSTRUMENT.md5
cp $OUT/logs/INSTRUMENT.md5 "$ART/logs/"
LIST="${1:-base lt_len c_dog rearm4 pre4 rearm_time ctl_collide wst_mc2 lt_blk rd_hi lt_wl wnz_lbl acc4_210}"
for m in $LIST; do
    if [ "$m" = base ]; then B=/tmp/gx529close_base; else B=$OUT/builds/gx_$m; fi
    [ -x "$B" ] || { echo "NOBIN $m"; continue; }
    t0=$(date +%s)
    python3 -u $P "$B" "$m" > $OUT/logs/probe_$m.raw 2>&1
    t1=$(date +%s)
    last=$(tail -1 $OUT/logs/probe_$m.raw)
    res=$(grep -o 'CRIMEP_RESULT=[0-9/]*' $OUT/logs/probe_$m.raw)
    ctl=$(grep -o 'CRIMEP_CONTROL=[A-Z]*' $OUT/logs/probe_$m.raw)
    fl=$(grep '^FAILING:' $OUT/logs/probe_$m.raw)
    echo "NEW $m $res $ctl last=$last secs=$((t1-t0)) $fl" | tee -a $OUT/table_close.out
    if [ "$last" = CRIMEP_DONE ]; then cp $OUT/logs/probe_$m.raw "$ART/logs/"; fi
    cp $OUT/table_close.out "$ART/"
done
echo PROBES_DONE
