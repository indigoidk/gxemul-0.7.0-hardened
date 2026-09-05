#!/bin/bash
#  SEAT CHECK -- pcc2widthkills pass 3 review.
#  Four mutants the brief does not measure, combined in ONE build (disjoint
#  channels; a green union with conjunctive rows implies each sweeps):
#    M_FALL_VECBASE   break removed at VECBASE  (body STORES idata & 0xf0)
#    M_FALL_IPL       break removed at IPL      (body print-only, like PSCALEADJ)
#    M_LENEQ2_GENCTL  len != 1 -> len == 2      (len-4 writes land; no put w rows)
#    M_NOWRF_SCCRX    writeflag clause dropped   (wide READS decline-announce)
#  Plus BASE (want 82/82) and POSCTL = M_DELETE_VECBASE (want RED) as controls.
set -x
S=/tmp/gxseat
T=$S/tree
PROBE=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/pcc2_width_probe.py

rm -rf $S
mkdir -p $T
cd /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
tar cf - --exclude=.git --exclude=_scratchpad --exclude=regress/artifacts . | (cd $T && tar xf -)
cd $T
md5sum $PROBE src/devices/dev_pcc2.c

./configure > $S/configure.log 2>&1 || { echo CONFIGURE_FAILED; tail -20 $S/configure.log; exit 1; }
make -j$(nproc) > $S/make.log 2>&1 || { echo BUILD_FAILED; grep -m5 error $S/make.log; exit 1; }
[ -x gxemul ] || { echo NO_BINARY; exit 1; }

cp src/devices/dev_pcc2.c $S/base.c

build () {
	rm -f $T/src/devices/dev_pcc2.o $T/gxemul
	( cd $T && make ) > $S/build.log 2>&1 || { echo BUILD_FAILED; grep -m5 error $S/build.log; return 1; }
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
G = "if (len != 1 && writeflag == MEM_WRITE) {"
def one(old, new):
    global s
    n = s.count(old); assert n == 1, "COUNT %d for %r" % (n, old[:70])
    s = s.replace(old, new)
if tag == "MUT4":
    one('pcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);\n\t\t\tbreak;',
        'pcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);')
    one('pcc2_width_decline(d, PCC2_W_IPL_LEN, "PCCTWO_IPL", len);\n\t\t\tbreak;',
        'pcc2_width_decline(d, PCC2_W_IPL_LEN, "PCCTWO_IPL", len);')
    one(G + '\n\t\t\tpcc2_width_decline(d, PCC2_W_GENCTL_LEN, "PCCTWO_GENCTL", len);',
        'if (len == 2 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_GENCTL_LEN, "PCCTWO_GENCTL", len);')
    one(G + '\n\t\t\tpcc2_width_decline(d, PCC2_W_SCCRX_LEN, "PCCTWO_SCCRX", len);',
        'if (len != 1) {\n\t\t\tpcc2_width_decline(d, PCC2_W_SCCRX_LEN, "PCCTWO_SCCRX", len);')
elif tag == "POSCTL":
    one('\t\t' + G + '\n\t\t\tpcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);\n\t\t\tbreak;\n\t\t}\n', '')
else:
    raise SystemExit("unknown " + tag)
open(p, "w").write(s)
print("  mutated: " + tag)
PYEOF
}

echo "=== SEATBASE (want 82/82) ==="
build && runprobe SEATBASE

echo "=== MUT4 (FALL_VECBASE+FALL_IPL+LENEQ2_GENCTL+NOWRF_SCCRX; 82/82 = all four sweep) ==="
cp $S/base.c $T/src/devices/dev_pcc2.c
mutate MUT4 && build && runprobe MUT4

echo "=== POSCTL = M_DELETE_VECBASE (want RED: op vecbase dcl, latch all) ==="
cp $S/base.c $T/src/devices/dev_pcc2.c
mutate POSCTL && build && runprobe POSCTL

cp $S/base.c $T/src/devices/dev_pcc2.c
echo SEATCHECK_DONE
