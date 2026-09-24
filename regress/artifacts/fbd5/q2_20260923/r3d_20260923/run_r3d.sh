#!/bin/bash
# #545 repair 3d kill table.  PRETABLE_Q2e.out and PREDICTIONS.txt/.tsv were written BEFORE this run (their mtimes
# are logged first).  Scratch trees only: /tmp/fbd5r3d_*; nothing under GXEMUL-SEC/src is written.  Every script this
# run executes is copied into the artifacts dir first and run from there.
set -u
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
Z=$R/_scratchpad/fbd5/q2g/r3d
OUT=$SEC/regress/artifacts/fbd5/q2_20260923/r3d_20260923
: > "$OUT/R3D.log"
log() { echo "$*" | tee -a "$OUT/R3D.log"; }
cp "$R/_scratchpad/fbd5/q2g/diff_footbridge.r3d.c" "$OUT/diff_footbridge.r3d.c"
cp "$SEC/regress/diff_footbridge.c" "$OUT/diff_footbridge.r3c_8309.c"
for f in gen_r3d.py run_r3d_worker.py analyze_r3d.py mkpred_r3d.py run_r3d.sh; do cp "$Z/$f" "$OUT/$f"; done
cp "$R/_scratchpad/fbd5/q2g/patch_r3d.py" "$OUT/patch_r3d.py"
M3D=$(md5sum "$OUT/diff_footbridge.r3d.c" | cut -c1-8); M3C=$(md5sum "$OUT/diff_footbridge.r3c_8309.c" | cut -c1-8)
log "R3D_START $(date '+%F %T')  SEC dev_footbridge.c $(md5sum $SEC/src/devices/dev_footbridge.c | cut -c1-8)  r3d instrument $M3D  r3c instrument $M3C"
log "order: PRETABLE_Q2e.out $(stat -c %y $OUT/PRETABLE_Q2e.out | cut -c1-19)   PREDICTIONS.txt $(stat -c %y $OUT/PREDICTIONS.txt | cut -c1-19)"
python3 "$OUT/gen_r3d.py" > "$OUT/GEN.log" 2>&1
log "GEN: $(grep -c '^ok ' $OUT/GEN.log) new variant files; $(grep -c 'ANCHOR-ERROR' $OUT/GEN.log) anchor errors; $(grep -E '^CARRIED|^VARIANT FILES' $OUT/GEN.log | tr '\n' ' ')"
F=/tmp/fbd5r3d_fix
rm -rf "$F"; mkdir -p "$F/regress"; cp -a "$SEC/src" "$F/src"; cp "$OUT/diff_footbridge.r3d.c" "$F/regress/diff_footbridge.c"; cp "$R/build/config.h" "$F/config.h"
( cd "$F/regress" && gcc -O2 -std=c99 -Wall -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections \
    -Wl,--gc-sections -I"$F/src" -I"$F/src/include" -I"$F/src/include/thirdparty" -o "$F/d" diff_footbridge.c -lm ) > "$OUT/cc_FIX.log" 2>&1
"$F/d" > "$OUT/diff_FIX.log" 2>&1; rc=$?
log "FIX rc=$rc $(grep -E 'rows, ' $OUT/diff_FIX.log)  $(grep -E '^DIFF_FOOTBRIDGE_' $OUT/diff_FIX.log)  compiler warnings: $(grep -c 'warning:' $OUT/cc_FIX.log)"
grep '^  ok    ' "$SEC/regress/artifacts/fbd5/q2_20260923/r3c_20260923/diff_FIX.log" \
  | sed -e 's/Clear 0x10 clears it, CPU line deasserted once/Clear 0x10 clears it, the raw status kept, CPU line deasserted once/' \
        -e 's/Clear 0x400 keeps it, CPU line asserted once/Clear 0x400 keeps it, the raw status kept, CPU line asserted once/' \
  | sort > /tmp/fbd5r3d_864prev.txt
grep '^  ok    ' "$OUT/diff_FIX.log" | sort > /tmp/fbd5r3d_864ok.txt
comm -23 /tmp/fbd5r3d_864prev.txt /tmp/fbd5r3d_864ok.txt > "$OUT/superset_missing.txt"
comm -13 /tmp/fbd5r3d_864prev.txt /tmp/fbd5r3d_864ok.txt > "$OUT/superset_new.txt"
log "SUPERSET: $(wc -l < /tmp/fbd5r3d_864prev.txt) ok-lines of the r3c FIX run (two renamed); missing from r3d: $(wc -l < $OUT/superset_missing.txt); new on r3d: $(wc -l < $OUT/superset_new.txt)"
ls /tmp/fbd5r3d_var | grep '\.c$' | grep -v '^FIX\.c$' | sed 's/\.c$//' | sort > "$OUT/list_all.txt"
grep '^R3D_' "$OUT/list_all.txt" > "$OUT/list_new.txt"
log "LISTS: $(wc -l < $OUT/list_all.txt) variants on r3d; $(wc -l < $OUT/list_new.txt) new shapes also on r3c"
for k in 0 1 2 3; do python3 "$OUT/run_r3d_worker.py" $k 4 r3d "$OUT/diff_footbridge.r3d.c" "$M3D" "$OUT/list_all.txt" > "$OUT/worker_r3d_$k.out" 2>&1 & done
wait
for k in 0 1; do python3 "$OUT/run_r3d_worker.py" $k 2 r3c "$OUT/diff_footbridge.r3c_8309.c" "$M3C" "$OUT/list_new.txt" > "$OUT/worker_r3c_$k.out" 2>&1 & done
wait
for f in "$OUT"/worker_*.out; do log "$(grep -E '^WORKER ' $f | tr '\n' ' ')"; done
python3 "$OUT/analyze_r3d.py" > "$OUT/TABLE.txt" 2>&1
sed -n '/^#545 r3d TABLE/,/^$/p' "$OUT/TABLE.txt" | tee -a "$OUT/R3D.log"
log "R3D_DONE $(date '+%F %T')"
