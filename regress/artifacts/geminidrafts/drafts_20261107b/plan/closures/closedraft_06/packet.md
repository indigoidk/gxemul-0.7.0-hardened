# Reading task: closedraft_06 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBCLOSE06-c84f` on a line of its own.

# GXemul hardened fork -- DRAFT THE CLOSURE RECORDS for 6 filed issues proposed for closing (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier triage pass proposed closing each row below.  Closing must be HONEST: a row closed
as documented says what was assessed and not changed; a dropped row says why it is not a defect worth a round; a row closed
as OVERTAKEN (someone else's fix removed the defect) is only closable on three conditions -- (1) a discriminating control,
measured at HEAD: neutralise the overtaking fix and this row's own symptom comes back; (2) the rows that now carry the
coverage named; (3) that control preserved at a durable path.  You cannot read files; work from the text.  Ledger at HEAD 8d9df658.

## The rows

### ROW `exitcensus` -- state `open`, severity `med`; PROPOSED: **DROP**

**title:** exit_census.py's BY-ENCLOSING-CONSTRUCT split attributed every call in a plain non-static function to the preceding DEVICE_ACCESS -- inflating the bucket used to rank reachability

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** The original tool was correctly restored and per-function attribution is deliberately rejected.

### ROW `exit0oracle` -- state `open`, severity `med`; PROPOSED: **DROP**

**title:** shipped rows pin survival as an `exit0` want, so a mutant that announces and then exit(0)s satisfies them -- count DERIVED, never restated: grep -h 'row(.*"exit0"' regress/*.py | wc -l

**state_note (head):** *** THE CLASS IS NOT A PREDICTION -- IT HAS A MEASURED TOTAL ESCAPE, AND THE PROBE THAT MEASURED IT
ALSO SHIPS THE REPAIR.  Read out of the source 2026-09-08, not reasoned. ***

`regress/sgi_re_unmapped_probe.py` records it in its own comments:

    E0   exit(0) after the whole catch-all, BOTH directions   47/48
    E0W  exit(0) in the WRITE arm only                        48/48  *** TOTAL ESCAPE ***

and gives the reason, which is the class in one sentence: *"a `surv' row wants "exit0", and a clean
`exit(0)' IS exit status 0, so the oracle is SATISFIED by the very thing it should catch; a `decl'
row counts the message, which was already printed before the exit.  The two together therefore
pass."*  **E0 was caught by exactly one row and only INCIDENTALLY** -- that row makes two accesses,
so it notices the second one never happening.

*** THE IN-TREE REPAIR IDIOM, which answers the "is there a probe that does this well" question:
A POST-STORE POSITIVE OBSERVABLE. ***  Seed RAM, perform the declined device access, then read the
seed back -- *"if the host quit at the write, the load never runs and `printed()' returns "absent",
which is not the datum."*  `#499` added two such rows, deliberately covering BOTH components,
because a write-side `exit(0)` conditioned on one component is the asymmetry that round *"has now
been bitten by three times"*.

*** THE OPEN QUESTION IS WHETHER TH [... 8210 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** the relevant file is on the never-commit list, so the finding is recorded but unactionable.

### ROW `gxprobepccache` -- state `open`, severity `med`; PROPOSED: **CLOSE-OVERTAKEN**

**title:** gxprobe cached the pc across `step`, so a driver that stepped without _exec_at() had its next pc assignment silently skipped -- a detector row that could not fail

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** fixed at source in send(), but must check if gxprobe.py is tracked.

### ROW `pcc2pscaleflood` -- state `open`, severity `med`; PROPOSED: **DROP**

**title:** pcc2pscaleflood  dev_pcc2.c: PSCALEADJ's write-side fatal() is unlatched and guest-drivable -- one of nine such prints (see pcc2huhflood)

**state_note (head):** Filed by the Opus seat on pass 3 while verifying something else.  floodclass member.  Filed in OUTSTANDING_BUGS.md (dated tail, `### pcc2pscaleflood`, line 14668 as of 2026-09-04); this row added 2026-09-04 so the dashboard shows it -- the bug file had it, the ledger did not.  FOLD (2026-09-04 fix review, both seats): into ONE floodclass round with pcc2huhflood (+ pcc2assertflood as the lowest); keep provenance, close as duplicate when the nine-site latch lands.

**hold_question:** (none)

**the triage pass's reason:** explicitly marked to close as duplicate of pcc2huhflood's nine-site latch

### ROW `wdcwidthmatrix` -- state `open`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** wdcwidthmatrix  the #475 detector covers access widths 4 and 2; the full width x remainder matrix and exact-fit controls are not shipped

**state_note (head):** Filed from the `#475` pass-1 panel.  The codex seat recommended a matrix over consumption
widths {2,4} at remainders {1} and {1,2,3} respectively, plus EXACT-FIT controls.

**Shipped: width 4 at remainders 3 and 1-of-37, and width 2 at remainder 1.**  That is what
was needed to kill the two measured escapes.  Not shipped: one-byte reads, exact-fit
controls, and the remaining cells.

**COMPLETENESS, NOT A LIVE HOLE, and the reason is arithmetic:** `consumed` is 1 for a
one-byte read, and a remainder is at least 1 whenever the arm is live, so a one-byte read
CANNOT step past zero.  The two widths that can overshoot are both covered.

*Worth one row if the fix is ever touched again -- and worth remembering that the width axis
was invisible until a seat named it: every row in that file used a four-byte read, so a clamp
narrowed to `len == 4` swept the whole table.*

**hold_question:** (none)

**the triage pass's reason:** text confirms completeness, not a live hole, reason is arithmetic.

### ROW `m88kexctaildefault` -- state `open`, severity `low`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** m88kexctaildefault  DESIGN OPTION RECORD (D4 of #502, named by the pass-1 panel and NOT adopted): make m88k_exception()'s tail `default:' deliver every vector below 128 instead of stopping the cpu

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** the issue explicitly states it is documented-only and the design option was deliberately not adopted due to blast radius.

## For EACH row return (a numbered block per row, its id first)

1. `AGREE` or `DISAGREE` with the proposed closure, and why in one line -- DISAGREE when the row's own text describes a live,
   reachable defect, or names work still owed.
2. If AGREE: the closure RECORD text, two to four lines, in that honest form (for OVERTAKEN: the control that would
   discriminate and the rows that would carry it, stated as OWED, never as done).
3. The ONE fact that would make closing wrong -- what someone must check before closing it.
Do not invent commits, measurements or file contents the text does not give.

End with one line: `CLOSEDRAFT_06: <a> AGREE, <d> DISAGREE`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBCLOSE06: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
