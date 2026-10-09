# `arm_msrmode_probe.py` -- **PRODUCE THE FINAL ROW TABLE.**  Eight amendments are in; reconcile them.

## VERDICT LINE FIRST.  TREE: `GXEMUL-SEC/`.  **DO NOT RATIFY** -- three of the eight amendments
## correct YOUR OWN earlier spec, and §S4 asks whether the reconciliation is even coherent.

## S1 -- WHERE THIS STANDS

Your spec (`regress/artifacts/armmsrmodekill/WITNESSSPEC_grok_20260917.txt`) is 16 rows,
`14/16 -> 16/16`.  It has since been amended EIGHT times, and the amendments live beside it at
`regress/artifacts/armmsrmodekill/SPEC_AMENDMENTS_READ_BEFORE_BUILDING.md`.  **Read both.**

Three amendments correct the spec's own reasoning, two of them yours:

| # | what changed | source |
|---|---|---|
| 1 | kill-row oracle: **EOF ALONE => RED**, the text is DIAGNOSIS not half the trigger | glm, packet-fed |
| 2 | the spec self-contradicts: "one process per data row" vs "12 sessions" for 15 rows | glm |
| 3 | the two RED rows may be DUPLICATES unless the second carries a SECOND mode write | glm |
| 4 | accept rows check ARRIVAL, not PRESERVATION; and the SVC32 row's want contradicts its stimulus | glm |
| 5 | the stimulus CLEARS I and F, so post-fix the guest runs reserved-mode with interrupts ON | glm |
| 6 | **the fake-green mechanism named in the spec is the WRONG ONE** | you, cross-spec review |
| 7 | **do NOT copy `arm_flags_probe.py`'s `session()`** -- it dumps once AT THE END and this guest dies | you |
| 8 | (a note carried for the Alpha spec: it lacks `CONTROL=DEAD` / `RESULT=0/0`) | you |

## S2 -- WHAT I NEED: ONE TABLE I CAN BUILD FROM

**Produce the FINAL row list**, every amendment folded in, as a table with:

    row name (<= 13 chars)  |  session #  |  stimulus  |  oracle  |  PRE (HEAD)  |  POST  |  role

plus, beneath it:
* **the ROW -> SESSION schedule**, explicitly, because amendment 2 says the spec's own arithmetic
  does not close.  If it is not 12, say the real number.
* **the final TALLY both sides.**  The spec says `14/16 -> 16/16`.  **Amendment 3 may change the
  row count and amendment 4 may change the accept rows.**  If the tally moves, say so -- a number
  carried from a superseded spec is exactly the frozen-number defect this project keeps correcting.
* **which rows are CONTROLS whose failure means SETUP-FAILED** (`ARMMSRMODE_CONTROL=DEAD`,
  `ARMMSRMODE_RESULT=0/0`, stop) rather than "no defect".

## S3 -- THE RECONCILIATION I CANNOT DO MYSELF

**Amendments 1 and 6 interact and I want that checked, not assumed.**

Amendment 1 makes an armed kill row RED on **EOF alone**.  Amendment 6 says the real fake-green is
**encoding-nop / c-bit-off / MSR-never-stepped**, which produces **no EOF at all** -- the process
survives, looking exactly like a correct post-fix decline.

> **So under amendment 1, does the `enc ok` / `no cbit` / dump-before-MSR machinery become the ONLY
> thing standing between this witness and a false green?**  If yes, those rows are no longer
> conveniences -- they are load-bearing, and they need the same scrutiny the kill rows got.
> **Are they strong enough?  What is the smallest edit that defeats them?**

**Amendments 3 and 5 also interact.**  Amendment 3 wants the second red row to carry a SECOND mode
write (`#0x14` then `#0x13`) so it is not a duplicate.  Amendment 5 says after the first write the
guest sits in a reserved mode **with IRQ and FIQ unmasked**, so an asynchronous exception can enter
the Save arm by itself.  **Does that make the second row's timing nondeterministic, and if so what
pins it?**

## S4 -- *** IS THE RECONCILIATION COHERENT AT ALL? ***

Eight amendments on a 16-row spec is a lot.  **Say plainly if the spec should be REWRITTEN rather
than patched.**  A patched spec whose amendments interact in ways nobody has traced is worse than a
clean one, and this project's stopping rule exists because a `#392` chain ran six passes without
converging.

**If the answer is "rewrite it, here is the rewrite", give me that instead of a table of patches.**
