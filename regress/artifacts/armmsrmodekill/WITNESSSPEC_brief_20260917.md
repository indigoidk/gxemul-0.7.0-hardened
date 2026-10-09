# `armmsrmodekill` -- **SPECIFY THE WITNESS.**  You confirmed the defect; this is its rung-3 probe.

## VERDICT LINE FIRST.  TREE: `GXEMUL-SEC/src/` -- three pristine-2021 `src/` copies sit at the
## project root; line numbers off by hundreds mean you read one.  **DO NOT RATIFY** -- §S4.

## S1 -- SETTLED BY YOU, EARLIER TODAY (re-inlined; do not re-derive)

You CONFIRMED this by a full instruction-to-`switch` trace and it is now filed as a **HIGH**:

* **One privileged guest instruction ends the emulator PROCESS.**  `MSR CPSR_c, #0x14`, encoding
  `0xE321F014`, on `-E testarm`.  `arm_load_register_bank()`'s `default:` -> `fatal(); exit(1)`.
* `testarm` boots **SVC32 (`0x13`), privileged**; `0x14` is the first hole above it and is none of
  the seven modelled modes.  **There is no `arm_mode_ok` anywhere.**
* Three things that look like filters are not: the USR32 mask tests `== ARM_MODE_USR32` and SYS32
  is not in it; the same-mode skip needs `0x13 != 0x14` and gets it; the c-bit is set.
* **SAVE (`:559`) IS NOT FIRST-HIT** -- it runs on the OLD mode (SVC32, modelled) and returns; the
  process dies in LOAD (`:606`).  A Load-only fix CREATES the Save kill, so it is ONE round.
* **Disposition: MEMBER 3, DECLINE + LATCHED ANNOUNCE, at both `default:` arms**, with the decline
  sitting BEFORE save (or `cpsr` rolled back in Load), because callers write `cpsr` BETWEEN save
  and load.  Member 1 DELETE is wrong; member 5 FAULT is available on ARM and still wrong (MSR is
  `Exceptions: None`).
* **DO NOT WITNESS WITH `#0`** -- the `#449`-shape trap.  Under the extracted Table A4-1
  `PrivMask = 0x0F` reading, `#0` keeps M4 and lands on USR32 `0x10`, which IS modelled and does
  NOT kill, so a `#0` probe **could go GREEN ON A LIVE DEFECT**.
* **The message prints `unimplemented mode 20`, DECIMAL** -- the `fatal()` uses `%i`.  A hex grep
  matches nothing and reports a clean, confident, wrong answer.
* Your own channel table: `exit(1)` = pty EOF mid-step + process DEAD + that line; `running = 0` =
  prompt RETURNS + alive; crash = EOF + dead + no line; post-fix decline = prompt returns + alive +
  one `(once)` line + `MRS r0,cpsr` still `0x13` in bits 4:0.

## S2 -- WHAT I NEED, TO THE STANDARD YOU SET TWICE TODAY

On `lcaisaphys` you grew a 3-row sketch into **12 data + 1 identity** because the ladder and the
arming proof demanded it, and gave `8/13 -> 13/13`.  On `armthumbabortkill` you gave **11 + 1** and
`7/12 -> 12/12`.  **Do that here.**  Specify `regress/arm_msrmode_probe.py`:

1. **THE ROW SET** -- stimulus, oracle, PRE (committed HEAD) and POST (member 3) per row, and the
   TALLY both sides.
2. **THE TWO LADDER CONTROLS.**  A first draft of another probe in this tree returned 0x0
   everywhere **with its RAM control GREEN**, so one control is not enough:
   * LIVENESS -- a known value returns through the same decode;
   * DEVICE-SIGNATURE -- the observed value could only have come from where you think.
   **On a bare `testarm` with the MMU off, what plays each role?**
3. **THE ARMING PROOF.**  How does a row prove the CPU was in **SVC32 and privileged** when the
   `MSR` executed?  If it was already in USR32 the mask fires, nothing switches, and the probe goes
   green while the defect is live -- the fake-green direction, which has bitten twice today.
4. **THE ORACLE FOR A DEAD PROCESS.**  `exit(1)` kills the emulator, so the probe cannot read a
   register afterwards.  `arm_bfx_width_probe.py` sets `alive = False` on pty EOF.  **Is EOF plus
   the message enough, and what distinguishes it from a crash** -- per the CHANNEL rule, a row whose
   channel cannot vary under its mutant is vacuous by construction.
5. **THE ACCEPT ROWS the de-escalation clause demands.**  Removing a host-fatal guard deletes the
   tripwire, so the detector owes a row per adjacent MODELLED mode proving legal writes still land:
   `0x10` USR32, `0x11` FIQ32, `0x12` IRQ32, `0x17` ABT32, `0x1b` UND32, `0x1f` SYS32.
   **WHICH of those can a guest actually reach from SVC32 by this store, and which cannot?**
   *Note USR32 is one-way -- once in USR32 the mask blocks the way back, so an accept row that
   enters it may poison every later row in the session.  Order matters; say so.*
   Each accept row is discharged by a MEASURED KILL under a joint guard-growth mutant, never by
   existing.
6. **Row-name length limit, `EXPECT_ROWS` identity row, completion sentinel**, as before.

## S3 -- THE TRAP I EXPECT AND CANNOT RESOLVE ALONE

**A probe that kills the emulator on row N cannot run rows N+1..M in the same session.**  So either
every defect row is its own session, or the defect row is LAST.  **Which, and what does that cost
the accept rows?**  If each session is a fresh process, the arming proof is owed PER SESSION, and
that is a real multiplier on the row count -- say the true number rather than the tidy one.

## S4 -- *** BREAK IT. ***

Two things I am relying on and cannot check without you:

* **`0xE321F014` is my encoding, not yours** -- you gave the mnemonic and the rotate reasoning.
  **Verify the word bit by bit** (cond/opcode/mask/rot/imm) against the fork's own decoder, and say
  plainly if it is wrong.  A hand-assembled encoding that decodes to something else is this
  project's oldest instrument trap, and a wrong register field yields 0, which a NaN/sentinel row
  accepts by accident.
* **"`testarm` boots SVC32 privileged"** is an initialisation claim.  You proved the MMU one by
  reading the CREATE path and then found the M bit set somewhere else entirely.  **Read the span
  that would CONTAIN a later mode change** -- the machine setup, any PROM emulation, the load stub
  -- before affirming it.

**If the witness is not cheap after all, say so.**  An honest "this costs a real round" beats a
plan that collapses when built, and the row may then ship documented-only with the attempt recorded.
