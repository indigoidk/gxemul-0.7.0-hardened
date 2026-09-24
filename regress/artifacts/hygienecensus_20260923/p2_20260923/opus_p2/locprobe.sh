#!/bin/bash
ls -d /usr/share/i18n/locales/en_US /usr/share/i18n/charmaps/UTF-8* 2>&1 | head
command -v localedef
D=/tmp/opus_census0923/loc
rm -rf "$D"; mkdir -p "$D"
localedef -i en_US -f UTF-8 "$D/en_US.UTF-8" 2>&1 | tail -3; echo "localedef rc=$?"
ls "$D" 2>&1
for L in C en_US.UTF-8; do
  printf '%s (LOCPATH): ' "$L"; printf 'arm_flags_probe.py\narm_bdt_probe.py\narmb_probe.py\narm_zz.py\nArm_x.py\nluna_absentcpu_probe.py\narmc.py\narm_c.py\n' | LOCPATH=$D LC_ALL=$L sort 2>&1 | tr '\n' ' '; echo
done
