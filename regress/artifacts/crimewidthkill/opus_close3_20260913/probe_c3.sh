#!/bin/bash
# run the FROZEN shipped 121-row probe against base + 12 mutants in 4 lanes, then the discriminators (serial, alone),
# then copy durable outputs to the ONE artifacts dir and delete the clone.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus529c3
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_close3
ART=$SEC/regress/artifacts/crimewidthkill/opus_close3_20260913
OUT=/tmp/oc3
P=/tmp/cwp_close3.py
md5sum $P >> $OUT/logs/INSTRUMENT.md5
echo "probes start $(date '+%F %T')" | tee -a $OUT/logs/ORDER.txt

lane() {
    for m in "$@"; do
        B=$OUT/builds/gx_$m
        [ -x "$B" ] || { echo "NOBIN $m"; continue; }
        t0=$(date +%s)
        python3 -u $P "$B" "$m" > $OUT/logs/probe_$m.raw 2>&1
        t1=$(date +%s)
        echo "RUN $m $(grep -o 'CRIMEP_RESULT=[0-9/]*' $OUT/logs/probe_$m.raw) $(grep -o 'CRIMEP_CONTROL=[A-Z]*' $OUT/logs/probe_$m.raw) last=$(tail -1 $OUT/logs/probe_$m.raw) secs=$((t1-t0)) | $(grep '^FAILING:' $OUT/logs/probe_$m.raw)"
    done
}
lane base rearm_ctlrd pre_revbr ans_hi32_b5 > $OUT/logs/lane0.out 2>&1 &
sleep 20
lane rearm_dogclr pre_dogbr byp_time ans_ctl_lb > $OUT/logs/lane1.out 2>&1 &
sleep 20
lane rearm_ctl0 pre_istat land_b4clr > $OUT/logs/lane2.out 2>&1 &
sleep 20
lane byp_rev pre_ctlrd > $OUT/logs/lane3.out 2>&1 &
wait
cat $OUT/logs/lane?.out | sort -k2 > $OUT/table_c3.out
echo "probes end $(date '+%F %T')" | tee -a $OUT/logs/ORDER.txt
cat $OUT/table_c3.out
echo "LOGS ending CRIMEP_DONE: $(for f in $OUT/logs/probe_*.raw; do tail -1 $f; done | grep -c '^CRIMEP_DONE$') of $(ls $OUT/logs/probe_*.raw | wc -l)"

# ---- discriminators, serial, nothing else running ----
for m in rearm_ctlrd rearm_dogclr rearm_ctl0 pre_istat pre_revbr pre_dogbr pre_ctlrd byp_rev byp_time ans_hi32_b5 land_b4clr ans_ctl_lb; do
    [ -x $OUT/builds/gx_$m ] || continue
    python3 -u $OUT/disc_c3.FROZEN.py $OUT/builds/gx_base $OUT/builds/gx_$m $m >> $OUT/logs/disc_c3.out 2>&1
done
cat $OUT/logs/disc_c3.out

# ---- durable copies ----
mkdir -p $ART/logs
cp $OUT/logs/* $OUT/table_c3.out $ART/logs/ 2>/dev/null
mv $ART/logs/table_c3.out $ART/
cp $SP/PRETABLE.out $SP/mutants_c3.py $SP/disc_c3.py $SP/build_c3.sh $SP/probe_c3.sh $ART/
cp $SP/logs/build_c3.out $ART/logs/ 2>/dev/null

# ---- delete the clone (only if no sentinel) ----
if [ -e $C/.MUTANT ]; then echo "SENTINEL PRESENT -- clone NOT deleted"; else rm -rf $C; fi
ls -d $C 2>/dev/null || echo "clone deleted"
echo PROBE_DONE
