# holdphase -- should a HELD marker be discharged only by an answer in its own phase?

> **DURABLE COPY, banked 2026-11-06 by a records commit.**  The original is `_scratchpad/wholdphase/EVIDENCE.md` (scratch, not durable; md5 7aced8e5).  This banner and one marked change to the heading of the section "Files in this directory" are the only edits.  Of the files this record names in its own directory, `analyze.py`, `analysis.out`, `markers.tsv` and `differing.tsv` are copied beside it, byte-identical; `assemble.py`, `EVIDENCE.template.md`, `frag_*.md`, `ledger_HEAD.json` and `HEAD_*.py` stay in the scratch original only.  `PROVENANCE.md` here lists every file of that directory with its md5, and which of them equal a `git show 2632277f:` blob.

Evidence for ledger row `holdphase`, whose `hold_question` asks whether discharging a
`[HELD AWAITING SEAT: <seat>]` marker should need an answer in the SAME PHASE, or whether a
later answer from the same seat in ANY phase may discharge it.

**Provenance.** Everything here was read from `HEAD` = `2632277f` only:
`git show HEAD:tools/pipeline/ledger.json` (blob `034d928d2d56`, extracted copy md5 `c2886383`),
and the HEAD copies of `stage_tokens.py` (`fbf894306549`), `check_stage_panels.py`
(`0a5640db3030`), `check_fable_queue.py` (`51e41e28711f`) and `gen_codex_wall.py`
(`d1f265932f06`). The working-tree ledger is modified against HEAD and was not read. The
numbers come from `analyze.py` in this directory; its output `analysis.out` ends with its
completion line `HOLDPHASE_ANALYSIS_DONE`. No gate, probe, build, panel or tool `main()` was run.

**How this file was checked.** `assemble.py` builds this file from a template and the generated tables. It refuses to write the file unless three things hold:
* every hand-typed number is found in `analysis.out`;
* every quote is found in the HEAD ledger or a HEAD tool;
* every attribution to a named entry (40) is found in that entry, with the stated phase and seat.

It was shown to fail on a changed number, and on a quote moved to a phrase that exists elsewhere in the ledger.

**Terms.**
* A **marker** is an entry whose `note` contains `[HELD AWAITING SEAT:` -- `is_held()`,
  `stage_tokens.py:53-54`. Defanged spellings such as `(HELD-AWAITING-SEAT ... -- defanged)` are not markers.
* A **marker-seat** is one marker paired with one seat it names. One marker can name several seats. This is the unit both rules decide.
* **Discharge test, both rules.** This is `live_holds()`'s own test, `stage_tokens.py:106-107`. An entry on the same row discharges the hold when all three hold:
  * its `seat` is the named seat;
  * `is_answer()` is true -- the note carries none of the HELD, NOT-A-SEAT-ANSWER, PRE-POLICY or NO-PANEL tokens (`:65-69`);
  * its `date` is later than the marker's: `>`, never `>=`.
* **SAME-PHASE** looks only at the marker's own phase, which is how all three tools call it. **ANY-PHASE** looks at the whole row.
* Neither rule tests length, because no tool does; section 4 measures what that leaves out.
* **Cross-check.** This file's SAME-PHASE result equals `st.live_holds()` on every stage that carries a marker: 92 stages compared, 0 mismatches.

## 1. Counts

| unit | total | SAME-PHASE | ANY-PHASE | differ |
|---|---|---|---|---|
| marker-seat | 141 | 104 live, 37 discharged | 93 live, 48 discharged | **11 of 141** |
| distinct (row, phase, seat) | 130 | 97 live | 87 live | 10 of 130 |
| stage (row, phase) carrying a marker | 92 | 81 with a live hold | 73 with a live hold | 8 of 92 |

The 141 marker-seats come from 122 marker entries (one literal each) on 62 rows. No marker is malformed, and none names a seat outside the 9-seat roster.

Not one marker-seat is discharged under SAME-PHASE and live under ANY-PHASE (0 of 141). ANY-PHASE can only add discharges.

Per marker phase. Each cell is a count of that phase's marker-seats:

| phase | marker-seats | SAME-PHASE discharged | ANY-PHASE discharged | differ |
|---|---|---|---|---|
| assess | 23 | 15 | 21 | **6** |
| design | 11 | 5 | 9 | **4** |
| regress | 36 | 1 | 2 | **1** |
| research | 21 | 2 | 2 | 0 |
| review | 50 | 14 | 14 | 0 |

**Where the literal sits.** The literal appears 132 times in the whole ledger file:

