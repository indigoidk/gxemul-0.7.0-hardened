#!/usr/bin/env bash
#  NB the previous check's "2 alive" was the pattern matching its own wrapper's
#  PATH (.../scratchpad/opus524/cleanup.sh) -- the bracket trick does not help
#  when the literal is in the script's own filename.  Match the real artifacts.
echo "gxemul processes:        $(pgrep -c -x gxemul || true)"
echo "make processes:          $(pgrep -c -x make || true)"
echo "arm_bdt_probe processes: $(pgrep -f -c 'arm_bdt_probe' || true)"
ps -eo pid,args | grep -E 'gxopus524|table_opus|control_run' | grep -v grep | head -5
echo "SCRATCH_CLEAN"
