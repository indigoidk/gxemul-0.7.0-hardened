# Reading task: oldrec424 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC424-3ce1` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #424 b1w (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 31553-31615 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
31553| ## R2 (#424) — the parser selftest ran nowhere, and could not see a mutant that moves text
31554| `regress/selftest_absorb.py` shipped in r421 to test the pty record parser and was invoked by NO
31555| GATE: dead coverage. The deeper defect was in its shape. Its helper returned `body + tail` and 27 of
31556| its 29 rows compared that SUM, so **any mutant that merely RELOCATES text between the two halves
31557| preserved the sum and stayed invisible** — including one that leaves a completed line in the tail,
31558| where the boot loop never looks, so a guest that reached its milestone is reported as not reaching
31559| it. Nine review seats assessed and researched the round; a measured census settled it.
31560| 
31561| **THE CENSUS CAME FIRST, IN RESEARCH, NOT AFTER THE FIX.** 22 mutants across the parser's decision
31562| axes — the three hold clauses, which string the hold is taken from, the bound, the record regex, the
31563| strip loop, the return — each applied to a COPY with its substitution asserted to apply EXACTLY
31564| ONCE. Against the SHIPPED selftest: **17 killed, 5 SURVIVED, 0 faults**, and every survivor was
31565| non-equivalent with an executed witness, so none could be retired as equivalent. Naming them, which
31566| is the point: the newline clause (marker unreachable); the `i != -1` guard (a bracket-free read
31567| holds its last character for ever); `<` → `<=` at the bound (the existing row used 400, far past the
31568| shipped 256, so the boundary was never tested); `rest.rfind` → `tail.rfind` (a second record leaks
31569| unstripped at one cut); and the ` instrs` literal (a look-alike line is eaten and a count INVENTED).
31570| 
31571| **The fix is two invariants and four edges, and it needed both.** The panel split: one seat wanted
31572| rows added and the 27 sum rows left alone (rewrite = churn); another wanted every newline-terminated
31573| row converted so the blind idiom stops existing. Settled by execution — a probe walked every cut
31574| point of eleven streams, 2,575 parser steps, against the shipped parser: zero violations of either
31575| proposed invariant, so the conversion is safe and the objection was about diff size, not
31576| correctness. Both are adopted, because the invariants catch the CLASS but do not kill the edges: the
31577| bound mutant still satisfies the length test, and the regex-literal mutant never touches the tail at
31578| all.
31579| - **I2, the hold shape**, checked inside `feed()` after EVERY step and reported as one row with its
31580|   step count (685 today): the tail is empty, or a `[`-headed, newline-free run shorter than the
31581|   bound. This is the parser's own guard restated as a postcondition, so it applies to all the
31582|   file's existing calls including the offset sweeps.
31583| - **I3, finality**: an input whose concatenation ends in a newline must leave the tail EMPTY. Every
31584|   newline-terminated row now pins the pair instead of the sum, and the sum idiom is gone from the
31585|   file.
31586| - **Section K**, the edges the census named: the hold bound AT 254/255 rather than near it; a
31587|   bracket-free read holding nothing; a multi-record split sweep pinning body, tail and count
31588|   separately at every offset; and the regex literal (`[ 100 frobs; p]` must not parse).
31589| 
31590| **Result, measured: 52 rows, and the census now reports 22 of 22 killed, 0 survived, 0 faults.**
31591| 
31592| **`regress/absorb_census.py` is COMMITTED, because a detector's worth is what it kills and that must
31593| be re-runnable by someone who was not here.** It carries the mutant table and enforces THE
31594| DENOMINATOR RULE, which exists because the record once said "10/10 parser mutants killed" over a
31595| census in which five of twenty-two survived: the header prints the identity `attempted = killed +
31596| survived + faults` and the program EXITS NONZERO if it does not hold; every survivor is NAMED with a
31597| disposition from a closed vocabulary; "Survivors: none" prints even when empty; A CRASH IS A FAULT,
31598| NEVER A DETECTION; a substitution that does not apply exactly once is a FAULT, not a survivor. The
31599| repository is never mutated — copies only, which is what the `.MUTANT` history is for.
31600| 
31601| **Wired into gate 2 BEFORE the compiler check**, since the selftest needs only python3 and a machine
31602| without `cc` must not silently lose parser coverage as well as the differentials. **The positive
31603| control is the named survivor mutant itself**, applied to copies: it proves THE ROW KILLS THE
31604| MUTANT, where an in-process wrong-expectation row would only prove the reporter can still print
31605| FAIL. Its rows separate three states — never ran, ran and crashed, ran and caught — because exit
31606| status alone cannot tell a crash from a catch.
31607| 
31608| **One row was written too tight and the gate caught it**: the control asserted the kill came from
31609| exactly ONE named row, but the mutant strands every bracket-carrying line and fails all three. It is
31610| now a floor, with the reason recorded — pinning the exact number would turn a legitimately added row
31611| into a red gate.
31612| 
31613| **Verified:** gate 2 PASS, 131 checks (was 122); selftest 52 rows / 0 failures on the shipped
31614| parser; census 22/22 with the identity self-check green; `bash -n` clean.
31615| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_424: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC424: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
