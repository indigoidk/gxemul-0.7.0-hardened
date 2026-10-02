#!/bin/bash
set -u
BINS=/tmp/gxopuscrimec7_bins
WD=/tmp/gxopuscrimec7_work
OUT=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close7_20260915
cp "$OUT/scripts/disc7b.py" "$WD/disc7b.frozen.py"
md5sum "$WD/disc7b.frozen.py"
for name in base E2_byp_time4 E1_byp_ctl4r E3b_byp_revout_acc F1_byp_ctl8w_0201 F1b_byp_ctl4w_0201 F3_byp_sw04; do
    n=2; case $name in base|E2_byp_time4) n=6;; esac
    python3 -u "$WD/disc7b.frozen.py" "$BINS/$name" "$name" "$n" > "$OUT/logs/disc7b_$name.out" 2>&1
    echo "$(date +%T) $name $(tail -1 "$OUT/logs/disc7b_$name.out")"
done
echo DISCALL7B_DONE
