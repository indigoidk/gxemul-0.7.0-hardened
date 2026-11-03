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

`alphaswpctxreg` (design:opus5) · `alphatbinegsel` (design:opus5) · `alphavmkill` (research:fable5) · `armbfiwidth` (design:opus5) · `armbfxwidth32` (assess:opus5; review:opus5) · `boilerplateprefix` (regress:fable5) · `carrier` (regress:fable5) · `cxlaunchdaybreak` (regress:fable5) · `cxlaunchquotation` (regress:fable5; review:fable5) · `dashokclass` (regress:fable5; review:fable5) · `es438` (regress:fable5) · `fableheldform` (design:fable5; review:fable5) · `fbctrlcmdkill` (regress:fable5; research:fable5; review:fable5) · `fbwitness` (regress:fable5) · `gdromcondlies` (regress:fable5) · `holdmarkermulti` (regress:fable5) · `i8259eoiirr` (research:agy,fable5; review:agy,fable5) · `ip30abortkill` (review:fable5) · `jazzvecdeassert` (research:fable5; review:codex,fable5) · `lcabadval` (assess:opus5) · `lcaconfbus1kill` (review:opus5) · `lcalenzerodrop` (regress:fable5) · `lecsrmask` (research:fable5; review:fable5) · `ledgerwitness` (regress:fable5) · `m88kbuserrregs` (research:fable5; review:fable5) · `m88kexcdeliver` (regress:fable5) · `m88kexcrrtrapmode` (regress:fable5) · `m88kscaledbyte` (research:fable5; review:fable5) · `mapledmaaddr` (regress:fable5; review:fable5) · `nineseatreminder` (regress:fable5) · `ns16550` (regress:fable5) · `pcc2widthkills` (assess:opus5) · `ppcdsformxo` (research:fable5; review:fable5) · `ppcgateimageskip` (regress:fable5; review:fable5) · `ppcrldimimask` (regress:fable5; review:fable5) · `ppcrlwimiwidth` (regress:fable5; review:fable5) · `scorehyphenfp` (regress:fable5) · `sgideprimop` (regress:fable5) · `sgidewidth` (regress:fable5) · `sgimtedepth4dead` (assess:fable5,opus5) · `sgirandomcolour` (regress:fable5; review:fable5) · `sgirekills` (assess:kimi,opus5; regress:fable5; research:fable5; review:fable5) · `sgireunmapped` (regress:fable5) · `sgitexindex` (assess:opus5) · `sh4sci` (regress:fable5) · `smhang` (regress:fable5) · `vmedefaultkill` (regress:fable5; research:agy,deepseek,kimi,minimax,opus5; review:agy,deepseek,kimi,minimax,opus5) · `wdccdbmidxfer` (regress:fable5; research:opus5) · `wdcdataoutdrain` (regress:fable5) · `wdclbaaddr` (research:kimi,minimax,opus5; review:kimi,minimax,opus5) · `wiringcliff` (design:fable5; review:fable5) · `xfamscope` (regress:fable5) · `xscaleinten` (regress:fable5; review:fable5)

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

**This is ONE outage plus one allocation, not 53 decisions, and it is written once rather than once per panel.**
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

*** THE PARAGRAPH THAT STOOD HERE WAS A FALSE ACTION-INSTRUCTION, RE-PRINTED INTO
`fable_queue.md` ON EVERY REGENERATION.  Corrected 2026-08-29. ***  It said: *"the older
08-17/08-18 panels (`exitsweep`, `ovsync`, `armbdt`, `b118L`, `b120r`, `dfreq`,
`reprowitness`) were NOT re-fired and still carry genuine codex holds."*

**Codex ANSWERED ALL SEVEN on 2026-08-26** -- verified by counting substantive codex entries
dated on or after that day on each row (ovsync carries three).  Six of the seven had their
stale markers defanged on 2026-08-29.  So this told the operator to re-fire seats that had
already answered, which is worse than a stale comment: a stale comment misleads a reader,
an action-instruction misdirects work.

**Action for the remaining rows:** consult the generated list below rather than any names
hardcoded here -- that is the whole point of generating it.  For `opus5`/`fable5`, fire them
against the cluster briefs when the owner's allocation frees them.  **A blank cell, a seat
failure and an allocation are three different things and this file names which is which.**

*A hardcoded roster inside a GENERATOR is a wrong record waiting for the data to move, which
is the same defect this project has now recorded for the `_scratchpad/*.pdf` inventory and the
seat-status tables.  Name no rows here that the ledger can name for you.*

<!-- END GENERATED: codex-wall -->

### `alphavmkill` (#541) — research stage — **QUEUED 2026-09-19**, a first-hand ruling owed

The pass-1 "fable5" answer (`panel_20260918_223507/fable5_p1.md`) was WRITTEN BY claude-opus-4-8 after a Fable
REFUSAL at the synthesis step (measured from the subagent transcript; `agentrefusal`).  The ledger entry is corrected
in place and the stage is HELD.  **Question:** is member 4 -- VA 0xfffffffd80000000 takes the base == 0 arm's identity
result like the rest of its window, the announcement latched once per CPU -- the right disposition against the full
option set?  **How:** at #541's pass-3 boundary, by RESUMING a Fable agent with a short verdict-first follow-up (the
measured remedy for a refusal fallback), then checking its turns with `_scratchpad/agent_models.py` before crediting.

### `pcc2c040assertrow` (#512, `9fa07fe`) — regress stage — **QUEUED 2026-09-11**

Surfaced by `check_fable_queue.py` while it was refusing an unrelated commit: *"closed at 9fa07fe
with NO regress entry and not queued"*.  **Holding a stage and queueing it are ONE action**, and
this row had done neither — it simply closed.

The row itself is the interesting part, and it is why the regress review is worth Fable's time
rather than being a formality.  `#512`'s detector had a **MEASURED clause-(d) escape**: a fix that
announces correctly and forgets `assert = 0` scored **7/7**.  The repair needed a **FREE-RUNNING**
probe, because the ICR INT bit is masked out of every guest-writable arm and its only producer is a
host-timer callback that `step` STOPS — `debugger.c:800` calls `timer_stop()` and the step command
returns before `timer_start()`, so a stepped probe reads "not delivered" on a correct build and on
a mutant alike.  That is the vacuous shape in its purest form, and it is a trap any future
interrupt-delivery detector in this tree can fall into.

It closed with `detector:regress/pcc2_c040_probe.py` naming four L2 rows (`irq pending`,
`irq live`, `c040 noassert`, `c040 noassert2`), with all three previously-sweeping clause-(d)
mutants killed.

**THE REGRESS QUESTION, stated so the seat is not guessing what it is asked** (a stage held FOR a
seat must carry the question it is held for — this queue's own rule, which scored zero compliance
once already):

