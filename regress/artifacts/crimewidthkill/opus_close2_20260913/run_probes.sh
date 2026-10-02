#!/bin/bash
# run the FROZEN 111-row probe against baseline + each mutant, one at a time
set -u
P=/tmp/cwp_close2.py
OUT=/tmp/close2
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_close2
mkdir -p $OUT/logs
md5sum $P > $OUT/logs/INSTRUMENT.md5
LIST="${1:-base rd_hi_lh soft_gate rd_hi_lb rd_lh_all}"
for m in $LIST; do
    if [ "$m" = base ]; then B=/tmp/gx529c2_base; else B=$OUT/builds/gx_$m; fi
    [ -x "$B" ] || { echo "NOBIN $m" | tee -a $OUT/table_c2.out; continue; }
    t0=$(date +%s)
    python3 -u $P "$B" "$m" > $OUT/logs/probe_$m.raw 2>&1
    t1=$(date +%s)
    last=$(tail -1 $OUT/logs/probe_$m.raw)
    res=$(grep -o 'CRIMEP_RESULT=[0-9/]*' $OUT/logs/probe_$m.raw)
    ctl=$(grep -o 'CRIMEP_CONTROL=[A-Z]*' $OUT/logs/probe_$m.raw)
    fl=$(grep '^FAILING:' $OUT/logs/probe_$m.raw)
    echo "NEW $m $res $ctl last=$last secs=$((t1-t0)) | $fl" | tee -a $OUT/table_c2.out
    cp $OUT/logs/probe_$m.raw "$SP/logs/" 2>/dev/null
done
cp $OUT/table_c2.out "$SP/" 2>/dev/null
echo PROBES_DONE
