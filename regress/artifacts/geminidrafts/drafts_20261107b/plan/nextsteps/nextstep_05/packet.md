# Reading task: nextstep_05 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBNEXT05-0aa7` on a line of its own.

# GXemul hardened fork -- THE NEXT STEP for 6 filed issues that must NOT be closed yet (a defensive project's queue work)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier pass found that each row below still names work owed, so it stays open.  You cannot
read files; work from the text.  Ledger at HEAD 8d9df658.  Proposals only.

## The rows

### ROW `uninorthdevscan` -- state `open`, severity `low`

**title:** dev_uninorth.c: `idata & (1 << dev)` at dev==31 is a signed-shift UB, but NOT guest-visible -- the address port is registered with length 4, so idata can never carry bits 32..63 (investigated and DOWNGRADED, not assumed)

**state_note:** FILED 2026-09-07, split out of [[shiftubcensus]] item (A) because it is the only member of that
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

*** WHAT IS NOT ESTABLISHED, AND IT IS THE WHOLE QUESTION: CAN `idata` ACTUALLY CARRY BITS 32..63? ***
`memory_readmax64(cpu, data, len | MEM_PCI_LITTLE_ENDIAN)` returns a value whose width follows the
ACCESS WIDTH.  On a 4-byte store -- the ordinary way a guest writes a PCI config address -- the
result cannot exceed 32 bits, the sign-extended ones meet only zeros, and **nothing observable
happens**.  The defect needs an **8-byte** access to that register.

**So the row is HELD at the reachability question, not at the arithmetic.**  A codex analysis is out
on exactly this (`regress/artifacts/shiftubcensus/UNINORTH_brief.md`), asking: what does
`memory_readmax64` return per width; what widths reach this handler on macppc; and -- the premise I
am least sure of -- whether `MEM_PCI_LITTLE_ENDIAN`, which is OR'd into the `len` PARAMETER, can
perturb the length itself rather than only the byte order.

**SEVERITY DELIBERATELY LEFT AT `med` PENDING THAT ANSWER.**  If an 8-byte access reaches the
handler this is a guest-drivable mis-decode on a supported machine and should be HIGH; if it cannot,
this collapses into the same language-level hygiene as the other two census members and should be
LOW.  *Grading it before the answer would be picking the number I prefer.*

**THE REPAIR IS ONE TOKEN EITHER WAY** (`1U << dev`), and it is correct under both outcomes -- the
question is only what the round may CLAIM, and whether it owes a witness.

*** MY SHAKIEST PREMISE IS ANSWERED BY READING, AND IT ANSWERS THE REASSURING WAY -- SO THE ROW
NARROWS TO EXACTLY ONE QUESTION. ***

