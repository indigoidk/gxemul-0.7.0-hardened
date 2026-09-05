import sys
CLONE = '/tmp/gxopus_p10/src/devices/dev_pcc2.c'
which = sys.argv[1]
HEAD = '\t\tif (len != 1 && writeflag == MEM_WRITE'
TAIL = '\t\t\tpcc2_width_decline(d, PCC2_W_TXICR_LEN, "PCCTWO_TxICR", len);\n'
OLD = HEAD + ') {\n' + TAIL
COND = {
 'M_T1JOINT': ('\n\t\t    && !(d->pending_timer1_interrupts && d->pending_timer2_interrupts\n'
               '\t\t         && relative_addr == PCCTWO_T1ICR)'),
 'M_P2T1':    ('\n\t\t    && !(d->pending_timer2_interrupts'
               ' && relative_addr == PCCTWO_T1ICR)'),
 'M_PENDOR':  ('\n\t\t    && !(d->pending_timer1_interrupts'
               ' || d->pending_timer2_interrupts)'),
}[which]
NEW = HEAD + COND + ') {\n' + TAIL
s = open(CLONE, encoding='utf-8', errors='replace').read()
n = s.count(OLD)
print("anchor occurrences:", n)
assert n == 1, "ANCHOR NOT UNIQUE -- ABORT"
open(CLONE, 'w', encoding='utf-8', newline='').write(s.replace(OLD, NEW))
print("mutant applied:", which)
