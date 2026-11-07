# Reading task: closedraft_10 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBCLOSE10-1c66` on a line of its own.

# GXemul hardened fork -- DRAFT THE CLOSURE RECORDS for 6 filed issues proposed for closing (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier triage pass proposed closing each row below.  Closing must be HONEST: a row closed
as documented says what was assessed and not changed; a dropped row says why it is not a defect worth a round; a row closed
as OVERTAKEN (someone else's fix removed the defect) is only closable on three conditions -- (1) a discriminating control,
measured at HEAD: neutralise the overtaking fix and this row's own symptom comes back; (2) the rows that now carry the
coverage named; (3) that control preserved at a durable path.  You cannot read files; work from the text.  Ledger at HEAD 8d9df658.

## The rows

### ROW `ascoutresid` -- state `open`, severity `MED`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** A DATA_OUT DMA clamped to the target's remaining length still reports residual 0 with Terminal Count set

**state_note (head):** GOVERNING TEXT (from the dispositions file, cut at 400 characters): as size_t (dev_asc.c:577-583, :610-622, :662-665, :1155). * `ascoutresid` MED -- a DATA_OUT DMA clamped to the target's remaining length still reports residual 0 with Terminal Count set (dev_asc.c:755-761; #281 fixed the DATA_IN twin). The `:707` decision is a MEASURED choice (#283) and stays; the repair is the report only. * `asccmddma` MED -- COMMAND-phase DMA reads the C

**hold_question:** (none)

**the triage pass's reason:** measured choice #283 stays

### ROW `m88kconvdelivery` -- state `open`, severity `MED`; PROPOSED: **DROP**

**title:** OUTSTANDING_BUGS.md:1549-1558 at db8b1a33 -- m88k float-to-int conversions complete in the emulator where the MC88100 raises a conversion-overflow or reserved-operand exception and writes nothing (cpu_m88k_instr.c:2063-2101)

**state_note (head):** AN ID FOR AN EXISTING PROSE ENTRY of OUTSTANDING_BUGS.md -- no second entry is opened.  GOVERNING TEXT (from the dispositions file, cut at 400 characters): (added by the review pass)  [Astra afile_01, D:532; MED by the severity rule -- the dispositions line states no grade]

**hold_question:** (none)

**the triage pass's reason:** Already tracked as an existing prose entry in OUTSTANDING_BUGS.md.

### ROW `qharmarchlevel` -- state `open`, severity `MED`; PROPOSED: **DROP**

**title:** ARM CPU table has no architecture level, so version gates cannot be applied

**state_note (head):** AN ID FOR AN EXISTING PROSE ENTRY of OUTSTANDING_BUGS.md (lines 3022-3040 at db8b1a33) -- no second entry is opened.  Where the text comes from: the governing line's quoted title (grok)

**hold_question:** (none)

**the triage pass's reason:** Already tracked as an existing prose entry.

### ROW `qharmexalign` -- state `open`, severity `HIGH`; PROPOSED: **DROP**

**title:** Both queue passages record one defect: unaligned LDREX and STREX halt the emulator, though an alignment Data Abort is mandatory when (A,U) is not (0,0) and the halt is wrong under either setting.

**state_note (head):** AN ID FOR AN EXISTING PROSE ENTRY of OUTSTANDING_BUGS.md (lines 3625-3626; 4181-4202 at db8b1a33) -- no second entry is opened.  Where the text comes from: grok/grok_ititles.txt

**hold_question:** (none)

**the triage pass's reason:** Already tracked as an existing prose entry.

### ROW `qharmmediaver` -- state `open`, severity `MED`; PROPOSED: **DROP**

**title:** ARMv6 media encodings decode on the modelled ARMv4 CPUs

**state_note (head):** AN ID FOR AN EXISTING PROSE ENTRY of OUTSTANDING_BUGS.md (lines 1870-1872 at db8b1a33) -- no second entry is opened.  Where the text comes from: the governing line's quoted title (grok)

**hold_question:** (none)

**the triage pass's reason:** Already tracked as an existing prose entry.

### ROW `cxlaunchcov` -- state `open`, severity `LOW`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** the launcher controls' coverage debt above the floor: `wc -w` for the empty test's `wc -c` passes all 123 after-column checks (measured), and PK keys codex's own rc 7/8 on row names

**state_note (head):** filed 2026-10-17 at the tools/cxlaunch.sh landing, from its v7 pass (GPT-6 Astra found the wc -w survivor, the main loop measured it 123/123 -- regress/artifacts/cxlaunchland_20261016/v7pass/main_meas/m_bodywords.out -- and its behaviour, rc 0 with one space on stdout and a quoted wall line: launcher 0, mutant 8; GLM 5.3 named the PK row-name residual).  Clause (e): the seats graded no floor breach.  Disclosed in the controls' CONTRACT.

**hold_question:** (none)

**the triage pass's reason:** no floor breach and already disclosed in the contract

## For EACH row return (a numbered block per row, its id first)

1. `AGREE` or `DISAGREE` with the proposed closure, and why in one line -- DISAGREE when the row's own text describes a live,
   reachable defect, or names work still owed.
2. If AGREE: the closure RECORD text, two to four lines, in that honest form (for OVERTAKEN: the control that would
   discriminate and the rows that would carry it, stated as OWED, never as done).
3. The ONE fact that would make closing wrong -- what someone must check before closing it.
Do not invent commits, measurements or file contents the text does not give.

End with one line: `CLOSEDRAFT_10: <a> AGREE, <d> DISAGREE`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBCLOSE10: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
