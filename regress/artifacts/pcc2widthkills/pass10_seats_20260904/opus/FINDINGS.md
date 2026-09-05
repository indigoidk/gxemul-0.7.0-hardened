PASS10_SEAT_ALIVE_20260904

First line of the brief, verbatim:
# pcc2widthkills -- PASS 10: the pass on the pass-9 repair.  Pass 9's measuring seat found a joint state no session held (both timers pending) and measured a total escape on it; this diff holds it, masks the load-sensitive overflow rows, and corrects the record.  Detector 190 -> 194; product code unchanged.  It carries a RULE QUESTION.

# Opus pass-10 seat -- FINDINGS

## VERDICT

DO NOT CLOSE.  RULE RULING: joint states ARE inside clause (d)'s DEPENDS-ON closure -- rule (2)
bounds the ALPHABET a qualifying conjunct may draw from, not its ARITY -- but the main loop's
proposed bound (PAIRS ... where the joint space is finite and a cell is a reachable guest state)
is the wrong dial, and ITS OWN BOUND CONDEMNS ITS OWN REPAIR: I MEASURED a TWO-lvalue conjunct,
drawn entirely from the guarded body's read set, sweeping the repaired 194-row detector CLEAN.
L2 floor breach, repair in-round.

## THE TABLE (every number names its log; all logs in this directory)

    run         predicted   measured   red rows   log
    BASE          194/194   194/194    0          BASE.out
    M_P2T1        194/194   194/194    0          M_P2T1.out     <- TOTAL ESCAPE
    M_T1JOINT     194/194   194/194    0          M_T1JOINT.out  <- TOTAL ESCAPE

    M_P2T1     && !(d->pending_timer2_interrupts && relative_addr == PCCTWO_T1ICR)
    M_T1JOINT  && !(d->pending_timer1_interrupts && d->pending_timer2_interrupts
                    && relative_addr == PCCTWO_T1ICR)
    both at the TxICR guard.  M_P2T1.diff = 3 lines vs SEC, M_T1JOINT.diff = 4 lines.

Both predictions were written BEFORE either build: PREDICTIONS.md mtime 13:19:27, first mutant
binary 13:24:15 (DRIVER.log records both).  BASE was measured FIRST, on an idle host (loadavg
0.06, nproc 8), and every pend / pendn / ovf / ovfhi / pendboth row was green, so the
free-running rows were not starved and the zeros are not apparatus artefacts.

APPARATUS, verified rather than trusted:
* clone /tmp/gxopus_p10 = cp -a of build/; cmp of src/devices/dev_pcc2.c against GXEMUL-SEC rc 0,
  md5 f91686366779f961a3776b438ce37992 both sides; no .MUTANT anywhere in build/ or the clone at
  start (clone_and_build.out).
* baseline rebuilt in the clone (rm src/devices/dev_pcc2.o; make -j4, MAKE_RC 0), binary 13:08:49
  newer than source 04:13:21.
* probe frozen to /tmp/frozen_probe_p10.py, md5 43471ae2b514d3b637f5190ec57a4000 == the live
  probe; run from GXEMUL-SEC/regress, which the probe only reads (its one write is
  /tmp/pcc2_dummy.bin).
* each mutant: sentinel dropped FIRST, source restored from SEC (never from a backup), mutated
  through a unique anchor (assert count == 1), diff-counted against SEC with the added lines
  quoted, rebuilt, [ binary -nt source ] checked.
* after the table: restored from SEC, rebuilt (MAKE_RC 0), cmp CLEAN, sentinel cleared.
  GXEMUL-SEC git status --porcelain is the same 21 entries it was at the start; the live probe's
  md5 is still 43471ae2; src/devices/dev_pcc2.c is still 32/12 against HEAD.  Nothing was written
  to GXEMUL-SEC, build/, est/ or build-asan/.

## 1.  THE RULE QUESTION

### 1a.  The text does not say what the dissent needs it to say

