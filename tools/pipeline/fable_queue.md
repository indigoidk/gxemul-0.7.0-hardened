# FABLE JOB QUEUE — work that requires the flagship seat, held until quota allows

**Why this file exists.** Fable usage ran high on 2026-08-16 and the owner asked to conserve it.
Two standing directives make some work *only* Fable's, so it cannot simply be reassigned:

- **`regress` is FABLE-ONLY** — only the flagship seat reviews regression, batched.
- **full panel on every stage** — a stage is not complete without all nine seats, and Fable is
  one of them. Under the stop-and-ask rule, a stage missing Fable is **held**, not degraded.

**The rule this file enforces on itself:** a queued job is not a done job. Nothing here may be
counted as reviewed, and no round may close on the strength of a queued entry. If a round needs a
Fable stage and Fable is unavailable, the round **waits** — that is the directive, and the whole
reason the queue is written down rather than remembered.

---

## QUEUED — in priority order

### The AGENT seats on the cluster panels — **held by OWNER ALLOCATION, not by outage**

The nine cluster panels of 2026-08-19/20 fired panel.sh's **seven scriptable seats**. The two
Agent seats — `opus5` and `fable5` — were **not fired on them**, so those assess stages are 7/9
or 8/9, not complete.

**Both seats are ALIVE and answering.** This is an allocation, and the owner made it: *Opus
drives* (it is implementing the `pitlatch` round) and *Fable adjudicates* (it delivered the drop
docket on 2026-08-20), with Fable separately deprioritised as a review seat. Recorded per row by
seat name rather than left blank, because **a blank cell and a seat failure must not look
alike** — which is the whole reason this file exists.

**It surfaced only when the codex wall was discharged.** With a `[HELD AWAITING SEAT: codex]`
marker present each stage read as HELD and was accepted; removing the marker revealed the true
count. That is worth keeping: *one held marker can mask another gap*, and section H cannot see a
shortfall that a different hold is covering.

**Action:** fire `opus5` and `fable5` against the cluster briefs under `_scratchpad/brief_*.md`
(`wdcarm`, `smharness`, `triage4`, `timerdomain`, `m88k`, `harness`, `access`, `records`,
`last3`, `pit`) when the allocation frees them. Nothing is blocked on it — every disposition
those panels produced had six or seven seats behind it.

<!-- BEGIN GENERATED: codex-wall -- edit gen_codex_wall.py, not this block -->
### HELD STAGES -- every row awaiting a seat, derived from the ledger

`armbdt` (assess:codex) · `b118L` (assess:codex) · `b120r` (assess:codex) · `carrier` (regress:fable5) · `census` (assess:opus5) · `constblind` (assess:opus5) · `devexit` (assess:opus5) · `dfreq` (assess:codex) · `es438` (regress:fable5) · `exitsweep` (assess:codex) · `gateflr` (assess:opus5) · `ieeeupgrade` (assess:opus5) · `m8probe` (assess:opus5) · `m8sarseq` (assess:opus5) · `mrwstore2` (assess:opus5) · `ns16550` (regress:fable5) · `ovsync` (assess:codex; research:codex; review:codex) · `pcheck` (assess:opus5) · `pitclobber` (assess:codex) · `reprowitness` (assess:codex) · `seam` (assess:opus5) · `sh4sci` (regress:fable5) · `sh4tlbda2` (assess:fable5; review:fable5) · `wdccdbmidxfer` (research:fable5,opus5) · `xfamscope` (assess:opus5)

*** TWO DIFFERENT KINDS OF HOLD APPEAR BELOW AND THEY MUST NOT BE READ ALIKE. ***

* **codex** -- a genuine OUTAGE, now DISCHARGED. It hit its usage limit and echoed eleven
  briefs; on 2026-08-20 it answered a health test and all eleven were re-fired against
  byte-identical briefs and verified real. Only the older 08-17/08-18 panels remain.
* **opus5 / fable5** -- NOT an outage. Both are alive and answering. They are held by an
  **owner allocation**: Opus DRIVES (implementing rounds) and Fable ADJUDICATES (it delivered
  the drop docket), with Fable deprioritised as a review seat. The nine cluster panels fired
  panel.sh's seven scriptable seats only, so those assess stages are 7/9 or 8/9.

**That second kind surfaced only when the first was discharged**: with a codex marker present
each stage read HELD and was accepted, and removing it revealed the true count. *One held
marker can mask another gap* -- section H cannot see a shortfall that a different hold covers.

**Neither kind is a blank.** A blank cell and a seat failure must not look alike, and an
allocation is a third thing again: recorded by seat name, per row, with the reason.

**This is ONE outage plus one allocation, not 25 decisions, and it is written once rather than once per panel.**
**THE CODEX HISTORY, kept because it calibrates what a wall looks like.** Across ten panels it
produced the identical signature every time -- the echoed brief followed by the usage-limit
error -- in files of 26,992 / 11,180 / 10,036 / 8,323 / 12,414 / 11,938 / 10,726 / 16,694 /
19,649 / 21,348 bytes. *A size check alone scores those as the largest answers in their panels.*
`panel.sh`'s seat check caught each as RATE-LIMITED rather than counting the blank as agreement,
and the discharge re-verified every rerun the same way: delta over the brief, and the absence of
the usage-limit string in the tail.

**A DISCHARGED CODEX FINDING IS HISTORICAL UNLESS RE-CHECKED.** Each rerun answered the brief AS
IT WAS FIRED -- byte-identical, so its answer is comparable with the seats that answered live --
and the tree has moved since. Measured example: its rtcdet verdict was DEFECTIVE on a `+1`
mutant that "admits UINT64_MAX while all nine rows remain green" -- correct against the 9-row
table it was shown, and MEASURED CLOSED against today's 18-row table. Three further codex
recommendations are already settled by measurements on the record (`tfreq` is fixed;
`mrwstore2`'s "produce a real-guest witness" was measured impossible; `constblind`'s drop was
rejected after a live instance was found).

**Action for the remaining rows:** the older 08-17/08-18 panels (`exitsweep`, `ovsync`,
`armbdt`, `b118L`, `b120r`, `dfreq`, `reprowitness`) were NOT re-fired and still carry genuine
codex holds. For `opus5`/`fable5`, fire them against the cluster briefs when the owner's
allocation frees them. **A blank cell, a seat failure and an allocation are three different
things and this file names which is which.**

<!-- END GENERATED: codex-wall -->

### `lethalonly` (#462, `7c9dd9e` + `15c4b0a`) — regress stage — **QUEUED 2026-08-24**

Closed by MEASUREMENT the same day it was filed, which is why the regress review matters more
than usual: **the row that raised the class and the row that discharged it are the same
round's work, reviewed by the adjudicating seat and by nobody else.**

*What it closed on:* `Mf` — the ARMING arm's `fatal()` deleted, latch and `idata = 0` kept —
scored **53/58** and reddened `arm says` at 0 against a wanted 1, plus `both decl`, `arm once`,
`arm count2`, `arm enable2`, and no sixth row. So `arm says` observes a SILENCED DECLINE WITH
THE HOST ALIVE (`regress/artifacts/kill462/table3_58rows/probe_Mf.raw`).

*The rule question this carries*, and it is the reason to fire the seat rather than batch it:
**the carve-out.** The class says a row whose only kill is a lethal mutant is not proven to
observe what it claims — with the exception that a lethal-only kill is CORRECT when the row's
predicate computes nothing but NON-TERMINATION, because for such a row a non-lethal kill is
IMPOSSIBLE rather than merely absent. That exception was authored and adjudicated inside one
round. **Ask whether it is sound or whether it is an author excusing three of their own rows**
(`arm survive`, `nodata live`, `nodata stale`).

