#!/bin/bash
# dryrun_r15p2.sh -- apply every mutants_r15p2.py leg to a throwaway copy (never the clone) and show the diffs.
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_r15p2_20260926
S=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_ip32.c
D=/tmp/r15p2_dry
mkdir -p "$D"
for m in $(python3 "$A/mutants_r15p2.py" list x y); do
    python3 "$A/mutants_r15p2.py" "$m" "$S" "$D/$m.c" > /dev/null || echo "FAIL $m"
    echo "== $m $(diff "$S" "$D/$m.c" | grep -c '^[<>]') changed lines"
done
for m in P_ist1r_set C_istW_clr census; do
    echo "######## $m"
    diff -u "$S" "$D/$m.c"
done
