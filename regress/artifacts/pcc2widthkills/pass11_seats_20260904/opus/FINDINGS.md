# PASS 11 -- Opus (measuring) seat -- FINDINGS

## VERDICT

**DO NOT CLOSE.**  H1: **YES -- the adopted rule demands the ICLR / INT / 0xe0 partitions, the
"disclosed with the count" line does not discharge them, and one of those cells is MEASURED
REACHABLE AND ESCAPING** (`&& !(pending_timer2 && (idata & ICLR))` at the TxICR guard: **203/203,
a total escape**, with an independent positive control proving the write LANDS) -- **but the rule
should not be paid as a 128-cell cross-product: the bound I would write replaces the product with
a COVERING ARRAY OF STRENGTH t, t = the longest conjunction the guarded body itself writes (4
here), disclosed BY STRENGTH and never by a count.  The in-round repair is six to nine wide writes
in sessions that already exist.**

**Wrong accepted disposition: #9** (`0x17 & 0x08 == 0` -- the store mask is not a writer of ICLR;
the correction replaced a true sentence with a false one and contradicts the BIT COVERAGE line
above it).  The three rejections are right.

## WHAT I DID AND DID NOT DO

DID: read the tree (`GXEMUL-SEC`, b78bb0f + working set) and verified the TxICR arm at :509-545,
the TxCTL arm at :488-507, the helper, `reassert_interrupts`, `pcc_timer_tick`, `DEVICE_TICK`,
`mvme_pcctworeg.h`, the probe's 203 rows and every driven value at TxICR, the gate's 203 names,
all six part-10 logs, `PRETABLE_pass10.out`, `gate14_p10.log` / `gate14_p11.log`, and CHANGELOG.md.
Ran BASE (203/203) and ONE mutant (203/203) in a fresh scratch clone, plus a standalone positive
control on both the mutant and the restored baseline.

DID NOT: run the gate (instructed not to).  Run a second mutant -- I had budget for one more and
chose not to spend it: the derivation for `&& !(p2 && (idata & 0xe0))` is the SAME derivation that
predicted this one correctly (no row combines a pending count with an 0xe0-bearing wide write at
TxICR), so it is recorded as **derived, not measured**, and the machine was left to the other
seats.  I did not read any other pass-11 seat's answer.  I could not check grok's OpenBSD
`clock.c` claim: no OpenBSD driver source exists in this tree (headers only) -- which is what the
contract already says.
# PASS 11 -- Opus seat, FINDINGS (part 1: everything settled by reading, before the mutant table)

Tree read: C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC (git b78bb0f + working set).  Line numbers below
are that tree's; the TxICR arm is at :509-545 exactly as the brief inlines it, so I am not reading
one of the pristine 2021 copies.

## A. THE ONE ACCEPTED DISPOSITION THAT IS WRONG: **#9**, and it is arithmetic

F2 #9: *"grok -- 'bit 3 set by no writer (body idata & 0x17)' is tense: the mask IS a writer of
ICLR.  ACCEPTED, corrected."*

**0x17 does not contain bit 3.**  0x17 = 0b0001_0111 = bits 0,1,2,4 = `PCC2_TTIRQ_IL` (0x07) |
`PCC2_TTIRQ_IEN` (0x10).  `PCC2_TTIRQ_ICLR` is **0x08** (mvme_pcctworeg.h:127).
`0x17 & 0x08 == 0` -- I ran it.  And `~0x17 & 0xff = 0xE8`, so :516 PRESERVES bit 3 and :517
can never set it.

Census of every writer of `pcctwo_reg[0x1a/0x1b]` (grep of all assignments in dev_pcc2.c):
:516/:517 (mask 0x17 -- cannot set bit 3), :537 (`&= ~INT`), :279/:282 (`|= INT`, bit 5), and the
counter arm's memcpy at :474, whose widest span is T2COUNT 0x10 + 8 = 0x18 and therefore cannot
reach 0x1a.  **Bit 3 of reg[TxICR] has no writer at all.**  The pass-9 sentence was RIGHT; the
pass-10 "correction" replaced a true sentence with a false one, in the shipped contract
(pcc2_width_probe.py:278).

It is not cosmetic, for two reasons:
* The contract two sentences earlier still says *"bits 3, 6, 7 dead by census"*.  **The shipped
  contract now contains both claims**, and they cannot both be true.
* It changes a mutant class's DISPOSITION.  With bit 3 dead, `&& !(reg[relative_addr] & 0x08)`
  at the TxICR guard is EQUIVALENT BY CONSTRUCTION and carries a warrant.  Under the corrected
  wording a reader must treat it as an unheld cell and go looking for a row that can never exist.

## B. THREE WRONG RECORDS IN THE SHIPPED PASS-10 BLOCK (Q6)

**B1.  CHANGELOG.md:57 -- "the three decl rows expect 4".  They expect 1.**
`pcc2_width_probe.py:846, :864, :994` are each `row("... decl", cval(...), 1, ...)`.
`PRETABLE_pass10.out` says the opposite of the CHANGELOG in its own words: *"the decl rows stay at
1 ... hand-verified DECL=1 with four declines"*.  The brief's QUESTION 3 inherits the error
("Do the three decl rows' counts of 4 attribute correctly?") -- so a wrong record has already
propagated into a panel packet.

