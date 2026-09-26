# The late codex seat answers on #550, #551 and #549 -- the adjudication packet (2026-09-26)

**Why this exists.**  The codex seat (GPT-6 Astra) was walled on every panel of 2026-09-25 (usage limit to 07:01).  The
three rounds' records say it was re-fired after the reset; the re-fires ran at ~08:20, AFTER all three commits
(`#550` 04500deb, `#551` f5e155ac, `#549` 8ea26abb).  They answered.  Under the carrier's LATE-DISSENT rule a stage
fired after a round closes adjudicates like any finding: a WRONG RECORD is L4, corrected in place; a MEASURED FALSE PASS
against the shipped detector's floor or contract is L2/L3 in a follow-up commit; everything else FILES, with the
dissent verbatim, and the closed round's record gains one line naming it.  **Closure changes the licence, never the
truth-value.**  Never amend shipped code under a closed round's number.

The tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`.  The answers, verbatim:
* `regress/artifacts/wdcidselfcheck_20260925/panels/codex_codexseat_551f.txt` -- on `#551f`'s pass brief
  (`wdcidselfcheck_20260925/pass551f/pass551f_brief.md`): **DO NOT SHIP**.
* `regress/artifacts/exemptredate_20260925/panels/codex_codexseat_f2b.txt` -- on the `#550`/`#551` F2 pass brief
  (`exemptredate_20260925/f2b/f2b_brief_550_551.md`, which reviewed `#551b`): **SHIP WITH CHANGES** x2.
* `regress/artifacts/fbctrlportkill_20260924/panels/codex_codexseat_f2v6.txt` -- on `#549` v6's adjudication brief:
  **SHIP**.
