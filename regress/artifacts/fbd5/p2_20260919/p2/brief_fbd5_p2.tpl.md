# fbdeclinefive (#545) -- PASS 2: review the REAL DIFF (six files) and the measured kill table

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly, and THIS round's pass-1
packet itself carried two wrong premises ("ten live exit(1)", "HEAD 9c28ca5") that every seat caught.  **Check the
premises, not just the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a
premise from something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\src\` at HEAD {{HEAD}} (source of every file below
byte-identical to 9c28ca5/f685d75 -- records-only commits since).**  Copies of `dev_footbridge.c` that are NOT this fork
exist under the project root (`_scratchpad/r6pass2_fb/`, 744 lines, a stale fork copy; three pristine-2021 copies under
`./src/` and `_archive/`).  If your line numbers disagree with mine by tens or hundreds you are reading one of them -- say
so rather than reconciling.

**If you cannot read files that is expected** -- every fact you need is inlined: the WHOLE diff, the whole fixed
enclosing function, the kill-table summary.  Name any premise you cannot settle from this packet rather than guessing.

**Where this brief states an ARITHMETIC claim -- a register offset, an ARM encoding, a row count, a mutant score --
ENUMERATE it rather than reasoning about it.**  Walk the values.  For an ARM word, decode the fields (cond, I, P, U, B,
W, L, Rn, Rd, imm12) rather than pattern-matching the mnemonic.

**VERDICT LINE FIRST**, so your answer survives truncation.  Ordinary engineering language: declines, terminating
calls, latches, detector rows.  This is a bounds-and-correctness review of a device model and its regression rows.

## 1. WHAT THIS ROUND DOES (the design pass 1 converged on; nine seats + the Fable adjudication)

`dev_footbridge.c` (DC21285 "footbridge", CATS machine) ended the emulator process with `exit(1)` when a guest accessed
five interrupt-controller registers in the direction the datasheet does not define: writes to IRQ_STATUS +0x180,
IRQ_RAW_STATUS +0x184, FIQ_STATUS +0x280, FIQ_RAW_STATUS +0x284 (`:6803`: "The Status and RawStatus are read-only, and
EnableClear and Soft are write-only"), and a read of IRQ_ENABLE_CLEAR +0x18c (Table 7-10's read column at 18Ch is `--`).
The fix is option-set member 3 -- DECLINE (no state change; a declined read returns 0 as the fork's POLICY, the nearest
datasheet support being `:1652` "nonexistent CSR ... zeros are read" and Figure 7-2 `:6814`) + a per-site latched
`fatal()` announce carrying `(once)`; five per-site `int` latch fields (fable5 Q3; the file had no latch of any kind); the
+0x18c arm drops its `odata = d->irq_enable` leak (that value is 188h's answer, not 18Ch's).  Four live `exit(1)` remain
in the file: the two SDRAM reads (+0x100/+0x104, `fbsdrampair`) and two construction-time ones in DEVINIT.  NOT touched,
by ruling: +0x28c (FIQ_ENABLE_CLEAR read) already declines silently -- `fiqenableread` facet (2), with the Opus seat's
dissent ("fix it in the same commit") recorded verbatim there; 190h/290h (IRQSoft/FIQSoft) reach `default:` --
`fbirqsoftunimpl`.

In the SAME commit the three probes' kill control (a +0x18c read that relied on the process dying) is RETIRED and
replaced by two HARNESS LEGS through each probe's own launcher: **H1** (an unknown `-E` name: NO prompt AND the
diagnostic `Sorry, emulation "<name>" is unknown.` naming THIS run's input AND `WIFEXITED && == 1`) and **H2** (`quit`
after a prologue VERIFIED by a fresh `reg` -- r3 bit 0 clear, r5 = 0x11223344, r6 = 0x1011, the timer-mask value
0x00345678 in r1 (sites) / r7 (drain, witness) -- then ONE more ordinary `reg` that must fail with `dead` set BEFORE
teardown, and a reap of exit 0).  Both non-obvious H2 clauses are load-bearing: a child dead BEFORE the prologue shows
`next send fails` and `dead` IDENTICALLY (measured, pass 1).

The detector: (a) `footbridge_sites_probe.py` arm S -- the five sites in ONE process, each accessed twice with a legal
sibling read between (rows S1-S5 values, SF1/SF2 final raw reads, N0 five distinct once-announces, N1-N5 per-site
access-local text counts, controls SC1/SA1); (b) `diff_footbridge.c` P-rows (rung-1 DETECTOR, never a witness): a
calloc'd instance seeded BY DIRECT FIELD WRITE (irq_status 0x18, irq_enable 0x30, fiq_status 0x50, fiq_enable 0xc0 -- so
masked != raw), each declined access at three widths, preservation, the read EXPRESSIONS, the announce count (fatal() is a
counter there), a byte-FIRST fresh instance (P9); (c) H1/H2 in all three launchers; (d) gate_arm.sh pins on the legs'
DISCRIMINATING tokens and the arm-S rows.  Two clause-(e) disclosures stand: no GUEST row observes a nonzero status
(irq_status stays 0 under single-step even with a timer armed -- host timers stop at the prompt), and the FIQ read
expressions are pinned only against seeded values no product code produces (`fiq_status` has no writer in the tree).

## 2. SETTLED PREMISES, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM (scope: this round)

* `fatal()` PRINTS and returns; it does not exit and is not gated by `-q` (`src/core/debugmsg.c:384-391`; `debug()` is
  gated at `:375`).  Every process death in this device is an explicit `exit(1)`.
* The five sites and directions are TRUE 5/5 (Table 7-10 `dc21285.txt:6821-6833`; §7.3.29-7.3.33; the one-sentence
  form `:6803`).  Table 7-1's "R = Read only. Writes have no effect." is §7.1's PCI-CONFIGURATION legend (`:4505-4520`,
  extracted staggered) -- it TRANSFERS to the CSR tables but is not a sentence about these registers.
* FAULT (member 5) is NOT available on ARM: `memory_rw.c:603-625` dispatches a device-access exception for MIPS and M88K
  only (no `MEM_ARM` arm).  `dev_unreadable.c`'s `return 0` yields MEMORY_ACCESS_FAILED with no abort delivered.
* The file had NO latch field (15 fields, `:60-85`); `struct footbridge_data` is zeroed by DEVINIT's memset (`:771`) AND
  by the offline differentials' `calloc` (`regress/diff_footbridge.c:151`, `diff_fbpending_bound.c:143`).
* The differential's instance has NULL `d->irq` interrupt callbacks under calloc; the enable arms call
  INTERRUPT_ASSERT(d->irq) -- so P-rows seed by direct field write and never through +0x188/+0x18c writes (the P-rows
  install counting no-ops on `d->irq` too, so a legal EnableClear write (P8) is safe).
* Five DIFFERENT startup refusals (`-E nosuch`, no file, missing file, bad option, `-M notanumber`) ALL exit 1 with no
  prompt (Opus, pass 1, s10_legmut.out); only the diagnostic text naming the input discriminates H1.  Two of them print
  the banner first, so the text search covers the whole buffer.
* Unknown `-E`: `machine.c:240` `fatal("\nSorry, emulation \"%s\"", stype)` ... `fatal(" is unknown.\n")`, returns 0 at
  `:258`; `main.c:543-544` `if (!res) exit(1);` -- before any prompt.  `quit`: `debugger_cmds.c:1636-1637` sets the
  shutdown flags; `main.c:807-821` cleans up and returns 0.
* The pass-1 packet's per-site row design was BELOW THE FLOOR: a two-site shared latch and an aggregate latch each swept
  it 29/29 because every row ran one site in its own process (Opus, s6_table.out); the one-process arm S with the N0
  count row is the measured repair (5 / 4 / 1).  A constant-0 IRQ_STATUS read (`m_swallow`) and a dropped `&` at FIQ_STATUS
  (`m_fiqraw`) also swept the guest rows -- the offline P-rows are the repair for the first and a NARROWING for the second.
* The FIQ enable is unobservable from the guest by any route today (+0x288 reads 0: `fiqenableread` facet 1).
* Rows named A1/A2/D1/K1 already existed on the sites probe and are gate-pinned (K1 is RETIRED by this diff; its old
  gate check would read 0, which is why the gate edit is forced).

## 3. THE DIFF -- all six files, unified, generated from the PATCHED scratch copies against SEC HEAD (md5 below)

{{FILE _scratchpad/fbd5/p2/diff545_6files.patch}}

## 4. THE FULL FIXED ENCLOSING FUNCTION (DEVICE_ACCESS(footbridge), every exit path and the common tail)

{{INLINE _scratchpad/fbd5/impl/dry/src/devices/dev_footbridge.c 500 800}}

## 5. THE KILL TABLE (scratch clone /tmp/gxfbd5 of build/; PRETABLE.out written before table 1)

{{FILE _scratchpad/fbd5/impl/PRETABLE.out}}

### Measured results

{{FILE _scratchpad/fbd5/impl/TABLE_SUMMARY.md}}

## 6. QUESTIONS (answer all; number them)

Q1 THE PREMISE AUDIT.  Every load-bearing premise in sections 1-2, stated as a question: TRUE / FALSE / NOT CHECKABLE,
   with the anchor that settles it.  In particular: does the fixed function's common tail still run for every declined
   access (odata 0 for the read, `return 1`)?  Does any of the five arms change state?  Is the +0x18c read's leak gone?
Q2 THE SMALLEST EDIT THAT BREAKS THIS AND STILL PASSES.  Against the diff as written and the table as measured: name the
   edit, the row you expect to stay green, and why.  Candidates the table did NOT build: a `&& len == 4` conjunct on
   ANOTHER site than IRQ_STATUS (P9 covers only IRQ_STATUS); a latch cleared by a LEGAL read of a sibling register; a
   decline that stores into the OTHER family's status; an announce text that names the right register but drops
   `(once)`; a gate pin regex that a duplicated green line satisfies.
Q3 THE FLOOR.  Walk clauses (a)-(f) against the SHIPPED composite detector: (a) fails on the pre-fix build, (b) fails
   on a verbatim reinstatement at EVERY site (the table reinstated ONE), (c) fails on a null medium, (d) DEPENDS-ON
   closure -- enumerate the predicates dominating the edited lines (the five latch tests, `writeflag`) and the
   operand-swap forms drawn from the bodies' read fields; (e) is the contract's disclosure list complete and honest;
   (f) is any row relative-only (anchored?).  A breach is L2 -- say so plainly.
Q4 THE HARNESS LEGS.  Do H1/H2 as implemented in the THREE launchers establish what the kill arm established?  Read
   each launcher's H2 code path: is `dead` observed BEFORE teardown in all three?  Is the prologue verification scored
   (drain/witness: `bad` empty, `len(ex) == PROLOGUE_N`, four register values)?  Does the sites probe's `send()` now
   forward its timeout, and does anything else in the tree depend on the old form?  Name the smallest edit to a leg that
   leaves it green while proving nothing (the table measured "omit quit" and "any nonzero exit"; what else?).
Q5 OPTION-SET AND RECORDS.  Is member 3 still the right disposition given what pass 2 sees?  Is anything in the
   comments or the probe header a WRONG RECORD (a claim the diff or the table refutes)?  Row counts: the differential's
   IDENTITY pin is 111 -- enumerate the P-rows to check it.
STANDING LICENCE: if, while verifying a claim, you found something ELSE -- say so.

End with a seat record: model, files read (with their md5 if you can compute one), nothing run / what you ran.