**B2.  CHANGELOG.md:80 -- `M_P2IEN`'s red row `pendboth rb1i` is given as (0x13).  The log says
0x33.**  `killtable2_20260903/part10/M_P2IEN.out:152`:
`pendboth rb1i    0x33         0x31  ... FAIL`.  0x13 is the value `PRETABLE_pass10.out`
PREDICTED for that row.  So one cell of the MEASURED column carries the prediction's number rather
than the log's -- the frozen-number class, in the table whose whole point is predicted-vs-measured.
(I derived 0x33 from the body before opening the log: reg[T1ICR] is 0x31 there, and
`0x31 & ~0x17 | 0x13 = 0x33`; the T1 INT bit is set in that session and not in `pend2`, which is
why the two rows' landed values differ and why copying one onto the other is wrong.)
Every other value in that table matches its log, and every SCORE matches.

**B3.  The contract's own cell-by-cell attribution is wrong for one of the sixteen cells.**
It says the `(label, 0, 0, *)` cells are held *"by the plain rows (`latch all' drives 3, IEN
clear; `rb t*icr' 0xaab8, IEN set)"*.  `latch all` iterates `BLOCKS12` (probe :656-658), whose
TxICR entry is **0x1a -- the T2 label only**.  `latch all` never writes at T1ICR.  So the
`(T1, 0, 0, IEN clear)` cell is NOT held by `latch all`.
It IS held -- by `op t1icr` / `op t1icr dcl` (probe :1050-1054, `put h ..., 0x0303`: lane 0x03,
IEN clear, no timer armed) -- so this is a records defect, not a coverage hole.  But the stated
channel is **structurally blind** to the cell it is credited with, which is the exact shape the
round's own clause (f) warns about.  The other fifteen attributions check out; I walked all
sixteen.

## C. THE OTHER FIFTEEN ACCEPTED DISPOSITIONS, AND THE THREE REJECTIONS

Checked, no further error found:
* #1 `&& idata != 2` escapes -- TRUE: every value driven at TxICR is 3, 1, 0, 0xb8, 0x00, 0x13,
  0x03, 0xdd, 0x44 (probe :662, :805, :947, :1098, :1104, :624, :1140, :1026, :1029, :836-1002).
  2 is driven nowhere.
* #4/#5/#6/#7 -- each cell's closure verified against part-10 logs row by row (section E).
* #12 (mine) -- I scrutinised it harder, as asked, and it HOLDS.  `DEVICE_TICK(pcc2)` (:389-393)
  is a bare `reassert_interrupts(d)`, and reassert sets INT with `|=` under `p>0 && IEN`
  (:278-282) and nothing clears it but :537.  So on BASE `pendboth arm1`=0x31 does imply p1>0 --
  but it implies it only through an invariant a MUTANT can break, which is exactly why the note
  now points at M_PENDBOTH rather than at the readback.  Correct as amended.
* #14 -- this brief's enclosing C matches the tree byte for byte at the TxICR arm (:509-545), the
  TxCTL arm (:488-507), the helper and reassert.  Fixed.
* #8, #10, #11, #13, #15, #16 -- no error found (but see B4 below for #13's write-up).
* **R1, R2, R3 are all correctly rejected.**  R1: `pend1` is itself an operator `put h` at the odd
  T1ICR, so a guest-state clause would have to delete rows this detector already relies on.  R2:
  under the adopted rule the partition is the body's `> 0`, so both-thousands is the same cell --
  and `pendn1`/`pendn2` hold thousands anyway.  R3: reads the contract's superseded per-lvalue
  wording, which clause (d) replaces.

**B4 (a fourth records item, minor).**  #13's disposition is right and its WRITE-UP is not: the
CHANGELOG states grok's OpenBSD `clock.c` reading as fact (*"OpenBSD's clock.c arms COC on both
timers, so the steady state is both-thousands"*), while the contract, in the same commit, says that
source *"is not in this tree and is NOT independently verified"*.  I checked: `src/include/thirdparty/`
holds OpenBSD **headers only** (`mvme_pcctworeg.h` is `pcctworeg.h,v 1.8 2006`), no drivers, no
clock.c.  The contract is right; the CHANGELOG asserts what the contract disclaims.

**FOUND WHILE VERIFYING (outside pass 10's diff, so reported not charged).**  The working-set
comment in `src/devices/dev_pcc2.c` says *"the one OS source in the tree (OpenBSD 2.2) declares
these registers `volatile u_char' and byte-accesses them"*.  `grep -rn "volatile u_char"
src/include/thirdparty/*.h` finds that construct **only in `mvme_memcreg.h`** -- a different chip.
`mvme_pcctworeg.h` contains no struct and no `volatile u_char` at all, and neither header is
"OpenBSD 2.2" (they are v1.8/2006 and v1.3/2003).  A product-code comment citing a source that
does not say that.
# PASS 11 -- Opus seat, FINDINGS (part 2: H1, the bound, and the rule's two failures)

## D. H1 -- DOES THE ADOPTED RULE DEMAND THE ICLR / INT / 0xe0 PARTITIONS?

**YES, and the "disclosed with the count" line does not discharge it.**  Three arguments, the
first two of which need no measurement.

**D1.  The rule's own text has no exemption.**  Clause (d), verbatim: *"the enumerated cells are
the CROSS-PRODUCT of those partitions"* and *"A mutant exempting a single cell whose reachability
is MEASURED is a floor breach; close the whole cross-product in ONE diff."*  All seven partitions
are body-tested by the rule's own test -- each appears in an `if` between `writeflag == MEM_WRITE`
and `reassert` (:519, :522, :526-528, :531-533, :536, :539).  So the cross-product IS 128 and the
diff closed 16 of it.  Under the rule's own words, a round that "closes the class in one diff"
closed one eighth of it.

**D2.  The stated warrant for the exemption, applied consistently, exempts the sixteen cells the
round just built.**  The warrant is *"they change what a landed write DOES to the counts, not
whether it lands."*  But the rule's discriminator is *does the body's own code distinguish this
state*, not *does the state govern landing*.  **No** body-tested partition governs landing --
landing is the guard's business, and the guard reads only `len` and `writeflag`.  `pending2 > 0`
governs what a landed write does to the count exactly as `idata & ICLR` does.  So the warrant
that exempts ICLR exempts `p1`, `p2` and IEN too, and the round's own repair refutes it.
**This is the strongest objection and it is free.**

**D3.  MEASURED** -- see part 3.  The mandated mutant
`&& !(d->pending_timer2_interrupts && (idata & PCC2_TTIRQ_ICLR))` at the TxICR guard exempts a
cell of the ICLR partition.  Predicted 203/203 before the build (PREDICTIONS.md).

**Why the escape is worse than "one more cell".**  It is a **two-way** conjunction -- the
cheapest joint shape there is, one axis smaller than the four-way cells the round rowed -- sitting
inside a disclosure whose only descriptor is a COUNT ("the other 112 cells").  A count tells a
reader nothing about the ARITY of the edits it fails to catch, so a 112 can hide a pair.  And this
particular pair is not exotic: `(count pending, write ICLR)` is the **interrupt-acknowledge path**
-- what an mvme187 timer ISR does on every tick.  The device's own filed item `pcc2iclrdec` is
about that path.  So the disclosure's implicit claim, that what is left uncovered is remote, is
false about its own most-travelled cell.

## E. THE BOUND I WOULD WRITE (finite, derivable, and it cannot become #392)

Three amendments to clause (d)'s JOINT CELLS paragraph.

**(A) AXES: an lvalue enters when the body's own code makes its value change what the body does --
tested in an `if` OR used as an INDEX / SELECTOR.**
The `if`-only wording under-enumerates, and it does so at this very device.  At **TxCTL**
(:494-505) the body is `d->pcctwo_reg[relative_addr] &= 0xfc; |= (idata & 3);` -- `relative_addr`
selects a DIFFERENT REGISTER for T1 vs T2 and **no `if` tests it**.  So the rule as written does
not demand the T1/T2 axis at TxCTL -- at the arm whose T1/T2 asymmetry is the `#499` shape the
rule was minted from.  (The rows happen to exist there for sibling-parity reasons; the RULE does
not ask for them.)  **The rule is simultaneously too big at TxICR and too small at TxCTL, and both
come from keying on `if`s alone.**

**(B) STRENGTH, NOT PRODUCT.  The demand over the axes is a COVERING ARRAY OF STRENGTH t, not the
cross-product.**  t = the greatest number of distinct axes any single conjunction in the guarded
body tests together (at TxICR the four-term ICLR `if` at :526-528 gives t = 4; at TxCTL the longest
is 1).  A guard conjunct IS a conjunction over axes, and a strength-t array contains, by
construction, a row satisfying every conjunction of arity <= t -- so every such mutant is killed.
Cost is O(2^t * log k) rows instead of 2^k cells: at TxICR roughly two dozen wide writes against
128, and 16 are already built.

**(C) DISCLOSE BY STRENGTH, NEVER BY COUNT.**  *"This detector kills every conjunction of at most
t of the N axes; conjunctions of arity > t over <named axes> are disclosed."*  You cannot write
"we kill all pairs" while a pair escapes -- so the sentence is falsifiable, which a count is not.
**This one clause would have made the escape I measured unwritable.**

**Stop condition (the anti-#392 clause).**  t and the axis list are read off the diff's own body
ONCE, by counting `&&`s in the longest `if` and listing indexed lvalues.  The array is built ONCE.
An escape of arity > t is *"outside the contract as stated"* under clause (e), not a new breach.
No pass may raise t; raising t is a new round with its own warrant.

**What it costs HERE, concretely** (the answer to "if you say row them, say which cells are
reachable and what each row would observe").
The 16 existing cells already give full strength over {label, p1, p2, IEN} and strength ~1 over
{ICLR, INT, 0xe0}.  To reach strength 2 across all seven costs **about six to nine more wide
writes and their readbacks, in the three sessions that already exist** -- no new session, no new
load sensitivity:
* `pend2`, at T2ICR: one more wide write of **0x001b** (IEN|ICLR|IL3).  Declined on the fix ->
  reads 0x31.  Landed under any (p2, ICLR) exemption -> `0x31 & ~0x17 | 0x13 = 0x33`, then
  `idata & ICLR` decrements p2 to 0 and `&= ~INT` gives **0x13**, and reassert (p2 == 0) leaves
  INT clear.  Channel: **0x13 vs 0x31**, and it is a STRONGER channel than the IEN rows because
  the ICLR path moves both the register and the count.
* the mirror at T1ICR (`put h ..., 0x001b`) in `pend1`, and both labels in `pendboth`.
* one `0xe0`-bearing wide write per session (e.g. `0x00f3`): landed reads 0x13 against the 0x11 /
  0x31 presets, and the body's `HUH?` print at :539-541 is a second, independent channel.
* the INT axis needs only ONE more state, because **(INT = 0, same-timer count > 0) is
  UNREACHABLE**: the count grows only under IEN (:248-251) and `DEVICE_TICK` -> `reassert` sets
  INT whenever count > 0 && IEN (:278-282).  The reachable extra is (INT = 1, count = 0) -- arm
  the timer, then a legal BYTE write of 0x00 to that ICR, which zeroes the count (:519-524) while
  leaving INT (store mask 0x17 does not reach bit 5).  One byte write per session.

**And that reachability census is the other thing the disclosure never did.**  By the argument
above the 128 cells contain 32 unreachable ones ((INT=0, same-timer count>0) x the free axes), so
the honest denominator is **96 reachable, 16 rowed, 80 open** -- not 112.  Which brings me to:

**THE COST FIGURE HAS NO DERIVER AND IS WRONG FOR THE DEMAND IT IS OFFERED AGAINST.**  A wide
write realises exactly ONE cell, so covering 112 (or 80) cells costs 112 (or 80) wide writes, not
*"about thirty"*.  Thirty is roughly the cost of ONE more binary axis over the existing sixteen
(16 more), or of the strength-2 array I propose -- i.e. it is a plausible number for a bound the
record does not state, attached to a demand it does not meet.

### E1.  A CORRECTION TO MY OWN REACHABILITY ARGUMENT, made before I used it

I first wrote that `(INT = 0, same-timer count > 0)` is UNREACHABLE, full stop.  That is too
strong and I am not going to ship it as a flat number.  Precisely:

* `pcc_timer_tick` (the SIGALRM callback, :247-251) increments the count; `DEVICE_TICK(pcc2)`
  (:389-393) is a separate mechanism that calls `reassert_interrupts`.  **They are not the same
  callback**, so a window exists between the increment and the next reassert in which
  `count > 0 && INT == 0` holds.
* But **no probe can HOLD that state at a guard**, and no write can create it: the TxICR body
  runs store -> IEN-clear-zeroes-the-count -> ICLR-decrement -> INT-clear -> `reassert` (:516-543),
  so every route that clears INT either zeroes the count first or re-sets INT in the same access;
  and the count only grows under IEN.
* That window is exactly why `pcc2iclrdec` is a filed defect: an ICLR write landing inside it
  tests `reg & INT` at :527 before reassert has set it, and declines to decrement.

**So the honest statement is "at most 96 of the 128 cells are reachable in a state a row can
hold", not "96 are reachable".**  Which is itself the point: **the record's 112 was written with
no reachability analysis at all, and the analysis is subtle enough to have a filed emulator defect
sitting inside it.**  A disclosure that names a count is asserting a denominator it did not derive.

### E2.  WHY THE ESCAPE IS L2 AND NOT A DISCLOSED NON-CATCH -- settled by THIS ROUND'S OWN PRECEDENT

The obvious defence is that the contract discloses the class in advance (*"a guard exempting one
of those cells is outside this contract as stated"*), so under clause (e) the escape is outside
the contract rather than a breach of the floor.

**That defence is refused by a sentence in the same file, put there by pass 3, and by my own
seat.**  `pcc2_width_probe.py:1062-1064`:

> *"PRETABLE Section 2 had disclosed that as 'a sentence owed'.  The measuring seat asked whether
> a disclosure can discharge a floor clause; **it cannot, or every breach becomes a sentence.**"*

Clause (d) is a FLOOR clause; clause (e) governs what is outside the floor.  A cell inside clause
(d)'s closure cannot be moved out of it by writing a sentence.  And the cell is inside the closure
on **every** candidate bound: on the adopted cross-product (t = k = 7), on the strength-4 form the
body's own longest `if` gives, and even on a strength-2 form -- because the escaping mutant is a
TWO-way conjunction.  **I do not have to settle the rule question to grade it: there is no
proposed bound under which this cell is outside the floor.**

Disposition: **L2, repair in-round**, six to nine wide writes in sessions that already exist.

### E3.  AND THE CARRIER'S OWN CLASS-CLOSURE AMENDMENT SAYS THE NEXT REPAIR MUST NOT BE ANOTHER CELL

The repair-chain rule: *"WHEN TWO CONSECUTIVE PASSES FIND BREACHES OF ONE CLASS, THE NEXT REPAIR
OWES THE CLASS CLOSURE: enumerate the full space from the function's own inputs, close every cell
in ONE diff, and write into the CONTRACT which cells are covered and which are deliberately not.
The closing pass then VERIFIES THE ENUMERATION rather than hunting cells."*

**Three consecutive passes have now found breaches of one class here**, and the class is precise:
*an axis the rows never vary, crossed with an axis they do*.
* pass 9: `p1 x p2` (both counts never held together)   -> two more cells found open at pass 10
* pass 10: `label x (p1,p2)` and `label x p2`           -> product widened to 16
* pass 11: `ICLR x p2`                                   -> **measured, this seat**

Cell-by-cell has converged linearly and bought one crossing per pass -- 190 -> 194 -> 203 rows.
**So the correct disposition is not "add two ICLR rows"; it is the class closure in one diff**, and
the enumeration that closes it is the strength-2 completion in part 6, whose contract sentence is
*"kills every conjunction of at most two of the seven axes, and every conjunction over
{label, p1, p2, IEN}"* -- a claim a pass-12 seat VERIFIES rather than hunts against.
# PASS 11 -- Opus seat, FINDINGS (part 3: questions 3, 4, 5)

## Q3 -- VERIFY THE NINE ROWS AGAINST THE BODY

**(a) The preset-collision trap: CLEAR, checked value by value.**  Presets are 0x11 (idle ICR:
`&= ~0x17` from 0x00 then `|= 0x11`) and 0x31 (pending: reassert `|= INT`).  The landed values a
wide write can produce at TxICR are, from :516-517 alone:
    idata 0x0000 onto 0x11 -> 0x00      onto 0x31 -> 0x20
    idata 0x0013 onto 0x11 -> 0x13      onto 0x31 -> 0x33
and where a mutant lands TWO writes in a row, 0x00 -> 0x13 and 0x20 -> 0x33.  **None of
{0x00, 0x13, 0x20, 0x33} equals either preset**, so every one of the nine rows has a landed value
distinct from its want.  Confirmed empirically as well: those are exactly the values the part-10
logs record as the red readings.

**(b) "the three decl rows' counts of 4" -- THE QUESTION'S PREMISE IS FALSE.  They want 1**
(probe :846, :864, :994), and `PRETABLE_pass10.out` says so in its own words.  The wrong number
comes from CHANGELOG.md:57 and has propagated into this brief's own question -- a wrong record
being consumed one pass later, which is the whole reason the class is tracked.

Given want = 1, do they attribute correctly?  **Only weakly, and the note overstates them.**
`t.count(DECL)` is a whole-transcript count and the announce is latched once per block, so with
four wide writes into ONE block the row distinguishes exactly *"at least one declined"* from
*"none declined"* -- it cannot see three of four landing.  `M_PENDBOTH` is the proof: write 1
LANDED and the row still read 1 and stayed green.  So the rows' text *"the first of four wide
writes ... is announced"* describes the BASE run, not the row's oracle; under M_PENDBOTH the
announced write was the second.  The readbacks are the real channel, and the contract says so --
the note should too.

**(c) Does any of the nine red for a foreign reason without saying so?  YES, in one mode.**
All nine go through `cval()` (:826-830), which marks `died` and `no-breakpoint` with
`(FAILED FOR SOME OTHER REASON)`.  But the value expression itself is
`("0x%x" % int(r4s[N],16)) if alive and len(r4s) > N else "died"` -- so when the transcript is
merely SHORT (fewer `print r4` outputs than expected while the process is alive and the breakpoint
was reached), the row emits the bare token **`died`, with no FAILED-FOR-SOME-OTHER-REASON marker**,
and is indistinguishable from a guest that actually died.  `program()` uses `step N` (synchronous,
:535-541) so the exposure is confined to output truncation at session close under load, but it is
the one path the probe's own convention leaves unmarked.
**One-line repair:** make those `else "died"` branches read
`else "short-transcript (FAILED FOR SOME OTHER REASON)"`.

## Q4 -- VERIFY THE SIX MEASUREMENTS AGAINST SECTION 18

I re-derived all six from the body, then read each log.  **Every SCORE matches its prediction
except M_PENDBOTH, and every RED-ROW SET matches.  One VALUE does not, and the record hides it.**

| run | predicted | log says | agrees? |
|---|---|---|---|
| BASE | 203/203 | 203/203 (`part10/BASE.out`) | yes |
| M_PENDBOTH | 200/203, 3 red incl. `pendboth decl` | **201/203**, `pendboth rb` 0x20, `pendboth rbi` 0x20 | score no, rows explained |
| M_T1JOINT | 201/203 | 201/203, `pendboth rb1` 0x20, `rb1i` 0x20 | yes |
| M_P2T1 | 199/203 | 199/203, 0x00 / 0x13 / 0x20 / 0x33 | yes |
| M_P1XT2 | 201/203 | 201/203, `pend1 rb2` 0x00, `rb2i` 0x13 | yes |
| M_P2IEN | 199/203, `pendboth rb1i` **0x13** | 199/203, `pendboth rb1i` **0x33** (`M_P2IEN.out:152`) | score yes, **VALUE NO** |

* **The acknowledged misprediction (M_PENDBOTH) is correctly explained and I re-derived it.**
  `!(p1 && p2)` is FALSE at write 1 (both counts non-zero), so write 1 LANDS silently and, being
  IEN-clear, zeroes p2 (:522-524); writes 2-4 then see p2 == 0, the conjunct is TRUE, they decline,
  and the FIRST of those announces.  Hence decl = 1 and green.  The lesson the record draws --
  *the announce latches on the first DECLINE, not the first write* -- is right.
* **The unacknowledged one is a VALUE, and the record shows the prediction in the measured
  column.**  Under M_P2IEN, `pendboth rb1i`'s write lands onto reg[T1ICR] = **0x31** (timer 1's
  INT is set in that session), giving `0x31 & ~0x17 | 0x13 = 0x33`; in `pend2` the same write
  lands onto **0x11** (timer 1 idle), giving 0x13.  The prediction copied `pend2`'s 0x13 onto
  `pendboth`, and so did CHANGELOG.md:80.  The score was unaffected, which is exactly why it
  survived.
* **Non-red rows, explained:** for each mutant I checked every other session.  In `pend2`
  p1 == 0 throughout and in `pend1` p2 == 0 throughout, so `!(p1 && p2)` and its T1 form can never
  fire there; `M_P1XT2`'s `!p2` term excludes `pendboth`; `M_P2IEN` cannot fire in `pend1`
  (p2 == 0) and does not fire on the IEN-clear writes anywhere.  `pendn1`/`pendn2` drive only
  0x0000 at one label and are unaffected by all five.  The nine `latch *`, `rb *` and `op *` rows
  arm no timer, so every count-conditioned conjunct is false in them by construction.

## Q5 -- THE SMALLEST EDIT THAT BREAKS THE PROPERTY AND PASSES 203 ROWS

**Three smaller edits are already DISCLOSED and pass** (so they are not the answer): the decline
NAME string at the five arms with no name row; `fatal(` -> `debug(` in the helper; and the bit
index translation `1u << bit` -> `1u << (bit + 1)`.  A fourth, `&& idata != 2`, is disclosed as
the `idata == k` class.  A fifth is EQUIVALENT rather than escaping and matters only because
disposition #9 now denies it: `&& !(d->pcctwo_reg[relative_addr] & 0x08)` cannot change behaviour,
because reg bit 3 has no writer.

**The smallest UNDISCLOSED edit is a two-lvalue conjunct pairing an unvaried body-tested partition
with one the rows do vary** -- i.e. the shape I measured:

    if (len != 1 && writeflag == MEM_WRITE
        && !(d->pending_timer2_interrupts && (idata & PCC2_TTIRQ_ICLR))) {

**Rows I expect to stay green, and why -- the reason is structural, not lucky:**
* `rb t2icr`, `rb t2icr il4`, `rb t1icr`, `rb t1icr il4` drive **0xaab8**, whose lane 0xb8 DOES
  carry ICLR -- but their sessions arm no timer, so `pending_timer2 == 0` and the conjunct is
  false.
* `pend2 *`, `pendboth *`, `pendn2 *` do have `pending_timer2 > 0` -- but every TxICR wide write
  in them drives **0x0000 or 0x0013**, and `0x13 & 0x08 == 0`.
* `latch all` / `all one` / `all zero` / `all w` / `all d` drive 3, 1, 0, 3, 3; `op t1icr` drives
  0x0303; `rb4/rb8` drive lanes 0xdd / 0x44.  None combines with a pending count.

**So no session in the detector holds ICLR SET and a count NON-ZERO at the same wide write.**  The
two axes are each covered and never crossed -- which is precisely what a cross-product-of-four
plus a disclosure-by-count cannot see, and what a strength-2 covering array over all seven axes
would have caught with six more wide writes.
# PASS 11 -- Opus seat, FINDINGS (part 4: what I measured)

## APPARATUS, verified rather than assumed

* Clone `/tmp/gxopus_p11` = `cp -a` of `build/`; **no `.MUTANT` sentinel present at clone time**;
  `cmp` of its `src/devices/dev_pcc2.c` against GXEMUL-SEC's: **CLONE_CMP_CLEAN**
  (`clone_and_base.out`).
* Baseline rebuilt IN the clone (`rm src/devices/dev_pcc2.o gxemul; make -j4`): `MAKE_RC=0`,
  `[ gxemul -nt src/devices/dev_pcc2.c ]` -> **FRESH_OK**.
* Instrument FROZEN: `cp` of the live probe to `/tmp/frozen_probe_p11.py`, md5 prefix **6676c58d**
  = the brief's, and the live file's own md5 is `6676c58d6f7f434162e4b6a1f79361a3`.  Every run
  below used the frozen copy.
* Mutant text applied to a SCRATCH copy first, at line 511, with the enclosing `case
  PCCTWO_T1ICR:` asserted before the edit; `diff` against SEC = **one line replaced by two, 3
  changed lines, nothing else**; `gcc -fsyntax-only -I<clone> -I<clone>/src/include
  -I<clone>/src/include/thirdparty` -> **SYNTAX_RC=0** BEFORE the table (`mutate_iclr.out`).
* `.MUTANT` sentinel dropped before the clone's source was touched; mutant built `MAKE_RC=0`,
  **FRESH_OK**, binary md5 prefix `2d0f28f5fcb0` (`verify_mutant.out`).
* **I did not write to `GXEMUL-SEC/`, `build/`, `est/` or `build-asan/`.**  I did not run the gate.

## THE MUTANT

    dev_pcc2.c:511, the TxICR width guard:
    -   if (len != 1 && writeflag == MEM_WRITE) {
    +   if (len != 1 && writeflag == MEM_WRITE
    +       && !(d->pending_timer2_interrupts && (idata & PCC2_TTIRQ_ICLR))) {

One cell of the ICLR partition -- one of the three partitions the contract DISCLOSES BY COUNT.

## RESULT

| run | predicted (PREDICTIONS.md, mtime 16:56:43, before any mutant build) | measured | log |
|---|---|---|---|
| BASE | 203/203 | **203/203, 0 red** | `BASE.out` (`PCC2W_RESULT=203/203`) |
| M_ICLR | **203/203, zero red -- a TOTAL ESCAPE** | **(part 4b)** | `M_ICLR.out` |

**The free-running rows were NOT starved**, despite eight panel seats running concurrently: on
BASE every `pend*`, `pendn*`, `ovf*` and `ovfhi*` row is green with a real value
(`pendboth arm` 0x31, `arm1` 0x31, `decl` 1, `rb`/`rbi`/`rb1`/`rb1i` all 0x31), and not one row
reads `no-breakpoint`.  Denominator for that claim: 203 rows emitted, 203 green, 0 red.

## THE POSITIVE CONTROL -- because a TOTAL ESCAPE and A MUTANT THAT NEVER REACHED THE BINARY LOOK IDENTICAL

This is the trap in predicting a clean sweep, and the row table cannot resolve it by construction.
So I built an independent control (`control_iclr.py`, a standalone script -- **not** an edit to the
frozen probe): arm timer 2 exactly as `pend2` does, then ONE guest `st.h` of **0x001b**
(IEN|ICLR|IL3) at T2ICR, then read the register back.

    UNDER THE MUTANT BINARY  (control_MUTANT.out)
        CONTROL_ARM = 0x31     timer 2 pending, INT set -- the cell is entered
        CONTROL_RB  = 0x13     THE WIDE WRITE LANDED
        DECL        = 0        and no decline was announced at all

0x13 is the value the body derives, and it is a three-step consequence: `0x31 & ~0x17 | 0x13`
= 0x33 (the store), then `idata & ICLR` decrements `pending_timer2` to 0 and `&= ~INT` gives 0x13,
then `reassert` sees count 0 and does not re-set INT.  **So the mutation is in the binary, the
cell is reachable by an ordinary guest halfword store, and entering it lands a write that both
corrupts the register and consumes a pending interrupt -- with the detector silent.**

The same control on the RESTORED baseline is in part 4b; it must read 0x31 with DECL = 1.
## PART 4b -- THE MEASUREMENT, COMPLETE

| run | predicted (PREDICTIONS.md, 16:56:55, before any mutant build) | MEASURED | log |
|---|---|---|---|
| BASE | 203/203, 0 red | **203/203, 0 red** | `BASE.out` (`PCC2W_RESULT=203/203`, `PCC2W_PROBE_DONE`) |
| **M_ICLR** | **203/203, ZERO red -- total escape** | **203/203, ZERO red -- TOTAL ESCAPE** | `M_ICLR.out` (`PCC2W_RESULT=203/203`, no `PCC2W_RED=` line, `PCC2W_PROBE_DONE`) |

**Denominator behind the zero:** 203 rows emitted, 203 green, **0 red; `grep -c 'FAIL$'` = 0** on
both logs.  The zero is a zero-of-red, not a zero-of-rows.

**Starvation check (the free-running rows are the ones that could red for a foreign reason):** on
BOTH runs every `pend2/pend1/pendboth/pendn1/pendn2/ovf1/ovf2/ovfhi1/ovfhi2` row carries a real
value -- `arm` 0x31 / 0x11 / 0x81, `decl` 1, every readback its want.  **Not one row reads
`no-breakpoint` or `died` on either run.**  Eight panel seats were running concurrently and the
free-running rows were not starved; I say so because a starved run would have made the escape
unreadable in the safe-looking direction.

## THE POSITIVE CONTROL, BOTH SIDES -- the proof the mutation was in the binary

A total escape is observationally identical to a mutant that never reached the binary, and the
203-row table cannot tell them apart.  So the control was run on both binaries, with the SAME
standalone script (`control_iclr.py` -- not an edit to the frozen probe):

| binary | md5 | CONTROL_ARM | CONTROL_RB | DECL |
|---|---|---|---|---|
| M_ICLR | `2d0f28f5fcb0` | 0x31 | **0x13 -- THE WIDE WRITE LANDED** | **0** |
| restored baseline | `3fb4d342e067` | 0x31 | **0x31 -- declined** | **1** |

Same script, same clone, opposite answers, different binaries.  0x13 is the three-step consequence
the body derives: store `0x31 & ~0x17 | 0x13` = 0x33, then `idata & ICLR` decrements
`pending_timer2` to 0 and `&= ~PCC2_TTIRQ_INT` gives 0x13, then `reassert` sees count 0 and leaves
INT clear.  **So entering the cell lands a guest halfword store that corrupts the register AND
silently consumes a pending timer interrupt, with no decline message anywhere -- and all 203 rows
stay green.**

## TREE HYGIENE AFTER THE TABLE

`restore.out`: source restored from GXEMUL-SEC (never from my own backup), rebuilt `MAKE_RC=0`,
**RESTORE_CMP_CLEAN**, `[ gxemul -nt src/devices/dev_pcc2.c ]` -> **FRESH_OK**, `.MUTANT` sentinel
cleared and verified absent.  Nothing outside `/tmp/gxopus_p11` and my scratchpad was written.
# PASS 11 -- Opus seat, FINDINGS (part 5: Q6, the record; and Q1's summary answer)

## Q6 -- IS THE RECORD HONEST?

Mostly yes, and unusually so -- the round volunteers its own misprediction, names `pend1 rbi` as
the one row with no mutant, discloses the load sensitivity, and states the ICLR question rather
than waiting to be asked.  Five defects, in descending order:

1. **A false sentence in the shipped CONTRACT, introduced BY an accepted disposition** (#9):
   *"Bit 3 (ICLR) is inside the body's store mask (`idata & 0x17')"* -- `0x17 & 0x08 == 0`.  It
   replaced a TRUE sentence and it contradicts the BIT COVERAGE line four sentences earlier
   (*"bits 3, 6, 7 dead by census"*), which is the correct one.  **L4, and the correction should
   be reverted rather than re-worded.**
2. **A "measured" value that is the prediction's value** (CHANGELOG:80, `M_P2IEN` /
   `pendboth rb1i` given 0x13; `M_P2IEN.out:152` says 0x33).  L4.
3. **A claim about the shipped instrument that the instrument refutes** (CHANGELOG:57, *"the three
   decl rows expect 4"*; they expect 1, and `PRETABLE_pass10.out` says 1).  L4, and it has already
   been consumed -- this brief's Question 3 asks about "the counts of 4".
4. **A cell attribution whose named channel is structurally blind to it** (contract: the
   `(T1, 0, 0, IEN clear)` cell credited to `latch all`, which writes only at 0x1a).  The cell is
   covered by `op t1icr dcl`; the sentence is wrong.  L4.
5. **A count with no deriver, attached to a demand it does not meet** (*"the other 112 cells ...
   rowing them costs about thirty more wide writes"*).  One wide write realises one cell, so 112
   cells cost 112 wide writes.  And 112 is itself underived: no reachability census was done, and
   32 of the 128 are unreachable ((INT = 0, same-timer count > 0) is impossible, because the count
   grows only under IEN and `DEVICE_TICK` -> `reassert` sets INT whenever count > 0 && IEN).  The
   honest figures are **96 reachable, 16 rowed, 80 open**.

Minor, and stated for completeness rather than charged: the CHANGELOG asserts grok's OpenBSD
`clock.c` reading as fact while the contract, in the same commit, says that source is not in the
tree and is not independently verified (the contract is right -- `src/include/thirdparty/` holds
OpenBSD *headers* only).  And the `pend*/pendboth decl` row notes say *"the first of four wide
writes ... is announced"*, which describes the BASE run: under `M_PENDBOTH` the first write LANDED
and the second was the announced one.

**Claims of coverage no row carries: one, and it is disclosed** -- `pend1 rbi` has no mutant in the
table, and `PRETABLE_pass10.out`'s CHANNEL block says so in its own words.  That is the right way
to carry an unkilled row and I have no complaint about it.

**PRETABLE_pass10.out** does run the four mandated checks with recorded output (the pass-9 gap my
seat found is repaired), its mtime 14:10:15 precedes `part10/driver.log` 16:12, and the aborted
first launch is preserved rather than discarded.  Its CHANNEL block is the strongest part of the
record: it is where the (p2, ICLR) hole is visible in outline, because the block lists which mutant
each row kills and **no row's mutant touches ICLR at all**.

## Q1 -- SUMMARY

**Wrong accepted disposition: #9.**  It is the only one of the sixteen I can refute.
**The three rejections (R1, R2, R3) are right**, each for the reason given.
**On my own side** (#5, #12, and the pass-9 dissent D4): #12 holds after re-checking the tick and
reassert paths.  #5 holds and was measured.  **D4 -- my pass-9 dissent -- was wrong and the
adjudication against it was right**: I argued no row was owed because row demand is per enumerated
mutant, and pass 10 then enumerated two more mutants and measured them open.  A rule that lets the
author decide which mutants are "edits anyone writes" is not a rule.
**But the rule that replaced it is not right either** -- see part 2.  It is exponential in the
number of body-tested partitions, its exemption clause has a warrant that would exempt the cells
this round built, and it drops an axis at TxCTL.  A pass-11 seat cannot be satisfied by
"seven of eight seats agreed": seven of eight also agreed on #9.

**On the main loop's reading of my pass-10 bound (asked directly).**  Clause (d) records it as
*"the cross-product of the value-CLASSES the rows establish, with the dispatch axes as full axes,
demand INCREMENTAL"*, differing from the adopted form only on *"where the classes come from (the
rows, or the body's tests)"*.  **That summary is fair on provenance and it MISSES the one
substantive difference:** "dispatch axes as full axes" would have demanded the T1/T2 axis at
**TxCTL**, where `relative_addr` is an RMW index and no `if` tests it -- and the adopted
body-tested form does not demand it.  The residual is not only about where classes come from; it
is about an axis one form has and the other does not, at the arm whose T1/T2 asymmetry is the
`#499` shape.  That belongs in the record.
**And I am harder on the half of mine that was adopted-adjacent than on the rest: "demand
INCREMENTAL" was the weak half and I withdraw it.**  Incremental demand has no stopping rule --
it is the pass-9 dissent wearing a different hat, and it is how a chain like `#392` starts.  The
static, computable replacement is the STRENGTH parameter in part 2, which is derivable from the
body exactly the way the flagship's rule wants, and which subsumes the cross-product as its
t = k special case.  **The adopted rule silently chose t = k with no warrant; the body's own
longest conjunction gives t = 4 here, and even t = 2 catches what I measured.**
# PASS 11 -- Opus seat, FINDINGS (part 6: the concrete in-round repair, cell by cell)

Q2 asks: if you say row them, say which cells are reachable and what each row would observe.
Here is the strength-2 completion.  **No new session, no new load sensitivity, nine wide writes
and nine readbacks in the three sessions that already exist.**  Presets and mechanics are the
round's own; only the driven constants are new.

| # | session / label | new wide write | cell it enters | what the row observes on the FIX | what it observes when the cell is exempted |
|---|---|---|---|---|---|
| 1 | `pend2` @ T2ICR | `st.h 0x001b` | (T2, p1=0, p2>0, IEN set, **ICLR set**) | 0x31 | **0x13** -- store gives 0x33, ICLR clears INT and decrements p2 to 0, reassert leaves INT clear.  MEASURED: `control_MUTANT.out` |
| 2 | `pend2` @ T1ICR | `put h ..., 0x001b` | (T1, 0, >0, IEN, ICLR) | 0x11 | 0x13 (p1 already 0, INT already clear) |
| 3 | `pend1` @ T1ICR | `put h ..., 0x001b` | (T1, >0, 0, IEN, ICLR) | 0x31 | 0x13 |
| 4 | `pend1` @ T2ICR | `st.h 0x001b` | (T2, >0, 0, IEN, ICLR) | 0x11 | 0x13 |
| 5 | `pendboth` @ T2ICR | `st.h 0x001b` | (T2, >0, >0, IEN, ICLR) | 0x31 | 0x13 |
| 6 | `pendboth` @ T1ICR | `put h ..., 0x001b` | (T1, >0, >0, IEN, ICLR) | 0x31 | 0x13 |
| 7 | `pend2` @ T2ICR | `st.h 0x00f3` | (T2, 0, >0, IEN, **0xe0 set**) | 0x31 + no `HUH?` | 0x33 **and** the body's `HUH? ... 0xf3` print at :539-541 -- two independent channels |
| 8 | `pend1` @ T1ICR | `put h ..., 0x00f3` | (T1, >0, 0, IEN, 0xe0) | 0x31 + no `HUH?` | 0x33 + `HUH?` |
| 9 | `pend2`, before the wide writes | legal `st.b 0x00` at T2ICR after arming | (**INT set, count 0**) -- the one extra INT state that is reachable | 0x20 (count zeroed by :522-524, INT survives the 0x17 store mask) | -- it is a STATE row, not a mutant row: it makes the following wide write's cell (INT=1, p=0) rather than (INT=1, p>0) |

**Which cells are NOT reachable, with the warrant** (so the disclosure names impossibility rather
than a count): `(same-timer count > 0, that register's INT clear)` cannot be held at a guard --
the count grows only under IEN (:248-251), and every route that clears INT either zeroes the count
first or re-sets it via `reassert` in the same access (:516-543).  A race window between the
SIGALRM increment and the next `DEVICE_TICK` reassert does exist; it is un-holdable by a probe and
it is the filed `pcc2iclrdec` defect.

**Why rows 1-6 are the ones that matter and not gold-plating.**  `(count pending, write ICLR)` is
the **interrupt-acknowledge path** -- the single most-travelled state a real mvme187 timer ISR puts
this register in.  The detector today crosses `{label} x {p1} x {p2} x {IEN}` fully and never
crosses ICLR with anything.  Rows 1-6 are the missing crossings; row 7-8 are the same for 0xe0;
row 9 is the only extra INT state.  After them the detector has strength 2 over all seven axes and
full strength over the four it already had -- and the CONTRACT can then say **"kills every
conjunction of at most two of the seven axes, and every conjunction over {label, p1, p2, IEN}"**,
which is a sentence a future seat can falsify.
# PASS 11 -- Opus seat, FINDINGS (part 7: two things found while verifying, both about the panel itself)

## G1.  THE BRIEF'S "VERBATIM" CLAUSE (d) IS ALREADY SUPERSEDED ON DISK -- and one of the
##      changed sentences is the WARRANT OF AN F2 DISPOSITION I was asked to adjudicate

I diffed the brief's inlined clause-(d) block against `C:\DocumentNoSnc\CC\GXEMUL\CLAUDE.md`.
mtimes: brief **16:47:05**, carrier **17:12:29** -- so the carrier moved 25 minutes into the panel.
Two regions differ, and both matter:

1. F2 **#2** gives fable5's objection as *"the counts are `int`, so 'finite' fails on its
   motivating case"*.  **The carrier now says the opposite about that clause:** *"the counts' raw
   value space is 2^32 apiece, so 'finite' does no bounding work on its motivating case (**a C
   `int` is finite -- the first wording here said it was not; codex and glm caught it on pass
   11**)"*.
   **So #2 is a SECOND wrong accepted disposition** -- one of its three legs is false as written.
   The other two legs (reachability would force rowing `idata == 2`; a PAIRS cap misses `#499`'s
   four axes) stand, and the substance of the first survives as *2^32 is not a bound*.  I found
   this by diffing, not independently; the credit is codex's and glm's, as the carrier records.
2. The carrier now also records *"pass 11 then found the ICLR x pending cell open and in-rule"*.
   **So I am not the first to name the cell I measured** -- another pass-11 seat reached it, by
   reading, and the main loop has already accepted it.  My PREDICTIONS.md (16:56:55) predates the
   carrier edit and I cannot establish priority against a seat answer I have not read, so I claim
   none.  **What I add is the MEASUREMENT (203/203, zero red) and the POSITIVE CONTROL** that
   proves the cell is entered by an ordinary guest `st.h` and that entering it lands a write which
   corrupts the register AND consumes a pending interrupt.

**The process finding, and it is the reportable one: a rule under adjudication was amended
mid-panel, so the nine seats are adjudicating different texts.**  A seat quoting the brief's
"VERBATIM" block is quoting a superseded warrant.  That is not an argument for freezing the
carrier -- incorporating findings as they land is what this pass is for -- but the adjudication
packet should carry the carrier's REVISION (an mtime or a one-line "as amended at HH:MM"), the way
a kill table carries its log, so a seat can tell which text it is being asked about.

Residual inconsistency left by that edit, noted not charged: the carrier's *"The measured case"*
paragraph still says *"the closure is {T2, T1} x {p1} x {p2} -- **eight cells**"* two lines above
the sentence that now describes a sixteen-cell product and a 128-cell denominator.

## G2.  WHAT THE RECORD GETS RIGHT (stated, because a review that only lists defects is a
##      wrong record of its own)

Checked against their logs and green:
* the gate paragraph: `gate14_p11.log` line 1193-1195 gives pcc2 width rows emitted **203**, green
  **203**, red **0**, and line 1234 `PASS (769 checks)`; `gate14_p10.log` gives 194 and 760.  All
  four numbers in the CHANGELOG sentence are exact.
* the gate's row-name list is exactly **203 names, zero duplicates**, matching both denominators.
* **8 of the 9 new rows carry a measured kill**; the ninth (`pend1 rbi`) is the one the record
  names as unkilled.  Derived: union of the five `PCC2W_RED=` lines in `part10/*.out`.
* the seven-partition denominator is correctly read off the body -- I re-derived it from
  :519-539 and got the same seven, no more and no fewer.
* the inlined repair diff is real: **6 hunks, 85 added, 17 removed** (it is the part-9 frozen
  instrument -> live delta, not the whole-round numstat, and it says so in its own header).
* `precommit_check.sh` section J would pass: root `CLAUDE.md`/`PIPELINE.md` and their
  `tools/` copies are byte-identical right now.
* `PRETABLE_pass10.out` runs all four mandated checks with recorded output, its mtime precedes the
  table it predicts, and the aborted first launch is preserved rather than deleted.

# PASS 11 -- Opus seat, FINDINGS (part 8: AN APPARATUS DEFECT OF MINE, and two live-file updates)

## H1a.  I BROKE THE ONE-INSTRUMENT RULE.  Reported before it is asked about.

The carrier: *"A COMPARISON RUN OWES ONE INSTRUMENT.  Freeze the probe (`cp`) for the duration."*
My `run_probe.sh` re-copies the live probe **on every invocation**, so the freeze was per-run and
not per-comparison -- and the main loop edited the live probe at **17:12:29**, between my BASE run
(ended 17:12:47) and my M_ICLR run (started 17:15:14).

    BASE    FROZEN_MD5=6676c58d   (the brief's instrument)
    M_ICLR  FROZEN_MD5=12c7a97b   (a DIFFERENT instrument)

**That is exactly the failure the rule names, in the run whose headline number is a clean sweep.**

**Damage, established mechanically rather than argued:**
* The two versions differ by **7 lines**, all of them TEXT: the contract docstring's bit-3 sentence
  (line 278, not executed) and ONE `row()` NOTE -- the FOURTH argument of
  `row("pendboth arm1", got, want, note)` -- "reddening the decl/rb rows" -> "reddening the rb/rbi
  readbacks".  No row NAME, no `got` expression, no `want` is touched.
* Verified from the OUTPUTS, not from the diff: the (row name, want) pairs emitted by the two runs
  are **203 and 203 and byte-identical as a set**.
* **And I re-ran BASE on the M_ICLR instrument** (`BASE2.out`, frozen once at
  `/tmp/frozen_probe_p11.py`, md5 12c7a97b, against the restored baseline binary md5 3fb4d342e067)
  so the pair rests on one instrument.  See the result line below.

I am reporting this rather than quietly re-running because the class matters more than my run: a
comparison driver that re-copies its instrument each time will silently straddle any edit, and on
a busier day the straddled edit would not have been a docstring.

## H1b.  THE MAIN LOOP HAS ALREADY REVERTED DISPOSITION #9 -- my finding is CORROBORATED, not outstanding

The live probe at 17:12:29 now reads:

> *"Bit 3 (ICLR, 0x08) is a WRITE STROBE: the body TESTS it (`idata & PCC2_TTIRQ_ICLR`) and never
> stores it -- the store mask 0x17 is bits 0, 1, 2, 4 -- so the register bit is set by no writer
> (**pass 10 accepted a sentence calling the mask a writer of it; pass 11 reverted that:
> 0x17 & 0x08 == 0**)."*

So another pass-11 reader reached #9 as well and it is fixed on disk.  I reached it independently
(from `mvme_pcctworeg.h:127` and the writer census) before seeing the edit, but I claim no
priority and the finding should be recorded as **confirmed by two seats and already repaired**.
The new wording is better than a bare revert -- *write strobe* names WHY the bit has no writer.

**Everything else in my part 1 and part 5 was still true of the live files when I checked at
17:33** -- CHANGELOG.md:57 ("the three decl rows expect 4") and CHANGELOG.md:80 (`pendboth rb1i`
0x13 where the log says 0x33) are unrepaired, and so is the `latch all` mis-attribution of the
(T1, 0, 0, IEN clear) cell.

# PASS 11 -- Opus seat, FINDINGS (part 9: the live state at 17:35, and what of mine is still open)

The round is repairing in-round while the panel answers.  Checked against the files at 17:34:

**ALREADY REPAIRED (my findings, confirmed by other seats and landed):**
* #9 reverted in the contract, the pass-10 block and the carrier -- and reworded BETTER than a
  revert: *"Bit 3 (ICLR, 0x08) is a WRITE STROBE: the body TESTS it and never stores it"*, which
  names WHY the bit has no writer.
* CHANGELOG's `pendboth rb1i` 0x13 -> **0x33**, with its provenance and the honest note that
  *"the score matched by coincidence"*.
* CHANGELOG's *"the three decl rows expect 4"* -> **want 1**.
* the carrier's *"the counts are `int`, so finite fails"* -> the 2^32 wording (codex, glm).
* the `pendboth arm1` note's "decl/rb" -> "rb/rbi" (grok).
* And the ICLR / 0xe0 repair is already designed: `0x0018` (IEN|ICLR, landed reads **0x10**) and
  `0x0020` (the HUH? bit, landed reads 0x20 at an armed ICR and 0x00 at an idle one) at both
  labels in all three sessions, twelve readbacks plus three `huh` rows -- **and the `huh` rows
  exist for the right reason**, which is the part-6 preset-collision problem again: a landed 0x20
  and a landed 0x00 read the SAME 0x20 at an armed ICR, so the readback alone cannot separate the
  0xe0 mutant from `M_PENDBOTH`.  My part-6 estimate of "six to nine wide writes" was an
  UNDERCOUNT for full label symmetry; twelve is right.

**STILL OPEN, from this seat, at 17:34:**
1. **The `(T1, 0, 0, IEN clear)` cell is credited to a row that is structurally blind to it.**
   The contract still reads *"(label, 0, 0, *) by the plain rows (`latch all' drives 3, IEN
   clear ...)"*.  `latch all` iterates `BLOCKS12`, whose TxICR entry is **0x1a**; it never writes
   at T1ICR.  The cell is really held by `op t1icr` / `op t1icr dcl` (`put h ..., 0x0303`), whose
   channel is the DECLINE COUNT, not a readback.  One-line fix, and it matters because a reader
   checking the sixteen-cell claim against the named row would find the row cannot see the cell.
2. **A short transcript renders as `died`, unmarked.**  The nine readback rows are
   `("0x%x" % int(r4s[N],16)) if alive and len(r4s) > N else "died"`.  `cval()` marks the
   `no-breakpoint` and dead cases with `(FAILED FOR SOME OTHER REASON)`; this branch does not, so
   fewer-prints-than-expected on a live guest reads as a dead guest.  `program()` uses `step N`
   so the exposure is small, but the convention is the probe's own.  One-line fix:
   `else "short-transcript (FAILED FOR SOME OTHER REASON)"`.
3. **The bound.**  Part 2 (E, E1, E2, E3): axes should include index/selector lvalues (the TxCTL
   under-enumeration is live), the demand should be a strength-t covering array rather than the
   cross-product, and the disclosure should name the STRENGTH rather than a count.  The 112 and
   the "about thirty" are both underived.  This is the H1 answer and it is not repaired by the
   ICLR/0xe0 rows -- those close two more axes; they do not put a bound in the rule.

# PASS 11 -- Opus seat, FINDINGS (part 10: DERIVED, NOT MEASURED -- the rule applied to the OTHER shared block)

**Nobody has applied the adopted rule to TxCTL.**  Every pass since 9 has enumerated at TxICR.
Doing it takes five minutes and it produces two results, one of which is a candidate floor cell.

**The TxCTL write body** (`dev_pcc2.c:494-505`) tests exactly two things: `idata & PCC2_TCTL_COVF`
(:499) and `idata & ~7` (:503).  It READS `d->pcctwo_reg[relative_addr]` as an RMW and uses
`relative_addr` as the INDEX.

**Result 1 -- the under-enumeration.**  Under the rule's letter (partitions the body's own TESTS
induce) the TxCTL closure is `{COVF} x {idata & ~7}` = **four cells, and the LABEL is not an axis**
-- because no `if` tests `relative_addr` there, even though it selects a different register.  So
`&& !(relative_addr == PCCTWO_T1CTL && (idata & COVF))` -- the `#499` shape at the other shared
block -- is **outside the closure the rule demands**.  *It happens to be killed anyway*: `rb t1ctl`
drives `put h ..., 0xaab8`, lane 0xb8, and `0xb8 & 0x04` is COVF, so the write lands and the row
reads 0x00 against its want `0x3`.  **Covered by luck, not by demand** -- which is the argument for
my axis amendment (E(A)), not a live escape.

