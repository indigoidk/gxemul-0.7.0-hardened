# Reading task: closedraft_14 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBCLOSE14-ed51` on a line of its own.

# GXemul hardened fork -- DRAFT THE CLOSURE RECORDS for 2 filed issues proposed for closing (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier triage pass proposed closing each row below.  Closing must be HONEST: a row closed
as documented says what was assessed and not changed; a dropped row says why it is not a defect worth a round; a row closed
as OVERTAKEN (someone else's fix removed the defect) is only closable on three conditions -- (1) a discriminating control,
measured at HEAD: neutralise the overtaking fix and this row's own symptom comes back; (2) the rows that now carry the
coverage named; (3) that control preserved at a durable path.  You cannot read files; work from the text.  Ledger at HEAD 8d9df658.

## The rows

### ROW `ppcifetchibinit` -- state `open`, severity `LOW`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** src/cpus/cpu_ppc_instr.c X(to_be_translated) -- `unsigned char ib[4]` is uninitialised, so a variant that skips the failed-read block decodes a stale stack word: #582's build-dependent variants (W5, D7, V7, D12), its four failure-test narrowings and the unpredicted V12; zero-initialising ib would make them deterministic

**state_note (head):** Filed 2026-11-05 by #582, the contract's '(filed)' (regress/ppc_ifetch_probe.py, clause (e)): table 12 records V12 as NOT PREDICTED and the build-dependent variants red on rows that move table to table (regress/artifacts/qhslowifetch/r7_20261105/table12/VERDICT.md).  Test determinism only: the shipped fix returns on every failed read, so ib is never decoded after one.

**hold_question:** (none)

**the triage pass's reason:** the shipped fix returns on failed reads, neutralizing the stale decode.

### ROW `fmtmissargwitness` -- state `open`, severity `LOW`; PROPOSED: **DROP**

**title:** fmtmissarg was recorded on a detector: witness without the rung-3 ATTEMPT that term's own bound requires -- its two guest-reachable sites (a PS2 timer 2/3 hold read; a non-byte MB89352 access) were not offered to one seat for a single rung-3 attempt (filed under the late-dissent rule, disposition 3)

**state_note (head):** Filed 2026-11-06 from Fable 5.1's code-scanning final ruling (regress/artifacts/codeqlscope/ruling_20261106/RULING.md, section 5, item 3), the dissent verbatim: 'the two guest-reachable sites (a PS2 timer-hold read; a non-byte MB89352 access) were not offered to one seat for a single rung-3 attempt before the round was recorded on a detector witness.'  The bound is the carrier's: a round using detector: still owes the rung-3 ATTEMPT and must record that it was made and what it found.  fmtattr met it (its probe is a boot-path reproduction on an unmodified machine); fmtmissarg's witness field records an honest NON-attempt, which must not render the same as tried-and-could-not.  A filed LOW item, not a round: the fix is in, the compiler's diagnostic is exact for the class, and a probe built now would be a detector row whose pre-fix behaviour is measurable only on ccd1c502^.  The OWNER may drop it as documented-only; the record then says 'not attempted, dropped by ruling'.  Not a wrong record (not L4).

**hold_question:** (none)

**the triage pass's reason:** Explicitly documented that the owner may drop it and the fix is already in.

## For EACH row return (a numbered block per row, its id first)

1. `AGREE` or `DISAGREE` with the proposed closure, and why in one line -- DISAGREE when the row's own text describes a live,
   reachable defect, or names work still owed.
2. If AGREE: the closure RECORD text, two to four lines, in that honest form (for OVERTAKEN: the control that would
   discriminate and the rows that would carry it, stated as OWED, never as done).
3. The ONE fact that would make closing wrong -- what someone must check before closing it.
Do not invent commits, measurements or file contents the text does not give.

End with one line: `CLOSEDRAFT_14: <a> AGREE, <d> DISAGREE`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBCLOSE14: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
