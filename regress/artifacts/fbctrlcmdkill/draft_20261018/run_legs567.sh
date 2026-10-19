#!/bin/bash
#  run_legs567.sh -- #567's draft detector on two builds, one instrument: PRE-FIX = /tmp/gx566's HEAD binary (both
#  clearance parts checked); POST-FIX = /tmp/gx567, a cp -a of /tmp/gx566 with the draft dev_fbctrl.c, rebuilt.  The
#  probe is frozen (copied) before either leg.  build/ is not touched.
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbcmd
F=src/devices/dev_fbctrl.c
echo "LEGS start $(date '+%F %T')"
cp "$S/fbctrl_cmd_probe.py" "$S/probe.frozen.py"; echo "probe md5 $(md5sum < "$S/probe.frozen.py" | cut -c1-32)"
[ -e /tmp/gx566/.MUTANT ] && { echo "gx566 carries a sentinel -- stop"; exit 9; }
cmp -s "$S/head_dev_fbctrl.c" /tmp/gx566/$F && [ /tmp/gx566/gxemul -nt /tmp/gx566/$F ] || { echo "gx566 not HEAD-clean -- stop"; exit 9; }
echo "PRE-FIX binary md5 $(md5sum < /tmp/gx566/gxemul | cut -c1-32)"
python3 -u "$S/probe.frozen.py" /tmp/gx566/gxemul > "$S/PROBE_prefix.out" 2>&1; echo "prefix rc=$? $(grep '^FBCMD_RESULT' "$S/PROBE_prefix.out") $(grep '^FBCMD_CONTROL' "$S/PROBE_prefix.out") last=$(tail -1 "$S/PROBE_prefix.out")"
if [ ! -d /tmp/gx567 ]; then cp -a /tmp/gx566 /tmp/gx567; echo "cloned /tmp/gx567"; fi
cp "$S/dev_fbctrl.fix567.c" /tmp/gx567/$F
(cd /tmp/gx567 && rm -f src/cpus/*.o src/devices/dev_fbctrl.o && make -j4 > "$S/build_fix567.log" 2>&1); echo "make rc=$?"
[ /tmp/gx567/gxemul -nt /tmp/gx567/$F ] || { echo "POST-FIX BINARY NOT FRESH -- stop"; exit 9; }
cmp -s "$S/dev_fbctrl.fix567.c" /tmp/gx567/$F && echo "post-fix source == the draft"
echo "POST-FIX binary md5 $(md5sum < /tmp/gx567/gxemul | cut -c1-32)"
python3 -u "$S/probe.frozen.py" /tmp/gx567/gxemul > "$S/PROBE_postfix.out" 2>&1; echo "postfix rc=$? $(grep '^FBCMD_RESULT' "$S/PROBE_postfix.out") $(grep '^FBCMD_CONTROL' "$S/PROBE_postfix.out") last=$(tail -1 "$S/PROBE_postfix.out")"
python3 -u "$S/fbctrl_cmd_witness.py" /tmp/gx567/gxemul > "$S/WITNESS_postfix.out" 2>&1; echo "witness postfix rc=$? $(grep '^FBCMDW_RESULT' "$S/WITNESS_postfix.out")"
echo "LEGS end $(date '+%F %T')"
echo LEGS_DONE
