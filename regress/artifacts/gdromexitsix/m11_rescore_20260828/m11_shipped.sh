#!/bin/bash
#  Settle the contract's M11 kill claim against the SHIPPED 19-row detector, not a replica.
R=/mnt/c/DocumentNoSnc/cc/GXEMUL
K=$R/_images/openbsd76-landisk-bsd.rd
P=$R/GXEMUL-SEC/regress/gdrom_toclen_probe.py
echo "=== fixed (reference) ==="
python3 -u "$P" /tmp/gxopus_r2/fixed/gxemul "$K" 2>&1 | grep -E "TOCLEN_RESULT|TOCLEN_CONTROL|FAIL$"
echo "=== M11 (DMA-arm operand swap) ==="
python3 -u "$P" /tmp/gxopus_r2/M11/gxemul "$K" 2>&1 | grep -E "TOCLEN_RESULT|TOCLEN_CONTROL|FAIL$"
echo M11_SHIPPED_DONE
