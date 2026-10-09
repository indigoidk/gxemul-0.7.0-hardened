#!/bin/bash
# fable5 7n-2 check: clause (c) null-medium leg for the shortread differential (#488),
# compile-only, in a SCRATCH COPY.  Reads GXEMUL-SEC; writes only under the scratchpad.
# CONTROL first (real diskimage.c must compile) so a null-medium failure is for the reason under test.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fableq/nullshortread
rm -rf "$S"
mkdir -p "$S/regress" "$S/src/disk" "$S/src/include"
cp "$SEC/regress/diff_diskimage_io.c" "$S/regress/"
cp -r "$SEC/src/include/." "$S/src/include/"
cp "$SEC/src/disk/diskimage.c" "$SEC/src/disk/diskimage_scsicmd.c" "$S/src/disk/"
cp "$SEC/config.h" "$S/config.h"   # cpu.h:41 includes ../../config.h from the tree root (the gate's -I resolves it to $SEC/config.h)
cd "$S/regress" || exit 9
F="-O2 -std=gnu99 -I../src/include -I../src/include/thirdparty -ffunction-sections -fdata-sections -Wl,--gc-sections"
echo "gcc: $(gcc --version | head -1)"
gcc $F -o "$S/ctl_bin" diff_diskimage_io.c > "$S/ctl.log" 2>&1
rc=$?
echo "CONTROL (real diskimage.c + diskimage_scsicmd.c): rc=$rc  log lines=$(wc -l < "$S/ctl.log")"
head -3 "$S/ctl.log"
printf '/* NULL MEDIUM: comment-only diskimage.c -- clause-(c) leg, fable5 7n-2 check, SCRATCH COPY ONLY */\n' > ../src/disk/diskimage.c
printf '/* NULL MEDIUM: comment-only diskimage_scsicmd.c -- scratch copy only */\n' > ../src/disk/diskimage_scsicmd.c
gcc $F -o "$S/null_bin" diff_diskimage_io.c > "$S/null.log" 2>&1
rc2=$?
echo "NULL MEDIUM (comment-only product files): rc=$rc2  log lines=$(wc -l < "$S/null.log")  lines naming a diskimage_* symbol=$(grep -c -E 'diskimage_[a-z_]+' "$S/null.log")"
grep -E 'error|undefined reference' "$S/null.log" | head -5
echo "binaries present:"; ls -la "$S"/ctl_bin "$S"/null_bin 2>&1 | sed "s#$S#SCRATCH#"
echo "NULLSHORTREAD_CHECK_DONE"
