# Reading task: closedraft_01 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBCLOSE01-4795` on a line of its own.

# GXemul hardened fork -- DRAFT THE CLOSURE RECORDS for 6 filed issues proposed for closing (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier triage pass proposed closing each row below.  Closing must be HONEST: a row closed
as documented says what was assessed and not changed; a dropped row says why it is not a defect worth a round; a row closed
as OVERTAKEN (someone else's fix removed the defect) is only closable on three conditions -- (1) a discriminating control,
measured at HEAD: neutralise the overtaking fix and this row's own symptom comes back; (2) the rows that now carry the
coverage named; (3) that control preserved at a durable path.  You cannot read files; work from the text.  Ledger at HEAD 8d9df658.

## The rows

### ROW `citestale` -- state `open`, severity `-`; PROPOSED: **DROP**

**title:** citestale  a same-file line citation is invalidated by the round's OWN later edits -- six instances in one round, and no gate checks it

**state_note (head):** *** ADJUDICATED 2026-08-26: NO CHECK. The proposed WARN was REJECTED ON MEASUREMENT, and THREE STATEMENTS I put in this row yesterday are WRONG RECORDS, corrected here. ***

**(a) 'So today's `:733` passed GREEN' is FALSE, and it was the load-bearing claim of my diagnosis.** Section D's regex is `\b[a-z0-9_]+\.(c|h)\b:[0-9]+` -- it requires a FULL `file.c:` prefix. The stale citation is BARE: `":720 is :733, ..."`. VERIFIED: D's extraction from `5b5089d` yields `dev_dreamcast_gdrom.c:307/338/515/611/722/889/922` and no 733. **It did not pass green -- it was never looked at.** That is a materially different defect from the one I recorded.

**(b) 'never by a gate' contradicts this row's own instance 5**, which the row says section X caught -- and the CHANGELOG headlines it *'The last thing a gate caught was a citation that decayed by MULTIPLYING.'*

**(c) 'MEASURED: fires on the real instance' is true at COMMIT granularity only, not CITATION granularity** -- the rule fires on that commit, but not on the citation that went stale.

*** THE PROPOSED WARN FAILS ITS OWN NEGATIVE CONTROLS IN BOTH DIRECTIONS. *** Measured over 429 commits since 2026-07-20: it fires on **57 commits / 263 citations (~11 per week)** and its **recall on the eight recorded instances is ZERO**, because every recorded instance is a BARE `:NNN` that D's extraction cannot see. On the motivating round itself it e [... 9611 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** Previously adjudicated and rejected on measurement.

### ROW `auditmap` -- state `held`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** auditmap  Fill the audit coverage table by measurement

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** Dashboard behavior was explicitly grandfathered by owner decision.

### ROW `b101` -- state `held`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** #101  SH4 TSTR can start a timer while timer_hz is 0

**state_note (head):** *** EVIDENCE 2026-08-27: the MECHANISM is TRUE, the SEVERITY IS NIL, and the tree already says so 600 lines from where the seat was looking. ***

**True as stated:** the `SH4_TSTR` arm (`dev_sh4.c:1929-1948`) starts a timer on a write with no `timer_hz` guard anywhere in it.

**But that state was already measured and recorded as harmless**, in this file, by the round that placed the guard (`:2062-2064`):
  > *"A seat measured the third option (store idata, skip the prescaler switch, leave timer_hz at 0) as SAFE -- no division by zero, no UNF, no pending interrupt."*

**And it is safe STRUCTURALLY, not incidentally:** `timer_hz` is the NUMERATOR at `:481`, `step = (uint32_t)(d->timer_hz[i] / SH4_PSEUDO_TIMER_HZ)`, so a zero can only make `step` zero -- it can never be a divisor. `:2071-2073` adds that `timer_hz[]` is already 0.0 from DEVINIT's memset, and those four prescaler cases are its only writes in the file.

**DISPOSITION: assessed, NOT a defect.** A started timer at 0 Hz that does not advance is the CORRECT behaviour, not a symptom -- so a detector keyed on TCNT0 failing to advance would pin the right answer as though it were a bug.

*The farmed seat confirmed the mechanism and could not have known the disposition: the assessment lives ~600 lines away in the same file. This is why a seat answer is verified locally before it is recorded, never transcribed.*

**hold_question:** (none)

**the triage pass's reason:** Assessed and proven safe structurally; not a defect.

### ROW `hlen` -- state `held`, severity `-`; PROPOSED: **CLOSE-OVERTAKEN**

**title:** hlen  Device handlers that ignore the access length (audit)

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** the three rows grinding through the class have largely shipped their fixes

### ROW `seam` -- state `held`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** seam  Nothing goes red if the driver and the log grader disagree about the path

**state_note (head):** *** 2026-09-13 CODEX RESEARCH (read-only, gpt-6-astra max): DOCUMENT-ONLY -- see regress/artifacts/codex_research_20260913/seam.answer.md.  Premises it corrected are in the entry; the row stays HELD pending the named next step and the batched flagship close pass. ***

**hold_question:** Nothing goes red if the driver and the log grader disagree about the PATH. The hold says the R1 fix removed the CAUSE but not the DETECTOR. QUESTION: is that still true at HEAD? Check whether `drive_guest.py` and the grader in `gate_hygiene.sh` can still disagree about which log they are reading -- `#422` made `drive_guest.py` honour `$LOGDIR`, so the specific divergence may be gone. If the cause is gone AND no detector exists, the honest disposition may be documented-only rather than a round; s [... 88 more characters not shown]

**the triage pass's reason:** The original divergence is fixed at HEAD, leaving only coverage debt.

### ROW `stateaudit0923` -- state `open`, severity `HIGH`; PROPOSED: **CLOSE-OVERTAKEN**

**title:** 2026-09-23 state audit after the 09-22 Windows-Update reboot: nothing on disk lost; the records and the tree disagree in ten places, all pre-reboot; gate 6 is red at HEAD; thirteen exemptions lapse 2026-09-28

**state_note (head):** [2026-11-02, records] The title and the 2026-09-23 entry are that day's audit and stay as written. 'Gate 6 is red at HEAD' was measured 2026-09-23 on that day's HEAD (f685d75c, the parent of #545's 4264ee20, which committed this row); #546 hygienecensus (3e33201d, 2026-09-24) re-derived those census pins, and this row records no later gate-6 run.  The thirteen exemptions were wired, re-dated or discharged by #548 (f4f601c4), #550 (04500deb) and #551 (f5e155ac); at 987cb596 EXEMPT holds eight dated entries, 2026-11-05 to 2026-12-03 (check_probe_wiring.py:3355-3419), and SC_EXEMPT holds ieee_store:2026-12-10 (gate_offline.sh:2391).  Of the five findings the entry calls draft-only, armdesc3kill, armdacr2kill and fbirqsoftunimpl were filed by #545's own commit (4264ee20), hygienecensus by #546 (3e33201d) and upstreamdeleteprose by #547 (bead6ad9).

**hold_question:** Owner: (1) the census population and one bulk pin re-derivation before the 2026-09-27 battery; (2) the thirteen exemptions lapsing 2026-09-28 [2026-11-02, records: decided -- #548 (f4f601c4) wired one, #550 (04500deb) re-dated eleven one by one, and #551 (f5e155ac) discharged wdc_identify]; (3) the #545 commit and its Fable hold; (4) commits of the other sessions' verified work since 2026-09-17; (5) the never-commit list vs section J.

**the triage pass's reason:** The audit's required holds and exemptions were wired by subsequent commits.

## For EACH row return (a numbered block per row, its id first)

1. `AGREE` or `DISAGREE` with the proposed closure, and why in one line -- DISAGREE when the row's own text describes a live,
   reachable defect, or names work still owed.
2. If AGREE: the closure RECORD text, two to four lines, in that honest form (for OVERTAKEN: the control that would
   discriminate and the rows that would carry it, stated as OWED, never as done).
3. The ONE fact that would make closing wrong -- what someone must check before closing it.
Do not invent commits, measurements or file contents the text does not give.

End with one line: `CLOSEDRAFT_01: <a> AGREE, <d> DISAGREE`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBCLOSE01: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
