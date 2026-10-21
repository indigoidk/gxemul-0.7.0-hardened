# `vmedefaultkill` (#568) -- THE ADJUDICATION PASS (§F2): every pass-2 finding, my disposition on each, and the disputes -- adjudicate them, and tell me which of my dispositions is wrong

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

This packet consolidates the FIVE pass-2 answers (GPT-6 Astra, Grok 4.7, GLM 5.3, Fable 5.1, and Argon -- Gemini web,
packet-fed) on one change.  **You are now reading the other seats' findings.  Correct them where they are wrong, and be
HARDEST on findings that are your own and on dispositions that adopt your position** -- a ruling in your favour is the
one you are least likely to test.  **I accepted most findings; that is a suspicious ratio, and agreement is not
evidence.**  Where a claim is checkable, check it rather than weigh it.

**THE TREE UNDER REVIEW IS `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/` -- its working tree on committed HEAD `1a59a47e`.**
The round's edits are uncommitted there.  Another session's uncommitted edits to `dev_pcc2.c`, `dev_lca.c`, `dev_sh4.c`,
`cpu_alpha_palcode.c` and `mvme_pcctworeg.h` are NOT part of this round.  Three pristine-2021-upstream copies of GXemul
sit under the project root; if your line numbers disagree with mine by hundreds you are reading one of them.

**If you cannot read files that is expected** -- the change (section 5) and every finding are inlined.  Name any premise
you cannot settle from this packet rather than guessing.  **VERDICT LINE FIRST.**

## 1. The round, and what changed since pass 2

`src/devices/dev_vme.c` ended the emulator (`exit(1)`, announced only by a `debug()` that is silent at default verbosity
while free-running) on any VME2 offset its switch did not name.  Owner rulings: the 26 header-named registers the model
does not implement (population 2) DECLINE + ANNOUNCE ONCE; every other unmatched offset (population 1) FAULTS via
`return 0` (memory_rw raises the m88k data-access exception).  The fix is section 5; the 34-row rung-3 detector is
`regress/vme_default_probe.py` (frozen copy md5 `19de15b3`); kill tables 1 and 1b ran 27 legs in a scratch clone
(every leg killed except the two predicted equivalents M_ODATA0 and M_SERVED0; NULL medium 5/34; HEAD 14/34).

**Measured since the pass-2 packet was written (it said the gate block had no run):** the gate-14 block run ALONE reds
on the pre-fix binary (22 of 39 checks) and is green on the fixed one (39/39); the FULL gate 14 on the fixed `build/gxemul`
PASSED, 1264 checks, 0 failed (`regress/artifacts/vmedefaultkill/gate_20261020/`: `mini_PREFIX.out`, `mini_FIX.out`,
`GATE14_FULL.out`).  The two-part clearance holds on `build/`, `build-asan/`, `/tmp/gxsec-build` (source cmp CLEAN,
binary newer) and `est/` (source CLEAN; no binary).  The probe-development files the docstring cites were copied to
`regress/artifacts/vmedefaultkill/probe_20261020/`.  Nothing else has changed: the fix and the probe are as pass 2 read them.

## 2. The findings, numbered, with my disposition on each

Seat key: **AX** GPT-6 Astra (file-reading), **GK** Grok 4.7 (file-reading), **GL** GLM 5.3 (packet-fed), **FB** Fable 5.1
(file-reading), **AR** Argon (packet-fed).  Each seat's own finding number is in brackets.

