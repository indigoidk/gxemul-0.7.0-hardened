#!/bin/bash
#  dryrun.sh -- apply every mutant into /tmp/c8dry and show the diff hunk count for each.  No tree is touched.
set -u
A=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close8_20260916
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_ip32.c
rm -rf /tmp/c8dry; mkdir -p /tmp/c8dry
for m in base L_dfl4w_hi L_dfl4w_lo L_dfl4r_hi L_dfl4r_lo W_rev8r_out W_rev8w_out W_rev4w_out W_rev4r_out G_lane_ist G_lane_tim G_lane_all D1_landpost D2_remappost; do
    if python3 "$A/scripts/mutants8.py" "$m" "$S" "/tmp/c8dry/$m.c"; then
        n=$(diff -u "$S" "/tmp/c8dry/$m.c" | grep -c '^[+-][^+-]')
        echo "    changed lines: $n"
    else
        echo "FAILED $m"
    fi
done
echo "=== compile-check each (syntax only, no link) ==="
cd /tmp/gxopusc8 || exit 1
for m in L_dfl4w_hi L_dfl4w_lo L_dfl4r_hi L_dfl4r_lo W_rev8r_out W_rev8w_out W_rev4w_out W_rev4r_out G_lane_ist G_lane_tim G_lane_all D1_landpost D2_remappost; do
    cp "/tmp/c8dry/$m.c" /tmp/c8dry/try.c
    if gcc -fsyntax-only -Isrc/include -I. /tmp/c8dry/try.c 2>/tmp/c8dry/$m.err; then echo "SYNTAX_OK $m"; else echo "SYNTAX_FAIL $m"; head -5 /tmp/c8dry/$m.err; fi
done
echo DRYRUN_DONE
