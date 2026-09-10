# Opus 5 review seat -- `pcc2c040kill` (#512, 9fa07fe), 2026-09-09

OPUS_SEAT_ALIVE_20260909_c040

Line 1 of `regress/pcc2_c040_probe.py`, verbatim:

    #!/usr/bin/env python3

---

## VERDICT

**The DISPOSITION is right and BOTH WARRANTS OFFERED FOR IT ARE WRONG.** No delivery-channel
row is owed at {MIEN clear, C040 set}, but not for the reason given: the channel is *not*
non-varying there (`M_return` varies it, and `M_return` is in the packet's own enumerated set),
and the inverting edit is *not* uniquely visible there (`c040 noassert` already kills it). The
correct warrant is DOMINATION, not vacuity. **Call the proposed row REDUNDANT, never VACUOUS** --
the CHANNEL rule rejects vacuous rows outright while redundancy is a cost judgement, and shipping
"vacuous by construction" hands a future round a false general principle about this site.

**Two corrections to the record and one finding the hold did not ask about:**

* **The detector is 16 rows, not 17.** "13 top-level, 4 indented" is wrong in both halves.
* **A guard-WIDENING mutant is predicted to sweep 16/16**, and the accept row that exists to
  catch it -- `genctl ctlq` -- is keyed on the RETIRED PRE-FIX STRING and is green under every
  post-fix mutant. That is a de-escalation accept-row failability finding (L3 at minimum),
  materially more serious than the MIEN cell the hold asks about, and the repair is one string.

Answers below are EXTENSIONAL. Everything material was read in the tree; predictions are
labelled PREDICTED and I did not build or run anything (read-only task).

---

## PROVENANCE AND A CITATION HAZARD

`git diff HEAD -- src/devices/dev_pcc2.c` is **NOT empty**: the working tree carries an
uncommitted 25-line COMMENT-ONLY correction at the file's not-fixed-here list (lines 112-142).
It does not touch `reassert_interrupts()`, but it **shifts every line below it by +21**.

    cmp <(git show 9fa07fe:src/devices/dev_pcc2.c | sed -n '268,382p') \
        <(sed -n '289,403p' src/devices/dev_pcc2.c)      ->  IDENTICAL

So the function under review is byte-identical to the shipped commit, at a +21 offset. **Every
line number below is given in BOTH frames** because a bare number here is wrong in one of them:

| construct | working tree | 9fa07fe |
|---|---|---|
| `static void reassert_interrupts` | :289 | :268 |
| MIEN test | :360-361 | :339-340 |
| C040 block | :390-397 | :369-376 |
| `if (assert) ASSERT else DEASSERT` | :399-402 | :378-381 |

`regress/pcc2_c040_probe.py` is clean against HEAD; its line numbers are unambiguous.

---

## Q1 -- STATEMENT ORDER: SIBLING, CONFIRMED

`grep -n`, not a hand count. Working tree (subtract 21 for 9fa07fe):

    360:	if (!(d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_MIEN))
    361:		assert = 0;
    362:
    363:	/*  #512: ... and not while C040 selects a delivery pin this model does not
    ...
    390:	if (d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_C040) {
    391:		if (!(d->warned & (1u << PCC2_W_C040))) {
    392:			d->warned |= (1u << PCC2_W_C040);
    393:			fatal("[ pcc2: C040 (MC68040 EIPL) interrupt delivery not "
    394:			    "implemented; assertion suppressed  (once) ]\n");
    395:		}
    396:		assert = 0;
    397:	}
    398:
    399:	if (assert)
    400:		INTERRUPT_ASSERT(d->cpu_irq);
    401:	else
    402:		INTERRUPT_DEASSERT(d->cpu_irq);
    403:}

**Both tests are at one tab -- function-body scope. The C040 block is a SIBLING statement
AFTER the MIEN test, not nested under it.** The packet's Q1 premise is confirmed: with MIEN
clear and C040 set, the MIEN test writes `assert = 0` at :361 and the C040 block still runs at
:390, so **the announce fires under MIEN clear.** `assert = 0` at :396 is inside the C040 block
and OUTSIDE the `warned` latch at :391-395 -- which is the distinction `M_latchinside` tested.

Supporting facts, read rather than assumed:

* `PCC2_C040 = 0x04`, `PCC2_MIEN = 0x02` (`src/include/thirdparty/mvme_pcctworeg.h:61-62`).
  Note :143 defines a **wrong** `PCC2_GENCTL_C040 = 0x03` carrying its own warning; the code
  uses `PCC2_C040`.
* GENCTL resets to `0x00` (`dev_pcc2.c:803` working tree).
* The write arm stores UNMASKED and calls the helper in the same access:

      512:		if (writeflag == MEM_WRITE) {
      513:			d->pcctwo_reg[relative_addr] = idata;
      514:			reassert_interrupts(d);

  This is load-bearing for Q3 -- it is what makes {MIEN clear, C040 set} reachable in ONE store
  from a state where the line is already asserted.

---

## Q2 -- THE FIVE ROW CLAIMS: CONFIRMED. THE COUNT: WRONG (16, not 17)

### The five rows are as claimed

`C040 = 0x04` (:223) and GENCTL resets to 0x00, so each of these drives **C040 SET, MIEN CLEAR**:

| row | site | session | channel |
|---|---|---|---|
| `c040 kill` | :239 | :238 `setup(r5=0x04)` + `ST_B(5, GENCTL)` | SURVIVAL (`alive`) |
| `c040 attrib` | :245 | same session `t2` | ATTRIBUTION (death carries the arm's text) |
| `c040 says` | :271 | same session `t2` | ANNOUNCE TEXT (`SAYS in t2`) |
| `c040 once` | :280 | :277, TWO `ST_B(5, GENCTL)` | ANNOUNCE COUNT (`n_says == 1`) |
| `c040 predirty` | :295 | :293, `ST_H` then `ST_B` | ANNOUNCE under a DIRTY latch field |

So the cell is held on the survival and announce channels by five rows, and the announce fires
there for exactly the structural reason Q1 confirms. **Packet claim CONFIRMED.**

### No delivery row is driven with MIEN clear -- CONFIRMED

`assert_row()` hardwires the precondition and the operand:

    421:             "r7=0x%x" % CLMPCC, "r8=0x%x" % IER_ON, "r9=0x02",
    422:             "r10=0x%x" % final_genctl, "r11=0x0", "r12=0x0",
    423:             "r13=0x%x" % (then_genctl if then_genctl is not None else 0)]

with `r9` stored at insn 4 (`ST_B(9, GENCTL)`, :399) as "MIEN only -- THE PRECONDITION". The four
call sites are `assert_row("live", 0x02)`, `("c040", 0x06)`, `("c040x2", 0x06, repeat=2)`,
`("c040rec", 0x06, then_genctl=0x02)`. **Every `final_genctl` and every `then_genctl` has MIEN
set. Packet claim CONFIRMED.**

### The count is 16, and the derivation that produced 17 keyed on a correlate

    grep -c 'row("'                     ->  17     <-- the record's number
    grep -c '^row("'                    ->  13
    grep -c '^[[:space:]]\+row("'       ->   0

The 17 includes the **four `assert_row("` sites**, because `assert_row("` contains the substring
`row("`. There is exactly **ONE** indented `row()` call site, :514-516, and it is a `for` over a
**3-tuple**, so it produces **three** rows -- and it does not match `row("` at all, because it is
called as `row(_lbl, ...)` with a variable.

Authoritative denominator, from the shipped artifact rather than from any grep:

    regress/artifacts/pcc2c040kill/witness_FIX512_16row_20260908.raw
      ->  PCC2C040_RESULT=16/16, and the transcript lists 16 named rows

**13 top-level + 3 from one indented loop = 16.** This is the carrier's own
deriver-keys-on-a-correlate failure: the regex tested a SUBSTRING, not "is this a `row()` call",
and returned a plausible number that is wrong in both of its parts.

Full row list, in execution order: `genctl ctl`, `genctl ctlq`, `c040 kill`, `c040 attrib`,
`c040 says`, `c040 once`, `c040 predirty`, `irq pending`, `irq live`, `c040 noassert`,
`c040 noassert2`, `c040 recover`, `c040 genctl`, `c040 pending`, `c040x2 pending`,
`c040rec pending`.

---

## Q3 -- THE DERIVATION IS FALSE AS STATED. COUNTER-EXAMPLE: `M_return`, ALREADY MEASURED

### The claim under attack

> "under every clause-(d)-shaped weakening of the C040 block (guard qualified, `assert = 0`
> deleted or moved) the delivery observable CANNOT VARY in this cell -- vacuous by construction"

### The counter-example

`assert = 0;` -> `return;` at :396. It is a ONE-TOKEN edit, it is inside the packet's own
enumeration (the "moved" form), and **its delivery observable DOES vary at {MIEN clear, C040
set}** -- because `return` skips the `INTERRUPT_DEASSERT` at :402 and leaves the incoming line
state untouched, whereas the shipped code deasserts.

Reachability of the cell WITH THE LINE INCOMING-ASSERTED, in two guest stores:

1. `st.b 0x02, GENCTL` with an SCC TX request pending -> MIEN set, C040 clear -> `assert = 1`
   -> `INTERRUPT_ASSERT`. **Line asserted.**
2. `st.b 0x04, GENCTL` -> the arm at :513 stores `idata` UNMASKED, so this is MIEN **CLEAR**,
   C040 **SET**, and :514 calls the helper in the same access. MIEN test writes `assert = 0`;
   the C040 block runs; shipped writes `assert = 0` and falls to `INTERRUPT_DEASSERT`.
   **`return` skips it and the line stays asserted from step 1.**

So the delivery channel varies in the cell the packet says it cannot. The probe's own header
records the same mechanism from the codex design review, at :356-366: *"deleting the assignment
permits assertion; returning preserves the incoming line state"* -- and the whole reason
`assert_row()` writes MIEN-only FIRST is to make the line asserted before the operation under
test.

### Why no row is owed anyway

`M_return` is **already killed at MIEN-SET, and it is MEASURED**:

    killtable_20260908/M_return.raw       PCC2C040_RESULT=9/10
      FAIL  c040 noassert   got 0x8   want 0x1001c
            "C040 SET on an ALREADY-ASSERTED line: must reach completion, NOT the interrupt vector"

`M_d1_noassert` reddens the same row (9/10). The floor demands a KILL, not a kill in every cell.

### The inverting edit is NOT uniquely visible in the cell either

The packet's second warrant -- *"what the cell WOULD see that nothing else sees: an INVERTING
edit"* -- is also false. Take `if (GENCTL & PCC2_C040) { announce; assert = 1; }` at the shipped
position. At `c040 noassert`'s operand 0x06 (MIEN set, C040 set, line already asserted) the
shipped code gives `assert = 0` -> completion, and the mutant gives `assert = 1` -> IRQ_ENTRY.
**Same signature as `M_return` and `M_d1_noassert`, on the same row, which those two are measured
to redden.** A MIEN-clear row would only tell an inversion placed AFTER the MIEN test apart from
one placed BEFORE it -- IDENTIFICATION, not a kill.

### The warrant that is actually true, and is checkable

> **No plausible mutant of the C040 block varies the delivery channel at {MIEN clear, C040 set}
> WITHOUT also varying it at {MIEN set, C040 set}, and the latter cell is held by `c040
> noassert`, `c040 noassert2` and `c040 recover`.**

Because shipped behaviour is `assert = 0` in BOTH cells, a mutant differing only in the
MIEN-clear one must assert when C040 is set and MIEN is clear while NOT asserting when both are
set -- i.e. literally `if (C040 && !(GENCTL & PCC2_MIEN)) assert = 1;`. That does not read like
the same check, so it fails the clause-(d) discriminator. **The cell is DOMINATED, not
non-varying.**

Enumeration behind that, each checked against the shipped source:

| mutant | MIEN clear, C040 set | MIEN set, C040 set | held by |
|---|---|---|---|
| guard qualified `&& MIEN` | delivery same; **announce LOST** | same | `c040 says` (announce, MIEN clear) |
| guard qualified `&& !MIEN` | announce same | **assert survives -> delivers** | `c040 noassert` |
| `assert = 0` deleted | same (already 0) | **delivers** | `c040 noassert` (measured 9/10) |
| `assert = 0` -> `return` | **differs** (skips DEASSERT) | **differs** | `c040 noassert` (measured 9/10) |
| repair conditioned `if (MIEN) assert = 0;` | EQUIVALENT (already 0) | EQUIVALENT | -- (equivalent mutant) |
| block asserts (`assert = 1`) | differs | **differs** | `c040 noassert` |
| block moved above the MIEN test | EQUIVALENT | EQUIVALENT | -- (equivalent mutant) |

Two genuinely EQUIVALENT mutants fall out of that table, which is a result in its own right
under the mutant-that-will-not-die rule: conditioning the repair on MIEN, and moving the whole
block above the MIEN test, are both no-ops for the SUPPRESSING form. Only the INVERTING form
makes the position observable -- and it is caught at MIEN-set regardless.

---

## Q4 -- DISPOSITION

**Agree: no delivery row is owed, and `c040 mienclr` should NOT be added.** But fix the record:

1. **Strike "vacuous by construction".** It is false for `M_return` and it would be quoted. The
   row is REDUNDANT (dominated), which is a different disposition with a different rule attached.
2. **Strike the inverting-edit warrant.** `c040 noassert` kills the inverting edit.
3. **The (e) disclosure is still worth writing**, but for what is actually unpinned: the probe's
   contract should say the detector observes the C040 block's delivery effect only with MIEN
   SET, that the MIEN-clear cell is covered on the SURVIVAL and ANNOUNCE channels by five rows,
   and that a mutant asserting only when MIEN is clear is outside the contract.

**Cost of adding `c040 mienclr` anyway, if the round insists.** It needs a NEW session
(`assert_row("c040 mienclr", 0x04)`), and sessions are where this probe's fragility has actually
lived -- the misaligned `ST_W` finding at :289-292 and the derived completion breakpoint at
:415-417 are both session-shape defects that reddened a correct fix. It moves the denominator
16 -> 17, so **every recorded score restates**: 7/7, 3/7, 4/7, 6/7, 6/7 (20260907) and 10/10,
11/11, 12/12, 13/13, 9/10, 10/10, 10/11, 12/13, 9/10, 11/12 (20260908). It kills nothing that
`c040 noassert` does not already kill. **Yes, it would need a table** -- any instrument change
does.

### THE ROW I WOULD ADD INSTEAD IS NOT ON THIS AXIS -- see the Q5 finding

---

## Q5 -- ENUMERATION OVER THE C040 BLOCK'S TWO LVALUES: COMPLETE. THE OPEN CELL IS ELSEWHERE

**Over {GENCTL.C040 clear/set} x {warned.C040 0/1} the 16-row detector is COMPLETE, and all four
cells are MEASURED rather than argued:** `irq live` (clear, 0), `c040 noassert` (set, 0),
`c040 noassert2` (set, 1), `c040 recover` (clear, 1) -- with `M_latchinside2` killed by
`c040 noassert2` (10/11) and `M_sticky` killed by `c040 recover` (11/12), i.e. the two cells that
were added last are the two that caught mutants. The announce channel covers (set, 0) via
`c040 says`, (set, 1) via `c040 once` -- and (clear, *) needs no announce row because the sticky
mutant `if (C040 || warned)` does not announce (the inner latch test is false) and is caught on
delivery. **I find no open cell in that product.**

The residual is on a **third axis the product does not contain**, and it is not the MIEN one:

### FINDING: `genctl ctlq` IS AN ACCEPT ROW KEYED ON RETIRED TEXT, AND A GUARD WIDENING IS PREDICTED TO SWEEP 16/16

    231:ctl_saw_c040 = ("C040 interrupt assertions" in t)
    232:row("genctl ctlq", "no" if not ctl_saw_c040 else "yes", "no",
    233:    "CONTROL: the benign write must NOT reach the C040 arm")

    $ grep -c 'C040 interrupt assertions' src/devices/dev_pcc2.c
    0

That string is the **PRE-FIX** `fatal()` text (`9fa07fe^:275`, `fatal("pcc2: C040 interrupt
assertions... TODO\n")`). The shipped announce is `"C040 (MC68040 EIPL) interrupt delivery not
implemented; assertion suppressed  (once)"`, which the probe binds separately as `SAYS` at :268.
So post-fix `ctl_saw_c040` is **always False** and `genctl ctlq` is **always green** -- confirmed
across all ten measured mutants: it appears in no FAIL list in either kill table.

**Why that matters, and it is the de-escalation clause exactly.** #512 removed a host-fatal
guard, so the detector owes the ACCEPT SIDE of that predicate -- and the accept-row failability
rule says such a row *"is not discharged by existing -- it is discharged by a MEASURED KILL ...
a row green under its own growth mutant is vacuous whatever the chosen bit's legality."*
`genctl ctlq` drives `BENIGN = 0x10` through the identical instruction, register and width, and
is precisely the row that should redden when the guard grows.

**PREDICTED (derived by reading; NOT measured -- this task is read-only):** build the canonical
growth mutant

    if (d->pcctwo_reg[PCCTWO_GENCTL] & (PCC2_C040 | 0x10)) {

and it is predicted **16/16, a clean sweep**, row by row: `genctl ctl` writes 0x10, the block
runs, announces and suppresses, host survives -> green; `genctl ctlq` looks for dead text ->
green; the five 0x04 rows are unaffected; `irq live`/`c040 recover` use 0x02, and `0x02 & 0x14`
is 0, so delivery is normal -> green; the 0x06 rows suppress as before -> green; `c040 genctl`
reads back 0x06 -> green.

**The repair is ONE STRING and it adds no row and no session** -- hoist `SAYS` above :226 and
write `ctl_saw_c040 = (SAYS in t)`. The denominator stays 16, so **no recorded score restates**.
Predicted after the repair: shipped build still 16/16 (the benign write genuinely does not reach
the C040 arm), widening mutant 15/16 with `genctl ctlq` red. That pair is the (a)/(b)-shaped
control the failability rule wants, and it must be MEASURED before this is graded.

**Grading, honestly bounded.** `genctl ctlq` is the sole carrier of the de-escalation accept
obligation for every GENCTL bit except 0x02 -- the 0x02 direction IS pinned, because widening
onto MIEN (`PCC2_C040 | PCC2_MIEN`) suppresses at `irq live`'s operand and reddens it. So the
accept side is half-pinned by accident and half-unpinned. That reads as **L3 (undischarged
obligation) at minimum and arguably L2**, but the grade should follow the measurement, not this
prediction -- writing a predicted sweep into a measured column is the frozen-number class.

### A SECOND, SMALLER CELL: THE ANNOUNCE CHANNEL AT MIEN-SET

Every announce assertion runs at MIEN CLEAR (`c040 says`, `c040 once`, `c040 predirty`, all on
0x04-from-reset sessions); no row asserts that the announce fires when MIEN is SET. Mutant:

    if (GENCTL & PCC2_C040) {
        if (!(GENCTL & PCC2_MIEN))          /*  announce only when MIEN is clear  */
            <announce, latched as now>;
        assert = 0;                          /*  suppression unchanged  */
    }