*Evidence to hand it:* the Mb1/Mb2 cross-pattern at 58 rows (a clean diagonal — each survival
row dies ONLY under the mutant re-fatalising its own arm), and the census correction from
22/3/32 to 21/4/32, where the defect was classifying by MUTANT IDENTITY instead of by the row's
OBSERVED failure mode. Lethality is PER-SESSION, not per-mutant.

### `gdromdefault` (#461, `ba30e64`) — regress stage — **QUEUED 2026-08-23**

Three panels ran on this round (pass 1, pass 2, pass 3) plus two flagship reviews, so
the diff itself is well covered. The regress question is narrower and concerns the
DETECTOR's shape rather than the fix.

**The question, and it comes from this round's own measurement:**

> `dma alias` — the row written specifically to pin the unaligned-store repair — was
> **STRUCTURALLY BLIND** to the one-character mutant that re-opened that exact repair
> (`& 3` -> `& 1`), because the row uses an ODD address and both guard forms drop it.
> The escape was found by an adversary, not by the row.
>
> **Is there a general rule here — that a row written FROM A FIX'S INTENT tests the
> intent rather than the boundary, and boundary rows must therefore come from
> somewhere other than the fix's author?**  If so it is a stronger statement than the
> existing ask-again, which asks the panel for another mutant AFTER a clean table;
> this would say something about who may write the row in the first place.

**Second, narrower:** `dma accept` and `accept8` are both READ-ONLY accept rows. A
flagship seat has already asked whether a read-only accept row can discharge a
de-escalation obligation, and kimi's M2 reached the same question independently
(whether the accept rows jointly assert quiescence AND write/read-back at all five
implemented DMA offsets). Two seats converging is usually this project's signal.

Also worth checking: the round declined a `relative_addr & 3` guard on the CONTROL
arm that two seats asked for, on the grounds it would be DEAD CODE there (no store
tail), and recorded the invariant instead. Is declining a guard and documenting an
invariant the right disposition, or does it just move the hazard into a comment?

### `sqreadtype` (#454, `3ff2138`) — regress stage — **QUEUED 2026-08-23**, and it
carries a RECORDED DISSENT that was never resolved

The round corrected a shipped gate row that pinned the OPPOSITE of the manual: the
store-queue PREF transfer is judged READ type. Its order discipline is the cleanest
instance of the oracle-correction rule on record -- re-pinned oracle **26/31 RED on
the committed build**, then 31/31 fixed, and the pass-1 panel proposed that order
after the brief proposed the reverse.

**The question, and it is a dissent rather than a gap:**

> The round shipped scope **C1**, which leaves the SQ **WRITE** half unjudged
> entirely -- `sh_translate_v2p()` maps `0xe0000000..0xe3ffffff` identically and
> unconditionally, because that is how an ordinary guest store reaches the modelled
> queue SRAM. So the initial-page-write exception and write-side protection cannot
> be raised at all, which the round states out loud and files as `sh4sqwrite`.
>
> **Codex dissented that C1 is an "unshippable intermediate state".** The
> round-scope rule decided against it — codex's own proposed witness needs a NEW
> oracle, and the rule says a second site joins only with no new oracle. That is a
> rule applied correctly to its author; it is not the same as the dissent being
> wrong.
>
> **Is "correct in one direction, silent in the other" a shippable state for a
> protection check?**  The round's defence is that the silent half was ALREADY
> silent before the fix, so nothing regressed and one named filing now carries it.
> The counter is that a half-judged protection path reads as judged.

Two further things worth a look, both from the round's own reviews: a seat found
**four sibling locations beyond the three the design named** (seven in total), which
is the corrected-in-one-place-survived-in-three failure caught before it shipped; and
the measuring seat found **`FLAG_NOEXCEPTIONS` returns 2 with `*return_paddr = 0`**,
landing the payload at PHYSICAL ZERO in silence, which scored full marks against the
value rows. Both were fixed in-round.

### `verdictbold` — regress stage — **QUEUED 2026-08-23**, and it carries a RULE QUESTION

Closed with a 17-row, 8-mutant selftest on `tools/pipeline/seat_verdicts.py`. Author
self-review disclosed (badge `A`) on the fix itself; the escapes came from four
independent seats and were then measured.

**The rule question, and it is the reason this is not batched with the closures:**

> Two mutants in this detector could not be made to fail, and each one taught something
> different. The first meant to restore a historical defect with ONE edit and measured
> GREEN, because `re.I` supplied the case-insensitivity the class edit was targeting —
> the defect needed BOTH edits. The second was aimed at a leading emphasis class and
> could not fail because that class was DEAD (`re.search` is unanchored).
>
> **Is "a mutant that will not die" a first-class RESULT that a round must dispose of
> explicitly, or is it noise to be silently re-aimed?**  This round treated them as
> results: the first made mutants multi-part, the second DELETED the dead code and
> recorded its own absence. That looks right, but it is a rule about how detectors are
> built and nothing has adjudicated it.
>
> The narrower half: **should a multi-part mutant be the default form?**  A single-edit
> mutant cannot express "restore what actually shipped" whenever two features combine
> to defend a row, and it reports the row as defended when nothing defended it — which
> is the vacuity shape this project already has four names for.

Also worth a look: the detector verifies against PRODUCTION (41 of 42 real seat answers
across six committed panel directories resolve). Is that a pattern other detectors here
should adopt — grading against accumulated real artefacts rather than only synthetic
rows — or is it a one-off that happens to be available for this file?

### `sh4iprbcd` + `sh4prioraise` (#458, `7e5c0f6`) — regress stage — **HELD, batched**

`regress/sh_iprbcd_probe.py`, 18 rows, wired into `gate_sh_rounding.sh` (PASS, 110 checks).
Measured 6/10 pre-fix, 18/18 post-fix. Kill table: `m_iprconly` 10/12, `m_nortc` 11/12,
`m_norescan` 11/12, `m_iprdread` 13/14, `m_sciftxonly` 15/18 — each red on exactly the row
built for it.

**THE QUESTIONS THIS STAGE IS HELD FOR** — named rather than left to be reconstructed:

1. **Is `iprd hold` an oracle or a veto?** It pins that a guest `IPRD := 0` does NOT move slot
   `0x240`. That is correct *today* because IRLM=1 is refused. If `sh4irlm` is ever
   implemented, the same row **blocks the feature** rather than defending a decision, and its
   oracle must be re-pinned FIRST under the oracle-correction rule. The closure note carries
   that tripwire. **Is a row whose correctness is contingent on another row staying open a
   legitimate detector, or is it a latent false oracle?** This is a rule question, not a
   sign-off.

2. **The detector grew twice inside one pass 2** — 12 -> 14 (the IPRD pair) -> 18 (the SCIF
   membership rows), each growth forced by a mutant the previous size could not see. Both
   growths were licensed under L1 (pre-ship construction) and the second additionally as a
   MEASURED FALSE PASS on live functionality (console input). **Is that the stopping rule
   working, or the #392 chain with better paperwork?** The distinguishing claim is that the
   ask-again cap was spent once and everything found after it was FILED — eight escape shapes
   in `sh4iprunpinned`, none fixed. Check that claim against the diff.

