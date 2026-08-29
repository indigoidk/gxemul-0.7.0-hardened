# Stale `[HELD AWAITING SEAT: x]` markers — the sweep, its THREE defects, and the adjudication

**2026-08-29.  Reading and ledger edits only; nothing built, no gate run.**

## THE CLASS

The marker is read FUNCTIONALLY by three precommit-wired tools — `gen_codex_wall.py`,
`check_fable_queue.py`, `check_stage_panels.py`.  A marker left in place after its seat answers
makes an answered stage report as WAITING, and **repeats the lie on every regeneration** rather
than self-refuting the way a stale citation does when a reader opens the file.

## THE NUMBERS, AND THEY MOVED TWICE

    27 held stages    pre-sweep (gen_codex_wall.py's own regex, on HEAD)
    12                after my first sweep      -- 20 markers defanged
     7                after the corrected sweep --  8 more

**My first headline (27 -> 12) UNDERSTATED the phantom fraction.**  The honest count is 7, and
those seven are real: five fable5-regress holds (`ns16550`, `carrier`, `es438`, `sh4sci`,
`wdcdataoutdrain`) plus `proberowsubset`/codex and `wdccdbmidxfer`/opus5.

## *** MY SWEEP HAD THREE DEFECTS AND MISSED ROUGHLY A THIRD OF ITS OWN POPULATION. ***

Found by the adjudicating seat, each then reproduced by me:

1. **THE STATE FILTER — the big one.**  My script opened with
   `if r.get("state") in ("closed","dropped"): continue`.  **`gen_codex_wall.py` does NOT
   filter on state**, so a CLOSED row's live marker still feeds the wall.  That single line hid
   `exitsweep`, `xfamscope`, `m8sarseq` and `asicbadaddr` — and three of those meet my own
   stated criterion *exactly*, which is what makes this a defect in the sweep rather than a
   judgement call.
2. **A 200-CHARACTER THRESHOLD**, chosen arbitrarily, which wrongly KEPT `probetimebased`:
   agy's real answer there is **182 characters**.
3. **DAY-GRANULAR DATES**, so a same-day-but-later answer was undecidable — `ieeeupgrade` and
   `pitclobber` both have answers on the marker's own date at a later entry index.

**So "20 of 20, found mechanically" was false.**  The population was at least 28.

## THE CORRECTED CRITERION

> A live marker naming seat S in stage P is stale **iff** there is a non-marker entry by S in
> the **SAME STAGE P**, at a later date, or the same date with a later entry index.

Stage-scoped deliberately: row-scope over-clears across stages, which is exactly how my first
pass mis-cited `wdccdbmidxfer`'s **regress** marker against a **research**-phase answer.  No
length threshold; no judgement about answer quality.  It is an internal contradiction inside
the one file the tools read.

## WHAT I GOT RIGHT — AND THE ONE THING THIS SECTION GOT WRONG

**19 of 20 from the first sweep were verified clean, not sampled** — each has a later
same-stage non-marker answer by the named seat.

> ### *** THIS SECTION ORIGINALLY SAID "NOTHING WAS WRONGLY DEFANGED" AND CALLED THE 20th
> ### "AN L4-GRADE NIT ON A NOTE, NOT A SILENCED SEAT".  THAT WAS WRONG, AND THE LATER GATE
> ### ADJUDICATION (BELOW) ESTABLISHED WHY. ***
>
> The 20th — `wdccdbmidxfer`'s **regress** marker — was not a citation nit.  Because entry
> classification keys on note CONTENT, defanging it made the entry stop being a marker and
> **fall through into the seat tally as an ANSWER**, so it became the sole evidence that fable5
> answered a FABLE-ONLY stage it has never answered.  **That is a manufactured seat answer, and
> it is a silenced seat.**  Restored to a live marker; full account in the gate-adjudication
> section below.
>
> *Kept in place rather than swapped, because the wrong version is the interesting part: I
> checked 20 markers, reported the 20th as borderline, and graded it as harmless on the wrong
> axis — I asked whether the SUBSTANCE was discharged and never asked what defanging DID to the
> tools that read the entry.*

## *** A LIVE DAMAGE CHANNEL I DID NOT FIND, AND IT IS THE WORST PART. ***

`check_stage_panels.py`'s held branch **exempts a stage from the nine-seat FAIL without checking
that the hold covers the missing seats.**  So ONE stale marker suppresses a hard gate for its
whole stage.  That is the seat-failure-counted-as-agreement shape, live in code.

Compounding it: the completeness short-circuit runs BEFORE the held branch, so a 9/9 stage never
has its `_held` examined — which is also why the documented CLOSED-WHILE-HELD anti-loophole is
**unfireable for exactly the population where markers go stale**.  `exitsweep`, `xfamscope`,
`m8sarseq` and `asicbadaddr` were all closed-with-live-markers and it reported zero violations.

## A SECOND TOOL DEFECT: THREE CONSUMERS, TWO MATCHING RULES

`gen_codex_wall.py`'s regex ends `([a-z0-9_]+)\s*\]`, which **cannot see a multi-seat marker**
like `[HELD AWAITING SEAT: codex, agy, ...]`.  So `asicbadaddr`'s and `probetimebased`'s markers
were invisible to the wall while `check_stage_panels` (substring plus split-on-`]`) saw them.
The generator also matches case-insensitively where the other two are exact-case.  **Unify into
one shared `marker_seats()` the three import** — filed, not done.

## FIXED IN THIS PASS

* **28 markers defanged** across the two sweeps, human-legible, pattern broken.
* **A FALSE ACTION-INSTRUCTION in `gen_codex_wall.py`'s prose constant**, re-printed into
  `fable_queue.md` on every regeneration: it named seven rows as *"NOT re-fired and still
  carry genuine codex holds"*.  **Codex answered all seven on 2026-08-26** (verified by counting
  substantive codex entries per row; `ovsync` has three).  Corrected in place, with the reason:
  *a hardcoded roster inside a GENERATOR is a wrong record waiting for the data to move.*

