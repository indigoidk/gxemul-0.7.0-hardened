#!/bin/bash
R=/mnt/c/DocumentNoSnc/cc/GXEMUL
P=$R/GXEMUL-SEC/regress/gdrom_default_probe.py
echo "=== post-fix, correct packet (the accept control) ==="
python3 -u "$P" $R/build/gxemul $R/_images/openbsd76-landisk-bsd.rd 2>&1 \
  | grep -E "GDROM_DEF_RESULT|GDROM_DEF_CONTROL|^(nodata stale|stale says|stale idle)"
echo R2_POSTFIX_DONE
