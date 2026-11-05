#!/bin/bash
# wsl_check_test.sh -- proves pvr_variants_3.py `check` runs under WSL python3 (as table3_pvr.sh calls it); read-only
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/pvrrenderexit/r3_20261105
python3 $A/pvr_variants_3.py check $A/sizing/selftest_scores.txt $A/base91/probe_base91.out | tail -2