I flagged as least certain whether `MEM_PCI_LITTLE

**hold_question:** (none)

### ROW `codexcyberflag` -- state `open`, severity `med`

**title:** codex briefs are rejected PLATFORM-SIDE by a cybersecurity content filter, and this project's own row ids are the trigger

**state_note:** *** A SEAT-FAILURE CLASS NOT ON THE CARRIER'S LIST, MEASURED BY CENSUS 2026-09-08. ***

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
ids are `sgirekills`, `lcaconfbus1kill`, `lcairqstubkill`, `pcc2c040kill`, `alphavmkill`,
`asicoffsetkill`; the probe rows are literally named `tlb_a ld kill`, and briefs speak of *death
rows* and *host kills*.  **A brief that merely NAMES its row carries the trigger.**  The graded
evidence is in `regress/artifacts/sgirekills/refusals/`:

    attempt1.err                       5,906 b   flagged early
    attempt2_neutralised.err           6,572 b   flagged early
    attempt3_scoping.err               6,829 b   flagged early
    attempt4_neutral_late_flag.err   382,773 b   did the WHOLE analysis, flagged at the END

*** THE RECOVERY ALREADY WORKS AND HAS BEEN USED THREE TIMES, AND IT IS WRITTEN DOWN NOWHERE. ***

    sgirekills      codex_rounddesign_20260908       0 b  ->  _RETRY_  6,868 b
    armbfiwidth     codex_fixdesign_20260907         0 b  ->  20260908 5,091 b, v2 7,308 b
    sgirebufuninit  codex_pass1_20260907             0 b  ->  _reworded_ 10,557 b

**The filename `codex_reworded_...` IS the technique**, applied by hand three times by whoever hit
the wall, and never promoted to a rule -- so the next round rediscovers it.  *That is the carrier's
own trigger-versus-memory finding: the knowledge existed, on disk, at the moment of the decision,
and did not fire.*

**STILL UNRECOVERED (codex lost; another seat covered the topic in all but the last):**
`lcaconfwidth` census (grok 25,281 b), `lcaconfbus1kill` witness (grok 10,679 b), `alphatbinegsel`
witness (grok 10,679 b -- grok took it after codex was flagged), and `m88kexcdeliver/pass1/
codex_p1_refire` which has a 0-byte `.txt` and **NO `.err` at all**, i.e. by the redirect-target
rule it nev

**hold_question:** (none)

### ROW `armcpabsent` -- state `open`, severity `MED`

**title:** MRC or MCR to an uninstalled ARM coprocessor fatals and falls through, with Undefined Instruction delivery still commented out; CDP already delivers Undefined Instruction

**state_note:** AN ID FOR AN EXISTING PROSE ENTRY of OUTSTANDING_BUGS.md (lines 18709-18713 at db8b1a33) -- no second entry is opened.  Where the text comes from: grok/grok_irule_a.txt A10 (conceding Astra's ifile_01 finding)

**hold_question:** (none)

### ROW `armdwordalign` -- state `open`, severity `MED`

**title:** OUTSTANDING_BUGS.md:5140-5144 at db8b1a33 -- (task #74) LDRD/STRD mask the address with ~7 where ARMv6 with U=1 permits word alignment and accesses address and address+4

**state_note:** AN ID FOR AN EXISTING PROSE ENTRY of OUTSTANDING_BUGS.md -- no second entry is opened.  GOVERNING TEXT (from the dispositions file, cut at 400 characters): (added by the review pass)  [Astra afile_01, D:779]

**hold_question:** (none)

### ROW `ascoutresid` -- state `open`, severity `MED`

**title:** A DATA_OUT DMA clamped to the target's remaining length still reports residual 0 with Terminal Count set

**state_note:** GOVERNING TEXT (from the dispositions file, cut at 400 characters): as size_t (dev_asc.c:577-583, :610-622, :662-665, :1155). * `ascoutresid` MED -- a DATA_OUT DMA clamped to the target's remaining length still reports residual 0 with Terminal Count set (dev_asc.c:755-761; #281 fixed the DATA_IN twin). The `:707` decision is a MEASURED choice (#283) and stays; the repair is the report only. * `asccmddma` MED -- COMMAND-phase DMA reads the C

**hold_question:** (none)

### ROW `dupidcheck` -- state `open`, severity `LOW`

**title:** tools/precommit_check.sh: no section refuses a duplicate ledger row id -- a row filed twice under one id, or a new row given an existing row's id, passes P, W, O, H, K, Q2, I2, I, L and X

**state_note:** filed 2026-10-22 from the external-fixes filing's pretest (regress/artifacts/research_20261022/filing_20261022/PRETEST.md, GAPS.md item 2): both duplicate-id controls -- the same new id twice, and a new row carrying an existing id -- left every checker green; only the records drafter's own uniqueness guard refused them.  A duplicate id makes two rows render and resolve as one on the dashboard and in every by-id lookup.  Remedy is a tooling change (an id-uniqueness section, or a check inside check_entry_domain.py / check_row_states.py), which the carrier says ships as its own harness round owing two negative controls: a duplicated id must red, and the 1067 unique ids at HEAD must stay green.

**hold_question:** (none)

## For EACH row (a numbered block, its id first)

1. The ONE concrete next step that would resolve it, as exactly one of: FIX-ROUND (a code change, with its site),
   MEASUREMENT (what to run and what result settles it), READING (a question a careful reading of named code or a manual
   answers), RECORD (a correction or closure note), OWNER-DECISION (the question, phrased so it can be answered).
2. If it is a READING or a RECORD that the text above already settles, DRAFT it now (two to six lines).  Otherwise say
   what the step needs that is not in the text.
3. Whether it can be COMBINED with another row in this packet (same device, same next step).
Do not invent measurements, commits or file contents.

End with one line: `NEXTSTEP_05: <f> FIX-ROUND, <m> MEASUREMENT, <r> READING, <c> RECORD, <o> OWNER-DECISION`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBNEXT05: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
