# i8259eoiirr (#574) -- pass-2 (the diff review) rulings of the main loop, 2026-10-25 09:0x, BEFORE the F2b adjudication

Six answers (`codex_t19p2.txt` 12,988 b DO NOT SHIP; `grok_t19p2.txt` 13,362 b SHIP WITH CHANGES; `ollama_glm_t19p2_Q12/Q34.txt`
7,909 / 6,849 b SHIP WITH CHANGES; `ollama_deepseek_t19p2_Q12/Q34.txt` 2,528 / 4,323 b SHIP WITH CHANGES).  No wall, no echo, no
burn (tails read).  Argon OWED (job dirs built; the sender sleeps to 12:32); Fable HELD (FABLE_HOLD_QUESTION.md); kimi/minimax/Opus
seat not fired by roster (SEATS_NOT_FIRED_20261025.txt); agy walled.  Count the arguments: the two instrument defects below were
each found by two or more seats independently; the design itself drew no overturn from any seat that could read the tree.

## Findings on the DIFF (product code) -- none required a change to the shipped design
P1  (Astra Q1(i), Grok (i), GLM (i), DeepSeek (i))  `d->isr & bit` is the right in-service discriminator for the contained model:
    the helper is the only setter (idempotent), both EOI arms only clear.  Astra's refinement accepted: a second acknowledge of the
    same line before its EOI is permitted (no priority inhibition, `i8259priority`), so one EOI clears the bit and a second EOI takes
    the legacy branch -- a consequence of the deferred priority defect, disclosed.  [accepted; no edit]
P2  (Astra (ii), Grok (ii), GLM (ii), DeepSeek (ii))  One-shot poll: no documented guest re-reads the command port without another
    OCW3; the revert to the IRR is the approximation the F2 record already flagged.  GLM Q34 (4): the chip reverts to the LAST RR/RIS
    selection, not to the IRR -- a guest that selected the ISR read, polled, and re-read would see the wrong register.  [accepted as a
    disclosed approximation; both documented guests re-select explicitly; recorded in the contract; no edit]
P3  (Astra (iii), DeepSeek (iii) NOT CHECKABLE; Grok (iii) SETTLED)  The GT read returns the LINE: Linux programs ICW2 bases 0 and 8
    (`I8259A_IRQ_BASE` 0) and dispatches `do_IRQ(MALTA_INT_BASE + irq)` on the raw IACK byte, so the byte IS the line; `last_int`'s
    convention is kept; adding the model's `irq_base` would double-offset the dispatch.  [accepted on Grok's reading of the Linux
    source; the model's `irq_base` stays write-only (filed note in `i8259ocw2nonspec`'s neighbourhood: none)]
P4  (Astra Q3(c), Grok Q3(c) -- both walked bus_isa.c; GLM Q34 (c) and DeepSeek (c) NOT CHECKABLE)  The fold-free diff handles two
    pending slave requests: the slave acknowledge asserts pic2's irq = the ISA line-2 path; `isa_interrupt_assert` samples the master
    mask BEFORE setting bit 2, `isa_interrupt_common` sees the transition and raises the CPU line.  CHECKED by the main loop before
    the edit (bus_isa.c 52-112).  [accepted; the two packet-fed dissents were unable to open the file and said so]
