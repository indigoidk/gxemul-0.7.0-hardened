#!/bin/bash
#  opus5 follow-up: is the guard's "must be an integer constant" property
#  optimisation-dependent for a const-qualified object argument?
set -u
M=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fableq/opus5_meas
INC=-I/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/include
cd "$M" || exit 1
for c in 2 3; do
	for o in -O0 -O1 -O2 -O3; do
		cc $o -Wall -Wextra $INC -DCASE=$c -c t_rt.c -o out/rtq.o 2> out/rtq.err
		r1=$?
		cc $o -Wall -Wextra -Wpedantic $INC -DCASE=$c -c t_rt.c -o out/rtp.o 2> out/rtp.err
		r2=$?
		printf 'CASE %s %s : plain rc=%s | -Wpedantic rc=%s %s\n' "$c" "$o" "$r1" "$r2" \
		    "$(grep -m1 -E 'error|warning' out/rtp.err | sed 's#^.*/##' | cut -c1-120)"
	done
done
echo RUN2_DONE