**F1 -- FLOOR BREACH (predicted, not yet built): the announce's DIRECTION predicate can be swapped to a body-read value
and every row stays green.**  AX [F8]: *"Replace only the population-2 announcement's direction condition: `- if
(writeflag == MEM_WRITE)` / `+ if (idata)`.  This should preserve all 34 greens ... Every tested population-2 store is
nonzero: a5a5a5a5, d4, c3d4, or 1122334455667788; reads leave idata zero.  A guest's first zero store to a fresh
population-2 register would instead produce a read/served announcement."*  **Checked by reading** the probe: every store
to a population-2 offset uses r2 = 0xa5a5a5a5, r12 (the 0xd4 / 0xc3d4 narrow value) or r10 (0x1122334455667788) --
section 5c; no row stores zero there.
**Disposition: ACCEPTED as a clause-(d) floor breach** -- the predicate `writeflag == MEM_WRITE` is one the fix ADDED,
and `idata` is a field the guarded body reads (it is printed), which is exactly the operand-swap form the DEPENDS-ON
enumeration names.  **Change:** measure leg M_IDATA on the frozen rev-2 instrument FIRST (predicted 34/34 -- if it reds,
the finding is refuted and recorded so); then probe REV 3 adds a first-access ZERO STORE to an untouched population-2
register, wanting the WRITE-form line `... (len 4): 0x0 -- declined.  (once) ]`; M_IDATA must red rev 3.

**F2 -- WRONG RECORD (product comment): the typedef claims more than it checks.**  GL [F5], FB [F1], AX [F1, as DEFECT],
GK (Q1b: "The 1ULL conjunct ... was not its own leg").  FB: *"Only the field is checked; `sizeof(1ULL)` in the typedef
is a different literal from the arm's.  A `1u` in the arm compiles with no diagnostic ... at runtime `1u << 35` is UB
and on x86-64's 5-bit shift mask lands on bit 3 = SLAVELMOD2's."*  AX wants a shared definition used by both shifts
and the check; FB and GL want the comment reworded (FB: "take the reword now and file the macro").
**Disposition: ACCEPTED; fix REFINED (see D5):** reword the comment to claim the FIELD only, DELETE the tautological
`&& (VME2_MISC >> 2) < 8 * sizeof(1ULL)` conjunct (a check that cannot fail, with no runtime footprint -- the binary is
unchanged), and MEASURE leg M_ONENARROW (both arm literals `1ULL` -> `1u`) on rev 3, so the comment may say what catches a
narrowed literal at run time instead of claiming a compile-time guard it does not have.

**F3 -- WRONG RECORD (product comment): "The in-tree OpenBSD 2.2 guest reaches six of them".**  GL [F4], FB [F7], AX [F5].
FB, verified in the guest source: six registers have guest SITES (MASTERCTL, MASTER3, MASTER4, MASTER4MOD, IRQSTAT,
IRQCLR), but IRQCLR is written only inside `if` on a non-zero IRQSTAT, so under this model the guest REACHES five; and
"in-tree" reads as GXemul's tree.  **Disposition: ACCEPTED.**  New wording: the OpenBSD 2.2 mvme88k driver
(`sys/arch/mvme88k/dev/vme.c`) has access sites at six of them and, with IRQSTAT served 0, reaches five.

**F4 -- NIT (product and gate comment): `default:`'s "memory_rw then raises the m88k data-access exception" is
unqualified.**  FB [F8], AX [F5].  An instruction fetch gets INSTRUCTION_ACCESS; NO_EXCEPTIONS callers never reach the
arm.  **Disposition: ACCEPTED:** "for a guest data load or store", in the device and in the gate block's comment.

**F5 -- the read announce prints `0x%x` of `(unsigned) odata` where pass 1's D2 named `0x%llx` / `(unsigned long long)`.**
GL [F6] ALIGN, AX [F4] ALIGN (NIT); FB [F10] KEEP and amend D2's record; GK [F4] KEEP and amend.  Two-two -- **see D1.**

**F6 -- DEFECT (landing) + WRONG RECORD (pass-2 packet section 3): the probe-wiring MANIFEST registration does not exist,
and SCORE_CLAIMS_MANIFEST is still 36.**  FB [F2], AX [F7], GK [F2].  The working tree's `check_probe_wiring.py` diff
(+15) is entirely OTHER units' lines (b115, wdcnullxfer, wdcrearmzero, fbclearread and a #563 comment); my packet's
section 3 described it as this round's.  **Disposition: ACCEPTED.**  The commit builds that file from HEAD's blob plus
this round's lines only: `regress/vme_default_probe.py` CLASS_DETECTOR (gate 14, pinned by EQUALITY at rev 3's row
count), the frozen probe copies CLASS_WITNESS, the leg generators / comparators CLASS_TOOL, the witness scripts
CLASS_WITNESS; `SCORE_CLAIMS_MANIFEST` 36 -> 37.  The packet-section-3 misdescription is recorded as a brief defect.

**F7 -- WRONG RECORD (probe docstring): "NO KILL TABLE EXISTS FOR THIS REVISION" and its neighbours.**  GL [F12], FB [F3],
AX [F10], GK [F3].  Additions: cite BOTH tables by full hash; keep the original predictions AS DATED PREDICTIONS (AX);
"a design claim until a kill table measures it" is now measured; the docstring's claim that EVERY device session opens
with `ld r30,r3,0x88` is false -- the control session reads VBR into r5 after an `or`, the cased census into r13 (AX);
the docstring cites scratchpad files with no durable copy (FB) -- now copied to `probe_20261020/`; mark which per-mutant
counts in the ROW PLAN were measured and which were never built (FB: "a latch set at one constant bit (51)", "a
per-direction latch (52)").  **Disposition: ACCEPTED, all of it, in rev 3's docstring.**

**F8 -- DEFECT (instrument reporting): product-reddable rows sit in CONTROL_ROWS.**  GL [F11], FB [F4], AX [F6], GK [F5].
`cased census`, `t1cmp rt` and `free ctl` red under product edits (M_DROPTCTL, M_DROPIRQEN, M_T1CMPWRDROP), so those kills
print CONTROL=FAIL -- a product failure under the apparatus reason.  AX: *"CONTROL failure cannot establish an apparatus
cause ... Move functional expectations into detector classification with separate apparatus controls."*  GK and FB: do
it at the next instrument revision, not by unfreezing the measured one.  **Disposition: ACCEPTED, in REV 3** (rev 3
exists anyway because of F1, so "next revision" and "now" coincide): CONTROL_ROWS = `session`, `live`, `neg apparatus`,
`unasm`, `vbr reset` (the device-presence signature), `free neg ctl` (the free-running proof); `cased census`, `t1cmp
rt`, `free ctl` and `free quiet` become scored detector rows.  See D2.

**F9 -- WRONG RECORD (instrument text): "(FAILED FOR SOME OTHER REASON)" on red rows whose stop IS the leg's edit.**  AX
[F11]: change before shipping, neutral wording (`dependent check not exercised: pass 1 did not complete`; `unexpected
stop pc=0x18 before announce verification`), keep them red.  GL [Q5b]: accurate, keep.  GK [Q5b]: leave it; the miss
note is the place.  FB [F9]: the second-pass text is honestly dependent; the non-word session's stop text misattributes
an own-channel kill -- change it at the next revision.  **Disposition: ACCEPTED in REV 3** with AX's neutral wording;
every such row stays red.  See D3.

**F10 -- COVERAGE DEBT from the one ask-again (clause e unless you show otherwise), with predicted 34/34 escapes:**
* (a) FB [F5]: the latch SET conditioned on width -- `if (len == 4)` in front of `d->warned_unimpl |= ...` -- leaves every
  non-word access announcing on EVERY access, an unbounded guest-drivable `fatal()` (the flood class).  The two-pass
  sessions use `ld`/`st` only; the non-word session touches each register once.
* (b) FB [F6], GK [Q3/F6], AX [F9 tail]: `default:`'s `debug(` -> `fatal(` (or deleting the two `debug()` lines) -- host
  output at population-1 faults is pinned by nothing; D5's text rests on review.
* (c) GL [F8]: `if (len == 2 && (relative_addr & 3) == 0) break;` in `default:` -- a halfword/byte at a WORD-ALIGNED
  population-1 offset declines instead of faulting; `p1 widths` probes only lanes 1-3 and len-8.
* (d) GK [Q3], FB: `case 0x91:` (any unsampled population-1 interior) added to the decline list -- already NOT CLAIMED.
* (e) GK [F6]: deleting the whole typedef -- all 34 green (a compile-time guard has no runtime row; M_CAPNARROW is a leg).
**Disposition: REFINED -- take (a), (b), (c) under L1 (pre-ship construction) in REV 3, because each is one or two
accesses in an EXISTING session: a second pass over the six non-word accesses wanting 0 lines; a count of `[ vme:` text
in the free-running population-1 census wanting 0; two lane-0 accesses (`ld.hu` and `st.b` at word-aligned population-1
offsets) added to `p1 widths`, 6 -> 8 faults.  FILE (d) and (e) as disclosed coverage debt.**  Both FB and GL
recommended FILING (a)-(c) -- **see D4**.

**F11 -- WRONG RECORD (pass-2 brief premises): the enumerations were incomplete.**  GL [F2], FB [Q1d], AX [F2], GK [F1]:
the `return 0` set also holds the 2964 sub-word starts inside population-1 words (AX: 7554 (offset, length) pairs per
direction reach `default:`).  AX [F3]: the brief's S4 says population 4 (a cased base at len != 4) reaches the fault --
**it does not**: byte and halfword accesses at all ten cased bases match their exact label and are SERVICED (and `ld.d`
succeeds at 0x00/0x50/0x60/0x80/0x88).  **Disposition: ACCEPTED** -- brief errata; the CHANGELOG block and the probe
contract state the correct sets; population 4 is described as serviced by the cased arm (with the `vmewidthlanes` lane
defect), never as faulting.

**F12 -- WRONG RECORD (contract): NOT CLAIMED lines are missing.**  GL [F10] (word-aligned narrow/double accesses at the
~22 population-2 registers no non-word row touches), AX [F9] (population-2 non-word offsets, cross-width latch reuse
and store-data patterns are SAMPLED; the fault rows do not assert the two `debug()` lines), FB [Q4e] (F10a's class; host
output at population-1 faults; D7's negative control lives only in the table), GK [Q4e] (the fault rows pin `return 0`,
DMA0 and DMT0, not the `debug()` text).  **Disposition: ACCEPTED** -- each becomes a NOT CLAIMED line in rev 3's contract
(those F10 (a)-(c) now rows are struck from it).

**F13 -- WRONG RECORD (kill-table observation (b)): the per-row kill census counts DEPENDENT reds as independent kills.**
FB [F9]: `p2 ann rd 2` / `p2 ann wr 2` each hold 3 own-channel + 4 dependent reds; `p2 nw rd` under M_WRFAULT and
`p2 nw wr` under M_LENFAULT are dependent.  **Disposition: ACCEPTED** -- a dated records note beside the table; the
table itself is not edited.

**F14 -- NIT (gate comment): "mvme88k/mvme187 constructs from the PROM, like the mk48/pcc2 blocks above".**  FB [F15]:
this probe constructs with `-M 64` and a 4-byte dummy at 0x10000, no PROM image.  **Disposition: ACCEPTED.**

**F15 -- RECORD FORM (clause c).**  GL [F9], FB [F13], AX [Q4c]: `(c): measured at
regress/artifacts/vmedefaultkill/killtable1_20261020/legs/NULL.raw` (the vme `device_add` removed from
`machine_mvme88k.c`; 5/34, CONTROL=FAIL).  **Disposition: ACCEPTED** -- the CHANGELOG block carries that line (and rev 3's
table re-measures it).

**F16 -- EVIDENCE GAP (gate run) -- RESOLVED.**  GL [F7]: "the gate-14 block has no measured run in the packet."  Now
measured both ways and inside the full gate (section 1).  **Disposition: ACCEPTED and discharged.**

**F17 -- PROVENANCE (legs).**  AX [Q1e]: freshness of the leg builds is *"corroborated historical evidence, not
independently remeasured"*; the build logs are not in the preserved directory.  **Disposition: ACCEPTED** -- copy the
per-leg build logs (`killtable1/build/*.build.log`, `table1b/build/`) beside the tables.

**F18 -- RECORD: FB withdrew its pass-1 D1 dissent.**  FB: *"My pass-1 D1 dissent (a bound test in `default:`) is
WITHDRAWN: M_ADD94 and M_ADD90 measured that the label form's growth edit is caught by the census."*  **Recorded.**

**Argon (AR)** -- PASS 2 NOT YET ANSWERED: its control passed at 23:42, the packet went at 23:43, and attempt 1 failed at
00:08 ("The connection to Gemini was lost while generating the response, and recovery timed out"); the sender is
retrying.  Recorded as a SEAT FAILURE for now, never as agreement.  If it lands, its findings go to every seat in a short
supplement.



## 3. The disagreements -- each side in its own words; adjudicate your own

**D1 -- the read announce's format (F5).**
* ALIGN to `0x%llx` / `(unsigned long long) odata` -- GL [F6]: *"the adjudication is the ruling artifact -- a silent
  code/record divergence is exactly the drift this process polices ... the contract itself contemplates a later
  vmewidthlanes fix composing a 64-bit odata ... under `%x` that future compose prints a truncated lie."*  AX [F4]:
  *"restoring the agreed form removes unexplained drift and accommodates a future composed 64-bit read."*
* KEEP `0x%x` and amend D2's record -- FB [F10] (D2 was FB's own pass-1 ask): *"the printed value is UNOBSERVABLE today
  -- M_SERVED0 (a literal 0 in its place) survives 34/34 ... a format-only edit now changes the fix md5 the table measured
  and invalidates the find-strings of two legs ... What may not ship is the current state -- a record that says `0x%llx`
  beside code that says `0x%x` with no reason anywhere."*  GK [F4]: *"changing this string now does not change a
  guest-visible bit ... A later vmewidthlanes edit that builds a real 64-bit odata owes its own format row."*
* **My ruling: ALIGN.**  FB's cost argument was the deciding one, and F1 removes it: rev 3 re-runs the whole table on a
  regenerated leg set anyway, so the format change costs no extra measurement.  What remains is GK's "no guest-visible
  bit", which is true and is equally an argument for either form -- so the adjudicated record decides.  **FB and GK:
  does that hold, or is there a reason to keep `%x` that is not about the re-run?**

**D2 -- when to reclassify the CONTROL rows (F8).**  AX: before shipping.  GK: *"Leave the tuple alone in this ship:
moving it changes VME_DEFAULT_CONTROL and unfreezes the measured instrument."*  FB: at the next revision.  GL: at the
next instrument revision.  **My ruling: in rev 3** -- rev 3 IS the next revision, and it re-measures everything.

**D3 -- the "(FAILED FOR SOME OTHER REASON)" text (F9).**  AX: change before shipping (*"its asserted causal exclusion is
not [accurate]. The oracle cannot know the reason is unrelated to the mutation."*).  GL, GK: keep (accurate from the
row's vantage; the miss note is the place).  FB: keep the dependent rows' text, change the non-word session's stop text
at the next revision.  **My ruling: rev 3 adopts AX's neutral wording on all of them, rows stay red** -- same reason as
D2.  GL and GK: is there a reason the neutral wording is WORSE, beyond the re-run cost that rev 3 pays anyway?

**D4 -- the ask-again's coverage debt (F10): FILE or take in-round.**  FB filed (a) and (b) as clause (e) (*"`len` is
PRINTED, not TESTED, by the body and is not device state, so this is outside the (d) floor -- FILE as coverage debt, or
take it under L1"*); GL put (c) in the `vmewidthlanes` round (*"closing it costs one probe line"*).  **My ruling: take
(a), (b), (c) under L1 in rev 3, FILE (d), (e)** -- because each is one or two accesses inside an existing session and
rev 3 re-tables anyway.  **The risk I see in my own ruling:** every added row is new floor-bound material for the repair
pass to review, and this project's `#499` chain grew one cell per pass.  If you think taking them now lengthens the chain
more than it closes, say FILE and say why.

**D5 -- the typedef (F2): a shared macro for the shift operand, or reword the comment.**  AX [F1]: *"Use a shared
mask-operand definition in both shifts and the capacity check, then verify its narrowing fails compilation."*  FB [F1]:
*"take the reword now and file the macro"* (because the macro invalidates the latch legs' find-strings -- moot under rev
3).  GL [F5]: reword to claim the field only.  **My ruling: reword + delete the tautological conjunct + measure
M_ONENARROW**, NOT the macro: the addition licence asks for a measured delta, and the macro's only delta is moving
detection of a narrowed literal from run time (where rev 3's announce rows should catch it -- M_ONENARROW will say) to
compile time.  If M_ONENARROW ESCAPES rev 3, the macro gains its measured delta and I adopt it.  AX: is that the right
test of your proposal?


## 3b. The first adjudication already in

**ALREADY IN: Fable 5.1's adjudication of this packet (verdict PROCEED WITH CHANGES; full text
`vme/f2/out/fable5_f2.md`).  Check its two overturns -- they are claims, not rulings, until you agree.**

* **F3's FIX OVERTURNED -- "reaches five" is still an overcount; the guest reaches FOUR.**  Fable: *"`vme2chip_init()`
  runs at attach (vme.c:351, BUS_PCCTWO) and touches MASTERCTL (:452 read, :494 write-back), MASTER3 (:467), MASTER4
  (:480), MASTER4MOD (:482) -- four registers; the `master1/master2` reads are `#if 0`. A struct-field grep of all of
  `sys/arch/mvme88k` for the 26 population-2 fields finds NO other site. IRQSTAT (:576) and IRQCLR (:581) live only in
  `vme2abort()`, installed as the ABORT-switch NMI handler by `intr_establish(110, &sc->sc_abih)` at :539 -- and
  dev_vme.c contains no interrupt assertion at all, so vector 110 is never delivered by this model."*  My pass-2
  correction said five; the witness's "7 of 7" is a SITE census, not a reach claim.  **Adopted provisionally:** the
  comment will say the driver has access sites at six, its attach reaches four, and IRQSTAT/IRQCLR sit in the
  ABORT-switch interrupt handler this model never triggers.  *Is the NMI-handler reading right?*
* **F10(c) REFINED -- two rows need two legs.**  Fable: GL's mutant is `len == 2` only; the `st.b` lane-0 access kills
  the `len == 1` twin, so table 2 owes M_LANE0H AND M_LANE0B or the st.b addition ships unmeasured.  **Adopted.**
* **D5 REFINED -- the "adopt the macro if M_ONENARROW escapes" test cannot fire.**  Fable: the kill is UB-mediated --
  on x86-64 `1u << 35` masks to bit 3 (SLAVELMOD2's), silencing MISC in `p2 ann rd`; where a 32-bit shift by >= 32 gives
  0, MISC never latches and `p2 ann rd 2` reds instead.  *"A kill either way, by DIFFERENT rows ... write 'macro FILED'
  outright and record the platform beside the leg."*  **Adopted: the macro is FILED; M_ONENARROW is measured and its
  red row recorded with the host it ran on.**
* **D1 / F5 -- Fable CONCEDES ALIGN** (its KEEP rested on the re-run cost, which rev 3 removes); table 1's provenance is
  never rewritten -- tables 1/1b measured the `%x` form (fix568, md5 4e3e7fc2), table 2 measures fix568b.
* **D2, D3, D4 -- Fable UPHOLDS** the rev-3 rulings and taking F10 (a)-(c) under L1, and supplies the CHANNEL lines:
  `p2 zero wr` (a first-access `st r0` -- r0 is hardwired zero -- in its OWN short session, want one write-form line;
  one width is enough because the swap tests idata's zero-ness and the body tests nothing on len), `p2 nw rd 2` /
  `p2 nw wr 2` (a second pass over the six non-word accesses, want 0 lines), `p1 quiet` (count `[ vme:` in the existing
  free-running census continue text, want 0 -- it varies ONLY because that session free-runs at verbosity 0),
  `p1 widths` + `ld.hu` and `st.b` at word-aligned population-1 offsets (8 faults).
* **Owed, from Fable's "what we all missed":** re-derive the probe's `unasm` literal BY HAND before rev 3's first run
  (its own rule); move the gate's row list and its three count pins to rev 3's count (38 rows); one `grep -c` for the
  CPU's own fault text on a free-running fault transcript, to settle D5's "INFO-level line" record; M_ONENARROW's red
  row named with its platform.  F17 is DONE: the kill tables' build logs are now under `killtable1_20261020/build/` and
  `table1b/build/`.


## 4. What is still OWED, and where I may be fooling myself

**THE REPAIR (not yet built -- everything below is planned, nothing is measured):**
* **fix568b** -- comment-only changes for F3, F4, the typedef rewording + conjunct deletion (F2), and -- if D1 holds --
  the `%llx` format change, which is the one behavioural-text change.  Object code is otherwise identical; the record will
  say so only after comparing the two objects, not from reading.
* **REV 3 of the probe** -- F1's zero-store first-access row; F10 (a)-(c)'s rows if D4 holds; the CONTROL split (F8);
  the neutral stop wording (F9); the docstring (F7, F12).  Every changed or added row named with its mutant and channel
  in a PRETABLE written before the table runs, and that PRETABLE diffed against the row list (the `#490` rule).
* **TABLE 2** -- in a fresh scratch clone: BASE, HEAD, NULL, every table-1 and table-1b leg regenerated on fix568b, plus
  M_IDATA (F1), M_ONENARROW (F2/D5), M_LATCHLEN4 (F10a), M_DFATAL (F10b) and M_LANE0 (F10c).  **M_IDATA is measured on
  the FROZEN rev-2 instrument first** -- if it already reds, F1 is refuted and recorded.
* **Then** the block-only gate both ways on rev 3, the full gate 14 alone, and a pass on the REPAIR DIFF (the repair-
  chain rule: a repair made in response to a pass 2 owes its own pass, scoped to that diff, closing on the first pass
  with zero floor breaches).

**Where I may be fooling myself:**
* F1 is a prediction by one seat, checked only by reading.  If M_IDATA reds on rev 2 I have over-reacted.
* I am about to add rows after a clean table -- the shape that grew `#499` by one cell per pass.  D4 is where you can
  stop me.
* "Comment-only, object code identical" is a claim I will measure, not assert -- the `-g` line tables alone can make the
  objects differ.
* The late-review RECORDS unit (a different item) commits before this round; nothing in it touches dev_vme.c or the probe.
* No seat has yet looked at the probe's FREE-RUNNING sessions' timing budgets under load (30 s per `continue`): three legs
  took 74 s because a stopped pass 2 waited out its budget.  A loaded host could turn a green row red by timeout; the
  rows would then fail LOUDLY (red), not silently, but the gate's wall-clock exposure is real.


## 5. The change under review (inlined for the seats that cannot read files)

### 5a. The diff of `src/devices/dev_vme.c`, verbatim

```diff
diff --git a/src/devices/dev_vme.c b/src/devices/dev_vme.c
index b4a6050d..34023b8d 100644
--- a/src/devices/dev_vme.c
+++ b/src/devices/dev_vme.c
@@ -51,8 +51,21 @@
 
 struct vme_data {
 	uint32_t	reg[VME_LEN / sizeof(uint32_t)];
+
+	/*  #568: one bit per register WORD (relative_addr >> 2) for the
+	    unimplemented-register announce below; the highest such word is
+	    VME2_MISC (0x8c >> 2 == 35).  Zeroed by DEVINIT's memset, so every
+	    instance starts with every announce armed.  */
+	uint64_t	warned_unimpl;
 };
 
+/*  #568: narrowing warned_unimpl, or the 1ULL below, would shift past bit
+    VME2_MISC >> 2; make that a compile error (dev_pcc2.c's
+    pcc2_w_fits_in_warned shape).  */
+typedef char vme_warned_fits[((VME2_MISC >> 2) <
+    8 * sizeof(((struct vme_data *)0)->warned_unimpl)
+    && (VME2_MISC >> 2) < 8 * sizeof(1ULL)) ? 1 : -1];
+
 
 DEVICE_ACCESS(vme)
 {
@@ -134,13 +147,74 @@ DEVICE_ACCESS(vme)
 			d->reg[relative_addr / sizeof(uint32_t)] = idata;
 		break;
 
+	/*  #568 (vmedefaultkill): registers the header names but this model
+	    does not implement.  Each ended the emulator in default: below.
+	    The in-tree OpenBSD 2.2 guest reaches six of them: vme2chip_init()
+	    reads MASTERCTL and writes it back and writes MASTER3, MASTER4 and
+	    MASTER4MOD; vme2abort() reads IRQSTAT (served 0, it reports "irq
+	    not set" and returns before writing IRQCLR).  A bus error here
+	    would panic that guest's attach, so these DECLINE: a read is served
+	    the word preloaded above, which is 0 because nothing writes these
+	    words of d->reg[] (odata is deliberately not forced to 0, so a store
+	    added by a later edit would show in a read-back); a write is
+	    dropped; one fatal() per register per device, the first access's
+	    direction deciding its wording (#501's shape in dev_pcc2.c).
+	    Sub-word starts inside these words are not matched here and reach
+	    default: (vmewidthlanes).  */
+	case VME2_SADDR2:
+	case VME2_SLAVELMOD1:
+	case VME2_SLAVELMOD2:
+	case VME2_SLAVECTL:
+	case VME2_MASTER1:
+	case VME2_MASTER2:
+	case VME2_MASTER3:
+	case VME2_MASTER4:
+	case VME2_MASTER4MOD:
+	case VME2_MASTERCTL:
+	case VME2_DMACTL:
+	case VME2_DMAMODE:
+	case VME2_DMALADDR:
+	case VME2_DMAVMEADDR:
+	case VME2_DMACOUNT:
+	case VME2_DMATABLE:
+	case VME2_DMASTAT:
+	case VME2_T2CMP:
+	case VME2_T2COUNT:
+	case VME2_PRESCALE:
+	case VME2_IRQSTAT:
+	case VME2_SETSOFTIRQ:
+	case VME2_IRQCLR:
+	case VME2_IRQL1:
+	case VME2_IRQL2:
+	case VME2_MISC:
+		if (!(d->warned_unimpl & (1ULL << (relative_addr >> 2)))) {
+			d->warned_unimpl |= 1ULL << (relative_addr >> 2);
+			if (writeflag == MEM_WRITE)
+				fatal("[ vme: unimplemented write to register "
+				    "0x%x (len %d): 0x%llx -- declined.  (once) ]\n",
+				    (unsigned) relative_addr, (int) len,
+				    (unsigned long long) idata);
+			else
+				fatal("[ vme: unimplemented read from register "
+				    "0x%x (len %d) -- served 0x%x.  (once) ]\n",
+				    (unsigned) relative_addr, (int) len,
+				    (unsigned) odata);
+		}
+		break;
+
 	default:if (writeflag == MEM_READ)
 			debug("[ vme: unimplemented READ from offset 0x%x ]"
 			    "\n", (int)relative_addr);
 		else
 			debug("[ vme: unimplemented WRITE to offset 0x%x: "
 			    "0x%x ]\n", (int)relative_addr, (int)idata);
-		exit(1);
+		/*  #568 (vmedefaultkill): an offset this model does not service:
+		    no header-named register, or the inside of one (a sub-word
+		    start).  Refuse the access -- memory_rw then raises the m88k
+		    data-access exception, the bus error a badaddr() probe
+		    expects -- instead of exit(1), which ended the emulator with
+		    no visible reason (debug() is silent at default verbosity).  */
+		return 0;
 	}
 
 	if (writeflag == MEM_READ)
```

### 5b. The whole device after the fix, numbered from the working file

```c
  52  struct vme_data {
  53  	uint32_t	reg[VME_LEN / sizeof(uint32_t)];
  54  
  55  	/*  #568: one bit per register WORD (relative_addr >> 2) for the
  56  	    unimplemented-register announce below; the highest such word is
  57  	    VME2_MISC (0x8c >> 2 == 35).  Zeroed by DEVINIT's memset, so every
  58  	    instance starts with every announce armed.  */
  59  	uint64_t	warned_unimpl;
  60  };
  61  
  62  /*  #568: narrowing warned_unimpl, or the 1ULL below, would shift past bit
  63      VME2_MISC >> 2; make that a compile error (dev_pcc2.c's
  64      pcc2_w_fits_in_warned shape).  */
  65  typedef char vme_warned_fits[((VME2_MISC >> 2) <
  66      8 * sizeof(((struct vme_data *)0)->warned_unimpl)
  67      && (VME2_MISC >> 2) < 8 * sizeof(1ULL)) ? 1 : -1];
  68  
  69  
  70  DEVICE_ACCESS(vme)
  71  {
  72  	struct vme_data *d = (struct vme_data *) extra;
  73  	uint64_t idata = 0, odata = 0;
  74  
  75  	if (writeflag == MEM_WRITE)
  76  		idata = memory_readmax64(cpu, data, len);
  77  
  78  	if (writeflag == MEM_READ)
  79  		odata = d->reg[relative_addr / sizeof(uint32_t)];
  80  
  81  	switch (relative_addr) {
  82  
  83  	case 0:	/*  Used by OpenBSD/mvme88k when probing...  */
  84  		break;
  85  
  86  	case VME2_GCSRCTL:
  87  		debug("[ vme: unimplemented GCSRCTL ]\n");
  88  		break;
  89  
  90  	case VME2_TCR:
  91  		if (writeflag == MEM_READ)
  92  			debug("[ vme: unimplemented READ from TCR ]\n");
  93  		else
  94  			debug("[ vme: unimplemented WRITE to TCR: "
  95  			    "0x%x ]\n", (int)idata);
  96  		break;
  97  
  98  	case VME2_T1CMP:
  99  		if (writeflag == MEM_WRITE)
 100  			d->reg[relative_addr / sizeof(uint32_t)] = idata;
 101  		break;
 102  
 103  	case VME2_T1COUNT:
 104  		if (writeflag == MEM_WRITE)
 105  			d->reg[relative_addr / sizeof(uint32_t)] = idata;
 106  		else {
 107  			/*  NOTE! This is a quick hack. TODO: Fix!  */
 108  			d->reg[relative_addr / sizeof(uint32_t)] += 100;
 109  		}
 110  		break;
 111  
 112  	case VME2_TCTL:
 113  		if (writeflag == MEM_WRITE)
 114  			d->reg[relative_addr / sizeof(uint32_t)] = idata;
 115  
 116  		/*  TODO  */
 117  		/*  debug("[ vme: unimplemented TCTL ]\n");  */
 118  		break;
 119  
 120  	case VME2_IRQEN:
 121  		if (writeflag == MEM_READ)
 122  			debug("[ vme: unimplemented READ from IRQEN ]\n");
 123  		else
 124  			debug("[ vme: unimplemented WRITE to IRQEN: "
 125  			    "0x%x ]\n", (int)idata);
 126  		break;
 127  
 128  	case VME2_IRQL3:
 129  		if (writeflag == MEM_READ)
 130  			debug("[ vme: unimplemented READ from IRQL3 ]\n");
 131  		else
 132  			debug("[ vme: unimplemented WRITE to IRQL3: "
 133  			    "0x%x ]\n", (int)idata);
 134  		break;
 135  
 136  	case VME2_IRQL4:
 137  		if (writeflag == MEM_READ)
 138  			debug("[ vme: unimplemented READ from IRQL4 ]\n");
 139  		else
 140  			debug("[ vme: unimplemented WRITE to IRQL4: "
 141  			    "0x%x ]\n", (int)idata);
 142  		break;
 143  
 144  	case VME2_VBR:
 145  		/*  Vector Base Register.  */
 146  		if (writeflag == MEM_WRITE)
 147  			d->reg[relative_addr / sizeof(uint32_t)] = idata;
 148  		break;
 149  
 150  	/*  #568 (vmedefaultkill): registers the header names but this model
 151  	    does not implement.  Each ended the emulator in default: below.
 152  	    The in-tree OpenBSD 2.2 guest reaches six of them: vme2chip_init()
 153  	    reads MASTERCTL and writes it back and writes MASTER3, MASTER4 and
 154  	    MASTER4MOD; vme2abort() reads IRQSTAT (served 0, it reports "irq
 155  	    not set" and returns before writing IRQCLR).  A bus error here
 156  	    would panic that guest's attach, so these DECLINE: a read is served
 157  	    the word preloaded above, which is 0 because nothing writes these
 158  	    words of d->reg[] (odata is deliberately not forced to 0, so a store
 159  	    added by a later edit would show in a read-back); a write is
 160  	    dropped; one fatal() per register per device, the first access's
 161  	    direction deciding its wording (#501's shape in dev_pcc2.c).
 162  	    Sub-word starts inside these words are not matched here and reach
 163  	    default: (vmewidthlanes).  */
 164  	case VME2_SADDR2:
 165  	case VME2_SLAVELMOD1:
 166  	case VME2_SLAVELMOD2:
 167  	case VME2_SLAVECTL:
 168  	case VME2_MASTER1:
 169  	case VME2_MASTER2:
 170  	case VME2_MASTER3:
 171  	case VME2_MASTER4:
 172  	case VME2_MASTER4MOD:
 173  	case VME2_MASTERCTL:
 174  	case VME2_DMACTL:
 175  	case VME2_DMAMODE:
 176  	case VME2_DMALADDR:
 177  	case VME2_DMAVMEADDR:
 178  	case VME2_DMACOUNT:
 179  	case VME2_DMATABLE:
 180  	case VME2_DMASTAT:
 181  	case VME2_T2CMP:
 182  	case VME2_T2COUNT:
 183  	case VME2_PRESCALE:
 184  	case VME2_IRQSTAT:
 185  	case VME2_SETSOFTIRQ:
 186  	case VME2_IRQCLR:
 187  	case VME2_IRQL1:
 188  	case VME2_IRQL2:
 189  	case VME2_MISC:
 190  		if (!(d->warned_unimpl & (1ULL << (relative_addr >> 2)))) {
 191  			d->warned_unimpl |= 1ULL << (relative_addr >> 2);
 192  			if (writeflag == MEM_WRITE)
 193  				fatal("[ vme: unimplemented write to register "
 194  				    "0x%x (len %d): 0x%llx -- declined.  (once) ]\n",
 195  				    (unsigned) relative_addr, (int) len,
 196  				    (unsigned long long) idata);
 197  			else
 198  				fatal("[ vme: unimplemented read from register "
 199  				    "0x%x (len %d) -- served 0x%x.  (once) ]\n",
 200  				    (unsigned) relative_addr, (int) len,
 201  				    (unsigned) odata);
 202  		}
 203  		break;
 204  
 205  	default:if (writeflag == MEM_READ)
 206  			debug("[ vme: unimplemented READ from offset 0x%x ]"
 207  			    "\n", (int)relative_addr);
 208  		else
 209  			debug("[ vme: unimplemented WRITE to offset 0x%x: "
 210  			    "0x%x ]\n", (int)relative_addr, (int)idata);
 211  		/*  #568 (vmedefaultkill): an offset this model does not service:
 212  		    no header-named register, or the inside of one (a sub-word
 213  		    start).  Refuse the access -- memory_rw then raises the m88k
 214  		    data-access exception, the bus error a badaddr() probe
 215  		    expects -- instead of exit(1), which ended the emulator with
 216  		    no visible reason (debug() is silent at default verbosity).  */
 217  		return 0;
 218  	}
 219  
 220  	if (writeflag == MEM_READ)
 221  		memory_writemax64(cpu, data, len, odata);
 222  
 223  	return 1;
 224  }
 225  
 226  
 227  DEVINIT(vme)
 228  {
 229  	struct vme_data *d;
 230  
 231  	CHECK_ALLOCATION(d = (struct vme_data *) malloc(sizeof(struct vme_data)));
 232  	memset(d, 0, sizeof(struct vme_data));
 233  
 234  	/*  According to OpenBSD/mvme88k:  */
 235  	d->reg[VME2_VBR / sizeof(uint32_t)] =
 236  	    VME2_SET_VBR0(6) + VME2_SET_VBR1(7);
 237  
 238  	memory_device_register(devinit->machine->memory, devinit->name,
 239  	    devinit->addr, VME_LEN, dev_vme_access, (void *)d,
 240  	    DM_DEFAULT, NULL);
 241  
 242  	return 1;
 243  }
```

### 5c. Every store instruction the probe places, with the register seeds, verbatim from `regress/vme_default_probe.py` (the population-2 stores are lines 655, 675 and 735-746 -- POP2_OFFS is the 26 offsets; the others store to the ten cased offsets or to 0x90+; r2 holds WVAL, r12 NARROW, r10/r11 DHI/DLO)

```
 164  WVAL = 0xa5a5a5a5
 169  NARROW = 0xa1b2c3d4         # st.b / st.h source: distinct bytes, so a lane mix-up is visible
 170  DHI, DLO = 0x11223344, 0x55667788   # st.d source pair: HIGH word != low word, so a 32-bit truncation shows
 581  prog = [OR_I(4, 0, LIVE), LD(5, 0x88), ST(2, 0x50), LD(6, 0x50), BR_SELF()]
 582  r = stepped([GUARD, (CODE, prog)], [(2, T1VAL), (4, SENT), (5, SENT), (6, SENT)], 4)
 594  r = stepped([GUARD, (CODE, prog)], [(rr, SENT) for rr in CC_WANT], len(prog) - 1)
 605  prog = [VSIG(), ST(2, 0x50), LD(5, 0x50), LD(8, 0x2c), OR_I(7, 0, LIVE), BR_SELF()]
 607  r = freerun([GUARD, (CODE, prog)], [(2, T1VAL), (5, SENT), (7, SENT), (8, SENT), (30, SENT)],
 623  prog = [VSIG(), ST(2, 0x60), LD(4, 0x60), ST(7, 0x88), LD(5, 0x88), ST(11, 0x88), LD(12, 0x88),
 624          ST(8, 0x54), LD(9, 0x54), LD(10, 0x54), OR_I(31, 0, LIVE), BR_SELF()]
 625  r = stepped([GUARD, (CODE, prog)],
 641  prog = [VSIG()] + [ST(2, o) for o in (0x00, 0x2c, 0x4c, 0x6c, 0x80, 0x84)] + [OR_I(31, 0, LIVE), BR_SELF()]
 642  r = stepped([GUARD, (CODE, prog)], [(2, WVAL), (30, SENT), (31, SENT)], len(prog) - 1)
 650  r = stepped([GUARD, (CODE, prog)], [(30, SENT), (31, SENT)] + [(rr, SENT) for rr in REGS26], len(prog) - 1)
 655  prog = ([VSIG()] + [ST(2, o) for o in POP2_OFFS] + [OR_I(1, 0, STLIVE)]
 657  r = stepped([GUARD, (CODE, prog)], [(2, WVAL), (1, SENT), (30, SENT), (31, SENT)] + [(rr, SENT) for rr in REGS26],
 669  r = stepped([GUARD, (CODE, prog)], [(4, SENT), (5, SENT), (6, SENT), (7, SENT), (30, SENT), (31, SENT)],
 675  prog = [VSIG(), ST_B(12, 0x28), ST_H(12, 0x28), ST_D(10, 0x08), OR_I(1, 0, STLIVE),
 677  r = stepped([GUARD, (CODE, prog)], [(12, NARROW), (10, DHI), (11, DLO), (1, SENT), (4, SENT), (5, SENT),
 735  announce_pair(("p2 ann rd", "p2 ann rd 2"), lambda o: LD(4, o), lambda o: ST(2, o),
 737  announce_pair(("p2 ann wr", "p2 ann wr 2"), lambda o: ST(2, o), lambda o: LD(4, o),
 743  NW_WR = [(ST_B(12, 0x14), WR_LINE % (0x14, 1, NARROW & 0xff)),
 744           (ST_H(12, 0x1c), WR_LINE % (0x1c, 2, NARROW & 0xffff)),
 745           (ST_D(10, 0x20), WR_LINE % (0x20, 8, (DHI << 32) | DLO))]
 746  prog = [VSIG()] + [i for i, _ in NW_RD + NW_WR] + [OR_I(31, 0, LIVE), BR_SELF()]
 748  r = freerun([GUARD, (CODE, prog)], [(12, NARROW), (10, DHI), (11, DLO), (4, SENT), (5, SENT), (6, SENT),
 760      g_w = "%d/%d" % (sum(1 for _, w in NW_WR if l.count(w) == 1), nwr)
 788  fault_row("p1 fault wr", ST(2, 0x90), [(2, WVAL)], 0x90, DMT_ST_WORD, "st at 0x90: the word-store DMT0")
 791  r = stepped([GUARD, (CODE, prog)], [(4, SENT), (5, SENT), (6, SENT), (30, SENT)], 4, cr=True)
 826  prog = [VSIG(), LD_BU(4, 0x93), LD_HU(5, 0x96), LD_D(6, 0x98), ST_B(12, 0x9d), ST_H(12, 0xa2), ST_D(10, 0xa8),
```

## 6. Questions

1. **Adjudicate F1..F18 and D1..D5: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE**, one line each with the reason.
   For a finding that is your own, say whether my DISPOSITION and my FIX are right -- not merely whether the finding was.
2. **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  I accepted 14 of 18 findings outright and refined 2.  Name
   the one you would overturn first.
3. **The planned instrument revision (section 4's REV 3)** adds rows.  For EACH proposed row, name the mutant it is
   meant to kill and the observable that differs under it (the CHANNEL line) -- and say if a row's channel CANNOT vary
   under its mutant (vacuous by construction).  For F1 in particular: is one zero-store first access enough, or does
   the closure need a zero store at more than one width?
4. **WHAT DID ALL OF US MISS?**  You now have every seat's output.

If, while verifying a claim, you found something ELSE -- say so.

## 7. Answer format

Your token on the first line, then ONE line `VERDICT: PROCEED AS DISPOSED | PROCEED WITH CHANGES | DO NOT PROCEED -- <one
line>`, then Q1 as a table (id | ruling | reason), then Q2-Q4.  Facts and flags; no restating the packet.