3. **Two table-reading rows (`iprb wdt`, `ipra rtc`) read CPU internals through the settings
   interface**, because the sources they cover have no `INTERRUPT_ASSERT` anywhere in the
   tree and no behavioural row can reach them. Two seats accepted the price; one asked for a
   read-only variant; one named a debugger interrupt-inject command as the shape that does
   not rot. **Is the settings channel the right home for detector-only observability?**

*Not a rule question, just a sign-off:* `sh4prioraise` closed on the same commit after the
assess-phase two-round ruling was overturned by an implementation fact. Recorded as a scope
CHANGE. Confirm the record reads honestly to someone who was not here.

---

### `sh4prioraise` (#458, `7e5c0f6`) — regress stage — **HELD, batched**

Closed on the SAME commit as `sh4iprbcd`, which the assess phase had ruled a separate round.
Covered by `raise` and `raise_lo` in `regress/sh_iprbcd_probe.py`; isolated by `m_norescan`
(11/12, red on `raise` alone).

**THE QUESTION:** the two-round ruling was overturned mid-round on an implementation fact —
rewriting priority nibbles of a table that may hold a pending request leaves `int_to_assert`
stale, so the rescan is load-bearing for the register fix itself and `rescanonly` measured
byte-identical to `pre`. **Was overturning an assess-phase scope ruling from inside the
round it constrains legitimate, given the round is the party that benefits?** The defence on
record is that the ruling was correct on its evidence, the change is recorded as a CHANGE
rather than merged silently, and an earlier draft of the round block contained both halves
of the contradiction ("is NOT in this round" beside "the rescan half IS present"). Check
whether that defence is sufficient or whether this is scope creep with a good story.

*Known gap, already filed as `sh4standinglower`:* no row asserts high then LOWERS while the
request stands, so a rescan guarded by `int_to_assert == 0` is predicted to escape.

---

### `sh4pclock` (#459, `0bb8be2`) — regress stage — **HELD, batched**

`regress/sh_pclock_probe.py`, 16 rows, wired into `gate_sh_rounding.sh` (PASS, 129 checks).
6/16 pre-fix, 16/16 post-fix, same script both sides. Kill table: `m_silent` 12/15,
`m_flat` 14/15, `m_nolatch` 14/15, `m_below` 14/15 — the last three each red on ONE row.

**THE QUESTIONS THIS STAGE IS HELD FOR:**

1. **A GATED PROBE THAT IS ALSO THE WITNESS.** `check_probe_wiring.py` refused this file
   while it was labelled a witness, on the correct ground that a witness asserts the PRE-fix
   symptom and goes red the day the fix lands. It is now labelled a detector, and the witness
   is the *recorded* 6/16 measurement rather than the rows. **Is that relabelling honest, or
   does it let a round claim a witness it no longer ships?** The same relabelling was applied
   to `#458`'s probe. This is a rule question about the whole witness/detector boundary, not
   a sign-off on one file.

2. **THE ROUND SHIPPED A FALSE CLAIM ABOUT ITS OWN PANEL.** A draft comment said "a panel of
   nine seats reached this 8-1" and was written while the ninth seat was still running; that
   seat then dissented. It was caught by the miscounted seat itself. Corrected in place. **Is
   in-place correction sufficient here, or does a false panel claim need a harder gate?** The
   existing sections G and H check that a seat which ANSWERED was recorded, and that seats
   were FIRED — neither can see a *count* asserted in prose before the answers arrive.

3. **THE PRE-FIX BUILD WAS UNDEFINED FOR PART OF THIS ROUND.** A seat measured
   `build/gxemul`'s mtime moving underneath it mid-review, so a run it believed was pre-fix
   was post-fix and the output could not distinguish them. The round re-derived its witness
   from `git show HEAD:`. **Should "rebuild the pre-fix from `git show HEAD:`, never from
   `build/`" become a harness rule?** It costs one line in every kill script.

*Sign-off only:* the four filed rows (`sh4testclock`, `sh4cpudevscope`, `sh4frqcr`,
`hpcshcpu`) — confirm the split between what shipped and what was filed reads honestly, and
in particular that `sh4cpudevscope` is correctly filed as the CLASS this round is one
instance of rather than as a duplicate of it.

---

### `sh4gdromexit` (#460, `98a3408`) — regress stage — **HELD, batched**

`regress/gdrom_data_probe.py`, 23 rows, wired into `gate_sh_rounding.sh` (PASS, 155 checks).
5/23 pre-fix, 23/23 post-fix, same script, pre-fix rebuilt from `git show HEAD:`. Kill table:
`m_widthdecline` 22/23 red on `accept w8` alone; deleted-arm 12/22; shared latch 21/22;
`0xffff`->`0` 21/22.

**THE QUESTIONS THIS STAGE IS HELD FOR** — named, not boilerplate:

1. **A DETECTOR THAT WAS INVERTED, AND WHAT THAT SAYS ABOUT THE ORACLE-CORRECTION RULE.** The
   first probe asserted the old `fatal()` text must be ABSENT, so deleting the register arm
   scored 13/13 and the intended fix 8/13 — it *rewarded* the vandalism it existed to
   forbid. It was caught by a seat building six variants, not by reading. **Is there a
   mechanical check for this class?** The vacuity floor tests (a) fails pre-fix, (b) fails on
   verbatim reinstatement, (c) fails on a null medium — and this detector would have passed
   (a) and (b). What it failed is something the floor does not name: *it did not fail on the
   CORRECT FIX*, which is not a clause anywhere. That looks like a genuine gap in the floor.

2. **RE-POINTED REGEXES.** A seat ruled that a pre-fix RED is NOT sufficient to make a
   re-pointed regex honest, because pre-fix the build reddens by PROCESS DEATH before any
   count is taken — death-red cannot distinguish "matches the correct diagnostic" from
   "matches any survival". What defends it is a SURVIVING-BUT-WRONG control. **Should that
   become a rule?** It is one sentence and it generalises past this round.

3. **A JOIN THAT FAILED ITS OWN TEST AND WAS TAKEN ANYWAY.** `:334` joined because it and the
   `COND_DATA_AVAIL` site are one predicate family. But the reopening rule prices "no new
   oracle", and reaching `:334` needed a new opcode, a new loop shape and a new state
   manipulation. It is recorded as **deliberately overridden**. **Is overriding that clause
   ever legitimate, and if so, what is the test?** Shipping three of four would have left a
   device where a declined read is safe in one state and lethal in another — which reads
   like a real reason, but "it would be untidy otherwise" is exactly the argument the
   reopening rule exists to refuse.

4. **SEVERITY INVERSION, STATED PLAINLY.** `gdromdefault` is MEASURED broader than everything
   this round fixed — 19 of 21 sampled offsets fatal, one predicate, ~248 of 256 byte
   offsets — and it was sequenced BEHIND this round. The stated reason is not severity but
   that its fix design is unsettled and this round builds the latch it needs. **Is that a
   sound exception to "severity orders the queue", or a rationalisation?**

*Sign-off only:* the shipped/filed split, and whether `gdromoob` reads correctly as
assessed-not-a-defect rather than as an unfixed finding.

---

### `selfcheckman` — regress stage — **HELD, batched**

