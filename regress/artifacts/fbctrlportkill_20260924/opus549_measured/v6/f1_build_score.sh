#!/bin/bash
# Build each floor candidate in the clone, score with a frozen v6 probe (ABSOLUTE binary path); clone-local sentinel;
# restore verified by cmp against GXEMUL-SEC then rebuilt + md5-checked before clearing the sentinel.
set -u
CL=/tmp/gxo549v6
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
C=$SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/v6
FIXMD5=b5b99e6d1e5fd077c8cf782d8c6a6a2c
cd "$CL" || exit 2
cmp -s var/fix.c "$SEC/src/devices/dev_fbctrl.c" && echo "fix.c == SEC" || { echo "fix.c DIFFERS"; exit 3; }
[ -e .MUTANT ] && { echo "SENTINEL PRESENT -- refusing"; exit 3; }
FZ=$CL/probe/frozen_v6.py; cp "$SEC/regress/fbctrl_port_probe.py" "$FZ"
echo "frozen v6 md5 $(md5sum < "$FZ" | cut -c1-8)"
rm -rf var/v; python3 "$C/gen_v6floor.py" var/fix.c var/v || exit 4
T=$C/TABLE_v6floor.out; mkdir -p "$C/logs"
echo "# $(date +%T) v6 probe md5=$(md5sum < "$FZ" | cut -c1-8); ABSOLUTE binary path" > "$T"
python3 -u "$FZ" "$CL/bins/gx_fix" > "$C/logs/_sanity_fix.out" 2>&1
echo "SANITY fix: $(grep -E '^FBCTRLP_(RESULT|CONTROL)=' "$C/logs/_sanity_fix.out" | tr '\n' ' ')" | tee -a "$T"
echo "src/devices/dev_fbctrl.c: v6 floor candidates, started $(date +%T)" > .MUTANT
for n in "$@"; do
  cp "var/v/$n.c" src/devices/dev_fbctrl.c; rm -f src/devices/dev_fbctrl.o
  make -j4 > "var/make_$n.log" 2>&1; rc=$?
  if [ "$rc" != 0 ] || [ ! gxemul -nt src/devices/dev_fbctrl.c ] || [ ! src/devices/dev_fbctrl.o -nt src/devices/dev_fbctrl.c ]; then
    echo "$n BUILD-FAILED rc=$rc" | tee -a "$T"; tail -4 "var/make_$n.log"; continue; fi
  cp gxemul "$CL/bins/gx_$n"
  python3 -u "$FZ" "$CL/bins/gx_$n" > "$C/logs/$n.out" 2>&1
  red=$(grep -E '^  FAIL ' "$C/logs/$n.out" | sed -E 's/^  FAIL +//; s/ +got=.*//' | tr '\n' ';')
  printf '%-12s md5=%s %s %s | %s\n' "$n" "$(md5sum < "$CL/bins/gx_$n" | cut -c1-8)" \
    "$(grep -E '^FBCTRLP_RESULT=' "$C/logs/$n.out")" "$(grep -E '^FBCTRLP_CONTROL=' "$C/logs/$n.out")" "${red:0:320}" >> "$T"
done
cp "$SEC/src/devices/dev_fbctrl.c" src/devices/dev_fbctrl.c; rm -f src/devices/dev_fbctrl.o; make -j4 > var/make_restore.log 2>&1
m=$(md5sum < gxemul | cut -d' ' -f1)
if cmp -s src/devices/dev_fbctrl.c "$SEC/src/devices/dev_fbctrl.c" && [ gxemul -nt src/devices/dev_fbctrl.c ] && [ "$m" = "$FIXMD5" ]; then
  rm -f .MUTANT; echo "RESTORED md5 $m == fix; sentinel cleared" | tee -a "$T"; else echo "RESTORE NOT VERIFIED md5 $m -- sentinel LEFT" | tee -a "$T"; fi
cmp -s "$FZ" "$SEC/regress/fbctrl_port_probe.py" && echo "# probe unchanged during run" >> "$T"
echo "----- TABLE_v6floor.out"; cat "$T"
