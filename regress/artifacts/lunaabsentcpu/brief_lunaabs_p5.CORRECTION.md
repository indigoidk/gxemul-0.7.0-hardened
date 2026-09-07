# CORRECTION to `brief_lunaabs_p5.md` -- written 2026-09-06 ~17:2x, AFTER the packet was sent.
# The brief itself is NOT edited: it is the record of what the three seats actually read.

## THE TABLE NAMED THE WRONG RED ROWS FOR ONE MUTANT, AND ALL THREE SEATS FOUND IT

The packet's table says `M_IRQACTIVEP1` reds **`cpu2 deliver23, cpu3 deliver23`** -- session E2's rows.
`killtable5/driver.log`, at the anchor `=== M_IRQACTIVEP1`, says:

    M_IRQACTIVEP1 LUNAABS_RESULT=35/37 (BASE 37/37) LUNA_ABSENTCPU_WITNESS=FAIL
        RED LUNAABS_ROW=cpu3 deliver
        RED LUNAABS_ROW=cpu2 deliver

**Session E, not session E2.**  Verified.  Found independently by codex, grok and kimi, each citing the log.

**And the mechanism makes it obvious in hindsight, which is why it is worth writing down rather than just fixing.**
That mutant aliases a WRITE -- the per-slot latch -- so the first arrival of each parity pair consumes the latch
whichever session pends them; the entered-set in the log reads `[0, 1]`, the two that arrived first.  Session E2
exists for the READ aliases and correctly does NOT red here.  The probe's own header note says exactly this
(`irqActive ... already covered by session E`), so the packet contradicted an artifact it shipped alongside --
which kimi caught and I had not.

## TWO FURTHER CORRECTIONS THE SAME PASS PRODUCED, both recorded on the ledger row

* **The derivation's attribution**: session C pins only `f(1) = 1`; **`f(0) = 0` is pinned by the ONE-CPU session**,
  not by C.  The constraint set is unchanged and correct; the credit was wrong.
* **The narrowed NULL-guard warrant is FALSE and is withdrawn.**  It came from the pass-4 measuring seat and I
  propagated it without checking.  `interrupt_handler_lookup`'s empty-name arm assigns the fallback handlers and
  **does not return**, so the scan runs and an unregistered name reaches `abort()`; nothing registers the empty
  string.  The assignment executes and is then discarded -- its EFFECT is unreachable, not its code.  The
  equivalence stands; its warrant is that DEVINIT connects exactly slots 0..ncpus-1 while two exits bound ncpus.

## A DEFECT IN THE PACKET ITSELF, named by kimi and worth keeping

Its second question asks which of five dispositions is wrong and refers to "TWO extra mutants" without naming them.
The seat could not settle their identity from the artifacts and read them as a different pair.  **A packet that asks
`which of N is wrong' must make the N enumerable from the artifacts it ships**, or the answer is to a question the
packet did not ask -- the same shape as pointing a seat at a working file instead of a frozen one.