What shipped: `regress/diff_wdc_identify.c` (`#551i`; its contract block is the comment above `selfcheck()`),
`regress/gate_offline.sh`, `tools/pipeline/check_probe_wiring.py` (`#550`'s exemption block), OUTSTANDING_BUGS.md.

## The findings and my proposed dispositions (numbered; the question is which of mine are wrong)

**L1 (#551, DO NOT SHIP item 1).**  The contract's (B) says a covered failure is not hidden by "a reset of either tally
or both at any placement ... (measured on #551f's pass: ...)".  The seat: the generator (`pass551f/meas551f.py.txt:83`)
built **9 of the 24** tally x conditionality x placement combinations.  **Proposed: L4** -- (B) says the report
mechanism covers every placement BY READING (the report line prints at the moment a comparator fails, before any later
reset) and was MEASURED for the nine built; **FILE** the fifteen unbuilt shapes (`wdcidresetcells`, LOW) rather than
measure them in a records commit.

**L2 (#551, item 2a).**  (B)'s "Hence no edit that leaves the covered rows running and the comparators' compiled
behaviour intact hides a covered failure" is too broad: `F_wrap` keeps both comparator bodies and the rows running,
changes their INPUTS, and escapes -- the disclosed (A) feed case.  **Proposed: L4** -- "...running, their inputs and the
comparators' compiled behaviour intact...".

**L3 (#551, item 2b).**  (B)'s "once the line is in the log no edit ... takes it back" presumes the log is not rewritten;
gate 2 writes an ordinary file and reads it afterwards.  That is (C)'s class (M19; the existing piped self-mutant lane
rejects it on all three tested defects).  **Proposed: L4** -- (B) says an edit that rewrites the log itself is (C).
The seat itself calls it "a structural objection, not a freshly measured escape".

**L4 (#551, item 4b).**  OUTSTANDING_BUGS' `wdcrowpin` says `#551e`'s pin closed the composite "for the COVERED rows",
"corroborated by the measured pin/no-pin deletion pair".  The measured pair deleted `R6 liveness: DRQ asserted`, a
VERDICT-HANDED `chk()` call the contract does not count as a covered comparison.  **Proposed: L4** -- the pin counts
comparator CALLS (all 32), and the measured pair deleted a verdict-handed one.

**L5 (#551, item 5).**  `pass551f/analyze8.py.txt` discards the shell scorer's stderr and return status, and its
CONTRACT CHECK tests only shapes whose pristine cell is green.  **Proposed: NO ACTION on the shipped record** -- the
359-job result rests on the Opus seat's independent reproduction with the real `lib.sh`
(`opus551_measured_f/analyze9.out`, all 41 table rows cell for cell), which #551's corrected record already names as the
real apparatus; **FILE** the analyzer defect only if it is to be reused (`analyze8robust`, LOW).

**L6 (#550, F2b item 5a).**  `check_probe_wiring.py`'s exemption header (HEAD `:2559`) says "These are wiring jobs, not
design ones" while `wdc_altoffset_sig_probe.py`'s entry (`:2595`) says it "owes a redesign" and the 4bit entry (`:2601`)
"an oracle choice".  **Proposed: L4** -- qualify the header sentence.

**L7 (#550, F2b item 5b).**  The `ppc_rldicl_probe.py` paragraph (`:2613`, `:2618-2619`) and its tuple (`:2624-2626`)
still frame RESULT/CONTROL lines as what "remains"/is "lacked", right after saying the rows can be scored as mk48's are.
**Proposed: L4** -- describe the protocol as one chosen approach, not a prerequisite.

**L8 (#551, F2b items 1-3).**  The seat reviewed `#551b`, and its three findings -- `sectors` never zero in the
`row_cmp()` probes, the `<`-for-`!=` escape, and a `failures` reset after `row_cmp()` returns -- were each closed by later
revisions before shipping (`rw[]` gained two `sectors == 0` probes, `#551c`; the covered-failure report, `#551f`).
**Proposed: NO ACTION; recorded** -- the seat independently found what later passes fixed.

**L9 (#549, SHIP).**  All 24 dispositions checked; N1/D1 OVERTURN-to-disclosure and N20 agree with what shipped; its
"N4's universal exit consequence is false" and "the DATA tripwire cannot see a wrong but valid selector" are already
v6c's text (NOT CLAIMED (0) and (3)).  **Proposed: NO ACTION; recorded.**

**L10 (#551, DO NOT SHIP items 4a, 4c).**  "69 named rows" (it is 69 predicates over 67 distinct rows, plus `high
byte`) is a premise of the pass brief, not of any committed text (`git grep '69 named' HEAD` is empty); the "first
covered row" lane wording is already `wdcidlane`'s two-group form.  **Proposed: NO ACTION.**

## What ships if the dispositions stand

One records commit, `#553 latecodex`: `diff_wdc_identify.c` comment text only (L1-L3; proved by the comment-stripped
preprocessor output, md5 c10d453c, and gate 2 re-run); `check_probe_wiring.py` comment text only (L6-L7); OUTSTANDING_BUGS
(L4; filings `wdcidresetcells`, and `analyze8robust` if L5 stands); one line in each of the `#550`, `#551` and `#549`
CHANGELOG blocks naming the late answer and where it went; ledger entries for the three re-fired seats; and `#549`'s
pass-2 receipt, which the next commit owes.

## The questions

1. **Which of my ten dispositions is wrong?**  Name the count.  In particular: is L1 a WRONG RECORD to reword, or a
   MEASURED-CLAIM gap that must be MEASURED before the record may stand (fifteen builds against four devices)?
2. Does any late finding state a MEASURABLE consequence that would make it L2 (a floor breach of the shipped detector)
   rather than L4 or FILE?  The discriminator is the carrier's: can it name a measurement that would come out wrong?
3. Is a separate `#553` right, or should these ride in `#529`'s commit (which is also owed and carries the receipt)?

## ADDENDUM (added after the packet went to the flagship seat, and sent to it as a message)

**L11 (#549, found by the main loop).**  `#549`'s commit (8ea26abb, ~08:31) staged its whole artifacts directory while
the codex seat re-fire on `#549` was still running, so it committed that job's files mid-flight:
`git show HEAD:regress/artifacts/fbctrlportkill_20260924/panels/codex_codexseat_f2v6.txt` is 0 bytes (the finished file
is 7,716 bytes, VERDICT: SHIP), the `.err` is truncated (1,588,311 of 1,649,553 bytes) and `codexseat_f2v6.launch.log`
is 17 of 157 bytes.  The carrier's "a preserved log is verified by its completion sentinel, not by its existence".
**Proposed: L4** -- the next commit carries the three completed files and its record says the committed versions were
truncations; **FILE** `commitinflight` (LOW, harness): a commit script refuses to stage an artifacts directory holding a
launch log without its completion line.
