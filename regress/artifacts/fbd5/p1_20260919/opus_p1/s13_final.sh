#!/bin/bash
cd /tmp/gxopusfbd5 || exit 9
echo "--- final clone state ---"
md5sum gxemul out/gxemul_HEAD
ls -la .MUTANT 2>/dev/null || echo ".MUTANT: absent"
stat -c '%y  %n' gxemul src/devices/dev_footbridge.c
echo "logs kept in clone: $(ls out/table | wc -l) files, $(du -sh out/table | cut -f1)"
echo "S13_DONE"
