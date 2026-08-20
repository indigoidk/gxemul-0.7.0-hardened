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

`armbdt` (assess:codex) · `b118L` (assess:codex) · `b120r` (assess:codex) · `capN` (assess:opus5) · `capgap` (assess:opus5) · `carrier` (assess:fable5) · `census` (assess:opus5) · `cflood` (assess:opus5) · `cmtattr` (assess:fable5) · `constblind` (assess:opus5) · `devexit` (assess:opus5) · `dfreq` (assess:codex) · `es438` (assess:fable5,opus5) · `exitsweep` (assess:codex,fable5) · `fablequeue` (assess:fable5) · `fbextrate` (assess:fable5) · `fbpending` (assess:fable5) · `fbwitness` (assess:fable5) · `floodclass` (assess:fable5) · `gateflr` (assess:opus5) · `gcsections` (assess:fable5) · `hlen` (assess:fable5) · `i8253zero` (assess:fable5) · `idesync` (assess:fable5) · `ieeeupgrade` (assess:opus5) · `isaorder` (assess:fable5) · `landiskdisk` (assess:fable5) · `ledgerwitness` (assess:fable5) · `m437multi` (assess:fable5) · `m437rtmp` (assess:fable5) · `m8invground` (assess:fable5) · `m8invpred` (assess:fable5) · `m8latch` (assess:fable5) · `m8patc` (assess:fable5,opus5) · `m8probe` (assess:opus5) · `m8sarseq` (assess:fable5,opus5) · `m8seg` (assess:fable5,opus5) · `m8snprintf` (assess:fable5) · `mrwgrind` (assess:opus5) · `mrwstore2` (assess:opus5) · `ns16550` (assess:fable5,opus5) · `optrow` (assess:opus5) · `ovsync` (assess:codex; research:codex; review:codex) · `pcchalt` (assess:fable5,opus5) · `pcheck` (assess:opus5) · `pitclobber` (assess:codex; regress:fable5; review:fable5) · `pitflip` (assess:fable5) · `pitlatch` (regress:fable5; review:fable5) · `pitlsb` (assess:fable5) · `reprowitness` (assess:codex) · `rtcflood` (assess:fable5) · `rtcnarrow` (assess:fable5) · `scunbacked` (assess:fable5) · `seam` (assess:opus5) · `selfcheckman` (regress:fable5) · `sigunsafe` (assess:opus5) · `smdatefmt` (assess:opus5) · `strad` (assess:fable5) · `tfreq` (assess:opus5) · `wdcflood` (assess:fable5) · `wdcnoirq` (assess:fable5) · `wdcstandby` (assess:fable5) · `xfamscope` (assess:fable5,opus5)

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

**This is ONE outage plus one allocation, not 63 decisions, and it is written once rather than once per panel.**
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
