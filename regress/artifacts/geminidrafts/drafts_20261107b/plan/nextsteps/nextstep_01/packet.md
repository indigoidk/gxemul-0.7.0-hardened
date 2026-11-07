# Reading task: nextstep_01 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBNEXT01-3f80` on a line of its own.

# GXemul hardened fork -- THE NEXT STEP for 6 filed issues that must NOT be closed yet (a defensive project's queue work)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier pass found that each row below still names work owed, so it stays open.  You cannot
read files; work from the text.  Ledger at HEAD 8d9df658.  Proposals only.

## The rows

### ROW `citestale` -- state `open`, severity `-`

**title:** citestale  a same-file line citation is invalidated by the round's OWN later edits -- six instances in one round, and no gate checks it

**state_note:** *** ADJUDICATED 2026-08-26: NO CHECK. The proposed WARN was REJECTED ON MEASUREMENT, and THREE STATEMENTS I put in this row yesterday are WRONG RECORDS, corrected here. ***

**(a) 'So today's `:733` passed GREEN' is FALSE, and it was the load-bearing claim of my diagnosis.** Section D's regex is `\b[a-z0-9_]+\.(c|h)\b:[0-9]+` -- it requires a FULL `file.c:` prefix. The stale citation is BARE: `":720 is :733, ..."`. VERIFIED: D's extraction from `5b5089d` yields `dev_dreamcast_gdrom.c:307/338/515/611/722/889/922` and no 733. **It did not pass green -- it was never looked at.** That is a materially different defect from the one I recorded.

**(b) 'never by a gate' contradicts this row's own instance 5**, which the row says section X caught -- and the CHANGELOG headlines it *'The last thing a gate caught was a citation that decayed by MULTIPLYING.'*

**(c) 'MEASURED: fires on the real instance' is true at COMMIT granularity only, not CITATION granularity** -- the rule fires on that commit, but not on the citation that went stale.

*** THE PROPOSED WARN FAILS ITS OWN NEGATIVE CONTROLS IN BOTH DIRECTIONS. *** Measured over 429 commits since 2026-07-20: it fires on **57 commits / 263 citations (~11 per week)** and its **recall on the eight recorded instances is ZERO**, because every recorded instance is a BARE `:NNN` that D's extraction cannot see. On the motivating round itself it emits 15 warns, none of them the stale one. **A checker policing the visible minority of a class while blind to its dominant form IS the check-that-cannot-fail shape -- the exact defect I had attributed to section D.**

