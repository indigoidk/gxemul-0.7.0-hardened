# ORACLE-CORRECTION DESIGN — `gdromcondavail`: the preferred repair turns a shipped green row RED by succeeding

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** You established the finding this brief rests on, so
I may have over-read it. Today you corrected five counts and four premises of mine across other rows.
**Assume I have over-read this one and say so.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** HEAD is `7a41b3f`.

**SCOPE:** `GXEMUL-SEC/src/devices/dev_dreamcast_gdrom.c`, `GXEMUL-SEC/regress/gdrom_*.py`.

**VERDICT LINE FIRST.**

## §C — SETTLED PREMISES

**S1 — THE DEFECT, reachable by a guest.** `:1194`/`:1202` let the guest write `d->cnt` a byte at a
time. `:1077` clears `COND_DATA_AVAIL` only when `cur_cnt >= cnt` **and** the buffer is exhausted.
Raise `cnt` after data is armed and the clear never runs: the buffer exhausts, reads fall to the
`:1087` else-arm returning `0xffff`, and **availability stays set** — with the diagnostic latched
after the first occurrence, so the log goes silent.

**S2 — YOUR PREFERRED REPAIR** (from the design pass): clear availability when the final valid
halfword consumes the **buffer**, independent of the guest count; keep re-arming when the count
boundary is reached with bytes remaining. Clearing only at `:1087` is correct but **one read late** —
a status-only poll after the last valid read still sees availability.

**S3 — THE COMPLETION EVENT IS COUPLED.** `SYSASIC_TRIGGER_EVENT` at `:1085` sits inside the same
`if (d->cur_cnt >= d->cnt)` block. Verified. **Moving only the availability clear leaves the final
completion notification suppressed in the inconsistent-count case.**

**S4 — AND THE REPAIR BREAKS A SHIPPED ROW.** `gdrom_data_probe.py:393`'s `overread x1` requires
**exactly one** OVERREAD diagnostic (`"1"`, *"reading past the buffer -> diagnostic exactly once"*).
Clearing on the final valid read makes subsequent reads enter NODATA immediately, so the OVERREAD
count becomes **zero** and that row goes red *because the fix worked*.

**S5 — THIS PROJECT'S RULE FOR THAT CASE.** The oracle-correction rule: **re-pin the row FIRST,
measure the COMMITTED build RED under the new expectations, and only THEN change the code** — same
scripts, opposite colour. Plus: the rewritten row's comment quotes the source verbatim with a
grep-able anchor (the old pin's authority is what is being overturned, so it cannot also be the
warrant); the false record is corrected in place, never silently superseded; and **a re-pin that
removes the last failing row is not finished** — ask what still fails afterwards.

## The questions

**Q1 — WHAT EXACTLY SHOULD `overread x1` BECOME?** It must be RED on HEAD under the new expectation
and GREEN after the fix. Name the diagnostic(s) and counts. My reading is that HEAD gives 1 OVERREAD
and 0 NODATA on that stimulus, and the fix gives 0 OVERREAD and N NODATA — **so a re-pin to "0
OVERREAD" is red on HEAD, which satisfies the order requirement.** Is that right, and what is N?

**Q2 — IS RE-PINNING EVEN CORRECT, OR IS THE OLD PIN RIGHT?** The row asserts a real property: an
over-read announces itself exactly once. **If the repair silences that announcement entirely, has the
device lost a truthfulness channel it should keep?** `#460`'s comment joins the `:1052` and `:1087`
arms as one predicate family *"read when there is nothing to give"* — argue that the repair should
preserve an announcement rather than route past it.

**Q3 — S5's LAST CLAUSE: what still fails after the re-pin?** If the answer is "nothing", the round
owes a row on another observable channel before it may ship. **Name it** — I expect it is the
`exhaust cond` row you already specified (GDROM_COND at `0xa05f709c`, `0xa8` → `0xa0` at the final
halfword), but say whether that is sufficient alone.

**Q4 — DOES THE COUPLED EVENT NEED ITS OWN ROW?** S3 says exhaustion and completion must move
together. **What observes the event?** If nothing does, a repair that moves the clear and forgets the
event is invisible to the detector — which is the clause-(d) shape.

**Q5 — THE SMALLEST EDIT that breaks the fix and still passes.** You already named
`d->cur_cnt == d->cur_data_offset`, which survives because without a re-arm both finish at 408.
**Is there a second, and does the detector need a SEGMENTED transfer to see either?**

## What I am not asking

Do not write a patch or a probe and do not run anything. **Nothing ships until the flagship
adjudication on 2026-09-09.**

**If, while verifying a claim, you found something ELSE — say so.**
