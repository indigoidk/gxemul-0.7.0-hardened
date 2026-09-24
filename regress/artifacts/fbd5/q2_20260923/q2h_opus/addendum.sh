#!/bin/bash
# Fix the one construction artifact (QIASRD: two statements into a braceless `if` -> dangling else).  Remake with a
# comma operator so it is ONE statement; measure on both instruments.  Prediction (written here, before the build):
# GREEN on both -- irq_asserted=1 on a LEGAL IRQ_STATUS read; X9/X10/X6 do not check irq_asserted, and the X14 line-4
# read row already has it 1.  Disclosed: NOT COVERED "irq_asserted = 1 at the other legal accesses and widths".
set -u
X=/tmp/opusr3e_add
F=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2h/frozen
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2h/opus
rm -rf "$X"; cp -a /tmp/opusr3e "$X"
rm -f "$X"/regress/b3d "$X"/regress/b3e "$X"/regress/d3d "$X"/regress/d3e
SRC="$X/src/devices/dev_footbridge.c"
CF() { gcc -O2 -std=c99 -Wall -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections \
    -Wl,--gc-sections -I"$X/src" -I"$X/src/include" -I"$X/src/include/thirdparty" -o "$2" "$1" -lm; }
echo "OQIASRD2: comma form"; echo "opusr3e_add.MUTANT" > "$X/.MUTANT"
python3 - "$SRC" <<'PY'
import io,sys
p=sys.argv[1]; s=io.open(p,encoding='utf-8',newline='').read()
old="\t\t\todata = d->irq_status & d->irq_enable;"
new="\t\t\todata = (d->irq_asserted = 1, d->irq_status & d->irq_enable);"
assert s.count(old)==1, s.count(old)
io.open(p,'w',encoding='utf-8',newline='').write(s.replace(old,new))
print("patched")
PY
cd "$X/regress"
for pair in "diff_footbridge.3d.c d3d 3d" "diff_footbridge.3e.c d3e 3e"; do
  set -- $pair; CF "$1" "$2" 2>/tmp/w.err
  echo "$3 build rc=$? warn=$(grep -c warning: /tmp/w.err)"
  [ -x "./$2" ] && { ./$2 >/tmp/o.log 2>&1; echo "$3 $(grep -c '^  FAIL' /tmp/o.log | tr -d '\n') FAIL; $(tail -1 /tmp/o.log)"; \
     grep '^  FAIL' /tmp/o.log | grep -v SELFCHECK | head -4; }
done
# restore + verify
cp "$F/dev_footbridge.c" "$SRC"
cmp "$SRC" "$F/dev_footbridge.c" && echo "restored == frozen"
CF diff_footbridge.3e.c d3e 2>/dev/null; ./d3e >/tmp/b.log 2>&1; echo "baseline after restore: $(tail -1 /tmp/b.log) $(grep -c '^  FAIL' /tmp/b.log) FAIL"
rm -f "$X/.MUTANT"; echo "sentinel cleared"; echo ADDENDUM_DONE
