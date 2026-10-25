# i8259eoiirr (#574) -- F2d (the class-closure verification pass) rulings of the main loop, 2026-10-25 16:0x

Six answers, all read in full: `codex_t19f2d.txt` (GPT-6 Astra at ultra, ADJUDICATING, pointer form: RATIFY WITH CHANGES -- zero
breaches with the denominator; two enumeration mappings, a chronology correction, three disclosure wordings, two record
corrections), `grok_t19f2d.txt` (Grok 4.7 xhigh, plan mode: RATIFY -- zero breaches; defends the retire-guard ">= 2" disclosure),
`ollama_glm_t19f2d_A.txt` (GLM 5.3, packet A: RATIFY WITH CHANGES -- one unlisted retire-guard cell; six rows "missing" from the
diff; the n2 < 0 warrant not settleable from the packet), `ollama_glm_t19f2d_B.txt` (GLM 5.3, packet B: RATIFY WITH CHANGES -- the
retire-guard cells constructible with count == 1; the revert-target disclosure names no mechanism; D_nonspec_high not built),
`ollama_deepseek_t19f2d_A.txt` and `_B.txt` (DeepSeek v4-pro: RATIFY, zero breaches, the enumeration swept cell by cell).  No wall,
no echo, no burn.  Argon: web-route jobs `argon_api_A/` and `argon_api_B/` CREATED and QUEUED behind the single sender (OWED by the
late-dissent rule); agy (Argon's file-reading transport) quota-walled; Fable HELD (`FABLE_HOLD_QUESTION.md`); kimi (both
transports), minimax and the Opus review seat DELIBERATELY NOT FIRED under the owner's roster (`SEATS_NOT_FIRED_20261025.txt`).
Evidence basis of this ruling: 6 of the 6 roster seats that fire; provisional only with respect to Argon's queued answers.

**THE CHAIN CLOSES ON THIS PASS.**  No seat produced or named a NEW measured clean-sweep mutant; the three escapes of the table of
record (`D_fold`, `D_retire_anypic`, `D_retire_anyline`, 123/123 each) are the three disclosed since F2b, and every other cell of the
enumeration carries a row whose red under its mutant is in `killtable_20261025/SCORES.txt`.  Denominator (Astra's, cross-checked
against Grok's, GLM A's, GLM B's and DeepSeek's sweeps -- they agree cell for cell): acknowledge {pending == 0; scan one line / two
lines; ISR set; IRR cleared}; the retire guard {(pic1, line 0, count > 0); (pic1, other line); (pic2, line 0); (pic2, other line) --
ADDED by D2 below; ptr NULL; count == 0}; the recompute {unmasked remains; nothing remains; only masked remains}; the poll byte
{nothing; a line}; the one-shot {after success; after failure; the revert target}; the specific-EOI predicate {in service unmasked;
in service masked; not in service alone; not in service with another; masked and not in service} and its body; the non-specific arm
{lowest; highest -- unbuilt, D6; empty ISR -- D4}; GT {writeflag; pic1 NULL; n == 2 && pic2 (cascade; non-cascade with slave work;
non-cascade without slave work -- D4; pic2 NULL); n2 >= 0 / < 0; n >= 0 / < 0}.

## Dispositions