* **122 of 132** in `entry.note`. These are the markers.
* **10 of 132** in fields no tool reads:
  * 6 of the 10 copy a marker that already sits in the same entry's note (`ev` 1, `outcome_note` 4, `outcome` 1);
  * 2 of the 10 are in `lcabadval` entry [5] (`ev`, `outcome_note`), whose note was defanged *"answered later in this stage"*;
  * 2 of the 10 are prose in `ledgerstatelies`'s `state_note`.

**The date rule, for the record.** That rule is settled; it is listed only because it still bites. Under `>=` instead of `>`, SAME-PHASE would discharge 43 of 141 (not 37). The 6 of 141 that flip are same-date siblings, all review/fable5:
* `wiringcliff` [55];
* `ip30abortkill` [55];
* `cxlaunchquotation`, two markers;
* `dashokclass`;
* `fableheldform` [11].

**Hand practice, as context only.** These are defanged copies, so they are not markers. The parser `\(HELD-AWAITING-SEAT[ /]+<seats>` reads 49 of the 50 notes that spell `HELD-AWAITING-SEAT`. The four `[was: HELD AWAITING SEAT ...]` spellings are not parsed.

Of the 87 parsed (entry, seat) pairs:
* **85 of 87** have an answer by that seat in the same phase:
  * 49 dated strictly later;
  * 36 on the same date only.
* **1 of 87** has only an other-phase answer: `n6` [4] assess/fable5.
* **1 of 87** has none: `gdromwarnbits` [12], removed because *"the stage was already 9/9 when I added it"*.

## 2. The differing set -- live under SAME-PHASE, discharged under ANY-PHASE (11 of 141)

The marker entry and every discharging entry are on the same row, from the same seat, dated strictly later, and pass `is_answer()`. The full text of every discharging entry is in `analysis.out` section 8, and one line per pair is in `differing.tsv`.

| # | row (state) | phase | seat | marker date [entry] | later entries by that seat, other phases: [entry] phase date (chars) opening words |
|---|---|---|---|---|---|
| 1 | wdccdbmidxfer (held) | regress | fable5 | 2026-08-27 [26] | [27] research 2026-08-29 (3654) "VERDICT: (1) OPTION C WAS NOT WRONGLY DISMISSED, AND MY QUESTION WAS M..."; [28] assess 2026-08-29 (1585) "MY MARKER SWEEP MANUFACTURED A SEAT ANSWER ON THIS ROW, AND IT IS THE..." |
| 2 | wiringcliff (in work) | design | fable5 | 2026-10-18 [28] | [54] review 2026-10-20 (926) "LATE REVIEW of #565's records (rldiclf2, items A0-A6). Fable 5.1: ADOP..." |
| 3 | wiringcliff (in work) | design | fable5 | 2026-10-18 [41] | [54] review 2026-10-20 (926) "LATE REVIEW of #565's records (rldiclf2, items A0-A6). Fable 5.1: ADOP..." |
| 4 | sgirekills (held) | assess | kimi | 2026-08-30 [2] | [15] design 2026-09-08 (141) "STEP-1 RE-PIN DESIGN. the CRIME_RE_ defines and array declarations are..."; [23] review 2026-09-08 (184) "PASS 2 ON THE DIFF. Found the enum comment ("next free bit is 1 << 11;..."; [34] review 2026-09-08 (118) "PASS 4, the closing pass. THE OBJECTION THAT SURVIVED: only 2 of 11 al..."; +2 more (research 1, review 1) |
| 5 | sgirekills (held) | assess | opus5 | 2026-08-30 [2] | [18] design 2026-09-08 (98) "STEP-1 RE-PIN DESIGN. preserved for the 2026-09-09 adjudication per th..."; [27] review 2026-09-08 (63) "PASS 2 ON THE DIFF. preserved for the 2026-09-09 adjudication."; [37] review 2026-09-08 (69) "PASS 4, the closing pass. preserved for the 2026-09-09 adjudication."; +2 more (research 1, review 1) |
| 6 | pcc2widthkills (open) | assess | opus5 | 2026-08-31 [3] | [26] research 2026-09-03 (196) "SEAT DOWN: API 529 Overloaded on claude-opus-5, twice (first firing +..."; [36] review 2026-09-03 (2278) "THE BUILDER. 11 sentinel-verified probe runs in a scratch clone of bui..."; [38] review 2026-09-03 (1749) "THE BUILDER'S OWN PASS 3 ON THE REPAIR, run unprompted per the repair-..."; +10 more (review 10) |
| 7 | lcabadval (in work) | assess | opus5 | 2026-08-31 [3] | [27] research 2026-09-09 (1328) "Agent-tool MEASURING seat, the one-invocation rung-3 ask. Built regres..."; [34] review 2026-09-10 (1043) "Agent-tool MEASURING seat, two agents: TABLE 1 on the 40-row pre-repai..." |
| 8 | sgimtedepth4dead (in work) | assess | opus5 | 2026-09-07 [7] | [21] review 2026-09-09 (1839) "Agent-tool MEASURING seat; liveness token and file quote returned. Scr..." |
| 9 | sgimtedepth4dead (in work) | assess | fable5 | 2026-09-07 [8] | [22] review 2026-09-09 (3298) "ADJUDICATED BY THE MAIN LOOP RUNNING AS FABLE 5.1 (owner directive), o..." |
| 10 | alphatbinegsel (closed) | design | opus5 | 2026-09-08 [18] | [32] review 2026-09-10 (3405) "THE STRONGEST ANSWER OF THE DAY, and it was asked to be harder on this..."; [34] assess 2026-09-10 (2789) "THE ASSESS-STAGE FLAGSHIP READ, held for this seat since 2026-09-08 by..." |
| 11 | fableheldform (held) | design | fable5 | 2026-10-18 [3] | [10] review 2026-10-20 (641) "LATE REVIEW of this row's records (fhfp1, items B0-B7). Fable 5.1: ADO..." |

