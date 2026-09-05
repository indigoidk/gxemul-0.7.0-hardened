# PASS 10 -- Opus seat PREDICTIONS, written BEFORE the first mutant build
# (this file's mtime is the order witness; the first mutant BINARY must be newer)

Instrument: /tmp/frozen_probe_p10.py, md5 43471ae2b514d3b637f5190ec57a4000 (== live probe).
Clone: /tmp/gxopus_p10, cp -a of build/, dev_pcc2.c md5 f91686366779f961a3776b438ce37992
       == GXEMUL-SEC (cmp rc 0), rebuilt, binary 13:08:49 > source 04:13:21.
Baseline named: the UNCOMMITTED working set on top of b78bb0f (dev_pcc2.c is
       identical to SEC's working copy, which is the round's post-fix product code).

## BASE
    194/194, zero red.
    (If any pend*/ovf*/pendboth row reds with "no-breakpoint" the host is starved by the
    other panel seats and every mutant score below is unusable; I will say so.)

## M_T1JOINT -- the joint-pending predicate CONDITIONED ON THE T1 LABEL
Edit at the TxICR guard (dev_pcc2.c, `case PCCTWO_T2ICR:`/`case PCCTWO_T1ICR:`):
    if (len != 1 && writeflag == MEM_WRITE
        && !(d->pending_timer1_interrupts && d->pending_timer2_interrupts
             && relative_addr == PCCTWO_T1ICR)) {

    PREDICTION: 194/194 -- a TOTAL ESCAPE.  ZERO red rows.

WHY (derived by reading, before the build):
  The conjunct disables the guard only when p1>0 AND p2>0 AND the access is at T1ICR
  (0x1b).  No session in the 194-row detector holds that cell:
    * pend1/pendn1 arm TIMER 1 ONLY -- pend_arm(T1CMP,T1COUNT,T1ICR,T1CTL); T2CTL keeps
      its init 0 so CEN is clear, pcc_timer_tick's timer-2 branch never runs, p2 == 0.
    * pendboth arms BOTH but wide-writes at T2ICR (0x1a) -- ST_H(9, T2ICR) at CODE+0x200.
    * every other T1ICR wide write (rb t1icr, rb t1icr il4, rb4/rb8 t1icr, op t1icr dcl)
      and every `latch all*' (which uses 0x1a for the TxICR block) has BOTH counts 0.
  So the pass-9 repair closed (p1>0,p2>0) at the T2 label and left the SYMMETRIC T1 cell
  open.  That is the `#499' two-by-two-with-one-cell-empty shape reproduced INSIDE the
  repair for it, which is what the carrier says a repair pass is for.
  It is in the clause-(d) DEPENDS-ON operand set by rule (2): relative_addr, p1 and p2 are
  ALL read by the guarded body (dev_pcc2.c :516,:519,:522,:526,:531).

## M_PENDOR -- the `||' form the task asks me to confirm
    ... && !(d->pending_timer1_interrupts || d->pending_timer2_interrupts)) {

    PREDICTION: 184/194 -- TEN red rows, all of them PRE-EXISTING except two:
        pend2 decl (0), pend2 rb (0x20)        <- pre-existing (pass 6)
        pend1 decl (0), pend1 rb (0x20)        <- pre-existing (pass 6)
        pendn2 decl (0), pendn2 rb (0x20)      <- pre-existing (pass 8)
        pendn1 decl (0), pendn1 rb (0x20)      <- pre-existing (pass 8)
        pendboth decl (0), pendboth rb (0x20)  <- the new rows (pass 9)
    Green and why: pend*/pendn*/pendboth `arm' and `arm1' are read BEFORE the wide write;
    every non-timer TxICR row has both counts 0, so !(0||0) is true and the guard fires.
    Readback value 0x20 in each case: the landed idata is 0x0000, so
    reg &= ~0x17 leaves INT (0x20) -- which reassert_interrupts sets with |= and NEVER
    clears -- and |= (0 & 0x17) adds nothing.
    => the `||' form is killed WITHOUT the new rows, by the eight single-timer rows named
    above.  It is NOT evidence for the pendboth row.

## Predictions about the ANSWERS (so they are falsifiable too)
* Q2 `pendboth arm1' soundness: the OBSERVABLE is the T1ICR INT bit, and INT is set with
  `|=' in reassert_interrupts and cleared ONLY by an ICLR write -- it is STICKY.  So the
  row observes "p1 was non-zero at some tick", not "p1 is non-zero now".  I predict the
  FACT holds anyway (one pcc_timer_tick callback services both timers, T1 is armed first,
  nothing decrements p1 in that session) but the ROW'S NOTE overclaims what it observes.
* Q2 load sensitivity: NOT load sensitive for the "both" property -- ONE callback sets
  both pending counts, because pcc_timer_tick handles T1 and T2 in the same call and both
  are armed compare=1/count=0.  The shared hazard is the 20 s `continue' ceiling.
* Q5 smallest edit that passes 194 rows: M_T1JOINT above (one added conjunct), and I
  expect it to pass.
* Q6: the brief's own "THE ENCLOSING CODE" section is EMPTY -- two bare `case' labels and
  zero body lines, where 57 lines of arm (dev_pcc2.c TxCTL and TxICR arms) are claimed.

Written 2026-09-04 by the Opus pass-10 seat, before any mutant build.

## APPENDED 2026-09-04 13:2x, STILL BEFORE ANY MUTANT BUILD (no mutant exists yet;
## the clone is BASE and the BASE probe run is still in flight)

## M_P2T1 -- a PAIR, inside the MAIN LOOP'S OWN proposed bound, that I predict escapes
    ... && !(d->pending_timer2_interrupts && relative_addr == PCCTWO_T1ICR)) {

    PREDICTION: 194/194 -- a TOTAL ESCAPE.  ZERO red rows.

WHY: the guard is disabled only when timer 2 has a pending count AND the access is at
T1ICR (0x1b).  Every detector row that wide-writes at T1ICR arms TIMER 1 or no timer at
all -- pend1, pendn1 (pend_arm(T1CMP,T1COUNT,T1ICR,T1CTL); T2CTL keeps init 0 so CEN is
clear and p2 stays 0), rb t1icr, rb t1icr il4, rb4/rb8 t1icr, op t1icr dcl (no timer
armed).  The one session that holds p2 > 0 (pend2/pendn2) writes at T2ICR, and the one
that holds BOTH (pendboth) also writes at T2ICR.  There is no rb2 t1icr.
    This matters MORE than M_T1JOINT for the rule question: it is a PAIR of body-read
    lvalues (p2, relative_addr), its joint space is finite (2 pending classes x 2 labels),
    and the empty cell is reachable by a path the detector ALREADY uses (arm timer 2, then
    an operator `put h' at the odd 0x1b -- exactly pend1's shape with the other timer).
    So it sits INSIDE the main loop's own proposed bound and the shipped repair does not
    cover it.  If it escapes, the main loop's ruling condemns its own repair.

## M_PENDOR -- I now intend to DERIVE this rather than measure it (time), and I will say so.
