# Reading task: #558 drafts consistency (reading 2) (Gemini web; 2026-10-06)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GX558TEXTS-88ed` on a line of its own.

## What is inlined

- `SECTION` - a draft section for a bug-queue file, recording an audit of a records commit by one reading seat.
- `CHANGELOG` - the draft changelog block for the same unit.
- `MSG` - the draft commit message.
- `LEDGER` - every ledger change the unit makes (three NEW rows, ten review entries on one row, one row's fields).

## What is being decided

Whether these four texts agree with each other and say nothing the others contradict.  Treat every sentence as a claim.

## Questions

1. Every number (flags, briefs, answers, entries, rows, files): does each text give the same number for the same thing?
2. The three NEW rows in LEDGER: does SECTION / CHANGELOG / MSG describe them (ids, severity, what they cover) exactly as
   LEDGER records them?  Any site, line number or carrier named differently between texts?
3. Does any text claim a check, seat answer or measurement that LEDGER does not record an entry for?
4. Any sentence that contradicts another sentence in any of the four texts.

---- SECTION (lines 1-61) ----
1 | 
2 | ## 2026-10-02 -- GXEMUL [087a90]: `#558` -- agy's audit of `#555`'s id-less table: 16 flags; one opened THREE MB89352 emulated-CPU-stop rows, the rest changed nothing
3 | 
4 | **What this is.**  `#555` gave ids to the prose entries of this file and committed its tables under
5 | `regress/artifacts/idless_20261002/`.  The owner's standing instruction (2026-10-02) is to keep agy busy on read-only
6 | audits and to take its FLAGS as facts to check while giving its agreement no weight.  Six briefs were generated from the
7 | committed tables (`regress/artifacts/idlessaudit_20261002/briefs/`; generator `mk_agy_idless2.py.txt`): two on the
8 | citations of the forty `#555` rows, three on the 104 passages `#555` points at an existing id, one on the 22 entries it
9 | ruled KEEP-AS-IS or UNSETTLED.  Five answered; `icite2_2` WALLED on launch (`error: Individual quota reached. Please upgrade your subscription to increase your limits. Resets in 101h48m29s.`).
10 | 
11 | | brief | agy's verdict | flagged items |
12 | |---|---|---|
13 | | `icite2_1` | 0 of 20 rows flagged, 0 not checked | -- |
14 | | `icite2_2` | SEAT WALLED (agy quota: Resets in 101h48m29s) | -- |
15 | | `ifiled2_1` | 4 of 35 passages flagged, 0 not checked | 15, 24, 26, 27 |
16 | | `ifiled2_2` | 0 of 35 passages flagged, 0 not checked | -- |
17 | | `ifiled2_3` | 1 of 34 passages flagged, 0 not checked | 28 |
18 | | `ikeep2` | 11 of 22 entries flagged, 0 not checked | 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18 |
19 | 
20 | **The 16 flags, read against the committed table** (`AGY_FLAGS_DISPOSITION.md`, v3; v1 was checked by GPT-6 Astra,
21 | `aconf_agyflags/codex_aconf_agyflags.txt`: 1 of 16 dispositions wrong -- the one wrong disposition is #27 below, and v1's framing of the
22 | eleven OWED flags as "clause-(e) debt that a live row exempts" was also wrong and is corrected):
23 | * **5 PARTLY** -- a passage pointed at an id that covers only part of it.  For four, the "left-out" item is
24 |   carried by a row the brief did not name: three filed by `#555` on the SAME queue lines (`qhscifssr`, `qhnetxlog`,
25 |   `qhslowifetch`) and one filed by `#554` from queue lines 18721-18722 (`armcp15cp14exits`, for #28's lines
26 |   16997-17000); the brief had named only the POINTER id, so agy read the pointer, found it partial, and said so --
27 |   correctly, of the pointer.  **The fifth (#27, passage 2616,
28 |   "dev_mb89352 fatal errors") is a real gap**: `qhm88kstops` carries ONE of the device's nine `cpu->running = 0` assignments (ten stop
29 |   messages: EXBF's write and read logging share one assignment).
30 | * **11 OWED** -- a KEEP-AS-IS entry whose work is not done at `c29a5fd3`.  All eleven are the entries `#555` kept
31 |   because an existing row already records the open work, in those words, in its own queue text; the carriers
32 |   (`armbfiwidth`, `mapledmaaddr`, `ppcrldimimask`, `xscaleinten`) are open or in work.  `#555` dropped nothing; whether a carrier owes its work is the carrier's question.
33 | 
34 | **The three rows this opens** -- Astra's finding (`aconf_agyflags`), grok's ruling (`grok/grok_mbstops.txt`: CONCEDE IN
35 | PART), Astra's confirmation against the source at `c29a5fd3` (`aconf_mbstops/codex_aconf_mbstops.txt`: CONFIRMED WITH CHANGES (3) -- correct reachability explanations, qualify carrier/title scope, and label evidence as source-only; retain three HIGH rows).  Of the
36 | nine `cpu->running = 0` assignments in `src/devices/dev_mb89352.c`, `:146` is `qhm88kstops`, `b120` carries the unknown-CDB producer omission and its empty-status
37 | consequence at `:176`, `:290` is dead; the rest, three fix shapes, three rows, each HIGH by the `qhm88kstops` grade, each saying that its reachability
38 | is established by source inspection at `c29a5fd3`; no runtime witness was measured:
39 | 
40 | #### `qhmbphasestops` (HIGH, filed by #558) -- An MB89352 data-register access, with a transfer object and a nonzero count, in a phase unsupported for the access direction stops the emulated CPU
41 | SITES (c29a5fd3, src/devices/dev_mb89352.c): :169 (DREG read, phase outside DATAIN/STAT/MSGIN) and :235 (DREG write, phase outside DATAOUT/CMD).  :290 (the end-of-write default:) is UNREACHABLE: the first switch returns only for unsupported phases, and DATAOUT/CMD break, reach the second switch with no intervening phase change, and exhaust its supported cases.  PREREQUISITES: every DREG helper call needs a NONZERO count before decrement (a zero-count access only warns) and these guards additionally need a transfer object -- 'unconditional' means independent of the abort flag, nothing more.  REACHED BY (by reading, not measured): SCMD/PCTL give the guest control of the phase.  FIX SHAPE: keep the CPU running while KEEPING the helper's early return (:170 / :236) -- the treatment #186 gave the XFR command at :507.
42 | #### `qhmbunimplstops` (HIGH, filed by #558) -- An MB89352 access with a non-byte length, an unhandled SCMD write, or the EXBF register stops the emulated CPU while mb89352_abort_on_unimplemented_stuff is fixed true
43 | SITES (c29a5fd3, src/devices/dev_mb89352.c): :312 (len != 1: a halfword or word callback access), :533 (an SCMD WRITE outside {0x00, 0x20, 0x84, 0x8c, 0xc0} unless bit 0x10 rewrites it to BUS_REL -- an SCMD read does not execute this switch), and EXBF, register index 15: WRITE logging at :676 and READ logging at :683 converge on the ONE assignment at :690.  All gated by const bool mb89352_abort_on_unimplemented_stuff = true (:61), so live; the shared fixed-true policy is what groups them.  REACHED BY (by reading, not measured): those accesses from the guest's register interface.  FIX SHAPE: the warning branch the flag already selects; clearing the flag leaves all five live unconditional DREG assignments (:146, :169, :176, :235, :242; :290 is dead) intact.  NOT mb89352halt's stop: that dropped row's record names the disk dispatcher's CDB default: and the controller's status-length guard, not :533.
44 | #### `qhmbbufendstops` (HIGH, filed by #558) -- An MB89352 data-register access at or past the end of the selected buffer, in a phase supported for the access direction, stops the emulated CPU
45 | SITES (c29a5fd3, src/devices/dev_mb89352.c): :176 (DREG read, transfer_bufpos >= len against the selected DATAIN, STAT or MSGIN buffer -- read completion changes phase WITHOUT resetting the cursor, so a subsequent nonempty buffer can meet this guard, not only the original DATAIN buffer) and :242 (DREG write: reachable through empty or unprepared outgoing-buffer states; an exact fill runs completion and can change phase so a further write reaches :235 instead).  PREREQUISITES: a transfer object and a nonzero count, as for the phase guards (the count prerequisite applies to every DREG helper call; the :146 stop is the case with NO transfer object).  CARRIERS OF THE REST: b120 carries the unknown-CDB producer omission and its empty-status consequence; this row's residual is every OTHER empty-buffer path and every nonempty-buffer case.  FIX SHAPE: keep the bounds protection and refuse the access or handle phase completion -- removing the guard exposes the indexed accesses at :180 / :246 -- a CONTROLLER fix; b120 remains the PRODUCER fix.
46 | 
47 | **What else changes: nothing in the queue text or the other ledger rows.**  The brief generator's defect -- a passage
48 | with both a pointer and a new row listed with the pointer alone -- is recorded and not re-run: agy is walled until
49 | 2026-10-07 by its own message and the fix is one column.  `icite2_2`'s twenty rows (the ones the first agy set had not
50 | reached) are unaudited by agy; Astra's own passes read the whole table before `#555` shipped (`ifile_04`: 128/128
51 | rows), so the gap is a missing second reader.
52 | 
53 | **Also in this commit:** the committed ledger's `boilerplateprefix` commits field, left for "the next commit" by
54 | `#557`'s post step, is filled with `e1871fa5`, and -- the row being closed WITH commits from then on -- it gets the
55 | regress `[HELD AWAITING SEAT: fable5]` entry and `hold_question` that section I's rule 3 asks for (found by `#557`'s
56 | post-commit check of the working ledger).
57 | 
58 | **Seats, by name.**  agy (gemini-3.8-flash-high): five of six briefs, one WALLED.  GPT-6 Astra (codex, `ultra`): the
59 | check of the disposition, the confirmation of grok's ruling.  grok (grok-4.7 xhigh): the ruling on Astra's finding.
60 | The Fable and Opus agent seats were deliberately not fired (owner instruction, 2026-10-02); kimi down; Ollama not fired.
61 | 

