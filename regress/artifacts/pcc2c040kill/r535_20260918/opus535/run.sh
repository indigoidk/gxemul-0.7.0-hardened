#!/bin/bash
SPW=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus535
CL=/tmp/gxopus535
rm -rf "$CL"; cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$CL" || exit 9
echo "sentinel: dev_pcc2.c mutants (opus535)" > "$CL/.MUTANT"
cd "$CL"; rm -f src/cpus/*.o
for M in BASE A_latch_bypass_mien C_fatal_to_debug D_latch_bit_masklen E_announce_pending_gate F_latchset_mienclear BASE; do
  echo "===== $M"
  python3 "$SPW/mutate.py" "$M" || exit 9
  diff "$SPW/pcc2_HEAD.c" src/devices/dev_pcc2.c
  rm -f src/devices/dev_pcc2.o
  make -j4 > "$SPW/build_$M.log" 2>&1; echo "MAKE_RC=$?"
  if [ gxemul -nt src/devices/dev_pcc2.c ]; then echo FRESH=OK; else echo FRESH=STALE; exit 9; fi
  python3 -u "$SPW/probe.frozen.py" "$CL/gxemul" "$M" > "$SPW/$M.raw" 2>&1
  echo "SAYS-count in raw: $(grep -c 'C040 (MC68040 EIPL)' "$SPW/$M.raw")"
  grep -E "RESULT|DONE" "$SPW/$M.raw"; grep " FAIL$" "$SPW/$M.raw"
  case $M in BASE|A_*|F_*) python3 -u "$SPW/probe.diag.py" "$CL/gxemul" "$M" > "$SPW/diag_$M.raw" 2>&1; grep -E "DIAG|RESULT" "$SPW/diag_$M.raw";; esac
done
cmp src/devices/dev_pcc2.c "$SPW/pcc2_HEAD.c" && [ gxemul -nt src/devices/dev_pcc2.c ] && rm -f .MUTANT && echo CLEARED
