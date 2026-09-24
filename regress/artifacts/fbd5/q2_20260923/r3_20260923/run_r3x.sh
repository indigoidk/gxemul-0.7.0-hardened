#!/bin/bash
# #545 repair 3 (r3x) kill table.  PRETABLE_Q2c.out and PREDICTIONS.txt/.tsv were written BEFORE this run (their mtimes
# are logged first).  Scratch trees only: /tmp/fbd5r3x_gen, /tmp/fbd5r3x_fix, /tmp/fbd5r3x_w0..3; nothing under
# GXEMUL-SEC/src is written.  Every script this run executes is copied into the artifacts dir first and run from there.
set -u
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
Z=$R/_scratchpad/fbd5/q2d/r3x
OUT=$SEC/regress/artifacts/fbd5/q2_20260923/r3_20260923
: > "$OUT/R3X.log"
log() { echo "$*" | tee -a "$OUT/R3X.log"; }
cp "$R/_scratchpad/fbd5/q2d/diff_footbridge.r3x.c" "$OUT/diff_footbridge.r3x.c"
for f in gen_r3x.sh gen_opus_r3x.py run_r3x_worker.py analyze_r3x.py run_r3x.sh; do cp "$Z/$f" "$OUT/$f"; done
log "R3X_START $(date '+%F %T')  SEC dev_footbridge.c $(md5sum $SEC/src/devices/dev_footbridge.c | cut -c1-8)  instrument $(md5sum $OUT/diff_footbridge.r3x.c | cut -c1-8)"
log "order: PRETABLE_Q2c.out $(stat -c %y $OUT/PRETABLE_Q2c.out | cut -c1-19)   PREDICTIONS.txt $(stat -c %y $OUT/PREDICTIONS.txt | cut -c1-19)"
bash "$OUT/gen_r3x.sh" > "$OUT/GEN.log" 2>&1
log "GEN: $(grep -c ' ok ' $OUT/GEN.log) carried/closing/codex variants built; $(grep -cE 'NOAPPLY|NOOP|ANCHOR-ERROR' $OUT/GEN.log) not; $(grep -E '^OPUS VARIANTS|^VARIANT FILES|RESTORED' $OUT/GEN.log | tr '\n' ' ')"
F=/tmp/fbd5r3x_fix
rm -rf "$F"; mkdir -p "$F/regress"; cp -a "$SEC/src" "$F/src"; cp "$OUT/diff_footbridge.r3x.c" "$F/regress/diff_footbridge.c"; cp "$R/build/config.h" "$F/config.h"
( cd "$F/regress" && gcc -O2 -std=c99 -Wall -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections \
    -Wl,--gc-sections -I"$F/src" -I"$F/src/include" -I"$F/src/include/thirdparty" -o "$F/d" diff_footbridge.c -lm ) > "$OUT/cc_FIX.log" 2>&1
"$F/d" > "$OUT/diff_FIX.log" 2>&1; rc=$?
log "FIX rc=$rc $(grep -E 'rows, ' $OUT/diff_FIX.log)  $(grep -E '^DIFF_FOOTBRIDGE_' $OUT/diff_FIX.log)  compiler warnings: $(grep -c 'warning:' $OUT/cc_FIX.log)"
grep '^  ok    ' "$SEC/regress/artifacts/fbd5/q2_20260923/repair2/diff_FIX.log" | grep -v 'IDENTITY' | sort > /tmp/fbd5r3x_707ok.txt
grep '^  ok    ' "$OUT/diff_FIX.log" | sort > /tmp/fbd5r3x_862ok.txt
comm -23 /tmp/fbd5r3x_707ok.txt /tmp/fbd5r3x_862ok.txt > "$OUT/superset_missing.txt"
log "SUPERSET: $(wc -l < /tmp/fbd5r3x_707ok.txt) ok-lines of the 707-row FIX run (IDENTITY excluded); missing from the 862-row run: $(wc -l < $OUT/superset_missing.txt)"
for k in 0 1 2 3; do python3 "$OUT/run_r3x_worker.py" $k 4 > "$OUT/worker_$k.out" 2>&1 & done
wait
for k in 0 1 2 3; do log "$(grep -E '^WORKER ' $OUT/worker_$k.out | tr '\n' ' ')"; done
python3 "$OUT/analyze_r3x.py" > "$OUT/TABLE.txt" 2>&1
sed -n '/^#545 r3x TABLE/,/^$/p' "$OUT/TABLE.txt" | tee -a "$OUT/R3X.log"
log "R3X_DONE $(date '+%F %T')"