D1  **The retire-guard pair (Astra; GLM B; Grok dissenting; GLM A).  The disclosure's WARRANT IS WITHDRAWN; the two cells are
    re-graded from "clause (e), disclosed" to OWED REPAIR, held by a classifier stop.**  The record said (PRETABLE.out v2g block,
    the probe docstring, the F2b/F2c rulings, the filed row `pit8253retireguard`): *"observable only with a pending count >= 2,
    which only host time produces"*.  Astra and GLM B each derived the count == 1 construction independently: one 8253 event in
    (the `pit` session's own wait), line 0 MASKED by OCW1, a foreign acknowledge (another master line by the poll, or the slave's
    line 0 through the GT cascade), then the LEGACY specific EOI of line 0 (not in service -> HEAD's consume, which clears IRR bit 0
    without retiring), then the next device tick: the fix (count still 1) re-asserts line 0, the mutant (count retired to 0) does
    not -- read in IRR bit 0.  CHECKED against the source: `dev_8253.c:118-129` -- `DEVICE_TICK(8253)` asserts the line on EVERY
    tick while `pending_interrupts_timer0 > 0`, with no deassert and no once-only flag; `fixsrc/dev_8259.c:76-78` retires only
    inside `pic8259_acknowledge`, so the legacy consume does not retire; the tick loop advances under single-stepping
    (`machine.c`: `ticks_till_next[te] -= single_step ? 1 : N_SAFE_DYNTRANS_LIMIT`), so the 8253 tick fires after a bounded
    number of steps.  Grok's defence -- *"then acknowledging line 0 ends at 0 for both"* -- assumes the next event
    on line 0 is an ACKNOWLEDGE; the construction clears the request through the legacy EOI instead, which is the path Grok's
    argument does not visit.  GLM A's derivation of the ">= 2" rationale makes the same assumption.  So: reachable cells of a
    body-tested conjunct of a predicate the fix adds, with measured escapes (123/123) and an observable the probe's own
    techniques reach -- the clause-(d) floor by its letter.  **THE REPAIR WAS ATTEMPTED AND CLASSIFIER-STOPPED (15:5x, the main
    loop reading the probe's session builders toward the two rows); per the standing rule for a stopped attempt (owner ruling
    2026-10-25 item 5: stop and report, never retry; memory `gxemul-panel-benign-framing`: hold it, file the measurement as
    owed, the #567 precedent) it is NOT retried in this round.**  #574 lands on v2g with the pair recorded as OWED REPAIR -- not
    as a disclosure that closes the cell -- carried by `pit8253retireguard` (re-worded: the construction in words, the grade,
    the stop), and named in the CHANGELOG's record as debt with its reason.  Astra's own disposition ("retain the disclosed
    timing debt, reject the >= 2 necessity") is adopted in substance and sharpened in grade: the setup needs one host-timer
    event, exactly as the shipped `pit` session already does, so "host-timed" no longer distinguishes this row from a shipped one.

D2  **The (pic2, line != 0) retire-guard cell is UNLISTED (GLM A).  ACCEPTED, L4: added to the enumeration by the PRETABLE
    correction.**  Its disposition is its neighbours': no single-conjunct mutant fires only there (it needs both `d == pic1` and
    `n == 0` dropped, which also fires at the two disclosed cells); observable by the D1 construction with the slave's line != 0
    acknowledged through the GT cascade -- OWED with D1's pair under `pit8253retireguard`.

D3  **Six rows "not in the packet" (GLM A finding 1; GLM B (e)).  REFUTED; the packet's "every hunk inlined" is true.**
    CHECKED: the v2f -> v2g diff has 14 hunks and all 14 are in `F2D_PACKET.md`; the 22 new rows are 16 explicit tuples plus the
    SIX LIVENESS rows the row generator emits per session (`ram` and `stable` from every session's register map,
    `regress/i8259_eoi_probe.py:901` `build_rows`; three new sessions x 2) -- the same pattern F2c's C7 recorded for v2f (13 + 4).
    Records: the packet should have said so (the F2c packet made the same omission); the CHANGELOG's row arithmetic names the
    generated rows.

D4  **Two enumeration mappings (Astra).  ACCEPTED, L4, PRETABLE correction:** (i) the non-specific arm with an EMPTY ISR is a
    no-op in both columns (HEAD's `isr = 0` on an all-zero ISR; the fix's lowest-bit clear finds no bit) -- disclosed at PRETABLE
    1.a since 08:1x, now carried into the v2g enumeration; (ii) "non-cascade acknowledge WITHOUT slave work" maps to the `gt`
    session's rows (line 4 acknowledged, slave ISR 0), `gtmask` being the distinct case WITH slave work pending.

D5  **The chronology (Astra).  ACCEPTED, L4.**  The packet's section 4 ("in this order") and F2C_RULINGS.md:31/:58 ("MEASURED
    first against v2f") overstate the order.  Measured from the artifacts: the v2f-extra sweep ran 13:23:36 - 13:42:08
    (`table_v2f_extra/SCORES.txt` header and `# done`); the v2g re-pin on unmodified HEAD started 13:23:56
    (`witness_20261025f/`, run dir `v2_witness_132356`, banked 13:27:36) and both legs 13:27:36 (`fixlegs_132736/`, banked
    13:34:57) -- CONCURRENT with the sweep, on separate scratch clones.  What holds: the shapes were named by F2c (13:03-13:25) and
    measured against the unchanged v2f instrument; the sweep COMPLETED (13:42:08) before the enumeration block (13:42:29) and
    the table of record (13:43:16); the oracle-correction order (the re-pin on HEAD before any FIX measurement of the same
    revision: 13:23:56 before 13:27:36) is intact.  The measurement values are unaffected.

D6  **`D_nonspec_high` not built (GLM B (c); Grok "that disclosure is honest").  ACCEPTED as DEBT, clause (e):** the arm's
    "highest instead" shape is a body effect, not a predicate the fix adds; `nonspec lowest` (ISR 0x18 -> 0x10) would read 0x08
    under it by arithmetic, and the measured-not-inferred rule says that is a prediction.  OWED (one mutant), filed with D1's row
    rather than built now (the stop).

D7  **B_eoi's PRETABLE description vs the mutant actually built (Astra).  ACCEPTED, L4 + a disclosure.**  PRETABLE.out:82
    prescribes *"both EOI arms' IRR clears + recalcs reinstated verbatim"*; `B_eoi.diff` edits the specific-EOI arm only
    (`@@ -161`, the ISR-branch condition), and `B_nonspec.diff` edits the 0x20 arm's ISR clear only (`@@ -145`; neither diff
    touches an `irr` line).  So HEAD's `irr &= ~isr` at the non-specific arm (a no-op on HEAD where ISR was always 0; live under
    the fix) was NOT reinstated by any mutant: clause (b) is discharged for the ISR half by `B_nonspec` 122/123 and is OWED for
    the IRR half (one mutant), disclosed, filed with D1's row.  The non-specific rows observe ISR, not a re-pending IRR bit.

