# PASS 11, Opus seat -- PREDICTIONS, written BEFORE the first mutant build
(this file's mtime is the order witness; nothing below was measured when it was written)

Instrument: frozen copy of GXEMUL-SEC/regress/pcc2_width_probe.py, md5 6676c58d..., 203 rows.
Clone: /tmp/gxopus_p11 (cp -a of build/), BASE rebuilt in the clone.

## BASE
    203/203, no red rows.
    (Caveat I state in advance: the pend*/pendn*/ovf* rows are FREE-RUNNING and need the
     host's 100 Hz SIGALRM to fire inside a 20 s `continue'.  Eight panel seats are running
     concurrently.  If BASE is not 203/203 I will report the run STARVED, name the rows
     that read `no-breakpoint', and NOT treat any mutant number as comparable.)

## M_ICLR -- the mandated H1 measurement
    Edit, at the TxICR width guard (dev_pcc2.c:511), one added conjunct:
        if (len != 1 && writeflag == MEM_WRITE
            && !(d->pending_timer2_interrupts && (idata & PCC2_TTIRQ_ICLR))) {
    This exempts exactly the cells (p2 > 0, ICLR set) -- a cell of the ICLR partition, which
    the contract DISCLOSES BY COUNT rather than rowing.

    PREDICTION: **203/203 -- a TOTAL ESCAPE.  ZERO red rows.**

    Derivation, from the probe's own driven values (no measurement):
      * The conjunct can only change behaviour at a WIDE write to the TxICR block whose
        idata has bit 3 (ICLR = 0x08) set AND where pending_timer2 > 0 at that moment.
      * Wide writes at TxICR with bit 3 SET: `rb t2icr' and `rb t2icr il4' (ST_H of
        r6=0xaab8 -> lane 0xb8, and 0xb8 & 0x08 != 0) and `rb t1icr il4'
        (`put h ..., 0xaab8').  In ALL of those sessions no timer is armed
        (setup() + a bare program, no pend_arm / pendboth_arm), so pending_timer2 == 0
        and the conjunct is FALSE -> the guard fires exactly as on BASE.
      * Sessions where pending_timer2 > 0: `pend2', `pendboth', `pendn2'.  Their TxICR wide
        writes drive ONLY 0x0000 and 0x0013 (r9 = 0x0, r10 = 0x13); 0x13 & 0x08 == 0.
        So the conjunct is FALSE there too.
      * Therefore no row's wide write lands, and no readback, decl or survival row moves.

    IF I AM WRONG the interesting directions are: (a) some session I have not read arms a
    timer and then wide-writes an ICLR-bearing value -- then one or two `rb *icr' rows red;
    (b) the free-running rows starve and red for `no-breakpoint', which is an apparatus
    result and not a kill.

    WHAT THE MEASUREMENT DECIDES: whether a cell inside a DISCLOSED partition is reachable
    and escaping.  If 203/203, the contract's "disclosed with the count" does not discharge
    the adopted rule at this device, and H1's answer is that the rule DOES demand more than
    sixteen cells -- with the bound I write in FINDINGS.md.

## A second mutant, only if time allows (I expect not to reach it)
    M_INTICLR -- `&& !((d->pcctwo_reg[relative_addr] & PCC2_TTIRQ_INT) && (idata & PCC2_TTIRQ_ICLR))'.
    PREDICTION: 203/203, also a total escape, by the same argument (every row holding INT
    set drives 0x0000/0x0013; every row driving 0xb8 has INT clear).  Derivable from
    M_ICLR's result, so I will NOT spend a run on it unless M_ICLR surprises me.

## Two predictions about the RECORD, made before any run (checkable by reading, not by the table)
    P1. The CHANGELOG's part-10 table gives `M_P2IEN' red row `pendboth rb1i' as (0x13).
        I derive 0x33 from the body (reg[T1ICR] = 0x31 there, 0x31 & ~0x17 | 0x13 = 0x33)
        and predict the LOG says 0x33 -- i.e. the "measured" column carries the
        PREDICTION's value, not the log's.
    P2. The CHANGELOG says "the three decl rows expect 4".  The probe's three decl rows
        want 1, and PRETABLE_pass10.out says they stay at 1.  I predict the CHANGELOG
        sentence is simply false.
    (Both are reading claims; I record them here so the order is not in doubt.)

## HONESTY NOTE, added in the same minute
    P1 and P2 are NOT blind: I had already opened
    `regress/artifacts/.../part10/M_P2IEN.out' and CHANGELOG.md before writing this file,
    so they are CONFIRMED READINGS recorded here for completeness, not predictions.
    The mutant predictions above ARE blind -- no mutant has been built or run at this
    file's mtime, and the clone's BASE build was still copying.