The 0x04 rows still see the announce; the 0x06 rows still see correct suppression. **PREDICTED
16/16.** The killing row costs ZERO new sessions -- `assert_row()` already returns the transcript
and `td` is already bound at :448:

    row("c040 says2", "yes" if SAYS in td else "no", "yes",
        "the announce must fire with MIEN SET too -- announce rows all run MIEN-clear")

I would **FILE** this rather than force it in-round: under the 2026-09-04 joint-cells rule a cell
is FLOOR only where *the guarded body's own code distinguishes the lvalues*, and the C040 block's
body does not test MIEN at all -- so this is clause-(e) coverage debt, not a floor breach. It is
noted because it is the honest answer to "what would a MIEN-axis row buy": **an ANNOUNCE row at
MIEN-SET, not a DELIVERY row at MIEN-CLEAR.**

---

## THREE HYGIENE NOTES

1. **Variable shadowing, latent not live.** `t2` is bound at :238 (the survival transcript, read
   by `c040 attrib` :244, the EVIDENCE loop :248 and `c040 says` :271) and **rebound at :464** by
   `assert_row("c040x2", ...)`. `t3` is bound at :277 and rebound at :488. Every read of the
   survival transcripts precedes its rebinding, so there is no defect today -- but it is a live
   trap for exactly the `c040 says2` row proposed above: written after :464 against `t2` it would
   silently read the delivery transcript and mean something else. Use `td`, or rename.

