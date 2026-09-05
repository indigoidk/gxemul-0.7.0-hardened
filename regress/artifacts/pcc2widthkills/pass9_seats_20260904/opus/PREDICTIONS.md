# Opus pass-9 seat -- PREDICTIONS, written BEFORE any mutant is built
(mtime of this file vs the mutant .out files is the order witness)

Clone /tmp/gxopus_p9 (cp -a of build/), dev_pcc2.c CMP_CLEAN vs SEC, baseline REBUILT
(MAKE_RC=0, FRESH_OK) before BASE.  Frozen instrument /tmp/frozen_probe_p9.py,
md5 36aabf395e641430cd639425e0711c63 == the shipped probe.

BASE                    190/190 expected.

## M_OPUS_PENDBOTH  -- the JOINT pending cell (in closure, NOT disclosed)
Edit, ONE line, at the TxICR guard only:
    if (len != 1 && writeflag == MEM_WRITE
        && !(d->pending_timer1_interrupts && d->pending_timer2_interrupts)) {
PREDICT **190/190 -- TOTAL ESCAPE**.
Why every row stays green: the TxICR body reads BOTH counts, so both are in the
clause-(d) rule-(2) operand set.  The instrument holds each SEPARATELY -- `pend2`/`pendn2`
arm timer 2 only (p1 == 0), `pend1`/`pendn1` arm timer 1 only (p2 == 0), and every other
session leaves both at 0.  NO SESSION ARMS BOTH TIMERS, so the conjunct is true in all 190
rows.  The joint state IS reachable (set T1CTL and T2CTL CEN with both ICR IEN).
Rows I expect to stay green and would most expect to red if I am wrong:
`pend1 decl`, `pend1 rb`, `pend2 decl`, `pend2 rb`, `pendn1 decl/rb`, `pendn2 decl/rb`.

## M_OPUS_IDATA2 -- the DISCLOSED value-test shape (control on the disclosure)
Edit, twelve lines, one per guard:  `&& idata != 2`
PREDICT **190/190 -- TOTAL ESCAPE**.
Wide-write values driven anywhere in the instrument: 0x0000, 0x0001, 0x0003, 0x0022,
0x0303, 0x1234, 0xaab8, 0xaabb, 0x00000003, 0xaab8ccd9, 0xaab8ccdd,
0x0000000000000003, 0xaab8ccdd00112240, 0xaab8ccdd00112244.  NONE is 2.
This is the contract's own disclosure ("any other constant is not (passes 7-8; Opus F13)")
turned into a measurement, so the Q4 answer is measured rather than reasoned.
Consequence if it shipped: `st.h 0x0002` to GENCTL stores 0x02 -- VECBASE's lane -- i.e.
the ORIGINAL lane defect, for exactly that value.
