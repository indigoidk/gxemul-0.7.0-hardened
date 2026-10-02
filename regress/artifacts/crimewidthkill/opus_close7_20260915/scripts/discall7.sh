#!/bin/bash
# discall7.sh -- run disc7.py (frozen copy) against every clone binary; base and E2 get 6 free-running TIME runs each.
set -u
BINS=/tmp/gxopuscrimec7_bins
WD=/tmp/gxopuscrimec7_work
OUT=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close7_20260915
cp "$OUT/scripts/disc7.py" "$WD/disc7.frozen.py"
for name in base E2_byp_time4 K1_w_imask4w K2_w_rev4 K3_w_ctl8r E1_byp_ctl4r E3_byp_revout; do
    n=2; case $name in base|E2_byp_time4) n=6;; esac
    python3 -u "$WD/disc7.frozen.py" "$BINS/$name" "$name" "$n" > "$OUT/logs/disc_$name.out" 2>&1
    echo "$(date +%T) $name $(tail -1 "$OUT/logs/disc_$name.out")"
done
echo DISCALL7_DONE
