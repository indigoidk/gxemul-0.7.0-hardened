# Reading task: closedraft_08 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBCLOSE08-97cc` on a line of its own.

# GXemul hardened fork -- DRAFT THE CLOSURE RECORDS for 6 filed issues proposed for closing (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier triage pass proposed closing each row below.  Closing must be HONEST: a row closed
as documented says what was assessed and not changed; a dropped row says why it is not a defect worth a round; a row closed
as OVERTAKEN (someone else's fix removed the defect) is only closable on three conditions -- (1) a discriminating control,
measured at HEAD: neutralise the overtaking fix and this row's own symptom comes back; (2) the rows that now carry the
coverage named; (3) that control preserved at a durable path.  You cannot read files; work from the text.  Ledger at HEAD 8d9df658.

## The rows

### ROW `printedvariants` -- state `open`, severity `low`; PROPOSED: **DROP**

**title:** 20 copies of printed() with FOUR different contracts, and two of them document their normalisation as matching a helper that does not mask

**state_note (head):** Filed 2026-09-07.  Full record in OUTSTANDING_BUGS.md under the same id.

*** THIS ROW EXISTS BECAUSE THE LEDGER<->BUGFILE SYNC IS ONE-DIRECTIONAL AND ITS WARRANT HAS DECAYED -- see [[bugfilereverse]].  It was filed into OUTSTANDING_BUGS and given no ledger row, which is precisely the failure check_bugfile_sync.py was written to stop, in the direction it does not check. ***

**hold_question:** (none)

**the triage pass's reason:** warrant has decayed and it is tracked in OUTSTANDING_BUGS.md

### ROW `probeneedleterm` -- state `open`, severity `med`; PROPOSED: **DROP**

**title:** unterminated needles accept longer numbers -- pcc2_default, sh4_val V22, m88k_exc captures

**state_note (head):** Filed 2026-09-07.  Full record in OUTSTANDING_BUGS.md under the same id.

*** THIS ROW EXISTS BECAUSE THE LEDGER<->BUGFILE SYNC IS ONE-DIRECTIONAL AND ITS WARRANT HAS DECAYED -- see [[bugfilereverse]].  It was filed into OUTSTANDING_BUGS and given no ledger row, which is precisely the failure check_bugfile_sync.py was written to stop, in the direction it does not check. ***

**hold_question:** (none)

**the triage pass's reason:** Row is a sync artifact with a decayed warrant that already exists in the bug file.

### ROW `ubsanshiftlane` -- state `open`, severity `med`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** a UBSAN differential would pin the shift-UB class that a guest-value probe provably cannot see

**state_note (head):** Filed 2026-09-07 from `#510`'s pass 2.  Full record in OUTSTANDING_BUGS.md under the same id.

grok showed two one-line regressions that re-open real UB and score FULL MARKS on a 12-row guest-value probe, and the reason is STRUCTURAL: both are DEFINEDNESS repairs, and definedness has no guest-visible value on a non-trapping host.  `1 << 31' and `1U << 31' give the same mask after the `- 1'; with a correct 32-bit mask `x |= ~mask' is `x |= 0'.

**build-asan already carries `-fsanitize=address,undefined`** -- established AFTER I wrote "unchecked" about it in the probe header, one grep from the answer.  So the class IS pinnable, as a DIFFERENTIAL: fixed source produces no shift diagnostic, the `1U'->`1' mutant produces one.

**Not bolted onto #510**: a second binary and a STDERR oracle is a new measurement lane, and #510's pass 2 had already run.  A lane added after a pass is a lane nobody reviewed.

Covers the same species at [[lcashiftub]], [[sgirebufshiftub]], m88k_rot:513, cpu_mips_instr.c:1757 [2026-11-02, records: not the same species -- `rs` is `uint32_t` (:1756), so nothing there shifts into a signed sign bit; its undefined behaviour is the shift count `32-lsb-size` going negative when lsb + size > 32 (C99 6.5.7p3), which a value oracle cannot see either] and the two is_userpage sites -- EIGHT sites across three CPUs, none directly visible to a value oracle.

*** THE FILED [... 7667 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** the filed question about the UBSan sweep is fully answered

### ROW `uninorthdevscan` -- state `open`, severity `low`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** dev_uninorth.c: `idata & (1 << dev)` at dev==31 is a signed-shift UB, but NOT guest-visible -- the address port is registered with length 4, so idata can never carry bits 32..63 (investigated and DOWNGRADED, not assumed)

**state_note (head):** FILED 2026-09-07, split out of [[shiftubcensus]] item (A) because it is the only member of that
census with a **GUEST-VISIBLE CONSEQUENCE** rather than a language-level one, and it therefore owes a
witness the others do not.

**THE SITE**, `dev_uninorth.c`, in the PCI address-register write path:

    :56    uint64_t idata = memory_readmax64(cpu, data, len | MEM_PCI_LITTLE_ENDIAN);
    ...
    :60    d->cur_addr = idata;
    :70    for (dev=11; dev<32; dev++)
    :71        if (idata & (1 << dev))
    :72            break;

**`idata` is `uint64_t` and `1 << dev` is an `int`.**  At `dev == 31` that is `0x80000000`, which as
a signed `int` is NEGATIVE, so converting it for the `&` against a `uint64_t` **SIGN-EXTENDS it to
`0xffffffff80000000`**.

> **CONSEQUENCE IF `idata` CARRIES ANY BIT IN 32..63: the loop matches at `dev == 31` when no
> device bit is set there, and the scan selects the WRONG DEVICE.**  The repair (`1U << dev`) is
> therefore NOT behaviour-preserving here -- unlike its sibling in `dev_v3.c`, where the operand's
> high bits are provably zero and the same edit changes nothing.

**REACHABLE AS A DEVICE:** `machine_macppc.c:68` calls
`dev_uninorth_init(machine, machine->memory, 0xe2000000, ...)`, and `dev_uninorth.c:141` registers
`"uninorth_pci_addr"` at `addr + 0x800000` = **0xe2800000**.  macppc is a supported machine here.

*** WHAT IS NOT ESTABLISHED, AND IT  [... 5578 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** verified that the width cannot exceed 32 bits, lacking guest visibility

### ROW `codexcyberflag` -- state `open`, severity `med`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** codex briefs are rejected PLATFORM-SIDE by a cybersecurity content filter, and this project's own row ids are the trigger

**state_note (head):** *** A SEAT-FAILURE CLASS NOT ON THE CARRIER'S LIST, MEASURED BY CENSUS 2026-09-08. ***

    ERROR: This content was flagged for possible cybersecurity risk.  If this seems wrong, try
    rephrasing your request.  To get authorized for security work, join the Trusted Access for
    Cyber program

**It is a PLATFORM content filter, not a model refusal**, and it is the only codex failure mode
here that can leave a ZERO-BYTE answer behind a large `.err`.  The carrier lists codex refusal
triggers as vocabulary, archive-reading, chain shape and the evasion-construction question; this
is a different mechanism and it is not listed.

*** THE CENSUS, and it corrects my own first reading of it. ***

    21   .err files carry the flag
     8   of those left a ZERO-BYTE .txt
     5   of the 21 produced a FULL answer anyway (14,102 / 18,687 / 12,952 / 8,682 / 6,868 b)

**So the flag is NOT terminal and its PRESENCE proves nothing** -- exactly like the refusal-line
rule already on record.  `gateworktree`'s 14,102 b assess carries the flag twice and answered in
full.  **The `.txt` SIZE is the only discriminator**, which is the rule this project already
learned once for refusal lines and had not connected to this filter.

*** THE TRIGGER IS THIS PROJECT'S OWN VOCABULARY, WHICH IS WHY IT KEEPS RECURRING. ***  The row
ids are `sgirekills`, `lcaconfbus1kill`, `lcairqstubkill`, `pcc2c040kill`, `alp [... 15397 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** The row acts as a ledger entry for a measured phenomenon whose circumvention technique is known but needs formal promotion to a rule.

### ROW `splitscorer` -- state `open`, severity `low`; PROPOSED: **DROP**

**title:** APPENDING a row BELOW a probe's score computation silently splits the summary -- numerator over the old row set, denominator evaluated at print time.  *** POPULATION AT HEAD IS ZERO across all 73 candidate probes: this is an EDITING hazard I introduced twice in one session, NOT a latent defect in the tree ***

**state_note (head):** FILED 2026-09-08, found by adding rows to two probes during `#516`.

**THE SHAPE.**  Both probes computed their score at a point ABOVE the last `row()` call:

    ok  = sum(1 for _, o in rows if o)      <- evaluated HERE
    ... more row() calls ...                <- appended AFTER
    print("..._RESULT=%d/%d" % (ok, len(rows)))

`ok` is a VALUE captured early; `len(rows)` is a call evaluated late.  So the numerator counts the
old row set and the denominator counts the new one.

*** IT IS SILENTLY RIGHT WHENEVER NOTHING FAILS, WHICH IS THE DANGEROUS HALF. ***  With every row
passing, the numerator equals the old count and the denominator the new, so the score reads `4/6`
rather than `6/6` -- visibly wrong.  But in the UART probe's POST-FIX run the formula was
`len(rows) - len(bad)` with `bad` empty, which renders `5/5` -- **correct by coincidence**.  Only the
PRE-FIX run, where rows actually failed, exposed it: reported 3/5, honest score 2/5.

> **A SCORE LINE THAT CONTRADICTS ITS OWN PRINTED ROWS IS THE CHEAPEST SIGNAL THERE IS, and it is
> only available because these probes print every row individually.**  A probe that printed only its
> summary would have shipped the wrong number with nothing to compare it against.

**REPAIRED IN BOTH FILES** by moving the computation adjacent to the print, with a comment saying
why, so the split cannot be reintroduced by appending a row.

 [... 3007 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** The author confirmed the defect was introduced and subsequently repaired within the same session, leaving a population of zero at HEAD.

## For EACH row return (a numbered block per row, its id first)

1. `AGREE` or `DISAGREE` with the proposed closure, and why in one line -- DISAGREE when the row's own text describes a live,
   reachable defect, or names work still owed.
2. If AGREE: the closure RECORD text, two to four lines, in that honest form (for OVERTAKEN: the control that would
   discriminate and the rows that would carry it, stated as OWED, never as done).
3. The ONE fact that would make closing wrong -- what someone must check before closing it.
Do not invent commits, measurements or file contents the text does not give.

End with one line: `CLOSEDRAFT_08: <a> AGREE, <d> DISAGREE`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBCLOSE08: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
