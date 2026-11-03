#!/bin/bash
# run_mutleg577.sh <mutant> -- one post-table #577 leg: /tmp/gxmut577_<mutant> = a copy of the FIXED clone + mutate577.py <mutant>,
# built, scored with the AS-RUN instrument (the preserved sh_tlbmulti_probe.ASRUN.py), then deleted.  No project tree is touched.
# Same per-mutant recipe as run_killtable577.sh / run_mguard577.sh so the leg is comparable with the table's.
set -u
MUT=$1
W=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w577; K=$W/killtable_20261102; F=/tmp/gxfix577; M=/tmp/gxmut577_$MUT
PROBE=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/shblreset/killtable_20261102/sh_tlbmulti_probe.ASRUN.py
KERNEL=/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd
LOG=$K/MUTLEG_$MUT.log
echo "mutleg577 $MUT start $(date '+%F %T')" | tee "$LOG"
[ "$F/gxemul" -nt "$F/src/cpus/cpu_sh.c" ] || { echo "FIXED CLONE STALE -- leg not run" | tee -a "$LOG"; exit 1; }
n=$(grep -c 'EXPEVT_RESET_MANUAL;' "$F/src/cpus/cpu_sh.c"); [ "$n" = 1 ] || { echo "fixed clone fix count $n -- leg not run" | tee -a "$LOG"; exit 1; }
[ -f "$PROBE" ] || { echo "AS-RUN PROBE MISSING -- leg not run" | tee -a "$LOG"; exit 1; }
rm -rf "$M"; cp -a "$F" "$M"
echo "MUTANT: src/cpus/cpu_sh.c $MUT (scratch clone, #577 table addendum)" > "$M/.MUTANT"
python3 "$W/mutate577.py" "$MUT" "$M/src/cpus/cpu_sh.c" >> "$LOG" 2>&1 || { echo "$MUT APPLY-FAILED" | tee -a "$LOG"; exit 1; }
echo "--- mutant diff against the fixed clone:" >> "$LOG"; diff "$F/src/cpus/cpu_sh.c" "$M/src/cpus/cpu_sh.c" >> "$LOG"
( cd "$M" && rm -f src/cpus/cpu_sh*.o && make -j4 > "make_$MUT.log" 2>&1 ); rc=$?
if [ $rc != 0 ] || [ ! "$M/gxemul" -nt "$M/src/cpus/cpu_sh.c" ]; then echo "$MUT BUILD-FAILED rc=$rc" | tee -a "$LOG"; tail -3 "$M/make_$MUT.log" >> "$LOG"; exit 1; fi
OUT=$K/$MUT.raw
{ echo "LEG $MUT binary=$M/gxemul $(ls -la --time-style=+%F_%T "$M/gxemul" | awk '{print $5, $6}') md5=$(md5sum "$M/gxemul" | cut -c1-12)";
  echo "binary newer than cpu_sh.c: $( [ "$M/gxemul" -nt "$M/src/cpus/cpu_sh.c" ] && echo yes || echo NO-STALE )";
  echo "sentinel: $(cat "$M/.MUTANT")";
  echo "instrument: $PROBE md5=$(md5sum "$PROBE" | cut -c1-12)"; } > "$OUT"
cd /tmp && python3 -u "$PROBE" "$M/gxemul" "$KERNEL" >> "$OUT" 2>&1
echo "LEG_DONE $MUT $(grep -E '^SH_TLBMULTI_RESULT=' "$OUT")" | tee -a "$OUT" "$LOG"
rm -rf "$M"
echo "MUTLEG577_DONE $MUT $(date '+%F %T')" | tee -a "$LOG"
