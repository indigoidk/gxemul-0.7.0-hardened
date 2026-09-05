#!/bin/bash
#  Split MUT4 into its two verdict-relevant mutants, one build+run each.
set -x
S=/tmp/gxseat
T=$S/tree
PROBE=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/pcc2_width_probe.py

build () {
	rm -f $T/src/devices/dev_pcc2.o $T/gxemul
	( cd $T && make ) > $S/build2.log 2>&1 || { echo BUILD_FAILED; grep -m5 error $S/build2.log; return 1; }
	[ "$T/gxemul" -nt "$T/src/devices/dev_pcc2.c" ] || { echo STALE_BINARY; return 1; }
	echo build ok
}
runprobe () {
	( cd $S && timeout 900 python3 -u $PROBE $T/gxemul "$1" ) > $S/$1.out 2>&1
	grep -E '^PCC2W_(RESULT|RED|PROBE_DONE)' $S/$1.out
}
mutate () {
python3 - "$1" <<'PYEOF'
import sys
tag = sys.argv[1]
p = "/tmp/gxseat/tree/src/devices/dev_pcc2.c"
s = open(p).read()
def one(old, new):
    global s
    n = s.count(old); assert n == 1, "COUNT %d for %r" % (n, old[:70])
    s = s.replace(old, new)
if tag == "FALL_VECBASE":
    one('pcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);\n\t\t\tbreak;',
        'pcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);')
elif tag == "FALL_IPL":
    one('pcc2_width_decline(d, PCC2_W_IPL_LEN, "PCCTWO_IPL", len);\n\t\t\tbreak;',
        'pcc2_width_decline(d, PCC2_W_IPL_LEN, "PCCTWO_IPL", len);')
else:
    raise SystemExit("unknown " + tag)
open(p, "w").write(s)
print("  mutated: " + tag)
PYEOF
}

echo "=== M_FALL_VECBASE alone (82/82 = sweep) ==="
cp $S/base.c $T/src/devices/dev_pcc2.c
mutate FALL_VECBASE && build && runprobe M_FALL_VECBASE

echo "=== M_FALL_IPL alone (82/82 = sweep) ==="
cp $S/base.c $T/src/devices/dev_pcc2.c
mutate FALL_IPL && build && runprobe M_FALL_IPL

cp $S/base.c $T/src/devices/dev_pcc2.c
echo SPLIT_DONE
