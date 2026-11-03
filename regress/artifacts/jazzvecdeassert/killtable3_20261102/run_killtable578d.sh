#!/bin/bash
# run_killtable578d.sh -- #578 TABLE 3: the deletion form (final comment, apply_fix578c.py) with the 24-row probe.  Scratch clones only.
# Builds the fix clone /tmp/gxfix578c first (from the HEAD clone /tmp/gxdivw), then base, fixed, null medium, 13 mutants.
set -u
W=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w578; K=$W/killtable3_20261102; B=/tmp/gxdivw; F=/tmp/gxfix578c; M=/tmp/gxmut578c
mkdir -p "$K"; cp -p "$W/jazz_vector_probe.py" "$K/jazz_vector_probe.ASRUN.py"
PROBE=$K/jazz_vector_probe.ASRUN.py; LOG=$K/KILLTABLE3.log
leg() { local OUT=$K/$2.raw
  { echo "LEG $2 binary=$1 $(ls -la --time-style=+%F_%T "$1" 2>/dev/null | awk '{print $5, $6}') md5=$(md5sum "$1" 2>/dev/null | cut -c1-12)";
    if [ -f "$(dirname "$1")/src/devices/dev_jazz.c" ]; then echo "binary newer than dev_jazz.c: $( [ "$1" -nt "$(dirname "$1")/src/devices/dev_jazz.c" ] && echo yes || echo NO-STALE )"; else echo "binary newer than dev_jazz.c: N/A (no source tree beside this binary)"; fi
    echo "sentinel: $(cat "$(dirname "$1")/.MUTANT" 2>/dev/null || echo none)"; echo "instrument: $PROBE md5=$(md5sum "$PROBE" | cut -c1-12)"; } > "$OUT"
  cd /tmp && JAZZVEC_LOG=$K/transcript_$2.log timeout 600 python3 -u "$PROBE" "$1" >> "$OUT" 2>&1
  echo "LEG_DONE $2 $(grep -E '^JAZZVEC_RESULT=' "$OUT" || echo 'JAZZVEC_RESULT=NONE') $(grep -E '^JAZZVEC_DRIVER=' "$OUT" || echo 'JAZZVEC_DRIVER=NONE')" | tee -a "$OUT"; }
echo "killtable578 TABLE 3 start $(date '+%F %T')" | tee "$LOG"
echo "PRETABLE3.out mtime: $(ls -la --time-style=+%F_%T "$K/PRETABLE3.out" 2>/dev/null | awk '{print $6}')" | tee -a "$LOG"
# the fix clone, final comment
rm -rf "$F"; cp -a "$B" "$F"; cd "$F" || exit 1
echo "MUTANT: src/devices/dev_jazz.c #578 DELETION fix, final comment (scratch clone, intentional)" > .MUTANT
python3 "$W/apply_fix578c.py" "$F/src/devices/dev_jazz.c" >> "$LOG" 2>&1 || { echo "APPLY FAILED" | tee -a "$LOG"; exit 1; }
rm -f src/devices/dev_jazz.o; make -j4 > make_fix.log 2>&1; rc=$?
if [ -x gxemul ] && [ gxemul -nt src/devices/dev_jazz.c ]; then echo "fixc BINARY_FRESH rc=$rc $(ls -la --time-style=+%T gxemul | awk '{print $5, $6}')" | tee -a "$LOG"; else echo "fixc BINARY_STALE_OR_MISSING rc=$rc" | tee -a "$LOG"; exit 1; fi
diff -u "$B/src/devices/dev_jazz.c" "$F/src/devices/dev_jazz.c" > "$W/product_c.diff"; echo "product_c.diff lines: $(wc -l < "$W/product_c.diff")" | tee -a "$LOG"
leg "$B/gxemul" base_head | tail -1 | tee -a "$LOG"
leg "$F/gxemul" fixedc | tail -1 | tee -a "$LOG"
leg /bin/true M_c_absent | tail -1 | tee -a "$LOG"
for mut in M_b M_offs0 M_offsne0 M_rd M_wr M_offs2 M_cond M_uart M_dfltw M_idnz M_id0 M_lbnz M_len2 M_vecb M_off3; do
    rm -rf "$M"; cp -a "$F" "$M"
    echo "MUTANT: src/devices/dev_jazz.c $mut (scratch clone, #578 table 3)" > "$M/.MUTANT"
    if ! python3 "$W/mutate578c.py" "$mut" "$M/src/devices/dev_jazz.c" >> "$LOG" 2>&1; then echo "$mut APPLY-FAILED" | tee -a "$LOG"; continue; fi
    echo "--- $mut diff vs fixedc:" >> "$LOG"; diff "$F/src/devices/dev_jazz.c" "$M/src/devices/dev_jazz.c" >> "$LOG"
    ( cd "$M" && rm -f src/devices/dev_jazz.o && make -j4 > "make_$mut.log" 2>&1 ); rc=$?
    if [ $rc != 0 ] || [ ! "$M/gxemul" -nt "$M/src/devices/dev_jazz.c" ]; then echo "$mut BUILD-FAILED rc=$rc" | tee -a "$LOG"; tail -3 "$M/make_$mut.log" >> "$LOG"; continue; fi
    leg "$M/gxemul" "$mut" | tail -1 | tee -a "$LOG"
done
rm -rf "$M"
echo "KILLTABLE578_T3_DONE $(date '+%F %T')" | tee -a "$LOG"
