# Reading task: hrec_constblind (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBHRECCONSTBLIND-7c8e` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one held harness row, `constblind` (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator; this fork keeps a
ledger of every filed issue, and a HARNESS row is about the project's own test tooling.  The row below is HELD with its
fix committed; its record is the commit message(s) and any CHANGELOG block shown.  A flagship review is still owed.  You
cannot read files, so judge the record AS WRITTEN.  Do not simply ratify it.  A bracketed dated note is this project's
in-place correction form (it quotes what it corrects); it is not by itself a contradiction.

## The ledger row `constblind` (state `held`)

**title:** constblind  Every differential that reads a #define for its expected value is blind to that #define

**state_note (head):** *** EVIDENCE 2026-08-27: TRUE IN PRINCIPLE, ALREADY LARGELY MITIGATED IN TREE, and HARNESS-ONLY. ***

The principle is sound and is a real vacuity class: **any assertion that reads a `#define` directly as its own expected value (`got == HEADER_MACRO`) is tautologically blind to a change in that macro.** Edit the header and both sides move together, so the row stays green while the constant it pins has changed underneath it.

**But the seat reports it is already largely mitigated in this tree**, and the exposure is **HARNESS-ONLY -- no guest can reach it.** So it is test-coverage debt rather than an emulator defect, and it ranks below every guest-reachable row.

**This is the same species as the anchor rule** the carrier already carries: a detector that tests the decode against ITSELF is invariant under an edit that moves both sides. There the remedy was an anchored row tied to a channel outside the thing under test; here it is a literal expected value rather than the macro. **Same shape, one level down.**

**DISPOSITION: keep open as harness debt, ranked low.** Not verified here how complete the mitigation is -- that is the one thing worth checking before it is closed.



*** 2026-09-13 CODEX RESEARCH (read-only, gpt-6-astra max): ROUND -- see regress/artifacts/codex_research_20260913/constblind.answer.md.  Premises it corrected are in the entry; the row stays HELD pending the named next step and the batched flagship close pass. ***

**hold_question:** Every differential that reads a `#define` for its EXPECTED value is blind to a change in that `#define`. The hold records a stale audit: it covered SEVEN differentials when there were THIRTEEN. QUESTION: how many are there NOW, and how many are blind? Count them rather than estimating. Then: is the fix per-differential (hardcode the expected value with a comment citing the define) or structural (a check that greps differentials for defines used as expectations)? The carrier's structure-first rule says propose the structural landing spot first and fall back to prose only if none exists.

## The record -- commit message(s)

### commit `af40df5a 2026-08-20`

```text
Five seats voted to drop constblind as "already fixed" -- and the live instance was mine, from hours earlier

The harness-integrity panel voted 5-0 to DROP `constblind` as already audited and
fixed.  minimax even named the closing commit.  The vote was WRONG, and how it was
wrong is worth more than the fix.

*** EVERY SEAT WAS READING THE SAME SENTENCE. ***  The row's own hold says
"AUDITED: diff_timer was the only one exposed; now fixed".  That audit covered
SEVEN differentials.  THERE ARE THIRTEEN NOW.  Six arrived after it, and one of
them is diff_rtc_range.c -- which I WROTE HOURS EARLIER IN THIS SESSION, and which
reads TIMER_MAX_FREQUENCY on the expected side of three rows.

MEASURED, and it is the whole constblind shape in one screen.  Changing
TIMER_MAX_FREQUENCY to 1073741823.0:

    ok    2^32: clamped to exactly TIMER_MAX_FREQUENCY   1073741823
    ok    bit31: clamped to exactly TIMER_MAX_FREQUENCY  1073741823
    ok    2^63: clamped to exactly TIMER_MAX_FREQUENCY   1073741823
    FAIL  ceiling IS INT_MAX, not merely some large literal   got 0 want 1

The three rows that READ the constant followed it and stayed GREEN.  Only an
absolute consequence derived from OUTSIDE the header noticed.  Fixed here exactly
as diff_timer.c:276-280 already does, named in the gate so deleting it is loud,
and negative-controlled both ways.  Gate 2 PASS at 259 checks, table 17 -> 18 rows.

*** A UNANIMOUS VERDICT DERIVED FROM ONE STALE RECORD IS ONE STALE RECORD, NOT
FIVE CONFIRMATIONS. ***  Five seats agreeing looks like strong evidence and was
worth exactly as much as the sentence they all read.  The three packet-fed seats
COULD NOT have checked it.  The two file-reading seats COULD have, and did not.
This is the clearest case yet for the standing rule that anything checkable in
under two minutes gets CHECKED rather than judged -- the check here was one grep,
and it overturned a 5-0 vote.

The row's stale hold is corrected in place, and what it actually needs is recorded:
a MECHANICAL check, because the differential count keeps moving and any re-audit
goes stale the next time one is added.

The panel's other dispositions, recorded: DROP `census` (five seats, and this one
HOLDS UP -- every seat called it policy rather than a defect); DROP-or-DOCUMENT
`xfamscope`; four-way split on what to do first (gateflr / pcheck / optrow).  No
drop executed -- all are codex-held and a drop is a closure.

Seats: 6 of 7.  Codex RATE-LIMITED, seventh panel today.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
```


## Questions -- verdict line first

1. Does the record contradict itself -- two numbers for one quantity, a total its parts do not sum to, a claim one
   paragraph makes and another undoes, or the ledger row saying something the commit message does not?  Quote both.
2. Which claims are stated as MEASURED but cite no artifact (a log, a file under regress/artifacts/)?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the record's own evidence covers less?
4. What would a reviewer checking this record against its artifacts most likely find wrong?
When you count items the record enumerates, list them by name before giving the count.

End with one line: `HARNESSREC_CONSTBLIND: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBHRECCONSTBLIND: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
