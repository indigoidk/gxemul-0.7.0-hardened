#!/bin/bash
echo "LANG=[${LANG-unset}] LC_ALL=[${LC_ALL-unset}] LC_COLLATE=[${LC_COLLATE-unset}]"
locale 2>&1 | head -20
echo "--- locale -a"
locale -a 2>&1 | head -30
echo "--- tools"
command -v python3 git sort comm xargs find grep awk sed
sort --version | head -1; grep --version | head -1; xargs --version | head -1; bash --version | head -1
echo "--- sort test of the two names and a few underscore/case pairs, per locale"
for L in C C.UTF-8 C.utf8 en_US.UTF-8 en_US.utf8 POSIX; do
  printf '%s: ' "$L"; printf 'arm_flags_probe.py\narm_bdt_probe.py\narmb_probe.py\narm_zz.py\nArm_x.py\nluna_absentcpu_probe.py\n' | LC_ALL=$L sort 2>&1 | tr '\n' ' '; echo
done