## FILED, NOT BUILT: the check

**Verdict was BUILD IT — the recall argument is genuinely inverted** versus the two checkers
this project rejected on measurement.  Those were rejected because recall was ~zero and no tool
read the artifact functionally.  Here the literal IS machine-read by three precommit-wired
tools, and a checker keyed on the consumers' own matchers has **definitional** recall.

**The decisive evidence is this sweep itself: run by hand, carefully, it missed a third.**  That
is the "a check a human has to remember eventually does not happen" failure, measured in the
session that proposed it.

Shape, as prescribed: home it **inside `check_stage_panels.py`** (not a fourth parser — four
counting methods once gave four answers); move the held-marker handling **ahead of** the
completeness short-circuit; **FAIL post-cutoff, report-not-fail the backlog**; **flag, never
auto-defang**, because staleness is mechanical while discharge is a judgement about the
`hold_question`.  Negative controls both ways before wiring.

**Honest caveat, recorded because it cuts against building it: no CONSUMED DECISION was found.**
The measured damage is tool-output corruption, operator misdirection, and the suppressed gate
above — not a wrong fix shipped.

---

# THE GATE ADJUDICATION, 2026-08-29 — five more consequences, and one wrong record of mine

## *** MY SWEEP MANUFACTURED A SEAT ANSWER.  ONE of 30, and it is restored. ***

Marker entries carry a `seat` field, and tools classify an entry by its NOTE CONTENT.  Once
defanged, the note stops matching the held literal — so **the entry falls through into the seat
tally as an ANSWER**.  Harmless for 29 defangs, because the seat really had answered that stage.

Not harmless for **`wdccdbmidxfer` / regress / fable5**: the defanged entry became the SOLE
evidence that fable5 answered the REGRESS stage, and fable5 never has.  **Root cause is my first
sweep's ROW-SCOPED criterion** — a RESEARCH answer discharged a REGRESS hold, and regress is
FABLE-ONLY by standing directive, which is exactly why cross-phase credit is wrong there.
Restored to a live marker.

**And my hunt for it failed in the other direction.**  I filtered candidates with
`"HELD" not in note`, which excluded two GENUINE answers that merely QUOTE the word — one of
them discussing held markers — inflating a true finding of ONE into a claimed THREE.  Third
time in one session that this literal has fooled a check of mine.

## MY PROPOSED PREDICATE WAS UNSOUND

I asked whether `len(got) + len(named) >= n_seats` would do.  **It double-counts**: a seat can
be in `got` AND named in a stale marker — that is the whole class — so 8 present including S,
plus a marker naming S, sums to 9 while seat T is missing and unexplained.  Addition fails in
the MASKING direction, which is the one direction this gate must never fail in.