**Result 2 -- a candidate floor cell that IS unheld.**  Enumerating the four cells against every
wide write the probe drives at the TxCTL block (`latch all` 0x03, `latch all one` 0x01,
`latch all zero` 0x00, `latch all w/d` 0x03, `rb t2ctl` / `rb t1ctl` / `rb2 t2ctl` 0xb8,
`op t1ctl` 0x03, `ovf*` / `ovfhi*` 0x0000, `rb4/rb8` lanes 0xdd / 0x44):

    (COVF clear, idata & ~7 clear)   HELD  -- 0x00, 0x01, 0x03
    (COVF set,   idata & ~7 set)     HELD  -- 0xb8, 0xdd, 0x44
    (COVF set,   idata & ~7 CLEAR)   ** NO ROW ** -- needs idata in 0x04..0x07
    (COVF clear, idata & ~7 set)     ** NO ROW ** -- needs e.g. 0x08 or 0xb0

So `&& !((idata & PCC2_TCTL_COVF) && !(idata & ~7))` at the TxCTL guard -- a conjunction of two
partitions the body itself tests, on ONE lvalue -- **is predicted to sweep all 203 rows**, and the
cell is reachable by an ordinary guest `st.h 0x0004` at T2CTL (0x16, even, 2-aligned).

**I did not measure it.**  I had budget for a second mutant and spent it on neither: the brief
named the ICLR mutant as the measurement it wanted most, and after that came back a total escape a
second run of the same shape would have added little.  This is recorded as **DERIVED, with its
derivation shown so it can be checked by reading** -- and it is the cheapest thing a pass-12
measuring seat could run.  If it holds, it says the class is not "TxICR needs more axes" but
**"every guarded body owes its own enumeration, and only one of the twelve has had one."**

