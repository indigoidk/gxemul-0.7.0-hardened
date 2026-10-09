#!/bin/bash
#  opus5 follow-up: under build-asan's OWN flags (-O3 -fsanitize=address,undefined),
#  does UBSan still report the in-domain 1 << 31 when the argument is a CONSTANT
#  (the only form SYSASIC_TRIGGER_EVENT can take), or does -O3 fold it away first?
set -u
M=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fableq/opus5_meas
INC=-I/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/include
ASANF="-Wshadow -Wcast-align -Wstrict-aliasing -Wall -Wextra -Wno-unused-parameter -Wno-cast-align -fstrict-aliasing -fomit-frame-pointer -fpeephole -fgnu89-inline -O3 -DNDEBUG -fsanitize=address,undefined -fno-omit-frame-pointer -g"
cd "$M" || exit 1
cc $ASANF $INC t_shift.c -o out/t_shift_asanflags 2> out/t_shift_asanflags.err
echo "compile rc=$?"
ASAN_OPTIONS=detect_leaks=0 ./out/t_shift_asanflags > out/asanflags.out 2> out/asanflags.err
echo "run rc=$?"
echo "runtime-error lines: $(grep -c 'runtime error' out/asanflags.err)"
grep 'runtime error' out/asanflags.err | sed -e 's#^.*t_shift.c#t_shift.c#' | sort | uniq -c
echo RUN3_DONE