Clause (d)'s own worked example is "a condition qualified (if (X) -> if (X && Y))".  Y is a
CONDITION, not a field.  No arity restriction appears anywhere in the clause.  What rule (2)
restricts is where the operands COME FROM -- "swaps drawn ONLY from fields the guarded BODY
reads".  That is an ALPHABET bound.  Reading it as an ARITY bound is an addition to the text,
and it is the addition the whole dissent rests on.

An alphabet bound is the right kind because it is derivable by reading and it is what makes the
closure NON-TRANSITIVE -- the property the carrier actually names.  An arity-1 cut is arbitrary:
nothing explains why 1 and not 2, and this pass measures that 1 is unsound.

### 1b.  Where the DISSENT fails -- my own seat's argument, so I take it first

(i) THE PLAUSIBILITY PREMISE IS REFUTED BY THE CODE THE GUARD GUARDS, and the dissent could not
see that because the brief did not inline it.  The dissent says && !(p1 && p2) "is not an edit
anyone writes".  The guarded body is written like this (dev_pcc2.c, the TxICR arm):

    if (relative_addr == PCCTWO_T1ICR && (idata & PCC2_TTIRQ_ICLR)
        && d->pcctwo_reg[relative_addr] & PCC2_TTIRQ_INT
        && d->pending_timer1_interrupts > 0)
            d->pending_timer1_interrupts --;

A FOUR-term conjunction over exactly the closure's lvalues -- label, idata, register, pending
count -- and it appears TWICE, once per timer.  Multi-term conjunctions over these fields are
this function's house style, so hoisting one into the guard is the MOST plausible growth this
arm admits, not the least.  "Nobody writes that" is measurably false of this function.

The pass-9 brief did not inline the TxICR body either (see 6b).  So the plausibility claim was
made with the evidence that refutes it outside the packet.  That is a brief defect that produced
a wrong seat argument, and it is the sketch rule's own failure mode.

(ii) EXPONENTIAL IN THE NUMBER OF BODY-READ FIELDS ARGUES AGAINST A BOUND NOBODY PROPOSED.  The
predicate space over these lvalues is INFINITE at arity 1 already (< 2, < 10000, == 0x37, any
mask).  The closure has never been bounded by counting predicates; it is bounded by (a) the
alphabet, (b) the value-classes the rows already establish, and (c) the standing rule that rows
are owed PER ENUMERATED MUTANT, never per reachable state.  Arity does no work in that argument,
and removing the arity cut touches none of (a), (b), (c).

(iii) ROW DEMAND IS PER ENUMERATED MUTANT, SO NO ROW IS OWED -- A CATEGORY ERROR.  That rule
governs the ROW/MUTANT ratio.  It cannot settle what the MUTANT SET contains.  The dissent uses a
rule about the denominator to answer a question about the numerator.

(iv) THE DISSENT'S OWN REMEDY IS INCONSISTENT WITH WHAT PASS 9 SHIPPED.  Its L4 sentence would be
"no session arms both timers, so a predicate over the PAIR is outside the sample."  Pass 9 then
shipped four rows for a mutant the same seat called out of scope.  Under the dissent's ruling
those four rows are the addition licence's "cannot hurt", and they cost one more ~25 s
free-running session in a gate the contract already calls load-sensitive.  The round cannot have
it both ways: either pairs are in the closure (and the repair is incomplete, which I measured),
or they are out (and the repair should not exist).

WHAT THE DISSENT GETS RIGHT, and it should be carried forward: every SINGLE-operand form at this
arm is killed, and it named the killing rows correctly.  I did not re-measure those (see
DENOMINATOR); the contract cites 118/118 for two of them and pass 8 measured M_PEND2_LT2 at
188/190.  Its warning that an unbounded multi-operand reading is #392 is also right, and it is
why 1e fixes the bound rather than removing it.

### 1c.  Where the MAIN LOOP's four-point disposition fails

