#!/bin/bash
#  restore566.sh -- return the scratch clone /tmp/gx566 to HEAD (dev_sgi_ip30.c from HEAD), rebuild, verify both parts
#  of the clearance against HEAD copies, and only then clear the clone's .MUTANT sentinel.
set -u
W=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/w566
C=/tmp/gx566
cp "$W/head_dev_sgi_ip30.c" "$C/src/devices/dev_sgi_ip30.c" || exit 9
(cd "$C" && rm -f src/cpus/*.o src/devices/dev_sgi_ip30.o && make -j4 > "$W/restore566_build.log" 2>&1); echo "make rc=$?"
ok=1
cmp -s "$W/head_dev_sgi_ip30.c" "$C/src/devices/dev_sgi_ip30.c" && echo "part 1: dev_sgi_ip30.c == HEAD" || { echo "part 1 FAILED: dev_sgi_ip30.c"; ok=0; }
for f in src/cpus/cpu_alpha_palcode.c src/devices/dev_lca.c src/devices/dev_pcc2.c src/devices/dev_sh4.c src/include/thirdparty/mvme_pcctworeg.h; do
    cmp -s "$W/headsrc/$f" "$C/$f" && echo "part 1: $f == HEAD" || { echo "part 1 FAILED: $f"; ok=0; }
done
for f in src/devices/dev_sgi_ip30.c src/devices/dev_lca.c src/devices/dev_pcc2.c src/devices/dev_sh4.c src/cpus/cpu_alpha_palcode.c src/include/thirdparty/mvme_pcctworeg.h; do
    [ "$C/gxemul" -nt "$C/$f" ] || { echo "part 2 FAILED: binary not newer than $f"; ok=0; }
done
[ "$ok" = 1 ] && { echo "part 2: binary newer than every restored source ($(date -r $C/gxemul '+%T'))"; rm -f "$C/.MUTANT"; echo "sentinel cleared"; } || echo "SENTINEL KEPT"
md5sum "$C/gxemul" | cut -c1-32 | sed 's/^/gxemul md5 /'
echo RESTORE566_DONE
