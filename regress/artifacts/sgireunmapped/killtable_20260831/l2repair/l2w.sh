#!/bin/bash
set -u
C=/tmp/gxl2; SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
cp $SEC/src/devices/dev_sgi_re.c $C/src/devices/dev_sgi_re.c
echo "$C/.MUTANT: W" > $C/.MUTANT
python3 /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/mkw.py || exit 1
cd $C; rm -f src/devices/dev_sgi_re.o
make -j4 > /tmp/l2_build_W2.log 2>&1
echo "  MAKE_RC=$?"
[ -f gxemul ] || { echo "  NO BINARY"; exit 1; }
[ gxemul -nt src/devices/dev_sgi_re.c ] && echo "  build: FRESH" || { echo "  STALE -- ABORT"; grep -iE 'error' /tmp/l2_build_W2.log | head -3; exit 1; }
cd $SEC/regress
timeout 300 python3 -u sgi_re_unmapped_probe.py $C/gxemul W > /tmp/l2_W.out 2>&1
echo "  probe rc=$?  sentinels=$(grep -c OPUS499T_DONE /tmp/l2_W.out)  $(grep -oE 'OPUS499T_RESULT=[0-9]+/[0-9]+' /tmp/l2_W.out | head -1)"
grep ' FAIL$' /tmp/l2_W.out | awk '{printf "    RED: %s %s\n", $1, $2}'
echo "  --- does W actually restore the witness? ---"
cd /mnt/c/DocumentNoSnc/cc/GXEMUL
printf 'put b 0xffffffffb5001800, 0x5a\nquit\n' | timeout 60 $C/gxemul -V -E sgi -e ip32 -M 64 0x80001000:/tmp/d500.bin 2>&1 | grep -icE 'len = 1 not implemented' | sed 's/^/    pre-fix kill text on a byte write: /'
cp $SEC/src/devices/dev_sgi_re.c $C/src/devices/dev_sgi_re.c
cmp -s $C/src/devices/dev_sgi_re.c $SEC/src/devices/dev_sgi_re.c && echo "  restore cmp: CLEAN" || echo "  DIRTY"
rm -f $C/.MUTANT
echo L2W_DONE
