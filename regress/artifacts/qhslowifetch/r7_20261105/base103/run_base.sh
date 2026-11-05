#!/bin/bash
# run_base.sh -- qhslowifetch repair 7: the 103-row probe (a copy, probe103_run.py) on build/gxemul, after CLEARANCE.txt.
B=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/qhslowifetch/r7_20261105/base103
python3 -u $B/probe103_run.py /mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul base103 $B/sessions > $B/probe_base103.out 2>&1
echo "probe rc=$?"
tail -n 6 $B/probe_base103.out