---- CHANGELOG (lines 1-43) ----
1 | # `#558` (idlessaudit): agy's read-only audit of `#555`'s committed table -- 16 flags; one opens three MB89352 emulated-CPU-stop rows (HIGH), the rest change nothing; `boilerplateprefix`'s commits field filled
2 | 
3 | **Why.**  The owner's instruction of 2026-10-02 is to keep agy on read-only audits and to CHECK its flags.  `#555`
4 | (`c29a5fd3`) was the largest records commit of the week -- 130 table rows and 37 ledger rows (36 rows plus the class row
5 | `idlesslow`), 104 pointed
6 | passages, 18 entries kept as they were and 4 left UNSETTLED -- read by grok and Astra, and in part by agy's first set
7 | (`icite_01`..`icite_03`); this second agy set was to read the forty rows that set had not reached (it read twenty: `icite2_2`'s twenty walled),
8 | the passages and the kept entries.
9 | 
10 | **How.**  Six briefs generated from the committed tables (`regress/artifacts/idlessaudit_20261002/briefs/`,
11 | `mk_agy_idless2.py.txt`), run through the agy pack runner at MAXJ 2.  Five answered; `icite2_2` walled on launch
12 | (`error: Individual quota reached. Please upgrade your subscription to increase your limits. Resets in 101h48m29s.`) and the runner, which would have slept until the stated reset, was stopped.  agy flagged 16 items; each was
13 | checked by the main loop against `IDLESS_TABLE2.tsv` and the ledger at `c29a5fd3` (`AGY_FLAGS_DISPOSITION.md`), the
14 | disposition was put to GPT-6 Astra as "which of the sixteen is wrong?" (1 of 16 dispositions wrong), Astra's one finding went to grok for a
15 | ruling (the owner's arrangement: grok rules Astra's findings, Astra confirms), and Astra confirmed the ruling against
16 | the source (CONFIRMED WITH CHANGES (3) -- correct reachability explanations, qualify carrier/title scope, and label evidence as source-only; retain three HIGH rows).
17 | 
18 | **What the flags were.**  5 PARTLY: the `ifiled2` briefs listed, per passage, the id `#555` POINTS it at; where
19 | `#555` also FILED a new row on the same lines, the pointer alone was listed, so agy correctly found the pointer partial.
20 | For four, rows the brief did not name carry every "left-out" item (`qhscifssr`, `qhnetxlog`, `qhslowifetch` filed by
21 | `#555` on the same lines; `armcp15cp14exits` filed by `#554` from lines 18721-18722).  For the fifth -- queue passage 2616, "dev_mb89352
22 | fatal errors" -- `qhm88kstops` names ONE of the device's nine `cpu->running = 0` assignments, and beyond `b120`'s unknown-CDB producer omission and
23 | its empty-status consequence no row names the residual.
24 | 11 OWED: the `ikeep2` brief asked for OWED on any KEEP-AS-IS entry whose work is undone, "whatever the ruling
25 | says"; the eleven are exactly the entries `#555` kept because an existing row records the open work in its own text
26 | (`armbfiwidth`, `mapledmaaddr`, `ppcrldimimask`, `xscaleinten`).  Nothing is owed by `#555` for them.  (The disposition's first draft called them "clause-(e) debt under a live
27 | row, which owes nothing"; Astra corrected that framing -- clause (e) distinguishes a declared exclusion from a breach,
28 | and a live row exempts nothing -- and v2 and v3 state the test that was actually applied.)
29 | 
30 | **What ships.**  `tools/pipeline/ledger.json`, `matrix.html` -- three new rows after `qhm88kstops` (`qhmbphasestops`, `qhmbunimplstops`, `qhmbbufendstops`, HIGH,
31 | open; sites, reaching paths, carriers and fix shapes in their notes, reachability marked as a reading); ten entries on
32 | `idlesslow` (one per agy brief including the wall, Astra's check, grok's ruling, Astra's confirmation, the main-loop
33 | disposition); `boilerplateprefix.commits = e1871fa5` plus its regress hold (the field `#557`'s post step filled in the working ledger and
34 | left to this commit for the committed one).  `OUTSTANDING_BUGS.md` -- the `#558` section with the three rows.
35 | `regress/artifacts/idlessaudit_20261002/` -- 43 files: the briefs, the five answers, the wall's `.err` (kept because
36 | it is the whole answer), the disposition (v3), Astra's checks, grok's ruling, Astra's confirmation, the generator, the
37 | runner's results.
38 | 
39 | **Seats, by name.**  agy: five of six (one WALLED, a seat failure).  GPT-6 Astra: two checks and a confirmation; no
40 | wall, no refusal.  grok: one ruling.  Fable and Opus agent seats deliberately not fired (owner, 2026-10-02); kimi down;
41 | Ollama not fired.  No `src/` touched; no pass-2 receipt owed.
42 | 
43 | 