**What the ledger itself says about each one.** The quotes are from HEAD. The sorting into kinds is my reading of them.

1. **`wdccdbmidxfer` regress/fable5** -- the marker's own text says the any-phase discharge is wrong:
   > *"RESTORED 2026-08-29. My marker sweep DEFANGED this and should not have. The sweep's criterion was ROW-SCOPED ... so fable5's RESEARCH-phase answer of 2026-08-29 was taken to discharge this REGRESS-phase hold. It does not: regress is a FABLE-ONLY stage and fable5 has never answered it on this row."*

   Entry [28] is that restoration note. It is filed under `seat: fable5` and `is_answer()` counts it, but it is not an answer.
2. **and 3. `wiringcliff` design/fable5 [28], [41]** -- these are the #565 and #566 pass-1 design briefs, *"NOT FIRED"* and *"NOT TRIED"*.
   * [54] is a late review of #565's records.
   * The row's review-phase marker [55], dated 2026-10-20, says that answer *"answered neither"* of the held review questions.
4. **`sgirekills` assess/kimi** -- the later entries split into two kinds:
   * packet-fed answers to the step-1 design and to passes 2 and 4: [15], [23], [34];
   * *"NOT FIRED"* notes: [64], [65].
5. **`sgirekills` assess/opus5** -- **every** later opus5 entry is a non-firing note:
   * *"preserved for the 2026-09-09 adjudication"*: [18], [27], [37];
   * *"NOT FIRED"*: [60], [61].

   ANY-PHASE would discharge this hold on records saying the seat did not answer.
6. **`pcc2widthkills` assess/opus5** -- the later entries are 12 review-phase passes on the detector plus a research *"SEAT DOWN"* note, [26]. The row's `hold_question` says *"No question remains held; what remains is the ROUND"*. This is a hold SAME-PHASE keeps although it looks moot.
7. **`lcabadval` assess/opus5** -- there are two later entries:
   * a research-phase rung-3 probe build, [27];
   * a review-phase kill-table measurement, [34].
8. **and 9. `sgimtedepth4dead` assess/opus5 [7] and assess/fable5 [8]** -- both holds name *"the load-bearing one is 7g-1"*.
   * The review-phase measurement [21] (`killtable3_20260909`) and ruling [22] (*"THE LABELS ARE FLOOR CELLS HERE"*) address 7g-1.
   * They discharged the matching review-phase holds [16]/[17] under SAME-PHASE.
   * The assess copies stay live: the 7g questions are held in two phases and answered in one.
10. **`alphatbinegsel` design/opus5, row CLOSED** -- opus5 later answered in review, [32], and in assess, [34].
    * [34] discharged the assess hold; its defanged copy [8] reads *"DISCHARGED by the assess answer below"*.
    * Under SAME-PHASE the design hold [18] stays live on a closed row.
    * No gate evaluates design holds (section 3).
11. **`fableheldform` design/fable5** -- the pass-1 design brief was walled.
    * [10] is a late review of the row's records.
    * The review-phase marker [11], dated 2026-10-20, restates hold question (3) as still owed. It says whether [10] discharges it *"is the adjudicator's to say"*.

**By kind:**
* **7 of 11** are answers to other stages of the same row's work: #1, #4, #6, #7, #8, #9, #10. Of these 7:
  * the ledger rejects #1 in its own words;
  * #6, #8 and #9 look answered or moot elsewhere.
* **3 of 11** are late records reviews: #2, #3, #11.
* **1 of 11** rests only on non-firing notes: #5.