> The four rows were added in response to a measured escape.  **Does the free-running oracle they
> depend on carry a wall-clock budget, and if so is it load-sensitive?**  This project has a
> recorded case of a free-running interrupt row being the SOLE discriminator for a mutant while
> also being the most timing-fragile row in its suite (`xscaleinten`'s `ANCHOR_EXC`, 2026-09-11).
> If `pcc2_c040_probe.py` has the same shape, the round shipped a detector whose only guard against
> its own measured escape can flake in a gate.

---

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

---

## 2026-08-27 -- two rows closed as RECORDS CORRECTIONS, and both raise the SAME rule question

### `wdcdataoutdrain`

### `wdccdbmidxfer`

*(Both ids head their own line above, because `check_fable_queue.py` counts an id as queued
only when it HEADS an entry or sits in the generated wall block -- never from prose. That
checker's own comment records being bitten by a parenthetical cross-reference satisfying
"named in the queue", on the round with the worst regression risk in its batch. My first
draft of this entry made exactly that mistake.)*

`wdcdataoutdrain` and `wdccdbmidxfer` were found closed-in-fact and open-in-record: each
fix shipped rounds ago under a full nine-seat pass-2 panel, each reproduction row is
committed and green, and only the ledger state was stale. Verified before closing --
`git log -S` on each fix text, each row DEFINED and REGISTERED in the detector, each
reporting `ok` on the current 87-row baseline.

**The gates refused both closures, and they were right to.** `check_fable_queue` wanted a
regress entry; `check_stage_panels` refused a close while a research stage sat at 7 of 9.

> **THE QUESTION, and it is one question wearing two row numbers: WHICH PANEL DISCHARGES A
> ROW -- the row's own stage, or the stage of the round that actually fixed it?**

Today the gates demand the first. If that is right, then **a row can never close on work
done under another row's number** -- which is how most cross-filed fixes land here, and
these two are only the instances that happened to be noticed. The two missing seats should
then be fired, and the same audit run across the other cross-filed rows.

If it is wrong, the checks need a **fixed-elsewhere** disposition that names the discharging
commit and panel instead of demanding a fresh stage.

**Please do not answer "fire the seats" without saying which of those the rule is.** A
stage fired to satisfy a check, that measures nothing the fixing round did not already
measure, is a stage that cannot fail -- and this project treats a check that cannot fail as
worse than no check, because it reassures.

*Provenance: found by chasing a dangling citation (`_scratchpad/held_repro_rows.c`, a file
that does not exist) that a read-only research subagent noticed while censusing something
else entirely. Nothing systematically re-checks a citation after the thing it cites moves.*

## wdcringambig / wdcaddtoinbufbound -- #484 regress stage (queued 2026-08-27)

The fix and its detector are committed, and **pass 2 on the real diff HAS run** --
kimi, opus5 and fable5 all answered it on 2026-08-27, and fable5's HOLD verdict on
that pass is what produced the corrections the round then shipped.

> *This paragraph read "its 119-row detector are committed; pass 2 on the real diff
> has not run" until 2026-08-30.  **Both halves were false.**  The detector shipped
> at 127 rows (up from 103); 119 was an intermediate count frozen mid-round.  The
> row count is deliberately not restated as a fresh literal here -- read the #484
> round block in CHANGELOG.md, which names it beside the gate and kill-table figures
> that were measured with it.  Found by a research agent checking something else,
> which is how every records defect in this file has been found.*
The panel saw the pass-1 brief only.

TWO QUESTIONS, both measurable:

1. The round claims the bulk-arm hunk is licensed by a MEASURED delta -- the producer-only
   variant (`Md_prodonly`) scores 13/16 and dies. **Verify that on the shipped bytes**,
   not on my report. Three reading seats judged that arm unreachable and one measuring
   seat refuted them; the disposition rests on the measurement being right.

2. Is `512 * to_read > (tail - head - 1 + SIZE) % SIZE` correct at **both** wrap
   orientations, or is there an orientation R7/R8 happen not to build? Those two rows
   were written from one setup (`head < tail`), which is exactly the shape that hides an
   asymmetry.

## wdcfloodstale -- #486 research stage -- ANSWERED 2026-08-27, hold released

The flagship seat answered: RE-AIM, one round, header correction inseparable, two mutations
owed (M_relatch and M_silent, the second being the anti-fake control).  It also named THREE
option-set members I had missed -- including re-pinning the want to 0, which it flagged as
*the cheapest path to a green battery* and rejected as a check that cannot fail.

*Original question, kept for the record:*

## wdcfloodstale -- #486 research stage (queued 2026-08-27)

Pass 1 is short two Agent seats and they are still running. **The question they carry is
the one the whole disposition turns on: what is the wall-clock of the re-aimed row?**

I settled by reading that the overrun `fatal()` is SYNCHRONOUS inside the data-port write
handler, so a stepped probe can see it -- free-running is a SPEED choice, not a correctness
one. So:

* if `step 394202` is tolerable, the round shrinks to a count change plus a header
  correction and needs no free-running conversion at all;
* if it is not, the conversion is required, and the `kimi-k3:cloud` seat's SPLIT proposal
  becomes right -- land the header fix now (immediately true) and the re-aim separately,
  since the deciding variable is not *same file* but **same landing date**, and Sunday's
  battery is the deadline.

## wdcoddstep -- regress stage (queued 2026-08-27)

Closed as **OVERTAKEN** by `#475`'s clamp, measured at HEAD with a discriminating control
(remove the clamp and the row's own figures return: `atapi_len -1`, `received 4` of 3).

**The question is the PRECEDENT, not this row.** The closure adds NO ROW: eight committed
rows already red on that control, two pinning exactly the saturation and truthfulness halves,
so the addition licence refuses one. Is a zero-row overtaken-closure right, or does a row
closed by someone else's fix owe a carrier of its own so the coverage is attributable?

I argue no. But **three more queue items are candidates for overtaken-closure** and they will
copy whatever this one does.

## wdcnoirq -- regress stage (queued 2026-08-27)

**A rule question, not a row question.** This round's detector was found below the floor
**twice on the same pass**, by two seats, for two different reasons:

* `M10` -- an invented predicate at the SEC arm, which you ruled **outside** clause (d)'s bound;
* `D1..D5` -- task-file guards at the `default:` arm, which are **inside** it, because the
  guarded body reads exactly those fields (they are literally the `fatal()` arguments).

Both closed in-round. But **the pre-table GUARD-FIELD-vs-BODY-FIELD check exists precisely to
enumerate `D1..D5` mechanically**, and this round ran no pre-table check at all — it went from
design straight to a table.

**Should that check be MANDATORY before any kill table rather than recommended?** It would have
cost one grep and saved two floor breaches and a whole pass. I argue yes — but it adds a
required step to every round, which needs your ruling rather than mine.

## shortread (#488) -- regress stage (queued 2026-08-27)

**A rule question the round produced by accident, and it is about BRIEFS rather than rows.**

Three packet-fed seats refused to ratify pass 2 and all three named the SAME missing fact:
the brief inlined a four-line window and not the function's `return`, so "the only consumer
of `totallenread` is the tail memset" and "the overlaid path returns `len` or 0" were not
checkable from the packet. Both are true. **But `fatal()` returning had been SETTLED IN
PASS 1 of this same round, and I did not carry the settled fact into the pass-2 packet** --
so three seats spent their answers re-deriving it, and one built a sound conditional defect
report on top of it ("if `fatal()` does not return, the memset is dead code").

**Should a pass-2 packet be REQUIRED to re-inline every premise pass 1 settled?** It costs a
paragraph and it is mechanical -- the pass-1 record already lists them. I argue yes. What I
cannot judge alone is whether that becomes a checkable brief-template line or stays prose,
given this project's own finding that prose rules fire only when they sit in the artifact
present at the moment of decision -- and a brief IS that artifact, which is the one place
prose has demonstrably worked.

**A second, smaller question in the same round.** The capped ask-again found three escapes.
I took one and filed two, reasoning that "the cap says I may take only one". The adjudicator
corrected the warrant: **the cap limits ASK-AGAINS, not FINDINGS** (`#452` took six rows from
one ask), and `E1` was never discretionary anyway -- `if (X)` -> `if (X && Y)` on the
dominating predicate is the canonical clause-(d) form, so it was a floor breach repaired
in-round. Pass 2 then closed the other two as well. **Is "one ask, all its findings" the
right reading, and should the carrier say so?** The cap's anti-runaway purpose survives
either way, but the two readings differ by several rows per round.

## gdromwarnbits -- assess stage (queued 2026-08-27)

**A rule question about PRE-SET TRIGGERS, raised by the gate refusing a closure.**

`dev_dreamcast_gdrom.c` carried a trigger written in advance: *"at the SEVENTH bit, widen
`warned` and convert these to an enum of bit POSITIONS ending in a GDROM_W_NBITS count."*
`gdromexitsix` Round 1 needs three more latches against six in use, so it fired. I executed
it: six masks became an enum, `warned` widened to uint32_t, and a compiled check confirms all
six masks are BIT-IDENTICAL to the originals.

Then I closed the row on a 2-seat stage and `precommit_check.sh` refused, correctly -- the
owner's rule is FULL PANEL ON EVERY STAGE. The row is now `in work` with the code shipped.

**The question: does discharging a pre-set trigger need a full panel?** The design decision
was made when the trigger was WRITTEN; this round only detected the condition and executed
it, and behaviour-preservation is measured rather than argued. Nine seats on a decided,
mechanical, measured-equivalent refactor may be the wrong use of the roster -- or the rule
may be exactly right that nothing closes without one, because "it was decided in advance" is
what every unreviewed change says about itself.

I lean toward: **a pre-set trigger discharge needs a panel only if it makes any choice the
trigger did not already fix.** This one made none -- the trigger named the enum, the count
suffix, and the mask form. But that test is mine and it is the kind of self-serving line a
seat should check rather than accept.

*Note the precedent it would set either way: `dev_sh4.c`'s equivalent conversion fired the
same way on its own pre-set trigger and the carrier records it as discharged, so whatever is
ruled here should be read back onto that one.*

## proberowsubset -- assess stage (queued 2026-08-29)

**The 2026-08-29 adjudication moved the row-filter spec HERE and added a fifth guard**, so
this row now carries a design that has never been panelled. The owner already ruled the
filter "ships as its own round with its own panel and its own negative controls"; that panel
has not run.

**Is the five-guard spec sufficient, and is SESSION-gating the right granularity?**

Guard 5 is the one the 08-28 spec dropped and the reason this is not a rubber stamp:
`GDROM_DEF_CONTROL` prints OK on `all(rows)`, and **`all([])` is True** — so a filter
excluding every control row passes guards 1–4 while the control line reports OK having
measured nothing. **The first use of the feature would manufacture a vacuous liveness claim
automatically.** Guard 5: controls are exempt from filtering, or the control line hard-fails
on an empty control set.

And a granularity constraint the panel should test rather than accept: selection must gate
SESSIONS, because 36 of 39 are module-level — a `row()`-level filter passes all five guards
and saves nothing.

---

### `widthkillclass` — review stage HELD at 2/9, awaiting the FINAL diff

**Held for: fable5, codex, grok, kimi, glm, deepseek, minimax.**

**Does the shipped `#497` diff — the FINAL one, after the kill table and after three
in-flight corrections — carry the residual-lethality sentence, the corrected memory-safety
characterisation, and rows that match its own sibling-parity verdict that the six arms are
NOT symmetric?**

This is not a scheduling hold, it is a **one-instrument** hold. Two seats have already
reviewed this diff (opus5's PRETABLE + implementation, agy's read-only review), and firing
the other seven right now would panel a **moving target**: the kill table is still running
against it, and three corrections are in flight to the implementing seat —

1. the **residual-lethality sentence** `#497` owes: the width guard is evaluated first, so
   after the fix a 4-byte read declines safely while **an ordinary 8-byte `ld` still ends
   the host at all six fixed windows**, because `len == 8` falls straight through to the
   read arm's `exit(1)`. The 1:1 width/read pairing makes that residual exact rather than
   vague — six width kills fixed leaves six read kills at the same six offsets;
2. the **corrected memory-safety characterisation** — `offsetof`, compiled and run, showed
   `re_linear_a[32]` IS `re_linear_b[0]` and `re_linear_b[32]` IS `de_reg[0]`, both at +0,
   so the over-run is UB plus silent intra-struct cross-array corruption, **not** a wild
   write, **not** a host crash, and **not** something plain ASAN can see. My brief told the
   seat to call it "load-bearing HOST memory safety", which would have shipped an L4 wrong
   record in product code;
3. the **alignment clause** — the invariant holds on every guest path (`ld`/`sd` raise
   ADES/ADEL before `memory_rw` is called; `ldl`/`ldr`/`sdl`/`sdr` coerce with
   `aligned_addr = addr & ~(wlen-1)`), but the host debugger's `put d` prints a warning and
   **proceeds**. Guest-only is true and incomplete; the comment should say which.

A panel convened on a diff that changes underneath it reviews code nobody will ship. That is
the one-instrument rule the comparison-run discipline already states, applied to a panel
instead of a probe.

**RELEASE CONDITION, stated so this hold cannot quietly become forgotten:** the kill table
reports and the diff stops changing. Then pass 2 fires on the FINAL diff with all seven
missing seats, in one panel. The two existing entries are **not** re-fired and do **not**
count toward the nine — a stage held for seven seats that closes with two is the
seat-failure-counted-as-agreement shape.

**The specific thing I want the panel hardest on:** the sibling-parity verdict says the six
arms are **not** symmetric — for TLB_A/B/C and TEX the width guard protects correctness only,
for LINEAR_A/B it is additionally the only thing preventing the OOB. Does that asymmetry
demand asymmetric ROWS, or is one decline row per window enough? Rows are owed per enumerated
mutant, never per site that "feels riskier" — a row added on feel is the addition licence's
"cannot hurt" wearing detector clothes.

---

### `sgirekills` — assess stage HELD at 2/9, awaiting `#497`'s table

**Held for: opus5, codex, grok, kimi, glm, deepseek, minimax.**

**TEX is ACCEPT only in the MIRRORED form — the read using the same `>> 3` expression as the
store — which round-trips per frame while shipping hardware-wrong reads at overlapping
offsets. Is a knowingly-wrong-but-self-consistent readback better than DECLINING that one arm
until `sgitexindex` lands? And is the round-trip row genuinely sufficient coupling
enforcement, or does a mirrored TEX read make the wrong index HARDER to fix by giving it a
green row?**

The rest of the design is settled and is on the row: five arms clean ACCEPT (TLB A/B/C
round-trip byte-exactly on this big-endian machine; LINEAR A/B are byte-order symmetric by
construction), TEX refuted as clean-ACCEPT because **`re_tex` has zero consumers** — it
appears three times in the file: declaration, store, and a `debug()` printing back what was
just stored — five named ACCEPT obligations, and an ordering dependency on `#497` for
**witness quality**, not merely for latch infrastructure: a faithful round-trip through a
device is value-indistinguishable from RAM, and the device-signature control is that
post-`#497` a 4-byte read *declines and returns 0* while RAM would serve it.

**Held rather than fired because a measurement is in flight.** `#497`'s table 2 is running
with wall-clock-sensitive oracles and the carrier serialises panel seats against it. Firing
seven CPU-bound seats now would risk a false FAIL in the round's most expensive measurement,
to save an hour on a round that cannot start until that table finishes anyway.

**Release condition:** `#497`'s table completes. The two existing entries are **not** re-fired
and do **not** count toward the nine.


---

## 2026-09-06 — THE THREE-DAY WALL: everything owed to the flagship seat while its allowance is out

**The wall is a fact, not an inference.** A real invocation at 12:40 returned HTTP 429
`You've reached your Fable limit`, and the owner states the allowance resets on **the 9th**. So
this is not the minutes-long wall the carrier's "test the seat, do not reason about it" rule is
usually about; it is three days, and the standing response to that is different: the rounds do
NOT wait, they close on the seats that answered and the flagship pass lands afterwards under the
**late-dissent rule** — closure changes the licence, never the truth-value. Every item below is
therefore *owed and written down*, not *blocking*.

**Read this section first on the 9th.** It is ordered by what a late dissent could still change.

### ~~1. `m88kexcdeliver` (#502) — passes 2 through 8, and the deferred ADJUDICATION~~ — **ANSWERED 2026-10-16** by Fable 5.1; GPT-6 Astra, Grok 4.7 and GLM 5.3 held it moot for the closure — the block at the end of this item

**Held for: fable5 (all passes), opus5 (passes 6-8).** Eight panel passes ran; the flagship seat
answered none of them. Packets, newest first:
`regress/artifacts/m88kexcdeliver/brief_m88kexc_p8.md` (the closing pass: probe v10 → v14, the
seven-mutant table 11, and the one question), then the pass-7, pass-6 and pass-4 briefs in the
same directory, with every seat's answer under `pass<N>_panel_*/`.

> **THE QUESTION: eleven kill tables and eight passes closed a detector that five separate
> mutants swept as recently as pass 7. Is the chain's stop condition being MET, or merely being
> declared? Specifically — the (d) DEPENDS-ON enumeration this round used treats the SFRZ
> re-route's PSR read as in-scope for PSR-bit conjuncts and switch 1's `implemented` arms as
> out of scope, because those arms read no PSR bit. That distinction is what makes the
> remaining {arm} × {C, IND, SFD1} surface clause-(e) debt rather than a floor breach. Is it
> the right cut?** Put precisely, because the evidence cuts finer than the question does: a
> pass-7 mutant (M_MISNOC) built to DEMONSTRATE that debt measured 41/41 on the old instrument
> and was then KILLED, 45/46, by the repair's own new `errc` row -- whose second fault is a
> MISALIGNED access with the carry bit set. That does not by itself refute the cut, since floor
> versus debt is a claim about what a round OWES rather than about what its rows happen to
> cover; what it does show is that the disclosed surface was smaller than the disclosure said,
> and the round narrowed the docstring rather than leave it overclaiming. **The question for the
> seat is whether "the arm reads no PSR bit" is the right test at all, given that the FAULT
> reaching the arm carries PSR state the arm could trivially be made to read.**

Second question, count named: of the pass-7 dispositions (five row closures; one seat claim
refuted by measurement; one disclosure narrowed; one mis-cut row repaired from the BASE gate;
one records note; one L4), **which is wrong?**

> **ANSWERED 2026-10-16, in the four-seat close adjudication (`regress/artifacts/adj_20261016/m88kexcdeliver/`).**
> Fable 5.1: the cut question is answered by the carrier's own later pins -- "tests" means masks or compares as a case
> (2026-09-25) and a derived input is graded by what the body tests on it (2026-10-09).  `m88k_exception()` tests ONE
> PSR bit, SFRZ, so {site} x {MODE, SFD1, IND, C, SER} is clause-(e) coverage at all four sites: the cut was right about
> the arms and wrong about the re-route, whose PSR-bit cells were graded L2 on passes 7 and 11 under a reads-PSR criterion
> the 09-25 pin does not support.  No row depends on it -- all those cells are rowed -- so it is recorded as one sentence,
> not as an L4.  GPT-6 Astra ("moot for closure, unresolved generally"), Grok 4.7 ("moot as stated") and GLM 5.3 ("moot as
> to rows") disagreed only about whether it needed answering now; pass 14 was asked to attack the sentence (D1).
> The second question is overtaken: opus5 measured the narrowed pass-7 disclosure wrong three ways on pass 8 and v16
> corrected it.  **And the same adjudication found what the chain's denominator had missed**: the delivery path also TESTS
> `cpu->delay_slot`, and `implemented = !cpu->delay_slot` swept the 59-row probe at four arms (measured,
> `regress/artifacts/m88kexcdeliver/delayslot_20261016/`) -- repaired as probe v22 (repair 13), and, when pass 14 found the class wider (Fable 5.1: the {7 labels} x {SFRZ} x
> {delay_slot} grid, 28 cells), as probe v23 (repair 14), which rows all 28 in one diff.

### 2. `lunaabsentcpu` (#503) — passes 1 through 4

**Held for: fable5 (all), opus5 (pass 4 fired, result pending).** Packet:
`regress/artifacts/lunaabsentcpu/brief_lunaabs_p4.md`; tables 1-5 under the same directory.

> **THE QUESTION: pass 4 found a clause-(d) floor breach that pass 3's own repair CREATED —
> the v4→v5 probe rewrite replaced the one session whose alias targets disagree instead of
> adding beside it, and two seats independently predicted the resulting 34/34 sweep, which
> table 5 then measured. That is the `#499` shape (a repair reproducing the defect it repairs)
> arriving inside a detector rather than inside a fix. The pass-4 repair answers it with a
> CLASS closure rather than a cell. Is the class enumerated correctly — every per-cpu array
> the walk touches, under every alias that is a function of `cpu` alone — or is "a function of
> `cpu` alone" itself the next cell someone will find outside?**

Also owed on this row: a ruling on `M_NULLAB`. A both-sided NULL guard measures EQUIVALENT to
the shipped bound on every reachable configuration (34/34, four tables running). It is recorded
as an alternative fix with a warrant that expires if a slot can ever be connected above the
bound or disconnected below it. **Is a measured equivalence with a stated expiry the right
disposition, or does the round owe a choice between the two forms?**

### 3. The retrospective re-check — FIVE adjudications, briefs already written

Each is a complete packet naming the reviewing seat's answer file beside it:

| batch | subject | brief |
|---|---|---|
| 6 | `dev_sgi_re.c` | `_scratchpad/retro_batch6_sgire/brief_fable_adj_batch6.md` (GPT-6 Astra refused this one on its content filter; a Grok substitute answered and is the file to adjudicate) |
| 11a / 11b / 11c | `dev_sh4.c`, `cpu_sh*.c`, `memory_sh.c` | `_scratchpad/retro_batch11{a,b,c}_sh/brief_fable_adj_batch11*.md` |
| 12 | the CPU-core remainder and `float_emul.c` | `_scratchpad/retro_batch12_core/brief_fable_adj_batch12.md` |

Batch 12 raises a candidate PRODUCT defect and it is the one item here that could become a
round: the MIPS `fpu_subst_tiny` path appears to detect tininess AFTER rounding where the R4000
manual specifies before, with `0x1.fffffep-127` through `cvt.s.d` as the discriminating input.
**Is that a real architectural divergence or a misreading of the manual's wording?**

### 4. Stages short of the flagship seat, no held marker, carried here so they are not silent

`sgirekills`, `sgitexindex`, `pcc2widthkills`, `lcabadval` (assess), `proberowsubset`,
`probetimebased`, `ieeeupgrade`, `pitclobber` — each already has its own entry above or in the
ledger; they are listed together here only so that a reader on the 9th sees the whole backlog in
one place rather than reconstructing it from the checker's output.

### 5. Two stages with live HELD markers and real questions — unchanged, still owed

`wdccdbmidxfer` (regress) and `lcabadval` (research). Both carry their `hold_question` in the
ledger; neither was defanged by the marker sweep.

**Nothing in this section may be counted as reviewed.** That is this file's own founding rule and
it is the reason the wall is written down rather than remembered.

### `sgirandompixel` (#504, `257f56f`) — regress stage — **QUEUED 2026-09-07**

Closed at `257f56f`.  `regress` is flagship-only, and the flagship seats are held for the 2026-09-09
adjudication by standing owner directive — so this is owed, not skipped, and written down rather than
remembered.  Section I caught it the moment the row closed.

**What shipped:** `horrible_getputpixel()`'s unimplemented-mode arm no longer does `*color = random()`; it
declines and announces once (`SGIRE_W_BADMODE`).  Witness AND detector is
`regress/sgi_re_randompixel_probe.py`, 8 rows, gate-wired into `gate_arm.sh`; five mutants, all killed; BASE
8/8 opening and closing; the re-pinned oracle measured RED at 7/8 on the committed pre-fix build before the
code changed.

**THE QUESTIONS THIS STAGE IS HELD FOR — three, and none is boilerplate:**

1. **Is the latch-sharing disclosure sufficient, or does it owe a row?**  The contract discloses that a
   latch-sharing mutant scores 8/8 *in isolation*, because nothing in these sessions sets another
   `d->warned` bit first.  But `d->warned` is a shared bitfield — `grep -c 'd->warned |='` on `dev_sgi_re.c`
   finds several setters, most inside `DEVICE_ACCESS`, so **ordinary guest register traffic sets neighbouring
   bits.**  A collision would therefore be silenced by benign traffic, which is exactly the shape `#490` paid
   for.  Is clause-(e) disclosure the right disposition here, or is this a row the round owed?

2. **Is `lin_b diag once`'s channel robust, or accidentally load-bearing on geometry?**  That row's oracle is
   the announcement COUNT, and it can only vary because the probe draws a **1 wide x 4 tall** rectangle —
   height, not width, because LIN_A addressing is `ofs = x & 4095` so four columns would collide on one byte
   and destroy the value oracle.  **The row is therefore coupled to an addressing quirk of the arm under
   test.**  If `sgirelinb` is ever implemented, or LIN_A addressing corrected, does this row silently stop
   discriminating?

3. **Is the five-way residual split right?**  `sgirandomskipput`, `sgirelinb`, `sgirandomcolour` (since raised
   to HIGH — YCRCB is documented and reaches the same `random()` shape), `sgitileptrsilent`,
   `sgirenamedstmode`.  In particular: the round DECLINED to reword the `dst_mode` diagnostic because doing so
   broke the probe's anchor mid-round, and filed it instead.  **Was filing right, or was that an L4 the round
   should have taken with the anchor moved in the same diff?**

---

## 6. RULE QUESTIONS — QUEUED 2026-09-07, ready for the 2026-09-09 reset

**These change how future rounds run, so the carrier caps their wait at about a day — and they have
waited longer, because the flagship seats are held for this adjudication by standing owner directive.
They are written out in full here so the adjudication can begin without reconstructing any of them.**

Each states its question, my position (so the seat has something to attack), and what a ruling costs.
**Where a ruling in my favour is available, please be harder on it than on the alternative** — a
ruling that adopts your author's position is the one he is least likely to test.

### `m88kexcdetectorl2` (HIGH) — is a MEASURED clean sweep an L2 floor breach, or clause-(e) debt?

**The only one of the five that is HIGH, and the only one where a wrong answer changes what ships.**

Deleting `implemented = true` at the DATA_ACCESS arm, or at RESET, scores **59/59 with zero row diffs**
against the shipped `regress/m88k_exc_probe.py`. I measured both, and verified the instrument is sound
by checking it reds on a control. The gap is real and it is not in dispute.

**The question is the GRADE.** The floor says a clause-(d) mutant that sweeps a detector clean is an
**L2 breach, repaired in-round however late**. But these two arms are **pre-existing** — `#502` added
exactly seven arms and these are not among them — so the DEPENDS-ON enumeration, which is closed over
the round's own diff, does not reach them. Under the strict reading they are clause-(e) coverage debt
in code that round never touched; under the broad reading the shipped composite detector has a
measured false pass and owes an in-round repair.

**MY POSITION, and I have already acted on it in the weaker direction:** I first graded it L2, then
downgraded it to a rule question on the diff-closure argument. **I think the downgrade is right and I
am not confident.** The argument that worries me is that the floor asks its question *of the shipped
composite on every pass* — which is `#499`'s own correction — and a composite includes arms the diff
did not add.

**COST OF EACH RULING:** L2 means two rows and a re-table on a closed round. Clause-(e) means a
disclosure sentence in the contract and a filed row. Neither is expensive; the precedent is what
matters, because this shape will recur on every detector that outlives the round that built it.

### `codexbriefscoping` (LOW) — a BRIEF_TEMPLATE change made on measurement rather than by ruling

`BRIEF_TEMPLATE.md` gained a **§C5** telling every codex brief to use ordinary engineering language and
to scope the seat's reading to `src/` and `regress/*.py`. The evidence is a four-run experiment with a
clean control: vocabulary alone converted an immediate refusal into a run that worked for minutes, and
scoping alone carried that run past the exact byte where the unrestricted one was flagged — 279,132 vs
279,268, same distance, opposite outcome. Six clean runs since.

**THE QUESTION:** is scoping the seat AWAY from `regress/artifacts/` and the ledger a review-quality
loss? Those archives hold the kill tables; a seat that cannot read them cannot check a historical
score, and pass-2 briefs sometimes ask exactly that. **The measurement says reading them gets the seat
refused; it does not say the reading was worthless.**

**MY POSITION:** the loss is real and small, and the middle form — scope out by default, inline the
specific artifact when a question depends on it — is right, since §C2 already mandates that machinery
for the packet-fed seats. Reverting is one deletion.

**AND A THIRD TRIGGER LANDED AFTER THAT EXPERIMENT, which strengthens the section and sharpens the
question:** a brief obeying both existing rules was still refused for **chain-shaped content** — a
numbered guest-controlled chain ending in a physical write. **See the entry below; that refusal has
now demonstrably cost a correct answer, which is new evidence this row did not have when it was
filed.**

### `briefforcedwrong` (LOW) — the template's closing question assumes a premise must be wrong

Filed by the codex seat against the template rather than against any code: *"the unsupported assumption
is 'at least one numbered premise must be wrong.'"* All three premises in that brief were correct.

The device earns its place — the carrier records it finding four wrong premises in one brief, and it
has produced real premise corrections since. **The objection is narrower: as worded it instructs the
seat to assume a defect exists, so a seat with sound premises must either invent one or push back on
the instruction.** Pushing back is the right answer and the template does not invite it.

**Proposed wording, held rather than applied:** keep the question, add *"or say NONE and name the
forcing assumption as the defect"*.

### ~~`m88ksfd1row` (LOW) — does the addition licence authorise a zero-delta row that buys attribution?~~ — **RULED 2026-10-16** by four seats: KEEP, not owed — the block after THE ASK

`trapfrozensfd1`'s measured delta against its own mutant is **ZERO** — delete it and the mutant is
still caught by `trapfrozenuser`, at 57/58 [CORRECTED 2026-10-16, GPT-6 Astra: this said "58/58", the score of a
mutant NOT caught; table 15 measured 57/59 with two rows red, so removing one leaves 57/58 -- arithmetic, not a preserved
run]. I claimed the anchor rule one level down: a row varying two
bits cannot say which one fired. **codex rejected that**, citing the carrier — the anchor rule repairs
an oracle comparing a path with *itself*, which this is not, and row demand is bounded *"per enumerated
mutant, never per attribution need"*. Its verdict: close the chain.

**Why the row is still in the tree, and it is the same seat's own next paragraph:** after removal, SFD1
coverage rests entirely on `trapfrozenuser`, whose `PSR_FRZUSER` is SHARED with `errpriv` and
`errunimpl`. Changing that constant from `0x03` to `0x0b` preserves *their* routes while silently
deleting the only SFD1-clear stimulus, and **BASE alone would not notice.**

**THE ASK:** either (a) the licence is right, the row goes, and the shared-constant hazard is handled
some other way — noting that a comment is memory, and this project's finding is that memory does not
fire; or (b) a distinguishing failure signature IS a licensed benefit when the alternative concentrates
an axis on a shared constant, in which case the licence's wording should say so, because it does not.

> **RULED 2026-10-16 (`regress/artifacts/adj_20261016/m88kexcdeliver/`): KEEP, not owed -- all four seats.**  Fable 5.1
> supplied the stronger warrant: the row's delta is NOT zero against every mutant.  The disclosed joint re-route
> `if (!is_trap || ((PSR & MODE) && !(PSR & SFD1)))` reds `trapfrozensfd1` and no other row -- MEASURED 62/63, table
> 16b (`regress/artifacts/m88kexcdeliver/repair13_20261016/ANALYSIS.out`) -- so it holds a third of the trap side's four
> {MODE} x {SFD1} joint cells: coverage, not attribution.  The shared-constant hazard got a STRUCTURAL answer instead of
> a sentence: two import-time asserts on `PSR_FRZUSER` / `PSR_FRZSUP` in the probe (`assert_controls.out`: each of four
> bit edits stops it at startup).  On the wording, 2-2: Grok 4.7 and GLM 5.3 want a sentence in the addition licence
> (Grok's form: a zero-delta row is licensed when it is the only stimulus for an enumerated cell not on a constant shared
> with rows whose oracles do not observe that bit); Fable 5.1 and GPT-6 Astra want none.  No carrier wording was written;
> the ledger line cites the warrant, and the wording is an OWNER rule question.

### *** `sgilinearnegidxpostmortem` — NEW, RAISED 2026-09-07 BY THE FAILURE ITSELF ***

**I filed a HIGH finding, escalated it to a guest-chosen physical write address, wrote it into a commit
message, and reported it as the session's most severe result. It was FALSE.** `tile_nr` is declared
`unsigned int` three lines above the code I quoted, so the `>= 32` guard rejects every negative `x`.
Withdrawn at `a264a34`; `15633bb`'s message is wrong and cannot be edited.

**THE RULE QUESTION, and it is not "be more careful":** I *did* apply this project's discipline. I
identified the link I doubted, verified it by grep, and ran an `offsetof` rather than trust hand
arithmetic about a struct. **Every one of those was aimed at a link I had already decided to question.
The defeating fact was in a declaration I never thought to read, in a range I had printed to my own
screen earlier in the same session.**

1. **Is there a STRUCTURAL form for this, or is it irreducibly judgement?** The carrier's thesis is
   that a rule which lives in prose does not fire. The candidate rule — *"a chain resting on an index
   or a bound quotes the DECLARATION of every variable in it"* — is cheap, mechanical, and would have
   caught this in one line. Is it worth the template line, or is it one instance wearing the clothes
   of a class?
2. **Does the premise-audit instruction need a self-directed twin?** It tells *seats* not to ratify my
   premises. Nothing tells *me* to enumerate which premises I never questioned — and that set is
   exactly where this lived. **A premise you did not notice you were making is not audited by an
   instruction aimed at your reader.**
3. **What does this say about §C5?** The refusal is no longer a cost paid in inconvenience. The
   chain-shaped brief asking for this exact chain to be attacked was REFUSED; the same seat, asked the
   same subject without the chain, put the refutation in its verdict line. **The refusal did not stop a
   bad question — it delayed a correct answer by hours, during which I escalated a false finding.**
   Does that change the disposition of `codexbriefscoping` above, and does it warrant splitting every
   chain into link questions BY DEFAULT rather than as a fallback?

**MY POSITION:** (1) yes, and narrowly — restricted to chains whose conclusion is a bound or an index,
which is a small and recognisable population. (2) yes, and it is the more valuable of the two. (3) it
strengthens the case for the middle form rather than for reverting §C5, but I hold that weakly, and it
is the question I would most like answered by someone who is not me.

### `codexrefusalclass` — RAISED 2026-09-07: is a REFUSAL a seat failure, and how is it recorded?

**This is a PANEL-MECHANICS question, deliberately separate from `codexbriefscoping` above.** That row
asks whether §C5's scoping is right. This one asks what the harness should *do* when a seat refuses,
and the answer changes every future round's record regardless of how §C5 is settled.

**THE FACTS, from five refusals on 2026-09-07.** Four distinct triggers have been found, each by
losing a run to it:

| trigger | level | how it presents |
|---|---|---|
| vocabulary (`kills`, `host dies`) | prompt | immediate refusal, tiny `.err` |
| reading `regress/artifacts/` or the ledger | content | refusal after minutes of work |
| chain-shaped content (a numbered guest-controlled sequence) | prompt | immediate, ~8 KB `.err` |
| **the defect CLASS itself** (information disclosure) | content | **refusal after 43,839 tokens** |

*** THE RECORDING PROBLEM: A REFUSAL LEAVES A ZERO-BYTE ANSWER FILE BESIDE A LARGE `.err`. THAT IS
BYTE-FOR-BYTE THE agy QUOTA-WALL SIGNATURE. *** The carrier already warns that a zero-byte agy log is
the normal mid-run state and that the discriminator is the `.err` — but a refusal and a wall both put
text there, and nothing distinguishes them by shape. `panel.sh`'s seat check does not classify
refusals at all; `seat_verdicts.py` gained a SEAT REFUSED label only for the echo shape, which this
is not.

**THE QUESTIONS:**

1. **Is a refusal a SEAT FAILURE?** It is not a wall (no quota is exhausted), not a burn (no thinking
   budget spent — well, 43k tokens *were* spent), not a stall, and not a considered non-answer. The
   seat ledger's rule is that a seat which did not answer is a failure and never agreement. **Does a
   refusal inherit that, or is it a sixth class needing its own disposition?**
2. **Should `seat_verdicts.py` and `panel.sh` learn the signature?** The content-level form is
   detectable — the `.err` tail carries a fixed provider string. The cost is one grep; the risk is
   the check-that-cannot-fail family if the string ever changes silently.
3. **IS THE ROUTING CLAUSE THE STANDING ANSWER?** Measured twice today: codex refused a witness-design
   brief and an information-disclosure brief; **grok answered both in full**, found a defect in my
   witness design and corrected three premises in the other. **One extra invocation, nothing lost.**
   Should §C5 gain *"witness designs and disclosure-class defects go to grok and the packet-fed seats;
   codex takes the reading questions"* — or does that quietly halve the roster's strongest seat on a
   class this fork's queue is full of (`#91`/`#93`/`#94`/`#95`, `sgirebufuninit`, `sgirandomcolour`,
   `sgimtedepth4dead`)?

**MY POSITION, weakly held:** (1) yes, a sixth class — it is an OPERATIONAL failure like a wall, and
must never read as agreement; (2) yes, but as a *report* rather than a gate, since the string is
outside our control; (3) the routing clause is right as a DEFAULT and wrong as a rule — the reworded
experiment (`PASS1_brief_reworded.md`) is meant to find out whether the framing or the subject is what
trips it, and that answer should decide this rather than my preference.

**AND A DISCLOSURE ABOUT THE REWORDING, because it is the part I am least comfortable with:** the
reworded brief keeps every technical premise and removes the sentence describing what the defect
*means*. That is honest — the design question does not depend on the consequence — but it is one step
from writing briefs that describe defects in words chosen to pass a filter rather than words chosen
to be true. **The adjudication should say where that line is**, because I will otherwise be drawing
it myself, repeatedly, under time pressure.


---

## 7. ADDED 2026-09-07 (afternoon) — CLOSURE RATIFICATIONS and four new rule questions

### 7a. TWO CLOSURES PROPOSED, NOT MADE — please ratify or refuse

Both were found by a codex rating pass and then **verified by me against the source**. I did not close
them, because closing on one seat's reading plus my own agreement is precisely the self-review the
conflict-of-interest badge exists to disclose. Badge: `A` (author self-review disclosed).

* **`pitclobber`** — `dev_8253.c:303-308` handles `I8253_TIMER_LATCH` with a `break;` *before* `:310
  d->mode_byte = idata;`, so a latch command can no longer reach the reprogramming store. **The row's
  own `witness` field already said so**: *"none needed -- the defect was fixed by `#439` (`020a672`),
  which also shipped `regress/pit8253_latch_probe.py` as its detector."* Carrying row:
  `R1 latch preserves programming`.
* **`asiceventaddr`** — `dreamcast_sysasicvar.h:140` is
  `(SYSASIC_BASE + 4*((e)>>5) + SYSASIC_EVENT_RANGE_OK(e))`, so the domain guard is *inside* the
  macro and an out-of-domain event cannot produce an address. Added by `#467`/`#468` (`29b450c`). The
  row's existing witness text is stale — it still gives the *pre-fix* warrant ("the highest defined
  event is 67 < 96").

**`wdcflood` is deliberately NOT proposed** although the same pass called it fixed and I verified the
latch at `dev_wdc.c:1065`: the row is `in work` with its own commit, and an `in work` row may carry an
obligation a source reading cannot see. **That judgement is the one I want checked**, in both
directions — am I being too cautious there, or not cautious enough on the other two?

### 7b. THE CLASS BEHIND THEM, and the question it raises

**Five already-fixed-and-still-open rows surfaced today** (`lunaabsentcpu`, `wdcflood`, `pitclobber`,
`asiceventaddr`, and a `dev_pvr.c` site grok found de-fatalised by `#166`). I derived a mechanical
signal — **a row carrying a `commits` value that is still open** — which returns 14 rows and contains
3 of the 4 known instances. A codex pass on the other 11 is in flight.

> **THE QUESTION: should closing be part of a round's own gate?** A round that fixes a defect and does
> not close its row leaves a queue that overstates the work outstanding — and this queue is the thing
> the standing directive asks me to prioritise from. But a mechanical auto-close is the
> check-that-cannot-fail family: a row can be fixed *and* still owe a detector.

### 7c. NEW RULE QUESTION — the two-deriver practice

**Four censuses of mine today each keyed on ONE spelling and missed a variant:** `severity` (the field
is `sev`) → 0 of 260 matched; `witness != 'none'` (the convention is `none -- <why>`) → 37 of 73
miscounted; `<< 24` (a `uint16_t << 16` is the same UB) → the structural site missed entirely;
`(int)idata` (the tree also writes `(int) idata`) → 226 where the answer is 309. **Every one was
caught by someone else's derivation, never by re-reading mine.**

The carrier already says *when two derivers DISAGREE neither is trustworthy until you look at what
each matched*, and `sgirekills` added *when two AGREE that is not evidence either, if they can fail
the same way*. **The proposal: a census written into a durable record runs TWO derivations with
different keys and PRINTS BOTH.** Cheap, and disagreement is a free signal available before any seat
reads the work. **Is that a rule, or is it the counts rule's stop condition being widened past what
the evidence supports?** The honest severity is the same as the counts rule's: *no stale census has
yet changed a decision* — though `lcaconfwidth`'s 226-vs-309 came within one brief of doing so.

### 7d. NEW RULE QUESTION — where does an apparatus control belong?

Three separate row-classes were built today whose entire purpose is to separate **"measured nothing"**
from **"measured a zero"**, independently and within hours of each other:

    UBSan in-band control   a known-UB binary must REPORT before a silent emulator run is read
    kill-table NUL check    a log with NUL bytes means concurrent writers; the score is VOID
    `swpctx mapped`         a 0 readback means the memory was never there -- a SETUP failure

**Each was added only after the corresponding failure nearly landed a false negative** — and one of
them (UBSan take 1) *did* produce a clean-looking `0` that I was one step from recording. **Should the
witness ladder's control clause (ii) be widened from LIVENESS + DEVICE-SIGNATURE to include an
explicit APPARATUS control** — *this instrument would have spoken if the thing were true* — or does
that duplicate what liveness already means? I think it is genuinely different: liveness proves the
path works, and this proves the OBSERVER works.

### 7e. REFUSAL #7 REFINES QUESTION 3 ABOVE

The `lcaconfwidth` census brief was refused after **108,432 tokens of completed work**. Its shape:
*"say whether a 64-bit value exists that trips the guard and prints as something the guard would
accept — give the discriminating value."* That is a printf-format-correctness question. **The trigger
is the SHAPE — find the input that defeats the check — not the subject**, which strengthens the
"chain-shaped content" reading already recorded and weakens "it is about the framing of consequences".

**grok answered it in full and corrected my census in both directions.** Routing worked for the fourth
time. The question in §6.3 stands and now has a fourth data point.


### 7f. THREE RUNG-3 WITNESSES BUILT AND RUN ON 2026-09-07 — two for HIGH rows that had none

All three show the symptom on the **committed** build, which is what clause (i) asks for, and all
three carry a control that separates *measured the thing* from *measured nothing*.

| row | probe | HEAD | the defect row |
|---|---|---|---|
| `alphaswpctxptbr` (high) | `regress/alpha_harness_probe.py` | **7/9** | `PCB_A+16` reads `0xbbbb2222` (A.flags) where `0xaaaa1111` (A.ptbr) is required |
| `lcaconfwidth` (med) | `regress/lca_confwidth_probe.py` | **4/6** | the IOC_CONF kill message reads `0x0` — a value that guard **accepts** |
| `alphapfnoffset` (high) | `regress/alpha_pfnoffset_probe.py` | **5/6** | a cold guest `ldq` of `vaddr+8` returns the `data+0` value |

**The question for the adjudication is not whether these are correct — it is what they cost.** Each
took one design pass from a reading seat plus one build, and **each design pass killed at least one
trap that would have produced a GREEN run on the defective build**:

* the Alpha harness's first draft planted every structure **past the end of RAM**, where writes are
  discarded and reads return zeros — three rows would have gone green measuring nothing;
* the LCA probe's read-back would have used debugger `dump`, which skips a `DM_DEFAULT` handler and
  returns the pre-zeroed buffer — *the unmapped signature produced by a hit*;
* the PFN probe would have planted its oracle value **through the walk under test**, so HEAD would
  have measured the defect against itself and gone green.

> **NONE OF THE THREE IS THE KIND OF ERROR A SECOND PAIR OF EYES ON THE *CODE* WOULD CATCH.** Each is
> a property of the APPARATUS, invisible in the probe's own text, and each was found by a seat asked
> specifically *what would make this go green while measuring nothing*. **Is that question worth
> adding to the brief template as a standing item for any witness design?**

**And one I got wrong twice, which is the reason to ask:** the first `lca_confwidth_probe.py` scored
**6/6 on the committed build** because it asserted the DEFECT as the passing state. It reads as
success and would have gone red the moment the bug was fixed. The sibling `alpha_harness_probe.py`
had the polarity right (7/9) **in the same tree on the same day**. The cheap tell is *"what does this
row do after the fix?"* — if the answer is "goes red", the polarity is inverted whatever the score
says. **Should that be a checkable rule rather than a habit?** A witness whose score is
`len(rows)` on HEAD is suspicious by construction, and that is mechanical.


## 7g. ADDED 2026-09-07 (evening) — `#509` sgimtedepth4dead: FOUR RULE QUESTIONS, one of them a
## live SEAT DISAGREEMENT I resolved by adopting one side, which is exactly the shape that owes
## an adjudication rather than an author's ruling

Round context, so the questions stand on their own: `dev_sgi_re.c` `do_mte_transfer()` had
`if (depth == 4)` where `depth` is a count of BITS (`8 <<` a two-bit field, so 8/16/32/64), and 4
is the corresponding BYTE count. The branch was unreachable, so every tiled MTE transfer took the
CI colour arm — which at 32bpp assigns `buf[0]` alone while `memory_rw` copies four, publishing
three bytes of host stack into guest memory. Fix: `depth == 32`. Six seats answered pass 1; all
six confirmed the enumeration and **three of them found errors in my brief**.

---

### `sgimtedepth4dead` -- the row these six questions belong to

*Section I of the pre-commit gate caught that 7g named its questions and never named its ROW:
"HELD but NOT NAMED IN THE QUEUE -- a promise nobody recorded". Holding a stage and queueing it
are ONE action. Both its `assess` and `review` stages stand at 7/9 awaiting opus5 and fable5.*

### 7g-1. (HIGH) *** A SEAT DISAGREEMENT ON SIBLING PARITY THAT I SETTLED BY READING, AND WHICH
### GENERALISES TO EVERY MULTI-LABEL SWITCH BLOCK IN THIS TREE. ***

> **RULED 2026-09-09 (Fable 5.1 adjudicating, on codex + grok self-adjudications and an Opus MEASUREMENT): the labels ARE floor cells here -- the selector flows into `dst_mode`, the operand the repair reads -- so `#509` owes two rows (B x 32, C x 32) as L2 in a follow-up commit; `&& dst_tlb == MTE_TLB_A` MEASURED 14/14 with the defect live at B/C (`regress/artifacts/sgimtedepth4dead/killtable3_20260909/`).  The bound that keeps it finite is DATA FLOW, written into the SIBLING PARITY row in CLAUDE.md.  Two premises of the adjudication brief were wrong and are recorded on the ledger row: `fill b top` never shipped; `dispatch axes as full axes` was a gloss.  Carried by `sgimtelabelcells` (med) and `multilabelfloor` (low).**

The edited comparison sits inside a block served by THREE `case` labels:

    switch (dst_tlb) {
    case MTE_TLB_A:
    case MTE_TLB_B:
    case MTE_TLB_C:
            { ... if (depth == 32) { src_mode |= RGBA; dst_mode |= RGBA; } ... }

The PRE-TABLE CHECK's SIBLING PARITY row says that at a block serving several labels, **the
siblings are the LABELS**. So do B and C owe rows?

* **codex (GPT-6 Astra, max):** enumerated the admitted pairs (`AA AB AC BA BB BC CA CB CC` ×
  `fill/copy` × four depths = 72 field combinations) and concluded *"`fill b top` covers B but
  leaves C uncovered ... the proposed rows are not exhaustive."*
* **grok (4.6, xhigh):** *"A/B/C share one block; the helper distinguishes TLB arrays.
  `fill b top` is sibling parity on PACKING, not a floor cell of the comparison. Cheap, not
  required."*

**I ADOPTED GROK** and DISCLOSED the cell in `PRETABLE.out`: a repair conditioned on
`dst_tlb == MTE_TLB_A` escapes this detector. My reasoning was that the repaired comparison does
not read `dst_tlb` at all, so a per-label row would pin the helper's ARRAY SELECTION — a
different property, already the subject of other rows in this tree.

> **THE QUESTION, stated generally because that is where it bites: when an edited expression sits
> in a block reached by several case labels but does NOT READ THE SELECTOR, are the labels FLOOR
> CELLS (rows owed) or DISCLOSED DEBT?**
>
> The floor's own wording — *the cross-product of the guard's dominating predicates with the
> device-STATE lvalues the fix's repair path reads* — arguably answers YES, because the switch IS
> a dominating dispatch and the pass-10 ruling says *dispatch axes are full axes*. My reading
> narrows that with "…that the repair path READS", and I am not confident the narrowing is
> licensed.

**Why it matters beyond this round:** this tree is full of multi-label device blocks. If codex is
right, a large number of shipped detectors are short by (labels − 1) rows apiece, and that is a
class finding, not a round finding. If grok is right, the narrowing should be written into the
SIBLING PARITY row so nobody re-argues it.

*I note against my own position that I adopted the reading which costs less work, and that the
seat I overruled is the one that actually enumerated the space.*

> #### *** PASS 2 SHARPENED THIS INTO A TENSION INSIDE grok's OWN TWO ANSWERS, AND IT LEANS
> #### AGAINST THE READING I ADOPTED.  Noticed while writing 7g-6; stated as a question, not a
> #### ruling, because it is my analysis of a seat rather than a seat's own words. ***
>
> In pass 2 grok reclassified `M4` from clause (d) to clause (e), and its reason is exact:
> **DEPENDS-ON takes (1) the predicates DOMINATING the edited line, plus (2) for operand-swap
> forms, lvalues the GUARDED BODY reads.**  `mode & MTE_MODE_COPY` is tested LATER, inside the
> transfer loop, so it dominates nothing, and the guarded body -- exactly the two `|=` statements
> -- never reads it.  Both clauses fail; clause (e).  **I verified that by reading and adopted it.**
>
> **But grok gave the SAME reason for B/C** -- *"the type OR does not read `dst_tlb`"* -- and
> there the two clauses come apart:
>
>     mode & MTE_MODE_COPY   dominates? NO   body reads it? NO    -> clause (e).  Agreed.
>     switch (dst_tlb)       dominates? YES  body reads it? NO    -> clause (1) ALREADY APPLIES
>
> **The `switch (dst_tlb)` is the dispatch that reaches the edited line at all.**  If clause (1)
> is what it says, the three labels are dominating predicates and the cross-product with the
> repair's written lvalues is FLOOR -- which is codex's position, reached by grok's own rule.
>
> So grok may be applying clause (2) uniformly in a place where clause (1) already answers.  It is
> right about `M4` either way; the B/C half is where the two clauses disagree and it did not
> separate them.
>
> **WHAT TURNS ON IT, concretely:** `if (depth == 32 && dst_tlb == MTE_TLB_A)` escapes this
> detector -- every row drives TLB_A.  **That mutant is buildable in one run.**  If the labels are
> floor cells it is an L2 breach and `#509` owes two more rows; if they are clause-(e) debt the
> disclosure already standing in `PRETABLE.out` is sufficient.  **I have deliberately NOT built it,
> because building it would not settle the rule -- it would only tell me the score I already
> predict.**  The rule is the question.

---

### 7g-2. (MED) MAY A DETECTOR ROW BE **GATED** ON ANOTHER ROW'S OUTCOME?

> *** SUPERSEDED BY 7g-6.  DO NOT ANSWER THIS ONE. ***  It was written from pass 1 with no
> evidence behind it, and two of its statements are now known false: it recorded "no
> precedent found in this tree" (there is one -- `pcc2_default_probe.py` gates on session
> survival), and it described the gate as per-row when it is a single shared flag.  7g-6
> carries the same question with the pass-2 measurements, the three-way seat split, and the
> two measured limits.  Kept below only as the record of what was asked before the evidence
> existed.

Two rows in the shipped detector — `fill bot` and `copy 2nd`, plus `copy 4th` — read bytes that
are HOST STACK before the fix and DEFINED after it. Asserting them pre-fix would score a
nondeterministic byte. So they are gated:

    rgba_ran = (got == "0x11")                      # the leading byte proves the RGBA arm ran
    row("fill bot", byte_n(fullword, 3) if rgba_ran else "n/a: dest[0] not RGBA", "0x44", ...)

Pre-fix the row reports `n/a: dest[0] not RGBA` and **FAILS deterministically, naming its own
reason**. Post-fix it reports `0x44` and passes. Under an RGB-for-RGBA substitution it reports
`0x00` and fails.

> **Is a gated row legitimate, or does it violate the spirit of the witness clauses?** Two
> readings, and I can argue both:
>
> * **FOR:** the alternative is asserting a byte whose value is undefined, which is worse. The
>   gate makes the row deterministic in all three states, which is exactly what the rows this
>   project keeps having to repair were missing.
> * **AGAINST:** the row's pre-fix red is not "red for the reason under test" — it is red because
>   a DIFFERENT row failed. A cascade of gated rows could make one real failure look like several.

**Precedent I could not find:** I looked for an existing gated row in this tree and found none, so
this is a new form and it is shipping in `#509` unless refused. *If it is refused, the fallback is
to drop the three rows and accept that RGB-for-RGBA is undetectable — which three seats
independently flagged as the round's most dangerous escape.*

---

### 7g-3. (MED) IS A **CODE-INTENT WARRANT** ENOUGH TO CHANGE GUEST-VISIBLE OUTPUT?

Raised by the minimax seat and confirmed by me: **there is no SGI/CRIME hardware documentation in
this project.** Derived, not assumed — `ls _scratchpad/*.pdf` lists sixteen manuals (ARM, MIPS,
m88k, SH, PowerPC, DC21285, i8254, MVME187) and **none for this device**.

So the fix picks `DE_MODE_TYPE_RGBA` on two internal warrants only: the dead branch itself named
RGBA, and the comment says *"copy 32 bits"* while the RGB arm zero-pads the low byte and therefore
does not copy 32 bits of data. minimax put the gap precisely: *"no CRIME/MTE hardware spec is
cited. A regression that picked RGB instead would still pass the witness."* (That specific escape
is now closed by `fill bot`/`copy 4th` — but the WARRANT question survives the closure.)

> **Is "the dead code's own choice, plus a comment" a sufficient warrant for a round that changes
> what a guest reads back?** This round says yes and discloses the basis. The alternative
> disposition would be to fix the UNREACHABILITY (make the branch live) while filing the TYPE
> choice separately — which nobody proposed and which I do not think is better, but I have not
> tested that opinion against a seat.

---

### 7g-4. (LOW) SCOPE — one round for the class, or one per cell?  **5–1, and please ratify.**

The same defect class (the CI arm assigns one byte while the transfer copies `bufdepth`) hits
depth 16 (one byte leaks), depth 32 (three) and encoding 3 (seven). `#509` fixes ONLY the 32 cell,
by a different mechanism (selecting RGBA, which assigns four).

* **codex, grok, glm, kimi-substitute:** ONE round for the remaining class
  (`sgirebufuninit`), across all widths. codex: *"Handle the shared initialization invariant
  across widths together in a companion repair, rather than scheduling one initialization fix per
  depth."*
* **deepseek:** *"One round per cell is defensible, provided the siblings are filed and tracked."*
* **minimax:** siblings, but *"a tracking issue at the class level is warranted so the three rounds
  don't drift."*

I went with the majority, because a per-depth chain is the `#499` same-class-three-times shape the
repair-chain rule exists to end.

> **AND THE TRAP THAT MAKES THIS MORE THAN BOOKKEEPING**, named by grok and now recorded in the
> CHANGELOG and `PRETABLE.out` verbatim: **`#509` fills `buf[0..3]` at depth 32, so it
> ACCIDENTALLY MASKS the 32-bit tiled cell of the uninitialised-buffer sibling.** A later round
> that rows only depth 32 on this path **will look fixed and will not be.** The sibling must be
> kept alive on depth 16.

---

### 7g-5. FOR THE RECORD, NOT A QUESTION — what the premise-audit opener bought this round

Three errors in my own brief, each found by a seat, none by me:

1. **A wrong count, caught INDEPENDENTLY by two seats** (kimi-substitute and codex). I wrote that
   `depth >= 32` "converts a four-byte problem into a four-byte problem". At encoding 3, CI leaves
   **seven** bytes uninitialised and RGBA would leave **four** — a reduction, not a neutral swap.
   The conclusion held; the arithmetic under it did not.
2. **A wrong record in the probe header** (codex): it said "only the top byte is read". The probe
   executes `lw` and masks afterwards — it **reads four bytes and asserts one**.
3. **An imprecise mechanism** (kimi-substitute): my `copy top` byte-walk gave the right answer for
   the wrong reason, and the seat asked for one sentence in the row's comment so a future reader
   would not "correct" the want.

And **two escapes in my row set** that three seats found between them (RGB-for-RGBA invisible to
`dest[0]`; `depth >= 16` reding nothing), plus **a third the PRE-TABLE CHECK found on its own** —
a source-side RGB substitution escaping all twelve rows. All three closed before table 1 ran.


### 7g-6. (MED) *** THE GATED-ROW FORM, AFTER PASS 2: THREE SEATS SPLIT, AND THE ONLY IN-TREE
### PRECEDENT TURNS OUT TO GATE ON SOMETHING ELSE. ***

7g-2 asked this from pass 1 with no evidence behind it. Pass 2 supplied the evidence and the
split, so it is restated here with both, and 7g-2 should be read as superseded by this.

**THE FORM.** Three rows in `#509`'s detector -- `fill bot`, `copy 2nd`, `copy 4th` -- read bytes
that are HOST STACK before the fix and DEFINED after it. Each is gated:

    fill_top_ok = (fill session's dest[0] == 0x11)
    row("fill bot", byte_n(fullword, 3) if fill_top_ok else "n/a: ...", "0x44", ...)

Pre-fix the row reports `n/a` and **FAILS deterministically, naming its reason**, instead of
scoring an undefined byte. The alternative is to drop all three -- which measurably re-opens two
total escapes (`dst_mode |= RGB` and `src_mode |= RGB`, M5 and M8, both 11/13 and 12/13 only
because these rows exist).

**THE SPLIT, and it is not a tally -- the arguments differ in kind:**

* **grok: SHIP `fill bot`, KEEP `copy 4th`, and write the coupling on the row.** Its reason is
  precise: `fill bot` gates on **the same `lw` it then scores**, so its coupling is local. The
  copy rows gate on a **different session**, which is a weaker thing, and it says so rather than
  lumping them together. *"Fail-when-closed is a derived red, and that is acceptable HERE because
  the n/a names the reason and the row's job is the RGB cell, not the pre-fix leak."*
* **codex: KEEP all three, with truthful dependency diagnostics.** *"Their pre-fix failures need
  not be independent defect witnesses to make useful post-fix assertions. A failed prerequisite
  should still prevent an overall pass."* It adds that the gate must be renamed `fill_top_ok`,
  because `dest[0] == 0x11` **admits RGB as well as RGBA** -- so the current name overclaims.
* **deepseek: NOT RATIFY -- fix the gate per-path or drop the rows.** *** ITS REMEDY IS REJECTED
  ON MEASUREMENT, NOT ON A VOTE: *** it proposes gating the copy rows on `copy dest[0] == 0x1a`.
  grok's byte-walk shows that is VACUOUS -- `0x1a` is what **both** CI-CI and RGBA-RGBA produce,
  so the gate would always be open, including pre-fix, and the rows would then score exactly the
  host stack the gate exists to avoid. *A proposed edit is a sketch until it is run against the
  real control flow.*

**WHAT I DID:** shipped all three, renamed the flag, corrected the message to name the FILL, and
wrote both measured limits into the probe. **The disposition is mine and it is the one that costs
least work, which is why it wants an adjudication.**

> #### THE PRECEDENT QUESTION, and pass 2 changed the answer to it
>
> Pass 1 recorded "no precedent found in this tree". **That was wrong in a way that cuts both
> ways.** `pcc2_default_probe.py:174-178` DOES use the `n/a`-and-fail shape --
> `t.count(MSG) if alive else "n/a"` -- so a row that refuses to score and names its reason is
> already house style. **But it gates on SURVIVAL of its own session.** codex and grok both drew
> the line in the same place: that establishes the *n/a idiom*, and it does **not** establish a
> **cross-session dependency**, which is what `copy 2nd` and `copy 4th` actually do.
>
> So the genuinely new thing is narrower than pass 1 thought and still real.

**THE TWO MEASURED LIMITS, both from grok, both now written into the probe rather than glossed:**

1. **Under a `&& (mode & MTE_MODE_COPY)` mutant the copy rows are a WRONG-REASON KILL.** The copy
   path there really does take RGBA -- `dest[3]` would be `0x4d` and would PASS -- but the FILL is
   CI, so the gate closes and both rows red anyway. **Their own bytes do not move.** The mutant is
   still killed by `fill top`, so nothing escapes; but the CHANNEL those rows report under it is
   vacuous, and the pre-table CHANNEL check is exactly what should have caught that.
2. **The dual, `if (depth == 32 && !(mode & MTE_MODE_COPY))`, is NOT PINNED AND CANNOT BE.** Every
   fill row stays green; `copy top` stays green because `dest[0]` of a same-type copy is invariant;
   and the gate OPENS, so the two tail rows would score bytes a CI-CI PUT never wrote. **There is
   no copy-local four-byte signal that is not those bytes themselves.** Disclosed as clause-(e)
   debt.

> **THE QUESTION IN ONE LINE: is a row that fails because ANOTHER SESSION'S row failed a
> legitimate detector row, or is it a cascade that makes one defect look like three?**
>
> And the sharper sub-question, which limit 1 makes concrete: **a gated row can red under a mutant
> whose own observable did not move.** That is a false kill in the strict sense, even though the
> mutant is caught by a different row. Does the vacuity floor care?

*If the form is refused, the fallback is to drop the three rows and accept that RGB-for-RGBA is
undetectable at this site -- which three seats independently called this round's most dangerous
escape. That is the cost, stated so the ruling can weigh it.*


## 7h. ADDED 2026-09-07 (late) — `#510` armbfxwidth32: THREE QUESTIONS, one of them about whether
## a round may ship a KNOWN-UNKILLABLE escape

### `armbfxwidth32` -- the row these questions belong to

Both stages stand at **7/9 awaiting opus5 and fable5**. `#510` fixed three sites in
`cpu_arm_instr.c` where `(1 << width) - 1` was undefined at width 32 (and at 31), with a rung-3
witness measured **9/11 pre-fix, 12/12 post-fix**.

---

### 7h-1. (HIGH) *** MAY A ROUND SHIP AN ESCAPE IT KNOWS IT CANNOT KILL, WHEN THE VEHICLE THAT
### COULD KILL IT ALREADY EXISTS IN THE TREE? ***

Pass 2 (grok) found two one-line regressions that re-open real undefined behaviour and score
**full marks** on the 12-row witness:

    `1U' -> `1' in the mask ternary                     re-opens C99 6.5.7p4 at width 31
    restore `topBitMask = 1 << (width-1)' above the if  re-opens the second UB

**Neither is killable by any row, and the reason is structural rather than a thin row set.** Both
are DEFINEDNESS repairs, and definedness has no guest-visible value on a non-trapping host:
`1 << 31` and `1U << 31` yield the same mask after the `- 1`, and with a correct 32-bit mask
`x |= ~mask` is `x |= 0`. *This also means `s w32` pins the MASK and not `topBitMask` — the probe
comment claimed otherwise and is corrected.*

> **BUT THE TREE ALREADY HAS THE VEHICLE.** `build-asan` carries `-fsanitize=address,undefined`,
> and `regress/gate_asan_sweep.sh` exists. A UBSAN DIFFERENTIAL pins both — fixed source produces
> no shift diagnostic, the `1U`->`1` mutant produces one — and it would cover the whole class:
> `lcashiftub`, `sgirebufshiftub`, `m88k_rot:513`, `cpu_mips_instr.c:1757` and the two
> `is_userpage` sites. **Eight sites across three CPUs, none visible to a value oracle.**

**I DID NOT BUILD IT, and the reason is the question.** It is a NEW MEASUREMENT LANE — a second
binary and a STDERR oracle instead of a value oracle — and this round's pass 2 had already run.
**A lane added after a pass is a lane nobody reviewed.** So I shipped with the escape disclosed in
the probe header and filed the lane as `ubsanshiftlane`.

> **The question, stated so it generalises past this round: when a floor-relevant escape is
> unkillable by the round's instrument BUT killable by a lane the tree already has, is disclosing
> it sufficient, or does the round owe the lane in-round?**
>
> The pull is real in both directions. *Owing it in-round* means every round that touches UB
> acquires a second measurement lane and a second pass — which is the `#392` shape. *Disclosing*
> means a clause-(d) escape ships with a full score beside it, and this project's own vacuity
> floor exists because a full score beside a live escape is exactly what it refuses.
>
> **My disposition was DISCLOSE, and it is the one that costs less work, which is why it wants
> adjudication rather than my say-so.**

---

### 7h-2. (MED) IS LEAVING `bfi` A CORRECT ONE-SITE SCOPING, OR A PARTIAL REPAIR? — kimi's challenge

`#510` fixed `ubfx` and `sbfx` and **left `bfi` alone**, on the ground that its
`width = msb - lsb + 1` spans **-30..32** (465 pairs strictly negative, 31 giving width 0) and
that ARM calls `msb < lsb` UNPREDICTABLE, with the fork answering that class inconsistently.

**The kimi substitute refused that rationale as too broad, and it is right:** `bfi`'s
**`msb = 31, lsb = 0` cell is architecturally DEFINED**, gives width 32, and is **the same
`(1 << 32) - 1` defect this round just fixed twice** — the same ternary would fix it. So the
UNPREDICTABLE argument covers `msb < lsb` and does **not** cover bfi's width-32 cell.

grok, independently, called leaving bfi *"a correct use of the one-site rule, not a partial repair
sold as complete"* — while agreeing the legal cell is the same defect.

> **So: does the one-site rule permit leaving a KNOWN, DEFINED, IDENTICAL-EXPRESSION cell unfixed
> because its NEIGHBOURING cells raise a design question?** Or does "same defect, same file, same
> one-token fix" oblige the round to take it, and confine the scoping argument to the
> UNPREDICTABLE half?
>
> *Note the witness does not cover bfi either way — there is no bfi row — so taking it would also
> have owed a row.*

---

### 7h-3. (MED) WHAT SHOULD `bfi` DO WHEN `msb < lsb`?  *(the row's `hold_question`)*

496 encodings reach it. ARM says UNPREDICTABLE. **No seat could settle it from the tree**, and a
codex pass examined 13 comparable decisions to say so: no-op has bitfield precedent, conditional
UND has decoder precedent, `cpu_arm_instr_loadstore.c:204` picks another defined result for an
UNPREDICTABLE halfword load, and **`#312`'s own comment argues AGAINST halting**.

*** AND THE OBVIOUS ROUTE IS WRONG AS WRITTEN: `X(und)` expects `arg[0]` to hold a PC OFFSET, and
`bfi`'s `arg[0]` is a REGISTER POINTER. *** Routing bfi's unchanged call record there would hand a
pointer to code that reads an offset.


---

## 7i. `lcabadval` — THE ROUND REVERSED THREE TIMES AND ITS CENTRAL PREMISE DIED TO ONE GREP

*Design stage: `regress/artifacts/lcabadval/panel_p1_20260907/` — six seats (codex, grok, glm,
deepseek, minimax, the kimi-k3:cloud substitute). The kimi CLI walled on a 403 weekly limit, so that
seat is covered. agy deliberately not fired (measurement reserve). **No flagship seat, by the
standing directive reserving opus5 and fable5 for this adjudication.** No product code is committed.*

**THE FORK AS PUT TO THE PANEL:**

    A  delete fatal()+exit(1) from all six arms, KEEP the store that already ran
    B  DECLINE — move the store BELOW the guard, as #447 did for SH4's RCR1

**WHAT THE PANEL DID TO IT.** Four of five landed seats said the fork was **mis-posed**: one
disposition for six arms is the wrong question, because `LCA_IOC_CONF` is the only field with a
consumer (`bus = d->ioc_conf & 1`) and the other five are pure storage. The kimi substitute named
the self-inflicted part — the brief **quoted `#447`'s own "check it per site" as a settled premise
and then asked for one answer across six arms.**

*** THEN codex LANDED LAST AND KILLED THE PREMISE UNDER BOTH SIDES. ***

My premise 6 was that LCA differs from RCR1 because RCR1's stored value "has a meaning the model
honours". **Verified in one grep:** `rtc_rcr1` has four occurrences — declaration, readback, store,
and one *inside the comment*. **Zero functional consumers.** `ioc_conf` also has four, but its
fourth is a real consumer. **So RCR1 is consumed LESS than LCA's CONF, not more.**

That also falsifies grok's formulation, which I had recorded as the keeper: *"B copies RCR1's edit
without RCR1's reason"* — the reason it names (consumed feature bits) does not exist.

### 7i-1. (HIGH) DOES `#447`'s PRECEDENT NOW SUPPORT **B**?  *(the row's `hold_question`)*

`#447` faced a store-before-guard field with **no functional consumer** and chose to move the store
below the guard. That is the LCA shape, arm for arm. codex, deepseek and glm all reached B; grok and
minimax reached A, **and both A positions rest on the consumed/unconsumed distinction that is now
measured false.**

*Count the arguments, not the seats: the load-bearing premise under A has been refuted by a grep.*

### 7i-2. (HIGH) IS **B** EVEN WELL-DEFINED AT RESET?

codex: `W_MASK0`, `W_BASE1` and `W_MASK1` **reset to zero**, which is **not in their accepted sets**
(they accept `0x700000`, `0x240000000`, `0x3ff00000`). So B's "retain the last accepted value" has no
defined meaning before the first accepted write. Retain the zero? Force the reset value? Decline only
the guarded bits? **B cannot ship without an answer**, and no seat supplied one.

And minimax's measurable objection to B stands unanswered: under B a rejected CONF write retains the
previous value, so **if it differs in bit 0 the PCI bus selection silently changes**, where A leaves
the consumer correct.

### 7i-3. (MED) DOES THE READBACK ARGUMENT SETTLE IT INDEPENDENTLY?

deepseek raised it and codex sharpened it: *"Previously, a rejected write ended execution before
subsequent guest code could observe that value. A creates that observation and allows the guest to
make further decisions from it."* **This does not depend on a model consumer at all** — and it is
exactly what `#447`'s comment means by *"the guest writes CIE|AIE, reads CIE|AIE back, and believes
the RTC will interrupt it."* If it is sound, it decides the round without needing 7i-1 at all.

### 7i-4. (MED) A BRIEF-CONSTRUCTION RULE, MINTED FROM THIS ROUND'S OWN FAILURE

The brief inlined `#447`'s comment **verbatim**, and that comment argues purely from readback — it
never claims a model consumer. The consumed/unconsumed gloss was mine, and **grok adopted my gloss
over the quotation sitting directly above it.**

> **Proposed rule: a premise that RESTATES an inlined quotation is the most dangerous kind, because
> it looks already verified.** Inlining the primary source does not protect against a wrong summary
> beside it — a seat reads the summary as the question and the quote as supporting material.

Is that a real rule worth carrying, or is the existing premise-audit instruction enough?

*Related and already filed: `refilingclass` (six findings re-derived this session that were already
recorded), and `lcaconfbus1kill` (a HIGH row split out of this one's own eleven-kill census, with a
witness design reviewed SOUND by grok).*


---

## 7j. `lcairqstubkill` — FOUR GUEST INSTRUCTIONS END THE HOST, and the fix is a disposition choice

*Witness: `regress/lca_irqstub_probe.py`, 3/4 on the committed build
(`regress/artifacts/lcairqstubkill/witness_HEAD_20260907.raw`). No flagship seat, by the standing
directive reserving opus5/fable5 for this adjudication.*

**MEASURED, not argued.** A store of `0xAA` — the standard 8042 self-test — to `0x1d0000064` on
unmodified `alphabook1` reaches `lca_interrupt_assert`, whose entire body is
`fatal("...TODO"); exit(1);`. Four guest instructions. No disk image, no OS, no host timer, no
driver setup, no unusual value. The matched control stores the **same value** one port away at the
LPT port (which never asserts) and survives, so the death is attributable to the device reached.

The PIC mask is **open at reset** (`dev_8259.c` memsets, and `ier` is written only by a guest
store), so nothing has to be configured first.

**CENSUS: 2 of 70.** Every function registered as an interrupt handler in the fork — 70, all bodies
located — and exactly two call `exit()`. Both are these. **68 handlers manage without terminating.**

### 7j-1. (HIGH) IS A LATCHED DECLINE ACCEPTABLE FOR AN INTERRUPT PATH? *(the row's `hold_question`)*

The option set's members 1–6 all presume a VALUE is being refused; here there is none — it is a
whole path stubbed out, which is why member 7 (IMPLEMENT) was added to the set **from these very
functions**. But IMPLEMENT means delivering an Alpha interrupt, which is a large job.

> **The cheap interim is a latched decline: return without asserting, announce once.** That trades a
> host kill for a **silently lost interrupt** — every ISA interrupt on this machine, forever, after
> one message. Is that an improvement or a different lie? It is the same readback-versus-reality
> tension `lcabadval` is held on (§7i), arriving on a delivery path instead of a register.

### 7j-2. (HIGH) WHAT OBSERVABLE DISCRIMINATES THE FIX MEMBERS?

**The witness cannot.** "Host survives" greens equally for a silent return, a latched announce, and
a real implementation. A fix round owes a row that tells them apart, and I do not have one. A codex
job is out on exactly this question; if it returns "none from a stepped probe", the round needs a
capability it does not have.

### 7j-3. (MED) THE DEASSERT STUB IS ON THE SAME PATH

`isa_interrupt_common` calls `INTERRUPT_DEASSERT(d->irq)` when the last unmasked IRR bit clears, and
`lca_interrupt_deassert` is the same bare kill. **A fix that de-fatalises only the assert converts
"dies on the first interrupt" into "dies on the first interrupt ACK"** and passes any test that
never acknowledges. Does the deassert side need the same disposition, or a different one?

---

## 7k. `m88kexcdetectorl2` — a MEASURED L2, and the repair's cost is the question

*agy measurement: BASELINE 59/59, MUTANT `implemented = (ncpus < 2)` 59/59, zero rows reddened
(`regress/artifacts/m88kexcdetectorl2/agy_measure_20260907.txt`).*

The clean sweep is **explained**: `m88k_exc_probe.py` never passes `-n`, so every row runs at one
CPU and the mutant's condition is true throughout. The repair is one session at `-n 2` asserting the
exception is still delivered — **de-risked by reading**: `-n` is validated to 1..256, the CPUs are
created in the generic path (so bare `-E testm88k` gets them), and `bootstrap_cpu` is deterministic
because `machine_test.c` never sets `use_random_bootstrap_cpu`. That last one would have been a
`random() % 2` flake.

### 7k-1. (MED) HOW MUCH RE-MEASUREMENT DOES ONE ADDED ROW OWE? *(the row's `hold_question`)*

This project's standing caution is that added rows perturb the scores of every mutant already
measured. **Does adding one row to a 59-row detector oblige a full re-table, or is a targeted run —
baseline plus the mutants whose kill sets could plausibly move — sufficient?** The difference is a
full table versus a few runs, and the answer governs every future L2 repair, not just this one.

*Also worth a line: the row said the mutant applies to SEVEN arms; agy derived ELEVEN and explained
the gap — the "seven" counted only arms carrying a `/* m88kexcdeliver */` annotation, silently
excluding four pre-existing vectors in the same switch. A count keyed on an annotation rather than
on what defines the class.*


---

## 7l. `lcaconfbus1kill` — the fix is SETTLED; the DETECTOR is not, and four seats agree it cannot be

*Pass-1 fix panel: `regress/artifacts/lcaconfbus1kill/pass1_panel/` — six seats (codex, grok, glm,
deepseek, minimax, the kimi-k3:cloud substitute). No flagship seat, by the standing directive
reserving opus5/fable5 for this adjudication.*

**THE DEFECT IS MEASURED** (`regress/lca_confbus_probe.py`, 3/4, the RED row being the defect): an
**accepted** `stq 0x1` to `LCA_IOC_CONF` arms a bare `fatal(); exit(1)` that the next PCI config
access reaches.

**THE FIX IS SETTLED AND CONFIRMED AGAINST A PRIMARY SOURCE.** Not from the fork's comment but from
`_guest-src-openbsd22/sys/arch/alpha/pci/lca_pci.c` — the real OpenBSD LCA driver, on this machine:

    } else {
            bus = (tag >> 16) & 0xff;    /*  lca_decompose_tag:103  */
            dev = (tag >> 11) & 0x1f;    /*  lca_decompose_tag:106  */
    }

and `lca_conf_read:127` writes `REGVAL(LCA_IOC_CONF) = 0x01` on the secondary path, proving the
register selects the configuration **format**, not a bus number. **The same driver shows my witness's
two accesses are its own secondary-bus sequence, line for line** — so the row's earlier caution
("not claimed that any shipped guest issues this") is withdrawn.

### 7l-1. (HIGH) SHIP A FIX WHOSE DETECTOR PROVABLY CANNOT DISCRIMINATE IT?  *(the `hold_question`)*

Four seats reached this independently, by different routes:

| seat | how it put the wall |
|---|---|
| grok | *"the witness address is not a type-1 tag, and empty-slot data cannot pin the extract"* |
| glm | it *"conflates IMPLEMENT with explicit-all-ones DECLINE, silent with latched, and can false-pass on stale all-ones unless the destination register is pre-seeded"* |
| minimax, kimi(sub) | only a **populated bus-1 device** could separate them |

**An empty bus 1 answers all-ones whether the model implements type-1 or merely fakes the reply**,
and nothing in this tree places a device on bus 1. So:

> **(a)** ship the fix and DISCLOSE the non-discriminating detector under clause (e); or
> **(b)** ADD a synthetic bus-1 device to the apparatus so the row becomes possible.
>
> **(b) is an addition to the test apparatus made in order to observe a fix** — which is precisely
> the shape the addition licence exists to police, and it is not obviously refused by it either,
> since the licence governs PRODUCT additions. **That boundary is the question.**

*glm's pre-seeding point is the one improvement available under (a) and should be taken either way:
seed the destination register so a stale all-ones cannot false-pass.*

### 7l-2. (MED) A CARRIER LINE FOR `guestsrcunknown` — proposed, not done

`_guest-src-openbsd22/` holds **8,138 `.c` files** covering `alpha`, `arc`, `arm32`, `mvme88k`,
`pmax` and `powerpc` — six of this fork's own targets — at the project root, untracked, and
**mentioned nowhere in the carrier or the harness**. I declared a chipset question unanswerable from
this machine one paragraph before a seat answered it from that tree.

The carrier already says to `ls _scratchpad/*.pdf` before reasoning from first principles about a
device, and records that an absent-source note was load-bearing and wrong for twelve days. **This is
the same shape one directory over.** Editing `CLAUDE.md` is owner-facing and section J checks its
tracked copy, so: **is the analogous line wanted, and in what words?**

*With the caution that belongs beside it: OpenBSD 2.2 is ONE guest at ONE version. Cite it as "the
OpenBSD 2.2 driver does X", never as "the hardware does X" — the models are obliged to match the
hardware, of which this is a well-informed second-hand reading.*


---

### `pcc2c040kill` — `#512` SHIPPED, and I declared a state axis CLOSED twice and was refused twice

*Three stages (assess, design, review) ran without a flagship seat, by the standing directive
reserving opus5 and fable5 for this adjudication. Panel dirs `_scratchpad/panel_20260907_233310/`
and `_scratchpad/panel_20260908_010245/`.*

**WHAT SHIPPED.** A one-instruction host kill removed; witness 3/4 red → 4/4 green on the same
script; a **16-row** detector killing **nine mutants across five tables**.

**WHAT I WANT ADJUDICATED IS NOT THE FIX.** It is that I graded floor-shaped holes as contract debt
**twice in one round**:

1. Table 1's escape (`assert = 0` removed, 7/7) — I graded it a breach correctly, then **shipped
   with it declared and the repair filed**. Pass 2: *"that is the (e) remedy applied to a (d)
   grade."* Four seats' worth of argument, and the CHANGELOG and ledger were saying contradictory
   things about it for about an hour.
2. Then, in the repair, I declared the **encounter axis closed** on two cells — while the C040
   block reads TWO lvalues, so the product is four. The empty cell (C040 cleared after the latch
   fired) went into the residual list as debt. **Four of six seats refused it**; the fifth defended
   it only conditionally and named its own condition. That cell's mutant swept all eleven rows.

### 7m-1. (HIGH) Is the enumeration now complete — and is there a WRITING-TIME rule that catches this?

Both refusals were correct and both arrived at pass 2. The carrier already says DEPENDS-ON
enumerates joint cells over the guard's operands where the body distinguishes them. **So either the
rule exists and I did not apply it, or it does not say what I think it says.** Which?

*Secondary, and cheap: is the 16-row enumeration complete over `GENCTL & C040` × `warned`, or is
there a fifth cell? Three rows past the product came from seats — collateral state (three seats,
independently) and per-session liveness (the substitute seat, alone).*

### `alphatbinegsel` — the OS's "invalidate everything" clears ONE page, and the severity raise is mine

**Source-confirmed by two seats and re-verified by me; witness DESIGNED, not built.**
`ALPHA_TBIA()` is `alpha_pal_tbi(-2, 0)`; `a0` is a `uint64_t` with no signed cast; `a0 >= 1` is
TRUE for `-2`; the call takes the **VADDR** arm with `a1 = 0`. So the primitive that means
*invalidate every TLB entry* invalidates **cached virtual page zero and nothing else** — and the
Alpha fast path goes on consuming the surviving `host_load`/`host_store` pointers into stale
physical backing.

#### 7n-1. (HIGH) Is the severity raise right — and it is MINE, not a seat's

I raised this med → high. The facts are the seats'; **the ranking is the one judgment in this row
that is not a measurement.** A documented OS primitive silently under-flushing during ordinary
operation put it, for me, with the other HIGH rows. **Confirm or correct.**

#### 7n-2. (HIGH) Ship the COARSE repair, or does the round owe the finer semantics?

`if (a0 >= 1 && a0 <= 3)` fixes the misdispatch and does **not** give `ALPHA_TBIAP()` its ASM=0
selectivity. A seat supplied the accurate CHANGELOG sentence and its limit. Is shipping the coarse
repair with that disclosed correct?

#### 7n-3. (MED) Ordering — the input to the existing ranking has changed

A file-reading seat ranked `alphaswpctxreg` FIRST and called that *"a confidence judgment, not a
claim that it has the greatest potential severity"* — explicitly because **this** row's consequences
were then unverified. They are now verified. Does that move this row first?

*Stage state: assess ran two targeted briefs (codex on the dispatch and the callback trace; grok on
the witness design after codex refused it) plus four packet-fed seats. **opus5 and fable5 are
preserved for this adjudication and agy is the measurement reserve, so no flagship seat could run.**
Held and queued as one action.*

### `alphaswpctxreg` (#514) — shipped with a rung-3 witness; the question is whether the round is complete

**MEASURED, not argued:** `cpu_alpha_palcode.c:251` published the old context into `ALPHA_A0` under
a comment saying v0, while the ABI wrapper declares `v0 __asm("$0")` an **output** and lists a0 as
**clobbered**. One identifier. `regress/alpha_swpctx_v0_probe.py` scores **HEAD 2/4, fix 4/4** with
the same script on unmodified `-E alpha -e alphabook1`, using a three-value oracle (old context C,
new context N, sentinel S) so an incorrect repair returning the **new** context is caught rather
than passing. Six seats agreed the fix is correct and sufficient; two independently corrected a
census of mine.

#### 1. (HIGH) Is the detector above the vacuity floor — and is clause (d) *by construction* enough?

I claim (a) from the 2/4 pre-fix run, (b) because that run **is** a verbatim reinstatement, (c) from
the two identity controls, and **(d) BY CONSTRUCTION** — the oracle wants C, and an incorrect repair
gives N, so it cannot pass. **But (d) here is an argument, not a built mutant**, because the fix
adds no predicate to weaken. **Is a clause-(d) satisfied by construction acceptable, or does the
round owe a built `v0 = a0` mutant?**

#### 2. (MED) Does an executed witness move severity?

Six seats said keep `med` and I did not argue. The round now has what the assessment did not: an
executed witness showing a documented primitive returns a sentinel instead of its result.
**Or is that exactly the reachability-versus-harm confusion the ladder warns against** — rung
measures proof strength, never harm?

#### 3. (MED) ~~`#514` landed first, so what does `alphatbinegsel` now owe?~~ — **WITHDRAWN, and the withdrawal is the answer**

Every seat called the `:296` `// TODO: Don't invalidate EVERYTHING!` a separate row and I excluded
it. But `alphatbinegsel` is open on the **same** flush behaviour, and glm warned that whichever of
the two lands second must re-baseline its witness with the other's fix present. **#514 has landed
first.**

*Stage state: design ran SIX seats — codex, grok, glm, kimi, deepseek, minimax — all confirming.
opus5 and fable5 are preserved for this adjudication and agy is the measurement reserve, so no
flagship seat could run. Held and queued as one action.*

### `armbfiwidth` — the third site of an idiom `#510` fixed at two, and the claim is the question

**Six seats agree `#510`'s form does not transfer.** UBFX/SBFX encode *widthm1* so their width is
never negative; **BFI encodes MSB**, so `width = msb - lsb + 1` reaches **[-30, 32]**. Of 1024
encodable (msb, lsb) pairs, **468 reach an undefined shift** and 465 of those also have
architecturally invalid ordering. Prescribed fix:

```c
uint32_t mask = (width <= 0) ? 0U : ((width == 32) ? 0xffffffffU : ((1U << width) - 1));
```

*** A CORRECTION CARRIED FROM `alphatbinegsel`, because the same over-read may colour how you read
its questions: I cited the 21066 manual as documenting `ALPHA_TBIAP()`'s selectivity.  TBIAP does
not appear in the 21066 manual at all -- the quoted sentence describes writes to the ITBASM
hardware register, which is the MECHANISM a PALcode TBIAP would use, not the selector's architected
scope.  The conclusion (ASM has no representation in this translation cache) is unaffected: it rests
on the cache entry's STRUCTURE, established by codex. ***

**The ARM manual is now local and read** — `ddi0406.txt:18066` (A8.8.20 BFI): `if msbit >= lsbit
... else UNPREDICTABLE`, with **no required destination value**.

#### 1. (HIGH) Is this definedness-only, or is a behaviour correction hiding inside it?

codex warns it is **not** definedness-only: at width 32 the manual has BFI copy the whole register,
while under the count-masked host lowering `#510` describes, the **old** mask would be zero and
leave the destination unchanged. **Neither of us has measured that lowering at BFI.** Does the round
owe the measurement before shipping, or is an explicit disclosure enough?

#### 2. (MED) Policy or architecture?

For `msbit < lsbit` the manual mandates nothing, so `mask = 0` is an **emulator policy choice**.
Silently preserve, or announce once? The tree has precedent for both and no universal policy.

#### 3. (MED) What may the detector honestly claim?

`#510`'s own finding: `1 << 31` and `1U << 31` give the **same** mask after the `- 1`, so **no
guest-value row can kill a `1U` → `1` regression** — only UBSAN or a source pin can. Must the
disclosed `ubsanshiftlane` debt land first?

*Stage state: design ran SIX seats — codex, grok, glm, kimi, deepseek, minimax — all confirming.
opus5 and fable5 preserved for this adjudication; agy is the measurement reserve. Held and queued
as one action.*

### `alphatbinegsel` — witnessed, ratified 6/6, and the questions are about what the round OWES

**Witness 5/7 → 7/7, both selectors, with a positive-selector control green on both builds.**
Six seats ratify the guard: grok *"ship `{1,2,3} → INVALIDATE_VADDR, else INVALIDATE_ALL`"*; codex
*"retain the bounded guard, recognise -1/-2 explicitly"*; deepseek, kimi, minimax and glm concur.

#### 1. (HIGH) The accept rows the de-escalation clause demands

minimax found the witness drives only `a0 ∈ {-2, -1, 2}` — **never `a0 == 1` or `a0 == 3`, the
boundaries the fix introduces.** I enumerated it: every bound-moving mutant (`>= 2`, `<= 2`, `<= 4`)
**differs on none of the driven values and escapes.**

The rows are subtle. At `a0 == 1` pre- and post-fix behave **identically**, so these are ACCEPT rows
that cannot red on HEAD; their kill is a bound-moving mutant, observed as an **unrelated page's
cached translation surviving** (because `>= 2` would send selector 1 to `INVALIDATE_ALL`).
**Does the round owe both rows before shipping, and is that the right oracle?**

#### 2. (MED) A citation of mine was over-read, and a seat caught it

I cited the 21066 manual as documenting `ALPHA_TBIAP()`'s selectivity. **`TBIAP` appears zero times
in it**; the quoted sentence describes writes to the **ITBASM hardware register** — the mechanism a
PALcode TBIAP would use, not the selector's architected scope. The conclusion survives on the cache
entry's **structure** (no ASM or ASN metadata). **Is the disclosure sentence now "the finer semantics
have no representation in this translation cache", with the manual cited only for the mechanism?**

#### 3. (MED) Undocumented selectors

`a0 == 0` and `a0 >= 4` are not among the five wrappers; the guard sends them to `INVALIDATE_ALL`.
glm argues the stakes are performance-only — over-invalidation cannot serve stale data and TB
contents are never architected state, so the fix *"can't be wrong, only conservative"*. **Is a
debug-level announce worth its line, or is silence right?**

*Stage state: design ran SIX seats. opus5 and fable5 preserved for this adjudication; agy is the
measurement reserve. Held and queued as one action.*


## 7n. THE NULL-MEDIUM SWEEP AND THE ORACLE-ORDER PROBLEM — four RULE questions from 2026-09-11

*Numbering note, 2026-10-09 (Fable 5.1's 7n answers, 'something ELSE'): `#### 7n-1` .. `#### 7n-3` headings ALSO exist inside the `alphaswpctxreg` entry above -- an older, unrelated numbering under another session's row.  THIS batch is the `### 7n-` headings below; resolve '7n-3' by heading level, never by text alone.*

*Staged ahead of the seat's window rather than during it.  All four change how future rounds run, which is the carrier's own test for what may not wait.*

### ~~7n-1. (HIGH) IS THE PRE-FIX-AS-NULL-MEDIUM SUBSTITUTION A HOUSE CONVENTION OR A FLOOR BREACH?~~ — **ANSWERED 2026-10-09** by Fable 5.1, GPT-6 Astra CONFIRM WITH CHANGES (8): NEITHER -- a pre-fix leg is clause (a) written in clause (c)'s column, an L4 label to correct in place; clause (c) is unmeasured there, not breached; a breach is a genuine null medium coming back GREEN; ppcrldimimask and ppcrlwimiwidth RELEASED; two unwired probes (ppc_rldicl, alpha_tbi) owe a measured leg.  Rule text written into CLAUDE.md and BRIEF_TEMPLATE.md §C6 by owner ruling.  `regress/artifacts/fablequeue7n_20261009/`

An owner-approved sweep of ~165 kill-table units found **one** leg that could never fail (`ppcrlwimiwidth`'s `NULL_MEDIUM`, which compiled byte-identical code to BASE; repaired, honest leg now 12/28).  But it also found **~16 tables that discharge clause (c) with a whole-file PRE-FIX medium** -- `ppcrldimimask`, `ppcrldiclzero`, `mk48nvramkill`, `alphatbinegsel`, `lcabadval`, `sgirandomcolour`.  Every one scored well below BASE, so none is vacuous.

**The difficulty: pre-fix is clause (a)'s medium.**  Using it for (c) collapses (c) into (a) and cannot demonstrate identity rows independently.  `CHANGELOG.md:222` and `:357` record it as an established convention, and two rounds disclose the substitution honestly.

> **THE MEASURED DATA THAT MAKE THIS DECIDABLE — TWO ROUNDS, INDEPENDENTLY, SAME DIRECTION:**
>
>     ppcrlwimiwidth   identity 12/28 (16 red)   pre-fix leg 14/28 (14 red)
>     ppcrldimimask    identity 13/27 (14 red)   pre-fix leg 17/27 (10 red)
>
> **In both, the identity medium reddens MORE rows than the pre-fix medium the convention substitutes for it.**  The identity form is strictly sharper, and in both cases it was available and cost one extra leg (~8 minutes).

**QUESTION: does "a strictly sharper form was available and cheap" convert an established convention into a breach?**  If YES, ~16 tables owe a re-run and `ppcrldimimask` is first (agy is building its leg now).  If NO, the convention stands and clause (c) needs re-wording to say pre-fix is admissible, because as written it is not.  **A third answer -- that (c) means something different for an offline differential than for a built binary -- is open and may be the true one.**

### ~~7n-2. (HIGH) A SHIPPED DETECTOR THAT *CLAIMS* CLAUSE (c) AND NEVER MEASURED IT — L4 OR L2?~~ — **ANSWERED 2026-10-09** by Fable 5.1, Astra-confirmed: NEITHER, ZERO rounds reopen -- luna's and sgirekills' labels are true by-construction claims; shortread's 'pinned at 90' is L4 (no preserved 90-row output; the differential pins 98) and its clause (c) was MEASURED red (`regress/artifacts/shortread/nullmedium_20261009/RECEIPT.txt`).  Rule: L4 exactly when a record asserts a measurement or number not made.  `regress/artifacts/fablequeue7n_20261009/`

Three detectors, all **shipped**, name clause (c) and discharge it by assertion:
* `regress/luna_absentcpu_probe.py:23` — `identity (floor c): 0x12345678 back`.  **The project's own CHANGELOG already ruled that `live` "is a liveness control and CANNOT DO MORE".**
* `sgirekills/PASS2_brief.md:505` — `(c) identity rows -- live, live64, devsig stat`, discharged by naming three rows.
* `shortread/round_20260827/brief_p2.md:86` — `(c) null medium | [IDENTITY] row count pinned at 90`, **while the probe's own output reads 98.**

~113 other tables never attempted (c) at all.  **Silence and a false claim are different things**, and only these three assert coverage a measurement would refute.

**QUESTION: is a claimed-but-unmeasured floor clause an L4 (wrong record, correct the prose in place) or an L2 (floor breach, replace the detector in-round)?**  The stopping rule governs findings against SHIPPED material, and L2 says *replace in-round however late it is found* -- so the answer decides whether three closed rounds reopen.  **I incline to L4 for the two that merely mislabel a real row, and L2 for `shortread`, whose pinned number is refuted by its own probe -- but that split is exactly what I want tested rather than adopted.**

### ~~7n-3. (HIGH) CAN AN ORACLE CORRECTION BE DISTINGUISHED FROM A FIT WHEN THE CODE DOES NOT MOVE?~~ — **ANSWERED 2026-10-09** by Fable 5.1, Astra-confirmed: the order discriminator IS available (rlwinm/rlwnm are still defective at HEAD -- measure the re-pinned oracle RED on HEAD before any fix); the divergence + provenance pair is corroboration, never a substitute; the shared-mask-helper rule NOT adopted.  Owed for ppcrlwhighhalf: records L4s, the oracle repair committed first, a rung-3 witness on HEAD, then the fix round.  `regress/artifacts/fablequeue7n_20261009/`

The oracle-correction rule's discriminator is ORDER: re-pin first, measure the committed build RED, then change the code.  **For `ppcrlwhighhalf` that order is unavailable** -- the defect is open and unfixed, so the oracle is the only thing moving.

Worse, the honest limit: **for `want_rlwimi` taken ALONE no measurement can distinguish a correct derivation from a fit**, because the repair is correct and the corrected oracle agrees with it.  Agreement with a correct implementation is what a right oracle and a fitted oracle both look like.

Two substitutes are proposed:
1. **THE DIVERGENCE TEST.** One shared `mask_range` feeds all four `want_*`.  Correcting it makes `want_rlwimi` agree with the repair AND makes `want_rlwinm` **DISAGREE with shipped code on 47,616 of 131,072 cells** -- a red on a defect filed *before* this correction, in a handler nobody was fitting to.  *A fitted oracle cannot produce a red on a sibling it was never fitted to.*
2. **PROVENANCE.** `mask_range` was written 2026-09-10 for `want_rldimi`, **whose implementation is still wrong today** -- so the helper predates and outlives the repair it is accused of matching.

**QUESTION (a): is that pair sufficient where the order discriminator is unavailable, or does the round owe something stronger?**  **QUESTION (b): should "KEEP ONE MASK HELPER SHARED BY ALL FOUR `want_*`" be minted as a rule?**  Its warrant is structural rather than stylistic: **the only way to fit one instruction while staying green on its sibling is to give the two DIFFERENT masks -- which Book I gives identically at `:4127` and `:4317` -- so a per-instruction split is the tell, and it is visible in the diff.**

### ~~7n-4. (MED) THE VME `default:` ARM IS THREE POPULATIONS. DOES THE FAULT RULING REACH ALL THREE?~~ — **ANSWERED 2026-10-09** by Fable 5.1, GPT-6 Astra CONFIRM WITH CHANGES (7) (`regress/artifacts/fablequeue7n_20261009/astra_7n4/codex_astra.txt`: six registers, SEVEN access sites; the guest panic under FAULT is conditional on unmeasured CMMU state; the file's siblings debug() per access, so 'latched' is a proposal; serving IRQSTAT as 0 skips the abort handler's clear and nmihand()).  **OWNER 2026-10-09: population 2 -> MEASURE FIRST** (a rung-3 probe of the guest's access sequence before any disposition; the FAULT edit stays held; tracked on `vmedefaultkill`).  Populations 3 and 4 filed as `vmewidthlanes`.  As answered: FAULT binds population 1 only.  Population 2 (the header-named registers the in-tree guest touches -- this said '26 header-named, unimplemented registers', which is the count of ALL uncased header offsets, not population 2) is CONTRADICTED by the ruling's own warrant -- the in-tree OpenBSD 2.2 guest accesses MASTERCTL / MASTER3 / MASTER4 / MASTER4MOD at attach and IRQSTAT / IRQCLR in its abort handler, unconditionally and unprobed, so FAULT would turn the host kill into a guest panictrap; default pending the re-ruling is DECLINE + latched announce (the #501 shape), BACKED ACCEPT not licensed.  Population 3 (sub-word lanes) is a width question: 'serve the containing word' refuted; filed as its own row, with a population 4 (cased offsets at len != 4, served lane-wrong).  `regress/artifacts/fablequeue7n_20261009/fable5_rule7n_4.md`

The owner ruled **FAULT (`return 0`)** for `dev_vme.c`'s `default:` arm, and a codex seat independently ruled the same way.  But the seat then split the arm in a way neither of us had:
1. offsets with **no register defined anywhere** — FAULT is honest;
2. **named registers the header defines and the emulator does not implement** — `VME2_DMACTL`, `VME2_T2CMP`, `VME2_T2COUNT`, `VME2_PRESCALE`.  **FAULT says "nothing is here" about something the board documents as present;**
3. **sub-word lanes of registers that ARE implemented** — a byte access at `0x51` is inside T1CMP.  **FAULT raises a bus error on a register that exists**, which is arguably a worse wrong answer than the host kill it replaces.

**QUESTION: does the FAULT ruling govern populations 2 and 3, or do they need their own dispositions?**  Population 3 has an obvious alternative (serve the containing word); population 2 is the genuinely open one, and BACKED ACCEPT is available for it under the addition licence.  **The owner ruled on the arm as a whole because I presented it as one thing; this is me saying it was not.**

### ~~7n-5. (HIGH) FLOOR OR DEBT — ARE A DERIVED-COORDINATE ESCAPE AND A VALUE SLICE THE SAME SPECIES?~~ — **ANSWERED 2026-10-09** by Fable 5.1, Astra-confirmed: NO -- 'closable by a finite row set' is the rejected 09-04 finiteness bound; a derived input is graded by what the body tests on IT, so #519's survivors (tile index, TLB contents, value slices) are all clause (e); one debt row of four readbacks; three L4s; EXHAUSTED/SAMPLED adopted.  Rule text written into CLAUDE.md by owner ruling.  `regress/artifacts/fablequeue7n_20261009/`

**Raised by the measuring seat AGAINST ITS OWN ROUND, and explicitly left unsettled: *"this round grades the tile-index escapes as FLOOR while treating value slices as DEBT, and those are arguably the same species.  It needs one ruling, not two."*

`#519`'s class closure shipped 59 -> 77 rows and killed all six 59/59 escapes.  Two kinds of surviving sweep remain, and the round treats them differently:

* **GRADED FLOOR** — the tile-index family (`M30`/`M31`/`M32`/`M33`), all now dead.  Warrant: `tile_nr` and friends are **pure functions of `(x, y, bufdepth, tlb_mode)`**, so the free input set is finite, read off the function, and closable in one diff.  It was.
* **GRADED DEBT** — `mode & 1`, `x & 1`, `y & 2`, and the `M28` nibble family.  Warrant: these are **within-class value slices, not closable by any finite row set.**

**AND A THIRD CASE SITS BETWEEN THEM, FILED AS OWED RATHER THAN FIXED:** the TLB array's *contents*.  The seat named it as an input to `tileptr`, dropped it from its completeness conclusion, and an audit caught that.  **`tileptr` is the store's ADDRESS OPERAND**, so by the same data-flow test that makes `tlb_mode` a floor axis, the array value looks floor-shaped — and `if (ok || (tileptr & 0xfff00000))` is predicted **77/77**.

*[CORRECTED 2026-10-18 at the row's closure, by this entry's own answer (the heading above;
`regress/artifacts/fablequeue7n_20261009/fable5_rule7n_35.md`): the GRADED FLOOR bullet was wrong as a grade -- the
tile-index family is clause (e), like the value slices and the TLB contents -- and the closure it credits was L1
strengthening on a severity warrant.  "Not closable by any finite row set" separates nothing: each slice is predicted
one-row closable (derived, never run) and only the family is not.  The contents slice is coverage debt, not owed:
`if (ok || (tileptr & 0xfff00000))` is equivalent to the fix on every driven row, by inspection.]*

**QUESTION: is "closable by a finite row set" the right discriminator between floor and debt?**  If YES, the TLB-array-contents gap is floor (L2, owes a repair and its own pass) and the value slices are correctly debt.  If NO, the round has graded one species two ways and the contract's new **EXHAUSTED vs SAMPLED** split is the thing to formalise instead.

*Note the seat rewrote its contract to separate EXHAUSTED axes (`tlb_mode`, `bufdepth`, `color_mode`) from SAMPLED ones rather than calling all of them closed — which is an honest disclosure, but it is a NEW vocabulary entering a contract without adjudication, and that is the half I most want ruled on.*


## BATCH 8n -- QUEUED 2026-09-18, ALL SURFACED BY READING SEAT ANSWERS NOBODY HAD OPENED

*Provenance: a sweep read 23 unread seat answers off disk and recorded them.  That took both stage
gates from GREEN to RED -- 19 violations where HEAD had zero -- because recording a seat's remark
about a row promotes that row's stage from ABSENT to a "short panel".  **The gates fired because the
record got more honest.**  Nine of the nineteen were annotated as never-convened stages; these are
the ones that are genuinely owed.*

### `lcaisalane`  (HIGH -- and see the new row `lcalenzerodrop`)

FOUR of five scriptable seats on `#530`'s CLOSING PASS said DO NOT CLOSE; the round closed on the
fifth.  Their shared argument is a contradiction: if the comment's premise *`len 0 has no producer`*
is TRUE then `if (len == 0) return 0;` is DEAD CODE, so a DROP of it is observationally identical to
base, scores **352/352**, and contradicts the round's own claim that no leg scored 352/352.
Codex adds an omitted **WIDTH** class (`writeflag == MEM_WRITE && len <= 8`, also predicted 352/352)
and flags an *expected -- not measured* 352/352.  **Build both mutants and report with the log named.**

**PASS 2 ON 8bd97e4 (closing pass 7), 2026-09-18 -- the §F2 adjudication pass runs next; fable5 rules LAST.**  PASS 2 ON 8bd97e4 (closing pass 7), D1 -- the rule question: the width row misses seven one-edit variants -- a cut-off at 16 (`&& len <= 16`, `len > 16` refused), wide writes serviced only at lane 3, a refusal below port 0x200, a refusal at k = 16 (two shapes), a second-chunk refusal -- each MEASURED undetected by the composite and each killed by the same GETENV instrument at another reachable cell (regress/artifacts/lcalenzerodrop/opus_p2_20260918/RESULTS.txt).  Are they L2 floor breaches, making pass 6 + pass 7 two consecutive width-class breaches that owe the CLASS CLOSURE in one diff, or clause-(e) debt that owes only an honest contract now that a shipped instrument can reach every cell?  Seats: L2 -- codex (a,b,c), glm (a,b,c,g), kimi (c,e), deepseek and minimax (all five); debt -- agy, grok (but the contract's 'any' must narrow), opus5 (pass 6's 'uncatchable' read as a condition on discharge).  The research question above now has measured answers on both halves: M1_lenzero 352/352 (equivalent by no producer), and the width class was pass 6's L2 -- the row shipped in 8bd97e4.

### ~~`wdcrearmzero`  (MED)~~ — **DISCHARGED 2026-10-09**: Fable 5.1 and Opus 5.5 answered the held review stage as late seats (both measured: the held question is CLOSED at HEAD, and an L2 floor breach of #473's shipped detector was found and filed as `wdc473floor`); recorded in `200671b6`.

The 2026-08-27 pass-2 panel ran eight scriptable transports only; opus5 and fable5 were never fired,
and the kimi seat was LOST on both transports (CLI 403 weekly wall, substitute HTTP 503).  Three cloud
seats recovered 2026-09-18 all RATIFY.  Minimax's premise audit is the open item: the 513-block figure
*"assumes `WDC_MAX_SECTORS=512` -- the author states this but the value is not in the brief"*.

### 8n-3. SIX CLOSED ROWS OWE A `regress` REVIEW  (regress is FABLE-ONLY by standing directive)

Each closed with commits and carries no `regress` entry.  They are named here individually because a
prose mention does not count as queued -- an id counts only if it HEADS an entry.

### ~~`wdcaltctrlbit`~~ — **DISCHARGED 2026-10-09**: Fable 5.1's regress review, REGRESS CLEAN (`regress/artifacts/fablequeue8n_20261009/regress_devices/`).
### ~~`diskimagesign`~~ — **DISCHARGED 2026-10-09**: REGRESS WITH FINDINGS (3), all records, applied in place.
### ~~`sgirergbroundtrip`~~ — **DISCHARGED 2026-10-09**: REGRESS CLEAN.
### `lcashiftub`
### `alphapfnoffset`
### `alphaswpctxptbr`

### ~~`landiskaux`~~ — **DISCHARGED 2026-10-09**: Fable 5.1's regress review, REGRESS WITH FINDINGS (1) -- a stale hold, dated in place.

`regress` review owed (flagship-only): #533 shipped in e16a8b7 -- fix `+0x2c`, detector regress/landisk_aux_probe.py (gate_sh_rounding.sh), rung-4 boot witness regress/artifacts/landiskaux/boot_20260918/.

### ~~`asiceventaddr`~~ — **DISCHARGED 2026-10-09**: Fable 5.1, Opus 5.5 and a deepseek re-fire answered the held review stage as late seats, and opus5's unrecorded 2026-08-26 pass-2 answer is now recorded; in `200671b6`.  The row stays OPEN for its closure round (a compile-only detector for the guard, and the records it found wrong).
REVIEW stage held 2026-09-18 (#534 F1): panel_20260826_222557 was PASS 2 on this row's own commit 9ca9cca and ran 6/9.
fable5 and opus5 were never fired; deepseek's answer there is a thinking burn (seat failure).  Question: is 9ca9cca's
comment-only disposition for SYSASIC_EVENT_RANGE_OK right, given codex's finding that the guard protects the ADDR macro
and not the BITMASK macro, and kimi/minimax's dissent that a name-insensitive build-time check is possible?

### ~~`pcc2c040assertrow`~~ (review stage) — **DISCHARGED 2026-10-09**: the four packet-fed seats re-fired (three ROW OWED, one CLOSED); both proposed one-line variants MEASURED undetected, 18/18 each; Fable 5.1 (v3, GPT-6 Astra concurring) graded both clause-(e) debt -- filed `pcc2c040assertxor` and `pcc2c040warnedeq` -- and the row is closed again, with the owner's ruling on the rule question it raised recorded (keep the written rule).  Its REGRESS stage, queued 2026-09-11 above, is still owed.
*As queued:* REVIEW stage reopened and held by OWNER DECISION 2026-09-18 (#534 R3): re-fire glm, deepseek, minimax, kimi(sub) on a
brief that inlines ASSERTROW_brief.md's rows and mutants (panel_20260917_100431 gave them dev_pcc2.c's stale comment).
Question: is the assert=0 -> return mutant (skips INTERRUPT_DEASSERT) killed by any shipped row; if not, what row is owed?
NB check_stage_panels reports this stage 9/9 complete because a full count masks a live HELD marker -- filed `heldmasked`.

### `n6`
**RULE QUESTION ANSWERED 2026-10-09**: Fable 5.1 ruled (a), a seat answer that re-opened the stage (`regress/artifacts/fablequeue8n_20261009/regress_harness/fable5_regress_harness.md`, section 4); GPT-6 Astra confirmed (a) on the owner's entry-[5] choice and the seven answers that completed the panel, and corrected two of the four reasons (`regress/artifacts/fablequeue8n_20261009/astra_confirm/`).  No further assess panel is owed.  **STILL OWED UNDER THIS HEADING: the `regress` review of #539 (`7836071`)** -- which is why the heading stays un-struck.

*As queued:* ASSESS stage held 2026-09-18 (#534 F2 pass): rule on the 2026-08-30 fable5 entry -- (a) a seat answer re-opening the stage,
(b) a single-seat re-read, or (c) an adjudication record.  My own RE_READ tag was reverted as self-dealing (5 of 7 seats).

### ~~`stagetokens`~~ — **DISCHARGED 2026-10-09**: REGRESS WITH FINDINGS (5) -- two records L4s applied in place; filed `stagetokenscontrols` and `dashokclass`; one finding folded into `fablequeueregress`.
`regress` review owed (flagship-only): #534 shipped in 09ded75 -- stage_tokens.py + four readers; controls
regress/artifacts/stagetokens/controls_534/ (49/49, 33 mutants).  fable5 already ruled last on the diff; this is the regress pass.

### ~~`heldmasked`~~ — **DISCHARGED 2026-10-09**: REGRESS WITH FINDINGS (1), filed in `stagetokenscontrols`.
`regress` review owed (flagship-only): fixed inside #534 (09ded75) -- live holds beat a full count; rows t_fullhold,
t_fullclosed, t_discharged, t_samedayhold.

### ~~`pcc2c040mienannounce`~~ — **DISCHARGED 2026-10-09**: REGRESS WITH FINDINGS (2), both records, applied in place.
`regress` review owed (flagship-only): #535 shipped in bb8efbf -- two rows close the {presence,count} x {MIEN} product for
the C040 announce; pcc2_c040_probe.py reclassified DETECTOR and gated in gate_arm.sh (18 rows).

### ~~`fbsmlane`~~ — **DISCHARGED 2026-10-09**: REGRESS WITH FINDINGS (1), a wording L4 applied in place; R3 is the right pin and no further lane coverage is owed.
`regress` review owed (flagship-only): #537 shipped in cdbe7d7 -- the fbpending_bound self-mutant lane wired in
gate_offline.sh, pinned on R3's case-qualified row (not the verdict-equivalent R4); measured P0-P4 in
regress/artifacts/fbsmlane/r537_20260918/f2_pin/out/, gate 2 345/346.  fable5 already ruled LAST on the diff; this is
the regress pass (is the R3 pin the right pin, or is further lane coverage owed?).