D8  **The revert-target disclosure names no mechanism (GLM B (b)2; GLM A 5).  ACCEPTED, L4 wording:** the revert
    (`current_command = 0x0a` after the poll) is diff-added; its IRR-selected-prior case is PINNED by `poll once2` (a bare read
    after a successful poll returns the IRR, symptom 0x83 vs HEAD 0x10); the ISR-selected-prior case (select 0x0b, poll, bare
    read: the model answers IRR, a remembered-selection implementation ISR) is the datasheet approximation `i8259ocw3revert`
    records, rowable with the port-I/O pattern the probe already uses -- added to that row's text as the row owed with any
    implementation.  Not a predicate cell; no floor consequence.

D9  **`n2 < 0` unreachability (GLM A 4; GLM B (d)(i)).  UPHELD, warrant sharpened in the record:** CHECKED `bus_isa.c:52-90`:
    `isa_interrupt_common` re-derives pic1's bit 2 from `pic2->irr & ~pic2->ier` at the end of EVERY ISA-line event (:58-61), and
    the slave's output IS ISA line 2 (`"8259 irq=%s.isa.2"`, :231-232), so a slave OCW1 mask write (`fixsrc/dev_8259.c:261-270`
    recalculates and asserts/deasserts `d->irq`), a slave acknowledge and a slave EOI all end in that fold; nothing else writes
    pic1's bit 2.  Grok and Astra read the same lines.  GLM A's proposed both-columns row is DECLINED (a row whose channel cannot
    vary under any reachable state is the CHANNEL-line vacuity; the addition licence's "cannot hurt").

D10 **EOI-side recompute cells (GLM B (a)).  REFUTED:** the fix adds a recompute in `pic8259_acknowledge` only; the specific
    EOI's legacy branch keeps HEAD's consume + recalc byte-for-byte (`fixsrc/dev_8259.c:168-174`, PRETABLE v2g row "the legacy
    branch's recalc -- HEAD's unchanged lines"), and the ISR-only branch has no output effect to recompute.  Not a cell of the diff.

D11 **D_fold's second slave source (GLM B (d)(ii)).  UPHELD as disclosed, with the fact GLM B could not read:** malta's slave
    carries the RTC on IRQ 8 and the IDE controller on IRQ 14/15 (`bus_isa.c` wdc0/wdc1 irqs), so a second pic2 source exists
    for the filed `i8259cascline` row; the instrument drives only the RTC.  Grok's reading of pass-2 P4 (the second slave
    request re-enters `isa_interrupt_assert` through the `isa.2` path and raises the CPU line, so a register table cannot see
    the stall) is the reason the cell is a CPU-line row, as filed.

D12 **Records (Astra; GLM A):** (i) the F2c roster line in the v2g block header -- *"six RATIFY-class answers, one NOT RATIFY"* --
    is FIVE RATIFY-class plus one NOT RATIFY (six answers), corrected in PRETABLE.out; (ii) F2c C2 *"v2f rows only the first"* ->
    *"v2f directly samples only the first"* (the true/none mutants already failed two rate rows at 99/101), corrected in
    F2C_RULINGS.md; (iii) F2c C9's attribution: the coherent over-catch observation is GLM A's, Astra supplied the
    prerequisite-versus-kill distinction, corrected in F2C_RULINGS.md; (iv) the companion rows `maskrem irr after`,
    `isrother isr`, `gtmask isr` stay green under their cells' mutants and are precondition witnesses, never kills (the SCORES
    reds already say so); (v) the `mfc0` insertions: the supported claim is "no old row regressed in these runs", not
    invariance under every tick phase; (vi) `pit ip2` establishes an empty unmasked request set after the retire, not an
    observed empty timer backlog -- `D_noretire` is killed by `rate storm`; (vii) the drafts' `rate_explore_20261025/` citations
    were patched to `pass1_20261025/rate_explore_20261025/` at 15:3x (Astra's NOT CHECKABLE item), and the probe docstring's
    ">= 2" sentence (`regress/i8259_eoi_probe.py:124-126`) is a WRONG RECORD in the shipped copy, left as measured (byte identity
    with the frozen copy) and corrected by the PRETABLE note; it goes with the `pit8253retireguard` repair.

## What this pass changes
Nothing in product code or in the instrument.  Records only: the PRETABLE correction (D1, D2, D4, D5, D7, D12.i), two F2c
corrections (D12.ii-iii), the `pit8253retireguard` and `i8259ocw3revert` row texts (D1, D2, D6, D7, D8), the CHANGELOG's record.
Owed, by name, all under `pit8253retireguard` unless stated: the two retire rows (D1) and the (pic2, line != 0) cell (D2) -- the
repair; `D_nonspec_high` (D6); the non-specific arm's IRR-half reinstatement mutant (D7); the ISR-selected-prior revert row (D8,
under `i8259ocw3revert`); the probe docstring sentence (D12.vii).

The Fable question for this pass (`FABLE_HOLD_QUESTION.md`) stands HELD; D1 is the answer this loop would most want checked.
