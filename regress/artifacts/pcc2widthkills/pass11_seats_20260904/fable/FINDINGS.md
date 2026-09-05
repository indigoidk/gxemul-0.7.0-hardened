PASS11_FABLE_ALIVE_20260904
Liveness quote (CHECKPOINT.md): "**GATE 14 PASS (769 checks, rc 0), pcc2 203/203/0** -- `killtable2_20260903/gate14_p11.log` (16:45:20,"

# VERDICT: CLOSE -- conditional on bounding clause (d) per H1 (below) and one L4 fix.

H1 IN ONE LINE: my pass-10 rule AS WRITTEN ("cross-product of body-tested partitions")
demands all 128 cells and is therefore #392-prone (2^k in the body's if-count, compounding
across 12 arms); the FLOOR it should demand is the cross-product of {dominating predicates}
x {device-STATE lvalues the fix's own data flow makes jointly reachable} = {label}x{p1}x{p2}
= 8 cells, all rowed (over-covered by the 16); the ICLR/INT/0xe0 partitions are single-write
operands, their single-axis mutants are ALREADY caught (rb t*icr drives 0xaab8 = ICLR+0xe0+IEN;
the pend rows hold INT via reg 0x31), and their higher-order joint cells (e.g. `&& !((idata&ICLR)
&& p2)`) are reachable escapes that are correctly DISCLOSED coverage debt -- so the rule does NOT
demand rowing them. Under the LITERAL rule the verdict flips to DO NOT CLOSE (112 unrowed floor
breaches), which is exactly why the rule must be bounded.

Tree: GXEMUL-SEC, uncommitted on b78bb0f. Probe md5 6676c58d == checkpoint. Line numbers matched
the brief throughout (I was on the fork, not a 2021 copy).

================================================================================
Q1 -- ADJUDICATION (16 accepted, 3 rejected)
================================================================================
WRONG ACCEPTED DISPOSITION: **#9**.
  #9 accepted grok's objection and rewrote the docstring to
  "Bit 3 (ICLR) is inside the body's store mask (`idata & 0x17') but NO ROW holds it SET".
  This is ARITHMETICALLY FALSE. ICLR = PCC2_TTIRQ_ICLR = 0x08 (mvme_pcctworeg.h:127);
  the store mask is 0x17 = bits 0,1,2,4 (dev_pcc2.c:515-516, `reg &= ~0x17; reg |= idata & 0x17`).
  0x08 & 0x17 == 0. Bit 3 is EXCLUDED from the store mask -- which is precisely WHY register
  bit 3 is dead (reads 0 always, by construction), the SAME category as bits 6-7 that the very
  same sentence calls "set by no writer at all".
  grok's "the mask IS a writer of ICLR" conflated the COMMAND bit (idata & 0x08, which the body
  TESTS at :526/:531/:536 for the decrement and INT-clear) with the stored REGISTER bit (never
  written). The ORIGINAL sentence grok flagged -- "bit 3 set by no writer (body idata & 0x17)" --
  was CORRECT about the register bit; the "correction" made a right sentence wrong. This is the
  carrier's "a correction is not safer than the thing it corrects" pattern.
  LIVE in regress/pcc2_width_probe.py:278 and CHANGELOG.md:104. L4 (wrong record), correct in
  place; does not block close (no row/kill/score touched). Correct text: "Bit 3 (ICLR) is a
  write-only COMMAND bit: the body tests idata & 0x08 but the store mask idata & 0x17 EXCLUDES it,
  so register bit 3 is dead by construction, like bits 6-7."

The other 15 are defensible. NOTE on #7 (idata & IEN rowed "because it is a body-tested
partition"): that reasoning is the seed of the H1 inconsistency -- ICLR, INT, 0xe0 are EQUALLY
body-tested, yet disclosed. IEN was rowed because the sessions already wide-write (cheap), not by
floor necessity. The IEN rows are valid OVER-coverage; #7's stated warrant over-claims floor.

THREE REJECTIONS: all three are correct RELATIVE TO THE ADOPTED RULE.
  R1 (grok, operator-only exclusion): right -- the detector rows operator-only blocks throughout
     (pend1 is itself an operator put h at odd T1ICR); no guest-state clause exists.
  R2 (glm, 3x3 counts): right -- the body's partition is `> 0` (:528,:533), so both-thousands is
     the same cell as both-1; disclosed (finding 13).
  R3 (minimax, per-lvalue letter): right that minimax read the OLD contract wording, not clause (d).
     BUT minimax's underlying instinct -- multi-lvalue predicates risk unboundedness -- and the
     pass-9 opus5 dissent (D4, "admitting boolean combinations makes the (d) space exponential")
     were POINTING AT THE REAL DEFECT that H1 must fix. R3 is right about the rule; the rule needs
     bounding. Do not read R3's rejection as vindicating the rule's exponential form.

