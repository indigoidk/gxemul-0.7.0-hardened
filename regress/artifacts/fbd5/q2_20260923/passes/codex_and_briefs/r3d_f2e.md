## §F2 — 3c's pass findings, with MY disposition of each (the panel sharing its findings)

Every seat answered blind to the others.  Here is each finding, who raised it, and what I did.  **Adjudicate your own
findings harder than anyone else's**, and say whether the FIX is right, not only whether the finding was.

* **S1** [codex, grok, glm, codex-dedicated; the Opus seat's FS01 is its asserted twin] the Clear 0x20 row names the
  pending status and never reads it; a Clear zeroing it at DEVINIT values passed 864.  **ACCEPTED -> E1** (CXC1 green
  -> red x2).
* **S2** [grok; glm secondary; codex-dedicated for the re-arm row] the IRQ_STATUS read row claims "(value, fields,
  output)" and never read the FIQ fields.  **ACCEPTED -> E2 + E4** (GF1 green -> red x2).
* **S3** [the Opus seat, FS01] a Clear dropping the masked line from the RAW status while irq_asserted -- guest-visible
  in 4 steps -- passed; the asserted-Clear rows named only the enable and the CPU line.  **ACCEPTED -> E3**, zero rows
  (FS01 green -> red x1).  `irq_asserted` deliberately unpinned there (E3's reason).
* **S4** [agy; codex-dedicated] the re-arm row's final check omitted `irq_asserted` (and the FIQ fields).  **ACCEPTED ->
  E4** (a decline clearing irq_asserted, DA1: green -> red x1).
* **S5** [deepseek] a fetch of 4 bytes whatever `len` is passed: every narrow write left the bytes above its width 0.
  **ACCEPTED -> E5** (FW1 green -> red x16).  The fetch is NOT an edited line, so this is above the floor; I took it
  because the fill costs no row and the delta is measured (the addition licence).  **A seat may say that is wrong.**
* **S6** [the Opus seat, MC01-MC05, MC07] every row calls the handler with mem NULL on a machine of type MACHINE_NONE,
  so a condition on `mem` or on the machine type passes.  **DISCLOSED, clause (e)**: no body of the five reads `mem` or
  the machine type (the joint-cells rule: a selector that touches nothing the guarded body reads is (e)).  Filed with
  the Opus seat's scratch rows (a cats and a netwinder caller with a real mem: 871 rows, 8 of its 9 greens red) as the
  ready detector.  Measured green on 3d, 6 of 6.
* **S7** [the Opus seat TX01; kimi-k3:cloud] the announce TEXT is unread.  **DISCLOSED.**
* **S8** [codex-dedicated] a latch that re-arms after four repeats passes (no instance declines one site five times).
  **DISCLOSED, clause (e)**: the latch test partitions {0, nonzero}, and both are rowed.  LH1 green on both, measured.
* **S9** [the Opus seat FS02] a Clear clearing irq_asserted passes.  **DISCLOSED** on the LEVEL line.
* **S10** [grok, the Opus seat] records: "X14 calls ... only to BUILD its instances" was false (PR09 reds the
  status-read row); "That pair is fbirqstuck's round" conflated F13's stuck-high line with the pair's bit logic
  (PR01/PR03/PR04); "passes all 862 rows" and F1's "red on the 862 rows" were stale.  **ACCEPTED -> rewritten.**
* **S11** [codex, the Opus seat] COVERED's reads line claimed IRQEnable x width 8 while NOT COVERED named it.
  **ACCEPTED** -> widths spelled out.
* **S12** [the Opus seat, codex] the exact-value example undercounted (the irq_* `!= 0x10` forms are red at +0x184
  since 3c and at all five latch tests; every fiq_* form is green) and `idata != 0x20` is red since 3c, not since X14;
  [minimax] "by value, not by design" was ambiguous.  **ACCEPTED** -> rewritten from the measured forms.
* **S13** [codex] bit 16 of the 25 unraised bits IS caught (N_SB16 reds ten rows: one each in X9/X10, four each in
  X12/X13); 24 masks pass.  **ACCEPTED.**
* **S14** [grok] NOT COVERED's field list omitted the rest of the instance THE SPACE names.  **ACCEPTED.**
* **S15** [glm] the X14 header's recap of the nine did not name TD04 (a decline driving at DEVINIT values, NOT
  asserted).  **ACCEPTED.**