**A structural fact the ledger states itself**, in its three 2026-10-20 RESTATED markers (this wording is `wiringcliff` [55]'s):
> *"stage_tokens.live_holds() discharges every earlier fable5 hold in a stage on any later-dated fable5 answer"*

The test matches seat and date, never the question asked. SAME-PHASE confines that to one stage; ANY-PHASE would extend it to the whole row.

## 3. The three tools -- which rule each one actually implements

| tool | where the decision is made | date | phase | real length | what it never evaluates |
|---|---|---|---|---|---|
| `stage_tokens.py` (shared) | `live_holds()` `:87-110`; the test at `:106-107` | `>` (`:107`) | whatever list the caller passes | **not tested**: `is_answer()` `:65-69` checks tokens only | a malformed marker is never discharged (`:98-104`) |
| `check_stage_panels.py` | per-phase groups `:168`; `st.live_holds(...)` at `:197` and `:211`; comment `:206-207` *"not answered in this stage at a strictly later date"* | `>` | **SAME** (per-phase group) | not tested | everything outside `STAGES = ("assess", "research", "review")` (`:65`, `:190`): every `regress` and `design` hold, including the closed-row clause (`:198`, `:224`) |
| `check_fable_queue.py` | per-phase groups `:102-108`; `st.live_holds(d["all"])` at `:136` | `>` | **SAME** | not tested | `regress` (`:122`); stages with fewer than 2 answering seats (`:124`); stages fable5 answered (`:126`); valid exemptions (`:130`); stages before 2026-08-16 (`:132`) |
| `gen_codex_wall.py` | per-phase groups `:152-155`; a seat is listed only if it is in `live[phase]` (`:180-181`) | `>` | **SAME** | not tested | nothing by phase; it skips a marker not in the strict shape (`:157-159`), which `live_holds()` still holds as malformed |

*A fourth reader, not asked about, agrees: `gen_dashboard.py:148` groups by phase and `:154` calls `st.live_holds(stage)`.*

**Where they agree.** All three call the same function, so the test itself is identical in every tool:
* the date comparison is `>`;
* only the marker's own phase counts;
* there is no length test.

"Not itself a marker" is enforced through `is_answer()`, which is stricter in one way and looser in two:
* stricter: it also refuses NOT-A-SEAT-ANSWER, PRE-POLICY and NO-PANEL entries;
* looser: it accepts any untokened note as an answer, including "NOT FIRED", "SEAT DOWN" and "preserved for" notes and defanged copies.

**Where they disagree: scope.** The table covers the 97 live (row, phase, seat) holds at HEAD under SAME-PHASE:

| tool | live holds it evaluates (of 97) | not evaluated |
|---|---|---|
| `check_stage_panels.py` | 57 | 40: every `regress` and `design` hold (`:65`, `:190`) |
| `check_fable_queue.py` | 20 | 77: fable5 answered (:126) 42, regress (:122) 35 |
| `gen_codex_wall.py` | 97 | 0 |

* **24 of the 97** live holds sit on CLOSED rows: 23 regress, 1 design. `check_stage_panels.py` flags **0 of the 24** with its closed-while-held clause, because neither phase is evaluated.
* For regress this is by design: a closed row owes its regress review afterwards, and both gates leave regress out on purpose (`check_stage_panels.py:17`, `:65`; `check_fable_queue.py:122-123`, *"flagship-only by directive; rule 3 covers its absence"*). So a live regress hold is recorded only by the wall.
* The one design hold is `alphatbinegsel`/opus5, item 10 above. It is a non-regress hold on a closed row that only the wall reports.
* Two differences are latent, with 0 instances at HEAD:
  * the wall skips a malformed marker, while the other two hold it;
  * the wall lists an unknown seat name without any discharge test (`:172-181`).

## 4. The "real length" clause

No tool tests length. Under SAME-PHASE, 37 of 141 marker-seats are discharged. For each one, take the longest note among its discharging entries: the shortest of those is 42 characters, the median 963. **3 of the 37** rest only on notes under 100 characters:

* `lcabadval` [3] assess/grok, by [18] (42 chars): *"ASSESS PANEL. MANUAL_brief, file-reading."*
* `lcabadval` [3] assess/kimi, by [20] (78 chars): *"ASSESS PANEL. PACKET_brief (kimi-k3:cloud substitute; the CLI is 403-walled)."*
* `armbfxwidth32` [8] assess/fable5, by [24] (70 chars): *"Discharged with the review ruling above (same reading, same residual)."*

The first two read as terse records of real answers. The third is a same-phase pointer to a review-phase ruling: in effect, a cross-phase discharge written down inside the held phase.

A character threshold would refuse all three. So "real length" cannot be made a number. What it guards against is a note with no token that is not an answer, and `is_answer()` accepts such notes. Items 1, 4, 5 and 6 above show it. ANY-PHASE widens the pool such notes come from; item 5 rests on them entirely.

Defanged copies: they are the only discharging entries for 0 of the 37 SAME-PHASE discharges and 0 of the 11 ANY-PHASE-only ones.

## 5. What switching the shared `live_holds()` to ANY-PHASE would do

These are the stages that hold a differing marker-seat. Each tool's output is shown first under today's rule, then under ANY-PHASE. The classification reproduces the cited lines; the tools themselves were not run.

| stage | row state | live, same -> any | `check_stage_panels` | `check_fable_queue` | `gen_codex_wall` |
|---|---|---|---|---|---|
| alphatbinegsel / design | closed | opus5 -> - | not evaluated | not evaluated | opus5 -> **(not listed)** |
| fableheldform / design | held | fable5 -> - | not evaluated | HELD -> **FAIL short, not held** | fable5 -> **(not listed)** |
| lcabadval / assess | in work | opus5 -> - | HELD 7/9 -> **FAIL incomplete 7/9** | not evaluated | opus5 -> **(not listed)** |
| pcc2widthkills / assess | open | opus5 -> - | HELD 8/9 -> **FAIL incomplete 8/9** | not evaluated | opus5 -> **(not listed)** |
| sgimtedepth4dead / assess | in work | opus5,fable5 -> - | HELD 7/9 -> **FAIL incomplete 7/9** | HELD -> **FAIL short, not held** | fable5,opus5 -> **(not listed)** |
| sgirekills / assess | held | kimi,opus5 -> - | HELD 7/9 -> **FAIL incomplete 7/9** | not evaluated | kimi,opus5 -> **(not listed)** |
| wdccdbmidxfer / regress | held | fable5 -> - | not evaluated | not evaluated | fable5 -> **(not listed)** |
| wiringcliff / design | in work | fable5 -> - | not evaluated | not evaluated | fable5 -> **(not listed)** |

Stages whose output changes: check_stage_panels 4 of 8, check_fable_queue 2 of 8, gen_codex_wall 8 of 8.

**Why the failures appear.** Seat tallies stay per-phase (`check_stage_panels.py:184-188`, `check_fable_queue.py:116-119`). An ANY-PHASE discharge therefore takes the hold off a short stage without adding the seat to it.
* `check_stage_panels.py` records a violation at `:250` and reports the stage as one that *"moved on without the full panel"* (`:291`).
* `check_fable_queue.py` records it at `:143` and prints that it *"ran with N seats and NO flagship seat, and is not held"* (`:168`).

**The regress hold.** `wdccdbmidxfer`'s regress hold would leave the wall. The other two tools never read regress holds, so no tool would record it.

## 6. Packet for the reviewer (rule without opening a file)

> Row holdphase: is a HELD marker (seat S, phase P, date D) discharged only by S's answer in P
> dated after D (SAME), or in any phase (ANY)?
>
> HEAD 2632277f: 122 markers name 141 marker-seats; SAME leaves 104 live, ANY 93. The 11
> differing sit in 8 stages: assess 6, design 4, regress 1, research/review 0. Their later
> other-phase entries: answers to other stages (7), late records reviews (3), only non-firing
> notes (1). Of the 7, the regress hold's own marker says a row-scoped sweep wrongly cleared it;
> three look answered or moot elsewhere (sgimtedepth4dead ×2, pcc2widthkills).
>
> The test cannot tell which question an answer addresses; ANY widens that from one stage to the
> row. Under ANY, check_stage_panels would fail 4 stages and check_fable_queue 2 (seat tallies
> stay per-phase); gen_codex_wall drops all 8.
>
> All three tools implement SAME, '>', no length test.

## Files in this directory  [durable copy: "this directory" is the scratch original `_scratchpad/wholdphase/`; four of these files are copied here -- see the banner and `PROVENANCE.md`]

* `analyze.py` -- the deriver. It reads only `ledger_HEAD.json` and `HEAD_stage_tokens.py`, and imports the classification from the latter.
* `analysis.out` -- every count above, plus the full text of each discharging entry (section 8).
* `markers.tsv` -- one line per marker-seat, 141 lines.
* `differing.tsv` -- one line per (differing marker-seat, discharging entry) pair.
* `frag_*.md` -- the generated tables pasted into this file.
* `EVIDENCE.template.md` and `assemble.py` -- the hand-written text and the script that builds this file from it, with the checks described under Provenance.
* `ledger_HEAD.json` and `HEAD_*.py` -- the HEAD copies everything was read from.

## Appendix -- all 141 marker-seats, both rules

`dis [j] phase date` gives the first discharging entry; `live` means none.

```
row                  entry phase     seat      date       state    SAME-PHASE                   ANY-PHASE
ns16550              [11]  regress   fable5    2026-08-22 closed   live                         live
xfamscope            [11]  regress   fable5    2026-10-02 closed   live                         live
carrier              [9]   regress   fable5    2026-08-22 closed   live                         live
fbwitness            [9]   regress   fable5    2026-10-02 closed   live                         live
ledgerwitness        [9]   regress   fable5    2026-10-02 closed   live                         live
smhang               [12]  regress   fable5    2026-10-02 closed   live                         live
es438                [11]  regress   fable5    2026-08-22 closed   live                         live
fbsmlane             [10]  regress   fable5    2026-09-19 closed   dis [11] regress 2026-10-09  dis [11] regress 2026-10-09
sh4sci               [18]  regress   fable5    2026-08-22 closed   live                         live
gdromcondlies        [38]  regress   fable5    2026-08-30 closed   live                         live
proberowsubset       [12]  assess    codex     2026-08-29 open     dis [13] assess 2026-09-08   dis [13] assess 2026-09-08
asiceventaddr        [9]   review    fable5    2026-09-18 open     dis [11] review 2026-10-09   dis [11] review 2026-10-09
asiceventaddr        [9]   review    opus5     2026-09-18 open     dis [12] review 2026-10-09   dis [12] review 2026-10-09
asiceventaddr        [9]   review    deepseek  2026-09-18 open     dis [13] review 2026-10-09   dis [13] review 2026-10-09
wdcrearmzero         [8]   review    opus5     2026-09-18 held     dis [10] review 2026-10-09   dis [10] review 2026-10-09
wdcrearmzero         [8]   review    fable5    2026-09-18 held     dis [9] review 2026-10-09    dis [9] review 2026-10-09
wdccdbmidxfer        [18]  research  opus5     2026-08-27 held     live                         live
wdccdbmidxfer        [26]  regress   fable5    2026-08-27 held     live                         dis [27] research 2026-08-29
wdcdataoutdrain      [9]   regress   fable5    2026-08-27 closed   live                         live
wiringcliff          [28]  design    fable5    2026-10-18 in work  live                         dis [54] review 2026-10-20
wiringcliff          [32]  review    fable5    2026-10-18 in work  dis [54] review 2026-10-20   dis [54] review 2026-10-20
wiringcliff          [41]  design    fable5    2026-10-18 in work  live                         dis [54] review 2026-10-20
wiringcliff          [48]  review    fable5    2026-10-18 in work  dis [54] review 2026-10-20   dis [54] review 2026-10-20
wiringcliff          [55]  review    fable5    2026-10-20 in work  live                         live
sgirekills           [2]   assess    codex     2026-08-30 held     dis [6] assess 2026-09-06    dis [6] assess 2026-09-06
sgirekills           [2]   assess    grok      2026-08-30 held     dis [9] assess 2026-09-07    dis [9] assess 2026-09-07
sgirekills           [2]   assess    kimi      2026-08-30 held     live                         dis [15] design 2026-09-08
sgirekills           [2]   assess    opus5     2026-08-30 held     live                         dis [18] design 2026-09-08
sgirekills           [45]  research  fable5    2026-10-17 held     live                         live
sgirekills           [49]  review    fable5    2026-10-17 held     live                         live
sgirekills           [56]  review    fable5    2026-10-18 held     live                         live
sgirekills           [72]  regress   fable5    2026-10-18 held     live                         live
sgitexindex          [3]   assess    codex     2026-08-31 open     dis [16] assess 2026-09-07   dis [16] assess 2026-09-07
sgitexindex          [3]   assess    grok      2026-08-31 open     dis [18] assess 2026-09-08   dis [18] assess 2026-09-08
sgitexindex          [3]   assess    kimi      2026-08-31 open     dis [22] assess 2026-09-08   dis [22] assess 2026-09-08
sgitexindex          [3]   assess    opus5     2026-08-31 open     live                         live
sgitexindex          [3]   assess    fable5    2026-08-31 open     dis [13] assess 2026-09-02   dis [13] assess 2026-09-02
sgidewidth           [18]  regress   fable5    2026-08-31 closed   live                         live
sgireunmapped        [9]   regress   fable5    2026-08-31 closed   live                         live
holdmarkermulti      [9]   regress   fable5    2026-08-30 closed   live                         live
sgideprimop          [65]  regress   fable5    2026-09-05 closed   live                         live
pcc2widthkills       [3]   assess    opus5     2026-08-31 open     live                         dis [26] research 2026-09-03
pcc2widthkills       [3]   assess    fable5    2026-08-31 open     dis [15] assess 2026-09-01   dis [15] assess 2026-09-01
lcabadval            [3]   assess    codex     2026-08-31 in work  dis [6] assess 2026-09-06    dis [6] assess 2026-09-06
lcabadval            [3]   assess    grok      2026-08-31 in work  dis [18] assess 2026-09-08   dis [9] design 2026-09-07
lcabadval            [3]   assess    kimi      2026-08-31 in work  dis [20] assess 2026-09-08   dis [12] design 2026-09-07
lcabadval            [3]   assess    opus5     2026-08-31 in work  live                         dis [27] research 2026-09-09
lcabadval            [3]   assess    fable5    2026-08-31 in work  dis [24] assess 2026-09-09   dis [15] design 2026-09-07
pcc2c040kill         [16]  assess    fable5    2026-09-08 open     dis [25] assess 2026-09-09   dis [25] assess 2026-09-09
pcc2c040kill         [17]  design    fable5    2026-09-08 open     dis [26] design 2026-09-09   dis [25] assess 2026-09-09
pcc2c040kill         [18]  review    fable5    2026-09-08 open     dis [27] review 2026-09-09   dis [25] assess 2026-09-09
m88kexcdeliver       [113] regress   fable5    2026-10-16 closed   live                         live
m88kexcrrtrapmode    [9]   regress   fable5    2026-10-02 closed   live                         live
sgirandomcolour      [28]  review    fable5    2026-10-18 held     live                         live
sgirandomcolour      [32]  review    fable5    2026-10-18 held     live                         live
sgirandomcolour      [34]  regress   fable5    2026-10-18 held     live                         live
sgimtedepth4dead     [7]   assess    opus5     2026-09-07 in work  live                         dis [21] review 2026-09-09
sgimtedepth4dead     [8]   assess    fable5    2026-09-07 in work  live                         dis [22] review 2026-09-09
sgimtedepth4dead     [16]  review    opus5     2026-09-07 in work  dis [21] review 2026-09-09   dis [21] review 2026-09-09
sgimtedepth4dead     [17]  review    fable5    2026-09-07 in work  dis [22] review 2026-09-09   dis [22] review 2026-09-09
m88kexcdetectorl2    [2]   design    fable5    2026-09-07 open     dis [3] design 2026-09-09    dis [3] design 2026-09-09
alphavmkill          [12]  research  fable5    2026-09-19 in work  live                         live
alphaswpctxreg       [7]   design    opus5     2026-09-08 open     live                         live
alphaswpctxreg       [8]   design    fable5    2026-09-08 open     dis [11] design 2026-09-09   dis [11] design 2026-09-09
alphatbinegsel       [3]   assess    fable5    2026-09-08 closed   dis [20] assess 2026-09-09   dis [20] assess 2026-09-09
alphatbinegsel       [18]  design    opus5     2026-09-08 closed   live                         dis [32] review 2026-09-10
alphatbinegsel       [19]  design    fable5    2026-09-08 closed   dis [22] design 2026-09-09   dis [20] assess 2026-09-09
armbfxwidth32        [7]   assess    opus5     2026-09-07 in work  live                         live
armbfxwidth32        [8]   assess    fable5    2026-09-07 in work  dis [24] assess 2026-09-09   dis [23] review 2026-09-09
armbfxwidth32        [16]  review    opus5     2026-09-07 in work  live                         live
armbfxwidth32        [17]  review    fable5    2026-09-07 in work  dis [23] review 2026-09-09   dis [23] review 2026-09-09
lcaconfbus1kill      [12]  review    opus5     2026-09-08 open     live                         live
armbfiwidth          [10]  design    opus5     2026-09-08 open     live                         live
armbfiwidth          [11]  design    fable5    2026-09-08 open     dis [12] design 2026-09-09   dis [12] design 2026-09-09
mapledmaaddr         [50]  review    fable5    2026-10-18 held     live                         live
mapledmaaddr         [51]  regress   fable5    2026-10-18 held     live                         live
xscaleinten          [21]  review    fable5    2026-10-18 held     live                         live
xscaleinten          [23]  regress   fable5    2026-10-18 held     live                         live
vmedefaultkill       [7]   research  opus5     2026-10-20 held     live                         live
vmedefaultkill       [8]   research  agy       2026-10-20 held     live                         live
vmedefaultkill       [9]   research  kimi      2026-10-20 held     live                         live
vmedefaultkill       [10]  research  deepseek  2026-10-20 held     live                         live
vmedefaultkill       [11]  research  minimax   2026-10-20 held     live                         live
vmedefaultkill       [24]  review    opus5     2026-10-21 held     live                         live
vmedefaultkill       [25]  review    agy       2026-10-21 held     live                         live
vmedefaultkill       [26]  review    kimi      2026-10-21 held     live                         live
vmedefaultkill       [27]  review    deepseek  2026-10-21 held     live                         live
vmedefaultkill       [28]  review    minimax   2026-10-21 held     live                         live
vmedefaultkill       [29]  regress   fable5    2026-10-21 held     live                         live
ppcrldimimask        [21]  review    fable5    2026-10-18 held     live                         live
ppcrldimimask        [24]  regress   fable5    2026-10-18 held     live                         live
ppcrlwimiwidth       [21]  review    fable5    2026-10-18 held     live                         live
ppcrlwimiwidth       [24]  regress   fable5    2026-10-18 held     live                         live
ppcgateimageskip     [3]   review    fable5    2026-10-18 held     live                         live
ppcgateimageskip     [11]  regress   fable5    2026-10-18 held     live                         live
ip30abortkill        [50]  review    fable5    2026-10-18 held     dis [54] review 2026-10-20   dis [54] review 2026-10-20
ip30abortkill        [55]  review    fable5    2026-10-20 held     live                         live
scorehyphenfp        [1]   regress   fable5    2026-10-02 closed   live                         live
boilerplateprefix    [1]   regress   fable5    2026-10-02 closed   live                         live
lcalenzerodrop       [34]  regress   fable5    2026-10-02 closed   live                         live
fbctrlcmdkill        [4]   research  fable5    2026-10-18 held     live                         live
fbctrlcmdkill        [8]   review    fable5    2026-10-19 held     live                         live
fbctrlcmdkill        [12]  review    fable5    2026-10-19 held     live                         live
fbctrlcmdkill        [16]  review    fable5    2026-10-19 held     live                         live
fbctrlcmdkill        [27]  regress   fable5    2026-10-19 held     live                         live
ppcllscrcexit        [21]  research  codex     2026-11-03 closed   dis [27] research 2026-11-04 dis [27] research 2026-11-04
nineseatreminder     [1]   regress   fable5    2026-10-02 closed   live                         live
shfcnvsdfpul         [10]  research  opus5     2026-11-03 held     live                         live
shfcnvsdfpul         [25]  review    opus5     2026-11-03 held     live                         live
cxlaunchdaybreak     [0]   regress   fable5    2026-10-17 closed   live                         live
cxlaunchquotation    [0]   regress   fable5    2026-10-17 held     live                         live
cxlaunchquotation    [26]  review    fable5    2026-10-17 held     live                         live
cxlaunchquotation    [30]  review    fable5    2026-10-17 held     live                         live
dashokclass          [29]  review    fable5    2026-10-17 held     live                         live
dashokclass          [33]  regress   fable5    2026-10-17 held     live                         live
fableheldform        [3]   design    fable5    2026-10-18 held     live                         dis [10] review 2026-10-20
fableheldform        [5]   review    fable5    2026-10-18 held     dis [10] review 2026-10-20   dis [10] review 2026-10-20
fableheldform        [11]  review    fable5    2026-10-20 held     live                         live
m88kscaledbyte       [4]   research  fable5    2026-10-23 held     live                         live
m88kscaledbyte       [13]  review    fable5    2026-10-23 held     live                         live
m88kscaledbyte       [22]  review    fable5    2026-10-23 held     live                         live
ppcdsformxo          [5]   research  fable5    2026-10-24 held     live                         live
ppcdsformxo          [16]  review    fable5    2026-10-24 held     live                         live
wdclbaaddr           [5]   research  fable5    2026-10-24 held     dis [22] research 2026-10-25 dis [22] research 2026-10-25
wdclbaaddr           [16]  review    fable5    2026-10-24 held     dis [23] review 2026-10-25   dis [22] research 2026-10-25
wdclbaaddr           [24]  research  kimi      2026-10-25 held     live                         live
wdclbaaddr           [24]  research  minimax   2026-10-25 held     live                         live
wdclbaaddr           [24]  research  opus5     2026-10-25 held     live                         live
wdclbaaddr           [25]  review    kimi      2026-10-25 held     live                         live
wdclbaaddr           [25]  review    minimax   2026-10-25 held     live                         live
wdclbaaddr           [25]  review    opus5     2026-10-25 held     live                         live
m88kbuserrregs       [4]   research  fable5    2026-10-23 held     live                         live
m88kbuserrregs       [15]  review    fable5    2026-10-24 held     live                         live
i8259eoiirr          [8]   research  agy       2026-10-25 held     live                         live
i8259eoiirr          [9]   research  fable5    2026-10-25 held     live                         live
i8259eoiirr          [29]  review    agy       2026-10-25 held     live                         live
i8259eoiirr          [30]  review    fable5    2026-10-25 held     live                         live
lecsrmask            [9]   research  fable5    2026-10-25 held     live                         live
lecsrmask            [21]  review    fable5    2026-10-25 held     live                         live
fmtattr              [27]  regress   fable5    2026-11-05 closed   live                         live
fmtmissarg           [1]   regress   fable5    2026-11-05 closed   live                         live
```
