# i8259eoiirr (#574) -- F2b (the adjudication of pass 2) rulings of the main loop, 2026-10-25 11:1x

Six answers, all RATIFY WITH CHANGES: `codex_t19f2b.txt` (GPT-6 Astra, ADJUDICATING; WRONG: F3 F13 D1 D3 D5), `grok_t19f2b.txt`
(WRONG: none), `ollama_glm_t19f2b_A.txt` / `_B.txt` (none overturned; D2/D3/D5 refined), `ollama_deepseek_t19f2b_A.txt` (WRONG:
F14) / `_B.txt` (D3 refined).  No wall, no echo, no burn (tails read; every answer read in full).  Argon OWED (job dirs queued
behind the single sender); Fable HELD (FABLE_HOLD_QUESTION.md); kimi/minimax/Opus seat not fired by roster
(SEATS_NOT_FIRED_20261025.txt); agy walled.  Count the arguments, not the seats.

## The ruling of record
Astra withdrew its one-shot ground on the measured kill (`M_sticky` 83/84) and ruled RATIFY WITH CHANGES; its surviving
ground is EVIDENCE for D3 (below), plus instrument cells.  **The product diff is unchanged by F2b: no seat asked for a product
edit before landing** (Astra: "No inspected evidence requires changing the supplied product diff"; DeepSeek A's F14 asks for a
ROW).  The changes are on the instrument and the records.

## Dispositions on the F2b answers
A1  D3/F3 (Astra OVERTURN, DeepSeek B REFINE, GLM B REFINE; Grok UPHOLD with a re-fetch): the packet's warrant for "the GT read
    returns the LINE" cited quotes that did not carry the ICW2 facts.  ACCEPTED as a records defect: the warrant is now Grok's
    F2b re-fetch (Linux programs ICW2 bases 0x00 and 0x08, `MALTA_INT_BASE` 0, the IACK byte masked `& 0xff`), DERIVED today by
    a seat, not by the main loop.  The conclusion stands; `irq_base + n` is a filed shape, not a diff change (GLM B, Grok).
    F3's sentence "the model's `irq_base` stays write-only" was FALSE globally -- `dev_footbridge.c:432` reads it -- and is
    corrected to "never read by dev_8259.c or dev_gt.c" (L4).
