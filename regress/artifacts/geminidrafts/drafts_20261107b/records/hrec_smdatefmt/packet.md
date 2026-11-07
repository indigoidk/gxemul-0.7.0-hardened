# Reading task: hrec_smdatefmt (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBHRECSMDATEFMT-15d6` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one held harness row, `smdatefmt` (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator; this fork keeps a
ledger of every filed issue, and a HARNESS row is about the project's own test tooling.  The row below is HELD with its
fix committed; its record is the commit message(s) and any CHANGELOG block shown.  A flagship review is still owed.  You
cannot read files, so judge the record AS WRITTEN.  Do not simply ratify it.  A bracketed dated note is this project's
in-place correction form (it quotes what it corrects); it is not by itself a contradiction.

## The ledger row `smdatefmt` (state `held`)

**title:** smdatefmt  A malformed or absent SM_EXEMPT date NEVER expires, silently

**state_note (head):** *** EVIDENCE 2026-08-27: HISTORICALLY TRUE, CURRENTLY FIXED IN TREE, and NOT guest-reachable (test-harness only). Recommend CLOSE. ***

The row says a malformed or absent `SM_EXEMPT` date never expires, silently. The seat reports that this was true and **is fixed in the current tree**, and that the whole surface is harness-only -- no guest can reach it.

*** FOURTH INSTANCE TODAY of a row describing work that is already done *** -- with [[smnotland]], [[pitclobber]] and [[sh4chcr]]. See [[baretitle]]: the class is not under-reviewed, it is under-CLOSED.

*Not independently re-verified here beyond the seat's reading; it is harness code with no guest exposure, so the cost of being wrong is a stale row rather than a missed defect. Confirm the date handling before executing the close.*



**hold_question:** (none)

## The record -- commit message(s)

### commit `6e369434 2026-08-20`

```text
smdatefmt: a malformed exemption date never expired, in BOTH manifests

REPRODUCED TEST-FIRST against the shipped loop, copied byte-for-byte rather than
paraphrased -- a paraphrased reproduction proves something about the paraphrase.
Both controls green (a well-formed past date DID expire; a future one did not),
and then all four malformed forms silently never expired:

    ieee_store             no date at all
    ieee_store:            empty tail -- the ONE case the old loop handled
    ieee_store:2026-8-1    unpadded, NINETEEN DAYS PAST
    ieee_store:garbage     not a date

MECHANISM.  `${e##*:}` strips to the LAST colon -- with NO colon it strips nothing
and returns the whole entry, so `ieee_store` was compared as a date: 's' > '2',
false, unexpired.  The unpadded case is the nastiest and least obvious:
`2026-8-1` against `2026-08-20` matches through `2026-`, then compares '8' against
'0', so a date nineteen days PAST sorts as FUTURE.  And every malformed entry
still satisfied the COVERAGE check, which keys on the stem -- so the exemption was
honoured throughout.  The exempt arm's teeth depended on a format NOTHING
VALIDATED.

*** BOTH MANIFESTS CARRIED THE IDENTICAL LOOP, a few hundred lines apart. ***
SM_EXEMPT at :1036 and SC_EXEMPT at :1679.  Fixing one would have left the other
-- this project's "grep for the siblings before calling it fixed" rule, written
after an "un-fakeable" claim was corrected in one place and survived in three.
One helper serves both: same file, same semantic class, one fix design, same
oracle, so they travel together under the reopening rule.

IT REFUSES RATHER THAN GUESSES.  A malformed entry is RED and NAMES ITSELF --
`ieee_store(NO-DATE)`, `wdc_identify(BAD-DATE:2026-8-1)` -- never silently
unexpired.  A `case` glob rather than a regex, because this runs under POSIX sh
and needs no external process.

NEGATIVE-CONTROLLED with the helper EXTRACTED FROM THE GATE rather than retyped:
all four malformed forms name themselves, both controls still behave, and -- the
check that actually matters for a repair -- THE LIVE MANIFESTS ARE STILL GREEN
(SM_EXEMPT -> none, SC_EXEMPT -> none).  A fix that reddens the real gate is a
regression, not a repair.

Gate 2 PASS at 259 checks.  Closure held behind codex (Aug 22), like every other
row tonight.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
```


## Questions -- verdict line first

1. Does the record contradict itself -- two numbers for one quantity, a total its parts do not sum to, a claim one
   paragraph makes and another undoes, or the ledger row saying something the commit message does not?  Quote both.
2. Which claims are stated as MEASURED but cite no artifact (a log, a file under regress/artifacts/)?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the record's own evidence covers less?
4. What would a reviewer checking this record against its artifacts most likely find wrong?
When you count items the record enumerates, list them by name before giving the count.

End with one line: `HARNESSREC_SMDATEFMT: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBHRECSMDATEFMT: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
