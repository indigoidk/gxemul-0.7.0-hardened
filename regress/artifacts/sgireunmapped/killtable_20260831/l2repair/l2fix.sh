#!/bin/bash
#  L2 repair verification.  The 34-row detector must be GREEN on the fix and RED on
#  both mutants that swept the 28-row version clean.
set -u
C=/tmp/gxl2
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
rm -rf $C; cp -a /tmp/gxsec-build $C
echo "L2FIX: clone made"
cmp -s $C/src/devices/dev_sgi_re.c $SEC/src/devices/dev_sgi_re.c && echo "  baseline cmp vs SEC: CLEAN" || { echo "  BASELINE DIFFERS -- ABORT"; exit 1; }
echo "$C/.MUTANT: dev_sgi_re.c L2 repair verification" > $C/.MUTANT

run () {   # $1 = label
  cd $C
  rm -f src/devices/dev_sgi_re.o
  make -j4 > /tmp/l2_build_$1.log 2>&1
  [ -f gxemul ] || { echo "  $1: NO BINARY"; return; }
  [ gxemul -nt src/devices/dev_sgi_re.c ] || { echo "  $1: STALE BINARY -- ABORT"; return; }
  cd $SEC/regress
  timeout 300 python3 -u sgi_re_unmapped_probe.py $C/gxemul "$1" > /tmp/l2_$1.out 2>&1
  RC=$?
  S=$(grep -c OPUS499T_DONE /tmp/l2_$1.out)
  R=$(grep -oE 'OPUS499T_RESULT=[0-9]+/[0-9]+' /tmp/l2_$1.out | head -1)
  echo "  $1: rc=$RC sentinels=$S  $R"
  grep ' FAIL$' /tmp/l2_$1.out | awk '{printf "      RED: %s %s\n", $1, $2}'
}

echo "=== 1. the FIX (unmodified) -- must be all green ==="
run fix

echo "=== 2. mutant T: CRIME_RE_TEX + 0xe0 -> + 0x100 ==="
sed -i 's/relative_addr < CRIME_RE_TEX + 0xe0/relative_addr < CRIME_RE_TEX + 0x100/' $C/src/devices/dev_sgi_re.c
grep -c 'CRIME_RE_TEX + 0x100' $C/src/devices/dev_sgi_re.c | sed 's/^/      edit applied: /'
run T
cp $SEC/src/devices/dev_sgi_re.c $C/src/devices/dev_sgi_re.c

echo "=== 3. mutant W: re-add a len != 8 kill at the top of the catch-all ==="
python3 - <<'PY'
import io
p = "/tmp/gxl2/src/devices/dev_sgi_re.c"
s = io.open(p, encoding="utf-8").read()
A = "\t} else {\n\t\tif (writeflag == MEM_WRITE) {\n\t\t\tif (!(d->warned & SGIRE_W_UNMAP_WR)) {"
assert s.count(A) == 1, s.count(A)
K = ("\t} else {\n"
     "\t\tif (len != 8) {\n"
     "\t\t\tfatal(\"[ sgi_re: len = %i not implemented ]\n\", (int) len);\n"
     "\t\t\texit(1);\n"
     "\t\t}\n"
     "\t\tif (writeflag == MEM_WRITE) {\n"
     "\t\t\tif (!(d->warned & SGIRE_W_UNMAP_WR)) {")
io.open(p, "w", encoding="utf-8", newline="\n").write(s.replace(A, K, 1))
print("      edit applied: len != 8 kill re-added")
PY
run W
cp $SEC/src/devices/dev_sgi_re.c $C/src/devices/dev_sgi_re.c

echo "=== RESTORE ==="
cmp -s $C/src/devices/dev_sgi_re.c $SEC/src/devices/dev_sgi_re.c && echo "  clone cmp vs SEC: CLEAN" || echo "  *** DIRTY ***"
rm -f $C/.MUTANT
echo L2FIX_DONE
