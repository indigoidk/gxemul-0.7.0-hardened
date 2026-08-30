# PANEL BRIEF SKELETON — copy this, do not write a brief from memory

**Adopted 2026-08-28 by flagship adjudication.**  Every section below exists because a
measured incident cost this project something, and the reason is recorded with it.  This file
is the artifact present at the moment a brief is written, which is this project's own finding
about where prose actually fires:

> *"the premise-audit paragraph is the one piece of prose that demonstrably works ... it lives
> in the BRIEF TEMPLATE, the artifact present at the moment of decision.  That is structure in
> the sense that matters — text located where the decision happens, not text located where the
> reasoning was recorded."*

**THE FAILURE THIS FILE EXISTS TO STOP is not forgetting the rules.  It is remembering them
and not applying them to the object in front of you.**  The `SETTLED PREMISES` section below
was invented on 2026-08-27, applied correctly the same evening at 22:21, and **dropped at
11:55 the next morning by its own author in the next brief of the same campaign** — fourteen
hours from minting to breaking.  Nobody had forgotten it.

---

## §A — THE OPENER (copy verbatim, adjust the incident count)

```
## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them — say so rather than
reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**VERDICT LINE FIRST**, so your answer survives truncation.
```

**Why each line is here:** the premise-audit instruction has two prior trials and caught
something both times, the second finding FOUR wrong premises.  The tree-naming line exists
because a seat once returned 80 KB of internally-consistent review of the WRONG `src/`.  The
cannot-read-files line exists because a stalled packet-fed seat is indistinguishable from a
quota wall in the output, and this project misdiagnosed that for days.  Verdict-line-first
exists because answers get truncated and the verdict is what survives.

> **AND THE WRONG-TREE HEURISTIC HAS A KNOWN HOLE:** it says *disagree by hundreds*.  A brief
> written against a stale checkout can be off by ~170, which is neither "hundreds" nor zero,
> and the heuristic then MISDIRECTS a seat reading the correct tree.  Prefer §B.

## §B — CITE BY GREP ANCHOR, NOT BY LINE NUMBER

**Same-file references: positional or by construct name.  Cross-file: a VERIFIED-UNIQUE grep
anchor.**  Give the anchor, not the number:

```
    the site        grep -n 'GDROM Read TOC not 408' <file>
    the common tail grep -n 'Any resulting data' <file>
```

*This is the citation-form rule, and it earned this section on 2026-08-28 when a brief shipped
`:409`/`:486` from a three-commit-stale checkout — the FIFTH generation of numbered-citation
drift on that one file, whose own probe header says in capitals **"DO NOT RE-NUMBER THEM —
GREP FOR THEM."**  A grep anchor that matches nothing is LOUD; a wrong number is silent.*

## §C0 — *** HAS THIS ROUND ALREADY SHIPPED?  TWO COMMANDS, BEFORE YOU WRITE ANYTHING. ***

**Adopted 2026-08-29, after a complete pass-1 brief was written and NINE SEATS WERE
FIRED to redo work that had shipped two days earlier under four commit numbers.**

```
git log -1 -- <each file the round would touch>
grep <each row id> CHANGELOG.md
```

Paste both outputs into §C as settled premises.  If the CHANGELOG names the row id,
**THE ROUND HAS ALREADY RUN** -- what remains is records work, not implementation.

### The incident, because the cost was a whole panel

Three `dev_wdc.c` rows carried a full **9/9 research stage**.  The work then shipped as
`#479`/`#480`/`#481`/`#482`.  **Zero entries landed back on the rows.**  The ledger froze
at `in work`, and the main loop -- correctly treating the ledger as the queue -- drafted
a fresh PASS-1 brief and convened nine seats on it.

The brief's own "mandatory" mutant (END-flush) was already in the preserved kill table
as `MdEndRing`, KILLED with 5 reds.  Its headline question -- *what is the smallest edit
that resets some state and not the rest?* -- was already answered by `MdNoPhase`,
`MdNoWip` and `MdNoRing`, each with a named SOLE carrier row.

> **THE CHANGELOG KNEW.  THE LEDGER DID NOT.**

