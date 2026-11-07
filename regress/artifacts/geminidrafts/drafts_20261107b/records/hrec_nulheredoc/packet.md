# Reading task: hrec_nulheredoc (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBHRECNULHEREDOC-acd9` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one held harness row, `nulheredoc` (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator; this fork keeps a
ledger of every filed issue, and a HARNESS row is about the project's own test tooling.  The row below is HELD with its
fix committed; its record is the commit message(s) and any CHANGELOG block shown.  A flagship review is still owed.  You
cannot read files, so judge the record AS WRITTEN.  Do not simply ratify it.  A bracketed dated note is this project's
in-place correction form (it quotes what it corrects); it is not by itself a contradiction.

## The ledger row `nulheredoc` (state `held`)

**title:** nulheredoc  A shell heredoc wrote three literal NUL bytes into two tracked text files, silently turning every grep against them binary

**state_note (head):** *** SYMPTOM ABSENT, CAUSE NOW GUARDED, 2026-08-27 -- and I reproduced the defect by accident while building the guard, which is the best evidence the guard is worth having. ***

**The row:** a shell heredoc wrote three literal NUL bytes into two tracked text files, *silently turning every grep against them binary*. The damage is not the bytes -- it is that grep then reports NOTHING, and nearly every gate in this tree is grep-based.

**Current state: 0 NUL bytes across 672 tracked text files**, measured with `tr -cd`.

*** MY FIRST MEASUREMENT OF THAT WAS INERT AND I REPORTED IT AS A RESULT. *** I scanned 1161 tracked files with `LC_ALL=C grep -qP` and got 0 hits. **grep REFUSES to run `-P` under `LC_ALL=C`** -- *"supports only unibyte and UTF-8 locales"* -- so it never ran, and with `-q` and `2>/dev/null` the refusal was invisible. **0 of 1161 was a check that could not fail.** The honest figure is 0 of 672, by a method with no regex engine in it.

*** AND THE FIRST VERSION OF THE GUARD WROTE A NUL INTO ITSELF. *** Writing `\\x00` through a Bash -> heredoc -> Python path lost one backslash level, exactly as the carrier documents, so Python emitted byte 0x00 into `precommit_check.sh` -- **reproducing this row's own mechanism inside the check meant to catch it**, and ordinary grep immediately called the script binary. That is how the inert `-P` was found at all.

**THE GUARD, and why it is shaped this way:** `precommit_check.sh` section Y uses **`tr -cd`, not grep** -- no regex engine, no `-P`, no locale dependency, and no backslash that has to survive a quoting layer. It carries a ZERO-DENOMINATOR guard (if the `ls-files` pattern selects nothing it FAILS loudly rather than reporting clean), and it is scoped to text extensions on purpose: a future tracked `.pdf` or `.png`

**hold_question:** (none)

## The record -- commit message(s)

### commit `25da4045 2026-08-27`

```text
precommit Y: guard tracked text files against NUL bytes

A shell heredoc once wrote three literal NUL bytes into two tracked text
files.  The damage is not the bytes -- grep then treats the file as binary and
silently stops reporting matches, and nearly every gate here is grep-based, so
one NUL can hollow out a whole gate while every row still reads green.

The symptom is currently absent: zero NUL bytes across 672 tracked text files.
No fix commit was ever recorded on that row, so the original bytes went away
in unrelated edits -- which is exactly why a guard is worth more than a
cleanup.

I WROTE THIS CHECK WRONG TWICE, AND BOTH FAILURES ARE NOW COMMENTS IN IT.

The first version used grep with a perl pattern under a C locale.  Grep
REFUSES to run that combination -- it says so, on stderr -- and with quiet
mode and stderr discarded the refusal is invisible, so every file reported
clean.  A check that cannot fail, built inside a checker.  The same mistake
had already made an earlier census inert: I scanned eleven hundred files, got
zero hits, and reported it as a measurement when grep had never run.

The second failure was worse and funnier.  Writing that pattern through a
heredoc lost one backslash level, so the escape became an actual NUL byte in
the script -- reproducing this row's exact mechanism inside the check meant to
catch it.  Ordinary grep immediately called precommit_check.sh binary, which
is how the first failure got noticed at all.

So the shipped check uses tr rather than grep: no regex engine, no perl mode,
no locale dependency, and no backslash that has to survive a quoting layer.
It carries a zero-denominator guard -- if the file pattern selects nothing it
fails loudly instead of reporting clean -- and it is scoped to text extensions
on purpose, because a future tracked pdf or png carries NULs legitimately and
a check that has to be switched off is worse than no check.

Negative-controlled both directions before landing, which is mandatory for a
change to the script every commit runs: injecting one NUL into a tracked
markdown file turns it red and names the file; restoring turns it green at six
hundred and seventy-two files.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
```


## Questions -- verdict line first

1. Does the record contradict itself -- two numbers for one quantity, a total its parts do not sum to, a claim one
   paragraph makes and another undoes, or the ledger row saying something the commit message does not?  Quote both.
2. Which claims are stated as MEASURED but cite no artifact (a log, a file under regress/artifacts/)?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the record's own evidence covers less?
4. What would a reviewer checking this record against its artifacts most likely find wrong?
When you count items the record enumerates, list them by name before giving the count.

End with one line: `HARNESSREC_NULHEREDOC: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBHRECNULHEREDOC: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
