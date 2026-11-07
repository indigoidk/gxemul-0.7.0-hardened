# Reading task: closedraft_07 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBCLOSE07-7052` on a line of its own.

# GXemul hardened fork -- DRAFT THE CLOSURE RECORDS for 6 filed issues proposed for closing (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier triage pass proposed closing each row below.  Closing must be HONEST: a row closed
as documented says what was assessed and not changed; a dropped row says why it is not a defect worth a round; a row closed
as OVERTAKEN (someone else's fix removed the defect) is only closable on three conditions -- (1) a discriminating control,
measured at HEAD: neutralise the overtaking fix and this row's own symptom comes back; (2) the rows that now carry the
coverage named; (3) that control preserved at a durable path.  You cannot read files; work from the text.  Ledger at HEAD 8d9df658.

## The rows

### ROW `m88ksfrzfatal` -- state `open`, severity `low`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** m88ksfrzfatal  cpu_m88k.c m88k_exception(): the SFRZ re-route's `fatal("[ SFRZ already set in PSR => ERROR ]")' is an UNLATCHED guest-drivable diagnostic (supervisor-only: any non-trap fault inside a handler) -- a floodclass instance, reachable by five more classes since #502 (BOUNDS and ERROR are trap-only and bypass the branch; this title said seven until codex, pass 5)

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** the text asserts this is not a correctness defect and merely documents a floodclass instance.

### ROW `cxseatcheck` -- state `open`, severity `med`; PROPOSED: **CLOSE-OVERTAKEN**

**title:** tools/cxlaunch.sh: a codex seat check that could report a REFUSED seat as a clean run, and a wall-grep over stderr that matched the project's own ledger text

**state_note (head):** [2026-09-19 06:2x] #544 IN WORK (e8a2bc): the fix is drafted with 20 launcher controls and a 38-row / 21-variant tally self-test; pass 2 in flight on panel_20260919_060945.  Built 2026-09-07 after the `lcaconfwidth` census was REFUSED by codex's content filter and my
launcher reported it as a completed run.  **Three defects, all mine, all found within an hour of
each other, and all of one family: a check that answers the same whether or not the thing it tests
is true.**

1. **The refusal check read the wrong stream.**  A content-filter refusal writes NOTHING to stdout
   and puts `ERROR: This content was flagged for possible cybersecurity risk.` on STDERR.  The check
   grepped stdout and printed `refusal hits: 0` on a refusal that had already destroyed 108,432
   tokens of completed work.
2. **The script exited 0 while holding `rc=1`.**  It captured codex's status, printed it, and ended
   on a successful command, so the harness reported the task COMPLETED.  Failure laundered into a
   clean completion -- the fourth instance of that class recorded here.
3. **The FIX introduced a third defect, measured on its first real run.**  Grepping stderr freely
   for wall text reported `wall: 3` on a HEALTHY seat, because **codex streams the source it reads
   into stderr** -- and all three hits were this project's own ledger prose about seat walls, one of
   them the line *"whose quotat [... 3698 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** Defect is being addressed in #544 (e8a2bc).

### ROW `dec21143deadclamp` -- state `open`, severity `low`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** three unreachable size guards and one always-true test in dev_dec21143.c -- bufsize is bounded to 0..2047 by its own masks

**state_note (head):** Filed 2026-09-07.  Full record in OUTSTANDING_BUGS.md under the same id.

*** THIS ROW EXISTS BECAUSE THE LEDGER<->BUGFILE SYNC IS ONE-DIRECTIONAL AND ITS WARRANT HAS DECAYED -- see [[bugfilereverse]].  It was filed into OUTSTANDING_BUGS and given no ledger row, which is precisely the failure check_bugfile_sync.py was written to stop, in the direction it does not check. ***

**hold_question:** (none)

**the triage pass's reason:** Evidence shows guards are mathematically unreachable.

### ROW `gdrommappedvacuous` -- state `open`, severity `med`; PROPOSED: **DROP**

**title:** four `gdrom map' controls convert any 0x... print to "mapped", so the memory fallback's zero-filled read satisfies them

**state_note (head):** Filed 2026-09-07.  Full record in OUTSTANDING_BUGS.md under the same id.

*** THIS ROW EXISTS BECAUSE THE LEDGER<->BUGFILE SYNC IS ONE-DIRECTIONAL AND ITS WARRANT HAS DECAYED -- see [[bugfilereverse]].  It was filed into OUTSTANDING_BUGS and given no ledger row, which is precisely the failure check_bugfile_sync.py was written to stop, in the direction it does not check. ***

**hold_question:** (none)

**the triage pass's reason:** already filed in OUTSTANDING_BUGS.md and warrant for this row has decayed

### ROW `mtesrcdup` -- state `open`, severity `low`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** do_mte_transfer computes the same source-TLB expression twice under two names (`src` and `src_tlb`)

**state_note (head):** Noticed 2026-09-07 while verifying that `sgi_mte_fill_probe.py`'s mode clears the pre-switch guards.

    :1312  int src     = (mode & MTE_MODE_SRC_BUF_MASK) >> MTE_SRC_TLB_SHIFT;
    :1333  int src_tlb = (mode & MTE_MODE_SRC_BUF_MASK) >> MTE_SRC_TLB_SHIFT;

**Byte-identical expressions.**  `src` guards `:1336 if (src > MTE_TLB_C)`; `src_tlb` builds
`src_mode` at `:1365`.  They cannot disagree today, so this is **not a defect** -- recorded because
the two-names-for-one-value shape is exactly what `#508` found in `memory_alpha.c`
(`ALPHA_PAGESHIFT` and a local `pageSizeShift` both meaning 13), where the hazard is that a later
edit changes one and not the other.

*The read that found it was checking something else: `:1336` tests `src`, not the `src_tlb` computed
one line above, which LOOKS like a variable mix-up until you find the earlier declaration.  That
momentary alarm is the actual cost of the duplication.*

Documented-only unless a round is already editing that function.

**hold_question:** (none)

**the triage pass's reason:** text states it is not a defect and is documented-only unless already editing

### ROW `negrowclass` -- state `open`, severity `med`; PROPOSED: **DROP**

**title:** an inequality row scores every NON-OBSERVATION green -- five ungated instances repaired and measured, two GATED ones still open

**state_note (head):** Filed 2026-09-07.  Full record in OUTSTANDING_BUGS.md under the same id.

*** THIS ROW EXISTS BECAUSE THE LEDGER<->BUGFILE SYNC IS ONE-DIRECTIONAL AND ITS WARRANT HAS DECAYED -- see [[bugfilereverse]].  It was filed into OUTSTANDING_BUGS and given no ledger row, which is precisely the failure check_bugfile_sync.py was written to stop, in the direction it does not check. ***

**hold_question:** (none)

**the triage pass's reason:** warrant has decayed and it is tracked in OUTSTANDING_BUGS.md

## For EACH row return (a numbered block per row, its id first)

1. `AGREE` or `DISAGREE` with the proposed closure, and why in one line -- DISAGREE when the row's own text describes a live,
   reachable defect, or names work still owed.
2. If AGREE: the closure RECORD text, two to four lines, in that honest form (for OVERTAKEN: the control that would
   discriminate and the rows that would carry it, stated as OWED, never as done).
3. The ONE fact that would make closing wrong -- what someone must check before closing it.
Do not invent commits, measurements or file contents the text does not give.

End with one line: `CLOSEDRAFT_07: <a> AGREE, <d> DISAGREE`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBCLOSE07: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