A2  F13/D5 (Astra OVERTURN, GLM B REFINE "rowable as band, declined on cost", Grok REFINE with the catch-up-loop reason, GLM A
    and DeepSeek B UPHOLD): F13 MIS-ATTRIBUTED GLM's pass-2 position -- it had asked for a banded mixed-source retirement row,
    not concluded "no row exists" (L4, corrected here and in the records).  The disposition becomes: no DETERMINISTIC row
    exists (Grok: timer.c's catch-up loop can deposit several counts before the guest sees IRR bit 0); a BAND row is
    constructible (GLM B's construction: mask IRQ 0, wait for two host fires, acknowledge the RTC, unmask, count deliveries);
    declined this round on cost and load sensitivity; FILED `pit8253retireguard` with the construction.  The two guard
    mutants are MEASURED against v2d (section below), as the disclosure requires.
A3  F14 (DeepSeek A OVERTURN "row before ship"; Astra REFINE "the two-slave row does not cover a bare DEASSERT"; Grok: the bare
    DEASSERT passes all 84 rows and drops the CPU line with a second request pending): ACCEPTED as a floor cell -- the
    recompute `d->irr & ~d->ier` is a predicate the fix ADDS, and an unconditional DEASSERT is its constant-false weakening.
    ROWED in v2e as `nonspec ip2` (CP0 Cause bit 10 read right after the acknowledge of line 3 with line 4 pending: 1 in both
    columns; a bare DEASSERT reads 0).  The two-SLAVE-request stall (D_fold) stays the owed `i8259cascline` row: `nonspec ip2`
    sees only the master-side recompute.
A4  Astra Q3.1-Q3.3 (three unrowed cells: a specific EOI clearing the whole ISR; the Linux mask-then-EOI order -- ISR set AND
    mask set at the EOI; the one-shot latch after a SUCCESSFUL poll): ACCEPTED, each measured as a mutant against v2d first
    (`B_spec_isr0`, `D_eoi_maskcond`, `D_latch_cond`) and ROWED in v2e: the `speceoi` session (`spec eoi one`), the `maskeoi`
    session (`maskeoi isr`), and `poll once2` in the nonspec session (a command-port read with no OCW3 after the SUCCESSFUL
    poll of line 3 with line 4 pending: FIX 0x10 / HEAD 0x83 / latch-on-failure-only 0x84).  The class is closed in ONE
    instrument diff (the DEPENDS-ON cells of the fix's three added predicates: `d->isr & bit` x the mask; the latch x poll
    success; the recompute x a second request), per the repair-chain amendment.
A5  GLM B Q3.6 (D_gt_write is rowable: a WRITE to the IACK address, then the ISR) -- ACCEPTED: `gt write isr` in the gt session
    (0x00 both; a write that acknowledges reads 0x10).  The main loop adds the nothing-pending cell of the GT read
    (`quiet iack`: last_int 0 both; `odata = n` unconditionally would read 0xffffffff), measured as `D_gt_always`.
A6  Grok Q2/Q3, DeepSeek B, GLM B Q3.5, Astra Q3.4 (the both-columns device-value rows are CONTRACT rows, not controls; a
    CONTROL=FAIL on them misreads a kill as an instrument failure) vs GLM A (keep CONTROL, label the kill): ACCEPTED the
    majority BY ARGUMENT -- the probe's own definition says control = the instrument's liveness/signature, and a poll byte is
    a model value.  v2e relabels `poll byte`, `poll3 byte`, `poll first`, `casc poll`, `casc slave poll`, `pit poll`, `gt iack`,
    `gtcasc iack`, `rate poll byte` (and the new `quiet iack`, `maskeoi poll`, `spec polls`) as contract.
A7  GLM B Q3.1 (the rate row "deliveries" cannot be right; the FIX side has no cadence floor): REJECTED on the mechanism -- the
    rate count IS the guest handler's entry count (`s2`, incremented per delivered interrupt; the handler polls and EOIs), not
    the 8253's pending count; FIX 3-4 deliveries in 180M instructions is one per host-timer fire during a run of about a
    second at 18 Hz after the counter is programmed (the first fire comes a period late), and the band `1..1000` is a guard, not
    a cadence claim.  The cadence question is real and FILED with `pit8253retireguard` (the same band-row instrument would
    measure it); the "retire too eagerly" edit it names is exactly `D_retire_anypic`, measured below.
A8  GLM B Q3.3 (special mask mode: NetBSD sets OCW3 0x68 at attach; the diff's comment says edge is "the only mode" the guests
    program): ACCEPTED as a filing (`i8259smm`, LOW): the acknowledge ignores SMM as HEAD did, and with no ISR priority
    inhibition the delivered set is unchanged; the comment's "mode" is ICW1's trigger mode, which stays true.
A9  GLM B D2 (file the revert-target approximation): ACCEPTED, `i8259ocw3revert` (LOW).  Astra D2 (the datasheet qualifies the
    remembered selection for polling, 8259A.txt:649): noted in the filing.
A10 Records (Astra F21: section 2.8 of the copied facts still says "never fires"; GLM A F16: the copied 2.8 still says "two
    orders of magnitude"; GLM B: "split 1-4" counts five answers from three seats; "both edited files" against three hashes):
    all ACCEPTED as L4 -- the CHANGELOG block carries the corrected sentences; the packet copies stand as sent and are
    corrected here.
A11 Astra Q3.5 (the probe's "re-asserts every tick" claim is false for the pckbc, which suppresses repeated assertions while
    asserted): ACCEPTED -- the docstring's sentence is narrowed to the ns16550s and the 8253 (the devices the rows drive).
A12 Astra F7/F9 refinements (compatibility claims scoped to non-polling unconverted paths; live ISR makes the init omissions
    consequential): ACCEPTED as wording; `i8259icwreset` carries the second.  Astra F17/F18 (older counts and the 06:51 stamp
    need their original artifacts): the artifacts exist (`rate_explore_20261025/rate_073912`, `witness_20261025/RUN_IDENTITY.txt`
    "2026-10-25 06:52:26") and are cited; nothing further owed.

## Measured against the v2d instrument BEFORE the repair (the floor says a breach is measured, never inferred)
Seven candidate mutants built from the fix clone with the frozen v2d probe in GATE mode (`run_extra19.sh`, scratch clones,
banked as `killtable_20261025/table_v2d_extra/`): see `SCORES.txt` there -- the per-mutant verdicts are appended below when
the table completes, and the v2e rows that answer each escape are named there.

MEASURED 11:04-11:23 (`run_extra19.sh` -> `/tmp/gxt19/killtable_v2d_extra_110448`, banked as `killtable_20261025/table_v2d_extra/`):
**ALL SEVEN ESCAPED the v2d instrument, 84/84 with CONTROL OK each** -- D_eoi_maskcond, D_latch_cond, B_spec_isr0, D_deassert,
D_gt_always (the five cells F2b named: four clause-(d) weakenings of predicates the fix ADDS and one body shape), and
D_retire_anypic / D_retire_anyline (the two DISCLOSED cells of D5, measured as the disclosure requires).  The five are floor
breaches of the shipped-to-be detector (L2: repaired in-round, not filed) and are ROWED in v2e -- `maskeoi isr`,
`poll once2`, `spec eoi one`, `nonspec ip2`, `quiet iack` -- plus `gt write isr` for the v2d-disclosed `D_gt_write`; the two
retire-guard cells stay disclosed (`pit8253retireguard`).  The repair's own pass (F2c) follows the v2e cycle and the v2e table
of record; `PRETABLE.out` carries the v2e block, appended before that table ran.

CORRECTION (11:4x): A6 listed `spec polls` among the relabelled CONTRACT rows.  Its columns differ (HEAD 0x8383 / FIX 0x8384),
which the v2e L0 leg showed (legs_113314: red as a contract row); it is a SYMPTOM row in v2f.  The v2e cycle (witness_20261025d
101/101 on HEAD; fixlegs_112709 101/101 both legs; legs_113314 L0 75/101, L3 0/101) stands as the measurement of v2e; v2f differs
from v2e by that one kind label and is re-measured in full before the table of record.
