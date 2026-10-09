# REFUTE THIS WITNESS SPEC BEFORE IT IS BUILT.  You cannot read files; that is the point.

**You are being asked to ATTACK the REASONING, not to verify repo facts.**  You have no file
access, so do not try to open anything and do not stall trying -- say plainly if a premise cannot
be settled from this packet, and attack everything that can.

## WHY YOU ARE BEING ASKED

ONE seat produced the whole specification below.  It is about to be built into a probe that will
be used as the rung-3 WITNESS for a HIGH-severity defect.  A single seat's research gets
independent scrutiny before it is acted on.  **Unanimity with it is worth nothing to me; a
refutation is worth a great deal.**

## THE DEFECT (settled, inlined so you need no files)

`GXEMUL-SEC/src/cpus/cpu_arm.c`, ARM CPU emulation.  `arm_load_register_bank()` ends with:

    default: fatal("arm_load_register_bank: unimplemented mode %i\n",
                 cpu->cd.arm.cpsr & ARM_FLAG_MODE);
             exit(1);

The seven modelled modes are USR32 0x10, FIQ32 0x11, IRQ32 0x12, SVC32 0x13, ABT32 0x17,
UND32 0x1b, SYS32 0x1f.  The emulated machine `testarm` boots in SVC32 (0x13), PRIVILEGED.
A single guest instruction `MSR CPSR_c, #0x14` (encoding `0xE321F014`) writes mode 0x14 -- a
reserved value, none of the seven -- and the emulator process calls `exit(1)`.

`fatal()` PRINTS and RETURNS; it does not exit.  The `exit(1)` on the next line is the kill.
The message uses `%i`, so it prints **`unimplemented mode 20`** in DECIMAL, not `0x14`.

## THE SPECIFICATION UNDER ATTACK

* **Vehicle:** unmodified `testarm`, 16 scored rows (15 data + 1 identity), **12 guest sessions**.
  Expected **14/16 before the fix** (two named rows RED) **-> 16/16 after**.
* **One fresh emulator process per data row.**  Reason given: a process that `exit(1)`s cannot run
  the next row, and entering USR32 is ONE-WAY (once in USR32 the hardware mask makes later writes
  flags-only), so sharing a process would poison later rows.
* **The death oracle is TWO SIGNALS TOGETHER:** the pty reaching end-of-file mid-step (process
  dead) **AND** the exact text `arm_load_register_bank: unimplemented mode 20`.
  Reason given: EOF alone is vacuous under a mutant that crashes for some other reason; the text
  alone is vacuous under a mutant that keeps the print and drops the `exit(1)`.
* **An "arming prefix" runs in every session and is NOT a scored row.**  It reads the mode
  architecturally (`MRS r0,cpsr`) and requires exactly 0x13 before issuing the MSR.  If the prefix
  fails, that row reports `unarmed` and FAILS.
  Reason given: if the CPU were somehow already in USR32, the mask would fire, nothing would
  switch, and **the kill rows would go green while the defect is live**.
* **Accept rows** prove the six legal modes still work after the fix.  Each checks the mode AND
  that the stack pointer changed from its boot value to 0.
  Reason given: SP changing is the signature that the register-bank copy actually ran; a mutant
  that writes the mode bits but skips the copy would pass a mode-only check.
* **`#0` is banned as a stimulus** -- not because it would pass wrongly, but because mode 0 is a
  *26-bit* mode, a different unimplemented case from the reserved 32-bit hole under test.

## ATTACK THESE, IN THIS ORDER

**Q1. THE ORACLE.**  Is "EOF AND that exact text" really sufficient to distinguish this defect from
every other way the process can die?  **Name a failure the pair cannot separate.**  Consider:
what if the emulator prints that line and dies of something else immediately after?  What if
output is buffered and lost when the process dies -- does the text survive?

**Q2. THE ARMING PREFIX.**  It is deliberately NOT scored.  **Is that right?**  An unscored check
that gates a scored row is a familiar hazard: it can pass for the wrong reason, or be skipped, and
nothing in the tally shows it.  Argue both sides and say which you believe.

**Q3. THE ONE-PROCESS-PER-ROW DESIGN.**  12 sessions for 16 rows.  **What does a fresh process
hide?**  A defect that only appears on the SECOND mode switch in one process would be invisible to
this design.  Is that a real gap, and is it inside or outside what a witness owes?

**Q4. THE ACCEPT ROWS.**  "SP changes from boot value to 0" is offered as proof the bank copy ran.
**Can you construct a mutant where SP goes to 0 for the wrong reason** -- and would the row notice?

**Q5. THE COUNT.**  14/16 -> 16/16 means exactly TWO rows change colour.  **Is two the right
number**, given the fix changes behaviour at two separate `default:` arms?  If a row you would
expect to move does not move, that row is doing nothing.

**Q6. FREE SHOT.**  Anything above that is wrong, unstated, or assumed.  **Say plainly which of
these questions you cannot settle from this packet** rather than guessing -- that is a real answer
and I would rather have it than a confident one.