# PASS 11 -- Opus seat, FINDINGS (part 11: the instrument-straddle CLOSED)

`BASE2.out` -- BASE re-run on the **same instrument the mutant table used** (frozen once at
`/tmp/frozen_probe_p11.py`, `FROZEN_MD5=12c7a97b`, no re-copy) and against the **restored baseline
binary** (`CLONE_BINARY_MD5=3fb4d342e067`), 17:33:17 -> 17:48:10:

    PCC2W_RESULT=203/203     FAILCOUNT=0     PCC2W_PROBE_DONE

and the (row name, want) pairs of `BASE2.out` and `M_ICLR.out` are **identical, 203 and 203**.

**So the final pair rests on ONE instrument:**

| run | instrument | binary | result |
|---|---|---|---|
| BASE2  | 12c7a97b | 3fb4d342e067 (baseline) | **203/203, 0 red** |
| M_ICLR | 12c7a97b | 2d0f28f5fcb0 (mutant)   | **203/203, 0 red -- TOTAL ESCAPE** |

plus the earlier BASE on 6676c58d (the brief's instrument), also 203/203, and the positive-control
pair that separates the two binaries (0x13/DECL=0 under the mutant, 0x31/DECL=1 on the baseline).
**Three baseline runs, two instruments, one mutant, and one control on each binary.  The escape
survives every way of cutting it.**
