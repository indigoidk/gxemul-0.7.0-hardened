#!/bin/bash
# clone_rm_3f.sh -- removes the RESTORED head128 clone /tmp/gxpvr3f (only if it has no .MUTANT and its dev_pvr.c cmp's clean vs SEC)
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c
d=/tmp/gxpvr3f
if [ -e "$d" ] && [ ! -e "$d/.MUTANT" ] && cmp -s "$d/src/devices/dev_pvr.c" "$SEC"; then rm -rf "$d" && echo "$d removed (restored, clean)"; else echo "$d absent or KEPT"; fi