Closed 2026-08-19 as **already fixed** by `7e3b120`, verified independently twice (the main
loop from the manifest's contents, the flagship seat from `gate_offline.sh:1645-1694`). No new
code shipped for it, and every battery run since `7e3b120` has already exercised the four
SELFCHECK manifest assertions.

That is exactly why it is queued rather than waived: *"already covered by earlier runs"* is a
**claim**, and the batched regress review is where a claim like that gets checked instead of
believed. Low priority — nothing is blocked on it.

One thing for the reviewer to confirm: the row's original premise line, *"ELEVEN differentials
have a gate-2 self-mutant, not twelve"*, is **stale** — `SM_COVERED` now lists 13 and all are
backed by real `selfmutant_one` calls. The closure records this; please sanity-check the count
against the tree at review time rather than against the closure note.

### 1. ~~`gate3scope` (#436) — review stage~~ — **DISCHARGED 2026-08-19, round CLOSED at 9/9.**
The ninth seat voted CLOSE and still found three MEASURED holes: `selfmutant.py` has **no
timeout**, so a hanging mutant emits no verdict token at all and wedges gate 2; the helper never
verifies the mutation LANDED in the tree it compiled (which unifies all three recorded
extra-flags hazards as one missing postcondition); and a malformed or absent `SM_EXEMPT` date
never expires, silently. Filed as `smhang`, `smnotland`, `smdatefmt`.

*Original entry, kept for the reasoning:*
**Status: was BLOCKING the round's closure.** Eight of nine seats have answered the *research* stage
and the implementation is done and gated, but the **review stage has not run at all**. Under the
full-panel rule this round cannot close until all nine review it, Fable included.

What Fable specifically should attack, given what the other seats already found:
- The control is a **liveness sentinel**, not a census — a measure seat proved 23 of 24 rows can
  be inert with both gate 2 and the self-mutant green. Is the shipped *wording* honest about that,
  or does it still read as a coverage claim anywhere?
- The **manifest** is the piece meant to stop this recurring on differential #12. Is a dated
  exemption list of six the right shape, or does a named exemption become permanent furniture?
- `selfmutant.py` scores a build failure as `SETUP`, deliberately unlike gate 3's `build_and_run()`
  which counts a crash as a detection (filed `#55`). Is the new helper's contract airtight, or does
  it have its own version of that bug?

### 2. ~~Regression review of the next full battery~~ — **DISCHARGED 2026-08-19.**
Adjudicated `verdict_20260819_135703` at `6014b7e` (REGRESS_PASS 16/16, 0 skipped). It
**refuted the main loop's own suspicion using the battery's own log** — gate 2 does assert the
guest-visible CHECK CONDITION, fault-injected through the real `diskimage_scsicommand()` — and
corrected the framing in both directions: the battery is not what proves the harness commits
were harmless (git is), but it IS the first end-to-end execution of their product. Named three
vacuity paths, the sharpest being that **#437's new code has never run under ASan**, because
gate 9 is a construction sweep. One cheap condition: run gate 3 once at HEAD, per
`selftest_mutation.sh`'s own header rule.

*Original entry:*
**FABLE-ONLY by directive.** The last one (R1–R9, three green batteries) is complete and committed.
The next battery — scheduled **23 Aug 18:00**, or any manual run before it — needs its own Fable
adjudication. It should specifically re-examine whether #436 changed what a green battery licenses:
the honest answer is probably *"a little, in one narrow way"*, and that is worth saying precisely.

### 3. ~~`selfmutant6`~~ — **DISCHARGED 2026-08-19.** All five controls built; `SM_EXEMPT` is `ieee_store:2099-01-01` alone, 11 days before the deadline. Kept struck-through rather than deleted so the queue shows what was done, not only what is left.

*Original entry, now false and kept only as the record of what was owed:* six differentials had
no failability control. Five were built on 2026-08-19; the sixth (`ieee_store`) is covered by
gate 3's weaker form and carries a far-future date — see `ieeeupgrade`, which argues that date
entrenches the weakest control on the largest differential.

### 4. `m8online` (`9494c6a`) — regression review never done, found mechanically
**FABLE-ONLY, and this entry is the first thing `check_fable_queue.py` caught.** The row is closed,
it changed code, and it has no `regress` entry. I first assumed the batched R1–R9 pass had covered
it and was about to write the attribution in — then read the brief's scope table, which lists R7 as
`#433`, a *different* commit. `9494c6a` appears nowhere in it. **So this is a real gap, and the
comfortable reading of it would have produced a rubber stamp on an unreviewed commit.**

Nearby and worth contrasting: `b47`/`b27` looked identical to this case and were **not** queued,
because their commit `2458cfb` *is* R5 and the brief does name it. They only ever lacked the
attribution, which is now written in. Two rows that look the same to the gate, two different
honest answers — which is why the gate names rows and does not decide them.

### 5. `exitsweep` — all three stages, PRE-EMPTIVELY QUEUED before the round starts
The next round by the owner's choice: `dev_luna88k.c:815` calls `exit(1)` on a guest write to
`INT_ST_MASK0-3` with any of bits 25..0 set (verified live). Under the full-panel rule its
**assess, research and review** stages each need all nine seats.

This is queued *before* the round exists on purpose. Every silent Fable gap in the ledger was
created mid-round, at the moment the stage was ready and the seat was not — which is exactly when
the queue is least likely to get written. Naming the three stages now means the round starts with
the obligation already recorded rather than discovering it at the point of maximum temptation
to proceed with eight.

### 11. `m8batc` (`7849fad`) — regress review
**FABLE-ONLY.** Closed, changed code, no `regress` entry.

39 mutants, 39 killed — the strongest kill table of the campaign. Two things a regress pass should
weigh rather than admire:

* **A mutant escaped everything, and the round's own hardening created it.** The first fixture used
  consecutive port addresses, catching a block-boundary mutant *by accident*; scattering them to
  close a different hole silently removed that coverage. **F17 is currently the only row defending
  that property.** Is any other row in either file similarly load-bearing-by-accident?
* **`diff_m8820x.c` now `#include`s the real `memory_m88k.c`.** That is what makes the oracle
  non-vacuous — but it means a differential named for a device now also compiles a CPU file, and
  ten kills land in the translator. `m8lanecomment` files the stale gate title; the deeper question
  is whether the file's *scope* is still what its name says.

### 10. `hpcabort` (`a29f87b`) — regress review
**FABLE-ONLY.** Closed, changed code, no `regress` entry.

Why it wants real time: its pass-2 panel had **five of seven seats say SHIP WITH CHANGES**, and
**four produced an eighth mutant independently** — all one class, because the detector pinned one
argument token and left every other field of the device string free. Two rows closed it. The
question for a regress pass is the one that generalises: **S1, S4 and S5 are all SOURCE-TEXT rows**,
and the round argues in each case that no behavioural row *can* catch the property. Is that argument
sound three times over, or is the file drifting toward asserting its own source?

Also carries a live residual pinned rather than fixed: `EXPECT_X_ONLY = 3`, three subtypes still
needing `-x` because two console inputs exist. That number goes to 0 in the commit that settles
which UART is the console.

### 9. `sh4pcicexit` (`6bec468`) — regress review, and THE GATE SAID THIS WAS ALREADY QUEUED
**FABLE-ONLY.** Closed, changed code, no `regress` entry.

*** THIS ENTRY EXISTS BECAUSE `check_fable_queue.py` REPORTED IT AS QUEUED WHEN IT WAS NOT. ***
Its membership test was a raw substring search over this whole file, and the only occurrence of
`sh4pcicexit` was a parenthetical cross-reference inside the `sh4bcr` entry above. A *mention*
satisfied "named in the queue". Found by the flagship seat in the batched pass; the check now
matches entry headings only.

Why it deserves real time, beyond the irony: **this round has the worst detector prior in the
project's history.** Its first detector passed SEVEN of seven mutants — one of them reinstating the
original host kill verbatim (`if (len == 2) exit(1);`), and three guest-visible. It is 38 rows now
and all seven die, but the closing move was *completing a product* (adding the width axis to a
census that only ever issued `len=4`), not adding spot rows. The question for a regress pass is
whether any OTHER quantifier in that file is still sampled rather than covered.

Two specific things:

* **`pcicmergeA` is filed and unwritten** — the PCICONF0 latch-merge reproduction has no row, and
  could not have had one before the third fault class landed, because a row written against the
  two-class code would have *asserted the merged behaviour as correct*. Worth checking the reasoning
  as much as the gap.
* **The fault classes are "kinds of complaint, not kinds of register"** — that distinction is what
  made the first two-class fix a half-fix. If a fourth complaint kind appears, does anything catch
  it being folded into an existing class?

### 8. `fbpending` (`3193d56`) — regress review, and the round it belongs to shipped UNREVIEWED
**FABLE-ONLY.** Closed, changed code, no `regress` entry.

Why this is worth flagship time rather than a formality: **the round shipped with no pass 2, no
CHANGELOG block, and a ledger row still reading `state=held` a day later.** The precommit gate
caught it by refusing the *next* commit. When the pass 2 finally ran it built twelve mutants and
found **five passing both detectors, eight passing the only detector any gate runs** — the smallest
being one token (`freq / 100.0`) that destroys 99% of the guest's clock.

R5 and R6 now close those, and were measured to. But the question a regress pass should ask is the
one the first detector answered wrongly: **R1 asserted an inequality against a constant while
printing the very number it should have compared against.** The same shape — an oracle that
computes the right value and then tests something weaker — is worth looking for in the rows this
round did *not* touch.

Two specific things, both recorded as untested rather than as findings:

* **`fbpending_drain_probe.py` runs in no gate at all**, and its assertion is opt-in
  (`--expect-cap`), so wiring it in without the flag would be born vacuous. Choosing the flag's
  value is choosing what the row asserts — and since the post-fix number is a *modular residue*,
  not the cap, a one-sided bound cannot tell a cap of 762 from one of 7.
* **The `fbpending_bound` self-mutant lane still does not run** (`fbsmlane`, dated `SM_EXEMPT` to
  2026-09-20), so this differential has one failability control where two are intended.

### 7. `sh4bcr` (`9de16b7`) — regress review, and the reason is a number
**FABLE-ONLY.** Closed, changed code, no `regress` entry.

Why this one is worth real flagship time rather than a formality: **its first nine-row detector
passed six mutants**, and one of them (`if (partial && writeflag == MEM_READ) exit(1);`) reinstated
the host kill this round exists to remove, with every row green. Seven of eight seats had said
SHIP over that detector. The rows are now 13 and every mutant dies to a named row — but the
question a regress pass should ask is whether **13 is enough**, given that 9 was confidently wrong.

Two specific things to look at, both recorded as untested predictions rather than findings:

* the pass-2 seat predicted, and did not build, that **a function-static latch instead of the
  struct field would pass all 13** — the shared-latch shape at device-instance rather than
  register granularity. It needs a two-machine config, which nothing in `regress/` currently
  builds.
* `D7a`/`D7b` construct a **big-endian machine from a config file**, a second invocation shape no
  other probe in the tree uses. It writes and unlinks a temp conf beside itself. That is worth an
  independent look for anything it leaves behind on a failure path.

Also carries the honest caveat that the round did NOT harden `dev_sh4`: eight measured
one-instruction kills remain in the same file (`sh4pcicexit`).

### 6. `pitflip` (`af4884c`) — regress review, and the round it belongs to ran NO PANEL AT ALL
**FABLE-ONLY.** Closed, changed code, no `regress` entry — the `m8online` shape, caught the same
mechanical way.

What makes this one worth the flagship's time rather than a formality: **the round was implemented
and gate-tested with no panel whatsoever**, which its implementing seat disclosed itself rather
than letting a blank read as agreement. The pass-2 panel then found that one of the three
mechanisms it adds — the control-word rewind — **shipped with zero detector coverage**, and two
seats independently produced the same one-line mutant that passed all ten rows while handing a
guest 265 Hz where it asked for 73. Rows R10/R11 close that, negative-controlled in both
directions and against a sibling mutant.

So the regress question here is not "does it still pass" but **whether R10/R11 are themselves
enough** — the measuring seat noted that R4/R7/R8/R9's ability to catch the *read*-side rewind
mutant is an accident of `PROLOGUE`'s A1 signature read leaving `rd_msb[0]` at 1, which nothing in
the file states. A refactor of `PROLOGUE` would silently un-pin it. That is exactly the kind of
latent-vacuity claim the batched regress pass exists to check.

Also carries an open UNKNOWN that a flagship reading may be able to settle where two seats could
not: `pitlatch2` — does a Counter Latch Command rewind the read flip-flop? The local `i8254.txt`
does not say and there is no second 8253/8254 source in the tree.

### 6. `fablequeue` (`c3d13e5`) and `carrier` (`1ba2cd4`) — regress review, queued BY THEIR OWN GATE
Both are harness rounds authored by the main loop with **no panel at all** — single-seat filings
carrying the `A` badge, which is why they must not read as reviewed. They are held `in work` rather
than closed, because the clean battery at `1ba2cd4` had not finished when they were written and a
row cannot honestly close on an unfinished battery.

**They are queued here because `check_fable_queue.py` was asked, prospectively, whether it would
fire when they close — and it does, naming both.** That was worth checking rather than assuming:
the author of a gate is the person least likely to notice it exempting his own work.

Worth Fable's attention specifically: rule 1's cutoff means a stage dated **before 2026-08-16 is
never examined**, so the gate is blind by construction to most of the ledger's history. That is
deliberate (a directive cannot judge work that predates it) but it does mean **the gate's green is
about recent rows only**, and nothing on the dashboard says so.

### 7. The five zero-seat triage rows — `b118L`, `b120r`, `ovsync`, `dfreq`, `armbdt`
Each is at **6/9** after the 2026-08-17 triage panel, held for **fable5, codex and grok**. These
had *no* seat entries at all before that panel — they were the emptiest cells in the matrix, and
the deepseek blanks the owner kept noticing were mostly rows of this kind.

**Fable's pass here is cheap and unusually well-prepared**, because the measure seat already did
the verification legwork and left four decided questions to adjudicate rather than investigate:

- **`b120r` is where the panel split, and it is worth Fable's judgement specifically.** Both
  file-reading seats say it is NOT a duplicate of the shipped ASC work (different layer, opposite
  direction: length fields inside the DATA_IN payload, not HBA transfer counts). Both packet seats
  voted DROP as a likely duplicate — **agreeing with the suspicion the brief itself planted.** The
  reading seats should win on repo fact, and the code confirms them, but the disagreement is on the
  record deliberately.
- **`b118L` is TRUE and INERT** — both call sites abort the process, so nothing consumes the broken
  entry. Recommended drop-as-a-round, keep-as-a-rider. That is a judgement call, which is Fable's.
- **`dfreq`** — unanimous close-as-design across all six seats that reached a verdict.
- **`armbdt`** ranks first, and its "zero seats" was a **ledger artifact**: the full analysis has
  been sitting in `OUTSTANDING_BUGS.md:2698+` all along.

### 8. `reprowitness` — a standing-rule challenge, and the highest-leverage item here
Raised unprompted by the measure seat: **the reproducibility rule asks "can this MACHINE boot?"
when it should ask "can this CODE PATH be executed?"** `armbdt` is the proof — no bootable ARM rig
exists here, yet gate 14 already scores 261 checks on `testarm` through the cold debugger with a
four-byte raw file. Machine-granularity would have demoted the best item on the triage list.

This needs the flagship seat because **it reopens `exitsweep`'s scope**, which was settled on rig
availability. If probe witnesses count equally, sites in devices no rig boots may still be
fixable-with-a-detector. It is a filing (one seat), not a short stage, so it is not blocking —
but it should be adjudicated before `exitsweep` implements anything.

### 9. `sh4rtcsr` (#449) — does the de-escalation clause need a companion rule?

A concrete question about this seat's own rule, raised by a measurement rather than an opinion.

`#449`'s accept-side row **A1 was written against `RTCSR_CMF` and was measured vacuous.** CMF is
**write-1-to-keep**, and nothing in the device ever sets it — so a guest *cannot* set that bit,
and the row could never trip a widened guard no matter what the mutant did. It was re-valued to
CKS|LMTS, which are ordinary storable bits, and then it fired.

**So: does the clause need a companion rule — that an accept-side row must use a value the guest
can actually PRODUCE?** The clause as written says pin the accept side of every predicate that
used to gate death. It does not say the pinning value must be reachable, and the obvious choice
here was the unreachable one.

Two more things for this seat, both from the same pass:

* *** A CLASS-SWAP MUTANT SCORES 10/10 AND IS EQUIVALENT, NOT SURVIVING. *** Swapping
  `SH4_VAL_RTCSRINT` for `SH4_VAL_RCR1INT` changes nothing observable, because the two bit sets
  are disjoint (`0x18` vs `0x42`) and the latch keys on bits. Nine classes now share one array
  and the separation rests entirely on that accident. Filed as `sh4latchcollide` — is a
  compile-time disjointness assertion worth it, or is this over-engineering?
* **Three seats caught a defect in the round's own brief**, by three different routes, and two of
  them returned DEFECT for it. The brief filtered its diff with grep and produced source that
  could not compile while claiming measurements against it. Is there a mechanical guard for that
  — e.g. precommit refusing a panel brief whose inlined diff does not apply cleanly?

### 10. `sh4chcr` (#448) — the FIRST APPLICATION of the de-escalation clause this seat wrote

Highest priority of the three, because it asks whether a rule this seat authored hours earlier
actually works when applied.

The `#447` adjudication established: *a fatal→survive fix deletes the accidental tripwire that
made guard growth self-announcing, so the detector shipping with the fix must pin the ACCEPT side
of every predicate that used to gate death.* `#448` is the first round to owe that, and rows
**A1–A4** are the attempt.

**ANSWERED 2026-08-21 by the flagship seat: A1–A4 substantially DISCHARGE the clause, and the
"RS gap" recorded here was itself a WRONG RECORD.**

*** This entry claimed "no accept row covers the RS field". That is FALSE, and the seat checked
it against the file. ***  A1's value `CHCR_LEGAL` carries `RS_ACCEPTED` (0x200) and requires ZERO
diagnostics, so narrowing or deleting `case 0x200:` makes the RS default print "resource select 2
… declined" — which matches the probe's own regex, and A1 reddens. A guard with exactly one
accepted encoding is the **easiest** to pin from above, not impossible: "a row per adjacent legal
value" degenerates to the single row carrying the lone member, and that row exists. The other
direction is pinned by R4/R5/R7.

The correct statement, which replaces the wrong one: *no accept row **varies** RS, because its
variation set is empty; A1 carries its only member.*

**THE REAL RESIDUAL, found by reading every row: the accept side is pinned at CHANNEL 0 ONLY,
uniformly across all four fields.** A1–A4 and X1 all write CHCR0; R6 and L3 reach channel 3 but
are reject rows. So a channel-conditional narrowing of any accept arm — `case 0x200: if (channel
== 0) break; else decline;`, the selector-guard family a reading seat named two rounds ago —
**passes all 18 rows**. This is `#447`'s H1 hole recurring in the very file built to answer
`#447`'s review. One row closes the instance axis for all four fields at once: CHCR3 =
`CHCR_LEGAL`, expect silence. Above the floor, so FILED as `sh4chcraccept` rather than reopened.

Also worth this seat's attention:

* *** FIVE detector rows were measured VACUOUS during the round and rebuilt *** — R2 (used the
  accepted RS so a `break` was invisible), L1 (second store a bit-subset of the first, so a
  whole-register latch computed `fresh == 0`), R5 (byte-identical to R4), R6 (proves reachability,
  not latch behaviour), and **R1 — the same defect as R2, fixed at R2/R3 in the same session and
  not carried across, with a comment left behind claiming it was covered.** A pass-2 seat found
  that one. Is there a cheap mechanical check for "sibling rows that should have been edited
  together", or is this irreducibly judgement?
* **X1 pins a defect that is NOT fixed** (`sh4dmacie`), so the gate reddens the day someone
  *[OVERTAKEN BY EVENTS 2026-08-26: `sh4dmacie` WAS fixed, by `#453`/`f532bb6`, and X1 now
  asserts survival plus one latched diagnostic rather than death.  A seat fired on this
  brief as written would be reviewing a defect that no longer exists -- the `sgiarcbiosoob`
  precedent, where a hold text outlived its own oracle.  Left in place with this bracket
  rather than deleted, because the brief's OTHER points are unaffected.]*
  repairs it, with the instruction "delete the row rather than the fix". Sound, or a trap?
* `fatal()` was kept for consistency with `#443`/`#447`. A pass-1 seat argued for `debug()` since
  the condition no longer terminates. `fatal()` ignores `-q`; `debug()` does not.
* F1's discriminating power is **conditional on `verbose == 0`** and the row says so — but it is
  the same conditional-rule shape this seat flagged as a liability on `#447`.

### 11. `sh4valguards` (#447) — review stage held, and the round shipped SAYING its detector is escapable

The review stage fired eight seats and not the flagship one. What it is owed for is unusually
well defined, because the panel already did the hard part and the round shipped anyway with the
gap named in its own CHANGELOG block.

**The judgement call to adjudicate, which is the real question:** nine measured mutants score
33/33 against the shipped detector, seven of them real defects, one a **guest-reachable host
death**. The round **filed** that as `sh4valrows` instead of fixing it in-round, on the argument
that this detector is **weak, not vacuous** — it kills 25 of 33 rows pre-fix and kills six real
mutants — whereas `#446`'s detector was vacuous (a 217-byte comment-only file passed it) and so
was replaced in-round.

Is that distinction sound, or is it a rationalisation? The stopping rule says a MEASURED FALSE
PASS gets fixed in-round, and these are measured false passes. The counter-argument is the
reopening rule: more witnesses create more ROUNDS, not bigger rounds. **Both rules apply and they
point opposite ways.** That is exactly an adjudication question and not a review question.

Worth weighing alongside it:

* *** The fix changed one hole's failure mode from LOUD to SILENT. *** Pre-`#447` a widened guard
  mask meant `exit(1)` on a legal write — unmissable. Post-`#447` it means a silently refused
  write. The round improved the failure and degraded its own detectability in the same edit, and
  **no rule in this harness would have caught that.** Should there be one?
* The round corrected a standing rule (`fatal()` vs `debug()` are distinguishable when
  free-running) and the correction is **conditional on `verbose == 0`** — a probe run with `-v`
  silently vacates the row that rests on it. Is a conditional rule in the carrier a liability?
* Six more guest-reachable `exit(1)` sites survive in the same file (`sh4chcr`, `sh4rtcsr`),
  measured during this pass. The in-file wording "four value guards in `DEVICE_ACCESS(sh4)`" is
  literally true but the file is not repaired — is the round title honest enough?

### 12. `probewiring` (`85bc6ab`) — regress review of a checker that now GATES every other detector

Queued by its own gate the moment it closed, which is the mechanism working: `regress` is
FABLE-ONLY, and a closed row owing a regress review reddens the next commit.

It matters more than a typical regress entry because **this checker is now upstream of every
other detector in the tree**. Section R fails a commit when a committed detector is run by no
gate, so a fault in `check_probe_wiring.py` does not fail loudly — it *stops demanding gates*,
and the harness quietly returns to the state it was written to fix.

Specific things for the flagship seat, all measured rather than guessed:

* **Command-position parsing is the whole defence** and it is a hand-written regex over
  comment-stripped shell. It correctly rejects `gate_hygiene.sh:331` — a line carrying a probe
  basename AND `python3` whose message is that the probe did NOT run. What else does it reject
  that it should accept, or accept that it should reject? A false ACCEPT is the dangerous
  direction: it marks an unwired probe as wired and the gap re-opens silently.
* **One level of variable indirection is resolved** (`DIVSWEEP=$HERE/x.py` … `python3
  "$DIVSWEEP"`). Two levels are not. Is one level the right cut, or an arbitrary one?
* **The four dated exemptions expire 2026-09-20**, a date the checker's author chose and
  explicitly flagged as a proposal. The owner has set these tighter before.
* **A detector misfiled as class `tool` is undetectable** beyond a filename tooth that a rename
  defeats. Stated in the file rather than hidden; is that residual acceptable?
* The **duplicate-key guard** added after the MANIFEST silently held one key twice: it re-reads
  the file's own source text because a dict literal cannot represent the fault it suffers from.
  Measured exit 0 clean / exit 2 duplicate — but that measurement was **void three times first**,
  through an eaten shell variable that read as 0.

Not blocking: the checker is green, its 18-mutant selftest was re-run independently before the
commit, and the four gaps it found are recorded as expiring debts rather than silence.

### 13. `sgiarcbiosoob` — a detector REPLACED mid-round, with no adversarial review of the replacement

The strongest reason on this list, because the round changed its own instrument after the panel
and nothing has attacked what replaced it.

`bcdbfb8` shipped the fix. Its pass-2 panel then measured the **shipped detector vacuous**: the
measuring seat built sixteen mutants and **all sixteen scored 7/7**, including
`0*ETHERNET_STRING_MAXLEN` — two characters, zero compiler warnings, the full heap overflow
restored and ASan-measured — and, decisively, **a 217-byte file containing nothing but a C
comment**. Six of seven scriptable seats returned DEFECT-IN-DETECTOR.

So the source-text detector was **replaced in the same round** by a runtime value oracle: break on
`arcbios_init()` in a real construction of the five reaching subtypes and require the ethernet
STRING to be the formatting of the MAC BYTES passed beside it. It kills every one of those
mutants, and a discriminating mutant was built for the one row (V4/ip32) that the first kill table
left unexercised.

**None of that has been reviewed by anything.** The panel reviewed the file it replaced. Specific
things worth attacking, all stated in the file rather than hidden:

* It reads arguments from **SysV AMD64 registers** (`$rcx`, `$r8`) because `build/gxemul` carries
  a symtab with no DWARF. That ties a committed gate row to one ABI. V6/V7 are supposed to make a
  wrong register fail loudly rather than read as zero — is that actually true, or is there a
  register whose garbage would pass?
* It **moved from gate 2 to gate 9**, on the argument that gate 2 runs no emulator at all and
  adding one would make its name untrue. Is gate 9 the right home, or does a non-instrumented run
  inside the ASan sweep confuse that gate's contract?
* `degrade()` was chosen over `gate_skip()` because gate_skip EXITS and would discard the sweep's
  own eleven checks. Correct call, or does a degraded gate 9 now under-report?
* The five-subtype scope (`REACHING`) is measured, not derived. If a subtype's fate changes, V8 is
  the only row that would notice — is one row enough there?

Not blocking: the fix is shipped and both gates are green. But this is precisely the
instrument-quality question the regress directive reserves for the flagship seat.

## `sh4sci` -- #451, the SCI command-byte validators (assess + review both held)

Two `exit(1)` calls in `sh4_sci_cmd()` ended the host on a guest-clocked command byte.
Three bytes reach them (0x00, 0x80, 0xb0); the third was found by a pass-1 seat AFTER the
witness had been written for two. Fixed by latching and declining; the round also fired
the standing `sh4latchcollide` disposition, converting `SH4_VAL_*` to a C99 enum, because
SCICMD is the tenth class.

Eight seats answered each stage. Gate 10 PASS at 60 checks; 22 mutants, no survivors.

**Two questions, both raised by measurement rather than by argument:**

* **ACCEPT-ROW FAILABILITY says build the JOINT growth mutant**, because #449's guard-only
  widening measured EQUIVALENT. At this site the measure seat found the OPPOSITE: the latch
  operand is a compile-time constant that cannot mask the guard, so guard-only and joint
  redden the accept rows byte for byte -- and guard-only ADDITIONALLY silences its own
  growth (one diagnostic line where joint prints two). **Guard-only is the harder form
  here.** Does the rule become "build the form the latch operand does not mask", or stay
  "joint" with this recorded as an exception?
* **The detector grew 9 -> 14 rows during pass 2, every added row forced by a MEASURED
  escape.** Two of the five surfaced only because seats were asked for another mutant
  AFTER fourteen were already dead. Is "ask again once the table is clean" worth making
  standing practice, or is it the #392 six-pass chain wearing a better hat? It converged
  here in two cycles and both cycles found real defects -- but that is one case.

Not blocking: shipped and gate-green.


## `sh4prio0` — regress review, queued 2026-08-22 (closed at `dc0c9d5`)

**Two questions, and the second is a RULE question, so it should not wait a week.**

1. **Disposition of two measured escapes.** #455 filed rather than fixed M4 (clears
   `SH_INT_ASSERTED` and returns) and M5 (deletes the guard outright). Both score 4/4 against
   the shipped rows because no row reads the pending bit or the arbitration state. The
   detector is above the vacuity floor — (a), (b), (c) all measured green — so the floor rules
   say coverage debt. **But the round's own comment argues that leaving `SH_INT_ASSERTED` set
   is REQUIRED, not merely correct**, because clearing it would make `sh4prioraise` unfixable.
   A required property whose sole carrier is a comment, with no row, is the L3 shape. Is FILE
   right for both, or does M4 owe a row?

2. **A rule question about accept-row failability.** The rule asks for the least-observable
   growth form that is measured non-equivalent at the site. I argued guard-only IS that form
   here **because there is no latch operand at all** — the fix is a bare `return`, so the
   JOINT form does not exist. Is "no latch operand, therefore guard-only" sound, or does the
   absence of a latch mean the rule wants a different reading at de-fatalising sites? This
   changes how future rounds of this shape are built, so per the queue-splitting rule it
   should get the seat at the next round boundary rather than in a weekly batch.

Not blocking: shipped, gate-green at 80 checks, and the accept row's kill is measured.


## `sh4irq15` (#456) and `sh4tlbmulti` (#457) — regress reviews, queued 2026-08-22

Both shipped green; neither is blocking. Each carries a RULE question, so per the
queue-splitting rule they want the seat at the next round boundary rather than a weekly batch.

**`sh4irq15` — a fix that silently voided a previous round's rows.** #456 moved the SH test
machine's interrupt line off priority 0, which made two of #455's seven rows exercise priority
1 while still reading GREEN. Measured: IRQ14 + a verbatim reinstatement of #455's kill scores
5/7 with both rows green; the same kill on IRQ15 scores 3/7 with both red. They were
repurposed into #456's own witness and #455's priority-0 coverage moved to the landisk TMU
rows. **Two questions.** Is repurpose-rather-than-drop right, or does the earlier round owe a
replacement so its coverage does not silently migrate to another rig? And: *nothing in the
harness noticed* — rows green, gate green. Is there a mechanical check for "a fix voided an
earlier round's rows", or is this a class we accept and hunt by hand?

**`sh4tlbmulti` — a no-op that only a pre-set state can see.** Three mutants are each killed
by exactly one row; a survival-only oracle passes all six. The sharpest, mutC, writes its own
reset arm setting `pc` and `vbr` and omitting the third statement — invisible to four of six
rows, because that statement is a **no-op from the reset-default SR**. It is caught only
because the row pre-sets SR. **Is "pre-set state so a no-op becomes observable" a general rule
worth carrying?** It looks like a sibling of accept-row failability — both choose a pinning
value the code path can actually reach — but the mechanism differs: failability is about the
predicate's OPERAND, this is about the STARTING STATE. Second question: two residuals were
filed rather than fixed (TEA never set, with a genuine UNKNOWN about which address is right;
and `EXPEVT_RESET_POWER` where the manual says manual-reset for the BL-set case). Is the
second — one identifier, in a function this round already touched — correctly filed?

---

## HOW TO RUN ONE

Agent tool, `model: "fable"`, framed as the SEAT role rather than the main-loop adjudicator — the
two hats are distinct and the seat reviews the design on its merits. Brief goes in
`_scratchpad/`, and the answer must be **read and recorded in `pipeline/ledger.json`**, or
`pipeline/check_seats_read.py` will fail the next commit. That check exists because three panels'
worth of seat answers went unread on this project, twice caught by the owner's eye rather than by
the harness.

## DEQUEUE DISCIPLINE

Delete an entry only when its answer is **recorded in the ledger** — not when the job is launched,
and not when it is skimmed. `check_stage_panels.py` is the mechanical backstop: it fails any
post-cutoff stage that moved on without all nine seats, so a silently dropped Fable job reddens
the next commit rather than passing quietly.

### `asicbadaddr` -- REGRESS REVIEW OWED (closed at 6cae5e4 f1fa6a0, 2026-08-25)

**The question this is queued for** -- a stage held for a seat must carry the question it is held
for, or the question gets reconstructed from the subject later: the round shipped a 13-row
detector whose last three rows were forced by seats, the final one (`mask9 rt`) by the capped
ask-again AFTER the table was already clean. **Does the shipped detector defend what the fix's
own comment calls load-bearing?** `alias`/`alias2`/`crossarr` are DISTINCTNESS rows and were
measured blind BY CONSTRUCTION to a `+1` translation; `mask9 rt` closes that single case with an
ANCHORED oracle. Is one anchored row enough, and is the contract's disclosure of `+2` as
unmeasured honest, or an evasion dressed as disclosure?

Artifacts: `regress/artifacts/asic463/table5_13rows/` -- 13/13 base, 12 mutants, no escapes.
Carrier vacuity-floor clause (f), THE ANCHOR RULE, was minted from this round and should be
reviewed alongside it.

### `gdromdmadefault` -- REGRESS REVIEW OWED (closed at 7c9dd9e)

**The question this is queued for:** this row joined #461/#462 on a MEASUREMENT rather than an
inference, and its `commits` field was empty until 2026-08-25 because the work shipped under the
joined round's id. **Is a duplicate-style close with the carrying commit now named the right
disposition, or does the row owe regress evidence of its own?**


### `sh4dmacie` -- REGRESS REVIEW OWED (closed at f532bb6)

**The question this is queued for:** the row was closed on RECORDS evidence, not on regress
evidence -- the shipped source reads `if (sh4_val_first(d, SH4_VAL_DMACIE, channel, 1u << 0))`
with zero `exit(` in that arm, and `OUTSTANDING_BUGS.md` has said "FIXED by #453" throughout.
**Does the de-fatalisation carry a DETECTOR that would redden if the `exit(1)` were reinstated,
or did #453 ship the fix without a row pinning it?** If the latter, this is vacuity-floor
clause (b) undischarged on a closed row, and the close is premature rather than merely late.

*Context worth having: the row sat `held` with an EMPTY commits field until 2026-08-26 while
the bug file said FIXED -- two records disagreeing about whether a defect was fixed. That was
corrected, and the close then followed for consistency with `panelseatlabel`, which closed the
same day on identical evidence. Section I refused the close until this review was queued, which
is the gate working: a product-code closure owes regress evidence in a way a harness closure
does not.*


## `arcbiosubsan` -- REGRESS stage owed (queued 2026-08-27)

Raised by the flagship-queue gate refusing a close: the row has both a full assess panel and a
full review panel, and a sound construction-rung witness, but **no regress stage was ever
fired**. It was closed in error during the closure sweep and immediately re-held.

**THE QUESTION THIS STAGE IS HELD FOR** (stated explicitly, because a held stage carrying only a
disposition note makes the seat guess, and a guessed question yields an answer to the wrong
question that still looks discharged):

> The fix removed undefined behaviour at ten uncast `buf[3]<<24` sites in `arcbios.c`. The
> witness is `construction:gate-9` -- a freshly rebuilt instrumented tree showing two UBSan
> left-shift lines on each of the five reaching SGI subtypes pre-fix and zero post-fix.
> **Is a construction-rung witness sufficient here, or does the absence of any runtime probe
> leave those ten sites uncovered against a future edit?**

> Concretely: *what is the smallest edit that re-introduces the 64-bit assembly defect at one of
> the ten sites and still shows zero UBSan lines on gate-9?*

Note the rebuild was load-bearing in the original measurement -- a stale July binary reported
the pre-fix pattern -- so any re-measurement must rebuild rather than reuse.

## `wdccdbmidxfer` — research stage HELD at 7/9 (2026-08-27)

Missing seats: **fable5, opus5**. The seven scriptable seats chose option B from a
five-member set; both flagship seats then answered the same design questions at PASS 2
and both found something the design pass had missed — fable5 MEASURED that option B alone
wedges a legal CDB permanently, opus5 MEASURED that the round's kill-table classified a
heap-buffer-overflow as an improvement.

**Not backfilled on purpose.** Writing a pass-1 entry from a pass-2 answer would be a false
record, and the stage genuinely ran seven seats.

> **The question:** three separate guards now stand in for one missing structural
> separation — the dispatch phase guard, the read-arm phase guard, and the occupancy bound
> that turns out to be the only thing sizing a `malloc(12)`. **Is option F (give the CDB
> its own accumulator, as `dev_mb89352.c` does) now the right call rather than a fourth
> guard?** And was option C (clear the flag at completion) wrongly dismissed, given that
> `#477`'s read-arm repair is a phase-scoped version of exactly that?

Measured migration cost of F, from a seat: it relocates where a CDB lives, so every
existing probe that fakes one stops working.