### Why the existing gates cannot catch it

`precommit_check.sh` section **H** reads LEDGER ENTRIES and **skips stages that never
started** -- and the implement and review stages never started on those rows.  A round
that ships without writing back is invisible to it BY CONSTRUCTION, not by oversight.
This is the unread-review class one step worse: **an unrecorded ROUND**.

*A checker -- warn when a row id named in a CHANGELOG round block is still `in work`
with no post-ship entry -- is FILED, not built: it changes what every commit must pass
and owes two negative controls, which is an owner decision rather than a round's.*

## §C — SETTLED PREMISES  *** MANDATORY.  COPY FORWARD.  THIS IS THE ONE THAT GETS DROPPED. ***

```
## N. PREMISES ALREADY SETTLED, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM

Settled by <which pass/round>, evidence <panel dir or file:construct>:

* **<premise>** — <one line> — <its warrant>
* ...
```

**Or, if genuinely none:** `## N. SETTLED PREMISES: none carried — first brief of this
campaign.`  **Say that explicitly; a missing section and an empty one must not render the
same.**

**THE OBLIGATION IS PER-PACKET AND BROAD:** *any* packet-fed brief re-inlines every settled
premise its own questions depend on — **whatever pass or round settled it.**  The narrow form
("pass 2 re-inlines pass 1") was considered and REFUTED by its own second instance, which ran
pass-1-to-pass-1 across two rounds with no pass 2 anywhere in the story.

**HOW: copy forward.**  The previous brief's settled block in the same campaign is the
starting point.  Copy it, prune what no question depends on, append what the latest pass
settled, name the source panel dir.

**THE STOP CONDITION, so this never becomes "inline everything":**

1. **Settled means SETTLED** — a recorded resolution (a file/line reading, a measurement, a
   panel convergence), citable in one or two lines WITH its warrant.  Premises and warrants;
   never derivations.
