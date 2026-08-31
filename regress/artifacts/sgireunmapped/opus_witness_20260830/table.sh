#!/bin/bash
set -u
H=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opussgire
CLONE=/tmp/gxopus_sgire
PRISTINE=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_re.c
cd $CLONE

for V in base fix mret0 mlatch mwonly mshrink mshrinkb mtexshrink mnolatch; do
  echo "==================================================================="
  echo "VARIANT: $V"
  echo "$V applied to $CLONE/src/devices/dev_sgi_re.c" > $CLONE/.MUTANT
  python3 $H/mkvariant.py $V $PRISTINE $CLONE/src/devices/dev_sgi_re.c
  RC=$?
  if [ $RC -ne 0 ]; then echo "VARIANT GEN FAILED rc=$RC -- ABORT"; exit 1; fi
  rm -f $CLONE/src/devices/dev_sgi_re.o
  make >/tmp/mk_$V.log 2>&1
  if [ ! -f $CLONE/gxemul ]; then echo "NO BINARY"; exit 1; fi
  if [ $CLONE/gxemul -nt $CLONE/src/devices/dev_sgi_re.c ]; then
      echo "  build: FRESH (binary -nt source)"
  else
      echo "  build: STALE -- ABORT"; tail -20 /tmp/mk_$V.log; exit 1
  fi
  cp $CLONE/gxemul $CLONE/gxemul.$V
  python3 -u $H/detector.py $CLONE/gxemul.$V $V 2>&1
done

echo "==================================================================="
echo "=== RESTORE the clone to baseline and VERIFY against SEC ==="
python3 $H/mkvariant.py base $PRISTINE $CLONE/src/devices/dev_sgi_re.c
cmp -s $CLONE/src/devices/dev_sgi_re.c $PRISTINE && echo "RESTORE cmp vs SEC: CLEAN" || echo "RESTORE: DIFFERS"
rm -f $CLONE/.MUTANT
echo "TABLE_DONE"
