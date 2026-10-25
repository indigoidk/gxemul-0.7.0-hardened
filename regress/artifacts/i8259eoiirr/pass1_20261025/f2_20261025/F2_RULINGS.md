# i8259eoiirr (#574) -- F2 (the adjudication of pass 1): the rulings of record, 2026-10-25 07:5x

The ruling of record is GPT-6 Astra's (`codex_t19f2.txt`): **NOT RATIFY -- (G) has delivery and accounting gaps, and its
proposed detector does not establish the claimed coverage.  WRONG: F12, F13, F20, F22, D2, D3.**  Provisional until the
roster completes (Argon owed; Fable held).  The other five answers: Grok RATIFY WITH CHANGES (WRONG: none; three required
changes), GLM A/B RATIFY WITH CHANGES (F3/F12 refined; four §4 changes), DeepSeek A/B RATIFY WITH CHANGES (D3's warrant
false; the cascade recompute).  Every seat upholds D1 (reject (A) alone) and the acknowledge member; every seat rejects
the §4 SKETCH as written.  Count the arguments: the three defects below were each found by two or more seats
independently.

## Roster record

| seat | answer | verdict |
|---|---|---|
| GPT-6 Astra (ADJUDICATES) | `codex_t19f2.txt` 14,190 b | NOT RATIFY; WRONG F12 F13 F20 F22 D2 D3 |
| Grok 4.7 | `grok_t19f2.txt` 12,141 b (a 195-byte opening line for 17 minutes, then the answer -- mid-answer, not dead) | RATIFY WITH CHANGES; WRONG none |
| GLM 5.3 A / B | 8,220 b / 8,229 b | RATIFY WITH CHANGES (A: F3, F12 refined; B: D4 refined, four §4 changes) |
| DeepSeek A / B | 2,452 b / 2,197 b | RATIFY WITH CHANGES (A: F1, F23 CANNOT SETTLE; B: D3 refined) |
| Argon (web route) | OWED -- `argon_api_A/`, `argon_api_B/` queued; the single sender sleeps until the meter's 12:32:15 reset | -- |
| Fable 5.1 | HELD -- `FABLE_HOLD_QUESTION.md` | -- |
| agy; kimi; minimax; Opus seat | not fired (wall; roster) -- `SEATS_NOT_FIRED_20261025.txt` | -- |

No wall text, no echo, no burn (tails read; the one grep hit in Grok's file is the word "quota" inside its own prose).

## The dispositions adopted (each with what changed as a result)

A1  **G2's manual cascade fold is deleted** (Astra Q3.1, Grok Q3, GLM B change 2, DeepSeek B Q3 -- four seats).  The
    helper writes `pic1->irr` bit 2 itself and then asserts/deasserts `d->irq`; for pic2 that irq IS the ISA line-2 path
    (`bus_isa.c:232`), whose `isa_interrupt_assert` samples the old mask BEFORE setting the bit and whose
    `isa_interrupt_common` returns when the mask did not change -- so the pre-fold swallows the transition and a second
    pending slave request is stranded with the CPU line low.  The helper now only asserts/deasserts `d->irq`; line 2's
    existing assert/deassert does the fold.  CHECKED by reading `bus_isa.c:52-90`; the patch script already carried the
    fold-free form.  Cascade row R9 is IN the round (GLM B change 4: under (G) the fold is the only drain of bit 2).
A2  **The acknowledge happens ONLY on a read with `current_command == 0x0c`, and the poll latch is ONE-SHOT** (Astra
    Q3.3, Grok Q3, GLM B change 1): the `default` read arm (the zero-filled initial state, any guest's first read of port
    0) stays byte-identical to HEAD and consumes nothing; after the acknowledging read `current_command` reverts to 0x0a
    (the datasheet: the NEXT read after P=1; "after initialization the 8259A is set to IRR").
A3  **The EOI keeps a LEGACY consume where no acknowledge preceded it** (Astra F20/D2 OVERTURN: "deferring other IACK
    consumers does not contain the shared EOI change"; Grok D2: "either this edit calls the helper from dev_prep.c:57 and
    dev_footbridge.c:432, or the EOI keeps a legacy consume when that line's ISR bit is clear").  Adopted: the HYBRID.
    Specific EOI for line n: if ISR bit n is SET (an acknowledge moved the request to service) -> clear ISR only; else
    (no acknowledge on this line: PReP, footbridge, Algor, any guest that EOIs without polling or IACK-reading) -> the
    request bit is consumed exactly as on HEAD, with HEAD's recalc.  CHECKED: `dev_footbridge.c:432-436` returns
    `pic->irq_base + last_int` with no acknowledge; `dev_prep.c:57` returns `last_int`.  Converting those two readers is
    NOT in this round (no witness machine; the hybrid contains the change); filed `isaiackreaders`.  Consequence for the
    witness: the pass-1 symptom rows `eoi irr4` / `eoi x8` (an EOI with NO preceding acknowledge) now want the LEGACY value
    in the FIX column too -- the oracle is RE-PINNED FIRST and HEAD measured red on the NEW symptom rows before the code
    moves (the oracle-correction rule).
A4  **Non-specific EOI (0x20) clears the LOWEST-NUMBERED set ISR bit, not all of them** (Astra Q3.4, GLM B Q3): with ISR
    live, `isr = 0` is wrong on the datasheet (the highest-priority in-service bit).  With no ISR bit set it does what HEAD
    did on IRR (nothing).  Priority INHIBITION (ISR masking equal/lower requests) is NOT implemented -- filed
    `i8259priority`; the CPU line stays `irr & ~ier`.
A5  **G4 is read-only, NULL-safe and total** (Astra Q3.7, Grok Q3, GLM B change 3): the GT IACK case acknowledges only
    on `writeflag == MEM_READ`; `pic1 == NULL` (MVME5500 instantiates the GT with no ISA PICs, `machine_mvmeppc.c:98-102`)
    returns `last_int` as before; `n == 2` with no slave request returns 2; the returned value is the LINE (0-15), as
    `last_int` is today -- never `irq_base + n`.
A6  **F22 OVERTURNED, CHECKED** (Astra): `dev_ns16550.c` calls `dev_ns16550_tick(cpu, d)` from its access function
    (:171, :200, :216, :290), so a serviced UART deasserts SYNCHRONOUSLY, not on its next scheduled tick.  Grok's F22 UPHOLD
    was wrong.  The pass-1 packet's "churn" warrant for (G) over "(A) + a line-0 special case" is withdrawn; the design
    rests on the acknowledge being the datasheet's consume (A3 keeps HEAD's consume where no acknowledge exists).
A7  **F12/F13 OVERTURNED** (Astra; GLM A gave the construction): rows R3/R8 as described cannot catch a reinstated IRR
    clear conditioned on `isr & bit`, because the acknowledge has already cleared that line's IRR bit.  The catching row:
    poll (ack: ISR set, IRR cleared) -> wait a UART tick (the level re-asserts: IRR set WHILE ISR set) -> EOI -> IRR read:
    fix 1, mutant 0.  That is also the row that pins the hybrid's own predicate (DEPENDS-ON: the ISR bit).
A8  **F5 REFINED** (Astra): `eoi x8` is one observation repeated eight times (the probe never re-establishes IRR between
    repetitions), not eight demonstrated clears.  Recorded; the row is renamed in the rewrite.
A9  **R6(c) DROPPED** (Astra Q3.5): the host timer base is 65 Hz and batches elapsed periods, so several 8253 events can
    be pending at the first visible assertion and one acknowledge need not empty the backlog -- "IRR bit 0 reads 0 after a
    short wait" has no established invariant.  The retirement is pinned instead by the RATE row (`rate_explore_20261025`:
    a band separated by two orders of magnitude) and by R6(a)/(b).  The decrement's read-modify-write against the
    SIGALRM-side increment is the house idiom (`dev_mc146818.c:80/111/563`, `dev_gt.c`, `dev_jazz.c` do the same); the
    8253's field is not `volatile` where mc146818's is -- recorded, not changed.
