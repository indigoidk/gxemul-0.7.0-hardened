#!/bin/bash
# #545 repair 3c kill table.  PRETABLE_Q2d.out and PREDICTIONS.txt/.tsv were written BEFORE this run (their mtimes
# are logged first).  Scratch trees only: /tmp/fbd5r3c_gen, /tmp/fbd5r3c_fix, /tmp/fbd5r3c_w0..3; nothing under
# GXEMUL-SEC/src is written.  Every script this run executes is copied into the artifacts dir first and run from there.
set -u
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
Z=$R/_scratchpad/fbd5/q2d/r3c
OUT=$SEC/regress/artifacts/fbd5/q2_20260923/r3c_20260923
: > "$OUT/R3C.log"
log() { echo "$*" | tee -a "$OUT/R3C.log"; }
cp "$R/_scratchpad/fbd5/q2d/diff_footbridge.r3c.c" "$OUT/diff_footbridge.r3c.c"
for f in gen_r3c.sh gen_opus_r3x.py gen_q2e_r3c.py run_r3c_worker.py analyze_r3c.py run_r3c.sh; do cp "$Z/$f" "$OUT/$f"; done
log "R3C_START $(date '+%F %T')  SEC dev_footbridge.c $(md5sum $SEC/src/devices/dev_footbridge.c | cut -c1-8)  instrument $(md5sum $OUT/diff_footbridge.r3c.c | cut -c1-8)"
log "order: PRETABLE_Q2d.out $(stat -c %y $OUT/PRETABLE_Q2d.out | cut -c1-19)   PREDICTIONS.txt $(stat -c %y $OUT/PREDICTIONS.txt | cut -c1-19)"
bash "$OUT/gen_r3c.sh" > "$OUT/GEN.log" 2>&1
log "GEN: $(grep -c ' ok ' $OUT/GEN.log) carried/closing/codex variants built; $(grep -cE 'NOAPPLY|NOOP|ANCHOR-ERROR' $OUT/GEN.log) not; $(grep -E '^OPUS VARIANTS|^VARIANT FILES|RESTORED' $OUT/GEN.log | tr '\n' ' ')"
F=/tmp/fbd5r3c_fix
rm -rf "$F"; mkdir -p "$F/regress"; cp -a "$SEC/src" "$F/src"; cp "$OUT/diff_footbridge.r3c.c" "$F/regress/diff_footbridge.c"; cp "$R/build/config.h" "$F/config.h"
( cd "$F/regress" && gcc -O2 -std=c99 -Wall -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections \
    -Wl,--gc-sections -I"$F/src" -I"$F/src/include" -I"$F/src/include/thirdparty" -o "$F/d" diff_footbridge.c -lm ) > "$OUT/cc_FIX.log" 2>&1
"$F/d" > "$OUT/diff_FIX.log" 2>&1; rc=$?
log "FIX rc=$rc $(grep -E 'rows, ' $OUT/diff_FIX.log)  $(grep -E '^DIFF_FOOTBRIDGE_' $OUT/diff_FIX.log)  compiler warnings: $(grep -c 'warning:' $OUT/cc_FIX.log)"
grep '^  ok    ' "$SEC/regress/artifacts/fbd5/q2_20260923/r3_20260923/diff_FIX.log" | grep -v 'IDENTITY' | sort > /tmp/fbd5r3c_862prev.txt
grep '^  ok    ' "$OUT/diff_FIX.log" | sort > /tmp/fbd5r3c_864ok.txt
comm -23 /tmp/fbd5r3c_862prev.txt /tmp/fbd5r3c_864ok.txt > "$OUT/superset_missing.txt"
log "SUPERSET: $(wc -l < /tmp/fbd5r3c_862prev.txt) ok-lines of the 862-row FIX run (IDENTITY excluded); missing from the 864-row run: $(wc -l < $OUT/superset_missing.txt)"
for k in 0 1 2 3; do python3 "$OUT/run_r3c_worker.py" $k 4 > "$OUT/worker_$k.out" 2>&1 & done
wait
for k in 0 1 2 3; do log "$(grep -E '^WORKER ' $OUT/worker_$k.out | tr '\n' ' ')"; done
python3 "$OUT/analyze_r3c.py" > "$OUT/TABLE.txt" 2>&1
sed -n '/^#545 r3c TABLE/,/^$/p' "$OUT/TABLE.txt" | tee -a "$OUT/R3C.log"
log "R3C_DONE $(date '+%F %T')"
