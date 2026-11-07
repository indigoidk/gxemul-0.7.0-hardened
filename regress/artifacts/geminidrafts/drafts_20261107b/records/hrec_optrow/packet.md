# Reading task: hrec_optrow (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBHRECOPTROW-d88c` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one held harness row, `optrow` (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator; this fork keeps a
ledger of every filed issue, and a HARNESS row is about the project's own test tooling.  The row below is HELD with its
fix committed; its record is the commit message(s) and any CHANGELOG block shown.  A flagship review is still owed.  You
cannot read files, so judge the record AS WRITTEN.  Do not simply ratify it.  A bracketed dated note is this project's
in-place correction form (it quotes what it corrects); it is not by itself a contradiction.

## The ledger row `optrow` (state `held`)

**title:** optrow  Any row measuring a RESOURCE is only as good as the optimisation it pins

**state_note (head):** 

**hold_question:** (none)

## The record -- commit message(s)

### commit `fd0ddefb 2026-08-20`

```text
optrow: the audit is done, its answer is "one", and it is now mechanised because audits expire

The row asked for an AUDIT of every differential that measures a resource, after
diff_memory_rw.c asserted "the split is a loop, not recursion" by measuring stack
growth -- and gcc 15.2.1 eliminated the tail call at -O2, so the recursion mutant
measured 96 bytes and THE ROW PASSED UNDER THE EXACT DEFECT IT EXISTED TO CATCH.
One flag makes it real: loop 0 bytes, recursion 1,572,768.

THE AUDIT'S ANSWER IS "memory_rw IS THE ONLY ONE".  Four other differentials
mention "stack" and every mention is PROSE -- the SUBJECT's stack use, an argument
that must not be a stack array, a reference to #410's reasoning, the phrase
"defence-in-depth".  None measures a resource.  Comments are stripped before
matching, so prose cannot masquerade as a measurement.

*** BUT AN AUDIT IS A CLAIM WITH A SHELF LIFE, AND THIS ROW'S SIBLING PROVED IT
THE SAME DAY. ***  constblind's audit covered SEVEN differentials; there are
THIRTEEN, and five seats voted to DROP that row on its stale audit sentence while
a live instance sat in a file added hours earlier.  So the audit is recorded and
then MECHANISED: check_optpin.py, precommit section N, HARD because the baseline
is clean -- exactly one differential measures stack and it is pinned.

IT REPORTS ITS OWN BLINDNESS ON EVERY RUN, which is the honest half.  It knows the
STACK-WATERMARK idiom only -- a static uintptr_t pair fed by the address of a
local.  An allocation counter, an iteration count, a timing loop, or a future
stack idiom would all slip past.  A green line means "no UNPINNED file uses the
shape that has actually bitten", NEVER "no row follows the compiler".  That
distinction is this project's newest named vacuity class, so it is printed rather
than buried.

NEGATIVE-CONTROLLED THREE WAYS: baseline green; the pin stripped -> RED naming
memory_rw; a new stack-measuring differential with no compile line -> RED naming
it.

*** THE SECOND CONTROL WAS VOID ON ITS FIRST RUN AND SAID SO. ***  A sed with a
LEADING SPACE removed 4 of 5 pin occurrences and left the fifth -- the
selfmutant_one line, where the flag is QUOTE-delimited -- so the checker's own
fallback found it and reported PASS.  That looked exactly like a detector failure
and was an injection failure.  Asserting the mutation LANDED is the only thing
that separated them, and it is the fifth void control this session caught the same
way.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
```


## Questions -- verdict line first

1. Does the record contradict itself -- two numbers for one quantity, a total its parts do not sum to, a claim one
   paragraph makes and another undoes, or the ledger row saying something the commit message does not?  Quote both.
2. Which claims are stated as MEASURED but cite no artifact (a log, a file under regress/artifacts/)?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the record's own evidence covers less?
4. What would a reviewer checking this record against its artifacts most likely find wrong?
When you count items the record enumerates, list them by name before giving the count.

End with one line: `HARNESSREC_OPTROW: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBHRECOPTROW: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