2. **A premise enters only if a question in THIS brief depends on it.**  Write-time test:
   *could a seat build a conditional answer — "if X then A, else B" — on it?*  That is
   exactly what a blocked seat produces (*"if `fatal()` exits, then `0x24` is also fatal and
   the asymmetry disappears"*), so it is dependence seen from the packet side.
3. **Scope is the CAMPAIGN.**  Blocks do not accrete across queue items.  A premise needed by
   many campaigns escalates to §E of this skeleton — **never into `panel_ollama.py`.**

> **WHY NEVER INTO THE TRANSPORT:** a tool that stamps a repo FACT onto every packet becomes a
> wrong record the day the fact changes, applied by machinery nobody rereads.  The transport
> preamble stays SEMANTIC-FREE.  (`panel_ollama.py` already asks seats to name premises they
> cannot settle — that is the READ side of this loop, and it worked: two seats named the
> missing premise plainly instead of guessing.  Only the WRITE side was broken.)

**MEASURED COST OF OMITTING IT:** ~10 lines omitted; two packet-fed seats spent their ENTIRE
answers re-deriving (3.4 KB and 9.7 KB), one built a sound-but-conditional defect report on
the unsettled fork, and a rule question was queued.  The block does not compete with the
inline-every-fact rule — **it displaces re-derivation, which is the most expensive thing a
packet-fed seat does.**

## §C2 — *** A PATH IS NOT EVIDENCE TO A PACKET-FED SEAT.  INLINE THE ARTIFACT. ***

**Four of the nine seats CANNOT READ FILES.**  Citing `regress/artifacts/<row>/RESULTS.txt` or
`src/include/thirdparty/wdcreg.h` tells them nothing — it tells them only that you had
evidence and did not show it.  A path is a citation for the RECORD and for the file-reading
seats; it is not a substitute for the bytes.

**INLINE, in the packet, anything a question depends on:**

* **constants you assert** — `WDCTL_RST` is `0x04`, not "the reset bit per `wdcreg.h`";
* **measured tables** — paste the histogram, do not name the log that holds it;
* **the body of any function whose EFFECTS you characterise** — if the brief says "it only
  latches a signature", show the four assignments;
* **negative claims** — "nothing else claims this address" is unverifiable from a packet
  unless you show the device list.

**MEASURED, 2026-08-28:** a brief did all four of these wrongly at once and the packet-fed
`deepseek` seat returned **NOT RATIFY**, itemising exactly them — *"NOT CHECKABLE: the measured
histogram is reported but not inlined; the artifact path is given but cannot be read from this
packet."*  **That is not a seat failure and not an objection to the design; it is the seat
doing precisely what the transport preamble asks.**  Score it as a BRIEF DEFECT.

> **THE TELL, when you are writing:** if a sentence contains a file path and the fact matters,
> ask *"what does a seat with no filesystem do with this line?"*  The answer is always
> "nothing", and that is the whole rule.

## §D — INLINE THE FULL ENCLOSING FUNCTION IF ANY EDIT IS PROPOSED OR EVALUATED

Every exit path, and the common tail included.  *A proposed edit is a SKETCH until it has been
run against real control flow: four independent readers once proposed the same `return` into a
function whose common tail none of them had read, which would have handed a guest an untouched
buffer.  When every reader makes the same mistake, suspect the brief.*

## §E — THE FIXED QUESTION SET (ask all three; add round-specific ones after)

Adopted on their PRIOR record, not on any single day's sample:

1. **The premise audit**, with load-bearing premises stated AS QUESTIONS.
   *Two trials, catches both times; the second found four.*
2. **"What is the SMALLEST EDIT that breaks this and still passes?"**  Name the row you expect
   to stay green.  *Highest recorded per-invocation yield in the project.*
3. **Option-set completeness**, wherever a disposition is chosen: *"is there a member this
   brief did not name?  Grep the fork for the existing idiom."*
   *Two measured catches — a whole option-set member, and a bounded-diagnostic idiom the tree
   already had.*

**PLUS THE STANDING LICENSE, and it is not decoration:**

```
If, while verifying a claim, you found something ELSE — say so.
```

*That channel produced FOUR carrier corrections in one day and found the DC21285 datasheet
that settled a round.  It came from seats with license to wander while verifying, not from any
directed question.  A template that is 100% directed questions removes the slack it operates
in.  The template guarantees the high-yield questions are ASKED; it must not imply they are
the only way to answer.*

## §F2 — *** THE ADJUDICATION PASS: THE PANEL SHARES ITS FINDINGS. ***
## Standing owner directive, 2026-08-30. This is a THIRD pass, not an optional extra.

> **"Make sure to always adjudicate findings and make sure the full panel shares findings."**

Until this directive, every seat answered the same brief **blind to the other eight**, and
the main loop silently arbitrated between them. That hid two things, and both are this
project's oldest failure shapes wearing new clothes:

* **A seat could not correct another seat's error.** The panel's own record shows seats
  refuting each other constantly *when given the chance* — but they were never given it, so
  the only cross-checking that happened was whatever the main loop chose to do.
* **A disagreement was resolved by whoever wrote it up.** That is the
  seat-failure-counted-as-agreement shape moved into the arbitration step: the loop's ruling
  and the loop's summary of the dispute are the same document, written by the same party.

### THE SHAPE OF THE PACKET

After pass 2, consolidate **every seat's findings** into one document and re-fire all nine:

1. **Number every finding** `F1..Fn`, attributing each to the seat(s) that raised it —
   including seats that reached it independently, because independent convergence is the one
   kind of agreement that IS evidence.
2. **State YOUR DISPOSITION on each** — accepted / rejected / refined — **and what you
   changed as a result.** A finding listed without a disposition is a finding nobody has to
   answer for.
3. **List DISAGREEMENTS separately as `D1..Dn`**, giving each side's argument in its own
   words, naming your ruling and its warrant. **Ask the parties to adjudicate their own
   dispute** — a seat that reconsiders and reverses is worth more than one that repeats.
4. **Say what is still OWED and where you might be fooling yourself.** The measured value of
   this section is high: it is where "the table has not run clean yet" and "this record is
   promissory" get written down instead of quietly aging.

### THE THREE QUESTIONS THE ADJUDICATION PASS ASKS

    1. Adjudicate F1..Fn and D1..Dn -- UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one
       line each with a reason.
    2. WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?  Name the count: "I have accepted ten
       findings in a row; that is a suspicious number and agreement is not evidence."
    3. WHAT DID ALL NINE OF US MISS?  You now have the whole panel's output.

**Question 2 is the load-bearing one** and it is why the disposition list must be honest
rather than tidy. A round that accepted everything has either had a very good panel or has
stopped arguing, and the packet cannot tell you which — a seat can.

### SELF-REVIEW IS DISCLOSED, AND ASKED TO BE HARDER

A seat adjudicating its own finding is doing self-review. **Say so in that seat's
invocation, and ask it to be harder on its own findings rather than softer** — and to check
that your FIX is right, not merely that its finding was. Those are different claims and the
second does not imply the first. The same applies to a ruling that ADOPTS a seat's position:
that seat should scrutinise the ruling more, not less, because a ruling in your favour is
the one you are least likely to test.

*This is the `A` conflict-of-interest badge the pipeline doctrine already mandates on
closures, applied one step earlier — to the adjudication rather than to the record.*

### WHAT IT COSTS, STATED PLAINLY

One extra nine-seat firing per round. That is real, and the honest counter-argument is that
pass 2 already produces the findings. **The answer is that pass 2 produces them in nine
separate documents that only one party ever reads together** — and this project's most
expensive recorded class, three times over, is a review that was written and never read.

## §F — BEFORE SENDING

* [ ] §C present, or an explicit "none carried"
* [ ] every citation is a grep anchor or a construct name
* [ ] every quote marked *verbatim* IS verbatim — condensed quotes labelled as condensed
      (*three seats in one day caught quotes labelled verbatim that were condensed; one made
      it a VERDICT LINE, because the source shown could not have produced the output quoted
      beside it*)
* [ ] state claims are TRUE as of sending — "shipped" means committed
      (*a brief claimed a round had shipped while its tree was dirty and its kill table still
      running; two seats caught it independently*)
* [ ] **PASS 2 ONLY — paste `git diff --numstat` for the round's files and mark each one
      INLINED / SUMMARIZED / NOT SHOWN, with the reason on the line.**

  > ### *** THIS IS THE ONE THE LAST THREE ROUNDS ALL MISSED, MEASURED 2026-08-29. ***
  >
  > A pass 2 is owed *on the round's own diff* — `regress/pass2_ledger.tsv`'s header says so,
  > and every receipt is keyed to the SHA of the commit reviewed.  **Three consecutive rounds
  > fired 9/9 on a brief that never named files their commit shipped:**
  >
  >     #488  09362f0   diff_diskimage_io.c +599, gate_offline.sh +42     brief mentions: 0
  >     #489  095aa96   gdrom_toclen_probe.py +427, gate_sh_rounding +64  brief mentions: 0
  >     #490  (pending) gdrom_default_probe.py +65, gate_sh_rounding +72  brief mentions: 0
  >
  > **A seat cannot flag a file it was never told exists.**  A packet-fed seat can name a
  > premise it needs and cannot settle — that is `§C2`'s measured case, and it happened again
  > on #490 — but omission is the one defect the consumer is *structurally blind* to.  That is
  > exactly the property the two checkers this project REJECTED did not have, and it is why
  > this one is worth having.
  >
  > **The item enforces DISCLOSURE, not inlining.**  A file marked `SUMMARIZED` or
  > `NOT SHOWN -- <reason>` passes; the harm is silent narrowing, not brevity.  The precedent
  > is the receipt that wrote *"this receipt says so rather than implying one"*.
  >
  > *And the temporal twin of this rule already existed and never generalised: `#480` adopted
  > "freeze a detector under panel review, or re-fire" after a 4-row skew in 87 — then three
  > rounds ran the SPATIAL version at far greater scale.  A rule earning its second and third
  > instance while sitting in a receipt note is this project's own structure-first trigger.*
* [ ] `bash -c 'wc -c <brief>'` — if a CLI seat will take it on argv, remember the ~32 KB
      Windows cap; `grok --prompt-file` is the seat immune to it
