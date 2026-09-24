# fbdeclinefive PASS 1 -- adjudication packet for the Fable seat (fires LAST; every other seat has answered)

Open your answer with the token `FABLE_SEAT_ALIVE_20260919_FBD5` and the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md` quoted verbatim.  VERDICT LINE FIRST.  Ordinary engineering
language throughout (declines, terminating calls, latches, detector rows).  Read-only: run nothing, edit nothing.

## The round in three sentences
`GXEMUL-SEC/src/devices/dev_footbridge.c` (HEAD f685d75) ends the emulator process with `exit(1)` when a guest accesses
five interrupt-controller registers in the direction the DC21285 datasheet does not define (writes to IRQ_STATUS +0x180,
IRQ_RAW_STATUS +0x184, FIQ_STATUS +0x280, FIQ_RAW_STATUS +0x284; a read of IRQ_ENABLE_CLEAR +0x18c).  The design is
member 3 of the option set: DECLINE (no state change, read returns 0) + a per-site latched `fatal()` announce carrying
`(once)`, five `int` latch fields, the +0x18c arm dropping its `odata = d->irq_enable` leak.  In the same commit the three
probes' "kill control" arms (which relied on the +0x18c read terminating the process) are replaced by two harness legs:
K1 (a rejected `-E` name exits 1 before any prompt with a diagnostic naming the input) and K2 (`quit` after a verified
prologue reaps exit 0 and the next interaction reports `dead` before cleanup).

## What the eight other seats settled (codex panel seat: REVISE -- its additions are C1-C8 in p1_findings.md) (all first-hand; the Opus seat MEASURED in a scratch clone)
Design template with every correction applied: `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\fbd5\brief_fbd5_design.tpl.md`.
Consolidated findings with attributions: `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\fbd5\p1_findings.md`.
Opus measurement: `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\fbd5\opus_p1_20260919\OPUS_P1_ANSWER.md` (verified opus-5).
* Brief defects corrected: nine live exits not ten; HEAD f685d75; the zero-on-declined-read warrant is policy backed by
  in-file silent siblings, not a datasheet quotation; the Table 7-10 excerpt was cut two rows short.
* Detector: the packet's per-site rows were BELOW THE FLOOR -- a shared latch (Q2 c) and an aggregate latch swept them
  29/29 because each row ran one site in its own process.  Adopted: ONE new arm touching all five sites in one process,
  with a count-of-distinct-announces row (5 / 4 / 1 measured), rows renamed S1-S5 (accept) / N0-N6 (decline) to avoid
  ids the probe already emits, an interleaved legal read inside each N row, one byte-width decline row, FIQ write value
  0x40 (inside the 0xc0 enable).  Two more escapes are DISCLOSED under clause (e), not rowed: a constant-0 IRQ_STATUS
  read (irq_status cannot become nonzero under single-step -- measured with a timer armed) and the FIQ read expression
  (`fiq_status` has no writer anywhere in the tree).
* Legs: K1 must key on the naming diagnostic (five different startup refusals all exit 1 -- measured); K2 must require
  BOTH `exit == 0` and a fresh-`reg` prologue check (a child dead before the prologue shows `dead` identically).  Legs in
  all three launchers with each launcher's register map; gate pins the discriminating tokens, one pair per probe.
* FAULT is unavailable on ARM (memory_rw dispatches device-access exceptions for MIPS/M88K only).

## THE QUESTIONS (answer each; number them)
Q1 THE ONE DISAGREEMENT.  `case FIQ_ENABLE_CLEAR` (+0x28c, the exact FIQ twin of +0x18c) ALREADY declines a read
   silently and returns 0 (measured on HEAD).  Opus5: give it the same latched announce IN THIS COMMIT (datasheet :6801
   says the nFIQ/nIRQ control registers are identical; same device, file, class; one field, one row; otherwise the
   controller carries four dispositions for one question).  Grok: leave it (addition licence -- it does not terminate,
   so a new announce on a silent path is an addition with no measured delta; the reopening rule admits a second site only
   for the WITNESSED class, and the witnessed class is process termination).  Main loop's provisional call: NOT this
   round; 28Ch is already facet (2) of the filed row `fiqenableread`, and PRETABLE.out records why the twin stays
   silent.  Which is right, and why?
Q2 THE DISCLOSURES.  The codex seat proposes closing both clause-(e) holes OFFLINE: `regress/diff_footbridge.c` already
   #includes the device, so seeded-`irq_status` rows can drive each declined access through the handler and assert
   preservation and the read expression (a rung-1 DETECTOR, never a witness; the guest rows keep reachability and
   survival).  Is that split acceptable, and does it discharge the two disclosures or merely narrow them?
Q3 THE LATCH FORM.  Five `int` fields (agy, grok, kimi) vs one bit-field plus an enum (opus5).  The file has no latch
   today.  Rule, and say whether N0 (the five-in-one-process count row) is still owed under your choice.
Q4 WHICH OF THE MAIN LOOP'S ACCEPTED DISPOSITIONS IS WRONG?  Fourteen were accepted (B1-B4, D1-D10 in p1_findings.md).
   Name at least one you would reverse or narrow, or say plainly that none is wrong and why you are confident.
Q5 FILING.  Two new finds are queued for filing: `armdacr2kill` and `armdesc3kill` (`src/cpus/memory_arm.c:79` and
   `:254` -- a reserved domain-access value and an unimplemented fine-page-table descriptor, both guest-writable, both
   ending the process).  The FIQ-side finds (28Ch silent, no FIQ output, fiq_status never written, FIQSoft absent) are
   ALREADY the five facets of the filed row `fiqenableread`; IRQSoft +0x190 (legal write announced unlatched on every
   access) would be its sixth facet.  Rank the two new rows against the open queue's usual scale, say whether IRQSoft
   belongs in `fiqenableread` or on its own, and name the next EASY resolvable item.

End with a seat record: model, files read, nothing run.
