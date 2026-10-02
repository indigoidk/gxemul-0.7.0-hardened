#!/bin/bash
# run the FROZEN shipped 131-row probe against base + 5 mutants (2 lanes, gentle: other tables run), then durable copy.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopuscrime4
ART=$SEC/regress/artifacts/crimewidthkill/opus_close4_20260914
OUT=/tmp/oc4
P=/tmp/cwp_close4.py
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
lane base c1_deepseek c2_kimik3 > $OUT/logs/lane0.out 2>&1 &
sleep 25
lane c3_codex_dbg c4_kimicli c5_codex_b1 > $OUT/logs/lane1.out 2>&1 &
wait
cat $OUT/logs/lane?.out | sort -k2 > $OUT/table_c4.out
echo "probes end $(date '+%F %T')" | tee -a $OUT/logs/ORDER.txt
cat $OUT/table_c4.out
echo "LOGS ending CRIMEP_DONE: $(for f in $OUT/logs/probe_*.raw; do tail -1 $f; done | grep -c '^CRIMEP_DONE$') of $(ls $OUT/logs/probe_*.raw | wc -l)"

mkdir -p $ART/logs
cp $OUT/logs/* $OUT/table_c4.out $ART/logs/ 2>/dev/null
mv $ART/logs/table_c4.out $ART/ 2>/dev/null
echo PROBE_C4_DONE
