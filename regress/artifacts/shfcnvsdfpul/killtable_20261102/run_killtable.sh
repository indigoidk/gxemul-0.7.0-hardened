#!/bin/bash
# run_killtable.sh -- #576 table: waits for the base leg, then the FIXED leg, then eight mutants built in /tmp/gxmut576 (a copy of
# the fixed clone, re-created per mutant, carrying a .MUTANT sentinel; deleted at the end).  No project tree is touched.
set -u
W=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w576; K=$W/killtable_20261102; F=/tmp/gxfix576; M=/tmp/gxmut576
LOG=$K/KILLTABLE.log
echo "killtable start $(date '+%F %T')" | tee "$LOG"
while ! grep -q '^LEG_DONE base_head' "$K/base_head.raw" 2>/dev/null; do sleep 20; done
echo "base leg done; fixed leg next $(date '+%T')" | tee -a "$LOG"
bash "$W/run_probe_leg.sh" "$F/gxemul" fixed | tail -1 | tee -a "$LOG"
for mut in M_b M_c M_d M_f M_g M_h M_i M_z; do
    rm -rf "$M"; cp -a "$F" "$M"
    echo "MUTANT: src/cpus/cpu_sh_instr.c $mut (scratch clone, #576 table)" > "$M/.MUTANT"
    if ! python3 "$W/mutate576.py" "$mut" "$M/src/cpus/cpu_sh_instr.c" >> "$LOG" 2>&1; then echo "$mut APPLY-FAILED" | tee -a "$LOG"; continue; fi
    ( cd "$M" && rm -f src/cpus/cpu_sh*.o && make -j4 > "make_$mut.log" 2>&1 ); rc=$?
    if [ $rc != 0 ] || [ ! "$M/gxemul" -nt "$M/src/cpus/cpu_sh_instr.c" ]; then echo "$mut BUILD-FAILED rc=$rc" | tee -a "$LOG"; tail -3 "$M/make_$mut.log" >> "$LOG"; continue; fi
    bash "$W/run_probe_leg.sh" "$M/gxemul" "$mut" | tail -1 | tee -a "$LOG"
done
rm -rf "$M"
echo "KILLTABLE_DONE $(date '+%F %T')" | tee -a "$LOG"
