#!/bin/bash
set -u
A=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close8_20260916
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_ip32.c
rm -rf /tmp/c8dry3; mkdir -p /tmp/c8dry3
for m in C_ctl4r G_lane_ctl G_glm_tim4clear G_clr_ist4r G_clr_ctl4r G_clr_imk4r K_ctl4w_reset_post K_ctl8w_reset_post; do
    python3 "$A/scripts/mutants8b.py" "$m" "$S" "/tmp/c8dry3/$m.c" || echo "FAILED $m"
done
echo "--- K_ctl4w_reset_post ---"; diff -u "$S" /tmp/c8dry3/K_ctl4w_reset_post.c | sed -n '3,14p'
echo "--- G_clr_ist4r ---"; diff -u "$S" /tmp/c8dry3/G_clr_ist4r.c | sed -n '3,14p'
echo "--- syntax ---"
cd /tmp/gxopusc8 || exit 1
for m in C_ctl4r G_lane_ctl G_glm_tim4clear G_clr_ist4r G_clr_ctl4r G_clr_imk4r K_ctl4w_reset_post K_ctl8w_reset_post; do
    cp /tmp/c8dry3/$m.c /tmp/c8dry3/try.c
    if gcc -fsyntax-only -Isrc/include -I. /tmp/c8dry3/try.c 2>/tmp/c8dry3/$m.err; then echo "SYNTAX_OK $m"; else echo "SYNTAX_FAIL $m"; head -5 /tmp/c8dry3/$m.err; fi
done
echo "--- syntax-check the two new probes ---"
python3 -c "import ast,sys; [ast.parse(open(p).read(), p) for p in sys.argv[1:]]; print('PROBES PARSE OK')" "$A/scripts/t4clear.py" "$A/scripts/ctlreset.py" "$A/scripts/ctl4r.py"
echo DRYRUN3_DONE