*** AND THE CLASS DOES NOT CLEAR THE `countderiver` BAR. *** The adjudicator hunted with denominators -- 135 'stale' mentions in the CHANGELOG, 19 citation-flavoured, every region read -- and **no stale line citation has ever consumed a decision.** The records say so themselves: *'Nothing the citations said was wrong -- only the numbers had moved'* (#408); *'The rows were right, the table number sent a reader to the wrong page'* (#457).

**AND THE REASON IS STRUCTURAL, which is why this class is WEAKER than the counts one that was already declined: NO GATE, PROBE OR SCRIPT IN THIS TREE READS A LINE CITATION FUNCTIONALLY** -- gates key on grep anchors and content. A citation is consumed only by a READER, and a reader using one opens the file, so a drifted number SELF-REFUTES AT THE POINT OF USE. A carried count does not. That is why all eight were caught by a seat or a re-read.

*** THE REMEDY HAS BEEN ADOPTED FOUR SEPARATE TIMES, EACH ROUND-LOCAL, NEVER CARRIED -- the `countderiver` 'already shipping, uncodified' shape exactly. *** The #340-era round (*'replaced by symbol-anchored citations instead of a third set of numbers'*), #408 (*'every citation now names the construct'*), the fourth-instance note (*'the arms are named by what they ARE'*), and my own grep-anchor conversion today. **Section D1's own header already says 'prefer naming the CONSTRUCT over th

**hold_question:** (none)

### ROW `auditmap` -- state `held`, severity `-`

**title:** auditmap  Fill the audit coverage table by measurement

**state_note:** 

**hold_question:** (none)

### ROW `hlen` -- state `held`, severity `-`

**title:** hlen  Device handlers that ignore the access length (audit)

**state_note:** 

**hold_question:** (none)

### ROW `seam` -- state `held`, severity `-`

**title:** seam  Nothing goes red if the driver and the log grader disagree about the path

**state_note:** 

*** 2026-09-13 CODEX RESEARCH (read-only, gpt-6-astra max): DOCUMENT-ONLY -- see regress/artifacts/codex_research_20260913/seam.answer.md.  Premises it corrected are in the entry; the row stays HELD pending the named next step and the batched flagship close pass. ***

**hold_question:** Nothing goes red if the driver and the log grader disagree about the PATH. The hold says the R1 fix removed the CAUSE but not the DETECTOR. QUESTION: is that still true at HEAD? Check whether `drive_guest.py` and the grader in `gate_hygiene.sh` can still disagree about which log they are reading -- `#422` made `drive_guest.py` honour `$LOGDIR`, so the specific divergence may be gone. If the cause is gone AND no detector exists, the honest disposition may be documented-only rather than a round; say which, and say what a detector would have to observe that a green run today does not.

### ROW `stateaudit0923` -- state `open`, severity `HIGH`

**title:** 2026-09-23 state audit after the 09-22 Windows-Update reboot: nothing on disk lost; the records and the tree disagree in ten places, all pre-reboot; gate 6 is red at HEAD; thirteen exemptions lapse 2026-09-28

**state_note:** [2026-11-02, records] The title and the 2026-09-23 entry are that day's audit and stay as written. 'Gate 6 is red at HEAD' was measured 2026-09-23 on that day's HEAD (f685d75c, the parent of #545's 4264ee20, which committed this row); #546 hygienecensus (3e33201d, 2026-09-24) re-derived those census pins, and this row records no later gate-6 run.  The thirteen exemptions were wired, re-dated or discharged by #548 (f4f601c4), #550 (04500deb) and #551 (f5e155ac); at 987cb596 EXEMPT holds eight dated entries, 2026-11-05 to 2026-12-03 (check_probe_wiring.py:3355-3419), and SC_EXEMPT holds ieee_store:2026-12-10 (gate_offline.sh:2391).  Of the five findings the entry calls draft-only, armdesc3kill, armdacr2kill and fbirqsoftunimpl were filed by #545's own commit (4264ee20), hygienecensus by #546 (3e33201d) and upstreamdeleteprose by #547 (bead6ad9).

**hold_question:** Owner: (1) the census population and one bulk pin re-derivation before the 2026-09-27 battery; (2) the thirteen exemptions lapsing 2026-09-28 [2026-11-02, records: decided -- #548 (f4f601c4) wired one, #550 (04500deb) re-dated eleven one by one, and #551 (f5e155ac) discharged wdc_identify]; (3) the #545 commit and its Fable hold; (4) commits of the other sessions' verified work since 2026-09-17; (5) the never-commit list vs section J.

### ROW `dfreq` -- state `held`, severity `-`

**title:** dfreq  A one-shot deadline is modelled as a repeating rate (design item)

**state_note:** [2026-10-22] WIDENED by the external-fixes research (regress/artifacts/research_20261022/TRIAGE.md T93; regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md B): two residuals no row carried -- the host-timer Compare rate ignores that Count runs at CPU/2 (cpu_mips_coproc.c:808-809 at de8c7547), and compare_interrupts_pending is an uncapped int (:422; include/cpu_mips.h:277) that re-asserts IP7 back to back while it stays above 0 (cpu_dyntrans.c:433-436) -- the uncapped-counter shape #442 bounded in dev_footbridge.c only.  Ports: jroark/GXemul 2fa3853 (rate halved, backlog capped at 1), 4729fb6, dabf5ce (report rows A3-26, A3-27; https://github.com/jroark/GXemul/commit/2fa38531d41426151943758faa46a2d3297b8c3f).  The wrap-reprogramming half stays `n1`'s.  witness: none -- research finding, not yet reproduced here.  ||  

*** 2026-09-13 CODEX RESEARCH (read-only, gpt-6-astra max): DOCUMENT-ONLY -- see regress/artifacts/codex_research_20260913/dfreq.answer.md.  Premises it corrected are in the entry; the row stays HELD pending the named next step and the batched flagship close pass. ***

**hold_question:** A one-shot deadline is modelled as a repeating rate. The hold says 'a design change, per the stopping rule'. QUESTION: is there a GUEST-OBSERVABLE consequence that makes this a defect rather than a modelling difference? This matters because the carrier records that dfreq's earlier 'no witness of either kind' claim was MEASURED FALSE -- a witness was built in one session. So: what does that witness actually show, and does it show a wrong VALUE reaching the guest or only a different internal representation? If only the latter, documented-only is the honest disposition and the row should say so.

## For EACH row (a numbered block, its id first)

1. The ONE concrete next step that would resolve it, as exactly one of: FIX-ROUND (a code change, with its site),
   MEASUREMENT (what to run and what result settles it), READING (a question a careful reading of named code or a manual
   answers), RECORD (a correction or closure note), OWNER-DECISION (the question, phrased so it can be answered).
2. If it is a READING or a RECORD that the text above already settles, DRAFT it now (two to six lines).  Otherwise say
   what the step needs that is not in the text.
3. Whether it can be COMBINED with another row in this packet (same device, same next step).
Do not invent measurements, commits or file contents.

End with one line: `NEXTSTEP_01: <f> FIX-ROUND, <m> MEASUREMENT, <r> READING, <c> RECORD, <o> OWNER-DECISION`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBNEXT01: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
