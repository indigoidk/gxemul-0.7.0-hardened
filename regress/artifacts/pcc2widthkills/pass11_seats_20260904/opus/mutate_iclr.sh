#!/bin/sh
#  M_ICLR: exempt the (pending_timer2 > 0, idata & ICLR) cell at the TxICR width guard.
set -x
D=/tmp/gxopus_p11
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SRC=$D/src/devices/dev_pcc2.c
P=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p11_opus

#  1. build the mutant text on a SCRATCH copy and SYNTAX-CHECK it before touching the clone
cp $SEC/src/devices/dev_pcc2.c /tmp/mut_scratch.c
python3 - <<'PY'
lines = open('/tmp/mut_scratch.c').read().split('\n')
#  line 511 (1-based) is the TxICR guard; assert it before editing
i = 510
assert lines[i].strip() == 'if (len != 1 && writeflag == MEM_WRITE) {', repr(lines[i])
#  and assert the two case labels immediately above it
assert 'PCCTWO_T1ICR' in lines[509], repr(lines[509])
lines[i] = ('\t\tif (len != 1 && writeflag == MEM_WRITE\n'
            '\t\t    && !(d->pending_timer2_interrupts '
            '&& (idata & PCC2_TTIRQ_ICLR))) {')
open('/tmp/mut_scratch.c','w').write('\n'.join(lines))
print('MUTANT_TEXT_APPLIED')
PY
echo "SCRATCH_EDIT_RC=$?"
diff $SEC/src/devices/dev_pcc2.c /tmp/mut_scratch.c | tee $P/M_ICLR.diff
echo "DIFF_CHANGED_LINES=$(diff $SEC/src/devices/dev_pcc2.c /tmp/mut_scratch.c | grep -c '^[<>]')"

cd $D || exit 9
gcc -fsyntax-only -I$D -I$D/src/include -I$D/src/include/thirdparty /tmp/mut_scratch.c
echo "SYNTAX_RC=$?"
