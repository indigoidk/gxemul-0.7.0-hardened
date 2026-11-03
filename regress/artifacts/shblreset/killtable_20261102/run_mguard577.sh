#!/bin/bash
# run_mguard577.sh -- the #577 GUARD-side clause-(d) leg (Fable pass 2, change 1).  /tmp/gxmut577g = a copy of the FIXED clone
# + mutate577.py M_guard, built, scored with the AS-RUN instrument (the preserved sh_tlbmulti_probe.ASRUN.py), then deleted.
# No project tree is touched.  Same per-mutant recipe as run_killtable577.sh so the leg is comparable with the table's.
set -u
W=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w577; K=$W/killtable_20261102; F=/tmp/gxfix577; M=/tmp/gxmut577g
PROBE=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/shblreset/killtable_20261102/sh_tlbmulti_probe.ASRUN.py
KERNEL=/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd
LOG=$K/MGUARD.log
echo "mguard577 start $(date '+%F %T')" | tee "$LOG"
# Baseline identity before mutant 1: the fixed clone is FRESH and carries the fix exactly once.
[ "$F/gxemul" -nt "$F/src/cpus/cpu_sh.c" ] || { echo "FIXED CLONE STALE -- leg not run" | tee -a "$LOG"; exit 1; }
n=$(grep -c 'EXPEVT_RESET_MANUAL;' "$F/src/cpus/cpu_sh.c"); [ "$n" = 1 ] || { echo "fixed clone fix count $n -- leg not run" | tee -a "$LOG"; exit 1; }
[ -f "$PROBE" ] || { echo "AS-RUN PROBE MISSING -- leg not run" | tee -a "$LOG"; exit 1; }
rm -rf "$M"; cp -a "$F" "$M"
echo "MUTANT: src/cpus/cpu_sh.c M_guard (scratch clone, #577 table addendum)" > "$M/.MUTANT"
python3 "$W/mutate577.py" M_guard "$M/src/cpus/cpu_sh.c" >> "$LOG" 2>&1 || { echo "M_guard APPLY-FAILED" | tee -a "$LOG"; exit 1; }
echo "--- mutant diff against the fixed clone:" >> "$LOG"; diff "$F/src/cpus/cpu_sh.c" "$M/src/cpus/cpu_sh.c" >> "$LOG"
( cd "$M" && rm -f src/cpus/cpu_sh*.o && make -j4 > make_M_guard.log 2>&1 ); rc=$?
if [ $rc != 0 ] || [ ! "$M/gxemul" -nt "$M/src/cpus/cpu_sh.c" ]; then echo "M_guard BUILD-FAILED rc=$rc" | tee -a "$LOG"; tail -3 "$M/make_M_guard.log" >> "$LOG"; exit 1; fi
OUT=$K/M_guard.raw
{ echo "LEG M_guard binary=$M/gxemul $(ls -la --time-style=+%F_%T "$M/gxemul" | awk '{print $5, $6}') md5=$(md5sum "$M/gxemul" | cut -c1-12)";
  echo "binary newer than cpu_sh.c: $( [ "$M/gxemul" -nt "$M/src/cpus/cpu_sh.c" ] && echo yes || echo NO-STALE )";
  echo "sentinel: $(cat "$M/.MUTANT")";
  echo "instrument: $PROBE md5=$(md5sum "$PROBE" | cut -c1-12)"; } > "$OUT"
cd /tmp && python3 -u "$PROBE" "$M/gxemul" "$KERNEL" >> "$OUT" 2>&1
echo "LEG_DONE M_guard $(grep -E '^SH_TLBMULTI_RESULT=' "$OUT")" | tee -a "$OUT" "$LOG"
rm -rf "$M"
echo "MGUARD577_DONE $(date '+%F %T')" | tee -a "$LOG"
