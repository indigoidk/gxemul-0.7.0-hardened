# Reading task: closedraft_09 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBCLOSE09-da68` on a line of its own.

# GXemul hardened fork -- DRAFT THE CLOSURE RECORDS for 6 filed issues proposed for closing (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier triage pass proposed closing each row below.  Closing must be HONEST: a row closed
as documented says what was assessed and not changed; a dropped row says why it is not a defect worth a round; a row closed
as OVERTAKEN (someone else's fix removed the defect) is only closable on three conditions -- (1) a discriminating control,
measured at HEAD: neutralise the overtaking fix and this row's own symptom comes back; (2) the rows that now carry the
coverage named; (3) that control preserved at a durable path.  You cannot read files; work from the text.  Ledger at HEAD 8d9df658.

## The rows

### ROW `agentmodelwall` -- state `open`, severity `med`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** a MODEL wall on the Agent tool is not a TRANSPORT outage: subagents on sonnet ran normally while opus and fable were both walled, and the carrier's shared-service note does not distinguish the two

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** establishes an operational rule for tool usage, not a code defect.

### ROW `wdcaddr2` -- state `open`, severity `LOW`; PROPOSED: **DROP**

**title:** dev_wdc.c: the aux-register address is keyed on machine_type; `devinit->addr2' (device.h, parsed at device.c:320) already exists and would declare it per machine INSTANCE, removing the second-wdc-on-landisk hazard

**state_note (head):** 

**hold_question:** No measured delta today, so the addition licence does not license it.  Reopen if the PCIIDE TODO at machine_landisk.c:41 ever lands (a second wdc on landisk).

**the triage pass's reason:** no measured delta today, so the addition licence does not license it.

### ROW `wdcrowpin` -- state `open`, severity `LOW`; PROPOSED: **CLOSE-OVERTAKEN**

**title:** gate 2 pins diff_wdc_identify.c's row count only as >= 42, so deleting the identity row AND an INLINE row is green (a composite that pre-dates #551; since #551e the LAST self-check's call counts catch a deleted COVERED row)

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** #551e already catches deleted covered rows via call counts

### ROW `wdcverdictone` -- state `open`, severity `LOW`; PROPOSED: **CLOSE-OVERTAKEN**

**title:** gate 2 accepts a wdc log carrying BOTH WDC_IDENTIFY_PASS and WDC_IDENTIFY_FAIL; since #551f a covered failure's report reds the count check anyway -- defence in depth for the inline rows

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** #551f reds the count check anyway

### ROW `armcpabsent` -- state `open`, severity `MED`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** MRC or MCR to an uninstalled ARM coprocessor fatals and falls through, with Undefined Instruction delivery still commented out; CDP already delivers Undefined Instruction

**state_note (head):** AN ID FOR AN EXISTING PROSE ENTRY of OUTSTANDING_BUGS.md (lines 18709-18713 at db8b1a33) -- no second entry is opened.  Where the text comes from: grok/grok_irule_a.txt A10 (conceding Astra's ifile_01 finding)

**hold_question:** (none)

**the triage pass's reason:** existing prose entry requires no second tracker.

### ROW `armdwordalign` -- state `open`, severity `MED`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** OUTSTANDING_BUGS.md:5140-5144 at db8b1a33 -- (task #74) LDRD/STRD mask the address with ~7 where ARMv6 with U=1 permits word alignment and accesses address and address+4

**state_note (head):** AN ID FOR AN EXISTING PROSE ENTRY of OUTSTANDING_BUGS.md -- no second entry is opened.  GOVERNING TEXT (from the dispositions file, cut at 400 characters): (added by the review pass)  [Astra afile_01, D:779]

**hold_question:** (none)

**the triage pass's reason:** existing prose entry requires no second tracker.

## For EACH row return (a numbered block per row, its id first)

1. `AGREE` or `DISAGREE` with the proposed closure, and why in one line -- DISAGREE when the row's own text describes a live,
   reachable defect, or names work still owed.
2. If AGREE: the closure RECORD text, two to four lines, in that honest form (for OVERTAKEN: the control that would
   discriminate and the rows that would carry it, stated as OWED, never as done).
3. The ONE fact that would make closing wrong -- what someone must check before closing it.
Do not invent commits, measurements or file contents the text does not give.

End with one line: `CLOSEDRAFT_09: <a> AGREE, <d> DISAGREE`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBCLOSE09: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