The sound form is set arithmetic over the roster:

```
unexplained = [s for s in seats if s not in got and s not in named_valid]
```

with two mandatory hardenings, both from the code as it stands: **validate names against the
roster** (the extraction takes free text to the `]`, so a typo'd seat name would otherwise
explain a gap silently — the check-that-cannot-fail shape), and **carry marker dates** (`_held`
stores note text only and discards `ent["date"]`, so no marker-dated cutoff is expressible).

Measured at today's ledger: **exactly one stage fails — `proberowsubset`, unexplained=6, marker
dated today.**  `wdccdbmidxfer` research 8/9 has unexplained=0 and passes.  *The design case and
the defect case separate cleanly at the live ledger*, which is the strongest argument the
predicate is right.

## (A) IS NARROWER THAN I FRAMED IT — a DEFERRAL hole, not a waiver

The debt SELF-RESTORES on two paths: clear the marker while the row is open and the stage lands
short and post-cutoff (hard violation); close while short-and-held and CLOSED-WHILE-HELD fires.
It never resurfaces on exactly three paths — an eternal marker on an eternally-open row, the
roster filling to 9/9 over a standing marker, and close-after-9/9.

> **The last two are (B).  So (A) is the LARVAL FORM of (B): the under-accounted hold matures
> into the invisible stale marker.  One defect at two ages, and one fix should take both.**

## THE PRESCRIBED MOVE REDS NOTHING TODAY — AND IS STILL THE WRONG SHAPE

Measured: zero stages currently have >=9 seats plus a live marker, and zero marker-only stages
exist.  **The backlog objection is moot BECAUSE THE SWEEP RAN FIRST** — pre-sweep it would have
redded all four closed rows.  *Sweep-then-fix was the right order and happened by scheduling
accident; the eventual commit message owes that dependency.*

But folding a 9/9-held stage into HOLD prints *"awaiting: X"* where X has answered — a wrong
report — and then subjects it to a hold_question FAIL keyed on seat dates, so a stale marker
reds as "no question" when the defect is "stale marker".  **Two states rendering the same,
which is this gate's founding rule.**

**Prescribed instead — three outcomes above the short-circuit:** (i) all named seats in `got`,
or stage complete -> **STALE-MARKER**, its own label, forward-only from a marker-date cutoff;
(ii) row closed -> violation, labelled stale-vs-genuine by the same test; (iii) open and short
-> HOLD with `unexplained` printed.  Today: 0, 0, and 2 lines with 1 red.

## THREE MORE CONSEQUENCES I DID NOT NAME

* **BLIND AT THE ZERO END TOO, AND THAT IS THE WORSE END.**  The seats-guard skips any stage
  with no `"seats"` key — so a stage whose ONLY entry is its hold marker is skipped wholesale,
  **including on closed rows**.  CLOSED-WHILE-HELD can therefore fire only in the 1–8 window.
  Zero seats, a marker, then close is verbatim the *"mark any gap and walk away"* shape the
  anti-loophole was written to forbid.  **The prescribed move does NOT fix this** — the guard
  itself must relax.
* **THE HOLDQ CUTOFF IS KEYED TO THE WRONG EVENT.**  A brand-new hold placed today on a stage
  whose answers predate the cutoff evades the hold_question FAIL, because `newest` is
  seat-answer dates, not marker dates.  "New holds carry questions" is enforced by the age of
  the ANSWERS.
* **PHASES OUTSIDE `STAGES` ARE STRUCTURALLY INVISIBLE**, and this **RECONCILES THE 7-vs-2**
  between the two tools rather than leaving it as a divergence: `gen_codex_wall`'s 7 = five
  `regress` holds + the two in `STAGES`.  Benign for regress by design, but `adjudicate` (15
  entries) and one phase-less entry share the blindness.

Plus: `RE_READ` sets the same `_annotated` flag as `ANNOTATION`, which grandfathers a short
stage regardless of date; `filed` ignores row state, so a closed row prints "not yet panelled"
forever; and **`FABLE_ONLY` is dead code** — defined once, consulted nowhere, so the regress
exemption is enforced only by accident of `regress` not being in `STAGES`.

*All FILED.  Every one is a change to a precommit-wired gate and owes negative controls in both
directions, and the machine is busy.*
