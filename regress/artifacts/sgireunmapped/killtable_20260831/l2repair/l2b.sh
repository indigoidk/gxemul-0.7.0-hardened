#!/bin/bash
set -u
C=/tmp/gxl2; SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
cp $SEC/src/devices/dev_sgi_re.c $C/src/devices/dev_sgi_re.c
echo "$C/.MUTANT: 36-row verification" > $C/.MUTANT
score () {
  cd $SEC/regress
  timeout 300 python3 -u sgi_re_unmapped_probe.py $C/gxemul "$1" > /tmp/l2b_$1.out 2>&1
  echo "  $1: rc=$? sentinels=$(grep -c OPUS499T_DONE /tmp/l2b_$1.out) $(grep -oE 'OPUS499T_RESULT=[0-9]+/[0-9]+' /tmp/l2b_$1.out | head -1)"
  grep ' FAIL$' /tmp/l2b_$1.out | awk '{printf "      RED: %s %s %s\n", $1, $2, $3}'
}
build () {
  cd $C; rm -f src/devices/dev_sgi_re.o
  make -j4 > /tmp/l2b_build_$1.log 2>&1
  [ -f gxemul ] || { echo "  $1: NO BINARY"; return 1; }
  [ gxemul -nt src/devices/dev_sgi_re.c ] || { echo "  $1: STALE -- ABORT"; grep -iE '\berror\b' /tmp/l2b_build_$1.log | head -3; return 1; }
  return 0
}
echo "=== fix (36 rows expected, all green) ==="
build fix && score fix
echo "=== T: TEX far bound grown ==="
sed -i 's/relative_addr < CRIME_RE_TEX + 0xe0/relative_addr < CRIME_RE_TEX + 0x100/' $C/src/devices/dev_sgi_re.c
build T && score T
cp $SEC/src/devices/dev_sgi_re.c $C/src/devices/dev_sgi_re.c
echo "=== W: pre-#499 len guard re-added ==="
python3 /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/mkw.py >/dev/null && build W && score W
cp $SEC/src/devices/dev_sgi_re.c $C/src/devices/dev_sgi_re.c
cmp -s $C/src/devices/dev_sgi_re.c $SEC/src/devices/dev_sgi_re.c && echo "  restore: CLEAN" || echo "  DIRTY"
rm -f $C/.MUTANT
echo L2B_DONE