P5  (Astra Q3(b), Grok, GLM, DeepSeek)  Lowest-numbered set ISR bit = highest priority in fixed mode.  [accepted]
P6  (Astra Q3(d), Grok, GLM)  `pic1 == NULL` (MVME5500) reachable and guarded; `n2 < 0` unreachable while the fold invariant holds;
    the total-function value 2 is right (hardware's spurious IR7 is not modelled; disclosed).  [accepted]
P7  (Astra Q1 2.5, GLM Q34 (a), DeepSeek (a))  "Unconverted machines behave as HEAD" holds only where no guest POLLS: the poll read
    now acknowledges on every machine, so a PReP/footbridge guest that polls would enter the ISR branch (a fix, not a regression).
    [accepted; the sibling `i8259isrnever` NARROWS, does not close]
P8  (Astra Q5)  The GT change reaches Cobalt's GT64011 (its machine creates ISA PICs); whether a Cobalt guest reads the IACK register
    is NOT CHECKABLE here.  [accepted; disclosed in the contract and the row's state note]
P9  (Astra Q5, GLM Q34 (c))  ISR lifecycle: ICW1 does not reset ISR or `current_command`; ICW4 AEOI is unsupported while the helper
    always sets ISR (an AEOI guest would accumulate ISR bits; the output never consults ISR, so no line is lost).  [accepted; FILED
    `i8259aeoi` (LOW) and `i8259icwreset` (LOW); not this round's edit]
P10 (GLM Q34 Q5 (3))  Special mask mode (OCW3 0x68, an empty TODO arm) vs the helper's `~ier`.  [accepted as a note on `i8259ltim`'s
    neighbour; filed with `i8259aeoi`]

## Findings on the INSTRUMENT -- two defects REPAIRED before the measurement of record (L1, pre-ship construction)
I1  (Astra Q2, Grok Q2+Q5, GLM Q12 Q2 -- three seats)  `poll once` as built in v2c was VACUOUS: the second poll ran with nothing
    pending, so a sticky poll of an empty IRR and an IRR read both return 0x00; M_sticky would have escaped a row the PRETABLE
    predicted as its kill.  REPAIR (v2d): the one-shot row moves to the MASKED session -- the masked poll acknowledges nothing, the
    request stays pending, the next command-port read returns the IRR 0x10 (one-shot) vs 0x00 (sticky) vs 0x84 (HEAD).  The v2c
    row stays under the honest name `poll again`.  PRETABLE.out carries the correction in place.
I2  (Astra Q2, Grok Q2+Q5)  No row pinned the GT read's RETURNED LINE: dropping `if (n >= 0) odata = n;` leaves `last_int`, and the
    single-source rows agree with it.  REPAIR (v2d): the session `gtboth` (UART IRQ 4 and RTC IRQ 8 pending together): the
    acknowledge returns 8 (line 2 outranks 4), HEAD's flat scan returns 4; mutant D_gt_noassign added to the table.
I3  (GLM Q12 Q2)  The retire guard `d == p->pic1 && n == 0`: dropping either conjunct is observable only through a race between a
    host-timer fire and the next tick (a UART or RTC acknowledge landing inside the window before the 8253's own tick asserts), so no
    deterministic row exists.  [DISCLOSED under clause (e) with the derivation, in PRETABLE.out and the contract; not rowed]
I4  (GLM Q12 Q2)  The helper's final recompute replaced by an unconditional DEASSERT escapes every register row and the single-line
    rate row; it is the CPU-line class the owed `i8259cascline` row covers.  [disclosed; filed with that row]
I5  (Astra Q4(e), GLM Q34 (e))  The pass-1 witness is SUPERSEDED, not wrong: it measured a disclosed different protocol; cite
    `witness_20261025b/` (and `witness_20261025c/` for v2d) as the oracle pin, `witness_20261025/` as history.  The v2 -> v2c -> v2d
    row additions had their HEAD column pinned on the base clone at 08:27 and in the v2d cycle; named explicitly in the records.
I6  (GLM Q12 2.8)  The rate band guarantees a 5x separation at its boundaries (>= 5000 vs <= 1000); "two orders of magnitude" is the
    measured gap (7,992 vs 4), not the guard.  [wording corrected in the probe docstring and the records]
I7  (GLM Q34 (b))  The storm count is cited as three numbers -- 7,415 (`rate_explore_20261025/rate_073912`), 7,397
    (`witness_20261025b/`), 7,992 (`fixlegs_082756/`): each names its artifact in the records.  [applied]

## Records corrections (L4, in place)
R1  (Astra Q4(e))  The pass-1 witness ran at 06:51 (WSL clock; `witness_20261025/RESULTS_base.txt`), not 03:49 -- corrected in the
    drafts and the generator.
R2  (Astra Q1 2.3)  The pass-2 brief cited "F2_RULINGS 1.7/1.8" for the guest-source quotes; they live in `f2_20261025/F2_PACKET.md`
    sections 1.7/1.8.  The brief is sent; the F2b packet names the right file.
R3  (Astra Q1 2.7, Q4(e))  "Before the code moves" overstated the order: the fix clone was built 07:56, the re-pinned probe first
    ran on HEAD 08:01; what every FIX measurement follows is the HEAD run.  The probe docstring and F2_RULINGS A3 say so now.
R4  (Astra Q1 2.8)  "A timer that never fires": the clamp is 1e-8 Hz -- "does not fire within any run" is the honest sentence
    (`pit8253count0`).

## The ruling taken to F2b
SHIP WITH CHANGES (the instrument's two repairs, both measured in the v2d cycle; the records corrections) -- against Astra's DO NOT
SHIP, whose three grounds are: the one-shot coverage claim (REPAIRED, I1), GT consumer compatibility (SETTLED by Grok's reading of
the Linux dispatch, P3; Cobalt disclosed, P8), the provenance record (CORRECTED, R1-R4).  The diff itself is unchanged by pass 2.
