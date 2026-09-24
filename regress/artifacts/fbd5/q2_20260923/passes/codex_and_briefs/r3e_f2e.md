## §F2 — 3d's pass findings, with MY disposition of each (the panel sharing its findings)

**Adjudicate your own findings harder than anyone else's**, and say whether the FIX is right, not only the finding.

* **T1** [codex] the toggle cancels across the re-arm row's two batches: "kept" was read only at the end.  **ACCEPTED as
  class (A)**: every field and irq_asserted after each access of X14's multi-access rows (CXT1: 0 -> 3 rows).
* **T2** [kimi-k3:cloud] the read write-back's width is unobserved, and a real narrow load's buffer is exactly len bytes.
  **ACCEPTED as class (B)**, with the fetch half 3d took: `pad_kept` in X6/X9/X10 (WB4: 0 -> 96; WB8: 0 -> 144).
* **T3** [grok: byte order, pc; the Opus seat: CX01-CX10 -- running, byte_order, is_32bit, ninstrs, machine->ncpus, pc,
  cpsr] the caller disclosure named two fields.  **DISCLOSED AS A CLASS** -- *any caller state*; the Opus seat measured
  that a row only fixes the fields it sets (CX09/CX10 stay green even against its real-caller row), so the class can
  only be closed by disclosure.  BO1/PC1 green on both, measured.
* **T4** [codex dedicated] a destination keyed on `fiq_enable & 1` passes at len 4.  **DISCLOSED AS A CLASS**; CXD1 green.
* **T5** [the Opus seat] stores to state no row reads after the access -- timer state at any legal access (SR01-SR09,
  SR11; SR02 zeroes timer 1's pending ticks on every IRQ_STATUS read -- #474's lost-interrupt class), a latch or the FIQ
  fields at X14's single-access rows (AS01-AS04, AS08).  None is in the DEPENDS-ON floor and none changes a channel a
  row or COVERED claims.  **DISCLOSED**; the Opus seat's scratch rows W1-W8 (872 rows) red 28 of its 29 greens and are
  the ready detector.
* **T6** [the Opus seat, FMT01] the announce text is a FORMAT string: a conversion added to an announce with no argument
  is undefined behaviour in the real `fatal()`.  **DISCLOSED** under the TEXT line.
* **T7** [codex, codex dedicated, the Opus seat] records: the 0xa5 fill's reason; E3's reason (the asserting sibling);
  "five checks" (six rows at four sites); FS02's condition; W02, not W03; the header cited a `q2e_opus` path that did
  not exist and the caller line a scratch path.  **ACCEPTED** -- rewritten, and the three Opus result folders copied to
  `q2_20260923/q2{e,f,g}_opus/` (each SUMMARY ends in its completion sentinel).
* **T8** [glm] premise: do X6 and X9-X13 read the four fields?  **MEASURED: yes** -- GLM1 red 23 and GLM2 red 149, on both
  instruments.
* **T9** [kimi-k3:cloud] premises: `x14_new`'s fifth argument is `devinit` (an int), not irq_asserted, so the r3d table
  is exact; the re-arm reads compare `RA[i].want`.  **Settled from the source.**
* **T10** [codex dedicated] a raw-status zeroing keyed so the re-arm row cannot see it.  **MEASURED**: CXS2 red on E3's two
  rows only -- E3 is not redundant with the re-arm row.
* **T11** [the Opus seat] `gate_offline.sh`'s footbridge "Not covered" summary lists less than the harness's NOT COVERED.
  **FILED** (records; the gate's comment, with `fbgateidentity`).
* **T12** [deepseek] D4: E3/E5 are "inside the floor".  The brief's Q2 SEARCH scope is not the DEPENDS-ON floor.  The Opus
  seat: take both, cite the row-demand rule (zero rows, measured deltas), not the addition licence.  **Kept taken.**

**DISAGREEMENTS -- both sides, in their own words:**
* **DD1** codex: *"S4 is incomplete if its acceptance means that E4 now establishes preservation throughout the
  sequence."*  I had accepted S4.  **Settled by CXT1** (green on 3d) and closed as class (A).
* **DD2** grok: *"The chain stays open on the caller bullet, which is one axis short."*  The Opus seat: *"the caller-context
  class can only be closed by disclosing it as a class."*  **Closed by the class sentence.**
* **DD3 (mine, open): is (A)'s enumeration complete?**  I claim X14's multi-access rows with a kept claim are exactly the
  DEVINIT declines rows and the re-arm row.  The DEVINIT Set/Clear row (two accesses) claims the enable and the drive,
  not kept fields; the DEVINIT reads row claims values.  Check that claim against the rows.

## §E -- QUESTIONS (answer each, numbered; if you are answering from this packet alone, do Q1 and Q3 first)

**Q1 -- VERIFY THE ENUMERATION (the closing pass's job).**  (a) Class (A): list every X14 row that makes more than one
access, what it claims kept, and whether 3e checks that claim after every access -- is any kept claim still read only at
an endpoint?  (b) Class (B): list every row that passes the device a narrow buffer, and whether a fetch past len or a
write-back past len is now observed there -- which arms and widths are covered, which are carried by another row?
(c) Is every COVERED line true of the 864 rows, and every NOT COVERED line outside the floor or honestly disclosed?
**Q2 -- THE FLOOR QUESTION, on the composite**: the smallest edit to the five arms, the two head tests, the Clear write
in the +0x18c case, or the common tail, that the 864 rows cannot see and the contract does not disclose.  **If none,
give your denominator** -- a bare zero does not close the chain.
**Q3 -- adjudicate T1-T12 and DD1-DD3**: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each.  Then: **WHICH OF MY
ACCEPTED DISPOSITIONS IS WRONG?**
**Q4 -- records.**  Is any sentence in 3e's changed comments false as of today?  `ls` every artifact the changed
comments cite.
**Q5 -- closing.**  Is this pass VALID to close the chain (diff delivered, roster, your denominator)?  If you would not
close it, name the one measurement that would let you.

If, while verifying a claim, you found something ELSE -- say so.

End with a seat record: model, what you read, what you ran.