A10 **D3 refined** (Grok, DeepSeek B, Astra): edge-only with `i8259ltim` filed stands; the "no guest sees a new shape"
    warrant is withdrawn -- a device re-assert between the acknowledge and the EOI leaves IRR set after the EOI (an
    immediate second interrupt HEAD's consume would have swallowed).  Disclosed in the contract as the held-level
    re-request (more generous than edge hardware, never less).
A11 **D5 upheld with Astra's wording**: MED WRONG-RESULT, one row, exposure rewritten to the EOI consume, the 8253 rate
    (a coupled acknowledgment/accounting defect; `pit8253pendingptr` records the dead pointer) and the mask-blind poll.
A12 **Floor (b) enumerates every edited site** (GLM B D4): the two EOI arms (the IRR clears AND the recalc blocks), the
    0x0c read arm, the GT IACK read, the helper -- each with its verbatim reinstatement.  R1's masked poll needs a VERIFIED
    pending request (no earlier unmasked poll in that session).
A13 Records: F1/F23 content accepted on two file-reading seats (DeepSeek: NOT CHECKABLE from a packet -- right); F16's
    `for (;;)` was quoted from the fetched source, not re-fetched by the seats; F26 (Argon) stays owed.

## The design as it goes to the implementation: (G') "acknowledge, contained"

 G1' the specific-EOI arm: `bit = 1 << (idata & 7); if (d->isr & bit) d->isr &= ~bit; else { legacy consume: old_irr =
     d->irr; d->irr &= ~bit; recalc as HEAD }`.  The 0x20 arm: clear the lowest set ISR bit if any; nothing else.
 G2  the helper, fold-free (as in the patch script).
 G3  the 0x0c read arm acknowledges and reverts `current_command` to 0x0a; `default` untouched.
 G4  the GT IACK read: read-only guard; NULL pic1 -> `last_int`; master 2 then slave; `n2 < 0` -> 2.
 Detector: rewritten rows per A3/A7/A9/A12 -- symptom rows are ACK-based (poll acks; masked poll; eoi after ack with a
 re-asserted level; the 8253 rows (a)/(b); the RATE row); the un-acknowledged EOI rows become CONTRACT rows (legacy).

## Where this record might be fooling itself
 * (G') converts no `last_int` reader but the GT's; the hybrid's claim "unconverted machines behave as HEAD" is a reading
   of `dev_8259.c`'s arms, measured only on malta.
 * The datasheet's one-shot poll semantics is applied to a model whose `current_command` latch has no P bit; "revert to
   0x0a" is the chosen approximation.
 * The 8253 rate on PReP/footbridge/Algor machines keeps HEAD's storm (their EOIs consume as before; no retire) --
   pre-existing, disclosed, not a regression.