(1) THE JOINT CELL IS ONE OF FOUR IN A FINITE TWO-BY-TWO THE CLASS-CLOSURE AMENDMENT SAYS TO
CLOSE IN ONE DIFF.  Correct as doctrine, FALSE as a description of what the diff did.  The
amendment says enumerate the full space FROM THE FUNCTION'S OWN INPUTS and close every cell in
ONE diff.  The function's own inputs at this arm include relative_addr, on which the body
branches four times; TxICR serves TWO case labels.  The space is 2x2x2; the repair closed the
eighth cell at ONE label; I measured the other one open.  The main loop cited the amendment
against cell-by-cell repair and then made a cell-by-cell repair.

(2) IT IS THE GUEST'S ORDINARY STATE (clock + statclock).  I cannot settle this premise: there is
no OpenBSD source and no PCC2 / MVME datasheet on disk (ls _scratchpad/*.pdf lists fifteen PDFs;
none is one), and the contract's own DOES NOT CATCH list already puts "what real hardware does"
out of scope.  It is an uncheckable premise carrying a load-bearing point.  THE IN-TREE
SUBSTITUTE IS STRONGER AND COSTS ONE READ: pcc_timer_tick services BOTH timers in ONE callback,
and reassert_interrupts reads BOTH counts unconditionally on every call -- so the MODEL treats
(p1, p2) as a joint input at every tick.  That is a fact about the code under test.  Also,
"ordinary" overstates: a real ISR writes ICLR promptly, so both-pending is a window, not a steady
state.  REACHABILITY is what the bound needs; typicality is not.

(3) ONE PEND-TYPE SESSION COSTS ~25 s AND IS LOAD-STABLE.  Load-stable in VALUE: true, and for a
better reason than given -- one callback arms both timers (compare 1, count 0, both CEN), and INT
is set with |= in reassert_interrupts and cleared only by an ICLR write, so 0x31 cannot decay.
Load-SENSITIVE in ARRIVAL: also true, and unstated -- the row still depends on a SIGALRM landing
inside program_free's 20 s continue ceiling, exactly like its four siblings.  The brief conflates
the two.

(4) THE ASYMMETRY ARGUMENT.  Sound, but it cannot be the warrant: taken alone it licenses any
row, which is the #392 shape the dissent fears.  The bound has to carry the weight.

### 1d.  Is the proposed bound finite / derivable / would it have found #499's cells?

FINITE: yes, but by accident of the arity cut, and its own words are loose.  "joint space is
finite" is false of two ints -- what is finite is the space of value-CLASSES the rows
distinguish, an abstraction rather than a domain.  "reachable GUEST state" is too narrow: half
this detector's blocks are operator-only, and BOTH escapes I measured live on the operator path
at an odd offset, which the contract admits as first-class coverage.

DERIVABLE FROM THE DIFF BY READING: yes, and this is the bound's best property -- the per-lvalue
value-class list is already written into the contract's GUARD'S OPERAND SPACE section.

WOULD IT HAVE FOUND #499's CELLS?  #499's third-pass breach was a guard "re-added and CONDITIONED
on the first component" -- a (predicate, component) PAIR -- so yes, a pairs bound admits it.
BUT THAT IS EXACTLY WHY THE PAIRS BOUND DOES NOT SAVE THIS ROUND: M_P2T1 is a pair too, and the
shipped detector has no row for it.  Under the main loop's own bound this is an L2 floor breach.
The arity cut fails on the NEXT axis: #499's pass 3 found "direction AND position" -- two more
axes at once -- and M_T1JOINT is the arity-3 form of the same escape, equally plausible, equally
reachable, sitting just outside a bound set at 2.  Arity is a guess about how many axes the next
breach will span.

### 1e.  THE BOUND I WOULD PUT INTO THE RULE -- one sentence

  Clause (d)'s multi-operand closure is the CROSS-PRODUCT of the value-classes the detector's own
  rows already establish for each lvalue the guarded body reads -- with the arm's DISPATCH axes
  (any lvalue the body itself branches on, such as relative_addr at a shared case block) included
  as full axes rather than as context -- a row being owed for a cell only when an enumerated
  mutant shape distinguishes it and a path the detector already admits reaches it, and every
  predicate not expressible as a union of those cells DISCLOSED by name.

with the operational corollary, which is what a round actually applies:

  A repair that adds a value-class to a body-read lvalue owes that class at EVERY value of the
  arm's dispatch axes, in the SAME diff.

Why it terminates, stated rather than assumed:
* the axes are the body's own read-set: finite, non-transitive, unchanged;
* the multiplicands are the classes the CONTRACT already lists (2-4 each here), not 2^n boolean
  functions -- a product of small integers.  At TxICR: 4 reg classes x 3 p1 x 3 p2 x 2 labels =
  72 cells;
* the DEMAND is INCREMENTAL: only cells a repair NEWLY creates are owed.  Here that is one new
  class x two labels = TWO ROWS, not 72;
* row demand stays per enumerated mutant, so cells no mutant separates collapse.  The generator
  side is untouched and "a filter can never demand a new row" still holds for everything else.

THE PRICE, named rather than glossed: a detector claiming clause-(d) closure must SHIP the
per-lvalue value-class list.  This one does (GUARD'S OPERAND SPACE); most do not.  That is a real
new obligation and the panel should adopt it knowingly.

I DO NOT REJECT THE ROW.  Keep pendboth * and add its T1 sibling.

## 2.  VERIFY THE FOUR ROWS

pendboth arm1 IS SOUND IN FACT AND ITS NOTE OVERCLAIMS WHAT IT OBSERVES.  Its observable is
T1ICR's INT bit, and INT is set with |= in reassert_interrupts and cleared ONLY by an ICLR write.
It is STICKY.  So the row proves "p1 was non-zero at some tick", not "p1 is non-zero now" -- and
its note says the latter ("both counts non-zero at the wide write").  The FACT holds anyway, by
reading: with compare 1 and count 0 the first callback sets interrupt1 = 1 and p1 += 1; T1 is
armed BEFORE T2 in pendboth_arm(), so the callback that gives T2 its INT has already given T1
one; without COC no later callback re-triggers (old_count < compare fails); and nothing decrements
p1 -- the only decrementer is a TxICR write body at T1ICR with ICLR, and this session's only
T1ICR access is a READ.  THE LOAD-BEARING PROOF IS NOT THE ROW, IT IS THE MUTANT: M_PENDBOTH
reddening pendboth decl proves p1 && p2 was TRUE at the guard.  Say that in the note, or the row
reads as a direct observation it is not.

LOAD SENSITIVITY: the four rows are load-STABLE in value (one callback arms both; INT cannot
decay) and load-SENSITIVE in arrival, like pend* / pendn* / ovf*: they need a SIGALRM inside
program_free's 20 s continue ceiling, after which how == no-breakpoint and all four red with the
reason named.  On my idle host all four were green on BASE and on both mutants.

DOES M_PENDBOTH RED EXACTLY TWO ROWS?  Verified in the round's own preserved artifact, not taken
from the brief: killtable2_20260903/part9/M_PENDBOTH.out has exactly two FAIL lines --
pendboth decl 0 vs 1, pendboth rb 0x20 vs 0x31 -- and PCC2W_RESULT=192/194.

WOULD A ||-FORM HAVE BEEN CAUGHT BY ROWS THAT ALREADY EXISTED?  YES -- DERIVED, NOT MEASURED, and
I say so plainly.  && !(p1 || p2) disables the guard whenever EITHER count is non-zero, so the
wide write lands and the arm's decl/rb pair reds at every timer session: pend2 decl + pend2 rb,
pend1 decl + pend1 rb, pendn2 decl + pendn2 rb, pendn1 decl + pendn1 rb (EIGHT rows, all
pre-existing) plus pendboth decl + pendboth rb.  Predicted 184/194.  The readback is 0x20 in each
case: the driven value is 0x0000, so reg &= ~0x17 leaves only INT and |= (0 & 0x17) adds nothing.
THE ||-FORM IS THEREFORE NOT EVIDENCE FOR THE NEW ROWS -- the eight single-timer rows kill it on
their own.  I dropped this run in favour of the two escapes; a deliberate omission, not an
oversight.

AND THE T1-LABEL WIDE WRITE IS THE FINDING: NO, IT WOULD NOT HAVE BEEN CAUGHT, AND IT STILL IS
NOT.  Both measured escapes are exactly that cell.  The repair's session writes only at T2ICR
(ST_H(9, T2ICR) at CODE+0x200); every detector row that wide-writes at T1ICR (0x1b) -- pend1,
pendn1, rb t1icr, rb t1icr il4, rb4/rb8 t1icr, op t1icr dcl, and every latch all*, which uses
0x1a for the TxICR block -- has p2 == 0, because pend_arm(T1...) leaves T2CTL at its init 0 so
CEN never sets and pcc_timer_tick's timer-2 branch never runs.  There is no rb2 t1icr.

A SIBLING-PARITY CENSUS MAKES IT MECHANICAL (derived from gate_arm.sh's own 194-name row list):
every operator-reachable TxICR/TxCTL cell established since pass 6 is DOUBLED at T1 --
pend2/pend1, pendn2/pendn1, ovf2/ovf1, ovfhi2/ovfhi1, rb t2icr il4 / rb t1icr il4,
rb t2ctl b27 / rb t1ctl b27, rb, rb4, rb8, op.  pendboth IS THE FIRST AND ONLY CELL THAT IS NOT.
(The T2-only hrd / hwr / acc / brd2 / rb2 rows are the GUEST path, structurally unavailable at an
odd offset -- a correctly disclosed asymmetry, not this one.)

THE REPAIR, AND IT IS CHEAP: the existing pendboth session already free-runs with both timers
armed and reads both ICRs.  Add an operator wide write at T1ICR and a readback --
put h (PCC2 + T1ICR), 0x0000 plus program([LD_BU(4, T1ICR)], at=CODE+0x400) -- as
pendboth decl1 / pendboth rb1 (both <= 15 chars, the gate's hard limit).  No new session, no
extra ~25 s.  Note that the existing pendboth decl counts DECL over the whole transcript, so it
becomes 2 -- bump it or use a separate session, and say which in the note.  Then re-measure
M_P2T1 and M_T1JOINT: both must red the new pair.

## 3.  THE MASKED OVFHI ROWS AND THEIR CONTROL

THE MASK IS & 0x81 AND THE KILL CHANNEL IS BIT 0 ALONE.  Every landed write at that arm drives
idata = 0 (OVF_REGS r9=0x0), and the body does reg &= 0xfc; reg |= (idata & 3), so ANY landed
write clears CEN.  0x81 -> 0x80, and 0x91 -> 0x90 -> masked 0x80: the row reds on bit 0 whatever
the count.  BIT 7 IN THE MASK IS DOING ARMING/LIVENESS WORK, NOT KILL WORK.  That is exactly the
tolerance the mask was for, and it exposes a fragility nothing states: IF A FUTURE EDIT CHANGES
THESE ROWS DRIVEN VALUE TO ANYTHING WITH BIT 0 SET, THE rb ROWS GO GREEN UNDER A LANDED WRITE
AND BECOME VACUOUS.

STILL KILLED UNDER THE MASK: every mutant whose landed write clears CEN -- i.e. every guard
qualifier at TxCTL true at reg == 0x81, including the shipped control && !(reg & 0xe0), and
&& !(reg & 0x80), && (reg & 0x0e) == 0, && reg != 0x11, plus the DEL / LEN / FALL shapes at that
arm.  NO LONGER KILLED: anything that changes only bits 1-6 of the ovfhi state -- principally the
EXACT VALUE of the overflow count (an oc = 1 + (reg >> 4) -> 2 + ... edit leaves bit 7 set and now
passes these rows).  THAT CLASS IS NOT LOST, because ovf1 / ovf2 remain EXACT at 0x11 and red on
any count-arithmetic change.  The contract bit-coverage claim also survives: bits 1-6 are held
by the unmasked presets {0x00, 0x03, 0x11, 0xfc}.  WHAT THE CONTRACT DOES NOT SAY AND SHOULD: the
ovfhi rows no longer pin bits 1-6, and the count exact value is pinned only by ovf*.

IS THE CONTROL THE RIGHT ONE?  Yes as far as it goes -- && !(reg & 0xe0) is true at 0x81 (bit 7),
lands the write, and reds the masked rows THROUGH the mask -- and it is honestly RE-measured
rather than transferred from part 8, which is the accept-row-failability rule correctly applied.
It is not a COMPLETE control: it exercises only the bit-0 half of the mask, and bit 7 is never
load-bearing for any mutant that lands a write.  A control for bit 7 would need a tick-side edit,
which is the job of ovf* rather than ovfhi*.  Say so.

## 4.  THE THREE PART-9 MEASUREMENTS, VERIFIED AGAINST SECTION 17

I re-read the artifacts rather than the table in the brief.  PRETABLE_pass9.out mtime 11:46:40;
part9/driver.log records the table launched 11:47:03, finished 12:30:21 -- the order witness
holds.  Each mutant driver line quotes its own first added line and a 2-line diff count.

  BASE           predicted 194/194, PCC2W_RESULT=194/194, zero FAIL lines.  CONFIRMED.
  M_PENDBOTH     predicted 192/194, measured 192/194, FAIL lines exactly pendboth decl (0 vs 1)
                 and pendboth rb (0x20 vs 0x31).  CONFIRMED; the non-red rows are explained --
                 every single-timer session has p1 && p2 false, so the conjunct never disables
                 the guard there.
  M_TXCTL_OVFHI  predicted 190/194, MEASURED 188/194: six FAIL lines -- ovfhi2 decl, ovfhi2 rb
                 (0x80), ovfhi1 decl, ovfhi1 rb (0x80), rb t2ctl b27 (0xff vs 0xfc), rb t1ctl b27
                 (0xff vs 0xfc).  The two extra reds are correct and derivable: 0xfc & 0xe0 =
                 0xe0, so the guard is off at the b27 rows too and the landed write gives
                 0xfc | 3 = 0xff.  The CHANGELOG records the miss and its cause (predicted from
                 intent, not from the part-8 red set) honestly, and I confirm the correction --
                 the part-8 red set for this mutant is the same six.

Gate 14 verified independently: gate14_p10.log (13:06:39) has GATE_RC=0, PASS (760 checks),
pcc2 width rows emitted 194 / green 194 / red 0, zero FAIL lines, and 194 UNIQUE row-name checks
(I checked the list for duplicates: none).

## 5.  THE SMALLEST EDIT THAT BREAKS THE PROPERTY AND PASSES 194 ROWS

MEASURED: && !(d->pending_timer2_interrupts && relative_addr == PCCTWO_T1ICR) -- 194/194, zero
red (M_P2T1.out).  One added conjunct, TWO operands, both body-read.

THE ROWS I EXPECTED TO STAY GREEN, AND WHY -- the ones that SHOULD have caught it are pend1 decl
and pend1 rb, the T1-label wide-write pair.  They stay green because their session arms timer 1
only, so pending_timer2 is 0 and the conjunct never fires.  pendboth decl / rb stay green because
their wide write is at T2ICR.  All 194 green, as predicted.

WHAT IT BREAKS IN THE PRODUCT: with both timers running -- the state the round itself argues is
the steady state of the device -- an operator put h halfword write to T1ICR is LANDED instead of
declined, storing the NEIGHBOUR lane into T1ICR; and because that lane has IEN clear, the body
then executes d->pending_timer1_interrupts = 0, silently discarding a pending timer interrupt.
That is precisely the defect the direction split exists to prevent, at the odd label of the arm
the round just added a row for at the even label.

THE CONTRACT SHOULD DISCLOSE BY NAME that it does not catch a TxICR guard qualifier conditioned
jointly on a pending count and the relative_addr label -- until the T1 rows land, at which point
it should say the opposite.

## 6.  IS THE RECORD HONEST?

6a.  A CLAIM OF COVERAGE NO ROW CARRIES (L4; the L2 under it is 1c and 5).  The contract says the
pending counts are held "at 0, 1, thousands, and BOTH non-zero (pendboth *)" and "BOTH non-zero
at once by pendboth *" -- with NO label qualifier, one line after the same paragraph qualifies
relative_addr BY LABEL ("the T1/T2 label: rb t1icr, op t1icr dcl, pend1 * hold the T1 value,
every T2 row the other").  Every other lvalue in that paragraph carries its T1/T2 split; the new
one does not, and I measured that the T1 half is empty.

6b.  THE ENCLOSING CODE SECTION OF THE BRIEF IS EMPTY, and this is the worst defect I found.
The heading says "the helper; the TxCTL and TxICR arms, each ONCE".  The block is TWELVE lines:
eight of helper, one blank, and two bare case labels with ZERO BODY LINES.  The real arms are 20
and 37 lines.  Worse for this pass specifically: each arm has TWO labels, and BOTH T1 LABELS
(case PCCTWO_T1CTL, case PCCTWO_T1ICR) ARE ABSENT -- so the single structural fact that makes
both measured escapes possible, that TxICR serves two case labels, is invisible in the packet.  A
packet-fed seat cannot find this defect, and cannot check the plausibility premise in 1b either.
This is a REGRESSION from pass 9, whose brief pasted the TxICR arm TWICE; the CHANGELOG records
that as corrected, and the correction overshot into the opposite failure with nothing checking it.
The remedy is the one the carrier already states: THE BRIEF BUILDER SHOULD REFUSE AT ZERO BODY
LINES for a section claiming to inline an arm, exactly as it should refuse at zero diff hunks.
(The DIFF itself IS delivered: 11 of 11 hunks, verified by regenerating part8/frozen_probe.py ->
regress/pcc2_width_probe.py and comparing hunk and plus/minus counts.)

6c.  A COUNT WITH NO DERIVER, AND IT DISCLOSES THE HOLE IT MISSES.  The pass-9 denominator reads
"seven lvalues, forty-eight single-operand predicates, ...".  Forty-eight SINGLE-operand
predicates is a sweep of the arity-1 space and says nothing about arity 2 -- which is where the
escape found by the pass-9 seat lived, and where both of mine live.  A denominator that
enumerates only the shapes it can enumerate is honest only if it says what it did NOT sweep.

6d.  THE PRE-TABLE BLOCK WAS NOT RUN FOR PASS 9.  PRETABLE_pass9.out is a Section-17 AMENDMENT:
it has none of the four mandated checks (the original PRETABLE.out does have SIBLING PARITY,
CLAIM -> ROW and GUARD FIELD vs BODY FIELD sections).  The block is MANDATORY for any round
shipping or EXTENDING a kill-table-backed detector, and pass 9 extended it 190 -> 194.  SIBLING
PARITY is precisely the check that catches this, and it costs one line.  One honest refinement:
as practised here SIBLING PARITY compares BLOCKS, and the T1/T2 labels are a WITHIN-block axis it
does not traverse -- so it needs the one-clause extension "at a shared block, the siblings are
the LABELS", which is also my 1e corollary.  The CHANNEL check would have caught it from the
other side: pendboth decl / rb name the mutant they kill (the p1-and-p2 form at T2ICR) and
nothing names the T1 mutant.

6e.  AN UNSETTLEABLE PREMISE CARRYING A LOAD-BEARING POINT -- the OpenBSD clock/statclock claim
(1c point 2).  Substitute the in-tree fact.

6f.  CORRECTLY RECORDED, AND WORTH SAYING SO: the two-row misprediction of the control and its
cause; the pass-8 header 171 -> 190; the cval() death half; the "nothing more is sent"
correction; the dissent of the pass-9 seat carried VERBATIM rather than paraphrased; and the
disclosure numstat, which matches git diff --numstat exactly, file for file.

6g.  CHECKED AND CLEAN, REPORTED BECAUSE I CHECKED IT: regress/sgi_de_primop_probe.py (20/6)
appears in the disclosure and in no narrative section.  It is the pass-16 records correction of
the sibling sgi_de round (mtime 09-03) and is not floor-bound material of this round.

## PREMISES I RE-DERIVED FROM SOMETHING THE BRIEF DID NOT GIVE ME

CONFIRMED: pcctwo_reg is uint8_t[PCC2_SIZE], so a store truncates to the big-endian high-address
lane (premise 1).  The twelve guarded blocks and their bodies match premise 4 exactly, including
"ten of the twelve read idata" -- the two that do not are SCCERR (stores constant 0) and IPL
(prints a fixed string through a function-static w).  Six EVEN blocks (0x02, 0x16, 0x1a, 0x1c,
0x1e, 0x3e) and eight ODD offsets (0x03, 0x15, 0x17, 0x1b, 0x1d, 0x1f, 0x2f, 0x3f); only SCCERR
0x1c is 4-aligned; T2COUNT 0x10 is 8-aligned (premise 2).  memory_rw.c:584-585 in the FORK (794
lines, not the 530-line pristine copy) gates the device call on
!no_exceptions || (flags & DM_READS_HAVE_NO_SIDE_EFFECTS), and DM_DEFAULT is 0 (premise 3).
PCC2_TTIRQ_INT 0x20 / IEN 0x10 / ICLR 0x08 / IL 0x07 and PCC2_TCTL_CEN 0x01 / COC 0x02 /
COVF 0x04 / OVF 0xf0 from mvme_pcctworeg.h.  d->warned is uint32_t with a COMPILE-TIME assert
that the bit count fits -- better than the plain sentence in the contract.  The assert
len(name) <= 15 in row() is EXACTLY right: the longest shipped name, brd pscale noig, is 15, and
%-16s plus the literal space in the format gives the gate pattern its two spaces; 16 would break
it.

## DENOMINATOR -- what I swept, and what I did NOT

SWEPT BY MEASUREMENT (3 probe runs x 194 rows = 582 row-observations):
* BASE, and two multi-operand guard qualifiers at the TxICR guard drawn from the read set of the
  guarded body: one PAIR (p2, relative_addr) and one TRIPLE (p1, p2, relative_addr), each aimed
  at the T1 label.  Both total escapes.

SWEPT BY READING (derived, NOT measured -- labelled as such throughout):
* the or-form and its ten predicted red rows;
* the T1/T2 sibling-parity census over all 194 gate row names (12 T1 names, 30 T2 names, the
  T2-only set identified arm by arm as the guest-path rows);
* the (p1, p2) square by two labels: seven cells closed, one open -- and the open one measured;
* the kill channel of the ovfhi mask and what it stops pinning;
* premises 1 to 4 of the brief against dev_pcc2.c, memory_rw.c, mvme_pcctworeg.h and gate_arm.sh.

NOT DONE, said plainly rather than left blank:
* I did NOT measure the or-form, any single-operand form, any TxCTL-arm mutant, any of the nine
  contract shapes, or any of the other eleven arms.  My zeros are zeros over the three runs above
  and nothing else.
* I did NOT run gate_arm.sh (instructed not to); I read its preserved log instead.
* I could NOT settle the OpenBSD clock/statclock premise -- no such source on disk.
* I did NOT re-measure the pass-9 table; I re-read its preserved artifacts and confirmed its
  scores and red sets from them.
* I did NOT review the CHANGELOG, OUTSTANDING_BUGS, ledger or panel.sh edits beyond checking that
  the numstat matches and that the sgi_de edit belongs to another round.
