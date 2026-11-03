#!/bin/bash
# run_killtable578c.sh -- #578 TABLE 2: the deletion form with the 22-row self-contained probe.  Scratch clones only.
set -u
W=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w578; K=$W/killtable2_20261102; B=/tmp/gxdivw; F=/tmp/gxfix578b; M=/tmp/gxmut578b
PROBE=$K/jazz_vector_probe.ASRUN.py; LOG=$K/KILLTABLE2.log
leg() { local OUT=$K/$2.raw
  { echo "LEG $2 binary=$1 $(ls -la --time-style=+%F_%T "$1" 2>/dev/null | awk '{print $5, $6}') md5=$(md5sum "$1" 2>/dev/null | cut -c1-12)";
    echo "binary newer than dev_jazz.c: $( [ "$1" -nt "$(dirname "$1")/src/devices/dev_jazz.c" ] && echo yes || echo NO-STALE )";
    echo "sentinel: $(cat "$(dirname "$1")/.MUTANT" 2>/dev/null || echo none)"; echo "instrument: $PROBE md5=$(md5sum "$PROBE" | cut -c1-12)"; } > "$OUT"
  cd /tmp && JAZZVEC_LOG=$K/transcript_$2.log timeout 600 python3 -u "$PROBE" "$1" >> "$OUT" 2>&1
  echo "LEG_DONE $2 $(grep -E '^JAZZVEC_RESULT=' "$OUT" || echo 'JAZZVEC_RESULT=NONE')" | tee -a "$OUT"; }
echo "killtable578 TABLE 2 start $(date '+%F %T')" | tee "$LOG"
leg "$B/gxemul" base_head | tail -1 | tee -a "$LOG"
leg "$F/gxemul" fixedb | tail -1 | tee -a "$LOG"
leg /bin/true M_c_absent | tail -1 | tee -a "$LOG"
for mut in M_b M_offs0 M_offsne0 M_rd M_wr M_offs2 M_cond M_uart; do
    rm -rf "$M"; cp -a "$F" "$M"
    echo "MUTANT: src/devices/dev_jazz.c $mut (scratch clone, #578 table 2)" > "$M/.MUTANT"
    if ! python3 "$W/mutate578b.py" "$mut" "$M/src/devices/dev_jazz.c" >> "$LOG" 2>&1; then echo "$mut APPLY-FAILED" | tee -a "$LOG"; continue; fi
    echo "--- $mut diff vs fixedb:" >> "$LOG"; diff "$F/src/devices/dev_jazz.c" "$M/src/devices/dev_jazz.c" >> "$LOG"
    ( cd "$M" && rm -f src/devices/dev_jazz.o && make -j4 > "make_$mut.log" 2>&1 ); rc=$?
    if [ $rc != 0 ] || [ ! "$M/gxemul" -nt "$M/src/devices/dev_jazz.c" ]; then echo "$mut BUILD-FAILED rc=$rc" | tee -a "$LOG"; tail -3 "$M/make_$mut.log" >> "$LOG"; continue; fi
    leg "$M/gxemul" "$mut" | tail -1 | tee -a "$LOG"
done
rm -rf "$M"
echo "KILLTABLE578_T2_DONE $(date '+%F %T')" | tee -a "$LOG"
