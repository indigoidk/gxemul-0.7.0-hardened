#!/bin/bash
# Independent re-verification in a FRESH clone: rebuild base + the 3 key mutants from scratch, score with a frozen v6
# probe (absolute path), re-run the exit witness.  Clone-local sentinel; restore verified by cmp against SEC + md5.
set -u
ROOT=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$ROOT/GXEMUL-SEC
C=$SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/v6
CL=/tmp/gxo549v6b
FIXMD5=b5b99e6d1e5fd077c8cf782d8c6a6a2c
T=$C/RECHECK_v6b.out
[ -e "$CL" ] && { echo "REFUSED: $CL exists"; exit 2; }
cp -a "$ROOT/build" "$CL" || exit 2
mkdir -p "$CL/bins" "$CL/probe" "$CL/var"
cmp -s "$CL/src/devices/dev_fbctrl.c" "$SEC/src/devices/dev_fbctrl.c" && echo "clone dev_fbctrl.c == SEC" || { echo DIFF; exit 3; }
FZ=$CL/probe/frozen_v6.py; cp "$SEC/regress/fbctrl_port_probe.py" "$FZ"
cmp -s "$FZ" "$SEC/regress/fbctrl_port_probe.py" && echo "frozen probe == SEC v6 ($(md5sum < "$FZ" | cut -c1-8))"
cp "$CL/src/devices/dev_fbctrl.c" "$CL/var/fix.c"
PRED='else if (idata >= DEV_FBCTRL_NPORTS) {'
mkstate() { python3 - "$1" "$2" "$3" <<PY
import io,sys
f,out,new=sys.argv[1],sys.argv[2],sys.argv[3]
s=io.open(f,encoding="utf-8",newline="").read()
assert s.count("$PRED")==1
io.open(out,"w",encoding="utf-8",newline="").write(s.replace("$PRED", new))
PY
}
mkstate "$CL/var/fix.c" "$CL/var/LB_unset16.c" 'else if (idata >= DEV_FBCTRL_NPORTS && !(idata == 0x10 && !d->warned_port)) {'
mkstate "$CL/var/fix.c" "$CL/var/MB_pc4.c"     'else if (idata >= DEV_FBCTRL_NPORTS && __builtin_popcountll(idata) != 4) {'
mkstate "$CL/var/fix.c" "$CL/var/MB_v18.c"     'else if (idata >= DEV_FBCTRL_NPORTS && idata != 0x18) {'
cd "$CL" || exit 2
rm -f src/cpus/*.o; make -j4 > var/make_base.log 2>&1
[ gxemul -nt src/devices/dev_fbctrl.c ] && echo "base FRESH" || echo "base STALE"
cp gxemul bins/gx_fix
echo "# fresh-clone re-verification $(date +%T)" > "$T"
echo "base md5 $(md5sum < gxemul | cut -c1-8) (== fix $FIXMD5?)" | tee -a "$T"
echo "SANITY fix: $(python3 -u "$FZ" "$CL/bins/gx_fix" | grep -E '^FBCTRLP_(RESULT|CONTROL)=' | tr '\n' ' ')" | tee -a "$T"
echo "src/devices/dev_fbctrl.c: v6 recheck" > .MUTANT
for n in LB_unset16 MB_pc4 MB_v18; do
  cp "var/$n.c" src/devices/dev_fbctrl.c; rm -f src/devices/dev_fbctrl.o; make -j4 > "var/make_$n.log" 2>&1
  [ gxemul -nt src/devices/dev_fbctrl.c ] || { echo "$n STALE BUILD" | tee -a "$T"; continue; }
  cp gxemul "bins/gx_$n"
  python3 -u "$FZ" "bins/gx_$n" > "$C/logs/recheck_$n.out" 2>&1
  echo "$n md5=$(md5sum < bins/gx_$n | cut -c1-8) $(grep -E '^FBCTRLP_RESULT=' "$C/logs/recheck_$n.out") $(grep -E '^FBCTRLP_CONTROL=' "$C/logs/recheck_$n.out")" | tee -a "$T"
done
# witness: fresh device, first PORT write = 16, then DATA read
cp "$C/unset_witness.py" "$CL/probe/uw.py"
echo "-- exit witness (first PORT write 16/32/64, then DATA read):" | tee -a "$T"
for b in fix LB_unset16; do echo "== $b" | tee -a "$T"; ( cd "$CL/probe" && python3 -u uw.py "$CL/bins/gx_$b" "$FZ" 2>&1 | grep -E '^U ' ) | tee -a "$T"; done
# restore
cp "$SEC/src/devices/dev_fbctrl.c" src/devices/dev_fbctrl.c; rm -f src/devices/dev_fbctrl.o; make -j4 > var/make_restore.log 2>&1
m=$(md5sum < gxemul | cut -d' ' -f1)
if cmp -s src/devices/dev_fbctrl.c "$SEC/src/devices/dev_fbctrl.c" && [ gxemul -nt src/devices/dev_fbctrl.c ] && [ "$m" = "$FIXMD5" ]; then rm -f .MUTANT; echo "RESTORED md5 $m == fix; sentinel cleared" | tee -a "$T"; else echo "RESTORE NOT VERIFIED md5 $m" | tee -a "$T"; fi
rm -f /tmp/gx_fbctrl549p_*.bin
echo "--- cleanup clone:"; rm -rf "$CL" && echo "clone removed"
echo "===== RECHECK_v6b.out"; cat "$T"
