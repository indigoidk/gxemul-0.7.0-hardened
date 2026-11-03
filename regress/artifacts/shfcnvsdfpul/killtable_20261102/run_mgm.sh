#!/bin/bash
set -u
W=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w576; K=$W/killtable_20261102; F=/tmp/gxfix576; M=/tmp/gxmut576
rm -rf "$M"; cp -a "$F" "$M"; echo "MUTANT: src/cpus/cpu_sh_instr.c M_gm (scratch clone, #576 table)" > "$M/.MUTANT"
python3 "$W/mutate576.py" M_gm "$M/src/cpus/cpu_sh_instr.c" >> "$K/KILLTABLE.log" 2>&1 || { echo "M_gm APPLY-FAILED" | tee -a "$K/KILLTABLE.log"; exit 1; }
( cd "$M" && rm -f src/cpus/cpu_sh*.o && make -j4 > make_M_gm.log 2>&1 ); rc=$?
if [ $rc != 0 ] || [ ! "$M/gxemul" -nt "$M/src/cpus/cpu_sh_instr.c" ]; then echo "M_gm BUILD-FAILED rc=$rc" | tee -a "$K/KILLTABLE.log"; exit 1; fi
bash "$W/run_probe_leg.sh" "$M/gxemul" M_gm | tail -1 | tee -a "$K/KILLTABLE.log"
rm -rf "$M"; echo "MGM_DONE $(date '+%T')" | tee -a "$K/KILLTABLE.log"