---- MSG (lines 1-17) ----
1 | #558 idlessaudit: agy's read-only audit of #555's committed table -- 16 flags; one opens three MB89352 emulated-CPU-stop rows (HIGH), the rest change nothing; boilerplateprefix's commits field filled
2 | 
3 | Six briefs generated from #555's committed tables; five answered, icite2_2 walled on launch (error: Individual quota reached. Please upgrade your subscription to increase your limits. Resets in 101h48m29s.).
4 | agy flagged 16 items: 5 PARTLY -- four carried by rows the brief had not named (qhscifssr, qhnetxlog,
5 | qhslowifetch filed by #555 on the same lines; armcp15cp14exits filed by #554), one real: queue passage 2616's "dev_mb89352 fatal errors" had ONE row (qhm88kstops) for
6 | nine cpu->running = 0 assignments; 11 OWED -- each recorded in its live carrier row's own queue text (`armbfiwidth`, `mapledmaaddr`, `ppcrldimimask`, `xscaleinten`), nothing owed
7 | by #555.  Astra checked the disposition (1 of 16 dispositions wrong); its one finding went to grok, who ruled CONCEDE IN PART (three rows
8 | owed, three fix shapes); Astra confirmed against the source (CONFIRMED WITH CHANGES (3) -- correct reachability explanations, qualify carrier/title scope, and label evidence as source-only; retain three HIGH rows).  Filed: `qhmbphasestops`, `qhmbunimplstops`, `qhmbbufendstops`, HIGH, reachability a reading.
9 | 
10 | Also: the committed ledger's boilerplateprefix commits field = e1871fa5 (#557's own sha, owed since #557's post step),
11 | with the regress hold section I then asks for.
12 | 
13 | Ten ledger entries on idlesslow; 43 artifact files.  No src/ touched.  Fable and Opus agent seats deliberately
14 | not fired (owner instruction).
15 | 
16 | Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
17 | 

