#!/bin/bash
#  Settle the CONTRACT claim against the detector that MAKES it: the 58-row probe.
#  Both trees carry the same R2 candidate fix, so the only delta is M11 itself.
R=/mnt/c/DocumentNoSnc/cc/GXEMUL
K=$R/_images/openbsd76-landisk-bsd.rd
P=$R/GXEMUL-SEC/regress/gdrom_default_probe.py
for tree in fixed M11; do
  echo "===== $tree ====="
  python3 -u "$P" /tmp/gxopus_r2/$tree/gxemul "$K" 2>&1 \
    | grep -E "GDROM_DEF_RESULT|GDROM_DEF_CONTROL|^(stale idle|stale says|nodata stale)|FAIL$"
done
echo M11_58ROW_DONE