================================================================================
Q2 / H1 -- DOES THE RULE DEMAND THE 112? THE BOUND. OPUS vs MINE.
================================================================================
DENOMINATOR verified: TxICR write body (dev_pcc2.c:515-543) tests SEVEN binary partitions --
label(==T1/T2), idata&IEN(0x10), idata&ICLR(0x08), reg&INT(0x20), pending1>0, pending2>0,
idata&0xe0. 2^7 = 128. Correct.

DOES MY RULE DEMAND THEM? Literally, YES -- all 128. The body's own code DISTINGUISHES ICLR
(:526/:531/:536), INT (:527/:532) and 0xe0 (:539), so "the cross-product of the partitions the
body's own tests induce" includes them. The rule text even says "close the WHOLE cross-product in
ONE diff." The repair closed 16 and disclosed 112 -- a narrowing the rule's text does NOT justify.
This is a genuine defect in the rule I got adopted: 2^k in the body's if-count, compounding across
arms/devices, is the #392 shape ("finite" the way each #392 pass is finite). The pass-10 record was
right to flag this residual for pass 11.

REACHABLE ESCAPES IN THE 112 (so it is not academic): `&& !((idata & PCC2_TTIRQ_ICLR) &&
d->pending_timer2_interrupts)` exempts wide writes carrying ICLR while timer 2 is pending. NO row
realizes both: the rb rows drive 0xaab8 (ICLR set) but arm no timer; the pend rows arm timers but
drive 0x0000/0x0013 (ICLR clear). Reachable: `put h T2ICR, 0x0008` while timer2 pending. It escapes
all 203 and lands a write the fix declines. So under the LITERAL rule this is a floor breach.

THE BOUND I WOULD WRITE (finite, does not license #392, keeps the measured escapes as floor):

  "The joint-cell CLOSURE (which mutants EXIST) is the cross-product of body-tested partitions.
   The FLOOR (which cells must be rowed IN-ROUND) is the cross-product of (i) the predicates
   DOMINATING the edited guard, and (ii) the DEVICE-STATE lvalues the fix's own repair path reads
   that are JOINTLY reachable through the fix's OWN data flow (state that persists across writes and
   can be non-initial together) -- NOT the bits of the single idata being written, which are
   single-operand swaps covered as marginals. Every other joint cell is clause-(e) coverage debt:
   disclosed, ranked, and subject to the ONE ask-again. A filter over the closure may REJECT a cell
   (unreachable) or DISCHARGE it (an existing super-cell row realizes its literals); it may DEMAND a
   new row only for a floor cell -- so it cannot grow without bound."

Applied at TxICR: dominating = {label}; jointly-reachable device STATE via the fix's own data flow
= {pending1, pending2} (one pcc_timer_tick callback increments both -- dev_pcc2.c:180/389/392 --
and reassert_interrupts reads both, :278-282). FLOOR = {label}x{p1}x{p2} = 8 cells. All 8 are rowed
(the 16 rows cover them at both IEN values -- over-covered). The idata bits (IEN/ICLR/0xe0) and the
derived INT bit are single-write operands / derived state; their single-axis mutants are caught at
the marginal (rb 0xaab8; pend 0x31); their higher-order joint cells are coverage debt. => FLOOR
SATISFIED => CLOSE.

Why this is not reverse-engineered to bless 16: it says only 8 cells are floor, and it declares
IEN's rows OVER-coverage -- it does not fit the rule to the detector. It keeps the pass-9/10
MEASURED escapes (p1&&p2&&label) as floor, because those are joint DEVICE STATE the fix creates.

OPUS's form (value-classes the rows establish x dispatch axes full, demand incremental) vs mine:
  DIFFERENCE IN CONSEQUENCE AT THIS ARM: my literal form demands 128 -> DO NOT CLOSE (112 breaches).
  Opus's form is satisfied by the 16 with the rest incremental -> CLOSE.
  WHICH IS RIGHT: Opus's CONSEQUENCE (CLOSE, rest is debt) is right; my literal form over-demands.
  BUT Opus's MECHANISM is CIRCULAR for a floor -- "value-classes the ROWS establish" defines the
  floor by what you already rowed, so it can never be under-satisfied (a check that cannot fail).
  The correct floor is neither: the fix's-own-data-flow joint-STATE bound above reaches Opus's
  consequence WITHOUT the circularity and keeps the measured escapes as floor. Side with Opus in
  RESULT; reject both mechanisms; adopt the data-flow-state bound.

================================================================================
Q3 -- THE NINE READBACKS vs THE BODY
================================================================================
Preset-collision trap: PASSED. Idle ICR preset 0x11 (IEN|IL1); wide values 0x0000/0x0013.
Landed values re-derived from `reg &= ~0x17; reg |= idata & 0x17` (~0x17 = 0xe8):
  idle T1ICR(0x11)+0x0000 -> 0x00 ; idle+0x0013 -> 0x13 ; armed(0x31)+0x0000 -> 0x20 (INT survives)
  ; armed(0x31)+0x0013 -> 0x33. None equals preset 0x11 or armed 0x31 -> every landed write is
  DISTINGUISHABLE from declined. Trap correctly avoided (unlike part 6, where 0x33 collided through
  the TxCTL/TxICR masks).
