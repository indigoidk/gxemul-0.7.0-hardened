#!/bin/bash
# run_killtable577.sh -- #577 table: base (HEAD clone), fixed, then seven mutants in /tmp/gxmut577 (copy of the fixed clone per mutant,
# sentinel, deleted at the end).  No project tree is touched.
set -u
W=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w577; K=$W/killtable_20261102; B=/tmp/gxdivw; F=/tmp/gxfix577; M=/tmp/gxmut577
LOG=$K/KILLTABLE.log
echo "killtable577 start $(date '+%F %T')" | tee "$LOG"
bash "$W/run_probe_leg577.sh" "$B/gxemul" base_head | tail -1 | tee -a "$LOG"
bash "$W/run_probe_leg577.sh" "$F/gxemul" fixed | tail -1 | tee -a "$LOG"
for mut in M_b M_c M_noex M_wrongex M_lt100 M_trapaonly M_power; do
    rm -rf "$M"; cp -a "$F" "$M"
    echo "MUTANT: src/cpus/cpu_sh.c $mut (scratch clone, #577 table)" > "$M/.MUTANT"
    if ! python3 "$W/mutate577.py" "$mut" "$M/src/cpus/cpu_sh.c" >> "$LOG" 2>&1; then echo "$mut APPLY-FAILED" | tee -a "$LOG"; continue; fi
    ( cd "$M" && rm -f src/cpus/cpu_sh*.o && make -j4 > "make_$mut.log" 2>&1 ); rc=$?
    if [ $rc != 0 ] || [ ! "$M/gxemul" -nt "$M/src/cpus/cpu_sh.c" ]; then echo "$mut BUILD-FAILED rc=$rc" | tee -a "$LOG"; tail -3 "$M/make_$mut.log" >> "$LOG"; continue; fi
    bash "$W/run_probe_leg577.sh" "$M/gxemul" "$mut" | tail -1 | tee -a "$LOG"
done
rm -rf "$M"
echo "KILLTABLE577_DONE $(date '+%F %T')" | tee -a "$LOG"
