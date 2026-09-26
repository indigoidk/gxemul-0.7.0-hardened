#!/bin/bash
set -u
CL=/tmp/gxo549c3
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
C=$SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/c3
FIXMD5=b5b99e6d1e5fd077c8cf782d8c6a6a2c
cd "$CL" || exit 2
cmp -s var/fix.c "$SEC/src/devices/dev_fbctrl.c" && echo "fix.c == SEC" || { echo "fix.c DIFFERS"; exit 3; }
[ -e .MUTANT ] && { echo "SENTINEL PRESENT -- refusing"; exit 3; }
FZ=$CL/probe/frozen_v5m.py; cp "$SEC/regress/fbctrl_port_probe.py" "$FZ"
echo "frozen v5 md5 $(md5sum < "$FZ" | cut -c1-8)"
rm -rf var/m; python3 "$C/gen_mask.py" var/fix.c var/m || exit 4
T=$C/TABLE_mask.out; echo "# $(date +%T) v5 md5=$(md5sum < "$FZ" | cut -c1-8); ABSOLUTE binary path" > "$T"
python3 -u "$FZ" "$CL/bins/gx_fix" > "$C/logs/_sanity_fix_mask.out" 2>&1
echo "SANITY fix: $(grep -E '^FBCTRLP_(RESULT|CONTROL)=' "$C/logs/_sanity_fix_mask.out" | tr '\n' ' ')" | tee -a "$T"
echo "src/devices/dev_fbctrl.c: compare-narrowing mutants, started $(date +%T)" > .MUTANT
for n in MK_b9_31 MK_b5_7 MK_b34_62 MK_b8_ctl; do
  cp "var/m/$n.c" src/devices/dev_fbctrl.c; rm -f src/devices/dev_fbctrl.o
  make -j4 > "var/make_$n.log" 2>&1; rc=$?
  if [ "$rc" != 0 ] || [ ! gxemul -nt src/devices/dev_fbctrl.c ]; then echo "$n BUILD-FAILED rc=$rc" | tee -a "$T"; continue; fi
  cp gxemul "$CL/bins/gx_$n"
  python3 -u "$FZ" "$CL/bins/gx_$n" > "$C/logs/$n.out" 2>&1
  red=$(grep -E '^  FAIL ' "$C/logs/$n.out" | sed -E 's/^  FAIL +//; s/ +got=.*//' | tr '\n' ';')
  printf '%-10s md5=%s %s %s | %s\n' "$n" "$(md5sum < "$CL/bins/gx_$n" | cut -c1-8)" "$(grep -E '^FBCTRLP_RESULT=' "$C/logs/$n.out")" "$(grep -E '^FBCTRLP_CONTROL=' "$C/logs/$n.out")" "$red" >> "$T"
done
cp "$SEC/src/devices/dev_fbctrl.c" src/devices/dev_fbctrl.c; rm -f src/devices/dev_fbctrl.o; make -j4 > var/make_restore_m.log 2>&1
m=$(md5sum < gxemul | cut -d' ' -f1)
if cmp -s src/devices/dev_fbctrl.c "$SEC/src/devices/dev_fbctrl.c" && [ gxemul -nt src/devices/dev_fbctrl.c ] && [ "$m" = "$FIXMD5" ]; then rm -f .MUTANT; echo "RESTORED md5 $m == fix; sentinel cleared" | tee -a "$T"; else echo "RESTORE NOT VERIFIED md5 $m -- sentinel LEFT" | tee -a "$T"; fi
echo "--- kill witness (0x200 to PORT, then one DATA read):" | tee -a "$T"
cp "$C/mask_witness.py" "$CL/probe/mw.frozen.py"
for b in fix MK_b9_31; do echo "== $b: $(cd "$CL/probe" && python3 -u mw.frozen.py "$CL/bins/gx_$b" "$FZ" 2>&1 | grep -E '^MW ')" | tee -a "$T"; done
rm -f /tmp/gx_fbctrl549p_*.bin
cmp -s "$FZ" "$SEC/regress/fbctrl_port_probe.py" && echo "# probe unchanged during run" >> "$T"
echo "----- TABLE_mask.out"; cat "$T"