---- LEDGER (lines 1-18) ----
1 | CHANGED  boilerplateprefix | fields: commits, entries, hold_question | commits: [] -> 'e1871fa5'
2 |     + entry: {"phase": "regress", "seat": "fable5", "date": "2026-10-02", "grade": "UNKNOWN", "grader": "", "ev": "not fired", "note": "[HELD AWAITING SEAT: fable5] boilerplateprefix closed with commits e1871fa5 (#557 landed its parked check_boilerplate.py repair) and so owes the REGRESS review, a distinct phase under the regress-is-fable-only directive.  Held by #558 (2026-10-02); the Fable agent seat is deliberately not fired (owner instruction, 2026-10-02), so the hold stands for the owner's batched flagship sign-off.  The question is in the row's hold_question."}
3 |     hold_question now: REGRESS (held 2026-10-02 by #558): does tools/pipeline/check_boilerplate.py as landed in e1871fa5 -- the comparison key is the whole seat note, EXCERPT = 60 display-only -- still catch the boilerplate it exists to catch at HEAD, and is its corrected comment true of the code?
4 | NEW  qhmbphasestops | HIGH | An MB89352 data-register access, with a transfer object and a nonzero count, in a phase unsupported for the access direction stops the emulated CPU | note: FILED BY #558 from queue passage 2616 at db8b1a33 ('#12 m88k CMMU / dev_mb89352 fatal errors'), which #555 gave ONE row (qhm88kstops, dev_mb89352.c:146).  SITES (c29a5fd3, src/devices/dev_mb89352.c): :169 (DREG read, phase outside DATAIN/STAT/MSGIN) and :235 (DREG write, phase outside DATAOUT/CMD).  :290 (the end-of-write default:) is UNREACHABLE: the first switch returns only for unsupported phases, and DATAOUT/CMD break, reach the second switch with no intervening phase change, and exhaust its supported cases.  PREREQUISITES: every DREG helper call needs a NONZERO count before decrement (a zero-count access only warns) and these guards additionally need a transfer object -- 'unconditional' means independent of the abort flag, nothing more.  REACHED BY (by reading, not measured): SCMD/PCTL give the guest control of the phase.  FIX SHAPE: keep the CPU running while KEEPING the helper's early return (:170 / :236) -- the treatment #186 gave the XFR command at :507.  PROVENANCE: agy's ifiled2_1 flag #27 (PARTLY) -> GPT-6 Astra's finding that the title carries one of nine `cpu->running = 0` assignments (regress/artifacts/idlessaudit_20261002/aconf_agyflags/codex_aconf_agyflags.txt) -> grok's ruling, CONCEDE IN PART, three rows (regress/artifacts/idlessaudit_20261002/grok/grok_mbstops.txt) -> Astra's confirmation (regress/artifacts/idlessaudit_20261002/aconf_mbstops/codex_aconf_mbstops.txt: CONFIRMED WITH CHANGES (3) -- correct reachability explanations, qualify carrier/title scope, and label evidence as source-only; retain three HIGH rows).  Severity HIGH by the qhm88kstops grade (a guest-drivable stop of the emulated CPU).  Reachability established by source inspection at c29a5fd3; no runtime witness measured -- the round that takes this row owes the rung-3 attempt.  NOT FIXED by #558.
5 | NEW  qhmbunimplstops | HIGH | An MB89352 access with a non-byte length, an unhandled SCMD write, or the EXBF register stops the emulated CPU while mb89352_abort_on_unimplemented_stuff is fixed true | note: FILED BY #558 from queue passage 2616 at db8b1a33 ('#12 m88k CMMU / dev_mb89352 fatal errors'), which #555 gave ONE row (qhm88kstops, dev_mb89352.c:146).  SITES (c29a5fd3, src/devices/dev_mb89352.c): :312 (len != 1: a halfword or word callback access), :533 (an SCMD WRITE outside {0x00, 0x20, 0x84, 0x8c, 0xc0} unless bit 0x10 rewrites it to BUS_REL -- an SCMD read does not execute this switch), and EXBF, register index 15: WRITE logging at :676 and READ logging at :683 converge on the ONE assignment at :690.  All gated by const bool mb89352_abort_on_unimplemented_stuff = true (:61), so live; the shared fixed-true policy is what groups them.  REACHED BY (by reading, not measured): those accesses from the guest's register interface.  FIX SHAPE: the warning branch the flag already selects; clearing the flag leaves all five live unconditional DREG assignments (:146, :169, :176, :235, :242; :290 is dead) intact.  NOT mb89352halt's stop: that dropped row's record names the disk dispatcher's CDB default: and the controller's status-length guard, not :533.  PROVENANCE: agy's ifiled2_1 flag #27 (PARTLY) -> GPT-6 Astra's finding that the title carries one of nine `cpu->running = 0` assignments (regress/artifacts/idlessaudit_20261002/aconf_agyflags/codex_aconf_agyflags.txt) -> grok's ruling, CONCEDE IN PART, three rows (regress/artifacts/idlessaudit_20261002/grok/grok_mbstops.txt) -> Astra's confirmation (regress/artifacts/idlessaudit_20261002/aconf_mbstops/codex_aconf_mbstops.txt: CONFIRMED WITH CHANGES (3) -- correct reachability explanations, qualify carrier/title scope, and label evidence as source-only; retain three HIGH rows).  Severity HIGH by the qhm88kstops grade (a guest-drivable stop of the emulated CPU).  Reachability established by source inspection at c29a5fd3; no runtime witness measured -- the round that takes this row owes the rung-3 attempt.  NOT FIXED by #558.
6 | NEW  qhmbbufendstops | HIGH | An MB89352 data-register access at or past the end of the selected buffer, in a phase supported for the access direction, stops the emulated CPU | note: FILED BY #558 from queue passage 2616 at db8b1a33 ('#12 m88k CMMU / dev_mb89352 fatal errors'), which #555 gave ONE row (qhm88kstops, dev_mb89352.c:146).  SITES (c29a5fd3, src/devices/dev_mb89352.c): :176 (DREG read, transfer_bufpos >= len against the selected DATAIN, STAT or MSGIN buffer -- read completion changes phase WITHOUT resetting the cursor, so a subsequent nonempty buffer can meet this guard, not only the original DATAIN buffer) and :242 (DREG write: reachable through empty or unprepared outgoing-buffer states; an exact fill runs completion and can change phase so a further write reaches :235 instead).  PREREQUISITES: a transfer object and a nonzero count, as for the phase guards (the count prerequisite applies to every DREG helper call; the :146 stop is the case with NO transfer object).  CARRIERS OF THE REST: b120 carries the unknown-CDB producer omission and its empty-status consequence; this row's residual is every OTHER empty-buffer path and every nonempty-buffer case.  FIX SHAPE: keep the bounds protection and refuse the access or handle phase completion -- removing the guard exposes the indexed accesses at :180 / :246 -- a CONTROLLER fix; b120 remains the PRODUCER fix.  PROVENANCE: agy's ifiled2_1 flag #27 (PARTLY) -> GPT-6 Astra's finding that the title carries one of nine `cpu->running = 0` assignments (regress/artifacts/idlessaudit_20261002/aconf_agyflags/codex_aconf_agyflags.txt) -> grok's ruling, CONCEDE IN PART, three rows (regress/artifacts/idlessaudit_20261002/grok/grok_mbstops.txt) -> Astra's confirmation (regress/artifacts/idlessaudit_20261002/aconf_mbstops/codex_aconf_mbstops.txt: CONFIRMED WITH CHANGES (3) -- correct reachability explanations, qualify carrier/title scope, and label evidence as source-only; retain three HIGH rows).  Severity HIGH by the qhm88kstops grade (a guest-drivable stop of the emulated CPU).  Reachability established by source inspection at c29a5fd3; no runtime witness measured -- the round that takes this row owes the rung-3 attempt.  NOT FIXED by #558.
7 | CHANGED  idlesslow | fields: entries | commits: '' -> ''
8 |     + entry: {"phase": "review", "seat": "agy", "date": "2026-10-02", "grade": "0 of 20 rows flagged, 0 not checked", "grader": "", "ev": "regress/artifacts/idlessaudit_20261002/icite2_1/agy_icite2_1.txt", "note": "#558 read-only audit of #555's table at c29a5fd3 (gemini-3.8-flash-high, brief regress/artifacts/idlessaudit_20261002/briefs/icite2_1.md; answer 4776 bytes): 0 flags.  agy's agreement carries no weight (owner, 2026-10-02); its flags were CHECKED against the committed table, not judged."}
9 |     + entry: {"phase": "review", "seat": "agy", "date": "2026-10-02", "grade": "WALLED (seat failure)", "grader": "", "ev": "regress/artifacts/idlessaudit_20261002/icite2_2/agy_icite2_2.err", "note": "#558 audit of #555's table, brief regress/artifacts/idlessaudit_20261002/briefs/icite2_2.md: the seat WALLED on launch (error: Individual quota reached. Please upgrade your subscription to increase your limits. Resets in 101h48m29s.; the .txt is 0 bytes, the .err is the whole answer).  The 20 rows it was to read (IDLESS_TABLE2.tsv rows 111-130, the ones agy's first set had not reached) are unaudited by agy; Astra's ifile_04 (128/128 rows) and ifile_05 passes read them before #555 shipped.  The runner was stopped rather than left asleep until the stated reset."}
10 |     + entry: {"phase": "review", "seat": "agy", "date": "2026-10-02", "grade": "4 of 35 passages flagged, 0 not checked", "grader": "", "ev": "regress/artifacts/idlessaudit_20261002/ifiled2_1/agy_ifiled2_1.txt", "note": "#558 read-only audit of #555's table at c29a5fd3 (gemini-3.8-flash-high, brief regress/artifacts/idlessaudit_20261002/briefs/ifiled2_1.md; answer 8872 bytes): 4 PARTLY flag(s) (items 15, 24, 26, 27): #15, #24 and #26 are carried by rows #555 filed on the same queue lines (qhscifssr, qhnetxlog, qhslowifetch), which the brief did not name; #27 is a real gap -- qhppciphack carries its PPC half, qhm88kstops one MB89352 assignment of nine, and three rows are filed for the residual (regress/artifacts/idlessaudit_20261002/AGY_FLAGS_DISPOSITION.md).  agy's agreement carries no weight (owner, 2026-10-02); its flags were CHECKED against the committed table, not judged."}
11 |     + entry: {"phase": "review", "seat": "agy", "date": "2026-10-02", "grade": "0 of 35 passages flagged, 0 not checked", "grader": "", "ev": "regress/artifacts/idlessaudit_20261002/ifiled2_2/agy_ifiled2_2.txt", "note": "#558 read-only audit of #555's table at c29a5fd3 (gemini-3.8-flash-high, brief regress/artifacts/idlessaudit_20261002/briefs/ifiled2_2.md; answer 8884 bytes): 0 flags.  agy's agreement carries no weight (owner, 2026-10-02); its flags were CHECKED against the committed table, not judged."}
12 |     + entry: {"phase": "review", "seat": "agy", "date": "2026-10-02", "grade": "1 of 34 passages flagged, 0 not checked", "grader": "", "ev": "regress/artifacts/idlessaudit_20261002/ifiled2_3/agy_ifiled2_3.txt", "note": "#558 read-only audit of #555's table at c29a5fd3 (gemini-3.8-flash-high, brief regress/artifacts/idlessaudit_20261002/briefs/ifiled2_3.md; answer 8595 bytes): 1 PARTLY flag(s) (items 28): #28 is carried by armcp15cp14exits, filed by #554 from queue lines 18721-18722 (not on #28's own lines 16997-17000), which the brief did not name (regress/artifacts/idlessaudit_20261002/AGY_FLAGS_DISPOSITION.md).  agy's agreement carries no weight (owner, 2026-10-02); its flags were CHECKED against the committed table, not judged."}
13 |     + entry: {"phase": "review", "seat": "agy", "date": "2026-10-02", "grade": "11 of 22 entries flagged, 0 not checked", "grader": "", "ev": "regress/artifacts/idlessaudit_20261002/ikeep2/agy_ikeep2.txt", "note": "#558 read-only audit of #555's table at c29a5fd3 (gemini-3.8-flash-high, brief regress/artifacts/idlessaudit_20261002/briefs/ikeep2.md; answer 6908 bytes): 11 OWED flag(s) (items 8-18): each recorded, in those words, in its LIVE carrier row's own queue text (armbfiwidth, mapledmaaddr, ppcrldimimask, xscaleinten); nothing owed by #555 (regress/artifacts/idlessaudit_20261002/AGY_FLAGS_DISPOSITION.md).  agy's agreement carries no weight (owner, 2026-10-02); its flags were CHECKED against the committed table, not judged."}
14 |     + entry: {"phase": "review", "seat": "codex", "date": "2026-10-02", "grade": "1 of 16 dispositions wrong", "grader": "", "ev": "regress/artifacts/idlessaudit_20261002/aconf_agyflags/codex_aconf_agyflags.txt", "note": "#558 GPT-6 Astra (codex, ultra) on the main loop's disposition of agy's 16 flags (brief regress/artifacts/idlessaudit_20261002/briefs/aconf_agyflags.md): asked which of the sixteen 'nothing owed' dispositions is wrong, per flag, against IDLESS_TABLE2.tsv and the ledger at c29a5fd3."}
15 |     + entry: {"phase": "review", "seat": "grok", "date": "2026-10-02", "grade": "CONCEDE IN PART -- :146 is qhm88kstops and b120 carries the empty-status reach of :176; rows are owed for the live stops those two leave unnamed", "grader": "", "ev": "regress/artifacts/idlessaudit_20261002/grok/grok_mbstops.txt", "note": "#558 grok (grok-4.7 xhigh, plan mode) RULING on Astra's finding about agy's flag ifiled2_1 #27 (brief regress/artifacts/idlessaudit_20261002/briefs/grok_mbstops.md): of dev_mb89352.c's nine cpu->running = 0 assignments (ten stop messages: EXBF's write and read share one), :146 is qhm88kstops, b120 carries the unknown-CDB producer omission and its empty-status consequence at :176, :290 is dead, and three rows are owed for the rest -- filed as qhmbphasestops, qhmbunimplstops, qhmbbufendstops."}
16 |     + entry: {"phase": "review", "seat": "codex", "date": "2026-10-02", "grade": "CONFIRMED WITH CHANGES (3) -- correct reachability explanations, qualify carrier/title scope, and label evidence as source-only; retain three HIGH rows", "grader": "", "ev": "regress/artifacts/idlessaudit_20261002/aconf_mbstops/codex_aconf_mbstops.txt", "note": "#558 GPT-6 Astra (codex, ultra) CONFIRMING grok's ruling against the source at c29a5fd3 (brief regress/artifacts/idlessaudit_20261002/briefs/aconf_mbstops.md): per site, the reaching path, the carriers, the partition into three rows and the HIGH grade."}
17 |     + entry: {"phase": "review", "seat": "fable5", "date": "2026-10-02", "grade": "", "grader": "", "ev": "regress/artifacts/idlessaudit_20261002/AGY_FLAGS_DISPOSITION.md", "note": "[NOT A SEAT ANSWER] #558 GXEMUL [087a90] (main loop): the disposition of agy's 16 flags (v3, after Astra's checks aconf_agyflags, aconf_558 and aconf_558b) -- 5 PARTLY: 4 carried by rows the brief had not named (qhscifssr, qhnetxlog, qhslowifetch filed by #555 on the same lines; armcp15cp14exits filed by #554), 1 (#27) WRONG IN PART per Astra -> grok's ruling -> three rows filed (qhmbphasestops, qhmbunimplstops, qhmbbufendstops); 11 OWED: each recorded in its live carrier's own queue text (armbfiwidth, mapledmaaddr, ppcrldimimask, xscaleinten), nothing owed by #555.  One defect in the brief generator (a passage with a pointer AND a new row was listed with the pointer alone), recorded and not re-run (agy walled until 2026-
18 | 

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GX558TEXTS: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
