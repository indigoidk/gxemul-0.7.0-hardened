#!/bin/bash
# Independently corroborate the brief's own motivating mutants on my 3d and 3e binaries:
#   CXT1 (codex toggle), WB4, WB8 (tail widened).  Brief claims: all GREEN on 3d, RED on 3e (3/96/144).
set -u
X=/tmp/opusr3e_bs
F=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2h/frozen
rm -rf "$X"; cp -a /tmp/opusr3e "$X"; rm -f "$X"/regress/b3? "$X"/regress/d3?
SRC="$X/src/devices/dev_footbridge.c"
CF() { gcc -O2 -std=c99 -Wall -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections \
    -Wl,--gc-sections -I"$X/src" -I"$X/src/include" -I"$X/src/include/thirdparty" -o "$2" "$1" -lm; }
run() { cd "$X/regress"; local nm="$1" py="$2"; echo "opusr3e_bs $nm" > "$X/.MUTANT"
  cp "$F/dev_footbridge.c" "$SRC"
  python3 - "$SRC" "$py" <<'PY'
import io,sys
p,expr=sys.argv[1],sys.argv[2]
s=io.open(p,encoding='utf-8',newline='').read()
old,new=expr.split('@@@')
# The tail line also occurs in footbridge_isa; the main footbridge handler is the LAST occurrence.
assert s.count(old)>=1,"anchor %d for %s"%(s.count(old),old[:30])
i=s.rfind(old)
io.open(p,'w',encoding='utf-8',newline='').write(s[:i]+new+s[i+len(old):])
print("  count=%d, replaced LAST"%s.count(old))
PY
  for pr in "diff_footbridge.3d.c d3d 3d" "diff_footbridge.3e.c d3e 3e"; do
    set -- $pr; CF "$1" "$2" 2>/dev/null
    ./$2 >/tmp/bs.log 2>&1
    echo "  $nm $3: $(grep -c '^  FAIL' /tmp/bs.log|tr -d '\n') raw-FAIL (incl 2 selfcheck) -> $(awk '/^[0-9]+ rows/{print}' /tmp/bs.log)"
  done
}
# CXT1: else if (!d->warned_irq_status_w)  ->  else if ((d->irq_asserted ^= 1, !d->warned_irq_status_w))
run CXT1 'else if (!d->warned_irq_status_w) {@@@else if ((d->irq_asserted ^= 1, !d->warned_irq_status_w)) {'
# WB4: the tail len -> (len<4?4:len)
run WB4 'memory_writemax64(cpu, data, len, odata);@@@memory_writemax64(cpu, data, len < 4 ? 4 : len, odata);'
# WB8: the tail len -> 8   (brief notes it also overflows the harness buf[4]; expect 3e RED, maybe rc!=0)
run WB8 'memory_writemax64(cpu, data, len, odata);@@@memory_writemax64(cpu, data, 8, odata);'
cp "$F/dev_footbridge.c" "$SRC"; cmp "$SRC" "$F/dev_footbridge.c" && echo "restored==frozen"
CF diff_footbridge.3e.c d3e 2>/dev/null; ./d3e >/tmp/b.log 2>&1; echo "baseline: $(awk '/rows,/{print}' /tmp/b.log)"
rm -f "$X/.MUTANT"; echo "sentinel cleared"; echo BS_DONE