* **S16** [kimi-k3:cloud] COVERED's "the read data over the width" read as a channel of the write rows.  **ACCEPTED** ->
  "for a read".
* **S17** [codex-dedicated] three PRE-EXISTING false comments (fbclearread's `case TIMER_1_CLEAR` sentence, "EVERY
  REAL ROW IN THIS FILE COMPARES NUMBERS", the DISABLED-timer sentence also in gate_offline.sh).  **FILED with R17**
  (pre-existing, the timer campaign's), not edited here.
* **S18** [R4 options: codex, grok, agy, minimax, kimi-k3:cloud, the Opus seat] a one-row len-1 Clear on X14's split
  counters, or re-wiring X9-X13's `d->irq` to X14's CPU counter pair (zero rows), would close the destination gap.
  **KEPT DISCLOSED** (the Clear write's body is not an edited line); both options go into the filing.
* **S19** [R2 options: kimi-k3:cloud, minimax, codex, grok, agy, the Opus seat] a bounded producer block.  **OWNER
  RULING 2026-09-23: disclose + file under `fbirqstuck`** (MED); the options and the Opus seat's ready rows go there,
  with the pair's bit logic named apart from F13 (grok).
* **S20** [glm] does the fork's `fatal()` exit?  It does not: `debugmsg.c`'s `fatal()` returns (it has no exit at all;
  the carrier records this).  No change.
* **S21** [kimi-k3:cloud] the family pins sum to 831, not 864: the other 33 are the 32 timer rows and IDENTITY
  (codex and grok enumerated 864).  No change.
* **S22** [agy, Q2] `(len & 1) == 0` on the Clear direction test: len 1 is odd, so X12's len-1 rows red it; the
  `len == 3` variant is not a guest input.  Not an escape.

**DISAGREEMENTS -- both sides, in their own words:**
* **D1** kimi-k3:cloud: *"'keeps 0x10 pending' is observed via the drive, exactly."*  codex, grok, glm: *"The drive
  proves bit 4 was live at drive time, not that the field retains it afterwards."*  **Settled by measurement**: CXC1
  zeroes the status AFTER the drive and passed all 864 rows on 3c.
* **D2** agy: *"No X14 row claims a channel it does not read."*  codex, grok, glm: the Clear 0x20 row and the status-read
  row do.  **Settled by CXC1 and GF1.**
* **D3** kimi-k3:cloud: *"disclosure + file is right iff fbirqstuck is a real, owned round."*  The other seats upheld
  R2 on the DEPENDS-ON function-boundary rule.  `fbirqstuck` is an open MED item and the owner ruled.
* **D4 (mine, open): E3 and E5 are rows/fills ABOVE the floor** -- the Clear write's body and the head fetch are not
  edited lines.  I took both because each costs no row and each has a measured delta.  The alternative is to disclose
  them, as S6/S8 are disclosed.  Which is right, and does taking them change what the CONTRACT claims (COVERED now
  names the raw status at the asserted Clears)?

## §E -- QUESTIONS (answer each, numbered; if you are answering from this packet alone, do Q1 and Q3 first)

**Q1 -- did 3d close what it claims?**  (a) For each strengthened check (E1-E4) and the fill (E5), name the edit it is
for and the observable that now differs -- and say whether ANY row still claims a channel it does not read.  (b) Is
every COVERED line true of the 864 rows, and every NOT COVERED line outside the floor or honestly disclosed?
**Q2 -- THE FLOOR QUESTION, on the composite**: the smallest edit to the five arms, the two head tests, or the Clear
write inside the edited case, that the 864 rows cannot see and the contract does not disclose.  Name it and the rows you
expect to stay green; **if none, give your denominator** -- a bare zero does not close the chain.
**Q3 -- adjudicate S1-S22 and D1-D4**: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each.  Then: **WHICH OF MY
ACCEPTED DISPOSITIONS IS WRONG?**  Above all D4 and S6 (caller context disclosed rather than rowed).
**Q4 -- records.**  Is any sentence in the changed comments false as of today?  Check the two renamed row names against
their checks, and the IDENTITY comment's history.
**Q5 -- closing.**  Is this pass VALID to close the chain if it finds zero breaches (diff delivered, roster, your
denominator)?  If you would not close, name the one measurement that would let you.

If, while verifying a claim, you found something ELSE -- say so.

End with a seat record: model, what you read, what you ran.
