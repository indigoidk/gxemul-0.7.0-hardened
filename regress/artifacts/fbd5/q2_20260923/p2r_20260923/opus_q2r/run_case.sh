#!/bin/bash
cd /tmp/opusq2r || exit 9
RESULTS_NAME=/results_case.tsv python3 -u /mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2r/opus/driver.py case 2>&1
ls -la /tmp/opusq2r/.MUTANT 2>&1
md5sum /tmp/opusq2r/src/devices/dev_footbridge.c