2. **No mutant has been scored against the shipped 16-row instrument.** The 2026-09-08 mutants
   were scored at 10, 11, 12 and 13 rows as the instrument grew; the 16-row artifact is BASE
   only. The four rows added after the last mutant run (`c040 genctl` and the three `*pending`)
   all ride on already-run sessions, so the kills should carry forward -- but "should" is an
   inference and the project's rule is that a score claim names its log. Any table this round
   runs should re-score all six at 16 rows and cost almost nothing.

3. **The `c040 attrib` row's `sig` half is also keyed on the retired string** (:244). That one is
   CORRECT as-is: attribution must recognise the OLD text, since the death it attributes is the
   reinstated pre-fix kill -- and `M_b_reinstate` confirms it, dying with that text while
   `c040 attrib` stays green (3/7, reddening `c040 kill`, `c040 says`, `c040 once`,
   `c040 predirty`). Do not "fix" it along with `genctl ctlq`; the two rows key on the same
   string for opposite and both-valid reasons.

---

## WHAT I READ vs WHAT I TOOK FROM THE PACKET

**READ AND VERIFIED IN THE TREE:**
`src/devices/dev_pcc2.c` :112-142 (the uncommitted comment hunk), :289-403 (the whole function),
:500-516 (the GENCTL write arm), :803 (reset value); `src/include/thirdparty/mvme_pcctworeg.h`
:61-62 and :135-143; `regress/pcc2_c040_probe.py` in full (522 lines); `9fa07fe^` and `9fa07fe`
versions of the function via `git show`; all sixteen `.raw` artifacts under
`regress/artifacts/pcc2c040kill/` for their `PCC2C040_RESULT` lines and their FAIL rows; the
`cmp` establishing working-tree/HEAD identity of the function.

**TAKEN FROM THE PACKET, NOT INDEPENDENTLY VERIFIED:**
that the flagship adjudication established the C040 block's read set as {GENCTL.C040,
warned.C040} and named {MIEN} x {C040} as a shared floor cell (I re-derived the read set from the
source and agree, but I did not read the adjudication); that part (a) of the original hold is as
described; the row-count claim of 17, which I checked and found wrong.

**NOT DONE (read-only task):** no build, no probe run, no mutant. Every "PREDICTED" figure above
is derived by reading the source and the probe and is explicitly NOT a measurement.