DECL rows: brief premise "counts of 4" is STALE/WRONG. Rows want 1 (probe:846/864/994; BASE.out
1/1). Four wide writes share ONE TxICR latch bit -> announce once -> DECL=1. Tree already corrected
"expect 4"->"stay at 1" (CHANGELOG:56-59, crediting the pass-11 Opus seat).
Any row red for a hidden reason? No. pend1 rbi has no mutant in this table -- disclosed as a
completeness/unkilled row (PRETABLE CHANNEL line + probe note), not a hidden reason.

================================================================================
Q4 -- SIX MEASUREMENTS vs SECTION 18 (all re-derived from the body)
================================================================================
BASE 203/203 ok.
M_PENDBOTH 201/203 red rb(0x20),rbi(0x20). MISPREDICTION (safe): predicted 200 with decl red; the
  first wide write LANDS silently (zeroes p2), the SECOND declines and still announces once -> DECL=1
  -> decl GREEN -> 201. CHANGELOG records it correctly. Confirmed.
M_T1JOINT 201/203 red pendboth rb1(0x20),rb1i(0x20). Confirmed.
M_P2T1 199/203 red pend2 rb1(0x00),rb1i(0x13),pendboth rb1(0x20),rb1i(0x33). Confirmed.
M_P1XT2 201/203 red pend1 rb2(0x00),rb2i(0x13). Confirmed.
M_P2IEN 199/203 red pend2 rbi(0x33),rb1i(0x13),pendboth rbi(0x33),pendboth rb1i(0x33).
  *** prediction/brief said pendboth rb1i=0x13; ACTUAL (part10/M_P2IEN.out:152)=0x33 -- armed T1ICR
  held 0x31, 0x31&0xe8|0x13=0x33, matching the probe's OWN note. The 0x13 was pend2's IDLE-T1ICR
  value copied into the ARMED cell. Score unaffected. Tree already corrected (CHANGELOG:81); PRETABLE
  keeps 0x13 correctly as a frozen prediction. Confirmed independently from the log + body. ***
Aborted first launch (14:10): M_T1JOINT missing a paren -> would not compile -> binary-newer-than-
source check refused it (working as designed). mut_syntax.py pre-compile fix is sound.

================================================================================
Q5 -- SMALLEST EDIT THAT BREAKS AND PASSES 203
================================================================================
Single-axis idata/reg-bit mutants are all CAUGHT (rb t*icr drives 0xaab8 = ICLR+0xe0+IEN; pend rows
hold INT via reg 0x31). Smallest ESCAPING edit is a TWO-axis joint over disclosed partitions:
  if (len != 1 && writeflag == MEM_WRITE && !((idata & PCC2_TTIRQ_ICLR) && d->pending_timer2_interrupts))
Rows staying GREEN: ALL 203. No row co-occurs ICLR-in-idata with a pending count (rb rows arm no
timer; pend rows drive 0x0000/0x0013 = no ICLR). Reachable: `put h T2ICR, 0x0008` while timer2
pending. This is the H1 escape class; the contract DISCLOSES it ("outside this contract as stated")
-> clause (e), above floor -> debt, not a close-blocker. (One-token `fatal(`->`debug(` in the helper
changes only announce SEVERITY -- disclosed "NOT CAUGHT" -- but does not break the decline.)

================================================================================
Q6 -- IS THE RECORD HONEST?
================================================================================
LIVE DEFECT (one): finding-9 sentence "Bit 3 (ICLR) is inside the body's store mask (idata & 0x17)"
is refuted by 0x08 & 0x17 == 0 (ICLR is EXCLUDED). probe:278, CHANGELOG:104. L4, correct in place.
ALREADY CORRECTED (I confirm both independently): "expect 4"->"stay at 1" (CHANGELOG:56-59);
pendboth rb1i "0x13"->"0x33" (CHANGELOG:81, == M_P2IEN.out:152).
COUNTS w/ derivers: 128=2^7 (7 partitions off :515-543); 203=194+9 (gate names present); OK.
HONEST DISCLOSURES CONFIRMED: OpenBSD clock.c flagged unverified, in-tree warrant substituted;
pendboth arm1 = STICKY INT (|= at :279/:282, cleared only by ICLR :537), note says so.
BRIEF-vs-TREE: the brief's inlined CHANGELOG/PRETABLE/F2 are PRE-CORRECTION snapshots; the TREE is
the honest artifact. Q3's "counts of 4" is one such stale premise (flagged per "check the premises").

================================================================================
SOMETHING ELSE
================================================================================
- The rule's justification ("finite, a product of small partition counts") UNDERSTATES growth:
  7 binary partitions = 128, no row-demand bound -> the #392 shape. H1 bound is the fix.
- Finding #7's warrant (row IEN "because body-tested") is inconsistent with disclosing ICLR/INT/0xe0
  (equally body-tested). Harmless over-coverage; record should call IEN over-coverage once H1 lands.
